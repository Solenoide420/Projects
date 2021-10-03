#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <jpeg_reader.h>
#include <bitstream.h>
#include <huffman.h>

struct Quantization_Table {
    uint32_t* pointer_to_table;
    bool set;
};

struct Colour_Component {
    uint32_t SOF_reading_order;
    uint32_t SOS_reading_order;
    uint32_t component_identifiant;
    uint32_t horizontal_sampling_factor;
    uint32_t vertical_sampling_factor;
    uint32_t table_index;
    uint32_t Huffman_DC_Table_index;
    uint32_t Huffman_AC_Table_index;
    bool used;
};

struct jpeg_desc {

    const char* filename;
    struct bitstream *bit_stream;
    struct Quantization_Table Quantization_Tables[4];

    struct huff_table* Huffman_DC_Tables[4];
    struct huff_table* Huffman_AC_Tables[4];

    uint32_t frametype;
    uint32_t height;
    uint32_t width;

    uint32_t start_of_selection;
    uint32_t end_of_selection;
    uint32_t successive_approximation_high;
    uint32_t successive_approximation_low;

    uint32_t restart_interval;

    uint32_t components_number;

    struct Colour_Component components[3];

    bool valid;
};

void jpeg_read_SOF0( struct jpeg_desc* jpeg, struct bitstream *stream ) {

    printf("/////////////////reading SOF0\n");
    jpeg->frametype = 0xC0;

    uint32_t length;
    uint8_t nb_read_1 = bitstream_read( stream, 16, &length, false );
    check_reading_process( nb_read_1, 16 );
    uint32_t precision;
    uint8_t nb_read_2 = bitstream_read( stream, 8, &precision, false );
    check_reading_process( nb_read_2, 16 );

    if ( precision != 8 ) {
        printf("Erreur : précision invalide\n");
        jpeg->valid = false;
        return;
    }

    uint8_t nb_read_3 = bitstream_read( stream, 16, &jpeg->height, false );
    check_reading_process( nb_read_3, 16 );
    uint8_t nb_read_4 = bitstream_read( stream, 16, &jpeg->width, false );
    check_reading_process( nb_read_4, 16 );

    if ( jpeg->height == 0 || jpeg->width == 0 ) {
        printf("Erreur : dimensions invalides\n");
        jpeg->valid = false;
        return;
    }

    uint8_t nb_read_5 = bitstream_read( stream, 8, &jpeg->components_number, false );
    check_reading_process( nb_read_5, 8 );

    if ( jpeg->components_number < 1 && jpeg->components_number > 3 ) {
        printf("Erreur : Le nombre de composantes est invalide\n");
        jpeg->valid = false;
        return;
    }

    for ( uint32_t i = 0; i < jpeg->components_number; i++ ) {

        uint32_t component_ID;
        uint8_t nb_read_6 = bitstream_read( stream, 8, &component_ID, false );
        check_reading_process( nb_read_6, 8 );

        struct Colour_Component* component = &jpeg->components[i];

        if ( component->used ) {
            printf("Erreur : Duplicate color component ID\n");
            jpeg->valid = false;
            return;
        }

        component->component_identifiant = component_ID;
        component->used = true;
        component->SOF_reading_order = i+1;

        uint8_t nb_read_7 = bitstream_read( stream, 4, &component->horizontal_sampling_factor, false );
        check_reading_process( nb_read_7, 4 );
        uint8_t nb_read_8 = bitstream_read( stream, 4, &component->vertical_sampling_factor, false );
        check_reading_process( nb_read_8, 4 );
        uint8_t nb_read_9 = bitstream_read( stream, 8, &component->table_index, false );
        check_reading_process( nb_read_9, 8 );

        if ( component->table_index > 3 ) {
            printf("Erreur : indice de table de quantification invalide\n");
            jpeg->valid = false;
            return;
        }
    }

    if ( (length - 8 - 3*jpeg->components_number) != 0 ) {
        printf("Erreur : SOF invalide\n");
        jpeg->valid = false;
    }

}

void jpeg_read_quantization_table( struct jpeg_desc* jpeg, struct bitstream *stream ) {

    printf("/////////////////reading DQT \n");
    uint32_t length;
    uint8_t nb_read_1 = bitstream_read( stream, 16, &length, false );
    check_reading_process( nb_read_1, 16 );
    length = length - 2;

    while ( length > 0 ) {
        uint32_t precision;
        uint8_t nb_read_2 = bitstream_read( stream, 4, &precision, false );
        check_reading_process( nb_read_2, 4 );
        uint32_t index;
        uint8_t nb_read_3 = bitstream_read( stream, 4, &index, false );
        check_reading_process( nb_read_3, 4 );
        length = length - 1;

        if ( index > 3 ) {
            printf("Erreur : Table de Quantification invalide\n");
            jpeg->valid = false;
            return;
        }

        jpeg->Quantization_Tables[index].set = true;

        if ( precision == 1 ) {
            for (uint32_t i = 0 ; i < 64 ; i++) {
                uint32_t value;
                uint8_t nb_read_4 = bitstream_read( stream, 16, &value, false );
                check_reading_process( nb_read_4, 16 );
                jpeg->Quantization_Tables[index].pointer_to_table[i] = value;
            }

            length = length - 128;
        }
        else {

            for (uint32_t i = 0 ; i < 64 ; i++) {
                uint32_t value;
                uint8_t nb_read_5 = bitstream_read( stream, 8, &value, false );
                check_reading_process( nb_read_5, 8 );
                jpeg->Quantization_Tables[index].pointer_to_table[i] = value;

            }

            length = length - 64;
        }
    }

    if ( length != 0 ) {

        printf("Erreur : DQT invalid \n");
        jpeg->valid = false;
    }
}

void jpeg_read_Huffman_Table( struct jpeg_desc* jpeg, struct bitstream *stream ) {

    printf("/////////////////reading DHT \n");
    uint32_t length;
    uint8_t nb_read_1 = bitstream_read(stream, 16, &length, false);
    check_reading_process( nb_read_1, 16 );
    length = length - 2;

    uint32_t dest;

    while ( length > 0 ) {

        uint8_t nb_read_2 = bitstream_read( stream, 3, &dest, false );
        check_reading_process( nb_read_2, 3 );

        uint8_t nb_read_3 = bitstream_read( stream, 5, &dest, false );
        check_reading_process( nb_read_3, 5 );

        uint16_t nb_byte_read = 0;

        struct huff_table *h_table = huffman_load_table( stream, &nb_byte_read, &dest);

        if ( huffman_get_AC_type( h_table ) == true) {
            huffman_free_table(jpeg->Huffman_AC_Tables[ huffman_get_index_table( h_table ) ]);
            jpeg->Huffman_AC_Tables[ huffman_get_index_table( h_table ) ] = h_table;
        }
        else {
            huffman_free_table(jpeg->Huffman_DC_Tables[ huffman_get_index_table( h_table ) ]);
            jpeg->Huffman_DC_Tables[ huffman_get_index_table( h_table ) ] = h_table;
        }

        if ( huffman_get_index_table( h_table ) > 3 ) {
            printf("Erreur : Huffmann Table invalide\n");
            jpeg->valid = false;
            return;
        }

        if ( huffman_get_nb_symbols( h_table ) > 162 ) {
            printf("Erreur : Trop de symboles dans la table de Huffman\n");
            jpeg->valid = false;
            return;
        }

        length -= 17 + huffman_get_nb_symbols( h_table );
    }

    if ( length != 0 ) {
        printf("Erreur : DHT invalide\n");
        jpeg->valid = false;
    }
}

void jpeg_read_SOS ( struct jpeg_desc* jpeg, struct bitstream *stream ) {

    printf("/////////////////reading SOS marker\n");

    if ( jpeg->components_number == 0 ) {
        printf("Erreur : SOS détecté avant SOF\n");
        jpeg->valid = false;
        return;
    }

    uint32_t length;
    uint8_t nb_read_1 = bitstream_read(stream, 16, &length, false);
    check_reading_process( nb_read_1, 16 );

    for (uint32_t i = 0 ; i < jpeg->components_number ; i++) {
        jpeg->components[i].used = false;
    }

    uint32_t number_components;
    uint8_t nb_read_2 = bitstream_read(stream, 8, &number_components, false);
    check_reading_process( nb_read_2, 8 );

    for (uint32_t i = 0 ; i < number_components ; i++) {
        uint32_t id_compo;
        uint8_t nb_read_3 = bitstream_read(stream, 8, &id_compo, false);
        check_reading_process( nb_read_3, 8 );

        uint8_t index;
        for ( uint8_t i = 0; i < jpeg->components_number; i++ ) {
            if ( jpeg->components[i].component_identifiant == id_compo ) {
                index = i;
            }
        }

        struct Colour_Component* component = &jpeg->components[index];
        if ( component->used ) {
            printf("Erreur : identifiant de composante dupliqué\n");
            jpeg->valid = false;
            return;
        }

        component->used = true;
        component->SOS_reading_order = i+1;

        uint8_t nb_read_4 = bitstream_read(stream, 4, &component->Huffman_DC_Table_index, false);
        check_reading_process( nb_read_4, 4 );
        uint8_t nb_read_5 = bitstream_read(stream, 4, &component->Huffman_AC_Table_index, false);
        check_reading_process( nb_read_5, 4 );

        if ( component->Huffman_DC_Table_index > 3 ) {
            printf("Erreur : indice de la table DC de Huffmann invalide\n");
            jpeg->valid = false;
            return;
        }

        if ( component->Huffman_AC_Table_index > 3 ) {
            printf("Erreur : indice de la table AC de Huffmann invalide\n");
            jpeg->valid = false;
            return;
        }
    }

    uint8_t nb_read_6 = bitstream_read(stream, 8, &jpeg->start_of_selection, false);
    check_reading_process( nb_read_6, 8 );
    uint8_t nb_read_7 = bitstream_read(stream, 8, &jpeg->end_of_selection, false);
    check_reading_process( nb_read_7, 8 );
    uint8_t nb_read_8 = bitstream_read(stream, 4, &jpeg->successive_approximation_high, false);
    check_reading_process( nb_read_8, 4 );
    uint8_t nb_read_9 = bitstream_read(stream, 4, &jpeg->successive_approximation_low, false);
    check_reading_process( nb_read_9, 4 );

    if ( jpeg->start_of_selection != 0 || jpeg->end_of_selection != 63 ) {
        printf("Erreur : sélection spectrale invalide\n");
        jpeg->valid = false;
        return;
    }

    if ( jpeg->successive_approximation_high != 0 || jpeg->successive_approximation_low != 0 ) {
        printf("Erreur : approximation successive invalide\n");
        jpeg->valid = false;
        return;
    }

    if ( (length - 6 - 2*number_components) != 0 ) {
        printf("Erreur : SOS invalide\n");
        jpeg->valid = false;
    }
}

void jpeg_read_restart_interval ( struct jpeg_desc* jpeg, struct bitstream *stream ) {
    printf("/////////////////reading DRI \n");
    uint32_t length;
    uint8_t nb_read_1 = bitstream_read(stream, 16, &length, false);
    check_reading_process( nb_read_1, 16 );

    uint8_t nb_read_2 = bitstream_read(stream, 16, &jpeg->restart_interval, false);
    check_reading_process( nb_read_2, 16 );

    if ( length - 4 != 0 ) {
        printf("Erreur : Marqueur DRI invalide");
        jpeg->valid = false;
    }
}

void jpeg_read_APPx( struct bitstream *stream ) {
    printf("/////////////////reading APPx\n");
    uint32_t length;

    uint8_t nb_read_1 = bitstream_read(stream, 16, &length, false);
    check_reading_process( nb_read_1, 16 );

    uint32_t dest;
    for ( uint32_t i = 0; i < length -2; i++ ) {
        uint8_t nb_read_2 = bitstream_read(stream, 8, &dest, false);
        check_reading_process( nb_read_2, 8 );
    }
}

void jpeg_read_commentary( struct bitstream *stream ) {
    printf("/////////////////reading COM marker\n");
    uint32_t length;
    uint8_t nb_read_1 = bitstream_read(stream, 16, &length, false);
    check_reading_process( nb_read_1, 16 );

    uint32_t dest;
    for ( uint32_t i = 0; i < length -2; i++ ) {
        uint8_t nb_read_2 = bitstream_read(stream, 8, &dest, false);
        check_reading_process( nb_read_2, 8 );
    }
}

// Cette fonction lit l'en-tête JPEG
struct jpeg_desc *jpeg_read( const char *filename ) {

    struct jpeg_desc *jpeg = jpeg_desc_create( filename );

    // ouverture du fichier
    struct bitstream *stream = bitstream_create( filename );

    jpeg->bit_stream = stream;

    uint32_t last_byte;
    uint32_t current_byte;
    uint8_t nb_read_1 = bitstream_read( stream, 8, &last_byte, false );
    check_reading_process( nb_read_1, 8);
    uint8_t nb_read_2 = bitstream_read( stream, 8, &current_byte, false );
    check_reading_process( nb_read_2, 8);

    if ( last_byte != 0xFF || current_byte != 0xD8 ) {
        jpeg->valid = false;
        fclose( bitstream_get_pointer_to_file( stream) );
    }

    uint8_t nb_read_3 = bitstream_read( stream, 8, &last_byte, false );
    check_reading_process( nb_read_3, 8);
    uint8_t nb_read_4 = bitstream_read( stream, 8, &current_byte, false );
    check_reading_process( nb_read_4, 8);

    while ( jpeg->valid ) {

        jpeg_check_errors_1( jpeg, last_byte, current_byte );

        if ( jpeg->valid == false ) {
            fclose( bitstream_get_pointer_to_file( stream ) );
            return jpeg;
        }

        uint8_t nb_read_7;

        switch ( current_byte )
        {
            case 0xC0 /*SOF0*/ : jpeg_read_SOF0( jpeg, stream ); break;

            case 0xDB /*DQT*/  : jpeg_read_quantization_table( jpeg, stream ); break;

            case 0xC4 /*DHT*/  : jpeg_read_Huffman_Table( jpeg, stream ); break;

            case 0xDA /*SOS*/  : jpeg_read_SOS( jpeg, stream );
                                 return jpeg; break;

            case 0xDD /*DRI*/  : jpeg_read_restart_interval( jpeg, stream ); break;

            case 0xE0 /*APP0*/ : jpeg_read_APPx( stream ); break;

            case 0xFE /*COM*/  : jpeg_read_commentary( stream ); break;

            case 0x01 /*TEM*/  : break;

            case 0xFF :
                nb_read_7 = bitstream_read( stream, 8, &current_byte, false ); continue;
                check_reading_process( nb_read_7, 8);
                break;

            default :
                if ( (current_byte >= 0xF0 && current_byte <= 0xFD) || current_byte == 0xDC || current_byte == 0xDE || current_byte == 0xDF ) {
                    jpeg_read_commentary( stream );
                }
                else {
                    return jpeg_check_errors_2( jpeg, stream, current_byte );
                }
        }

        uint8_t nb_read_5 = bitstream_read( stream, 8, &last_byte, false );
        check_reading_process( nb_read_5, 8);
        uint8_t nb_read_6 = bitstream_read( stream, 8, &current_byte, false );
        check_reading_process( nb_read_6, 8);
    }

    return jpeg;
}

// Cette fonction initialise un descripteur JPEG vide.
struct jpeg_desc *jpeg_desc_create( const char *filename ) {

    struct jpeg_desc* jpeg = malloc(sizeof(struct jpeg_desc));
    jpeg->valid = true;
    jpeg->filename = filename;


    struct Colour_Component compo = { 0, 0, 0, 1, 1, 0, 0, 0, false };
    jpeg->frametype = 0;
    jpeg->height = 0;
    jpeg->width = 0;
    jpeg->restart_interval = 0;
    jpeg->components_number = 0;

    for (uint32_t i = 0 ; i < 4 ; i++) {
         jpeg->Quantization_Tables[i] = quantization_create_table( );
    }

    for (uint32_t i = 0 ; i < 4 ; i++) {
        jpeg->Huffman_DC_Tables[i] = huffman_create_empty_table( );
    }
    for (uint32_t i = 0 ; i < 4 ; i++) {
        jpeg->Huffman_AC_Tables[i] = huffman_create_empty_table( );
    }
    for (uint32_t i = 0 ; i < 3 ; i++) {
        jpeg->components[i] = compo;
    }

    jpeg->start_of_selection = 0;
    jpeg->end_of_selection = 63;
    jpeg->successive_approximation_high = 0;
    jpeg->successive_approximation_low = 0;
    return jpeg;
}

// Cette fonction crée une table de quantification vide.
struct Quantization_Table quantization_create_table( ) {
    uint32_t* point = malloc(64 * sizeof(uint32_t));
    struct Quantization_Table table_quant = { point, false };
    return table_quant;
}

// Cette fonction vérifie si On a Un JPEG valide.
void jpeg_check_errors_1( struct jpeg_desc *jpeg, uint32_t last_byte, uint32_t current_byte ) {

    if ( (int)last_byte == EOF || (int)current_byte == EOF ) {
        printf("Erreur : On est arrivé à la fin du fichier\n");
        jpeg->valid = false;
    }

    if ( last_byte != 0xFF ) {
        printf("Erreur : On attend un marqueur \n");
        jpeg->valid = false;
    }
}

// Cette fonction vérifie si on a un JPEG invalide.
struct jpeg_desc *jpeg_check_errors_2( struct jpeg_desc *jpeg, struct bitstream *stream, uint32_t current_byte ) {

    switch ( current_byte )
    {
        case 0xD8 : printf("Erreur : JPG insupportable \n"); break;

        case 0xD9 : printf("Erreur : EOI détecté avant SOI \n"); break;

        case 0xCC : printf("Erreur : Le mode de codage arithmétique est insupportable\n"); break;

        default :
            if ( current_byte >= 0xC1 && current_byte <= 0xCF )  {
                printf("Erreur : Le marqueur SOF est insupportable \n");
            }
            else if ( current_byte >= 0xD0 && current_byte <= 0xD7 ) {
                printf("Erreur : RSTx détecté avant SOS\n");
            }
            else {
                printf("Erreur : marqueur inconnu\n");
            }
    }

    jpeg->valid = false;
    fclose( bitstream_get_pointer_to_file(stream));

    return jpeg;
}

const char *jpeg_get_filename(const struct jpeg_desc *jpeg) {
    return jpeg->filename;
}

struct bitstream *jpeg_get_bitstream(const struct jpeg_desc *jpeg) {
    return jpeg->bit_stream;
}

uint8_t jpeg_get_nb_quantization_tables(const struct jpeg_desc *jpeg) {
    uint8_t counter = 0;
    for ( uint8_t i = 0; i < 4; i++ ) {
        if ( jpeg->Quantization_Tables[i].set ) {
            counter += 1;
        }
    }
    return counter;
}

uint8_t *jpeg_get_quantization_table(const struct jpeg_desc *jpeg, uint8_t index) {
    uint8_t *pointer = calloc(64, sizeof(uint8_t));
    for ( uint8_t i = 0; i < 64; i++ ) {
        pointer[i] = jpeg->Quantization_Tables[index].pointer_to_table[i];
    }
    return pointer;

}

uint8_t jpeg_get_nb_huffman_tables(const struct jpeg_desc *jpeg, enum sample_type acdc) {
    uint8_t counter = 0;
    if ( acdc == AC ) {
        for ( uint8_t i = 0; i < 4; i++ ) {
            if ( huffman_get_set_value( jpeg->Huffman_AC_Tables[i]) ) {
                counter += 1;
            }
        }
    }
    else if ( acdc == DC ) {
        for ( uint8_t i = 0; i < 4; i++ ) {
            if ( huffman_get_set_value( jpeg->Huffman_DC_Tables[i]) ) {
                counter += 1;
            }
        }
    }
    return counter;
}

struct huff_table *jpeg_get_huffman_table(const struct jpeg_desc *jpeg, enum sample_type acdc, uint8_t index) {
    if ( acdc == AC ) {
        return jpeg->Huffman_AC_Tables[index];
    }
    else if ( acdc == DC ) {
        return jpeg->Huffman_DC_Tables[index];
    }
    printf(" Il y a un souci avec jpeg_get_huffman_table, on voue renvoie une table vide\n");
    return huffman_create_empty_table ( );
}

uint16_t jpeg_get_image_size(struct jpeg_desc *jpeg, enum direction dir) {
    if ( dir == H ) {
        return jpeg->width;
    }
    else if ( dir == V ) {
        return jpeg->height;
    }
    printf(" Il y a un souci avec jpeg_get_image_size\n");
    return 255;
}

uint8_t jpeg_get_nb_components(const struct jpeg_desc *jpeg) {
    return jpeg->components_number;
}

uint8_t jpeg_get_frame_component_id(const struct jpeg_desc *jpeg, uint8_t frame_comp_index) {
    for ( uint8_t i = 0; i < jpeg->components_number; i++) {
        if ( jpeg->components[i].SOF_reading_order == frame_comp_index ) {
            return jpeg->components[i].component_identifiant;
        }
    }
    printf(" Il y a un souci avec jpeg_get_frame_component_id\n");
    return 255;
}

uint8_t jpeg_get_frame_component_sampling_factor(const struct jpeg_desc *jpeg, enum direction dir, uint8_t frame_comp_index) {
    for ( uint8_t i = 0; i < jpeg->components_number; i++) {
        if ( jpeg->components[i].component_identifiant == frame_comp_index ) {
            if ( dir == H ) {
                return jpeg->components[i].horizontal_sampling_factor;
            }
            else if ( dir == V ) {
                return jpeg->components[i].vertical_sampling_factor;
            }
        }
    }
    printf(" Il y a un souci avec jpeg_get_frame_component_sampling_factor\n");
    return 255;
}

uint8_t jpeg_get_frame_component_quant_index(const struct jpeg_desc *jpeg, uint8_t frame_comp_index) {
    for ( uint8_t i = 0; i < jpeg->components_number; i++) {
        if ( jpeg->components[i].SOF_reading_order == frame_comp_index ) {
            return jpeg->components[i].table_index;
        }
    }
    printf(" Il y a un souci avec jpeg_get_frame_component_quant_index\n");
    return 255;
}

uint8_t jpeg_get_scan_component_id(const struct jpeg_desc *jpeg, uint8_t scan_comp_index) {
    for ( uint8_t i = 0; i < jpeg->components_number; i++) {
        if ( jpeg->components[i].SOS_reading_order == scan_comp_index ) {
            return jpeg->components[i].component_identifiant;
        }
    }
    printf(" Il y a un souci avec jpeg_get_scan_component_id\n");
    return 255;
}


uint8_t jpeg_get_scan_component_huffman_index(const struct jpeg_desc *jpeg, enum sample_type acdc, uint8_t scan_comp_index) {
    for ( uint8_t i = 0; i < jpeg->components_number; i++) {
        if ( jpeg->components[i].component_identifiant == scan_comp_index ) {
            if ( acdc == AC ) {
                return jpeg->components[i].Huffman_AC_Table_index;
            }
            else if ( acdc == DC ) {
                return jpeg->components[i].Huffman_DC_Table_index;
            }
        }
    }
    printf(" Il y a un souci avec jpeg_get_scan_component_huffman_index\n");
    return 255;
}

// Cette fonction libère la mémoire destinée au descripteur JPEG
void jpeg_close(struct jpeg_desc *jpeg) {
    free(jpeg);
}

// Cette fonction permet de vérifier si on a lu le bon nombre de bits.
void check_reading_process( uint8_t nb_read_practically, uint8_t nb_read_theorically ) {
    if (nb_read_practically == nb_read_theorically) {
        // printf("On a lu le nombre souhaité de bits\n");
    }
    else {
        // printf("Il y a un problème dans la lecture des bits\n");
    }
}
