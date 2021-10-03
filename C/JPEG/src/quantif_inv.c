#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>


void quantification_inverse(uint16_t* bloc , uint8_t* table_quantif) {
    for (uint8_t i = 0; i < 64; i++) {
        bloc[i] *= table_quantif[i];
        //printf("bloc : %u\n", bloc[i]);
    }
}
