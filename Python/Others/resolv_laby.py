#!/usr/bin/env python3
"""Solveur de labyrinthe"""

# Idée du programme :

# Construire un arbre ayant le départ comme racine et dont les fils sont les
# cases accessibles (on retient l'ancetre UNIQUE dans cet arbre de chaque noeud)

# Il suffit alors de remonter la lignée de l'arrivée jusqu'au départ pour obtenir le parcours


## Importations
from random import randint
import pygame as pg
import labyrinthe as lab

## Valeurs importantes
TAILLE = 40
DEPART = (0, 0)
ARRIVEE = (TAILLE-1, TAILLE-1)

AFF_PROG = False

## Initialisations
pg.init()
pg.font.init()

## Classes
class File():
    """Classe de file, implémentée par une liste"""

    def __init__(self):
        self.corps = []

    def est_vide(self):
        """Indique si la file est vide"""
        return len(self.corps) == 0

    def enfile(self, elt):
        """Ajoute l'élément à la file"""
        self.corps.append(elt)

    def defile(self):
        """Retourne le premier élément de la file en l'enlevant de celle-ci"""
        if len(self.corps) == 0:
            print("La file est vide")
            return
        else:
            elt = self.corps.pop(0)
            return elt


## Fonctions principales
def init_mat(n, p, val):
    """Initialise une matrice n x p à la valeur donnée"""
    res = []
    for _ in range(n):
        res.append([val]*p)
    return res

def labyrinthe_to_tree(laby, racine):
    """Retourne l'arbre de racine donnée (matrice de pères)"""
    i_rac, j_rac = racine
    vert, hori = laby
    n = len(vert)
    deja_vu = init_mat(n, n, 0)
    ancetre = init_mat(n, n, (-1, -1))

    file = File()
    file.enfile(racine)
    deja_vu[i_rac][j_rac] = 1

    while not file.est_vide():
        i_actu, j_actu = file.defile()

        if i_actu != 0:     # Case du dessus
            if not hori[i_actu-1][j_actu] and not deja_vu[i_actu-1][j_actu]:
                ancetre[i_actu-1][j_actu] = (i_actu, j_actu)
                file.enfile((i_actu-1, j_actu))
                deja_vu[i_actu-1][j_actu] = 1

        if i_actu != n-1:     # Case du dessous
            if not hori[i_actu][j_actu] and not deja_vu[i_actu+1][j_actu]:
                ancetre[i_actu+1][j_actu] = (i_actu, j_actu)
                file.enfile((i_actu+1, j_actu))
                deja_vu[i_actu+1][j_actu] = 1

        if j_actu != 0:     # Case de gauche
            if not vert[i_actu][j_actu-1] and not deja_vu[i_actu][j_actu-1]:
                ancetre[i_actu][j_actu-1] = (i_actu, j_actu)
                file.enfile((i_actu, j_actu-1))
                deja_vu[i_actu][j_actu-1] = 1

        if j_actu != n-1:     # Case de droite
            if not vert[i_actu][j_actu] and not deja_vu[i_actu][j_actu+1]:
                ancetre[i_actu][j_actu+1] = (i_actu, j_actu)
                file.enfile((i_actu, j_actu+1))
                deja_vu[i_actu][j_actu+1] = 1

    return ancetre

def rev_liste(liste):
    """Retourne la liste"""
    res = []
    for i in range(len(liste)-1, -1, -1):
        res.append(liste[i])
    return res

def chemin(lab, départ, arrivee):
    """Retourne la liste des cases a emprunter pour aller de départ à arrivée dans lab"""
    ancetre = labyrinthe_to_tree(lab, départ)
    chemin_rev = [arrivee]
    actu = arrivee

    while not actu == départ:
        i, j = actu
        actu = ancetre[i][j]
        chemin_rev.append(actu)

    return rev_liste(chemin_rev)

## Fonctions d'affichage
def affiche_chemin(chemin, surface, couleur):
    """Affiche le chemin donné sur la surface"""
    vert = pg.Surface((3, 13)) ; vert.fill(couleur)
    hori = pg.Surface((13, 3)) ; hori.fill(couleur)
    actu = chemin[0]

    for k in range(1, len(chemin)):
        suivant = chemin[k]
        trajet = (suivant[0] - actu[0], suivant[1] - actu[1])
        if trajet[1] == 0:
            surface.blit(vert, (10*actu[1] +4, 10*actu[0] + 5*trajet[0] -1))
        if trajet[0] == 0:
            surface.blit(hori, (10*actu[1] + 5*trajet[1] -1, 10*actu[0] + 4))
        actu = suivant


## Boucle principale
def Main(TAILLE):

    screen = pg.display.set_mode((TAILLE*10 + 1, TAILLE*10 + 1))
    timer = pg.time.Clock()

    fond = pg.Surface((TAILLE*10 + 1, TAILLE*10 + 1))
    perso = pg.Surface((5, 5)) ; perso.fill((0, 0, 255))
    CASE, VERT, HORI = lab.init_labyrinthe(TAILLE)
    suppr = 0

    while suppr < TAILLE*TAILLE - 1:
        vert = randint(0, 1)
        if vert:
            lig, col = randint(0, TAILLE - 1), randint(0, TAILLE - 2)
            suppr = suppr + 1 if lab.suppr_mur_vert(CASE, VERT, HORI, lig, col) else suppr
        else:
            lig, col = randint(0, TAILLE - 2), randint(0, TAILLE - 1)
            suppr = suppr + 1 if lab.suppr_mur_hori(CASE, VERT, HORI, lig, col) else suppr
        lab.chargement(VERT, HORI, screen, suppr, TAILLE)
        pg.display.flip()

    lab.affichage(VERT, HORI, fond, (255, 255, 255), TAILLE) ; carré = pg.Surface((9, 9))
    carré.fill((255, 255, 0)) ; fond.blit(carré, (10*DEPART[0] +1, 10*DEPART[1] +1))
    carré.fill((0, 255, 0)) ; fond.blit(carré, (10*ARRIVEE[0] +1, 10*ARRIVEE[1] +1))
    screen.blit(fond, (0, 0))
    pg.display.flip()

    parcours = chemin((VERT, HORI), DEPART, ARRIVEE)
    if not AFF_PROG:
        affiche_chemin(parcours, fond, (255, 0, 0))
        screen.blit(fond, (0, 0))
        pg.display.flip()

    else:
        timer = pg.time.Clock()
        vert = pg.Surface((3, 13)) ; vert.fill((255, 0, 0))
        hori = pg.Surface((13, 3)) ; hori.fill((255, 0, 0))
        actu = parcours[0]

        for k in range(1, len(parcours)):
            timer.tick(5)

            suivant = parcours[k]
            trajet = (suivant[0] - actu[0], suivant[1] - actu[1])
            if trajet[1] == 0:
                fond.blit(vert, (10*actu[1] +4, 10*actu[0] + 5*trajet[0] -1))
            if trajet[0] == 0:
                fond.blit(hori, (10*actu[1] + 5*trajet[1] -1, 10*actu[0] + 4))
            actu = suivant
            screen.blit(fond, (0, 0))
            pg.display.flip()

    while 1:
        pg.display.flip()

        for event in pg.event.get():
            if event.type == 12 or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                return False



## Execution
if __name__ == '__main__':
    Main(TAILLE)
