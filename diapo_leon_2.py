
################################################################################
# Fichier 2 : 22:05.py
################################################################################

import matplotlib.pyplot as plt  # pour tracer courbes et barres
import numpy as np               # tableaux numériques, calculs vectoriels
import random                    # tirages aléatoires
import pandas as pd              # structures tabulaires (DataFrame) pour analyse

################################################################################
# PARAMÈTRES GLOBAUX
################################################################################
rows, cols, num_agents = 6, 6, 21
infection_prob_S, infection_prob_V = 0.6, 0.1  # proba infection S ou V
initial_infection_rate = 0.1                  # fraction initiale infectée
vaccination_base_rate, vaccination_max_rate = 0.0025, 0.35  # taux de vacc. de base et max
immune_after_steps, lose_immunity_steps = 14, 20  # acquérir/ perdre immunité
vaccine_decay_rate = 0.2       # décroissance efficacité vaccinale
external_interval = 50         # ré-intro externe tous les 50 tours
block_threshold = 0.4          # blocage si >40% infectés

# Codes d’états (caractères uniques pour chaque état)
SUSCEPTIBLE, INFECTED, VACCINATED, IMMUNE, BLOCKED = 'S','I','V','R','X'

################################################################################
# CLASSE Agent
# But : stocker l’état et gérer le déplacement selon zones bloquées
# Entrée : id (int), x,y (coords), state (str)
# Sortie : mise à jour de x,y via move()
################################################################################
class Agent:
    def __init__(self, id, x, y, state=SUSCEPTIBLE):
        self.id = id               # identifiant (0…num_agents-1)
        self.x, self.y = x, y      # position sur la grille
        self.state = state         # état initial
        self.infected_step = None  # tour où devient infecté
        self.immune_step = None    # tour où devient immunisé
        self.vaccine_effectiveness = 1.0  # facteur entre 0 et 1

    def move(self, blocked):
        # Définir vecteurs de déplacement possibles (N,S,O,E)
        deltas = [(-1,0),(1,0),(0,-1),(0,1)]
        options = []
        for dx, dy in deltas:
            nx, ny = self.x + dx, self.y + dy
            # vérification des bornes
            if 0 <= nx < rows and 0 <= ny < cols:
                # si infecté, rester dans zone bloquée uniquement
                if self.state == INFECTED and (nx,ny) not in blocked:
                    continue
                # si pas infecté, éviter les zones bloquées
                if self.state != INFECTED and (nx,ny) in blocked:
                    continue
                options.append((nx, ny))
        # Choix aléatoire parmi les options valides
        if options:
            self.x, self.y = random.choice(options)

################################################################################
# FONCTION initialize_agents
# Entrée : aucune
# Sortie : liste d’agents avec positions non chevauchantes
# But : peupler la grille
################################################################################
def initialize_agents():
    agents, used = [], set()
    while len(agents) < num_agents:
        x, y = random.randrange(rows), random.randrange(cols)
        if (x,y) in used:  # éviter doublons
            continue
        state = INFECTED if random.random() < initial_infection_rate else SUSCEPTIBLE
        a = Agent(len(agents), x, y, state)
        if state == INFECTED:
            a.infected_step = 0  # horodatage de l’infection
        agents.append(a)
        used.add((x, y))
    return agents

################################################################################
# FONCTION update_states
# Entrée : agents, tour t, probabilities inf_S, inf_V
# Sortie : blocked (ensemble de positions bloquées)
# But : appliquer infection, guérison, vaccination, blocage
################################################################################
def update_states(agents, t, inf_S, inf_V):
    infected_positions = [(a.x, a.y) for a in agents if a.state == INFECTED]
    blocked = set()
    # Blocage si proportion infectés > seuil
    if len(infected_positions)/num_agents > block_threshold:
        for ix, iy in infected_positions:
            for dx in range(-2,3):
                for dy in range(-2,3):
                    if abs(dx)+abs(dy) <= 2:
                        bx, by = ix+dx, iy+dy
                        if 0<=bx<rows and 0<=by<cols:
                            blocked.add((bx, by))
    # Taux vacc. accéléré lors des pics
    vac_rate = min(vaccination_max_rate,
                   vaccination_base_rate + len(infected_positions)/num_agents * 0.05)
    for a in agents:
        # Logique d’infection et vaccination
        if a.state == SUSCEPTIBLE:
            if any(abs(a.x-ix)+abs(a.y-iy)==1 for ix,iy in infected_positions):
                if random.random() < inf_S:
                    a.state, a.infected_step = INFECTED, t
            elif random.random() < vac_rate:
                a.state, a.immune_step = VACCINATED, t
        elif a.state == VACCINATED:
            a.vaccine_effectiveness *= (1 - vaccine_decay_rate)
            if any(abs(a.x-ix)+abs(a.y-iy)==1 for ix,iy in infected_positions):
                if random.random() < inf_V * (1 - a.vaccine_effectiveness):
                    a.state, a.infected_step = INFECTED, t
        elif a.state == INFECTED and t - a.infected_step >= immune_after_steps:
            a.state, a.immune_step = IMMUNE, t
        elif a.state == IMMUNE and t - a.immune_step >= lose_immunity_steps:
            a.state = SUSCEPTIBLE
    return blocked

################################################################################
# FONCTION simulate
# Entrée : nombre de tours
# Sortie : pandas.DataFrame des vagues (start,end,peak,duration)
# But : détecter chaque vague et compiler les données pour analyse
################################################################################
def simulate(steps=1000):
    agents = initialize_agents()
    inf_S, inf_V = infection_prob_S, infection_prob_V
    records = []
    active = False; start = peak = 0
    for t in range(steps):
        blocked = update_states(agents, t, inf_S, inf_V)
        count = sum(a.state == INFECTED for a in agents)
        if count > 0:
            if not active:
                active, start, peak = True, t, count
            else:
                peak = max(peak, count)
        elif active:
            records.append({'start':start,'end':t,'peak':peak,'duration':t-start})
            active = False
        # Réintroduction externe au besoin
        if count == 0 and t % external_interval == 0:
            sus = [a for a in agents if a.state == SUSCEPTIBLE]
            if sus:
                p = random.choice(sus)
                p.state, p.infected_step = INFECTED, t
                inf_S, inf_V = min(1, inf_S*1.1), min(1, inf_V*1.1)
        # Déplacement
        for a in agents:
            a.move(blocked)
    return pd.DataFrame(records)

################################################################################
# EXÉCUTION ET TRACÉS FINAUX
################################################################################
wave_df = simulate(1000)
print(wave_df)
print("Pic moyen:", wave_df['peak'].mean())
print("Durée moyenne:", wave_df['duration'].mean())

plt.figure(figsize=(8,4))
plt.subplot(121)
plt.bar(wave_df.index+1, wave_df['peak'], color='red')
plt.xticks(wave_df.index+1)
plt.xlabel('Vague #')
plt.ylabel('Pic infecté')
plt.title('Pics par vague')

plt.subplot(122)
plt.bar(wave_df.index+1, wave_df['duration'], color='blue')
plt.xticks(wave_df.index+1)
plt.xlabel('Vague #')
plt.ylabel('Durée (tours)')
plt.title('Durée par vague')

plt.tight_layout()
plt.show()
