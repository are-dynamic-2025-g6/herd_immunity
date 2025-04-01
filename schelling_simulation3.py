import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

# パラメータ設定
GRID_SIZE = 20  # グリッドのサイズ
EMPTY_RATIO = 0.2  # 初期の空白の割合
THRESHOLDS = [0.3, 0.5, 0.7]  # 不満閾値を変える

# エージェントの定義
EMPTY, RED, BLUE = 0, 1, 2

# グリッドの初期化
def initialize_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    agents = [RED] * ((GRID_SIZE * GRID_SIZE) // 2) + [BLUE] * ((GRID_SIZE * GRID_SIZE) // 2)
    random.shuffle(agents)

    idx = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if random.random() > EMPTY_RATIO:
                grid[i, j] = agents[idx]
                idx += 1
    return grid

# 近隣の異種エージェントの割合を計算
def calculate_dissimilarity(grid, x, y):
    if grid[x, y] == EMPTY:
        return 0
    agent_type = grid[x, y]
    neighbors = [grid[i, j] for i in range(max(0, x-1), min(GRID_SIZE, x+2))
                              for j in range(max(0, y-1), min(GRID_SIZE, y+2))
                              if (i, j) != (x, y) and grid[i, j] != EMPTY]
    
    return sum(1 for n in neighbors if n != agent_type) / len(neighbors) if neighbors else 0

# 近くの空き地を探す（Moore 近傍: 8マス以内）
def find_nearby_empty(grid, x, y):
    empty_spaces = [(i, j) for i in range(max(0, x-1), min(GRID_SIZE, x+2))
                              for j in range(max(0, y-1), min(GRID_SIZE, y+2))
                              if grid[i, j] == EMPTY]
    return random.choice(empty_spaces) if empty_spaces else None

# エージェントの移動（近くの空き地のみ移動可能）
def move_agents(grid, threshold):
    new_grid = np.copy(grid)
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x, y] in [RED, BLUE] and calculate_dissimilarity(grid, x, y) > threshold:
                new_pos = find_nearby_empty(grid, x, y)
                if new_pos:
                    new_grid[new_pos] = grid[x, y]
                    new_grid[x, y] = EMPTY  # もともといた場所を空にする
    return new_grid

# シミュレーションをアニメーションで表示
def run_animation(threshold, ax):
    grid = initialize_grid()

    def update(frame):
        nonlocal grid
        grid = move_agents(grid, threshold)
        ax.clear()
        ax.imshow(grid, cmap="coolwarm", vmin=0, vmax=2)
        ax.set_title(f"THRESHOLD = {threshold}, Step = {frame}")

    ani = animation.FuncAnimation(fig, update, frames=50, interval=200, repeat=False)
    return ani

# 3つの THRESHOLD を比較
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

animations = []
for i, threshold in enumerate(THRESHOLDS):
    animations.append(run_animation(threshold, axes[i]))

plt.tight_layout()
plt.show()
