
population =   100 # le nombre d'individus
taux_infection = 0.05 # le taux d'infection
taux_immunité = 0.02 #taux d'immunité
taux_de_recuperation = 0.01 # taux de recuperation
nb_infecte = 5  # nbre de personne infecté a l'etat initiale
# 1 pour une personne sensible 2 infecté et 3 immunisé
import random
import numpy as np
def creer_monde(lign, col, population, nb_infecte):
    a = np.zeros((lign, col), dtype=int)
    nb_sensibles = population - nb_infecte  # Le reste sont des sensibles
    individus = [1] * nb_sensibles + [2] * nb_infecte
    for x in range(lign):
        for y in range(col):
            a[x, y] = random.choice(individus)
    return a
print(creer_monde(10,10,100,5))
def liste_voisins(tableau, x, y):
    voisins = [] 
    for i in range(-1, 2):  
        for j in range(-1, 2):  
            if i != 0 and j != 0:
                nx, ny = x + i, y + j
            if (0 <= nx < lign and 0 <= ny < col):
                voisins.append((nx, ny, tableau[nx][ny]))  

    return voisins

def mettre_a_jour_grille(grille):
    nouv_grille = grille.copy()
    for x in range(lign):
        for y in range(col):
            if grille[x, y] == 2: 
                if random.random() < taux_immunité:
                    nouv_gril[x, y] = 3
            elif grille[x, y] == r:
                 if random.random() < taux_de_recuperation:
                    nouv_gril[x, y] = 1
            elif grille[x, y] == 1:  
                voisins = liste_voisins(x, y)
                for nx, ny in voisins:
                    if grille[nx, ny] == 2: 
                        if random.random() < taux_infection:
                            nouv_gril[x, y] = 2
                            break
                        
    return nouv_gril