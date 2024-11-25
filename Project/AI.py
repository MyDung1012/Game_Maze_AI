import pygame
from collections import deque
import heapq
import random
import math
import numpy as np

directions = [
    (-1, 0),  # lên
    (1, 0),   # xuống
    (0, -1),  # trái
    (0, 1),   # phải

 ]
# Hàm thuật toán bfs
def solve_maze_bfs(maze, start, goal):

    rows = len(maze)
    cols = len(maze[0])
    
    queue = deque([(start)])
    visited = {start}
    
    # Dictionary lưu đường đi
    came_from = {}
    
    while queue:
        current = queue.popleft()
        
        if current == goal:
            # Tái tạo đường đi
            path = []
            while current in came_from:
                prev = came_from[current]
                path.append((current[0] - prev[0], current[1] - prev[1]))
                current = prev
            path.reverse()
            return path
            
        # Kiểm tra tất cả các hướng có thể đi
        for dx, dy in directions:
            next_row = current[0] + dx
            next_col = current[1] + dy
            neighbor = (next_row, next_col)
            
            # Kiểm tra điều kiện hợp lệ
            if (0 <= next_row < rows and 
                0 <= next_col < cols and 
                maze[next_row][next_col] == 0 and  # 0 là đường đi
                neighbor not in visited):
                
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current
    
    return None  # Không tìm thấy đường đi

# Hàm thuật toán A*
def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
def solve_maze_astar(maze, start, goal):

    
    rows = len(maze)
    cols = len(maze[0])
    
    # Tập đóng và tập mở
    closed_set = set()
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    # Lưu đường đi
    came_from = {}
    
    # g_score[n] là chi phí từ start đến node n
    g_score = {start: 0}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            # Tái tạo đường đi
            path = []
            while current in came_from:
                prev = came_from[current]
                path.append((current[0] - prev[0], current[1] - prev[1]))
                current = prev
            path.reverse()
            return path
            
        closed_set.add(current)
        
        # Kiểm tra tất cả các hướng có thể đi
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Ki���m tra điều kiện hợp lệ
            if (neighbor[0] < 0 or neighbor[0] >= rows or 
                neighbor[1] < 0 or neighbor[1] >= cols or
                maze[neighbor[0]][neighbor[1]] == 1 or  # 1 là tường
                neighbor in closed_set):
                continue
                
            tentative_g_score = g_score[current] + 1
            
            if (neighbor not in g_score or 
                tentative_g_score < g_score[neighbor]):
                
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))
    
    return None  # Không tìm thấy đường đi

#### BACKTRACKING + AC3
def min_consistent_ac3(grid):
    """
    Xây dựng danh sách các nước đi hợp lệ từ mỗi ô trong mê cung.
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Các hướng di chuyển: lên, xuống, trái, phải

    possible_moves = {(r, c): [] for r in range(rows) for c in range(cols) if grid[r][c] != 1}

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:  # Không phải tường
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
                        possible_moves[(r, c)].append((nr, nc))

    queue = list(possible_moves.keys())
    while queue:
        current = queue.pop(0)
        updated = False
        neighbors = possible_moves[current]

        if not neighbors:
            del possible_moves[current]
            updated = True

        for neighbor in neighbors:
            if neighbor in possible_moves and current not in possible_moves[neighbor]:
                possible_moves[neighbor].remove(current)
                updated = True

            if updated:
                queue.append(neighbor)

    return possible_moves


def heuristic(a, b):
    """
    Tính toán khoảng cách Manhattan giữa hai ô.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def calculate_max_depth(maze, complexity='medium'):
    size = len(maze) * len(maze[0])  # Tổng số ô
    wall_density = sum(row.count(1) for row in maze) / size  # Mật độ tường
    
    # Hệ số điều chỉnh dựa trên độ phức tạp
    if complexity == 'simple':
        factor = 0.3
    elif complexity == 'medium':
        factor = 0.5
    elif complexity == 'complex':
        factor = 0.7
    
    # Điều chỉnh dựa trên mật độ tường
    if wall_density > 0.5:
        factor += 0.1  # Tăng nếu mật độ tường cao
    
    max_depth = int(factor * size)
    return max_depth

def backtrack_with_ac3(grid, ghost_position, pacman_position):
    max_depth = calculate_max_depth(grid, complexity='medium')
    print (max_depth)
    possible_moves = min_consistent_ac3(grid)

    def search(path, depth):
        if depth > max_depth:  # Giới hạn độ sâu
            return None
        current = path[-1]
        if current == pacman_position:  # Đạt được Pacman
            return path

        # Sử dụng hàng đợi ưu tiên để tìm nước đi tốt nhất dựa trên heuristic
        pq = []
        for next_pos in possible_moves.get(current, []):
            if next_pos not in path:
                # Ưu tiên bước đi gần người chơi hơn
                priority = heuristic(next_pos, pacman_position)
                heapq.heappush(pq, (priority, next_pos))

        # Duyệt qua các bước đi trong hàng đợi ưu tiên
        while pq:
            _, next_pos = heapq.heappop(pq)
            result = search(path + [next_pos], depth + 1)
            if result:
                return result

        return None

    result_path = search([ghost_position], 0)

    # Kiểm tra tính hợp lệ của đường đi
    if result_path:
        for step in result_path:
            r, c = step
            if not (0 <= r < len(grid) and 0 <= c < len(grid[0])):
                print(f"Invalid step in path: {step}")
                return None
    return result_path

# SIMULATED ANNEALING
def schedule(t, k=20, lam=0.005, limit=1000):
    """Cooling schedule function."""
    return (k * np.exp(-lam * t) if t < limit else 0)

def simulated_annealing_path(maze, start, goal, max_iterations=1000, initial_temp=100, cooling_rate=0.99):
    """
    Simulated Annealing for the maze game. The boat tries to minimize the distance to the player.
    """
    current = start
    current_cost = heuristic(current, goal)
    temperature = initial_temp
    path = []  # Store the path the boat takes

    for t in range(max_iterations):
        if current == goal:
            print(f"Boat reached the player after {t} iterations.")
            return path

        # Get all valid neighbors
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_row, next_col = current[0] + dx, current[1] + dy
            if 0 <= next_row < len(maze) and 0 <= next_col < len(maze[0]) and maze[next_row][next_col] == 0:
                neighbors.append((next_row, next_col))

        if not neighbors:  # No valid moves
            print("Boat is stuck.")
            break

        # Choose a random neighbor
        next_position = random.choice(neighbors)
        next_cost = heuristic(next_position, goal)

        # Calculate the change in cost
        delta_cost = next_cost - current_cost

        # Determine whether to accept the move
        if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / temperature):
            current = next_position
            current_cost = next_cost
            path.append((next_position[0] - start[0], next_position[1] - start[1]))

        # Cool down the temperature
        temperature *= cooling_rate
        if temperature < 1e-3:  # If the temperature is too low, stop
            print("Temperature is too low, stopping.")
            break

    return path if current == goal else None

def heuristic(a, b):
    """
    Manhattan distance heuristic for the maze game.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

