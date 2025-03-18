import numpy as np
import matplotlib.pyplot as plt
import random

# パラメータ設定
GRID_SIZE = 20  # グリッドのサイズ
EMPTY_RATIO = 0.2  # 初期の空白の割合
THRESHOLD = 0.3  # 不満閾値
BOID_INFLUENCE = 0.2  # Boidルールの影響度

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

# Boidの影響（周囲のエージェントの方向を考慮）
def boid_influence(grid, x, y):
    neighbors = [(i, j) for i in range(max(0, x-1), min(GRID_SIZE, x+2))
                          for j in range(max(0, y-1), min(GRID_SIZE, y+2))
                          if (i, j) != (x, y) and grid[i, j] != EMPTY]
    if not neighbors:
        return None  # 近くに仲間がいない場合、影響なし
    
    # 近隣のエージェントの平均位置を求める
    avg_x = int(np.mean([i for i, _ in neighbors]))
    avg_y = int(np.mean([j for _, j in neighbors]))
    
    # ランダムに近隣のエージェントの方向へ移動
    if random.random() < BOID_INFLUENCE:
        return avg_x, avg_y
    return None

# 近くの空き地を探す（Moore 近傍: 8マス以内）
def find_nearby_empty(grid, x, y):
    empty_spaces = [(i, j) for i in range(max(0, x-1), min(GRID_SIZE, x+2))
                              for j in range(max(0, y-1), min(GRID_SIZE, y+2))
                              if grid[i, j] == EMPTY]
    return random.choice(empty_spaces) if empty_spaces else None

# エージェントの移動（Schelling + Boid 統合）
def move_agents(grid):
    new_grid = np.copy(grid)
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x, y] in [RED, BLUE]:
                # Schelling のルール（不満なら移動）
                if calculate_dissimilarity(grid, x, y) > THRESHOLD:
                    new_pos = find_nearby_empty(grid, x, y)
                else:
                    # Boid のルール（群れ行動）
                    new_pos = boid_influence(grid, x, y)

                if new_pos and grid[new_pos] == EMPTY:
                    new_grid[new_pos] = grid[x, y]
                    new_grid[x, y] = EMPTY  # もともといた場所を空にする
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
