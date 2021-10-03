#ifndef _GAME_H_
#define _GAME_H_

#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

/*
Une partie de bataille navale
*/
extern int game(char* gage, uint32_t base);

/*
L'écran de victoire avec affichage des grilles
*/
void victoire(uint8_t** bateauv, bool** bombesv, uint8_t** bateaup, bool** bombesp, uint8_t joueur, char* gage, uint32_t base, uint8_t reste);

#endif /* _GAME_H_ */
