import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random

# Susceptible,Infected,Vaccinated
S, I, V = 0, 1, 2

# parametre
N = 80  # nombre d'agent
initial_infected = 5 
infection_prob = 0.2
recovery_rate = 0.05
p_vaccine = 0.01
steps = 100 
infection_radius = 0.05
speed = 0.01 #speed des agents


#Placer N agents dans des positionitions aléatoires
#Donner une direction de vitesse aléatoire
#initial_infected: Placer l'agent dans l'état infecté (I)


def initialize_agents():
    agents = []  # stocker les agents
    for i in range(N):  # créer N agents
        x, y = np.random.rand(2)  # Tire deux valeurs aléatoires entre 0 et 1 pour la position (x, y)
        angle = random.uniform(0, 2 * np.pi)  # Choisit un angle de direction aléatoire entre 0 et 2π
        vx, vy = speed * np.cos(angle), speed * np.sin(angle)  # Génère un vecteur de vitesse en 2D pointant dans une direction aléatoire
        state = S  # Initialise l’état de l’agent à “Susceptible”
        agents.append({'position': np.array([x, y]), 'vitesse': np.array([vx, vy]), 'state': state})  # Crée l'agent et l'ajoute à la liste
    infected_indices = random.sample(range(N), initial_infected)  # Sélectionne aléatoirement des N agents pour les infectés
    for i in infected_indices:  # Pour chaque indice choisi
        agents[i]['state'] = I  # Modifie l’état de l’agent à “Infecté”
    return agents  # Retourne la liste complète des agents

#Mettre à jour l’état de chaque agent (S, I ou V) en fonction de la proximité avec des infectés, de la vaccination, et de la récupération.
def update_states(agents):
    new_states = [agent['state'] for agent in agents]  # Copie les états actuels dans une nouvitessele liste
    for i, agent in enumerate(agents):  # Parcourt tous les agents avec leur indice
        if agent['state'] == S:  # Si l’agent est Susceptible
            if random.random() < p_vaccine:  # Tirage aléatoire : vacciné avec une certaine probabilité
                new_states[i] = V  # Change l’état en Vacciné
                continue  # Passe au prochain agent
            for j, other in enumerate(agents):  # Compare avec tous les autres agents
                if other['state'] == I:  # Si l'autre agent est infecté
                    dist = np.linalg.norm(agent['position'] - other['position'])  # Calcule la distance entre les deux agents
                    if dist < infection_radius and random.random() < infection_prob:  # Si assez proche et avec proba d’infection
                        new_states[i] = I  # L’agent devient infecté
                        break  # Arrête de chercher d'autres sources d'infection
        elif agent['state'] == I:  # Si l’agent est infecté
            if random.random() < recovery_rate:  # Peut récupérer avec une certaine probabilité
                new_states[i] = S  # Redevient susceptible (modèle SIS)
    for i in range(N):  # Applique les nouveaux états à la liste des agents
        agents[i]['state'] = new_states[i]


#Faire avancer les agents selon leur vitesse, et les faire rebondir sur les murs si nécessaire.
def update_positions(agents):
    for agent in agents:  # Parcourt tous les agents
        agent['position'] += agent['vitesse']  # Met à jour la position en ajoutant la vitesse
        for d in range(2):  # Pour chaque dimension (x et y)
            if agent['position'][d] < 0 or agent['position'][d] > 1:  # Si l’agent sort de la zone (0 à 1)
                agent['vitesse'][d] *= -1  # Inverse la direction de vitesse (rebond)
                agent['position'][d] = np.clip(agent['position'][d], 0, 1)  # Remet la position à l’intérieur des bornes

#Dessiner la position et l’état de tous les agents sur un graphique, avec des couleurs selon leur statut.
def draw_agents(agents, step, ax):
    ax.clear()  # Efface l’image précédente
    colors = {S: 'skyblue', I: 'crimson', V: 'gold'}  # Définition des couleurs pour chaque état
    for agent in agents:  # Parcourt tous les agents
        ax.plot(agent['position'][0], agent['position'][1], 'o', color=colors[agent['state']], markersize=6)  # Dessine un cercle pour chaque agent
    ax.set_title(f"Mobile Agent SIS+V Model\nStep {step}")  # Titre du graphique
    ax.set_xlim(0, 1)  # Limite horizontale
    ax.set_ylim(0, 1)  # Limite verticale
    ax.set_aspect('equal')  # Garde les proportions égales
    ax.axis('off')  # Cache les axes (pas de grille ni de chiffres)

    # Crée une légende explicative avec les couleurs
    legend_patches = [
        mpatches.Patch(color='skyblue', label='S: Susceptible'),
        mpatches.Patch(color='crimson', label='I: Infected'),
        mpatches.Patch(color='gold', label='V: Vaccinated'),
    ]
    ax.legend(handles=legend_patches, loc='upper right', fontsize='small')  # Affiche la légende

def run_mobile_simulation():
    agents = initialize_agents()  # Initialise les agents avec position, vitesse et état
    fig, ax = plt.subplots(figsize=(6, 6))  # Crée une figure et un axe pour dessiner
    plt.ion()  # Active le mode interactif pour l’animation
    for step in range(steps):  # Pour chaque étape de la simulation
        draw_agents(agents, step, ax)  # Dessine la scène actuelle
        plt.pause(0.1)  # Fait une pause de 0.1 secondes (animation fluide)
        update_states(agents)  # Met à jour les états des agents (infection, vaccin, récupération)
        update_positions(agents)  # Met à jour les positions (déplacement, rebond)
    plt.ioff()  # Désactive le mode interactif
    plt.show()  # Affiche la dernière image en statique

run_mobile_simulation()  # Lance la simulation
