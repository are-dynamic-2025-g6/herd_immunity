import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import ipywidgets as widgets
from IPython.display import display

# 状態定義
S, I, V = 0, 1, 2

# モデル実行関数
def run_simulation_UI(N, beta, gamma, p_vaccine, infection_radius, speed, steps):
    # エージェント初期化
    def initialize_agents():
        agents = []
        for _ in range(N):
            x, y = np.random.rand(2)
            angle = random.uniform(0, 2 * np.pi)
            vx, vy = speed * np.cos(angle), speed * np.sin(angle)
            state = S
            agents.append({'pos': np.array([x, y]), 'vel': np.array([vx, vy]), 'state': state})
        infected_indices = random.sample(range(N), max(1, N // 20))
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
        for i in range(len(agents)):
            agents[i]['state'] = new_states[i]

    # 移動更新
    def update_positions(agents):
        for agent in agents:
            agent['pos'] += agent['vel']
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
        ax.set_title(f"Mobile Agent SIS+V\nStep {step}")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        legend_patches = [
            mpatches.Patch(color='skyblue', label='S: Susceptible'),
            mpatches.Patch(color='crimson', label='I: Infected'),
            mpatches.Patch(color='gold', label='V: Vaccinated'),
        ]
        ax.legend(handles=legend_patches, loc='upper right', fontsize='small')

    # 実行本体
    agents = initialize_agents()
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.ion()
    for step in range(steps):
        draw_agents(agents, step, ax)
        plt.pause(0.05)
        update_states(agents)
        update_positions(agents)
    plt.ioff()
    plt.show()

# ウィジェットUI
N_slider = widgets.IntSlider(value=80, min=10, max=200, step=10, description='Agents N')
beta_slider = widgets.FloatSlider(value=0.2, min=0.0, max=1.0, step=0.01, description='Infect β')
gamma_slider = widgets.FloatSlider(value=0.05, min=0.0, max=1.0, step=0.01, description='Recover γ')
p_vaccine_slider = widgets.FloatSlider(value=0.01, min=0.0, max=0.2, step=0.005, description='Vaccine p')
radius_slider = widgets.FloatSlider(value=0.05, min=0.01, max=0.2, step=0.005, description='Infect radius')
speed_slider = widgets.FloatSlider(value=0.01, min=0.001, max=0.05, step=0.001, description='Speed')
steps_slider = widgets.IntSlider(value=100, min=10, max=300, step=10, description='Steps')

ui = widgets.VBox([
    N_slider, beta_slider, gamma_slider,
    p_vaccine_slider, radius_slider, speed_slider, steps_slider
])

out = widgets.interactive_output(run_simulation_UI, {
    'N': N_slider,
    'beta': beta_slider,
    'gamma': gamma_slider,
    'p_vaccine': p_vaccine_slider,
    'infection_radius': radius_slider,
    'speed': speed_slider,
    'steps': steps_slider
})

display(ui, out)
