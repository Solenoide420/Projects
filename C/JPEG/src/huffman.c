#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <huffman.h>
#include <bitstream.h>
#include <jpeg_reader.h>

struct huff_table {
    // true si la table de Huffman est de type AC
    bool AC;
    // indice de la table de Huffman
    uint32_t index;
    // tableau auxiliaire permettant de générer les symboles et les codes.
    uint32_t offsets[17];
    // tableau stockant l'ensemble des symboles lus dans la table de Huffman.
    uint32_t symbols[162];
    // le nombre de symboles de cette table de Huffman.
    uint32_t nb_symbols;
    // tableau stockant le nombre de symboles par longueur de code.
    uint32_t codes_per_length[16];
    // tableau stockant l'ensemble des codes correspondants à cette table de Huffman.
    uint32_t codes[162];
    // auxiliaire.
    bool set;
};

// Cette fonction permet de retourner la table de huffman lue dans le bitstreaù
struct huff_table *huffman_load_table( struct bitstream *stream,
                                              uint16_t *nb_byte_read,
                                              uint32_t *dest) {

    struct huff_table* table = malloc(sizeof(struct huff_table));

    table->set = true;
    table->AC = (bool) (*dest >> 4);
    table->index = (*dest << 28 ) >> 28;

    huffman_generate_symbols( table, stream, nb_byte_read );

    huffman_generate_codes( table );

    return table;
}

// Cette fonction permet de générer les symboles de la table de Huffman
void huffman_generate_symbols( struct huff_table *table,
                               struct bitstream *stream,
                                      uint16_t *nb_byte_read ) {

    uint32_t running_total_of_symbols = 0;

    uint32_t bits = 0;

    table->offsets[0] = 0;

    for ( uint8_t i = 0 ; i < 16 ; i++) {
        uint8_t nb_read_1 = bitstream_read(stream, 8, &bits, false);
        check_reading_process( nb_read_1, 8 );
        running_total_of_symbols = running_total_of_symbols + bits;
        *nb_byte_read += 1;
        table->offsets[i+1] = running_total_of_symbols;
        table->codes_per_length[i] = bits;
    }

    table->nb_symbols = running_total_of_symbols;

    uint32_t dest;
    for ( uint32_t i = 0 ; i < running_total_of_symbols ; i++ ) {
        uint8_t nb_read_2 = bitstream_read(stream, 8, &dest, false);
        check_reading_process( nb_read_2, 8 );
        table->symbols[i] = dest;
    }
}

// Cette fonction permet de générer les codes correspondants à la table de Huffman.
void huffman_generate_codes( struct huff_table *table ) {

    uint32_t code = 0;

    for ( uint8_t i = 0; i < 16; i++ ) {
        for ( uint8_t j = table->offsets[i]; j < table->offsets[i+1]; j++ ){
            table->codes[j] = code;
            code += 1;
        }
        code = code << 1;
    }
}

// Cette fonction permet de renvoyer le prochain symbole rencontré.
uint8_t huffman_next_value( struct huff_table *table, struct bitstream *stream ) {

    uint32_t current_code = 0;
    uint32_t bit = 0;

    for ( uint8_t i = 0; i < 16; i++ ) {

        // Lecture d'un bit à partir du bitstream
        uint8_t nb_read_1 = bitstream_read( stream, 1, &bit, true );

        if ( nb_read_1 != 1 ) {
            printf("Echec de lecture d'un bit à partir du bitstream");
            return EXIT_FAILURE;
        }

        current_code =  ( current_code << 1) | bit;

        for ( uint32_t j = table->offsets[i]; j < table->offsets[i+1]; j++ ){
            if ( table->codes[j] == current_code ) {
                return table->symbols[j];
            }
        }

    }

    return EXIT_FAILURE;
}

// Cette fonction permet de libérer la mémoire correspondant à la table de Huffman.
extern void huffman_free_table( struct huff_table *table ) {
    free( table );
}

// Cette fonction permet de créer une table de Huffman "vide".
struct huff_table *huffman_create_empty_table ( ) {

    struct huff_table* table = malloc(sizeof(struct huff_table));

    table->set = false;
    table->AC = false;
    table->nb_symbols = 0;
    table->index = 0;

    for (uint8_t i = 0 ; i < 162 ; i++) {
        table->symbols[i] = 0;
        table->codes[i] = 0;
        if ( i < 17 ) {
            table->offsets[i] = 0;
        }
        if ( i < 16 ) {
            table->codes_per_length[i] = 0;
        }
    }

    return table;
}

uint8_t huffman_get_index_table( struct huff_table *table ) {
    return table->index;
}

bool huffman_get_AC_type( struct huff_table *table ) {
    return table->AC;
}

uint32_t huffman_get_nb_symbols( struct huff_table *table ) {
    return table->nb_symbols;
}

bool huffman_get_set_value( struct huff_table *table ) {
    return table->set;
}
