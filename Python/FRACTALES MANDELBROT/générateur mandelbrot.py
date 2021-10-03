# Ensemble de Mandelbrot
# (basé sur l'itération de la formule z² + c)

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from math import pi
from random import uniform

# On représente les complexes par un couple (Re, Im)

itérations = 100
taille = 1500
echelle = 0.002
limite_norme = 2
centre = (0, 0)
# Complexité temporelle en O(taille² * itérations)

coin_h_g = (-taille*echelle/2 + centre[0], taille*echelle/2 + centre[1])
phase_R, phase_G, phase_B = uniform(0, 2*pi), uniform(0, 2*pi), uniform(0, 2*pi)

def carré(nbr_cmplx):
    """Retourne le couple représentant le carré du nombre donné"""
    a, b = nbr_cmplx
    return (a*a - b*b, 2*a*b)

def somme(cmplx1, cmplx2):
    """Retourne le couple représentant la somme des deux nombres"""
    a, b = cmplx1
    c, d = cmplx2
    return (a + c, b + d)

def norme(cmplx):
    """Retourne la norme du nombre complexe représenté"""
    a, b = cmplx
    return (a*a + b*b)**0.5

def init_mat(n, p, val):
    """Initialise une matrice n x p à la valeur donnée"""
    res = []
    for _ in range(n):
        res.append([val]*p)
    return res

def couleur(flt, phase_R, phase_G, phase_B):
    """Retourne une couleur selon la gamme générée"""
    R = 255 * np.cos(flt + phase_R)
    G = 255 * np.cos(flt + phase_G)
    B = 255 * np.cos(flt + phase_B)
    return (abs(int(R)), abs(int(G)), abs(int(B)))

def affichage_image(img):
    """Affiche l'image codée dans le tableau"""
    plt.imshow(img)
    plt.show()

def matrice_to_nmatrix(liste):
    """Transforme une matrice non prise en charge par np.matrix en matrice numpy"""
    n, p = len(liste), len(liste[0])
    res = np.full(shape=(n,p,3),dtype=np.uint8, fill_value=0)
    for i in range(n):
        for j in range(p):
            for k in range(3):
                res[i][j][k] = liste[i][j][k]
    return res

def fractale():
    """Affiche l'ensemble de Mandelbrot avec les paramètres donnés initialement"""
    hg_re, hg_im = coin_h_g
    image = init_mat(taille, taille, 0)
    for i in range(taille):
        for j in range(taille):
            actu = (0, 0)
            c = (hg_re + j*echelle, hg_im - i*echelle)
            k, continuer = 0, True
            while k < itérations and continuer:
                actu = somme(carré(actu), c)
                if norme(actu) > limite_norme:
                    image[i][j] = couleur(k/10, phase_R, phase_G, phase_B)
                    continuer = False
                k += 1
            actu_norme = norme(actu)
            if actu_norme <= limite_norme:
                image[i][j] = (0, 0, 0)
        if i % (taille//100) == 0:
            print(i//(taille//100), '%')
    print('Affichage en cours...')
    affichage_image(image)
    return image

##if __name__ == '__main__':
##    IMAGE = fractale()
##    print("CONVERTISSAGE DE L'IMAGE...")
##    imgpil = Image.fromarray(matrice_to_nmatrix(IMAGE))
##    name = "ens_mandelbrot_" + str(centre[0]) + '+' + str(centre[1]) + 'i_' + str(echelle) + '.jpg'
##    print("SAUVEGARDE DE L'IMAGE...")
##    imgpil.save(name)
##    print('FIN')