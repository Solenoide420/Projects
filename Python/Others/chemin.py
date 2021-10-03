# L'objectif est d'aller d'un point à un autre d'une grille en prenant le plus court chemin
#
# -> Algo du labyrinthe n'est plus efficace car il n'y a pas unicité du chemin

# Carte donnée sous la forme d'une matrice avec des 1 pour les obstacles

# Implémentation de l'algorithme " pathfinding A* "

## Importations
from random import randint
import pygame as pg
from time import sleep

## Valeurs importantes
TAILLE = 100


## Initialisations
pg.init()
screen = pg.display.set_mode((TAILLE, TAILLE))

## Classes
class File():
    """Classe de file, implémentée par une liste"""

    def __init__(self):
        self.corps = []

    def est_vide(self):
        return len(self.corps) == 0

    def enfile(self, elt):
        self.corps.append(elt)

    def defile(self):
        if len(self.corps) == 0:
            print("La file est vide")
        else:
            x = self.corps.pop(0)
            return x

## Fonctions principales
def init_mat(n, p, val):
    """Initialise une matrice n x p à la valeur donnée"""
    res = []
    for _ in range(n):
        res.append([val]*p)
    return res

def vol_oiseau(carte, arrivée):
    """Retourne la matrice des distances à vol d'oiseau de chaque point à l'arrivée"""
    x, y = len(carte), len(carte[0])
    i_arr, j_arr = arrivée
    res = init_mat(x, y, 0)
    for i in range(x):
        for j in range(y):
            res[i][j] = round(((i - i_arr)**2 + (j - j_arr)**2)**0.5, 4)
    return res

def mini(a, b):
    """Retourne le minimum en supposant que -1 représente +infini"""
    if a < 0:
        return b
    if b < 0:
        return a
    return min(a, b)

def dist_depart(carte, nouveau, dist):
    """Actualise la matrice des distances pour les cases accessibles depuis le nouveau"""
    x, y = len(carte), len(carte[0])
    i_new, j_new = nouveau
    for i in range(-1, 2):
        for j in range(-1, 2):
            if -1 < i_new + i < x and -1 < j_new + j < y and not carte[i_new+i][j_new+j]:
                if abs(i) + abs(j) == 1:
                    dist[i_new+i][j_new+j] = mini(dist[i_new+i][j_new+j], dist[i_new][j_new] + 1)
                elif abs(i) + abs(j) == 2:
                    dist[i_new+i][j_new+j]=mini(dist[i_new+i][j_new+j], dist[i_new][j_new] + 1.4142)
    return dist

def choix_case(carte, deja_vus, vol, dist):
    """Choisit la nouvelle case à explorer"""
    x, y = len(carte), len(carte[0])
    i_min, j_min = -1, -1
    minim = -1
    for i in range(x):
        for j in range(y):
            access = not (carte[i][j] or deja_vus[i][j])
            if access and dist[i][j] != -1 and (vol[i][j]+dist[i][j]<minim or minim == -1):
                minim = vol[i][j] + dist[i][j]
                i_min, j_min = i, j
    return (i_min, j_min)

def rev_list(liste):
    """Retourne la liste donnée en argument"""
    res = []
    for k in range(len(liste)-1, -1, -1):
        res.append(liste[k])
    return res

def retrouve_chemin(dist, arrivée, départ):
    """Retourne le chemin entre départ et arrivée ayant la matrice des distances"""
    x, y = len(dist), len(dist[0])
    i_arr, j_arr = i_act, j_act = arrivée
    i_dep, j_dep = départ
    inv_res = [(i_arr, j_arr)]
    while not (i_act, j_act) == départ:
        minim = -1 ; i_sui, j_sui = -1, -1
        for i in range(-1, 2):
            for j in range(-1, 2):
                access = -1 < i_act +i < x and -1 < j_act +j < y and dist[i_act +i][j_act +j] != -1
                if access and (dist[i_act+i][j_act+j] < minim or minim == -1):
                    minim = dist[i_act + i][j_act + j]
                    i_sui, j_sui = i_act + i, j_act + j
        i_act, j_act = i_sui, j_sui
        inv_res.append((i_act, j_act))
    return rev_list(inv_res)

def plus_court_chemin(carte, départ, arrivée):
    x, y = len(carte), len(carte[0])
    vol = vol_oiseau(carte, arrivée)
    dist = init_mat(x, y, -1)
    deja_vus = init_mat(x, y, 0)

    i_act, j_act = départ
    dist[i_act][j_act] = 0
    deja_vus[i_act][j_act] = 1

    while not (i_act, j_act) == arrivée:
        dist = dist_depart(carte, (i_act, j_act), dist)
        i_act, j_act = choix_case(carte, deja_vus, vol, dist)
        deja_vus[i_act][j_act] = 1

    return retrouve_chemin(dist, arrivée, départ)


## Fonctions d'affichage
def fond_carte(carte):
    """Retourne une surface sur laquelle on a affiché la carte"""
    x, y = len(carte), len(carte[0])
    fond = pg.Surface((x, y)) ; fond.fill((255, 255, 255))
    pix = pg.Surface((1, 1))  ;  pix.fill((  0,   0,   0))
    for i in range(x):
        for j in range(y):
            if carte[i][j]:
                fond.blit(pix, (i, j))
    return fond

def affiche_dep_arr(depart, arrivee, surface):
    """Affiche le départ et l'arrivée sur la surface"""
    pix = pg.Surface((3, 3)) ; pix.fill((0, 255, 0))
    x_dep, y_dep = depart
    x_arr, y_arr = arrivee
    surface.blit(pix, (x_dep, y_dep))
    surface.blit(pix, (x_arr, y_arr))

def chemin(chemin, surface):
    """Imprime le chemin sur la surface donnée"""
    pix = pg.Surface((1, 1)) ; pix.fill((255, 0, 0))
    for elt in chemin:
        i, j = elt
        surface.blit(pix, (i, j))


## Boucle principale
def Main():
    carte = init_mat(TAILLE, TAILLE, 0)
    for _ in range(int(TAILLE ** 1.8)):
        carte[randint(0, TAILLE -1)][randint(0, TAILLE -1)] = 1
    fond = fond_carte(carte)

    screen.blit(fond, (0, 0))
    pg.display.flip()

    depart = 0, 0
    arrivee = TAILLE -1, TAILLE -1
    affiche_dep_arr(depart, arrivee, screen)
    pg.display.flip()

    chemin(plus_court_chemin(carte, depart, arrivee), screen)
    pg.display.flip()
    sleep(10)

    pg.quit()
    print('OK')


## Execution
if __name__ == '__main__':
    Main()
