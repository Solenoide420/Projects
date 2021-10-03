#ifndef _PLACEMENT_H_
#define _PLACEMENT_H_

#include <stdint.h>

/*
Pour vider le buffer si le bro met trop de char
*/
extern void viderBuffer(void);

/*
Pour récup ce que le bro écrit
*/
extern int lire(char *chaine, int longueur);

/*
Place le bateau de façon adéquate sur la grille
*/
extern void bateau(uint8_t** grille, uint8_t ligne, uint8_t colonne, bool horizontal,uint8_t taille, uint8_t bateau);

/*
Gère la phase de placement du joueur indiqué et sur la grille donnée
*/
extern void place_bateaux(uint8_t** grille, uint8_t joueur);

#endif /* _PLACEMENT_H_ */
