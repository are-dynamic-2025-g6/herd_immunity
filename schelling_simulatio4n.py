import numpy as np
import matplotlib.pyplot as plt
import random

# パラメータ設定
GRID_SIZE = 20  # グリッドのサイズ
EMPTY_RATIO = 0.2  # 初期の空白の割合
THRESHOLDS = [0.3, 0.5, 0.7]  # 不満閾値の設定
STEPS = 50  # シミュレーションの最大ステップ数

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

# 分離度（平均類似度）を計算
def calculate_similarity_score(grid):
    total_similarity = 0
    count = 0
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x, y] in [RED, BLUE]:
                similarity = 1 - calculate_dissimilarity(grid, x, y)  # 近隣との類似度
                total_similarity += similarity
                count += 1
    return total_similarity / count if count > 0 else 0

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

# シミュレーションの実行（分離度の測定）
def run_simulation(threshold):
    grid = initialize_grid()
    similarity_scores = []

    for step in range(STEPS):
        similarity_scores.append(calculate_similarity_score(grid))  # 分離度を記録
        new_grid = move_agents(grid, threshold)
        if np.array_equal(grid, new_grid):  # 変化がなければ終了
            break
        grid = new_grid
    
    return similarity_scores

# 各 THRESHOLD でシミュレーションを実行し、グラフを描画
plt.figure(figsize=(8, 6))

for threshold in THRESHOLDS:
    scores = run_simulation(threshold)
    plt.plot(range(len(scores)), scores, label=f"THRESHOLD = {threshold}")

plt.xlabel("Time Step")
plt.ylabel("Segregation Level (Similarity Score)")
plt.title("Segregation Progress Over Time")
plt.legend()
plt.grid()
plt.show()
