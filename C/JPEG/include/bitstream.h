#ifndef __BITSTREAM_H__
#define __BITSTREAM_H__

#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct bitstream;

extern struct bitstream *bitstream_create(const char *filename);

extern void bitstream_close(struct bitstream *stream);

extern uint8_t bitstream_read(struct bitstream *stream,
                              uint8_t nb_bits,
                              uint32_t *dest,
                              bool discard_byte_stuffing);

extern bool bitstream_is_empty(struct bitstream *stream);

FILE *bitstream_get_pointer_to_file( struct bitstream *stream);

void read_next_byte(struct bitstream *stream);

#endif
