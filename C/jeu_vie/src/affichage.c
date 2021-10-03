#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

/* L'écran maximal en affichage console est de 44 x 84 (= 168/2) */


void affiche_grille(bool** grille, uint8_t largeur, uint8_t hauteur) {
    /* La grille est de taille 6+hauteur x 6+largeur (3 de plus dans les 4 directions) */
    system("clear");

    for (uint8_t i = 3; i < hauteur-3; i++) {
        for (uint8_t j = 3; j < largeur-3; j++) {
            if (grille[i][j]) {
                printf("\x1B[48;5;15m  ");
            } else {
                printf("\x1B[48;5;0m  ");
            }
        }
        if (i != hauteur -4) {
            printf("\x1B[48;5;0m\n");
        } else {
            printf("\x1B[48;5;0m");
        }
    }
}