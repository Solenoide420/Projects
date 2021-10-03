# Changer la taille des tuiles en fonction de la taille de la carte demandée
# Ecran de victoire
# Eventuellement, changer les skins parce que en fait c'est pas si ouf que ça

import sys
import os
from random import randint
from time import sleep

import pygame as pg
from pygame.locals import QUIT

pg.init()
pg.font.init()

font = pg.font.SysFont("Impact", 15)
font2 = pg.font.SysFont("francaise", 40)

os.system('cls')

try:
    TAILLE = int(sys.argv[1])
    BOMBES = int(sys.argv[2])
except:
    print("Utilisation:", sys.argv[0], "\nArgument :\n\t- la taille du quadrillage")
    print("\t- le nombre de bombes")
    sys.exit(1)

DIM = (TAILLE*20, TAILLE*20 + 30)
screen = pg.display.set_mode(DIM)

sys.setrecursionlimit(TAILLE*TAILLE)

def init_mat_carre(n, val):
    """Initialise une matrice carrée de taille n a la valeur indiquée"""
    res = []
    for _ in range(n):
        res.append([val]*n)
    return res

def init(TAILLE, BOMBES):
    """Retourne la matrice de la carte et la matrice de cases cachées"""
    carte = init_mat_carre(TAILLE, 0)
    mods = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for _ in range(BOMBES):
        x, y = randint(0, TAILLE-1), randint(0, TAILLE-1)
        while carte[x][y] == 'b':
            x, y = randint(0, TAILLE-1), randint(0, TAILLE-1)
        carte[x][y] = 'b'
        for a, b in mods:
            if -1 < x+a < TAILLE and -1 < y+b < TAILLE:
                try:
                    carte[x+a][y+b] += 1
                except:
                    None
    return carte, init_mat_carre(TAILLE, 1)

def init_affichage(carte):
    """Initialise la surface de fond"""
    fond = pg.Surface((20*TAILLE, 20*TAILLE)) ; fond.fill((100, 100, 100))
    bombe = pg.image.load("Bombe.png").convert_alpha()
    for i in range(TAILLE):
        for j in range(TAILLE):
            nbr = carte[i][j]
            if nbr in [1, 2, 3, 4, 5, 6, 7, 8]:
                str_nbr = font.render(str(nbr), 1, (255, 160 - 20*nbr, 160 - 20*nbr))
                fond.blit(str_nbr, (20*i + 5, 20*j))
            elif nbr == 'b':
                fond.blit(bombe, (20*i, 20*j))
    return fond

def compte_mat(mat, val):
    """Calcule le nombre d'occurences de val dans mat"""
    cpt = 0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == val:
                cpt += 1
    return cpt

def cacher(CACH):
    """Imprime les caches sur l'écran"""
    cach = pg.image.load("Tuile.png").convert_alpha()
    att = pg.image.load("Attention.png").convert_alpha()
    for i in range(TAILLE):
        for j in range(TAILLE):
            if CACH[i][j]:
                screen.blit(cach, (20*i, 20*j + 30))
            if CACH[i][j] == 'a':
                screen.blit(att, (20*i, 20*j + 30))

def decouvrir(CARTE, CACH, i, j):
    """Découvre récursivement la carte à la position donnée"""
    if CACH[i][j] and CARTE[i][j] in [1, 2, 3, 4, 5, 6, 7, 8]:
        CACH[i][j] = 0
        return 0
    elif CACH[i][j] and CARTE[i][j] == 0:
        CACH[i][j] = 0
        mods = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for a, b in mods:
            if -1 < i+a < TAILLE and -1 < j+b < TAILLE:
                decouvrir(CARTE, CACH, i+a, j+b)
        return 0

def afficher_textes(FOND, CACH, CARTE, TAILLE, BOMBES):
    """Affiche les différents textes sur l'écran"""
    bande = pg.Surface((20*TAILLE, 30)) ; bande.fill((0, 0, 0))
    screen.blit(bande, (0, 0))
    drap = compte_mat(CACH, 'a')
    reste = BOMBES - drap
    txt1 = font2.render(str(reste)+'/'+str(BOMBES), 1, (255, 255, 255))

    screen.blit(txt1, (5, 2))

def Main():
    CARTE, CACH = init(TAILLE, BOMBES)
    FOND = init_affichage(CARTE)
    timer = pg.time.Clock()

    screen.blit(FOND, (0, 30))
    cacher(CACH)
    pg.display.flip()

    perdu, gagné, clic, drap, x, y = 0, 0, 0, 0, 0, 0

    while 1:
        timer.tick(30)
        for event in pg.event.get():
            if event.type == QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                return None

        if pg.mouse.get_pressed()[0] == 1:
            clic = 1
            x, y = pg.mouse.get_pos()
            i, j = x // 20, (y - 30)// 20

            if CARTE[i][j] == 'b' and not perdu:
                CACH = init_mat_carre(TAILLE, 0)
                perdu = 1
            else:
                decouvrir(CARTE, CACH, i, j)

            if compte_mat(CACH, 'a') + compte_mat(CACH, 1) == BOMBES and not gagné:
                gagné = 1
                print("Et c'est la win !!!")
                sleep(3)
                pg.quit()
                return


        if perdu and not gagné:
            print('Vous avez perdu... Mais vous pouvez réessayer à tout moment ;)')
            sleep(5)
            pg.quit()
            return

        if pg.mouse.get_pressed()[2] == 1:
            drap = 1
            x, y = pg.mouse.get_pos()
            i, j = x // 20, (y - 30)// 20
            CACH[i][j] = 'a'

        screen.blit(FOND, (0, 30))
        cacher(CACH)
        afficher_textes(FOND, CACH, CARTE, TAILLE, BOMBES)
        pg.display.flip()


if __name__ == '__main__':
    Main()
