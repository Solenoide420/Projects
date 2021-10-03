#ifndef __ECRITURE_H__
#define __ECRITURE_H__

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

/*
Gère l'écriture du fichier ppm (pour les images en couleur donc) à partir de son nom, et d'une matrice contenant 
la liste des composantes RGB pour chaque pixel
*/
void ecriture_PPM(const char* nom_fichier, uint8_t*** image, uint16_t largeur, uint16_t hauteur);

/*
Gère l'écriture du fichier pgm (pour les images en noir-blanc donc) à partir de son nom, et d'une matrice contenant 
la composante grise pour chaque pixel
*/
void ecriture_PGM(const char* nom_fichier, uint8_t** image, uint16_t largeur, uint16_t hauteur);

/*
Décomposition pour l'écriture ligne par ligne
*/
void init_ecriture_PPM(FILE* fichier, uint16_t largeur, uint16_t hauteur);
void ajoute_PPM(FILE* fichier, uint8_t*** image, uint16_t largeur, uint16_t hauteur);

void init_ecriture_PGM(FILE* fichier, uint16_t largeur, uint16_t hauteur);
void ajoute_PGM(FILE* fichier, uint8_t** image, uint16_t largeur, uint16_t hauteur);


#endif