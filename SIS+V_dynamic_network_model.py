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
p_rewire = 0.05  # 再配線の確率
steps = 50

# グラフ初期化（初期はランダムネットワーク）
G = nx.erdos_renyi_graph(N, p=0.05)

# ノードの状態初期化
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
        state = G.nodes[node]['state']
        if state == S:
            if random.random() < p_vaccine:
                new_states[node] = V
            else:
                if any(G.nodes[neigh]['state'] == I for neigh in G.neighbors(node)):
                    if random.random() < beta:
                        new_states[node] = I
        elif state == I:
            if random.random() < gamma:
                new_states[node] = S
    for node, new_state in new_states.items():
        G.nodes[node]['state'] = new_state

# エッジ再構成（動的ネットワーク）
def rewire_edges(G, p_rewire):
    edges_to_rewire = []
    for edge in list(G.edges):
        if random.random() < p_rewire:
            edges_to_rewire.append(edge)
    
    for u, v in edges_to_rewire:
        G.remove_edge(u, v)
        potential_nodes = set(G.nodes) - {u} - set(G.neighbors(u))
        if potential_nodes:
            new_v = random.choice(list(potential_nodes))
            G.add_edge(u, new_v)

# シミュレーション実行
def run_dynamic_network_simulation():
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(7, 6))
    plt.ion()

    legend_patches = [
        mpatches.Patch(color='skyblue', label='S: Susceptible'),
        mpatches.Patch(color='crimson', label='I: Infected'),
        mpatches.Patch(color='gold', label='V: Vaccinated'),
    ]

    for step in range(steps):
        ax.clear()
        colors = get_node_colors(G)
        nx.draw(G, pos, node_color=colors, edge_color='lightgray',
                with_labels=False, node_size=100, ax=ax)
        ax.set_title(f"Dynamic Network SIS+V Simulation\nStep {step}")
        ax.legend(handles=legend_patches, loc='upper right', fontsize='small')
        plt.pause(0.3)
        update_states(G)
        rewire_edges(G, p_rewire)

    plt.ioff()
    plt.show()

run_dynamic_network_simulation()
