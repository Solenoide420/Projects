#ifndef _BATAILLE_H_
#define _BATAILLE_H_

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

/*
Effectue le tour du joueur
*/
bool joue_bombe(uint8_t** grillep, bool** bombep, uint8_t** grilleo, bool** bombeo, uint8_t joueur, char* coupprec, char* gage, uint32_t base);

/*
Regarde si le bateau touché est coulé
*/
bool est_coule(uint8_t** grilleo, bool** bombep, uint8_t ligne, uint8_t colonne);

#endif /* _BATAILLE_H_ */
