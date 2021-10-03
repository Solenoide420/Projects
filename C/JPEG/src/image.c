#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

#include "jpeg_reader.h"
#include "bitstream.h"
#include "huffman.h"

#include "extraction.h"
#include "quantif_inv.h"
#include "izig_zag.h"
#include "idct_rapide.h"
#include "conversion.h"
#include "ecriture.h"

char* nom_final(const char* filename, bool est_pgm) {
    uint8_t n = strlen(filename);
    char* res = malloc((n+1) * sizeof(char));

    uint8_t i = 0;
    while ((i < n) && (filename[i] != '.')) {
        res[i] = filename[i];
        i++;
    }
    res[i] = '.';
    res[i+1] = 'p';
    res[i+2] = (est_pgm) ? 'g' : 'p';
    res[i+3] = 'm';
    res[i+4] = '\0';

    return res;
}

uint8_t indice(uint8_t i, uint8_t j, uint8_t nb_lig, uint8_t nb_col) {
    if (((nb_lig == 1) && (nb_col == 1)) || ((i < 8) && (j < 8))) {
        return 0;
    } else if ((nb_col == 2) && (i < 8)) {
        return 1;
    } else if ((nb_lig == 2) && (nb_col == 1)) {
        return 1;
    } else if (j < 8) {
        return 2;
    } else {
        return 3;
    }
}

int mainNB(const char* filename, struct jpeg_desc* jdesc)
{
    printf("\n\nC'est une image en N&B, on est parti !\n");
    /* On recupere le flux des donnees brutes a partir du descripteur. */
    struct bitstream *stream = jpeg_get_bitstream(jdesc);



    /* On recupère les infos importantes sur l'image */
    uint16_t hauteur = jpeg_get_image_size(jdesc, V);
    uint16_t largeur = jpeg_get_image_size(jdesc, H);
    uint16_t nb_blocs_haut = (hauteur % 8 == 0) ? hauteur / 8 : hauteur / 8 +1;
    uint16_t nb_blocs_larg = (largeur % 8 == 0) ? largeur / 8 : largeur / 8 +1;
    uint32_t nb_blocs = nb_blocs_haut * nb_blocs_larg;
    char* new_filename = nom_final(filename, true);

    /* On initialise l'image finale */
    printf("La matrice finale...\n");
    uint8_t** imagePGM = malloc(8 * sizeof(uint8_t*));
    for (uint16_t i = 0; i < 8; i++) {
        imagePGM[i] = malloc(largeur * sizeof(uint8_t));
    }

    /* On charge les tables de Huffman */
    printf("Les tables de Huffman...\n");
    uint8_t nb_huff_ac = jpeg_get_nb_huffman_tables(jdesc, AC);
    struct huff_table** huff_tables_ac = malloc(nb_huff_ac * sizeof(struct huff_table*));
    for (uint8_t i = 0; i < nb_huff_ac; i++) {
        huff_tables_ac[i] = jpeg_get_huffman_table(jdesc, AC, i);
    }

    uint8_t nb_huff_dc = jpeg_get_nb_huffman_tables(jdesc, DC);
    struct huff_table** huff_tables_dc = malloc(nb_huff_dc * sizeof(struct huff_table*));
    for (uint8_t i = 0; i < nb_huff_dc; i++) {
        huff_tables_dc[i] = jpeg_get_huffman_table(jdesc, DC, i);
    }

    /* On charge les blocs de quantification */
    printf("Les tables de quantification...\n");
    uint8_t nb_tables_quant = jpeg_get_nb_quantization_tables(jdesc);
    uint8_t** tables_quant = malloc(nb_tables_quant * sizeof(uint8_t*));
    for (uint8_t i = 0; i < nb_tables_quant; i++) {
        tables_quant[i] = jpeg_get_quantization_table(jdesc, i);
        for ( uint8_t j = 0; j < 64; j++ ) {
        }
    }

    /* Puis on extrait les blocs */

    // Préparation
    int16_t DC_prec = 0;

    // Pour éviter d'allouer à chaque boucle
    int16_t* bloc = malloc(64 * sizeof(int16_t));
    int16_t** zigzaged = malloc(8 * sizeof(int16_t*));
    uint8_t** final_bloc = malloc(8 * sizeof(uint8_t*));
    for (uint8_t i = 0; i < 8; i++) {
        zigzaged[i] = malloc(8 * sizeof(int16_t));
        final_bloc[i] = malloc(8 * sizeof(uint8_t));
    }

    printf("Ouverture du fichier...\t\t\t\t\t.                                                   .\n");
    FILE *fichier = fopen(new_filename, "w");
	if (fichier == NULL) {
		perror("Impossible d'ouvrir le fichier donné");
		exit(EXIT_FAILURE);
	}
    init_ecriture_PGM(fichier, largeur, hauteur);

    float avancement = 0;
    float d_avancement = (float) nb_blocs / (float) 50.0;
    uint8_t printed = 0;

    printf("Extraction et sauvegarde des blocs...\t\t\t|");
    for (uint32_t k = 0; k < nb_blocs; k++) {
        avancement += 1;
        if (((int) avancement > printed * d_avancement)) {
            printf("@");
            printed++;
            fflush(stdout);
        }

        /* On extrait le bloc brut */
        extraction_bloc(huff_tables_ac, huff_tables_dc, stream, jdesc, jpeg_get_frame_component_id(jdesc, 1), bloc);
        bloc[0] += DC_prec;
        DC_prec = bloc[0];

        /* On effectue la quatification inverse */
        quantification_inverse(bloc, tables_quant[0]);

        /* On zigzag le bloc */
        inverse_zigzag(zigzaged, bloc);

        /* iDCT (passage fréquentiel to spatial) */
        iDCT_AAN(final_bloc, zigzaged);

        /* et on le sauvegarde dans l'image */
        uint16_t i_base = 8 * (k / nb_blocs_larg);
        uint16_t j_base = 8 * (k % nb_blocs_larg);

        if ((j_base == 0) && (i_base != 0)) {
            ajoute_PGM(fichier, imagePGM, largeur, 8);
        }

        for (uint8_t i = 0; i < 8; i++) {
            for (uint8_t j = 0; j < 8; j++) {
                if ((i_base + i < hauteur) && (j_base + j < largeur)) {
                    imagePGM[i][j_base + j] = final_bloc[i][j];
                }
            }
        }
    }

    ajoute_PGM(fichier, imagePGM, largeur, (hauteur % 8 == 0) ? 8 : hauteur % 8);
    fclose(fichier);

    /* Nettoyage de printemps : close_jpeg ferme aussi le bitstream
     * (voir Annexe C du sujet). */
    printf("@|\nLibération de la mémoire...\n\n");

    jpeg_close(jdesc);
    free(new_filename);
    free(huff_tables_ac);
    free(huff_tables_dc);
    free(tables_quant);
    free(bloc);

    for (uint8_t i = 0; i < 8; i++) {
        free(zigzaged[i]);
        free(final_bloc[i]);
    }
    for (uint16_t i = 0; i < 8; i++) {
        free(imagePGM[i]);
    }

    free(zigzaged);
    free(final_bloc);
    free(imagePGM);

    /* On se congratule. */
    printf("L'image est décodée, la nostalgie vous attend !\n");
    return EXIT_SUCCESS;
}


int mainCOLORE(const char* filename, struct jpeg_desc* jdesc)
{
    printf("\n\nC'est une image en COULEURS, on est parti !\n");
    /* On recupere le flux des donnees brutes a partir du descripteur. */
    struct bitstream *stream = jpeg_get_bitstream(jdesc);

    /* On recupère les infos importantes sur l'image */
    uint16_t hauteur = jpeg_get_image_size(jdesc, V);
    uint16_t largeur = jpeg_get_image_size(jdesc, H);

    uint16_t nb_blocs_haut = (hauteur % 8 == 0) ? hauteur / 8 : hauteur / 8 +1;
    uint16_t nb_blocs_larg = (largeur % 8 == 0) ? largeur / 8 : largeur / 8 +1;

    char* new_filename = nom_final(filename, false);

    uint8_t nb_col = jpeg_get_frame_component_sampling_factor(jdesc, H, 1);
    uint8_t nb_lig = jpeg_get_frame_component_sampling_factor(jdesc, V, 1);
    uint16_t nb_bloc_MCU = 2+ nb_lig * nb_col;

    uint32_t nb_iter = ((nb_lig > 1) ? (nb_blocs_haut+1)/nb_lig : nb_blocs_haut) * ((nb_col > 1) ? (nb_blocs_larg+1)/nb_col : nb_blocs_larg);

    /* On initialise l'image finale */
    printf("Le tenseur tampon...\n");
    uint8_t*** imagePPM = malloc(nb_lig * 8 * sizeof(uint8_t**));
    for (uint16_t i = 0; i < nb_lig * 8; i++) {
        imagePPM[i] = malloc(largeur * sizeof(uint8_t*));
    }

    /* On charge les tables de Huffman */
    printf("Les tables de Huffman...\n");
    uint8_t nb_huff_ac = jpeg_get_nb_huffman_tables(jdesc, AC);
    struct huff_table** huff_tables_ac = malloc(nb_huff_ac * sizeof(struct huff_table*));
    for (uint8_t i = 0; i < nb_huff_ac; i++) {
        huff_tables_ac[i] = jpeg_get_huffman_table(jdesc, AC, i);
    }

    uint8_t nb_huff_dc = jpeg_get_nb_huffman_tables(jdesc, DC);
    struct huff_table** huff_tables_dc = malloc(nb_huff_dc * sizeof(struct huff_table*));
    for (uint8_t i = 0; i < nb_huff_dc; i++) {
        huff_tables_dc[i] = jpeg_get_huffman_table(jdesc, DC, i);
    }

    /* On charge les blocs de quantification */
    printf("Les tables de quantification...\n");
    uint8_t nb_tables_quant = jpeg_get_nb_quantization_tables(jdesc);
    uint8_t** tables_quant = malloc(nb_tables_quant * sizeof(uint8_t*));
    for (uint8_t i = 0; i < nb_tables_quant; i++) {
        tables_quant[i] = jpeg_get_quantization_table(jdesc, i);
    }

    /* Puis on extrait les blocs */

    // Préparation
    int16_t* DC_prec = malloc(3 * sizeof(int16_t));
    DC_prec[0] = 0; DC_prec[1] = 0; DC_prec[2] = 0;

    // Pour éviter d'allouer à chaque boucle
    int16_t* bloc = malloc(64 * sizeof(int16_t));
    int16_t** zigzaged = malloc(8 * sizeof(int16_t*));
    for (uint8_t i = 0; i < 8; i++) {
        zigzaged[i] = malloc(8 * sizeof(int16_t));
    }
    uint8_t*** MCU = malloc(nb_bloc_MCU * sizeof(uint8_t**));
    for (uint8_t i = 0; i < nb_bloc_MCU; i++) {
        MCU[i] = malloc(8 * sizeof(uint8_t*));
    }
    for (uint8_t k = 0; k < 8; k++) {
        for (uint8_t i = 0; i < nb_bloc_MCU; i++) {
            MCU[i][k] = malloc(8 * sizeof(uint8_t));
        }
    }

    printf("Ouverture du fichier...\t\t\t\t\t.                                                   .\n");
    FILE *fichier = fopen(new_filename, "w");
	if (fichier == NULL) {
		perror("Impossible d'ouvrir le fichier donné");
		exit(EXIT_FAILURE);
	}
    init_ecriture_PPM(fichier, largeur, hauteur);

    const float* cos_tab = get_cos_tab();

    printf("Extraction, upsampling et sauvegarde des blocs...\t|");
    float avancement = 0;
    float d_avancement = (float) nb_iter / (float) 50.0;
    uint8_t printed = 0;

    for (uint32_t k = 0; k < nb_iter; k++) {
        // Pour aider à comprendre où on en est...
        avancement += 1;
        if (((int) avancement > printed * d_avancement)) {
            printf("@");
            printed++;
            fflush(stdout);
        }

        // On extrait les blocs Y puis Cr puis Cb
        for (uint8_t i = 0; i < nb_bloc_MCU; i++) {
            uint8_t ind = (i < nb_lig * nb_col) ? 0 : (i+1 - nb_lig * nb_col);
            extraction_bloc(huff_tables_ac, huff_tables_dc, stream, jdesc, jpeg_get_frame_component_id(jdesc, ind+1), bloc);
            bloc[0] += DC_prec[ind];
            DC_prec[ind] = bloc[0];
            quantification_inverse(bloc, tables_quant[jpeg_get_frame_component_quant_index(jdesc, ind+1)]);
            inverse_zigzag(zigzaged, bloc);
            iDCT_plus_rapide(MCU[i], zigzaged, cos_tab);
        }

        // L'upsampling est fait dans la sauvegarde

        /* Conversion et sauvegarde dans l'image */
        uint16_t i_base = 8 * nb_lig * (k / ((nb_blocs_larg+((nb_col > 1) ? 1 : 0)) / nb_col));
        uint16_t j_base = 8 * nb_col * (k % ((nb_blocs_larg+((nb_col > 1) ? 1 : 0)) / nb_col));

        if ((j_base == 0) && (i_base != 0)) {
            ajoute_PPM(fichier, imagePPM, largeur, nb_lig*8);
        }

        for (uint8_t i = 0; i < 8 * nb_lig; i++) {
            for (uint8_t j = 0; j < 8 * nb_col; j++) {
                if ((i_base + i < hauteur) && (j_base + j < largeur)) {
                    if (i_base != 0) {
                        free(imagePPM[i][j_base + j]);
                    }
                    imagePPM[i][j_base + j] = YCbCr_RGB(MCU[indice(i, j, nb_lig, nb_col)][i %8][j %8], MCU[nb_lig*nb_col][i/nb_lig][j/nb_col], MCU[nb_lig*nb_col +1][i/nb_lig][j/nb_col]);
                }
            }
        }
    }

    ajoute_PPM(fichier, imagePPM, largeur, (hauteur % (nb_lig*8) == 0) ? (nb_lig*8) : hauteur % (nb_lig*8));
    fclose(fichier);

    /* Nettoyage de printemps : close_jpeg ferme aussi le bitstream
     * (voir Annexe C du sujet). */
    printf("@|\nLibération de la mémoire...\n");
    jpeg_close(jdesc);

    free(new_filename);
    free(huff_tables_ac);
    free(huff_tables_dc);
    free(tables_quant);
    free(bloc);
    free(DC_prec);

    for (uint8_t i = 0; i < 8; i++) {
        free(zigzaged[i]);
    }
    for (uint8_t i = 0; i < nb_bloc_MCU; i++) {
        for (uint8_t j = 0; j < 8; j++) {
            free(MCU[i][j]);
        }
        free(MCU[i]);
    }
    for (uint16_t i = 0; i < 8 * nb_lig; i++) {
        for (uint16_t j = 0; j < largeur; j++) {
            free(imagePPM[i][j]);
        }
        free(imagePPM[i]);
    }

    free(zigzaged);
    free(MCU);
    free(imagePPM);

    /* On se congratule. */
    printf("L'image est décodée, profitez bien de ses magnifiques pixels RBG !\n\n");
    return EXIT_SUCCESS;
}



int main(int argc, char **argv) {
    printf("Lancement de Décodeur3000...\n");

    printf("%x", 0xFFFFFFFF & EOF);

    if (argc < 2) {
	/* Si y'a pas au moins un argument en ligne de commandes, on
	 * boude. */
	    fprintf(stderr, "Usage: %s fichier.jpeg\n", argv[0]);
	    return EXIT_FAILURE;
    }

    for (uint8_t i = 1; i < argc; i++) {
        /* On recupere le nom du fichier JPEG sur la ligne de commande. */
        const char *filename = argv[i];
        printf("\n\nOn s'occupe de %s (%u/%u)\n", filename, i, argc-1);

        /* On cree un jpeg_desc qui permettra de lire ce fichier. */
        printf("\nLecture de l'entête...\n");
        struct jpeg_desc *jdesc = jpeg_read(filename);

        uint8_t nb_couleurs = jpeg_get_nb_components(jdesc);

        uint8_t cont = EXIT_SUCCESS;

        if (nb_couleurs == 1) {
            cont = mainNB(filename, jdesc);
        } else if (nb_couleurs == 3) {
            cont = mainCOLORE(filename, jdesc);
        } else {
            fprintf(stderr, "Nombre de composantes de couleur inadéquat\n");
            return EXIT_FAILURE;
        }

        if (cont == EXIT_FAILURE) {
            return EXIT_FAILURE;
        }
    }

    printf("Merci d'avoir utilisé Décodeur3000 ! A bientôt ;)\n\n");
    return EXIT_SUCCESS;
}
