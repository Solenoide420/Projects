#ifndef _GRILLE_H_
#define _GRILLE_H_

#include <stdbool.h>


/*
Initialise une grille de bataille navale
*/
extern uint8_t** init_grille(void);

/*
Initialise une grille de bombardements
*/
extern bool** init_bombardes(void);

/* 
Affiche la grille pour la phase de placement des bateaux
*/
extern void affiche_grille_depart(uint8_t** grille);

/*
Affiche la grille de bataille navale en tant que sienne
*/
extern void affiche_grille_perso(uint8_t** grille, bool** bombardes);

/*
Affiche la grille de bataille navale en tant que adversaire
*/
extern void affiche_grille_oppo(uint8_t** grille, bool** bombardes);

/*
Vérifie que le placement du bateau est valide
*/
extern bool verif_placement(uint8_t** grille, uint8_t ligne, uint8_t colonne, bool horizontal, uint8_t taille);

/*
Vérifie que les coordonnées de bombardement sont valides
*/
extern bool verif_bombardement(bool** bombardes, uint8_t ligne, uint8_t colonne);

/*
Free la grille de bataille
*/
extern void free_grille(uint8_t** grille);

/*
Free la grille de bombardement
*/
extern void free_bombes(bool** bombes);

/*
Focntion pour attendre le joueur prochain
*/
void attendre_prochain(uint8_t joueursuiv);


#endif /* _GRILLE_H_ */