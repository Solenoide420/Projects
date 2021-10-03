# On utilise les corrdonnées sphériques pour placer les points et satellites :
# la longitude et la colatitude (angle depuis le meridien de Greenwich et le pole Nord)

# Distances en km
# Angles en radian

# Les satellites sont répartis également sur les orbites et leur position est modifiée quand on en
# enlève un pour que ca reste le cas

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
ALT = 23222
ANGLE_DETEC = 82
MASSE_PLANETE = 5.972e24
RAYON_PLANETE = 6371

G = 6.67430e-11
DEG_RAD = pi/180

TMP = 2*RAYON_PLANETE*cos(pi-ANGLE_DETEC*DEG_RAD)
DIST_DETEC = 0.5*(TMP + (TMP*TMP - 4*(RAYON_PLANETE**2 - (ALT+RAYON_PLANETE)**2))**0.5)
PERIODE = (((4*pi*pi*((ALT+RAYON_PLANETE)*1000)**3)/(G*MASSE_PLANETE))**0.5) / 3600

NECESS = 50
INIT_SAT = 50
NB_ORBITES = 3
NB_NECESS = 3
DIV_TMP = 20

TERRE_ENTIERE = 1

## Définition des classes
class Satellite():
    """Classe qui crée un satellite par ses éléments caractéristiques"""

    def __init__(self, lat_m_orbite, long_m_orbite, tmps):
        """Initialise un satellite sur une orbite"""
        self.lat_max = lat_m_orbite
        self.long_init = long_m_orbite
        self.tmps = tmps
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


class Orbite():
    """Classe qui crée une orbite"""

    def __init__(self, nb, lat, long):
        """Initialise l'orbite (aléatoirement), avec nb_sat satellites dessus"""
        self.lat_m = lat
        self.long_m = long
        self.compo = [Satellite(self.lat_m, self.long_m, k*PERIODE/nb) for k in range(nb)]


class Point():
    """Classe qui crée un point à la surface de la Terre à la position donnée : colat, long"""

    def __init__(self, cola, long):
        """Initialise un point (en fonction des paramètres donnés)"""
        self.long = long * DEG_RAD
        self.cola = cola * DEG_RAD
        self.x = RAYON_PLANETE * sin(self.cola) * cos(self.long)
        self.y = RAYON_PLANETE * sin(self.cola) * sin(self.long)
        self.z = RAYON_PLANETE * cos(self.cola)

    def distance(self, sat):
        """Retourne le distance entre le point et le satellite"""
        x_dist = self.x - sat.x
        y_dist = self.y - sat.y
        z_dist = self.z - sat.z
        return hypot3(x_dist, y_dist, z_dist)

    def detecté(self, orbites):
        """Dit si le point en question est détecté"""
        cpt = 0
        for orbite in orbites:
            for sat in orbite.compo:
                if self.distance(sat) <= DIST_DETEC:
                    cpt += 1
                if cpt == NB_NECESS:
                    return True
        return False

#
## Créations des constellations de systèmes en place
GLONASS = [Orbite(8, 65*DEG_RAD, 0*DEG_RAD),     # Altitude = 19130 km
           Orbite(8, 65*DEG_RAD, 120*DEG_RAD),
           Orbite(8, 65*DEG_RAD, 240*DEG_RAD)]

GALILEO = [Orbite(8, 56*DEG_RAD, 0*DEG_RAD),     # Altitude = 23222 km
           Orbite(8, 56*DEG_RAD, 120*DEG_RAD),
           Orbite(8, 56*DEG_RAD, 240*DEG_RAD)]

## Définition des fonctions utiles pour les tests
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

def test(pts, orbites):
    """Teste la configuration de satellites pour chaque point de la Terre"""
    for pt in pts:
        if not pt.detecté(orbites):
            return False
    return True

def hypot3(x, y, z):
    """Retourne la distance cartésienne entre le 0 et la position donnée"""
    return sqrt(x*x + y*y + z*z)

def rotation(satellites, temps):
    """Fait rotationner la totalité des satellites de satellites"""
    for sat in satellites:
        sat.bouger(temps)

def rotation_orbites(orbites, temps):
    """Fait tourner les satellites sur les orbites de orbites"""
    for orbite in orbites:
        rotation(orbite.compo, temps)

def test_temporel(pts, orbites, PERIODE, DIV_TMP):
    """Teste la configuration d'orbites sur une période"""
    INTERV = PERIODE/DIV_TMP
    for _ in range(DIV_TMP):
        if not test(pts, orbites):
            return False
        rotation_orbites(orbites, INTERV)
    return True

def init_orbites(INIT_SAT, NB_ORBITES):
    """Initialise une constellation par des orbites"""
    sat_par_orbite = [INIT_SAT//NB_ORBITES] * NB_ORBITES
    restants = INIT_SAT - sum(sat_par_orbite)
    for k in range(restants):
        sat_par_orbite[k] += 1
    return [Orbite(k, randint(0, 90)*DEG_RAD, randint(0, 359)*DEG_RAD) for k in sat_par_orbite]

#
## Définition de fonctions de vérification de ce qui est fait
def barre(config, NECESS, actuel, tests):
    """Imporime une barre de chargement sur l'écran"""
    fond = pg.Surface((504, 24)) ; fond.fill((255, 255, 255))
    barre = pg.Surface((int(500*config/NECESS), 20)) ; barre.fill((255, 0, 0))
    screen.blit(fond, (8, 8)) ; screen.blit(barre, (10, 10))
    texte = font.render(str(config)+'/'+str(NECESS), 1, (255, 255, 255))
    screen.blit(texte, (10, 40))
    txt = font.render(str(actuel)+'  '+str(tests), 1, (255, 255, 255)) ; screen.blit(txt, (100, 40))

def affichage3D(pts, orbites):
    """Affiche le résultat en 3D de la simulation"""
    liste = ['r', 'b', 'y', 'k']
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    k = 0
    for orbite in orbites:
        X, Y, Z = [], [], []
        for sat in orbite.compo:
            X.append(sat.x) ; Y.append(sat.y) ; Z.append(sat.z)
        X.append(orbite.compo[0].x) ; Y.append(orbite.compo[0].y) ; Z.append(orbite.compo[0].z)
        ax.plot(X, Y, Z, color= liste[k])
        k += 1
    cpt = 0
    Xp, Yp, Zp = [], [], []
    for pt in pts:
        cpt += 1
        if cpt % 950 == 0:
            Xp.append(pt.x) ; Yp.append(pt.y) ; Zp.append(pt.z)
    ax.scatter(Xp, Yp, Zp, color='g')
    plt.show()

def verif_orbite(n):
    """Affiche l'orbite avec n satellites"""
    orb = Orbite(n, randint(0, 90)*DEG_RAD, randint(0, 359)*DEG_RAD)
    X, Y, Z = [0], [0], [0]
    for k in range(n):
        X.append(orb.compo[k].x) ; Y.append(orb.compo[k].y) ; Z.append(orb.compo[k].z)
    fig = plt.figure()
    ax = ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X, Y, Z, color='r')
    plt.show()

def verif_orbite2(n):
    """Affiche l'orbite avec n satellites et verifie la rotation"""
    orb = Orbite(n, randint(0, 90)*DEG_RAD, randint(0, 359)*DEG_RAD)
    interv = PERIODE/20
    fig = plt.figure()
    ax = ax = fig.add_subplot(111, projection='3d')
    for _ in range(20):
        X, Y, Z = [], [], []
        rotation(orb.compo, interv)
        for sat in orb.compo:
            X.append(sat.x) ; Y.append(sat.y) ; Z.append(sat.z)
        ax.scatter(X, Y, Z, color='r')
    plt.show()

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
def Main(INIT_SAT, NB_ORBITES):
    orbites = GALILEO
    points = init_points() if TERRE_ENTIERE else init_points2()
    BEST = orbites
    actuel = best = 24
    tests = 0
    fini = False

    while 1:
        for event in pg.event.get():
            if event.type == 12 or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                return points, BEST

        if fini:
            pg.quit()
            return points, BEST

        enlevé = orbites.pop(0)
        orbites.append(Orbite(len(enlevé.compo)-1, enlevé.lat_m, enlevé.long_m))
        reussi = test_temporel(points, orbites, PERIODE, DIV_TMP)

        if reussi:
            actuel -= 1
            if actuel < best:
                BEST = orbites
                best -= 1
            tests = 0
        else:
            orbites.pop()
            orbites.append(enlevé)
            tests += 1

        if tests == NB_ORBITES:
            fini = True

        screen.fill((0, 0, 0))
        barre(0, NECESS, actuel, tests)
        pg.display.flip()

#
## Execution
if __name__ == "__main__":
    points, BEST = Main(INIT_SAT, NB_ORBITES)
    affichage3D(points, BEST)

##if __name__ == "__main__":
##    verif_orbite(20)
##
##pg.quit()