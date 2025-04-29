# I Herd You

![Image](<chemin_ou_URL_de_l’image>)

## Description du projet

L’objectif est de comprendre la dynamique de l’immunité de groupe via le comportement collectif des individus, en s’appuyant sur l’explorable « I Herd You ».  
> **À remplir** : le concept, l’intérêt pédagogique et scientifique.

## Règles de la modélisation

#### Modèle simplifié  
Nous représenterons chaque individu par une particule sur une grille ou dans un espace continuel. Les états possibles sont :  
- **S** : Susceptible (non immunisé)  
- **I** : Infecté  
- **R** : Rétabli / Immunisé (post‐infection)  

> **À compléter** : les règles de transition (infection, récupération, immunité, etc.).

## Paramètres du modèle

- **Population** : `<nombre_d’individus>`  
- **Taux de transmission** (`β`) : `<valeur>`  
- **Durée d’infection** : `<nombre_de_tours>`  
- **Durée d’immunité** : `<nombre_de_tours>`  
- **Autres paramètres** : `<…>`

## Les fonctions
1. run_simulation_UI(N, beta, gamma, p_vaccine, infection_radius, speed, steps)
2. initialize_agents()
3. update_states(agents)
4. update_positions(agents)
5. draw_agents(agents, step, ax)


## Le comportement attendu de chaque fonction.
1. run_simulation_UI: C'est la fonction principale qui exécute la simulation. Elle initialise les agents, met à jour leur état et leur position à chaque étape, et affiche la simulation en temps réel avec matplotlib.

2. initialize_agents(): Elle initialise les agents avec une position et une vitesse aléatoires. Elle attribue à certains agents un état initial infecté (I), les autres étant sensibles (S).

3. update_states(agents)
  Elle met à jour l’état de chaque individu :
    +) Un agent sensible (S) peut devenir vacciné (V) avec une probabilité p_vaccine, ou infecté (I) s’il est proche d’un infecté (selon infection_radius) avec une probabilité beta.
    +) Un agent infecté (I) peut redevenir sensible (S) avec une probabilité gamma.
   
4. update_positions(agents): Cette fonction permet de faire bouger chaque agent dans un espace bidimensionnel (un carré de coordonnées entre 0 et 1).

5. draw_agents: Elle affiche graphiquement les agents sur un graphique 2D. Chaque agent est représenté par un point coloré selon son état :
  - Bleu pour sensible (S),
  - Rouge pour infecté (I),
  - Jaune pour vacciné (V).
  - Elle ajoute aussi une légende et le numéro de l’étape (step).


## Liens et ressources

- **Explorable “I Herd You”** : https://www.complexity-explorables.org/explorables/i-herd-you/  
- **Documentation complémentaire** : `<URL ou référence bibliographique>`  
- **Tutoriels / articles** : `<…>`

## Membres du groupe

- Leon Mantani
- Nam Khanh MAI
- Mariama Ba
- Awa Gueye

## Compte rendu hebdomadaire

- **Semaine 1** : ``  
- **Semaine 2** : ``  
- **Semaine 3** : ``  
- …

---
