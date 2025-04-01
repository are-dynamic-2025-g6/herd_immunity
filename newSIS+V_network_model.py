

import networkx as nx  # Pour créer et manipuler les graphes
import matplotlib.pyplot as plt  # Pour visualiser le graphe
import matplotlib.patches as mpatches  # Pour la légende colorée
import random  # Pour les tirages aléatoires
import ipywidgets as widgets  # Pour créer des sliders interactifs
from IPython.display import display  # Pour afficher l'interface dans un notebook

# --- Définition des états ---
S, I, V = 0, 1, 2  # Susceptible, Infecté, Vacciné

# --- Paramètres par défaut ---
default_N = 100
default_initial_infected = 5
default_beta = 0.3  # Probabilité de transmission
default_gamma = 0.1  # Probabilité de guérison
default_p_vaccine = 0.01  # Probabilité de vaccination
default_steps = 50

# --- Initialisation du réseau ---
def initialize_graph(N, initial_infected):
    G = nx.watts_strogatz_graph(N, k=4, p=0.1)  # Réseau petit monde : liens locaux + aléatoires
    for node in G.nodes:
        G.nodes[node]['state'] = S  # Tous les noeuds sont initialement susceptibles
    infected_nodes = random.sample(list(G.nodes), initial_infected)  # Infecter quelques noeuds
    for node in infected_nodes:
        G.nodes[node]['state'] = I
    return G

# --- Obtenir la couleur de chaque noeud selon son état ---
def get_node_colors(G):
    color_map = {
        S: "blue",
        I: "red",
        V: "gold"
    }
    return [color_map[G.nodes[n]['state']] for n in G.nodes]

# --- Mise à jour des états des noeuds ---
def update_states(G, beta, gamma, p_vaccine):
    new_states = {}  # Temporaire pour stocker les modifications
    for node in G.nodes:
        current = G.nodes[node]['state']
        if current == S:
            if random.random() < p_vaccine:
                new_states[node] = V
            else:
                neighbors = list(G.neighbors(node))
                if any(G.nodes[n]['state'] == I for n in neighbors):
                    if random.random() < beta:
                        new_states[node] = I
        elif current == I:
            if random.random() < gamma:
                new_states[node] = S
    for node, state in new_states.items():
        G.nodes[node]['state'] = state  # Appliquer les nouveaux états

# --- Fonction de simulation avec animation ---
def interactive_simulation(N, initial_infected, beta, gamma, p_vaccine, steps):
    G = initialize_graph(N, initial_infected)
    pos = nx.spring_layout(G, seed=42, k=0.3)  # Disposition claire des noeuds

    fig, ax = plt.subplots(figsize=(8, 6))
    plt.ion()

    legend_patches = [
        mpatches.Patch(color='blue', label='S: Susceptible'),
        mpatches.Patch(color='red', label='I: Infected'),
        mpatches.Patch(color='gold', label='V: Vaccinated'),
    ]

    for step in range(steps):
        ax.clear()
        colors = get_node_colors(G)
        nx.draw(G, pos, node_color=colors, with_labels=False, node_size=120, ax=ax)
        ax.set_title(f"SIS+V Network Simulation\nStep {step}")
        ax.legend(handles=legend_patches, loc='upper right', fontsize='small')
        plt.pause(0.3)
        update_states(G, beta, gamma, p_vaccine)

    plt.ioff()
    plt.show()

# --- Interface interactive ---
N_slider = widgets.IntSlider(value=default_N, min=20, max=300, step=10, description='Population N:')
infected_slider = widgets.IntSlider(value=default_initial_infected, min=1, max=50, step=1, description='Initial I:')
beta_slider = widgets.FloatSlider(value=default_beta, min=0.0, max=1.0, step=0.01, description='Taux infection:')
gamma_slider = widgets.FloatSlider(value=default_gamma, min=0.0, max=1.0, step=0.01, description='Taux guérison:')
vaccine_slider = widgets.FloatSlider(value=default_p_vaccine, min=0.0, max=0.2, step=0.005, description='Taux vaccin:')
steps_slider = widgets.IntSlider(value=default_steps, min=10, max=200, step=10, description='Étapes:')

# Organisation des widgets dans l'interface
ui = widgets.VBox([N_slider, infected_slider, beta_slider, gamma_slider, vaccine_slider, steps_slider])

# Liaison des valeurs des sliders avec la fonction de simulation
out = widgets.interactive_output(interactive_simulation, {
    'N': N_slider,
    'initial_infected': infected_slider,
    'beta': beta_slider,
    'gamma': gamma_slider,
    'p_vaccine': vaccine_slider,
    'steps': steps_slider,
})

# Affichage de l'interface interactive
display(ui, out)
