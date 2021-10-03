#include <stdlib.h>
#include <stdint.h>
#include <math.h>



float cos_pi_16(int8_t i) {
    float mem[9] = {1, 0.9807852805, 0.9238795325, 0.8316696123, 0.7071067812, 0.555570233, 0.3826834324, 0.195190322, 0};

    int8_t mod = i % 32;

    if (mod < 9) {
        return mem[mod];
    } else if (mod < 17) {
        return -mem[16-mod];
    } else if (mod < 25) {
        return -mem[mod-16];
    } else {
        return mem[32-mod];
    }
}

float C(uint8_t eps) {
    if (eps != 0) {
        return 1;
    }
    return 0.7071067812;
}

void iDCT_naif(uint8_t** final_bloc, int16_t** frequentiel) {
    float tmp[64];
    for (uint8_t k = 0; k < 64; k++) {
        tmp[k] = 0;
    }

    for (uint8_t i = 0; i < 8; i++) {
        for (uint8_t j = 0; j < 8; j++) {
            for (uint8_t lbda = 0; lbda < 8; lbda++) {
                for (uint8_t mu = 0; mu < 8; mu ++) {
                    tmp[8*i + j] += C(lbda) * C(mu) * cos_pi_16((2*i +1)*lbda) * cos_pi_16((2*j +1)*mu) * frequentiel[lbda][mu];
                }
            }
            tmp[8*i +j] *= 0.25;
        }
    }

    for (uint8_t i = 0; i < 8; i++) {
        for (uint8_t j = 0; j < 8; j++) {
            tmp[8*i + j] += 128;
            if (tmp[8*i + j] < 0) {
                final_bloc[i][j] = 0;
            } else if (tmp[8*i + j] > 255) {
                final_bloc[i][j] = 255;
            } else {
                final_bloc[i][j] = (int) roundf(tmp[8*i + j]);
            }
        }
    }
}