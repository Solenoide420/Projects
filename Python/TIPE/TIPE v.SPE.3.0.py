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
MASSE_PLANETE = 5.972e24
RAYON_PLANETE = 6371

G = 6.67430e-11
CSTE_DEG_RAD = pi/180

TMP = 2*RAYON_PLANETE*cos(pi-ANGLE_DETEC*CSTE_DEG_RAD)
DIST_DETEC = 0.5*(TMP + (TMP*TMP - 4*(RAYON_PLANETE**2 - (ALT+RAYON_PLANETE)**2))**0.5)
PERIODE = (((4*pi*pi*((ALT+RAYON_PLANETE)*1000)**3)/(G*MASSE_PLANETE))**0.5) / 3600

NECESS = 10000
INIT_SAT = 50
NB_NECESS = 3
DIV_TMP = 20

TERRE_ENTIERE = 0

## Définition des classes
class Satellite():
    """Classe qui crée un satellite par ses éléments caractéristiques"""

    def __init__(self):
        """Initialise un satellite (aléatoirement)"""
        self.lat_max = randint(0, 90) * CSTE_DEG_RAD
        self.long_init = randint(0, 359) * CSTE_DEG_RAD
        self.tmps = randint(0, int(PERIODE))
        self.cola = self.lat_max * cos(2*pi*self.tmps/PERIODE) - pi/2
        self.long = self.long_init + 2*pi*self.tmps/PERIODE
        self.x = (RAYON_PLANETE + ALT) * sin(self.cola) * cos(self.long)
        self.y = (RAYON_PLANETE + ALT) * sin(self.cola) * sin(self.long)
        self.z = (RAYON_PLANETE + ALT) * cos(self.cola)

    def bouger(self, temps):
        """Simule le mouvement d'un satellite pendant la période temps"""
        self.tmps += temps
        self.cola = self.lat_max * cos(2*pi*self.tmps/PERIODE) - pi/2
        self.long = self.long_init + 2*pi*self.tmps/PERIODE
        self.x = (RAYON_PLANETE + ALT) * sin(self.cola) * cos(self.long)
        self.y = (RAYON_PLANETE + ALT) * sin(self.cola) * sin(self.long)
        self.z = (RAYON_PLANETE + ALT) * cos(self.cola)

class Point():
    """Classe qui crée un point à la surface de la Terre à la position donnée : colat, long"""

    def __init__(self, cola, long):
        """Initialise un point (en fonction des paramètres donnés)"""
        self.long = long * CSTE_DEG_RAD
        self.cola = cola * CSTE_DEG_RAD
        self.x = RAYON_PLANETE * sin(self.cola) * cos(self.long)
        self.y = RAYON_PLANETE * sin(self.cola) * sin(self.long)
        self.z = RAYON_PLANETE * cos(self.cola)

    def distance(self, sat):
        """Retourne le distance entre le point et le satellite"""
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

#
## Définition des fonctions
def init_points():
    """Retourne la liste de points utilisée pour discrétiser la totalité de la Terre"""
    pts = []
    for i in range(1, 180):
        for j in range(360):
            pts.append(Point(i, j))
    pts.append(Point(0, 0)) ; pts.append(Point(180, 0))
    return pts

def init_points2():
    """Retourne la liste de points utilisée pour discrétiser la Terre sur la bande [-60, 70]"""
    pts = []
    for i in range(20, 151):
        for j in range(360):
            pts.append(Point(i, j))
    return pts

def test(pts, satellites):
    """Teste la configuration de satellites pour chaque point de la Terre"""
    for pt in pts:
        if not pt.detecté(satellites):
            return False
    for k in range(len(satellites)):
        for i in range(k):
            test_x = satellites[k].x == satellites[i].x
            test_y = satellites[k].y == satellites[i].y
            test_z = satellites[k].z == satellites[i].z
            if test_x and test_y and test_z:
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
    txt = font.render(str(actuel)+'  '+str(tests), 1, (255, 255, 255)) ; screen.blit(txt, (100, 40))

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
        if cpt % 950 == 0:
            Xp.append(pt.x) ; Yp.append(pt.y) ; Zp.append(pt.z)
    ax.scatter(Xp, Yp, Zp, color='g')
    plt.show()

def verif_rotation(n):
    """Affiche la trajectoire du satellite avec n points sur la période"""
    sat = Satellite()
    X, Y, Z = [0], [0], [0]
    interv = PERIODE/n
    for _ in range(n):
        sat.bouger(interv)
        X.append(sat.x) ; Y.append(sat.y) ; Z.append(sat.z)
    fig = plt.figure()
    ax = ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X, Y, Z, color='r')
    plt.show()

def rotation(satellites, temps):
    """Fait rotationner la totalité des satellites"""
    for sat in satellites:
        sat.bouger(temps)

def test_temporel(pts, satellites, PERIODE, DIV_TMP):
    """Teste la configuration de satellites sur une période"""
    INTERV = PERIODE/DIV_TMP
    for _ in range(DIV_TMP):
        if not test(pts, satellites):
            return False
        rotation(satellites, INTERV)
    return True

def hex_bis(n):
    """Retourne la valeur hexa décimale de n sur 2 chiffres"""
    res = hex(n).upper()
    return res[2:] if len(res) == 4 else '0'+ res[2:]

def color_hexa(R, G, B):
    """Donne la représentation de la couleur en hexadécimal"""
    res = '#' + hex_bis(R) + hex_bis(G) + hex_bis(B)
    return res.upper()

def affichage_temporel(pts, sats):
    """Crée un affichage permattant de montrer les trajectoires des satellites"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    cpt = 0
    Xp, Yp, Zp = [], [], []
    for pt in pts:
        cpt += 1
        if cpt % 950 == 0:
            Xp.append(pt.x) ; Yp.append(pt.y) ; Zp.append(pt.z)
    ax.scatter(Xp, Yp, Zp, color='g')
    for sat in sats:
        X, Y, Z = [], [], []
        col = color_hexa(randint(0, 255), randint(0, 255), randint(0, 255))
        for _ in range(DIV_TMP):
            X.append(sat.x) ; Y.append(sat.y) ; Z.append(sat.z)
            sat.bouger(PERIODE/DIV_TMP)
        ax.scatter(X, Y, Z, color=col)
    plt.show()

#
## Définition de la boucle principale
def Main(n):
    satellites = [Satellite() for _ in range(n)]
    points = init_points() if TERRE_ENTIERE else init_points2()
    BEST = satellites
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
        reussi = test_temporel(points, satellites, PERIODE, DIV_TMP)

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

#
## Execution
if __name__ == "__main__":
    points, BEST = Main(INIT_SAT)
    affichage3D(points, BEST)

##if __name__ == "__main__":
##    verif_rotation(40)
##
##pg.quit()