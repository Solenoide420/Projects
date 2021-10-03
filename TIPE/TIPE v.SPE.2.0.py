# On utilise les corrdonnées sphériques pour placer les points et satellites :
# la longitude et la colatitude (angle depuis le meridien de Greenwich et le pole Nord)

# Distances en km
# Angles en radian

## Importations
import pygame as pg
from math import sin, cos, sqrt, pi
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

## Initialisations
pg.init()
pg.font.init()

font = pg.font.SysFont("Impact", 20)

DIM = 550, 80
screen = pg.display.set_mode(DIM)

## Valeurs importantes
ALT = 20200
ANGLE_DETEC = 82
DIST_DETEC = 24924
MASSE_PLANETE = 5.972e24
RAYON_PLANETE = 6371

G = 6.67430e-11
CSTE_DEG_RAD = pi/180

NECESS = 100000
INIT_SAT = 50
NB_NECESS = 4

## Définition des classes
class Satellite():

    def __init__(self):
        """Initialise un satellite (aléatoirement)"""
        self.cola = randint(0, 180) * CSTE_DEG_RAD
        self.long = randint(0, 359) * CSTE_DEG_RAD
        self.x = (RAYON_PLANETE + ALT) * sin(self.cola) * cos(self.long)
        self.y = (RAYON_PLANETE + ALT) * sin(self.cola) * sin(self.long)
        self.z = (RAYON_PLANETE + ALT) * cos(self.cola)

class Point():

    def __init__(self, cola, long):
        """Initialise un point (en fonction des paramètres donnés)"""
        self.long = long * CSTE_DEG_RAD
        self.cola = cola * CSTE_DEG_RAD
        self.x = RAYON_PLANETE * sin(self.cola) * cos(self.long)
        self.y = RAYON_PLANETE * sin(self.cola) * sin(self.long)
        self.z = RAYON_PLANETE * cos(self.cola)

    def distance(self, sat):
        """Retourne le distance entre le ppoint et le satellite"""
        x_dist = self.x - sat.x
        y_dist = self.y - sat.y
        z_dist = self.z - sat.z
        return hypot3(x_dist, y_dist, z_dist)

    def detecté(self, satellites):
        """Dit si le point en question est détecté"""
        cpt = 0
        for sat in satellites:
            if self.distance(sat) <= DIST_DETEC:
                cpt += 1
            if cpt == NB_NECESS:
                return True
        return False


## Définition des fonctions
def init_points():
    """Retourne la liste de points utilisée pour discrétiser la Terre"""
    pts = []
    for i in range(1, 180):
        for j in range(360):
            pts.append(Point(i, j))
    pts.append(Point(0, 0)) ; pts.append(Point(180, 0))
    return pts

def test(pts, satellites):
    """Teste la configuration de satellites pour chaque point de la Terre"""
    for pt in pts:
        if not pt.detecté(satellites):
            return False
    return True

def hypot3(x, y, z):
    """Retourne la distance cartésienne entre le 0 et la position donnée"""
    return sqrt(x*x + y*y + z*z)

def barre(config, NECESS, actuel, tests):
    """Imporime une barre de chargement sur l'écran"""
    fond = pg.Surface((504, 24)) ; fond.fill((255, 255, 255))
    barre = pg.Surface((int(500*config/NECESS), 20)) ; barre.fill((255, 0, 0))
    screen.blit(fond, (8, 8)) ; screen.blit(barre, (10, 10))
    texte = font.render(str(config)+'/'+str(NECESS), 1, (255, 255, 255))
    screen.blit(texte, (10, 40))
    txt = font.render(str(actuel)+'  '+str(tests), 1, (255, 255, 255)) ; screen.blit(txt, (200, 40))

def affichage3D(pts, sats):
    """Affiche le résultat en 3D de la simulation"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X, Y, Z = [], [], []
    for sat in sats:
        X.append(sat.x) ; Y.append(sat.y) ; Z.append(sat.z)
    ax.scatter(X, Y, Z, color='r')
    cpt = 0
    Xp, Yp, Zp = [], [], []
    for pt in pts:
        cpt += 1
        if cpt % 1000 == 0:
            Xp.append(pt.x) ; Yp.append(pt.y) ; Zp.append(pt.z)
    ax.scatter(Xp, Yp, Zp, color='g')
    plt.show()

## Définition de la boucle principale
def Main(n):
    satellites = [Satellite() for _ in range(n)]
    points = init_points()
    actuel = n
    tests = 0
    config = 0

    while 1:
        for event in pg.event.get():
            if event.type == 12 or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                return points, BEST
        if config == NECESS:
            pg.quit()
            return points, BEST

        enlevé = satellites.pop(0)
        reussi = test(points, satellites)

        if reussi:
            BEST = satellites
            actuel -= 1
            tests = 0
            config = 0
        else:
            satellites.append(enlevé)
            tests += 1

        if tests == actuel:
            tests = 0
            config += 1
            satellites = [Satellite() for _ in range(actuel)]

        screen.fill((0, 0, 0))
        barre(config, NECESS, actuel, tests)
        pg.display.flip()

## Execution
if __name__ == "__main__":
    points, BEST = Main(INIT_SAT)
    affichage3D(points, BEST)
    print(len(BEST))