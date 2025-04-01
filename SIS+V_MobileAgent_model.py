import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random

# 状態定義
S, I, V = 0, 1, 2

# パラメータ設定
N = 80  # エージェント数
initial_infected = 5
beta = 0.2
gamma = 0.05
p_vaccine = 0.01
steps = 100
infection_radius = 0.05
speed = 0.01

# エージェントの初期化
def initialize_agents():
    agents = []
    for i in range(N):
        x, y = np.random.rand(2)
        angle = random.uniform(0, 2 * np.pi)
        vx, vy = speed * np.cos(angle), speed * np.sin(angle)
        state = S
        agents.append({'pos': np.array([x, y]), 'vel': np.array([vx, vy]), 'state': state})
    infected_indices = random.sample(range(N), initial_infected)
    for i in infected_indices:
        agents[i]['state'] = I
    return agents

# 状態更新
def update_states(agents):
    new_states = [agent['state'] for agent in agents]
    for i, agent in enumerate(agents):
        if agent['state'] == S:
            if random.random() < p_vaccine:
                new_states[i] = V
                continue
            for j, other in enumerate(agents):
                if other['state'] == I:
                    dist = np.linalg.norm(agent['pos'] - other['pos'])
                    if dist < infection_radius and random.random() < beta:
                        new_states[i] = I
                        break
        elif agent['state'] == I:
            if random.random() < gamma:
                new_states[i] = S
    for i in range(N):
        agents[i]['state'] = new_states[i]

# 位置更新（ランダム移動）
def update_positions(agents):
    for agent in agents:
        agent['pos'] += agent['vel']
        # 壁で反射
        for d in range(2):
            if agent['pos'][d] < 0 or agent['pos'][d] > 1:
                agent['vel'][d] *= -1
                agent['pos'][d] = np.clip(agent['pos'][d], 0, 1)

# 描画
def draw_agents(agents, step, ax):
    ax.clear()
    colors = {S: 'skyblue', I: 'crimson', V: 'gold'}
    for agent in agents:
        ax.plot(agent['pos'][0], agent['pos'][1], 'o', color=colors[agent['state']], markersize=6)
    ax.set_title(f"Mobile Agent SIS+V Model\nStep {step}")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    # 凡例
    legend_patches = [
        mpatches.Patch(color='skyblue', label='S: Susceptible'),
        mpatches.Patch(color='crimson', label='I: Infected'),
        mpatches.Patch(color='gold', label='V: Vaccinated'),
    ]
    ax.legend(handles=legend_patches, loc='upper right', fontsize='small')

# シミュレーション実行
def run_mobile_simulation():
    agents = initialize_agents()
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.ion()
    for step in range(steps):
        draw_agents(agents, step, ax)
        plt.pause(0.1)
        update_states(agents)
        update_positions(agents)
    plt.ioff()
    plt.show()

run_mobile_simulation()
