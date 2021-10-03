#!/usr/bin/env python3
"""
Module de mise en mosaique d'image en partant de toutes les images disponibles dans le fichier
"""
# pylint: disable=C0321, C0200, E1101, C0103

## Importations
from os import system
import sys
import glob
import cv2
import numpy as np

## Fonctions principales
def init_mat(dim, val):
    """Initialise une matrice de dim donnée à la valeur donnée"""
    return [[val] * dim[1] for _ in range(dim[0])]

def importer(image):
    """Importe l'image donnée en argument"""
    img = cv2.imread(image)
    res = init_mat((len(img), len(img[0])), 0)
    for i in range(len(img)):
        for j in range(len(img[0])):
            res[i][j] = img[i][j]
    return res

def redimensionner(img, taille):
    """Redimensionne l'image pour que sa largeur soit taille"""
    dim_fin = int(len(img) * taille /len(img[0])), taille
    redm = len(img[0]) // taille
    res = init_mat(dim_fin, 0)
    for i in range(dim_fin[0]):
        for j in range(dim_fin[1]):
            red, gre, blu = 0, 0, 0
            for x in range(redm):
                for y in range(redm):
                    r_pix, g_pix, b_pix = img[i*redm + x][j*redm + y]
                    red += r_pix
                    gre += g_pix
                    blu += b_pix
            res[i][j] = [round(red/(redm*redm)), round(gre/(redm*redm)), round(blu/(redm*redm))]
    return res

def rogner(image):
    """Rogne l'image afin qu'elle soit carrée et la plus grande possible"""
    long = min(len(image), len(image[0]))
    res = init_mat((long, long), 0)
    for i in range(long):
        for j in range(long):
            res[i][j] = image[len(image)//2 - long//2 + i][len(image[0])//2 - long//2 + j]
    return res

def distance(img1, img2):
    """Calcule la distance entre les deux images de même dimension"""
    norme = 0
    haut, larg = len(img1), len(img1[0])
    for i in range(haut):
        for j in range(larg):
            r_im1, g_im1, b_im1 = img1[i][j]
            r_im2, g_im2, b_im2 = img2[i][j]
            norme += (r_im1 - r_im2) ** 2 + (g_im1 - g_im2) ** 2 + (b_im1 - b_im2) ** 2
    return norme

def sous_image(image, dim, pos):
    """Retourne l'image rognée à la dimension donnée avec le coin hg donné"""
    res = init_mat(dim, 0)
    x, y = pos
    for i in range(dim[0]):
        for j in range(dim[1]):
            res[i][j] = image[x + i][y + j]
    return res

def indice_minimum(liste):
    """Retourne l'indice du minimum de la liste"""
    ind, mini = 0, liste[0]
    for k, elt in enumerate(liste):
        if elt < mini:
            ind, mini = k, elt
    return ind

def choix_vignette(reference, images):
    """Choisit l'image la plus proche, selon la norme, de la référence dans la liste d'images"""
    normes = list(map(lambda x: distance(reference, x), images))
    return indice_minimum(normes)

def mosaique(image, images):
    """Retourne la matrice de la mosaique avec des vignettes carrées dans images"""
    taille_vig = len(images[0])
    x, y = len(image)//taille_vig, len(image[0])//taille_vig
    res = init_mat((x, y), -1)
    dim = taille_vig, taille_vig
    for i in range(x):
        if i % (x//10) == (x//10)-1:
            print('#', end='', flush=True)
        for j in range(y):
            pos = i*taille_vig, j*taille_vig
            res[i][j] = choix_vignette(sous_image(image, dim, pos), images)
    return res

def image_finale(image, choisies, images, tai):
    """Retourne la matrice représentant l'image formée par la mosaique d'images"""
    haut, larg = len(image), len(image[0])

    for i in range(haut):
        if i % (haut//10) == 0:
            print('#', end='', flush=True)
        for j in range(larg):
            if i < len(choisies) * tai and j < len(choisies[0]) * tai:
                image[i][j] = images[choisies[i//tai][j//tai]][i - tai*(i // tai)][j - tai*(j // tai)]

    return image

## Fonctions pour la sauvegarde
def matrice_to_nmatrix(liste):
    """Transforme une matrice non prise en charge par np.matrix en matrice numpy"""
    haut, larg = len(liste), len(liste[0])
    res = np.full(shape=(haut, larg, 3), dtype=np.uint8, fill_value=0)
    for i in range(haut):
        if i % (haut//10) == 0:
            print('#', end='', flush=True)
        for j in range(larg):
            for k in range(3):
                res[i][j][k] = liste[i][j][k]
    return res

## Boucle principale
def main():
    """`"""
    system('cls')
    if len(sys.argv) != 5 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("Utilisation:", sys.argv[0], "\nArguments :\n\t- chemin relatif vers dossier images")
        print("\t- extension des images\n\t- l'image à mosaiquer\n\t- la taille des 'pixels'")
        print(len(sys.argv))
        sys.exit(1)

    try:
        doss_img, nom_img, exten, taille = sys.argv[1], sys.argv[3], sys.argv[2], int(sys.argv[4])
        noms_images = glob.glob('{}/*.{}'.format(doss_img, exten))
        print("Images prises en compte : ", len(noms_images), '\t\t(interruption : Ctrl + C)')
        print('Importation...             |', end='', flush=True)
        image = importer(nom_img)
        images = []
        for k in range(len(noms_images)):
            if k % (len(noms_images)//10) == 0:
                print('#', end='', flush=True)
            images.append(importer(noms_images[k]))
    except ValueError:
        print("Entrer une taille valide")
        sys.exit(2)
    except TypeError:
        print("Nom de l'image ou dossier des images invalide")
        sys.exit(3)

    print("|\nAdaptation...              |", end='', flush=True)
    image = rogner(image)
    for k in range(len(images)):
        images[k] = redimensionner(rogner(images[k]), taille)
        if k % (len(images)//10) == 0:
            print('#', end='', flush=True)

    print("|\nMosaiquage...              |", end='', flush=True)
    choisies = mosaique(image, images)

    print('|\nFormation...               |', end='', flush=True)
    finale = image_finale(image, choisies, images, taille)
    del image, images

    print('|\nNumpysation (de merde)...  |', end='', flush=True)
    finale = matrice_to_nmatrix(finale)

    print('|\nExportation...')
    cv2.imwrite(f"{doss_img}/{nom_img[:-4]}_mosaique.jpg", finale)

    print(f'Terminé\nImage créée : {doss_img}/{nom_img[:-4]}_mosaique.jpg dans le fichier')

## Execution
if __name__ == '__main__':
    main()
