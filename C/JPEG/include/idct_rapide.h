#ifndef __IDCT_RAPIDE_H__
#define __IDCT_RAPIDE_H__

#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <stdio.h>


#ifndef M_PI
    #define M_PI 3.14159265358979323846
#endif
extern void idct_1_dimension(int16_t* vecteur);
extern void iDCT_AAN(uint8_t** frequentiel,int16_t** final_bloc);

extern float* get_cos_tab(void);

void iDCT_plus_rapide(uint8_t** final_bloc,int16_t** frequentiel,const float* const idctMap);

void iDCT_meilleur(uint8_t** final_bloc,int16_t** frequentiel, const float* const  idctMap);

#endif
