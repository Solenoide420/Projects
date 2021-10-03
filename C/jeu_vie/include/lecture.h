#ifndef _LECTURE_H_
#define _LECTURE_H_

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

/*
Retourne la grille contenue dans le fichier _filename_

SI le fichier n'existe pas ou est invalide, une erreur est levée
*/
bool** lecture_vie(char* filename, uint8_t h_ecran, uint8_t l_ecran);

#endif /* _LECTURE_H_ */