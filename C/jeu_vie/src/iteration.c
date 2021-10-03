#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


bool** iteration_grille(bool** grille, uint8_t largeur, uint8_t hauteur)  {
    bool** suivante = malloc(hauteur * sizeof(bool*));

    for (uint8_t i = 0; i < hauteur; i++) {
        suivante[i] = malloc(largeur * sizeof(bool));

        for (uint8_t j = 0; j < largeur; j++) {
            if ((j == 0) || (i == 0) || (i == hauteur-1) || (j == largeur-1)) {
                suivante[i][j] = 0;
            } else {
                uint8_t autour = 0;
                for (uint8_t di = 0; di < 3; di++) {
                    for (uint8_t dj = 0; dj < 3; dj++) {
                        autour += grille[i + di-1][j + dj-1];
                    }
                }
                autour -= grille[i][j];
                suivante[i][j] = ((autour == 3) || ((autour == 2) && (grille[i][j])));
            }
        }
        if (i > 0) {
            free(grille[i-1]);
        }
    }
    free(grille[hauteur-1]);
    free(grille);
    return suivante;
}