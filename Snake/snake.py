"""Le jeu snake bien connu"""

## Importations
import sys
from os import system
from random import choice, randint
from time import sleep

import pygame

## Valeurs importantes
try:
    TAILLE = int(sys.argv[1])
except:
    print("Utilisation:", sys.argv[0], "\nArgument :\n\t- la taille du quadrillage")
    sys.exit(1)

try:
    manger = sys.argv[2]
except:
    manger = "pomme.png"

## Initialisations
screen = pygame.display.set_mode((TAILLE*20, TAILLE*20))

## Classes
class Cell():
    """Une cellule pour une liste chainée"""
    def __init__(self, valeur, suivant):
        self.val = valeur
        self.suiv = suivant

    def __eq__(self, cell):
        return self.val == cell.val

    def __str__(self):
        return "{}, {}".format(self.val, ']' if self.suiv is None else str(self.suiv))

class ChList():
    """Une liste chainée"""
    def __init__(self, tete):
        self.hd = tete

    def ajoute(self, elt):
        self.hd = Cell(elt, self.hd)

    def long(self):
        k = 0
        actu = self.hd
        while not actu is None:
            actu = actu.suiv
            k += 1
        return k

    def __str__(self):
        return '[' + str(self.hd)

# Liste chainée pour représenter le serpent (ok compl si elim dernier et verif avance simul)

## Fonctions principales
def init_mat(n, p, val):
    """Initialise une matrice n x p à la valeur donnée"""
    return [[val] * p for _ in range(n)]

def avance_serpent(serpent, new_hd, t_serp):
    """Modifie la liste chainée représentant le serpent à l'étape suivante
    (en vérifiant qu'il peut se déplacer dans cette direction)"""
    x_suiv, y_suiv = new_hd
    if (not -1 < x_suiv < TAILLE) or (not -1 < y_suiv < TAILLE):
        return False

    serpent.ajoute((x_suiv, y_suiv))

    k = 2
    actu = serpent.hd.suiv
    while (not actu is None) and k <= t_serp:
        if actu == serpent.hd:
            return False
        k += 1
        actu = actu.suiv

    if actu is not None:
        actu.suiv = None
    return True

def nouvelle_pomme(serpent, t_serp):
    """Retourne la position de la nouvelle pomme (par la méthode la plus efficace)
    Deux méthodes : - case aléatoire puis vérification disponibilité
                    - liste des cases disponibles puis choix"""
    if t_serp < TAILLE * TAILLE * (3**0.5 -1):    # Méthode 1
        while 1:
            x, y = randint(0, TAILLE-1), randint(0, TAILLE-1)
            actu = serpent.hd

            while not actu is None:
                if (x, y) == actu.val:
                    break
                actu = actu.suiv

            if actu is None:
                return x, y


    else:               # Méthode 2
        vides = init_mat(TAILLE, TAILLE, True)
        actu = serpent.hd

        while not actu is None:
            i, j  = actu.val
            vides[i][j] = False
            actu = actu.suiv

        liste_vides = []
        for i in range(TAILLE):
            for j in range(TAILLE):
                if vides[i][j]:
                    liste_vides.append((i, j))

        return choice(liste_vides) if len(liste_vides) != 0 else False

def quelle_rot(pos, pos_suiv):
    """Donne l'angle de rotation pour la tete du serpent"""
    x, y = pos ; x_s, y_s = pos_suiv
    return -90 * (x_s - x) + 180 * int(y_s - y == 1)


## Fonctions d'affichage
def init_fond(TAILLE):
    """Retourne une surface qui sera le fond du jeu"""
    fond = pygame.Surface((20*TAILLE, 20*TAILLE)) ; fond.fill((0, 0, 0))
    vert = pygame.Surface((2, 20*TAILLE)) ; vert.fill((50, 50, 50))
    hori = pygame.Surface((20*TAILLE, 2)) ; hori.fill((50, 50, 50))
    for i in range(TAILLE+1):
        fond.blit(vert, (20*i -1, 0))
        fond.blit(hori, (0, 20*i -1))
    return fond

def affiche_serpent(serpent, surface):
    """Affiche le serpent sur la surface donnée"""
    i, j = serpent.hd.val
    actu = serpent.hd.suiv
    im_tete = pygame.image.load("tete_serp.png").convert_alpha()
    rot_tete = pygame.transform.rotate(im_tete, quelle_rot((i, j), actu.val))
    surface.blit(rot_tete, (i*20, j*20))

    case = pygame.Surface((20, 20)) ; case.fill((141, 197, 63))
    while not actu.suiv.suiv is None:
        antep = i, j = actu.val
        surface.blit(case, (i*20, j*20))
        actu = actu.suiv

    i, j = actu.val
    im_queu = pygame.image.load("queu_serp.png").convert_alpha()
    rot_queu = pygame.transform.rotate(im_queu, quelle_rot(antep, (i, j)))
    surface.blit(rot_queu, (i*20, j*20))

def affiche_pomme(pomme, surface):
    """Affiche la pomme sur la surface donnée"""
    pase = pygame.image.load(manger).convert_alpha()
    x, y = pomme
    surface.blit(pase, (x*20 +1, y*20 +1))

## Boucle principale
def Main():
    fond = init_fond(TAILLE)
    t_serp = 3
    serpent = ChList(Cell((0, 1), Cell((0, 0), Cell((0, -1), None))))
    direc, rempl = (0, 1), 0
    pomme = nouvelle_pomme(serpent, t_serp)
    timer = pygame.time.Clock()

    while 1:
        timer.tick(3)

        for event in pygame.event.get():
            if event.type == 12 or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                print(f"Abandon : score = {t_serp}")
                return

        keys = pygame.key.get_pressed()
        new_direc = (keys[pygame.K_d] - keys[pygame.K_q], keys[pygame.K_s] - keys[pygame.K_z])
        if new_direc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            direc = new_direc

        old_hd_x, old_hd_y = serpent.hd.val ; dir_x, dir_y = direc
        new_hd = old_hd_x + dir_x, old_hd_y + dir_y

        if new_hd == pomme:
            t_serp += 1
            rempl = 1
            system('cls')
            print('Taille actuelle :', t_serp)

        if not avance_serpent(serpent, new_hd, t_serp):
            print(f"Perdu : score = {t_serp}")
            pygame.quit()
            return

        if rempl:
            pomme = nouvelle_pomme(serpent, t_serp)
            rempl = 0

        if not pomme:
            print('Gagné !! Félicitations')
            pygame.quit()
            return

        screen.blit(fond, (0, 0))
        affiche_serpent(serpent, screen)
        affiche_pomme(pomme, screen)

        pygame.display.flip()

## Execution
if __name__ == '__main__':
    Main()
    sleep(1)
