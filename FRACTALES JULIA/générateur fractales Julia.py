# Fractales de Julia-Fatou
# (basées sur l'itération de la formule z² + c)

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from math import pi
from random import uniform

# On représente les complexes par un couple (Re, Im)

c = (-1.417022285618, 0.0099534)
itérations = 1000
taille = 10000
echelle = 0.0004
centre = (0, 0)
info = 100 if taille > 100 else 10
coin_h_g = (-taille*echelle/2 + centre[0], taille*echelle/2 + centre[1])

limite_norme = 2
# Complexité temporelle en O(taille² * itérations)

# sous le format centre, c, itérations, taille, echelle
a_faire = [((0.8, 0.8), (-0.1225611669, 0.7448617666), 1000, 8000, 0.0002),
           ((-0.8, -0.8), (-0.1225611669, 0.7448617666), 1000, 8000, 0.0002),
           ((0.8, -0.8), (-0.1225611669, 0.7448617666), 1000, 8000, 0.0002),
           ((-0.8, 0.8), (-0.1225611669, 0.7448617666), 1000, 8000, 0.0002)]

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
    """Affiche la fractale de Julia-Fatou associée a c"""
    print("CREATION...    c = ", str(c[0]), ' + ', str(c[1]), 'i')
    hg_re, hg_im = coin_h_g
    image = init_mat(taille, taille, 0)
    for i in range(taille):
        for j in range(taille):
            actu = (hg_re + i*echelle, hg_im - j*echelle)
            k, continuer = 0, True
            while k < itérations and continuer:
                actu = somme(carré(actu), c)
                if norme(actu) > limite_norme:
                    image[j][i] = couleur(k/10, phase_R, phase_G, phase_B)
                    continuer = False
                k += 1
            actu_norme = norme(actu)
            if actu_norme <= limite_norme:
                image[j][i] = (0, 0, 0)
        if i % (taille//info) == 0:
            print(i//(taille//info), '%')
    print('Affichage en cours...')
    affichage_image(image)
    return image

def sauv_fractale(centre, c, itérations, taille, echelle, info):
    """Sauvegarde l'image de la fractale de Julia-Fatou associée a c"""
    print("CREATION...    c = ", str(c[0]), ' + ', str(c[1]), 'i')
    info = 100 if taille > 100 else 10
    hg_re, hg_im = (-taille*echelle/2 + centre[0], taille*echelle/2 + centre[1])
    image = init_mat(taille, taille, 0)
    for i in range(taille):
        for j in range(taille):
            actu = (hg_re + i*echelle, hg_im - j*echelle)
            k, continuer = 0, True
            while k < itérations and continuer:
                actu = somme(carré(actu), c)
                if norme(actu) > limite_norme:
                    image[j][i] = couleur(k/10, phase_R, phase_G, phase_B)
                    continuer = False
                k += 1
            actu_norme = norme(actu)
            if actu_norme <= limite_norme:
                image[j][i] = (0, 0, 0)
        if i % (taille//info) == 0:
            print(i//(taille//info), '%')
    print("CONVERTISSAGE DE L'IMAGE...")
    imgpil = Image.fromarray(matrice_to_nmatrix(image))
    name = "fractale_julia_" + str(c[0]) + '+' + str(c[-1]) + 'i_' + str(centre[0]) + '+'
    name = name + str(centre[1]) + 'i_' + str(echelle) + '3.jpg'
    print("SAUVEGARDE DE L'IMAGE...")
    imgpil.save(name)
    print('TERMINE c = ', str(c[0]), ' + ', str(c[1]), 'i')

##if __name__ == '__main__':
##    IMAGE = fractale()
##    print("CONVERTISSAGE DE L'IMAGE...")
##    imgpil = Image.fromarray(matrice_to_nmatrix(IMAGE))
##    name = "fractale_julia_" + str(c[0]) + '+' + str(c[-1]) + 'i_' + str(centre[0]) + '+'
##    name = name + str(centre[1]) + 'i_' + str(echelle) + '_final.jpg'
##    print("SAUVEGARDE DE L'IMAGE...")
##    imgpil.save(name)
##    print('FIN')

##if __name__ == '__main__':
##    for donnée in a_faire:
##        centre, c, itérations, taille, echelle = donnée
##        sauv_fractale(centre, c, itérations, taille, echelle)