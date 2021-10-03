#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>


void inverse_zigzag(int16_t** zigzaged, int16_t* depli) {
    uint8_t actu = 0;

    for (int8_t k = 0; k <15; k++) {
        if (k % 2 == 0) {
            for (uint8_t i = 7; i < 8; i--) {
                if ((k - i) < 8 && (k - i) > -1 ) {
                    zigzaged[i][k-i] = depli[actu];
                    actu++;
                }
            }
        } else {
            for (uint8_t i = 0; i < 8; i++) {
                if ((k - i) < 8 && (k - i) > -1 ) {
                    zigzaged[i][k-i] = depli[actu];
                    actu++;
                }
            }
        }
    }
}