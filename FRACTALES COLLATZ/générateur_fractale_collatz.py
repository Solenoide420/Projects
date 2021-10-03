#!/usr/bin/env python3
"""Fractale de Collatz

(basées sur l'itération de f(z) = 0.25 * (2 + 7z - (2 + 5z)cos(pi z)))"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from math import pi, cos, sin, cosh, sinh
from random import uniform

# On représente les complexes par un couple (Re, Im)

itérations = 100
hauteur, largeur = 5000, 10000
echelle = 0.0004
centre = (-1, 0)
info = 100 if hauteur > 100 else 10
coin_h_g = (-largeur*echelle/2 + centre[0], hauteur*echelle/2 + centre[1])
limite_norme = 10

# Complexité temporelle en O(hauteur * largeur * itérations)

# sous le format centre, itérations, (largeur, hauteur), echelle
a_faire = []

phase_R, phase_G, phase_B = uniform(0, 2*pi), uniform(0, 2*pi), uniform(0, 2*pi)

def cos_cmplx(nbr_cmplx):
    """Retourne le couple représentant le cos du nombre donné"""
    a, b = nbr_cmplx
    return cos(a) * cosh(b), -1 * sin(a) * sinh(b)

def somme(cmplx1, cmplx2):
    """Retourne le couple représentant la somme des deux nombres"""
    a, b = cmplx1
    c, d = cmplx2
    return (a + c, b + d)

def produit(cmplx1, cmplx2):
    """Retourne le couple représentant le produit des deux nombre complexes"""
    a, b = cmplx1
    c, d = cmplx2
    return a*c - b*d, a*d + b*c

def f(cmplx):
    """Retourne le couple représentant l'image de l'argument donné

    f(z) = 0.25 * (2 + 7z - (2 + 5z)cos(pi z))"""
    a, b = cmplx
    mm_d = produit(somme((-2, 0), produit((-5, 0), cmplx)), cos_cmplx(produit((pi, 0), cmplx)))
    parenth = somme((2, 0), somme(produit((7, 0), cmplx), mm_d))
    return produit((0.25, 0), parenth)

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
    """Affiche la fractale de Collatz"""
    print("CREATION...")
    hg_re, hg_im = coin_h_g
    image = init_mat(hauteur, largeur, 0)
    for i in range(largeur):
        for j in range(hauteur):
            actu = (hg_re + i*echelle, hg_im - j*echelle)
            k = 0
            while k < itérations:
                actu = f(actu)
                if norme(actu) > limite_norme:
                    image[j][i] = couleur(k/10, phase_R, phase_G, phase_B)
                    break
                k += 1
            actu_norme = norme(actu)
            if actu_norme <= limite_norme:
                image[j][i] = (0, 0, 0)
        if i % (largeur//info) == 0:
            print(i//(largeur//info), '%')
    print('Affichage en cours...')
    affichage_image(image)
    return image

def sauv_fractale(centre, itérations, taille, echelle, info):
    """Sauvegarde l'image de la fractale de Collatz demandée"""
    print("CREATION...")
    largeur, hauteur = taille
    info = 100 if hauteur > 100 else 10
    hg_re, hg_im = (-largeur*echelle/2 + centre[0], hauteur*echelle/2 + centre[1])
    image = init_mat(hauteur, largeur, 0)
    for i in range(largeur):
        for j in range(hauteur):
            actu = (hg_re + i*echelle, hg_im - j*echelle)
            k = 0
            while k < itérations:
                actu = f(actu)
                if norme(actu) > limite_norme:
                    image[j][i] = couleur(k/10, phase_R, phase_G, phase_B)
                    break
                k += 1
            actu_norme = norme(actu)
            if actu_norme <= limite_norme:
                image[j][i] = (0, 0, 0)
        if i % (largeur//info) == 0:
            print(i//(largeur//info), '%')
    print("CONVERTISSAGE DE L'IMAGE...")
    imgpil = Image.fromarray(matrice_to_nmatrix(image))
    nom = "fractale_collatz_" + str(centre[0]) + '+' + str(centre[1]) + 'i_' + str(echelle) + '.jpg'
    print("SAUVEGARDE DE L'IMAGE...")
    imgpil.save(nom)
    print('TERMINE')

if __name__ == '__main__':
    IMAGE = fractale()
    print("CONVERTISSAGE DE L'IMAGE...")
    imgpil = Image.fromarray(matrice_to_nmatrix(IMAGE))
    nom = "fractale_collatz_" + str(centre[0]) + '+' + str(centre[1]) + 'i_' + str(echelle) + '.jpg'
    print("SAUVEGARDE DE L'IMAGE...")
    imgpil.save(nom)
    print('FIN')

##if __name__ == '__main__':
##    for donnée in a_faire:
##        centre, itérations, taille, echelle = donnée
##        sauv_fractale(centre, itérations, taille, echelle)