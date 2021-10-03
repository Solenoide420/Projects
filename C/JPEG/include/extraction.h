#ifndef __EXTRACTION_H__
#define __EXTRACTION_H__

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#include "bitstream.h"
#include "jpeg_reader.h"
#include "huffman.h"

/*
Détermine la valeur encodé à partir de la magnitude et des bits qui suivent
*/
int16_t magnitude_to_int(uint8_t magn, uint32_t bits);


/*
Décode le bloc nb_bloc à l'aide des tables, des données brutes et des infos sur l'image.
*/
void extraction_bloc(struct huff_table** huff_tables_ac, struct huff_table** huff_tables_dc, struct bitstream* stream, const struct jpeg_desc *jpeg, uint8_t nb_bloc, int16_t* bloc);

/*
Imprime le bloc
*/
void imprime_bloc(int16_t* bloc);

/*
Imprime un bloc sous forme matricielle
*/
void imprime_mat(int16_t** bloc);

void imprime_mat2(int8_t** bloc);

#endif