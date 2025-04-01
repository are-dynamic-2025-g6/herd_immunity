import numpy as np
import matplotlib.pyplot as plt
import random

# パラメータ設定
GRID_SIZE = 20  # グリッドのサイズ
EMPTY_RATIO = 0.2  # 初期の空白の割合
THRESHOLD = 0.3  # 不満閾値（異なる隣人の割合がこれ以上なら移動）

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

# エージェントの移動
def move_agents(grid):
    new_grid = np.copy(grid)
    empty_spaces = list(zip(*np.where(grid == EMPTY)))
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x, y] in [RED, BLUE] and calculate_dissimilarity(grid, x, y) > THRESHOLD:
                if empty_spaces:
                    new_pos = random.choice(empty_spaces)
                    new_grid[new_pos] = grid[x, y]
                    new_grid[x, y] = EMPTY
                    empty_spaces.remove(new_pos)
                    empty_spaces.append((x, y))  # もともとエージェントがいた場所を空白リストに追加
    return new_grid

# シミュレーションの実行
def run_simulation():
    grid = initialize_grid()
    plt.figure(figsize=(6, 6))

    for step in range(50):
        plt.clf()
        plt.imshow(grid, cmap="coolwarm", vmin=0, vmax=2)
        plt.title(f"Step {step+1}")
        plt.pause(0.2)
        
        new_grid = move_agents(grid)
        if np.array_equal(grid, new_grid):  # 変化がなければ終了
            break
        grid = new_grid

    plt.show()

run_simulation()
