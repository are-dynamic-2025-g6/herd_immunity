# I Herd You

![Image](<chemin_ou_URL_de_l’image>)

## Description du projet

L’objectif est de comprendre la dynamique de l’immunité de groupe via le comportement collectif des individus, en s’appuyant sur l’explorable « I Herd You ».  
> **Le concept** : L’immunité collective également appelée effet de troupeau est une forme de protection indirecte qui ne s’applique qu’aux maladies contagieuses. Il se produit lorsqu’un pourcentage suffisant d’une population est devenu immunisé contre une infection, que ce soit par des infections antérieures ou par la vaccination, que l’agent pathogène transmissible ne peut pas se maintenir dans la population, sa faible incidence réduisant ainsi la probabilité d’infection pour les individus qui n’ont pas d’immunité.

## Règles de la modélisation

#### Modèle simplifié  
Nous représenterons chaque individu par une particule sur une grille ou dans un espace continuel. Les états possibles sont :  
- **S** : Susceptible (non immunisé)  
- **I** : Infecté  
- **R** : Rétabli / Immunisé (post‐infection)  

> **les règles de transition** :
>  - Une fois infectée, la personne peut transmettre la maladie à d’autres personnes sensibles.
>  - Une personne infectée reste contagieuse pendant un certain temps, se rétablit par la suite et redevient vulnérable.
>  - Une personne sensible peut être vacciner et devient ainsi immunisée contre la maladie.

## Paramètres du modèle

- **Population** : `<nombre_d’individus>`  
- **Taux de transmission** (`β`) : `<valeur>`  
- **Durée d’infection** : `<nombre_de_tours>`  
- **Durée d’immunité** : `<nombre_de_tours>`  
- **Autres paramètres** : `<…>`
- **Taux de transmission** : Probabilité qu’une personne infectée transmette la maladie.
- **Taux de guérison** : Probabilité qu’une personne infecté se rétablisse et acquière une immunité.
- **Taux d’immunité décroissant** : c’est le taux de perte de cette immunité.
- **Taux de vaccination** : Probabilité qu’une personne sensible se vaccine.

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
- **Documentation complémentaire** : `[(https://www.complexity-explorables.org/explorables/sirs/)]`  ,`[https://www.complexity-explorables.org/explorables/epidemonic/]`

## Membres du groupe

- Awa Gueye
- Leon Mantani
-  Mariama Ba
- Nam Khanh MAI

## Compte rendu hebdomadaire

> **Semaine 1 (17 février)**
- **Objectif** :
Formation du groupe et discussion sur les thèmes potentiels.

- **Activités** :
Lors de la première séance de travail en groupe, les quatre membres ont présenté chacun les thèmes ou modèles dynamiques qui les intéressaient, en s'appuyant sur ceux publiés sur <nom du site>.
Sur la base des intérêts individuels, nous avons discuté afin de converger vers un modèle accepté par tous.

- **Critères de sélection** :
1.Compréhension théorique du modèle.
2.Possibilité de reproduction en tant que programme.
3.Adéquation avec le niveau de connaissance et de compétence actuel du groupe.

- **Considération scientifique** :
Un modèle trop complexe rendrait la reproduction et l’analyse difficiles, compromettant ainsi la validité du projet.
Par conséquent, nous avons décidé de limiter notre choix aux modèles compréhensibles et reproductibles, en mettant l’accent sur la reproductibilité.

> **Semaine 2 (10 mars)**
- **Activités** :
Le début du travail collaboratif était maladroit en raison de notre rencontre récente.
Avec l'aide des conseils du professeur, nous avons choisi comme thème principal herd immunity.

- **Raison du choix**:
Comparé aux autres thèmes envisagés, le modèle de l’immunité est en lien avec des problématiques des années récentes (ex : récentes épidémies virales).
De plus, il existe plusieurs modèles théoriques liés à ce thème, permettant un apprentissage progressif.

> **Semaine 3 (17 mars)**
- **Activités** :
Après avoir consulté plusieurs modèles liés à l’immunité acquise, nous avons constaté des variations entre eux.

Nous avons donc adopté la stratégie suivante :
1.Répartition : chaque membre est responsable de la reproduction d'un modèle.
2.Mise en place d’un environnement collaboratif sur GitHub.
3.Élaboration d’un planning avec des objectifs à moyen et long terme.

> **Semaine 4 (24 mars)**
- **Activités** :
Début de la reproduction individuelle des modèles attribués.
Du fait de l'interdépendance élevée entre les modèles, nous avons mis l’accent sur :

des communications fréquentes,
le partage régulier des mises à jour de codes et de documents sur GitHub.

> **Semaine 5 (31 mars)**
- **Problèmes rencontrés** :
Nous avons rencontré des difficultés pour reproduire le déplacement des agents dynamiques et l'évolution de la structure du réseau (nœuds et liens).
Cela a entraîné un retard important par rapport au planning initial.

Solutions mises en œuvre :
1.Suspension temporaire des travaux d'implémentation.
2.Priorité à l’analyse et à la compréhension théorique du modèle.
3.Poursuite des travaux réalisables en parallèle.

> **Semaine 6 (7 avril)**
- **Activités et changement de stratégie** :
Pour rattraper le retard, nous avons adopté une approche en deux étapes :

1.Analyser les structures mathématiques, hypothèses et comportements des modèles de base.
2.Reconstruire notre modèle principal (immunité acquise) à partir de ces analyses.

Dans la seconde moitié du projet, nous avons également tenté d’adapter les modèles à des scénarios réels, comme par exemple leur application sur un campus universitaire.

> **Semaine 7 (Jour de la présentation)**
- **Résultats** :
La présentation a été un échec.

Les principales raisons sont les suivantes :
**1. Limites de la communication de groupe**

Tous les membres n'étaient pas natifs francophones, ce qui a freiné les discussions approfondies.
L'absence d’un leadership affirmé a conduit à un flou dans les orientations du projet.
Le respect mutuel excessif a ralenti la prise de décision collective.

**2. Complexité du modèle choisi**

Les modèles de base étaient nombreux et indépendants.
La coordination pour intégrer les reproductions individuelles n’a pas été suffisante.

**3. Raisons techniques**

Manque de maîtrise des outils collaboratifs comme GitHub.
Interruptions dues à des problèmes informatiques.
Trop d’efforts consacrés à l’implémentation, au détriment de l’analyse critique du modèle.

## -Bilan général :
Cette expérience a souligné l'importance cruciale de partager des objectifs clairs et de construire un système de communication solide dans un travail de groupe.
Il est également nécessaire de garder en tête que dans une recherche scientifique, il ne suffit pas de reproduire un modèle : il faut passer par le cycle reproduction → analyse → évaluation → application pour aboutir à une véritable compréhension.

# Message et conseils pour les futurs étudiants :

1.Dès la sélection du thème, formulez clairement par écrit ce que vous voulez accomplir dans ce projet.
2.Faites des répartitions de tâches, mais assurez-vous que chaque tâche soit revue par un autre membre : évitez les travaux totalement isolés.
3.Considérez le plan initial comme provisoire, non définitif.
4.Choisissez votre thème non seulement pour son attrait, mais aussi en évaluant réaliste­ment vos compétences et votre temps disponible.

## Bonne chance à vous !
