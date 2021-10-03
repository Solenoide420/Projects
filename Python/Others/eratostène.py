import pygame as pg
from time import sleep

N = 100

def eratostène(n):
    """Donne la liste des premiers < n"""
    ints = list(range(2, n))
    k = 0
    while ints[k] <= n ** 0.5:
        div = ints[k]
        f = lambda x : x % div == 0 if x != div else False
        suppr = list(map(f, ints))
        ints = [ints[i] for i in range(len(ints)) if not suppr[i]]
        k += 1
    return ints

DIM = N, N

screen = pg.display.set_mode(DIM)

def affichage():
    n = DIM[0]
    prem = pg.Surface((1, 1)) ; prem.fill((255, 0, 0))
    non_prem = pg.Surface((1, 1)) ; non_prem.fill((0, 0, 0))
    erat = eratostène(n*n)
    for i in range(n):
        for j in range(n):
            nbr = i * n +j
            if nbr in erat:
                screen.blit(non_prem, (j, i))
            else:
                screen.blit(prem, (j, i))

if __name__ == '__main__':
    affichage()
    pg.display.flip()
    sleep(2)
    pg.quit()
