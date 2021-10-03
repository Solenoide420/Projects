#define _DEFAULT_SOURCE

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

#include "affichage.h"
#include "iteration.h"
#include "lecture.h"


int main(int argc, char** argv) {
    if (argc != 5) {
        fprintf(stderr, "Entrée en commande incorrecte...\n");
        printf("Utilisation : %s nom_fichier hauteur largeur iter", argv[0]);
        printf("\n\t- le nom de la structure de base\n\t- taille de l'écran (2 paramètres)\n\t- le nombre d'itérations\n\n");
        exit(1);
    }

    uint8_t hauteur = (uint8_t) atoi(argv[2]) + 6;
    uint8_t largeur = (uint8_t) atoi(argv[3]) + 6;
    uint64_t max_iter = (uint64_t) atoi(argv[4]);

    if ((largeur > 90) || (hauteur > 50)) {
        fprintf(stderr, "Taille d'écran trop grande (maximum 44 x 84)\n\n");
        exit(2);
    }

    bool** grille = lecture_vie(argv[1], hauteur, largeur);

    affiche_grille(grille, largeur, hauteur);
    fflush(stdout);
    usleep(250000);

    for (uint64_t k = 0; k < max_iter; k++) {        
        grille = iteration_grille(grille, largeur, hauteur);
        affiche_grille(grille, largeur, hauteur); 
        fflush(stdout); 
        usleep(250000);
    }
      
    printf("\x1B[48;5;0m\n\n");

    for (uint8_t i = 0; i < hauteur; i++) {
        free(grille[i]);
    }
    free(grille);

    return EXIT_SUCCESS;
}