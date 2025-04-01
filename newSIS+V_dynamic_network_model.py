import networkx as nx # Librairie pour la création et manipulation de graphes
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random

SUSCEPTIBLE = 0
INFECTE = 1
VACCINE = 2

# Paramètres fixés
nombre_personnes = 80  # Nombre total de personnes dans le réseau
nombre_infectes_initialement = 5  # Nombre de personnes déjà infectées au début
taux_transmission = 0.3  # Chance de transmission si contact avec un infecté
taux_guerison = 0.1  # Chance de guérison pour un infecté
taux_vaccination = 0.02  # Chance qu'une personne saine se fasse vacciner
taux_reconfiguration_liens = 0.05  # Chance qu'une connexion soit changée
nombre_tours = 50  # Nombre de tours de simulation

# Création du réseau initial 
#crée un réseau aléatoire entre n individus, où chaque lien est ajouté avec une probabilité p.
reseau = nx.erdos_renyi_graph(nombre_personnes, p=0.05)

# Initialisation des états des personnes
for personne in reseau.nodes:
    reseau.nodes[personne]['etat'] = SUSCEPTIBLE # Tout le monde commence sain
personnes_infectees = random.sample(list(reseau.nodes), nombre_infectes_initialement)
for personne in personnes_infectees:
    reseau.nodes[personne]['etat'] = INFECTE # Marquer comme infecté

# Déterminer la couleur des noeuds selon leur état 
def couleurs_personnes(reseau):
    couleurs = {
        SUSCEPTIBLE: "skyblue",
        INFECTE: "crimson",
        VACCINE: "gold"
    }
    return [couleurs[reseau.nodes[p]['etat']] for p in reseau.nodes]

#  Mettre à jour les états des personnes 
def mise_a_jour_etats(reseau):
    changements = {} # Dictionnaire pour stocker les changements à appliquer
    for personne in reseau.nodes:
        etat = reseau.nodes[personne]['etat']
        if etat == SUSCEPTIBLE:
            if random.random() < taux_vaccination:
                changements[personne] = VACCINE # Vaccination spontanée
            elif any(reseau.nodes[voisin]['etat'] == INFECTE for voisin in reseau.neighbors(personne)):
                if random.random() < taux_transmission:
                    changements[personne] = INFECTE  # Infection via un voisin
        elif etat == INFECTE:
            if random.random() < taux_guerison:
                changements[personne] = SUSCEPTIBLE

    # Appliquer les changements d'état
    for personne, nouvel_etat in changements.items():
        reseau.nodes[personne]['etat'] = nouvel_etat

# Modifier dynamiquement les connexions du réseau 
def modifier_connexions(reseau, taux_reconfiguration):
    connexions_a_modifier = [lien for lien in list(reseau.edges) if random.random() < taux_reconfiguration] # Sélection des liens à modifier
    for a, b in connexions_a_modifier:
        reseau.remove_edge(a, b) # Supprimer le lien actuel
        candidats = set(reseau.nodes) - {a} - set(reseau.neighbors(a)) # Chercher un nouveau voisin possible
        if candidats:
            nouveau_voisin = random.choice(list(candidats))  # Choisir un nouveau voisin au hasard
            reseau.add_edge(a, nouveau_voisin)

# Simulation principale 
def simulation():
    position = nx.spring_layout(reseau, seed=42)
    fig, ax = plt.subplots(figsize=(7, 6))
    plt.ion()

    legende = [
        mpatches.Patch(color='skyblue', label='Personne saine'),
        mpatches.Patch(color='crimson', label='Personne infectée'),
        mpatches.Patch(color='gold', label='Personne vaccinée'),
    ]

    for tour in range(nombre_tours):
        ax.clear()
        couleurs = couleurs_personnes(reseau)
        nx.draw(reseau, position, node_color=couleurs, edge_color='lightgray',
                with_labels=False, node_size=100, ax=ax)
        ax.set_title(f"Propagation d'une infection sur réseau dynamique\nTour {tour}")
        ax.legend(handles=legende, loc='upper right', fontsize='small')
        plt.pause(0.3)
        mise_a_jour_etats(reseau)
        modifier_connexions(reseau, taux_reconfiguration_liens)

    plt.ioff()
    plt.show()

#  Lancement 
simulation()
