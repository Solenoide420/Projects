#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "bitstream.h"

struct bitstream {

    FILE *file;
    // L'octet du fichier auquel on a accès.
    uint8_t current_octet;
    // Indice du dernier bit lu (des poids forts aux poids faibles).
    uint8_t bit_index;
    // Nombre de bits lus dans le fichier.
    uint8_t nb_bits_read;
    // true si le fichier est vide ( il n'y a plus d'octets à lire ), false sinon
    bool is_empty;
};


// Cette fonction permet de créer le flux de bits.
struct bitstream *bitstream_create(const char *filename){

    FILE *file = fopen(filename, "rb");

    if( file == NULL) {
        printf("On peut pas lire le fichier %s ! \n", filename);
        return NULL;
    }

    struct bitstream *stream = malloc(sizeof(struct bitstream));

    if (stream == NULL){
        printf("Echec de l'allocation de mémoire à bitstream. \n");
        return NULL;
    }
    if ( fread(&stream->current_octet, sizeof(uint8_t), 1, file) == 0) {
        fclose(file);
        return NULL;
    }
    else {
        stream->bit_index = 0;
        stream->is_empty = false;
        stream->file = file;
        stream->nb_bits_read = 0;
    }
    return stream;
}

/* Cette fonction permet de fermer le fichier en question et le flux de bits
correspondant */
void bitstream_close(struct bitstream *stream){
    fclose(stream->file);
    free(stream);
}


// Cette fonction permet de lire nb_bits du flux de bits considéré.
uint8_t bitstream_read(struct bitstream *stream, uint8_t nb_bits, uint32_t *dest, bool discard_byte_stuffing){

    if ( nb_bits > 32 ) {
        printf("Lecture de 32 bits max par appel de la fonction. \n");
        return EXIT_FAILURE;
    }

    uint8_t nb_bits_read = 0;
    uint8_t bit_read;

    *dest = 0;

    while ( nb_bits_read < nb_bits && !stream->is_empty) {

        bit_read = stream->current_octet >> ( 7 - stream->bit_index ) & 1;
        *dest = ( *dest << 1 ) + bit_read;
        stream->nb_bits_read += 1;
        nb_bits_read += 1;
        stream->bit_index += 1;

        if (stream->bit_index == 8){
            if (stream->current_octet == 0xFF){
            // Cas où on doit faire un (ou des) byte stuffing
                read_next_byte(stream);
                if ( discard_byte_stuffing && stream->current_octet == 0x00 ) {
                    read_next_byte(stream);
                }
            }
            else {
                read_next_byte(stream);
            }
        }
    }
    return nb_bits_read;
}

// Cette fonction retourne true s'il n'y a plus d'octets à lire, false sinon
bool bitstream_is_empty(struct bitstream *stream){
    return (stream->is_empty);
}

// Cette fonction permet d'accéder à l'octet suivant du flux de bits.
void read_next_byte(struct bitstream *stream){
    if ( fread(&stream->current_octet, sizeof(uint8_t), 1, stream->file) == 0){
        stream->is_empty = true;
    }
    stream->bit_index = 0;
}

FILE *bitstream_get_pointer_to_file( struct bitstream *stream) {
    return stream->file;
}
