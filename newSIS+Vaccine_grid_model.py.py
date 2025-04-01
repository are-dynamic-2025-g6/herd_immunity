

import numpy as np  # Pour manipuler efficacement la grille de cellules
import matplotlib.pyplot as plt  # Pour afficher la grille à chaque étape
import random  
from matplotlib.colors import ListedColormap  
import matplotlib.patches as mpatches  


S, I, V = 0, 1, 2  # Susceptible, Infecté, Vacciné


grid_size = 40       # Taille de la grille (40x40)
infection_prob = 0.3           # Probabilité d'infection par voisin
recovery_rate = 0.1          # Probabilité de guérison (retour à S)
p_vaccine = 0.01     # Probabilité de vaccination spontanée
steps = 100          # Nombre d'étapes de la simulation

# Initialisation de la grille 
def initialize_grid():
    grid = np.full((grid_size, grid_size), S)  # Grille remplie d'états S
    for _ in range(10):  # Place 10 agents infectés au hasard
        x, y = np.random.randint(0, grid_size, 2)
        grid[x, y] = I
    return grid

# Comptage des voisins infectés (avec bords connectés type tore) 
#La grille est pliée :
# gauche <-> droite
# haut <-> bas
def count_infected_neighbors(grid, x, y):
    infected = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # On ne compte pas soi-même
            nx, ny = (x + dx) % grid_size, (y + dy) % grid_size  # Bords connectés
            if grid[nx, ny] == I:
                infected += 1
    return infected


# Mise à jour de la grille pour une étape 
def update_grid(grid):
    new_grid = np.copy(grid)
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x, y] == S:
                if random.random() < p_vaccine:
                    new_grid[x, y] = V
                elif count_infected_neighbors(grid, x, y) > 0 and random.random() < infection_prob:
                    new_grid[x, y] = I
            elif grid[x, y] == I and random.random() < recovery_rate:
                new_grid[x, y] = S
    return new_grid

# Fonction principale pour exécuter la simulation
def run_simulation():
    grid = initialize_grid()  # Grille de départ
    plt.figure(figsize=(6, 6))  # Taille de l'affichage
    cmap = ListedColormap(["blue", "red", "green"])  # Couleurs : S, I, V

    for step in range(steps):  # Boucle de simulation
        plt.clf()  # Nettoie l'affichage précédent
        plt.imshow(grid, cmap=cmap, vmin=0, vmax=2)  # Affiche la grille avec les couleurs
        plt.title(f"Step {step}")  # Titre de l'étape

        # Crée une légende explicative
        legend_patches = [
            mpatches.Patch(color="blue", label='S: Susceptible'),
            mpatches.Patch(color="red", label='I: Infected'),
            mpatches.Patch(color="green", label='V: Vaccinated'),
        ]
        plt.legend(handles=legend_patches, loc='upper right', fontsize='small')

        plt.pause(0.1)  # Petite pause pour animation
        grid = update_grid(grid)  # Mise à jour de l'état

    plt.show()  # Affiche le résultat final


run_simulation()
