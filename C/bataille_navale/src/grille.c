#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>


uint8_t** init_grille(void) {
    uint8_t** grille = malloc(10 * sizeof(uint8_t*));

    for (uint8_t i = 0; i < 10; i++) {
        grille[i] = malloc(10 * sizeof(uint8_t));

        for (uint8_t j = 0; j < 10; j++) {
            grille[i][j] = 0;
        }
    }
    return grille;
}

bool** init_bombardes(void) {
    bool** bombes = malloc(10 * sizeof(bool*));

    for (uint8_t i = 0; i < 10; i++) {
        bombes[i] = malloc(10 * sizeof(bool));

        for (uint8_t j = 0; j < 10; j++) {
            bombes[i][j] = false;
        }
    }
    return bombes;
}

void affiche_grille_depart(uint8_t** grille) {
    char* mem = " 0&$%#";
    printf("    A B C D E F G H I J\n");
    printf("   +--------------------+\n");
    for (uint8_t i = 0; i < 10; i++) {
        printf("%i  |", i);
        for (uint8_t j = 0; j < 10; j++) {
            if (grille[i][j] == 0) {
                printf("\x1B[48;5;4m  ");
            } else {
                printf("\x1B[48;5;4m\x1B[38;5;0m%c%c", mem[grille[i][j]], mem[grille[i][j]]);
            }
        }
        printf("\x1B[0m|\n");
    }
    printf("   +--------------------+\n");
}

void affiche_grille_perso(uint8_t** grille, bool** bombardes) {
    char* mem = " 0&$%#";
    printf("    A B C D E F G H I J\n");
    printf("   +--------------------+\n");
    for (uint8_t i = 0; i < 10; i++) {
        printf("%i  |", i);
        for (uint8_t j = 0; j < 10; j++) {
            if ((grille[i][j] == 0) && !(bombardes[i][j])) {
                printf("\x1B[48;5;4m  ");
            } else if ((grille[i][j] != 0) && !(bombardes[i][j])) {
                printf("\x1B[48;5;4m\x1B[38;5;0m%c%c", mem[grille[i][j]], mem[grille[i][j]]);
            } else if ((grille[i][j] == 0) && bombardes[i][j]) {
                printf("\x1B[48;5;1m  ");
            } else {
                printf("\x1B[48;5;1m\x1B[38;5;0m@@");
            }
        }
        printf("\x1B[0m|\n");
    }
    printf("   +--------------------+\n");
}

void affiche_grille_oppo(uint8_t** grille, bool** bombardes) {
    printf("    A B C D E F G H I J\n");
    printf("   +--------------------+\n");
    for (uint8_t i = 0; i < 10; i++) {
        printf("%i  |", i);
        for (uint8_t j = 0; j < 10; j++) {
            if (bombardes[i][j]) {
                if (grille[i][j] != 0) {
                    printf("\x1B[48;5;1m\x1B[38;5;0m@@");
                } else {
                    printf("\x1B[48;5;1m  ");
                }
            } else {
                printf("\x1B[48;5;4m  ");
            }
        }
        printf("\x1B[0m|\n");
    }
    printf("   +--------------------+\n");
}

bool verif_placement(uint8_t** grille, uint8_t ligne, uint8_t colonne, bool horizontal, uint8_t taille) {
    if (horizontal) {
        for (uint8_t i = 0; i < taille; i++) {
            if (colonne+i > 9 || (grille[ligne][colonne+i] != 0)) {
                return false;
            }
        }
    } else {
        for (uint8_t i = 0; i < taille; i++) {
            if (ligne+i > 9 || (grille[ligne+i][colonne] != 0)) {
                return false;
            }
        }
    }
    return true;
}

bool verif_bombardement(bool** bombardes, uint8_t ligne, uint8_t colonne) {
    return !bombardes[ligne][colonne];
}

void free_grille(bool** grille) {
    for (uint8_t i = 0; i < 10; i++) {
        free(grille[i]);
    }
    free(grille);
}

void free_bombes(bool** bombes) {
    for (uint8_t i = 0; i < 10; i++) {
        free(bombes[i]);
    }
    free(bombes);
}

void attendre_prochain(uint8_t joueursuiv) {
    int balec = 0; balec++;
    balec = system("clear");
    printf("C'est au tour du suivant, c'est à dire ");
    if (joueursuiv == 0) {
        printf("\x1B[38;5;2mJoueur 1\x1B[0m\n\n");
    } else {
        printf("\x1B[38;5;13mJoueur 2\x1B[0m\n\n");
    }
    printf("Aller aller, on fait passer le PC\n\n");
    printf("C'est bon ?\n\nBon ben entrée pour pouvoir jouer alors\n\n");

    int c = 0;
    while (c != '\n' && c != EOF)
    {
        c = getchar();
    }
}