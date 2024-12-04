import pygame
from collections import deque
import heapq
import random
import time
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

    rows = len(maze)      #xác định số hàng
    cols = len(maze[0])   #xác định cột
    
    queue = deque([(start)]) #tạo chỗ xếp hàng
    visited = {start} #đánh dấu ô 
    
    # Dictionary lưu đường đi
    came_from = {} 
    
    while queue: #
        current = queue.popleft() #lấy phần tử đầu tiên
        
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
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])    #f(n)=g(n)+h(n)
def solve_maze_astar(maze, start, goal):

    rows = len(maze)
    cols = len(maze[0])
    
    # Tập đóng (closed_set): Lưu các điểm đã xử lý.
    closed_set = set()

    # Tập mở (open_set): Hàng đợi ưu tiên, lưu các điểm cần xử lý tiếp theo.
    # Sử dụng heapq để đảm bảo các phần tử có giá trị f nhỏ nhất được xử lý trước.
    open_set = []
    heapq.heappush(open_set, (0, start))  # Thêm điểm bắt đầu với giá trị f = 0.
    
    # Dictionary lưu "cha" của mỗi điểm, phục vụ cho việc tái tạo đường đi.
    came_from = {}
    
    # g_score lưu chi phí từ điểm bắt đầu đến mỗi điểm.
    g_score = {start: 0}

    # Lặp cho đến khi không còn điểm nào trong tập mở
    while open_set:
        # Lấy điểm có giá trị f nhỏ nhất từ open_set
        current = heapq.heappop(open_set)[1]
        
        # Nếu đã đến đích, tái tạo và trả về đường đi
        if current == goal:
            path = []  # Danh sách lưu các bước di chuyển
            while current in came_from:
                prev = came_from[current]  # Lấy điểm cha của current
                path.append((current[0] - prev[0], current[1] - prev[1]))  # Lưu hướng di chuyển
                current = prev  # Quay về điểm cha
            path.reverse()  # Đảo ngược danh sách để có đường đi từ start đến goal
            return path  # Trả về danh sách các bước di chuyển
        
        # Thêm điểm hiện tại vào tập đóng
        closed_set.add(current)
        
        # Kiểm tra các điểm lân cận
        for dx, dy in directions:  # directions chứa các vector di chuyển hợp lệ (vd: [(0,1), (1,0), (0,-1), (-1,0)])
            neighbor = (current[0] + dx, current[1] + dy)  # Tính tọa độ của điểm lân cận
            
            # Kiểm tra điều kiện hợp lệ của điểm lân cận
            if (neighbor[0] < 0 or neighbor[0] >= rows or  # Nằm ngoài lưới (hàng)
                neighbor[1] < 0 or neighbor[1] >= cols or  # Nằm ngoài lưới (cột)
                maze[neighbor[0]][neighbor[1]] == 1 or     # Là tường (giá trị 1 trong maze)
                neighbor in closed_set):                  # Đã được xử lý trước đó
                continue
            
            # Tính toán chi phí tạm thời từ start đến neighbor qua current
            tentative_g_score = g_score[current] + 1
            
            # Nếu neighbor chưa được thăm hoặc tìm thấy đường đi tốt hơn
            if (neighbor not in g_score or tentative_g_score < g_score[neighbor]):
                came_from[neighbor] = current  # Cập nhật cha của neighbor
                g_score[neighbor] = tentative_g_score  # Cập nhật g_score của neighbor
                
                # Tính giá trị f = g + h (h là giá trị heuristic từ neighbor đến goal)
                f_score = tentative_g_score + heuristic(neighbor, goal)
                
                # Thêm neighbor vào tập mở
                heapq.heappush(open_set, (f_score, neighbor))
    
    # Nếu không tìm thấy đường đi
    return None


# Backtracking + AC3
def min_consistent_ac3(grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Các hướng di chuyển: lên, xuống, trái, phải

    # Khởi tạo danh sách các nước đi hợp lệ
    possible_moves = {(r, c): [] for r in range(rows) for c in range(cols) if grid[r][c] != 1}

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:  # Không phải tường
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
                        possible_moves[(r, c)].append((nr, nc))

    # Áp dụng AC3 để loại bỏ các nước đi không hợp lệ
    queue = list(possible_moves.keys())
    while queue:
        current = queue.pop(0)
        neighbors = possible_moves[current]

        for neighbor in neighbors:
            if neighbor in possible_moves and current not in possible_moves[neighbor]:
                possible_moves[neighbor].remove(current)
                queue.append(neighbor)


        if not neighbors:  # No valid moves
            print("Boat is stuck.")
            break


    return possible_moves


def heuristic(a, b):
    """
    Tính toán khoảng cách Manhattan giữa hai ô.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def calculate_max_depth(maze, complexity='medium'):
    """
    Tính toán độ sâu tối đa dựa trên kích thước mê cung và độ phức tạp.
    """
    size = len(maze) * len(maze[0])
    wall_density = sum(row.count(1) for row in maze) / size

    # Hệ số điều chỉnh dựa trên độ phức tạp
    factor = {
        'simple': 0.3,
        'medium': 0.5,
        'complex': 0.7
    }.get(complexity, 0.5)

    if wall_density > 0.5:  # Điều chỉnh nếu mật độ tường cao
        factor += 0.1

    return int(factor * size)


def backtrack_with_ac3(grid, boat_position, player_position, time_limit=2):
    """
    Thuật toán backtracking với AC3 và giới hạn thời gian.
    """
    max_depth = calculate_max_depth(grid, complexity='medium')
    possible_moves = min_consistent_ac3(grid)
    memo = {}  # Bộ nhớ đệm cho các trạng thái đã duyệt
    start_time = time.time()  # Thời gian bắt đầu

    def search(path, depth):
        """
        Hàm tìm kiếm đệ quy.
        """
        # Kiểm tra giới hạn thời gian
        if time.time() - start_time > time_limit:
            return None

        # Kiểm tra giới hạn độ sâu
        if depth > max_depth:
            return None

        current = path[-1]
        # Nếu đạt đến Pacman
        if current == player_position:
            return path

        # Kiểm tra nếu trạng thái đã được duyệt
        if current in memo:
            return memo[current]

        # Tìm nước đi tốt nhất dựa trên heuristic
        pq = []
        for next_pos in possible_moves.get(current, []):
            if next_pos not in path:  # Tránh đi qua ô đã duyệt
                priority = heuristic(next_pos, player_position)
                heapq.heappush(pq, (priority, next_pos))

        while pq:
            _, next_pos = heapq.heappop(pq)
            result = search(path + [next_pos], depth + 1)
            if result:  # Nếu tìm thấy đường đi hợp lệ
                memo[current] = result
                return result

        # Lưu trạng thái không tìm thấy đường đi
        memo[current] = None
        return None
    # Bắt đầu tìm kiếm từ vị trí của "ghost"
    result_path = search([boat_position], 0)

    # Kiểm tra đường đi hợp lệ
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
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

