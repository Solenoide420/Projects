#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

#include "grille.h"
#include "placement.h"

bool est_coule(uint8_t** grilleo, bool** bombep, uint8_t ligne, uint8_t colonne) {
    uint8_t num_bateau = grilleo[ligne][colonne];
    bool res = true;

    for (uint8_t i = 0; i < 10; i++) {
        for (uint8_t j = 0; j < 10; j++) {
            if ((grilleo[i][j] == num_bateau) && (!bombep[i][j])) {
                res = false;
            }
        }
    }
    return res;
}

bool joue_bombe(uint8_t** grillep, bool** bombep, uint8_t** grilleo, bool** bombeo, uint8_t joueur, char* coupprec, char* gage, uint32_t base) {
    int balec = 0; balec++;
    balec = system("clear");

    if (joueur == 0) {
        printf("\x1B[38;5;2mJoueur 1\x1B[0m\n\n");
    } else {
        printf("\x1B[38;5;13mJoueur 2\x1B[0m\n\n");
    }
    printf("L'adversaire a joué : %s\n\n", coupprec);

    uint8_t ligne = 0; uint8_t colonne = 0;
    while (true) {
        printf("Mes bateaux et les bombes lancées par l'adversaire\n");
        affiche_grille_perso(grillep, bombeo);
        printf("\n\nLa grille de l'adversaire et les bombardements alliés\n");
        affiche_grille_oppo(grilleo, bombep);
        printf("\nQuelle case bombarder ?\nEntrer la colonne et la ligne\nExemple : \'A3\'\n");

        char* input = malloc(3 * sizeof(char));
        lire(input, 3);

        if (input[0] >= 'a' && input[0] <= 'j') {
            input[0] = input[0] - 32;
        }
        colonne = input[0] - 65;
        ligne = input[1] - 48;

        if (colonne < 10 && ligne < 10) {
            if (verif_bombardement(bombep, ligne, colonne)) {
                coupprec[0] = input[0]; coupprec[1] = input[1];
                free(input);
                break;
            }
        }
        balec = system("clear");
        printf("Entrée \"%s\" invalide : réessayer\n\n", input);
        free(input);
    }
    bombep[ligne][colonne] = true;
    balec = system("clear");
    if (joueur == 0) {
        printf("\x1B[38;5;2mJoueur 1\x1B[0m\n\n");
    } else {
        printf("\x1B[38;5;13mJoueur 2\x1B[0m\n\n");
    }
    uint8_t res = 0;
    if (grilleo[ligne][colonne] != 0) {
        if (est_coule(grilleo, bombep, ligne, colonne)) {
            printf("Coulé\n\n");
            res = 1;
        } else {
            printf("Touché\n\n");
            res = 2;
        }
    } else {
        printf("Plouf !\n\n");
        res = 0;
    }
    affiche_grille_oppo(grilleo, bombep);

    if (base > 0) {
        if (res == 1) {
            printf("\nC'est coulé, c'est %u %ss pour l'adversaire", base+1, gage);
        } else if (res == 2) {
            printf("\nC'est touché, c'est %u %s%s pour l'adversaire", base, gage, (base > 1) ? "s" : "");
        }
    }

    int c = 0;
    while (c != '\n' && c != EOF)
    {
        c = getchar();
    }
    return res;
}
