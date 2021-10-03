#ifndef __IZIG_ZAG_H__
#define __IZIG_ZAG_H__

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

/*
Effectue le pli de la liste en un bloc de 8x8
*/
void inverse_zigzag(int16_t** zigzaged, int16_t* depli);

#endif