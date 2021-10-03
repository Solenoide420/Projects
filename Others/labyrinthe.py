## Importations
import pygame as pg
from random import randint

## Valeurs importantes
TAILLE = 10
JOUE = 1

## Initialisations
pg.init()
pg.font.init()

## Classes

## Fonctions principales
def init_labyrinthe(TAILLE):
    """Retourne les matrices de cases, murs verticaux et murs horizontaux"""
    case, vert, hori = [], [], []
    for i in range(TAILLE):
        ligne = []
        for j in range(TAILLE):
            ligne.append(i*TAILLE + j)
        case.append(ligne)
    for _ in range(TAILLE):
        vert.append([1]*(TAILLE-1))
    for _ in range(TAILLE-1):
        hori.append([1]*TAILLE)
    return case, vert, hori

def remplacer(mat, remplacé, remplacant):
    """Remplace les occurences de remplacé par remplacant dans la matrice"""
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == remplacé:
                mat[i][j] = remplacant

def suppr_mur_hori(case, vert, hori, i, j):
    """Essaye de supprimer le mur horizontal à la position i,j"""
    if case[i][j] == case[i+1][j]:
        return False
    hori[i][j] = 0
    remplacer(case, case[i][j], case[i+1][j])
    return True

def suppr_mur_vert(case, vert, hori, i, j):
    """Essaye de supprimer le mur vertical à la position i,j"""
    if case[i][j] == case[i][j+1]:
        return False
    vert[i][j] = 0
    remplacer(case, case[i][j], case[i][j+1])
    return True

def matrice_homogene(mat):   # Pas utile finalement
    """Dit si la matrice donnée est un multiple de la matrice d'Attila"""
    val = mat[0][0]
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] != val:
                return False
    return True

def collision(fond, x, y):
    """Regarde si il y a collision entre le joueur et un mur du labyrinthe"""
    X = [0, 1, 2, 3, 4, 0, 0, 0, 0, 4, 4, 4, 4, 1, 2, 3]
    Y = [0, 0, 0, 0, 0, 1, 2, 3, 4, 1, 2, 3, 4, 4, 4, 4]
    for k in range(16):
        if fond.get_at((x + X[k], y + Y[k])) == (0, 0, 0):
            return True
    return False

def labyrinthe(TAILLE):
    """Retourne un labyrinthe sous forme du couple de matrices de murs"""
    CASE, VERT, HORI = init_labyrinthe(TAILLE)
    suppr = 0

    while suppr < TAILLE*TAILLE - 1:
        vert = randint(0, 1)
        if vert:
            lig, col = randint(0, TAILLE - 1), randint(0, TAILLE - 2)
            suppr = suppr + 1 if suppr_mur_vert(CASE, VERT, HORI, lig, col) else suppr
        else:
            lig, col = randint(0, TAILLE - 2), randint(0, TAILLE - 1)
            suppr = suppr + 1 if suppr_mur_hori(CASE, VERT, HORI, lig, col) else suppr

    return (VERT, HORI)


## Fonctions d'affichage
def affichage(VERT, HORI, surface, couleur, TAILLE):
    """Imprime les murs du labyrinthe sur la surface"""
    surface.fill(couleur)
    vert = pg.Surface((1, 11)) ; vert.fill((0, 0, 0))
    hori = pg.Surface((11, 1)) ; hori.fill((0, 0, 0))
    for i in range(len(HORI)):
        for j in range(len(HORI[0])):
            if HORI[i][j]:
                surface.blit(hori, (10*j, 10*(i+1)))
    for i in range(len(VERT)):
        for j in range(len(VERT[0])):
            if VERT[i][j]:
                surface.blit(vert, (10*(j+1), 10*i))
    for k in range(TAILLE):
        surface.blit(vert, (0, 10*k)) ; surface.blit(vert, (10*TAILLE, 10*k))
        surface.blit(hori, (10*k, 0)) ; surface.blit(hori, (10*k, 10*TAILLE))
    surface.blit(hori, (10*TAILLE, 10*TAILLE))

def chargement(VERT, HORI, surface, n, TAILLE):
    """Imprime l'écran de chargement sur la surface"""
    affichage(VERT, HORI, surface, (100, 100, 100), TAILLE)
    haut, long = TAILLE//2, (40*TAILLE)//5
    fond = pg.Surface((long+4, haut+4)) ; fond.fill((255, 255, 255))
    barre = pg.Surface(((long*n)//TAILLE**2, haut)) ; barre.fill((255, 0, 0))
    surface.blit(fond, (TAILLE -2, TAILLE*5 - haut//2 - 2))
    surface.blit(barre, (TAILLE, TAILLE*5 - haut//2))

## Boucle principale
def Main(TAILLE):
    screen = pg.display.set_mode((TAILLE*10 + 1, TAILLE*10 + 1))

    timer = pg.time.Clock()
    fond = pg.Surface((TAILLE*10 + 1, TAILLE*10 + 1))
    perso = pg.Surface((5, 5)) ; perso.fill((0, 0, 255))

    CASE, VERT, HORI = init_labyrinthe(TAILLE)
    suppr = 0

    while suppr < TAILLE*TAILLE - 1:
        vert = randint(0, 1)
        if vert:
            lig, col = randint(0, TAILLE - 1), randint(0, TAILLE - 2)
            suppr = suppr + 1 if suppr_mur_vert(CASE, VERT, HORI, lig, col) else suppr
        else:
            lig, col = randint(0, TAILLE - 2), randint(0, TAILLE - 1)
            suppr = suppr + 1 if suppr_mur_hori(CASE, VERT, HORI, lig, col) else suppr
        chargement(VERT, HORI, screen, suppr, TAILLE)
        pg.display.flip()

    affichage(VERT, HORI, fond, (255, 255, 255), TAILLE) ; carré = pg.Surface((9, 9))
    carré.fill((255, 255, 0)) ; fond.blit(carré, (1, 1))
    carré.fill((0, 255, 0)) ; fond.blit(carré, (10*(TAILLE-1) +1, 10*(TAILLE-1)+1))
    x, y = 3, 3

    while 1:
        timer.tick(30)
        screen.blit(fond, (0, 0))

        pressed = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == 12:
                pg.quit()
                return False

        if pressed[27]:
            pg.quit()
            return False

        if (pressed[pg.K_LEFT] or pressed[pg.K_a]) and not collision(fond, x-1, y):
            x -= 1
        if (pressed[pg.K_RIGHT] or pressed[pg.K_d]) and not collision(fond, x+1, y):
            x += 1
        if (pressed[pg.K_UP] or pressed[pg.K_w]) and not collision(fond, x, y-1):
            y -= 1
        if (pressed[pg.K_DOWN] or pressed[pg.K_s]) and not collision(fond, x, y+1):
            y += 1

        screen.blit(perso, (x, y))
        pg.display.flip()

        if x > 10*(TAILLE-1) and y > 10*(TAILLE-1):
            pg.quit()
            return True


## Execution
if __name__ == '__main__':
    while TAILLE <= 71 and JOUE:
        JOUE = Main(TAILLE)
        TAILLE += 2
    print("Vous avez atteient le niveau", (TAILLE-10)//2)
