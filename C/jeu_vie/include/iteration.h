#ifndef _ITERATION_H_
#define _ITERATION_H_

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

/*
Effectue une otération du jeu de la vie sur la grille donnée en paramètre

Retourne le pointeur vers la nouvelle grille et free la grille donnée
*/
bool** iteration_grille(bool** grille, uint8_t largeur, uint8_t hauteur);

#endif /* _ITERATION_H_ */