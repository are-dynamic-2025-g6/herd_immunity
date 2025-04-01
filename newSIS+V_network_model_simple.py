
import networkx as nx  # Pour créer et manipuler des réseaux (graphes)
import matplotlib.pyplot as plt  
import matplotlib.patches as mpatches  
import random  


S, I, V = 0, 1, 2  # Susceptible, Infecté, Vacciné


initial_infected = 5  # Nombre de noeuds infectés au départ
infection_prob = 0.3  # Probabilité de transmission de l'infection (contagion)
recovery_rate = 0.1  # Probabilité de guérison d'un infecté
p_vaccine = 0.02  # Probabilité qu'un individu se fasse vacciner
steps = 50  # Nombre d'étapes dans la simulation

G = nx.grid_2d_graph(8, 10)  # Grille 2D, plus lisible pour la visualisation

# --- Initialisation des états des noeuds ---
for node in G.nodes:  # Tous les noeuds sont initialement susceptibles
    G.nodes[node]['state'] = S
infected_nodes = random.sample(list(G.nodes), initial_infected)  # Sélection aléatoire d'infectés
for node in infected_nodes:
    G.nodes[node]['state'] = I  # Ces noeuds commencent infectés

# --- Fonction pour déterminer la couleur de chaque noeud selon son état ---
def get_node_colors(G):
    color_map = {
        S: "skyblue",   # Bleu clair pour susceptible
        I: "crimson",   # Rouge pour infecté
        V: "gold"        # Jaune/or pour vacciné
    }
    return [color_map[G.nodes[n]['state']] for n in G.nodes]  # Liste des couleurs par noeud


def update_states(G):
    new_states = {}  # Stocker les changements d'état
    for node in G.nodes:
        current = G.nodes[node]['state']  # Etat actuel du noeud
        if current == S:
            if random.random() < p_vaccine:
                new_states[node] = V  # Vaccination
            else:
                neighbors = list(G.neighbors(node))  # Voisins du noeud
                if any(G.nodes[n]['state'] == I for n in neighbors):  # Si au moins un voisin est infecté
                    if random.random() < infection_prob:
                        new_states[node] = I  # Infection
        elif current == I:
            if random.random() < recovery_rate:
                new_states[node] = S  # Guérison
    for node, state in new_states.items():  # Applique les changements d'état
        G.nodes[node]['state'] = state

def run_simple_simulation():
    pos = {node: (node[1], -node[0]) for node in G.nodes}  # Coordonnées pour affichage en grille
    fig, ax = plt.subplots(figsize=(7, 5))  # Taille de la fenêtre graphique
    plt.ion()  # Mode interactif ON pour animation

    # Création de la légende avec couleurs
    legend_patches = [
        mpatches.Patch(color='skyblue', label='S: Susceptible'),
        mpatches.Patch(color='crimson', label='I: Infected'),
        mpatches.Patch(color='gold', label='V: Vaccinated'),
    ]

    for step in range(steps):  
        ax.clear()  # Efface le dessin précédent
        colors = get_node_colors(G)  # Couleur par noeud selon son état
        nx.draw(G, pos, node_color=colors, with_labels=False, node_size=300,
                edge_color='lightgray', ax=ax)  # Dessine le graphe
        ax.set_title(f"SIS+V Grid Network (Step {step})")  # Titre
        ax.legend(handles=legend_patches, loc='upper right', fontsize='small')  # Légende
        plt.pause(0.3)  # Pause pour animation
        update_states(G)  # Mise à jour des états

    plt.ioff()  # Mode interactif OFF
    plt.show()  # Affiche le résultat final


run_simple_simulation()
