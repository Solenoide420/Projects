## Importations
import os
import sys
import colorama
from random import randint
import time

## Valeurs importantes


## Initialisations
colorama.init()

## Fonctions principales
def init_grille():
    """Retourne la grille de départ du puissance 4"""
    res = []
    for _ in range(6):
        res.append([-1] * 7)
    return res

def indice(elt, liste):
    """Retourne l'indice de l'elt dans la liste"""
    for n, x in enumerate(liste):
        if x == elt:
            return n
    return -1

def ajout(grille, joueur, colonne):
    """Ajoute le pion du joueur à la grille dans la colonne indiquée **EN PLACE** """
    i = 0
    while i < 6 and grille[i][colonne] == -1:
        i += 1
    grille[i-1][colonne] = joueur

def gagne(grille, joueur, colonne):
    """Indique si le joueur a gagné en plaçant son jeton dans la colonne"""
    i = 0
    while i < 6 and grille[i][colonne] == -1:
        i += 1
    ligne = i
    poss = [[(0, -3), (0, -2), (0, -1)], [(0, -2), (0, -1), (0, 1)], [(0, -1), (0, 1), (0, 2)],
            [(0, 1), (0, 2), (0, 3)], [(1, 0), (2, 0), (3, 0)], [(-3, -3), (-2, -2), (-1, -1)],
            [(-2, -2), (-1, -1), (1, 1)], [(-1, -1), (1, 1), (2, 2)], [(1, 1), (2, 2), (3, 3)],
            [(-3, 3), (-2, 2), (-1, 1)], [(-2, 2), (-1, 1), (1, -1)], [(-1, 1), (1, -1), (2, -2)],
            [(1, -1), (2, -2), (3, -3)]]

    for elt in poss:
        suite = 0
        for x, y in elt:
            if -1 < ligne + x < 6 and -1 < colonne + y < 7:
                if grille[ligne + x][colonne + y] != joueur:
                    break
                suite += 1
        if suite == 3:
            return elt
    return False

## Fonctions d'affichage
def imprime_grille(grille):
    """Affiche la grille dans le terminal (en nettoyant le terminal)"""
    os.system('cls')
    print('| 0  1  2  3  4  5  6 |\n|---------------------|')
    for i in range(6):
        ligne = ''
        for j in range(7):
            if grille[i][j] == 0:
                ligne += '\033[41m   \033[40m'
            elif grille[i][j] == 1:
                ligne += '\033[44m   \033[40m'
            else:
                ligne += '   '
        print('|' + ligne + '|\n|' + ligne + '|')
    print('|---------------------|')

## Demandes de jeux
def joue_H(grille, joueur):
    """Demande à un humain de jouer"""
    imprime_grille(grille)
    test = -1
    while 1:
        print("Quelle colonne jouer ? (vous êtes {})".format('bleu' if joueur == 1 else 'rouge'))
        try:
            inp = input()
            test = int(inp)
        except:
            if inp == 'quit':
                quit()
            print('Invalide')
        if -1 < test < 7 and grille[0][test] == -1:
            return test

def joue_O1(grille, joueur):
    """Demande à un ordi aléatoire de jouer"""
    while 1:
        test = randint(0, 6)
        if grille[0][test] == -1:
            return test

## Boucle principale
def Main():
    possibles = ['H', 'O1']
    possibles_f = [joue_H, joue_O1]

    if len(sys.argv) != 3 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("Utilisation:", sys.argv[0], "\nArguments :\n\t- joueur 1")
        print("\t- joueur 2\nLes joueurs disponibles sont : H 'humain' | O1 'ordiT1'")
        sys.exit(1)

    if not (sys.argv[1] in possibles and sys.argv[2] in possibles):
        print("Les joueurs disponibles sont : H 'humain' | O1 'ordiT1'")
        sys.exit(2)

    grille = init_grille()
    joueurs = (indice(sys.argv[1], possibles), indice(sys.argv[2], possibles))
    tour = -1
    joues = 0

    while 1:
        tour = (tour +1) %2
        choix_colonne = possibles_f[joueurs[tour]](grille, tour)
        ajout(grille, tour, choix_colonne)
        imprime_grille(grille)

        est_gagne = gagne(grille, tour, choix_colonne)
        time.sleep(1)
        if bool(est_gagne):
            print("Le joueur", tour+1, "a gagné, félicitations !!")
            return

        joues += 1
        if joues == 42:
            print('Egalité, relancez pour départager ? (y/n)')
            if input() == 'y':
                Main()
            else:
                return

## Execution
if __name__ == '__main__':
    Main()
    time.sleep(5)
    print('jte bez')
    os.system('exit')
