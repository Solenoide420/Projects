#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#include "bitstream.h"
#include "jpeg_reader.h"
#include "huffman.h"

#include "extraction.h"


int16_t magnitude_to_int(uint8_t magn, uint32_t bits) {
    if (magn == 0) return 0;

    int16_t tmp = magnitude_to_int(magn-1, bits >> 1);

    if ((bits & 0x1) == 1) {
        if (tmp >= 0) {
            return 1 + 2*tmp;
        } else {
            return 2*tmp;
        }

    } else {
        if (tmp > 0) {
            return 2*tmp;
        } else {
            return -1 + 2*tmp;
        }
    }
}

void extraction_bloc(struct huff_table** huff_tables_ac, struct huff_table** huff_tables_dc, struct bitstream* stream, const struct jpeg_desc *jpeg, uint8_t nb_bloc, int16_t* bloc) {

    uint8_t id_table_dc = jpeg_get_scan_component_huffman_index(jpeg, DC, nb_bloc);
    uint8_t id_table_ac = jpeg_get_scan_component_huffman_index(jpeg, AC, nb_bloc);

    uint32_t bits;
    uint8_t lus;

    uint8_t nb_bits_DC = huffman_next_value(huff_tables_dc[id_table_dc], stream);
    uint8_t nb_read = bitstream_read(stream, nb_bits_DC, &bits, true); nb_read++;
    bloc[0] = magnitude_to_int(nb_bits_DC, bits);

    uint8_t actu = 1;
    while (actu < 64) {
        lus = huffman_next_value(huff_tables_ac[id_table_ac], stream);

        if (lus == 0) {               // On a lu 0x00
            while (actu < 64) {
                bloc[actu] = 0;
                actu++;
            }
            return ;
        } else if (lus == 0xf0) {     // On a lu 0xf0
            for (uint8_t u = 0; u < 16; u++) {
                bloc[actu] = 0;
                actu++;
            }
        } else if (lus % 16 == 0) {   // On a lu 0x?0
            perror("\n\nFichier invalide en lecture de données brutes");
            exit(1);
        } else {
            for (uint8_t u = 0; u < (lus >> 4); u++) {

                if (actu > 63) {
                    break;
                }
                bloc[actu] = 0;
                actu++;
            }

            uint8_t nb_bits_AC = lus & 0X0F;
            uint8_t nb_read = bitstream_read(stream, nb_bits_AC, &bits, true); nb_read++;

            if (actu > 63) {
                break;
            }

            bloc[actu] = magnitude_to_int(nb_bits_AC, bits);
            actu++;
        }
    }
    return (void) NULL;
}

void imprime_bloc(int16_t* bloc) {
    for (uint8_t i = 0; i < 64; i++) {
        printf("%x ", bloc[i] & 0xFFFF);

        if (i % 8 == 7) {
            printf("\n");
        }
    }
    printf("\n\n");
}

void imprime_mat(int16_t** bloc) {
    for (uint8_t i = 0; i < 8; i++) {
        for (uint8_t j = 0; j < 8; j++) {
        printf("%x ", bloc[i][j] & 0xFFFF);
        }
        printf("\n");
    }
    printf("\n\n");
}

void imprime_mat2(int8_t** bloc) {
    for (uint8_t i = 0; i < 8; i++) {
        for (uint8_t j = 0; j < 8; j++) {
        printf("%x ", bloc[i][j] & 0xFF);
        }
        printf("\n");
    }
    printf("\n\n");
}
