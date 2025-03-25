import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import ipywidgets as widgets
from IPython.display import display

# 状態定義
S, I, V = 0, 1, 2

# デフォルトパラメータ
default_N = 100
default_initial_infected = 5
default_beta = 0.3
default_gamma = 0.1
default_p_vaccine = 0.01
default_steps = 50

# ネットワークの初期化
def initialize_graph(N, initial_infected):
    G = nx.watts_strogatz_graph(N, k=4, p=0.1)
    for node in G.nodes:
        G.nodes[node]['state'] = S
    infected_nodes = random.sample(list(G.nodes), initial_infected)
    for node in infected_nodes:
        G.nodes[node]['state'] = I
    return G

# ノードの色設定
def get_node_colors(G):
    color_map = {
        S: "blue",
        I: "red",
        V: "gold"
    }
    return [color_map[G.nodes[n]['state']] for n in G.nodes]

# 状態更新
def update_states(G, beta, gamma, p_vaccine):
    new_states = {}
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
        G.nodes[node]['state'] = state

# インタラクティブシミュレーション
def interactive_simulation(N, initial_infected, beta, gamma, p_vaccine, steps):
    G = initialize_graph(N, initial_infected)
    pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=(6, 6))
    plt.ion()

    legend_patches = [
        mpatches.Patch(color='blue', label='S: Susceptible'),
        mpatches.Patch(color='red', label='I: Infected'),
        mpatches.Patch(color='gold', label='V: Vaccinated'),
    ]

    for step in range(steps):
        ax.clear()
        colors = get_node_colors(G)
        nx.draw(G, pos, node_color=colors, with_labels=False, node_size=100, ax=ax)
        ax.set_title(f"SIS+V Network Simulation\nStep {step}")
        ax.legend(handles=legend_patches, loc='upper right', fontsize='small')
        plt.pause(0.3)
        update_states(G, beta, gamma, p_vaccine)

    plt.ioff()
    plt.show()

# ウィジェットUIの作成
N_slider = widgets.IntSlider(value=default_N, min=20, max=300, step=10, description='Population N:')
infected_slider = widgets.IntSlider(value=default_initial_infected, min=1, max=50, step=1, description='Initial I:')
beta_slider = widgets.FloatSlider(value=default_beta, min=0.0, max=1.0, step=0.01, description='Infection β:')
gamma_slider = widgets.FloatSlider(value=default_gamma, min=0.0, max=1.0, step=0.01, description='Recovery γ:')
vaccine_slider = widgets.FloatSlider(value=default_p_vaccine, min=0.0, max=0.2, step=0.005, description='Vaccine p:')
steps_slider = widgets.IntSlider(value=default_steps, min=10, max=200, step=10, description='Steps:')

ui = widgets.VBox([N_slider, infected_slider, beta_slider, gamma_slider, vaccine_slider, steps_slider])
out = widgets.interactive_output(interactive_simulation, {
    'N': N_slider,
    'initial_infected': infected_slider,
    'beta': beta_slider,
    'gamma': gamma_slider,
    'p_vaccine': vaccine_slider,
    'steps': steps_slider,
})

display(ui, out)
