import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import tkinter as tk
from tkinter import ttk

from matplotlib.patches import Patch



# Definition les etats
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

grid_size = 100  # Taille de population
neigh = 1 

def neighborhood(cell_x, cell_y, neigh):
    """Trouver les voisinages'"""
    neighbors = []
    for dx in range(-neigh, neigh + 1):
        for dy in range(-neigh, neigh + 1):
            if (dx != 0 or dy != 0) and (0 <= cell_x + dx < grid_size) and (0 <= cell_y + dy < grid_size):
                neighbors.append((cell_x + dx, cell_y + dy))
    return neighbors

# Creer la population
grid = np.full((grid_size, grid_size), SUSCEPTIBLE)
infected_positions = np.random.choice(grid_size * grid_size, 40, replace=False)
for pos in infected_positions:
    x, y = divmod(pos, grid_size)
    grid[x, y] = INFECTED

# Configuration de couleur
cmap = mcolors.ListedColormap(["white", "red", "black"])
norm = mcolors.BoundaryNorm([0, 1, 2, 3], cmap.N)

def update(frame):
    global grid
    new_grid = np.copy(grid)
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x, y] == SUSCEPTIBLE:
                neighbors = neighborhood(x, y, neigh)
                for nx, ny in neighbors:
                    if grid[nx, ny] == INFECTED and np.random.rand() < infection_rate.get():
                        new_grid[x, y] = INFECTED
                        break
            elif grid[x, y] == INFECTED:
                if np.random.rand() < recovery_rate.get():
                    new_grid[x, y] = RECOVERED
            elif grid[x, y] == RECOVERED:
                if np.random.rand() < waning_immunity.get():
                    new_grid[x, y] = SUSCEPTIBLE
    grid = new_grid
    im.set_array(grid)
    return [im]

# Interface Tkinter
root = tk.Tk()
root.title("Simulation d'épidémie")

tk.Label(root, text="Transmission rate").pack()
infection_rate = tk.DoubleVar(value=0.3)
infection_slider = ttk.Scale(root, from_=0, to=1, orient='horizontal', variable=infection_rate)
infection_slider.pack()

tk.Label(root, text="Recovery rate").pack()
recovery_rate = tk.DoubleVar(value=0.1)
recovery_slider = ttk.Scale(root, from_=0, to=1, orient='horizontal', variable=recovery_rate)
recovery_slider.pack()

tk.Label(root, text="Waning immunity rate").pack()
waning_immunity = tk.DoubleVar(value=0.5)
waning_slider = ttk.Scale(root, from_=0, to=1, orient='horizontal', variable=waning_immunity)
waning_slider.pack()

def start_animation():
    ani.event_source.start()

def stop_animation():
    ani.event_source.stop()

def reset_simulation():
    global grid
    grid.fill(SUSCEPTIBLE)
    for pos in infected_positions:
        x, y = divmod(pos, grid_size)
        grid[x, y] = INFECTED
    im.set_array(grid)

ttk.Button(root, text="▶ Start", command=start_animation).pack()
ttk.Button(root, text="⏸ Stop", command=stop_animation).pack()
ttk.Button(root, text="🔄 Restart", command=reset_simulation).pack()

# Dessiner le graph
fig, ax = plt.subplots()
im = ax.imshow(grid, cmap=cmap, norm=norm)

# Ajouter la description 
legend_elements = [
    Patch(facecolor="white", edgecolor='black', label="Susceptible"),
    Patch(facecolor="red", edgecolor='black', label="Infected"),
    Patch(facecolor="black", edgecolor='black', label="Recovered")
]
ax.legend(handles=legend_elements, loc="upper right", frameon=True, facecolor="white", edgecolor="black")

#Animation
ani = animation.FuncAnimation(fig, update, frames= 400, interval = 50, blit=False)
plt.show()

root.mainloop()
