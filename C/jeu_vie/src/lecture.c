#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>


bool** lecture_vie(const char* filename, uint8_t h_ecran, uint8_t l_ecran) {
    FILE* fichier = fopen(filename, "r");

    uint8_t hauteur, largeur;

    fscanf(fichier, "%hhu %hhu\n", &hauteur, &largeur);
    if ((hauteur > h_ecran) || (largeur > l_ecran)) {
        fprintf(stderr, "Taille de l'écran et de structure de base incompatibles\n(%u # %u || %u # %u)\n\n",
        hauteur, h_ecran, largeur, l_ecran);
        exit(3);
    }

    bool** grille = malloc(h_ecran * sizeof(bool*));

    for (uint8_t i = 0; i < h_ecran; i++) {
        grille[i] = malloc(l_ecran * sizeof(bool));

        for (uint8_t j = 0; j < l_ecran; j++) {
            if ((2*j < l_ecran - largeur) || (2*i < h_ecran - hauteur) || (2*j >= l_ecran + largeur) || (2*i >= h_ecran + hauteur)) {
                grille[i][j] = (bool) 0;
            } else {
                char actu = fgetc(fichier);
                if (actu == ',') {
                    grille[i][j] = (bool) 0;
                } else if (actu == 'x') {
                    grille[i][j] = (bool) 1;
                } else {
                    fprintf(stderr, "Lecture invalide dans le fichier\n");
                    printf("%u %u _%c_", i, j, actu);
                    exit(4);
                }
            }
        }
        fscanf(fichier, "\n");
    }
    fclose(fichier);
    return grille;
}
