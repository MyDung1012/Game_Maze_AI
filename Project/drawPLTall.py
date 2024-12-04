import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Dữ liệu từ bài toán
data = {
    "maze": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    "bfs": [18, 28, 31, 47, 62, 50, 73, 85, 75, 100],
    "A*": [18, 28, 31, 47, 62, 50, 70, 85, 75, 100],
    "backtracking": [18, 28, 35, 47, 0, 50, 0, 85, 0, 0],
    "SA": [162, 444, 933, 1161, 3844, 1064, 2067, 3179, 0, 0]
}

# Chuyển dữ liệu thành DataFrame
df = pd.DataFrame(data)

# Chuẩn hóa dữ liệu về khoảng [0, 1]
normalized_df = df.copy()
for column in ["bfs", "A*", "backtracking", "SA"]:
    col_min = df[column].min()
    col_max = df[column].max()
    normalized_df[column] = (df[column] - col_min) / (col_max - col_min)

# Vẽ biểu đồ với dữ liệu chuẩn hóa
plt.figure(figsize=(12, 6))
plt.plot(normalized_df['maze'], normalized_df['bfs'], marker='o', label='BFS')
plt.plot(normalized_df['maze'], normalized_df['A*'], marker='o', label='A*')
plt.plot(normalized_df['maze'], normalized_df['backtracking'], marker='o', label='Backtracking')
plt.plot(normalized_df['maze'], normalized_df['SA'], marker='o', label='Simulated Annealing (SA)')

# Thêm tiêu đề, nhãn và chú thích
plt.title("Comparison of Algorithm Efficiency (Normalized Data)")
plt.xlabel("Maze Size")
plt.ylabel("Normalized Efficiency")
plt.legend()
plt.grid(True)

# Hiển thị biểu đồ
plt.show()