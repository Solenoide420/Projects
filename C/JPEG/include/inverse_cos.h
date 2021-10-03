#ifndef __INVERSE_COS_H__
#define __INVERSE_COS_H__

#include <stdlib.h>
#include <stdint.h>
#include <math.h>

/*
Fonction pour un calcul plus rapide des cos(n PI/16)
*/
float cos_pi_16(int8_t i);

/*
Fonction de normalisation (1/sqrt(2) pour eps = 0, 1 sinon)
*/
float C(uint8_t eps);

/*
Effectue naïvement la discrétisation cosinus inverse (passage des fréquences aux pixels)
*/
void iDCT_naif(uint8_t** final_bloc, int16_t** frequentiel);


#endif
