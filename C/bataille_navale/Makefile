CC = gcc
LD = gcc
CFLAGS = -Wall -Wextra -g -O2 -Iinclude/ -fPIC

all: lib/libbataille.so build-tests

lib/libbataille.so: obj/game.o obj/placement.o obj/bataille.o obj/grille.o 
	$(CC) -shared $^ -o $@

obj/%.o: src/%.c
	$(CC) $(CFLAGS) -c $^ -o $@

build-tests:
	make -C tests/

.PHONY: clean

clean:
	rm -rf obj/*.o lib/libbataille.so
	rm -f bataille
	make -C tests/ clean

