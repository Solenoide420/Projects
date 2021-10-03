#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>


uint8_t* YCbCr_RGB(uint8_t Y, uint8_t Cb, uint8_t Cr) {
    uint8_t* res = malloc(3 * sizeof(uint8_t));

    float R = Y - 0.0009267 * (Cb - 128) + 1.4016868 * (Cr - 128);
    float G = Y - 0.3436954 * (Cb - 128) - 0.7141690 * (Cr - 128);
    float B = Y + 1.7721604 * (Cb - 128) + 0.0009902 * (Cr - 128);

    res[0] = (R > 255) ? 255 : ((R < 0 ) ? 0 : (uint8_t) R);
    res[1] = (G > 255) ? 255 : ((G < 0 ) ? 0 : (uint8_t) G);
    res[2] = (B > 255) ? 255 : ((B < 0 ) ? 0 : (uint8_t) B);

    return res;
}

uint8_t* YCbCr_RGB_simple(uint8_t Y, uint8_t Cb, uint8_t Cr) {
    uint8_t* res = malloc(3 * sizeof(uint8_t));

    float R = Y + 1.402 * (Cr - 128);
    float G = Y - 0.34414 * (Cb - 128) - 0.71414 * (Cr - 128);
    float B = Y + 1.772 * (Cr - 128);
    
    res[0] = (R > 255) ? 255 : ((R < 0 ) ? 0 : (uint8_t) R);
    res[1] = (G > 255) ? 255 : ((G < 0 ) ? 0 : (uint8_t) G);
    res[2] = (B > 255) ? 255 : ((B < 0 ) ? 0 : (uint8_t) B);

    return res;
}