#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

#include "grille.h"
#include "placement.h"
#include "bataille.h"
#include "game.h"



int game(char* gage, uint32_t base) {
    char* mem = malloc(3 * sizeof(char));
    mem[0] = (char) '-'; mem[1] = (char) '-'; mem[2] = (char) 0;
    bool res = true; res = !res;

    /* INITIALISATION */
    uint8_t** bateau1 = init_grille();
    uint8_t** bateau2 = init_grille();
    bool** bombes1 = init_bombardes();
    bool** bombes2 = init_bombardes();
    uint8_t touche1 = 0; uint8_t touche2 = 0;
    uint8_t tour = 0;

    /* PHASE 1 : PLACEMENT DES BATEAUX */
    attendre_prochain(0);
    place_bateaux(bateau1, 0);
    attendre_prochain(1);
    place_bateaux(bateau2, 1);

    /* PHASE 2 : BATAILLE */
    while (touche1 < 17 && touche2 < 17) {
        if (tour == 0) {
            attendre_prochain(0);
            res = joue_bombe(bateau1, bombes1, bateau2, bombes2, 0, mem, gage, base);
            if (res) {
                touche1++;
            }       
        } else {
            attendre_prochain(1);
            res = joue_bombe(bateau2, bombes2, bateau1, bombes1, 1, mem, gage, base);
            if (res) {
                touche2++;
            }  
        }
        tour = (tour+1) %2;
    }

    /* PHASE 3 : VICTOIRE */
    if (touche1 == 17) {
        victoire(bateau1, bombes1, bateau2, bombes2, 0, gage, base, 17 - touche2);
    } else {
        victoire(bateau2, bombes2, bateau1, bombes1, 1, gage, base, 17 - touche1);
    }

    /* Libération de la mémoire */
    tour = system("clear");
    free_grille(bateau1);
    free_grille(bateau2);
    free_bombes(bombes1);
    free_bombes(bombes2);
    free(mem);

    return EXIT_SUCCESS;
}

void victoire(uint8_t** bateauv, bool** bombesv, uint8_t** bateaup, bool** bombesp, uint8_t joueur, char* gage, uint32_t base, uint8_t reste) {
    int balec = 0; balec++;
    balec = system("clear");
    printf("Victoire de ");
    if (joueur == 0) {
        printf("\x1B[38;5;2mJoueur 1\x1B[0m\n");
        printf("Du coup, le \x1B[38;5;13mJoueur 2\x1B[0m reçoit %u %ss, c'est cadeau\n", base*2, gage);
    } else {
        printf("\x1B[38;5;13mJoueur 1\x1B[0m\n\n");
        printf("Du coup, le \x1B[38;5;2mJoueur 2\x1B[0m reçoit %u %ss, c'est cadeau\n", base*2, gage);
    }
    printf("Et en plus, il récupère ceux que l'adversaire n'a pas à faire,");
    printf("c'est pas cool ça ? (aller les %u %s%s)\n\n", reste, gage, (reste > 1) ? "s" : "");
    printf("Grille du gagnant\n");
    affiche_grille_perso(bateauv, bombesp);
    printf("\nGrille du perdant\n");
    affiche_grille_perso(bateaup, bombesv);
    printf("\n\n");
    printf("@@@@@@@@@@@     @@@@@@@@@@@         @@@@@.    @@@@       @@@@    /@@@@@@@@@.\n");
    printf("@@@@    @@@@    @@@@    @@@@       @@@@@@@     @@@@     (@@@/  @@@@@     @@@@@ \n");
    printf("@@@@@@@@@@@#    @@@@    @@@@      @@@@ .@@@     @@@@    @@@@  (@@@@       @@@@ \n");
    printf("@@@@@@@@@@@@    @@@@@@@@@@       @@@@   @@@@     @@@@  @@@@   @@@@@       @@@@,\n");
    printf("@@@@     @@@@   @@@@    @@@@    @@@@@@@@@@@@@     @@@,@@@@     @@@@       @@@@ \n");
    printf("@@@@@@@@@@@@    @@@@     @@@@  @@@@       @@@@    /@@@@@@       &@@@@@@@@@@@. \n");
    printf("\n");

    int c = 0;
    while (c != '\n' && c != EOF)
    {
        c = getchar();
    }


}