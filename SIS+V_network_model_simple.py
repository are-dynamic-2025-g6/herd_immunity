import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random

# 状態定義
S, I, V = 0, 1, 2

# パラメータ
N = 80
initial_infected = 5
beta = 0.3
gamma = 0.1
p_vaccine = 0.02
steps = 50

# ネットワークの初期化（格子状の構造でシンプルな表示）
G = nx.grid_2d_graph(8, 10)  # 8x10のグリッド構造で見やすく

# 状態の初期化
for node in G.nodes:
    G.nodes[node]['state'] = S
infected_nodes = random.sample(list(G.nodes), initial_infected)
for node in infected_nodes:
    G.nodes[node]['state'] = I

# ノードの色設定
def get_node_colors(G):
    color_map = {
        S: "skyblue",
        I: "crimson",
        V: "gold"
    }
    return [color_map[G.nodes[n]['state']] for n in G.nodes]

# 状態更新
def update_states(G):
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

# シンプルで見やすい描画
def run_simple_simulation():
    pos = {node: (node[1], -node[0]) for node in G.nodes}  # 整列表示
    fig, ax = plt.subplots(figsize=(7, 5))
    plt.ion()

    legend_patches = [
        mpatches.Patch(color='skyblue', label='S: Susceptible'),
        mpatches.Patch(color='crimson', label='I: Infected'),
        mpatches.Patch(color='gold', label='V: Vaccinated'),
    ]

    for step in range(steps):
        ax.clear()
        colors = get_node_colors(G)
        nx.draw(G, pos, node_color=colors, with_labels=False, node_size=300,
                edge_color='lightgray', ax=ax)
        ax.set_title(f"SIS+V Grid Network (Step {step})")
        ax.legend(handles=legend_patches, loc='upper right', fontsize='small')
        plt.pause(0.3)
        update_states(G)

    plt.ioff()
    plt.show()

run_simple_simulation()
