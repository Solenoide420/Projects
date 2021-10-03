CC = gcc
CFLAGS = -Wall -Wextra -g -O2 -I../include
# truc cracra pour récupérer le chemin absolu vers le répertoire lib/
LIBDIR = $(shell dirname $(shell find $(shell pwd) | head -n 1))/lib/
LDFLAGS = -Wl,-rpath=$(LIBDIR) -L$(LIBDIR) -lbataille

TESTS = bataille

SRC = $(TESTS:=.c)
OBJ = $(TESTS:=.o)

all: $(TESTS)

bataille: test1.o
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)
	mv bataille ./..

%.o: %.c
	$(CC) $(CFLAGS) -c $^

.PHONY: clean

clean:
	rm -rf *.o *~ $(TESTS)