#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "grille.h"


void viderBuffer(void)
{
    int c = 0;
    while (c != '\n' && c != EOF)
    {
        c = getchar();
    }
}
 
int lire(char *chaine, int longueur)
{
    char *positionEntree = NULL;
 
    if (fgets(chaine, longueur, stdin) != NULL)
    {
        positionEntree = strchr(chaine, '\n');
        if (positionEntree != NULL)
        {
            *positionEntree = '\0';
        }
        else
        {
            viderBuffer();
        }
        return 1;
    }
    else
    {
        viderBuffer();
        return 0;
    }
}

void bateau(uint8_t** grille, uint8_t ligne, uint8_t colonne, bool horizontal,uint8_t taille, uint8_t bateau) {
    if (horizontal) {
        for (uint8_t i = 0; i < taille; i++) {
            grille[ligne][colonne+i] = bateau;
        }
    } else {
        for (uint8_t i = 0; i < taille; i++) {
            grille[ligne+i][colonne] = bateau;
        }
    }
}

void place_bateaux(uint8_t** grille, uint8_t joueur) {
    uint8_t a_placer[5] = {2, 3, 3, 4, 5};
    int ignore = 0; ignore++;

    for (uint8_t i = 0; i < 5; i++) {
        uint8_t ligne = 0; uint8_t colonne = 0;
        bool horizontal = false;
        ignore = system("clear");

        while (true) {
            if (joueur == 0) {
                printf("\x1B[38;5;2mJoueur 1\x1B[0m\n\n");
            } else {
                printf("\x1B[38;5;13mJoueur 2\x1B[0m\n\n");
            }
            affiche_grille_depart(grille);
            printf("\n\nOù placer le bâteau de taille %d ?\n", a_placer[i]);
            printf("Indiquer la case qui sera en haut à droite du bâteau, puis H/V pour le placer verticalement ou horizontalement\n");
            printf("Exemple : \'B4V\' pour un bâteau de taille 3 le placera sur les cases B4 - B5 - B6\n");

            char* input = malloc(4 * sizeof(char));
            lire(input, 4);

            if (input[0] >= 'a' && input[0] <= 'j') {
                input[0] = input[0] - 32;
            }
            colonne = input[0] - 65;
            ligne = input[1] - 48;

            if (input[2] >= 'a' && input[2] <= 'z') {
                input[2] = input[2] - 32;
            }
            input[2] = input[2];
            
            if (colonne < 10 && ligne < 10 && (input[2] == 'H' || input[2] == 'V')) {
                horizontal = input[2] == 'H';
                if (verif_placement(grille, ligne, colonne, horizontal, a_placer[i])) {
                    free(input);
                    break;
                }
            }
            ignore = system("clear");
            printf("Entrée %s invalide : réessayer\n\n", input);
            free(input);
        }
        bateau(grille, ligne, colonne, horizontal, a_placer[i], i+1);
    }
    ignore = system("clear");

    if (joueur == 0) {
        printf("\x1B[38;5;2mJoueur 1\x1B[0m\n\n");
    } else {
        printf("\x1B[38;5;13mJoueur 2\x1B[0m\n\n");
    }
    affiche_grille_depart(grille);
    printf("\nDonc voilà ta grille du coup, noice\n\n");
    printf("Entrée pour passer à la suite");
    int c = 0;
    while (c != '\n' && c != EOF)
    {
        c = getchar();
    }
}