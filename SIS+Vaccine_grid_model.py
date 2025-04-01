import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

# 状態定義
S, I, V = 0, 1, 2

# パラメータ
grid_size = 40
beta = 0.3       # 感染確率
gamma = 0.1      # 回復確率
p_vaccine = 0.01 # ワクチン接種確率
steps = 100

# 初期化
def initialize_grid():
    grid = np.full((grid_size, grid_size), S)
    for _ in range(10):  # 初期感染者をランダムに配置
        x, y = np.random.randint(0, grid_size, 2)
        grid[x, y] = I
    return grid

# 近傍の感染者をチェック
def count_infected_neighbors(grid, x, y):
    infected = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % grid_size, (y + dy) % grid_size
            if grid[nx, ny] == I:
                infected += 1
    return infected

# 1ステップの更新
def update_grid(grid):
    new_grid = np.copy(grid)
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x, y] == S:
                if random.random() < p_vaccine:
                    new_grid[x, y] = V
                elif count_infected_neighbors(grid, x, y) > 0 and random.random() < beta:
                    new_grid[x, y] = I
            elif grid[x, y] == I and random.random() < gamma:
                new_grid[x, y] = S
    return new_grid

# 実行
def run_simulation():
    grid = initialize_grid()
    plt.figure(figsize=(6, 6))
    cmap = ListedColormap(["blue", "red", "gold"])  # S, I, V を青・赤・金に
    for step in range(steps):
        plt.clf()
        
        plt.imshow(grid, cmap=cmap, vmin=0, vmax=2)
        plt.title(f"Step {step}")

        # 凡例の追加（注釈）
        legend_patches = [
    mpatches.Patch(color="blue", label='S: Susceptible'),
    mpatches.Patch(color="red", label='I: Infected'),
    mpatches.Patch(color="gold", label='V: Vaccinated'),
]
        plt.legend(handles=legend_patches, loc='upper right', fontsize='small')
        plt.pause(0.1)
        grid = update_grid(grid)
    plt.show()

run_simulation()
