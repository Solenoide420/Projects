#ifndef __HUFFMAN_H__
#define __HUFFMAN_H__

#include <stdint.h>
#include <stdbool.h>
#include "bitstream.h"

/*
    ┌───────────────────────────────────────────────────────────┐
    │                                                           │
    │              	   Fonctions Principales                    │
    │                                                           │
    └───────────────────────────────────────────────────────────┘
*/

struct huff_table;

extern struct huff_table *huffman_load_table( struct bitstream *stream, uint16_t *nb_byte_read, uint32_t *dest );

extern uint8_t huffman_next_value(struct huff_table *table,
                                 struct bitstream *stream);

extern void huffman_free_table(struct huff_table *table);

/*
    ┌───────────────────────────────────────────────────────────┐
    │                                                           │
    │              	   Fonctions Auxiliaires                    │
    │                                                           │
    └───────────────────────────────────────────────────────────┘
*/

void huffman_generate_symbols( struct huff_table *table,
                               struct bitstream *stream,
                                      uint16_t *nb_byte_read);

void huffman_generate_codes( struct huff_table *h_table );

struct huff_table *huffman_create_empty_table( );

uint8_t huffman_get_index_table( struct huff_table *table );

bool huffman_get_AC_type( struct huff_table *table );

uint32_t huffman_get_nb_symbols( struct huff_table *table );

bool huffman_get_set_value( struct huff_table *table );

#ifdef BLABLA
extern int8_t huffman_next_value_count(struct huff_table *table,
                                 struct bitstream *stream,
                                 uint8_t *nb_bits_read);
#endif
#endif
