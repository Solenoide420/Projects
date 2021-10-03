#ifndef __CONVERSION_H__
#define __CONVERSION_H__

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

/*
Retourne une liste [R, G, B] par conversion selon la formule complète
*/
uint8_t* YCbCr_RGB(uint8_t Y, uint8_t Cb, uint8_t Cr);

/*
Retourne une liste [R, G, B] par conversion selon la formule simlifiée
*/
uint8_t* YCbCr_RGB_simple(uint8_t Y, uint8_t Cb, uint8_t Cr);

#endif