#ifndef __QUANTIF_INV_H__
#define __QUANTIF_INV_H__

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

/*
Effectue la quantification inverse d'un bloc (sous forme de liste) avec la table de quatification
donnée
*/
void quantification_inverse(int16_t* bloc , uint8_t* table_quantif);


#endif