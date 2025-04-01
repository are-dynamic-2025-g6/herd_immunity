import random
import numpy as np
population = 100 # le nombre d'individus
taux_infection = 0.05 # le taux d'infection
taux_immunité = 0.05 #taux d'immunité
taux_de_recuperation = 0.08 # taux de recuperation
nb_infecte = 5 # nbre de personne infecté a l'etat initiale
# 1 pour une personne sensible 2 infecté et 3 immunisé
def creer_monde(lign, col, population):
    a = np.zeros((lign, col), dtype=int)
    nb_sensibles = population - nb_infecte  # Le reste sont des sensibles
    individus = [1] * nb_sensibles + [2] * nb_infecte
    random.shuffle(individus)
    i = 0
    #print(individus)
    for x in range(lign):
        for y in range(col):
            a[x, y] = individus[i]
            i=i+1
    return a
grille = creer_monde(10,10,100)
print(creer_monde(10,10,100))

def liste_voisins(tableau,lign,col, x, y):
    voisins = [] 
    for i in range(-1, 2):  
        for j in range(-1, 2):  
            if i != 0 and j != 0:
                nx, ny = x + i, y + j
            if (0 <= nx < lign  and 0 <= ny < col):
                voisins.append((nx, ny, tableau[nx][ny]))  

    return voisins

def mettre_a_jour_grille(grille,lign,col):
    nouv_gril = grille.copy()
    for x in range(lign):
        for y in range(col):
            if grille[x, y] == 2: 
                if random.random() < taux_immunité:
                    nouv_gril[x, y] = 3
            elif grille[x, y] == 3:
                 if random.random() < taux_de_recuperation:
                    nouv_gril[x, y] = 1
            elif grille[x, y] == 1 :  
                voisins = liste_voisins(grille,lign,col,x, y)
                for nx, ny,_ in voisins: 
                    if grille[nx, ny] == 2: 
                        if random.random() < taux_infection:
                            nouv_gril[x, y] = 2
                            break
                        
    return nouv_gril
print(mettre_a_jour_grille(grille,10,10))