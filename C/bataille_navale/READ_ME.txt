+-----------------------------------------------------+
|   Date de début de projet : 20/04/2021              |
|                                                     |
|   Versions :                                        |
|      - v1.0 : 24/04/2021                            |
|                                                     |
|   Chef de projet : Solénoide420_                    |
|   Développeur(s) : Solénoide420_                    |
|                                                     |
|   Titre du projet : Bataille navale                 |
+-----------------------------------------------------+

Utilisation :

Mode sans gage
./bataille.exe

OU

Mode avec gage
./bataille.exe "shot" 2
             ^    ^
             |    -- Nombre de base
             |
      Type de boisson


================----- DESCRIPTION -----================

Objectif :

Une bataille navale, en 1v1, sur le même PC avec affichage sur terminal.
On veut également un système de gage, afin de le transformer en jeu à boire (ou autre) si on veut.


==================----- DEROULE -----==================

## Phase 1 : Placement

-> Placer tous les bâteaux au départ
-> Position d'une extrémité et orientation (puis vérification de la validité)

PUIS 
// -> Possibilité de modifier le placement des bâteaux
// -> Valider le placement


## Phase 2 : Bataille

-> Afficher les deux grilles (celle des bateaux du joueur, celle des cases jouées)
-> Bien notifier la dernière case jouée par l'adversaire

-> Demande de la case à jouer (puis vérification de la validité)

-> Afficher le résultat du bombardement et éventuellement victoire
-> Efface l'écran et demande de passage à l'adversaire

-> L'adversaire valide que c'est lui qui joue avant de boucler


## Phase 3 : Ecran final

-> Afficher les deux grilles, avec les positions tentées
-> Petit écran de victoire kalitati'