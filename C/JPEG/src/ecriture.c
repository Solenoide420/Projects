#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>


void ecriture_PPM(const char* nom_fichier, uint8_t*** image, uint16_t largeur, uint16_t hauteur) {
	FILE *fichier = fopen(nom_fichier, "w");
	if (fichier == NULL) {
		perror("Impossible d'ouvrir le fichier donné");
		exit(EXIT_FAILURE);
	}

	fputs("P6\n", fichier);
	fprintf(fichier, "%u ", largeur);
	fprintf(fichier, "%u\n", hauteur);
	fputs("255\n", fichier);

    for (uint32_t i = 0; i < hauteur; i++) {
        for (uint32_t j = 0; j < largeur; j++) {
            fwrite(&(image[i][j][0]), sizeof(uint8_t), 1, fichier);  // Composante rouge
            fwrite(&(image[i][j][1]), sizeof(uint8_t), 1, fichier);  // Composante verte
            fwrite(&(image[i][j][2]), sizeof(uint8_t), 1, fichier);  // Composante bleue
        }
    }

    fclose(fichier);
}

void init_ecriture_PPM(FILE* fichier, uint16_t largeur, uint16_t hauteur) {
	fputs("P6\n", fichier);
	fprintf(fichier, "%u ", largeur);
	fprintf(fichier, "%u\n", hauteur);
	fputs("255\n", fichier);
}

void ajoute_PPM(FILE* fichier, uint8_t*** image, uint16_t largeur, uint16_t hauteur) {
	for (uint32_t i = 0; i < hauteur; i++) {
        for (uint32_t j = 0; j < largeur; j++) {
            fwrite(&(image[i][j][0]), sizeof(uint8_t), 1, fichier);  // Composante rouge
            fwrite(&(image[i][j][1]), sizeof(uint8_t), 1, fichier);  // Composante verte
            fwrite(&(image[i][j][2]), sizeof(uint8_t), 1, fichier);  // Composante bleue
        }
    }
}



void ecriture_PGM(char* nom_fichier, uint8_t** image, uint16_t largeur, uint16_t hauteur) {
	FILE *fichier = fopen(nom_fichier, "w");
	if (fichier == NULL) {
		perror("Impossible d'ouvrir le fichier donné");
		exit(EXIT_FAILURE);
	}

	fputs("P5\n", fichier);
	fprintf(fichier, "%u ", largeur);
	fprintf(fichier, "%u\n", hauteur);
	fputs("255\n", fichier);

    for (uint32_t i = 0; i < hauteur; i++) {
        for (uint32_t j = 0; j < largeur; j++) {
            fwrite(&(image[i][j]), sizeof(uint8_t), 1, fichier);  // Niveau de gris
        }
    }

    fclose(fichier);
}

void init_ecriture_PGM(FILE* fichier, uint16_t largeur, uint16_t hauteur) {
	fputs("P5\n", fichier);
	fprintf(fichier, "%u ", largeur);
	fprintf(fichier, "%u\n", hauteur);
	fputs("255\n", fichier);
}

void ajoute_PGM(FILE* fichier, uint8_t** image, uint16_t largeur, uint16_t hauteur) {
	for (uint32_t i = 0; i < hauteur; i++) {
        for (uint32_t j = 0; j < largeur; j++) {
            fwrite(&(image[i][j]), sizeof(uint8_t), 1, fichier);
        }
    }
}