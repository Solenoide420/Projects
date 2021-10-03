/* 
Test d'une partie
*/

#include <stdio.h>
#include <stdlib.h>

#include "game.h"


int main(int argc, char *argv[]) {
    int _ = system("clear"); _++;

    if (argc != 3 && argc != 1) {
        fprintf(stderr, "Usage: %s\n\t- gage (str)\n\t- nombre de base\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int32_t base = atoi(argv[2]);
    if (argc == 3 && base == 0) {
        fprintf(stderr, "Eh aller, on perd pas son courage et on parie un minimum de %ss svp...\n\n", argv[1]);
        fprintf(stderr, "Usage: %s\n\t- gage (str)\n\t- nombre de base\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    if (argv[1] != NULL) {
        printf("Alors la team, ça parie %u %s%s ?\nBen z'est parti alors\n", base, argv[1], (base > 1) ? "s" : "");
    } else {
        printf("Et z'est parti, juste lez gong");
    }

    int c = 0;
    while (c != '\n' && c != EOF)
    {
        c = getchar();
    }

    game(argv[1], base);
    return EXIT_SUCCESS;
}