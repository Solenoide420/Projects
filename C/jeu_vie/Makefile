CC=gcc
LD=gcc

CFLAGS = -Wall -Wextra -std=c99 -Iinclude -g
LDFLAGS =

SRC_FILES = $(wildcard src/*.c)
OBJ_FILES = $(patsubst src/%.c, obj/%.o, $(SRC_FILES))


all: la_vie

la_vie: $(OBJ_FILES)
	$(LD) $(OBJ_FILES) $(LDFLAGS) -o $@ -lm

obj/%.o: src/%.c
	$(CC) -c $(CFLAGS) $< -o $@

.PHONY: clean

clean:
	rm -rf la_vie $(OBJ_FILES)