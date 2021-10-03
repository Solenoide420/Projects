#ifndef _AFFICHAGE_H_
#define _AFFICHAGE_H_

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

/*
Affiche la grille en tenant compte de la bordure d'épaisseur 3 autour
*/
void affiche_grille(bool** grille, uint8_t largeur, uint8_t hauteur);

#endif /* _AFFICHAGE_H_ */