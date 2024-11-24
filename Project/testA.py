import pygame
import random
import sys
from Colors import Colors
from enum import Enum
import json
from collections import deque 
import heapq  
import time

pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

maze_width = screen_width * 2 // 3

# Âm thanh nền
pygame.mixer.music.load('Sound/8bit.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()


with open('difficulty.txt', 'r') as f:
    maze_size = int(f.read().strip())

try:
    with open('difficulty.txt', 'r') as f:
        maze_size = int(f.read().strip())
except (FileNotFoundError, ValueError) as e:
    print(f"Error reading difficulty: {e}")
    initial_depth_limit = 100  # Giá trị mặc định nếu gặp lỗi



win_image = pygame.image.load("Image/win.jpg")
win_image = pygame.transform.scale(win_image, (600, 450))
win_sound = pygame.mixer.Sound("Sound/happy.mp3")

close_button = pygame.Rect(screen_width // 2 + win_image.get_width() // 2 - 30,
                           screen_height // 2 - win_image.get_height() // 2, 30, 30)

win_imagee = pygame.image.load("Image/win.jpg")
lose_image = pygame.image.load("Image/lose.jpg")

win_image = pygame.transform.scale(win_imagee, (600, 450))
lose_image = pygame.transform.scale(lose_image, (600, 450))


with open(f"Maze/{maze_size}.txt", "r") as f:
    maze_matrix = json.load(f)


cell_width = maze_width // len(maze_matrix[0])
cell_height = screen_height // len(maze_matrix) 

background_image = pygame.image.load('Image/bgbg.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

path_image = pygame.image.load('Image/blockk.png') 
path_image = pygame.transform.scale(path_image, (cell_width, cell_height))


goal_image = pygame.image.load('Image/moon.png')
goal_image = pygame.transform.scale(goal_image, (cell_width, cell_height))
goal_rect = goal_image.get_rect()

planet_images = [
    pygame.image.load('Image/planet1.png'), 
    pygame.image.load('Image/planet2.png'), 
    pygame.image.load('Image/planet3.png')  
]

directions = [
    (-1, 0),  # lên
    (1, 0),   # xuống
    (0, -1),  # trái
    (0, 1),   # phải

 ]
class Planet:
    def __init__(self, image, x, y):
        self.image = pygame.transform.scale(image, (85, 64)) 
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.randint(1, 5)
        self.direction = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x < -self.rect.width or self.rect.x > screen_width:
            self.rect.x = random.randint(screen_width, screen_width + 100)
            self.rect.y = random.randint(0, screen_height - self.rect.height)
            self.direction = random.choice([-1, 1])

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Maze:
    def __init__(self, matrix):
        self.matrix = matrix

    def draw(self, surface):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                x, y = col * cell_width, row * cell_height
                if self.matrix[row][col] == 1:
                    surface.blit(path_image, (x, y))
                    self.draw_wall_border(surface, row, col)

        self.draw_stylized_border(surface)

    def draw_wall_border(self, surface, row, col):
        x, y = col * cell_width, row * cell_height
        outer_border_color = (186, 85, 211) 
        inner_border_color = (255, 250, 150) 

        adjacent = [
            ((x, y), (x + cell_width, y), row > 0 and self.matrix[row - 1][col] == 0),          
            ((x, y + cell_height), (x + cell_width, y + cell_height), row < len(self.matrix) - 1 and self.matrix[row + 1][col] == 0),  # Cạnh dưới
            ((x, y), (x, y + cell_height), col > 0 and self.matrix[row][col - 1] == 0),        
            ((x + cell_width, y), (x + cell_width, y + cell_height), col < len(self.matrix[0]) - 1 and self.matrix[row][col + 1] == 0)  # Cạnh phải
    ]

        for start, end, condition in adjacent:
            if condition:
                pygame.draw.line(surface, outer_border_color, (start[0] - 1, start[1] - 1), (end[0] - 1, end[1] - 1), 3)
                pygame.draw.line(surface, inner_border_color, start, end, 2)

    def draw_stylized_border(self, surface):
        maze_width = len(self.matrix[0]) * cell_width
        maze_height = len(self.matrix) * cell_height
        corner_size = 10 

        layers = [
            ((186, 85, 211), 6),  
            ((64, 224, 208), 3)  
        ]

        for i, (color, thickness) in enumerate(layers):
            offset = i * 1 
            pygame.draw.rect(surface, color, (offset, offset, maze_width - 1 * offset, maze_height - 1 * offset), thickness, border_radius=corner_size)


planets = [Planet(planet_images[i], random.randint(0, screen_width), random.randint(0, screen_height - 50)) for i in range(3)]

maze = Maze(maze_matrix)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.original_image = pygame.image.load('Image/rocket.png')
        self.image = self.original_image
        self.reset_position()
        self.game_completed = False 
        try:
            self.original_image = pygame.transform.scale(self.original_image, (cell_width, cell_height))
            self.image = self.original_image
        except pygame.error as e:
            print(f"Error loading rocket image: {e}")
            sys.exit()

    def reset_position(self):
        self.row = 0
        self.col = 0
        self.game_completed = False 
        self.image = self.original_image
    
    def is_at_goal(self):
        return self.row == maze_size - 1 and self.col == maze_size - 1 
    
    def reset_game(self):
        global game_completed, sound_played, show_image, player_step_counter,game_over
        game_completed = False
        sound_played = False
        show_image = True
        game_over =False
        player_step_counter = 0
        player.reset_position()

    def move(self, direction, maze_matrix):
        if self.game_completed:
            return False
            
        new_row = self.row + direction[0]
        new_col = self.col + direction[1]
        
        if (0 <= new_row < len(maze_matrix) and 
            0 <= new_col < len(maze_matrix[0]) and 
            maze_matrix[new_row][new_col] == 0):
            
            if direction == (-1, 0):  # lên
                self.image = pygame.transform.rotate(self.original_image, 0)
            elif direction == (1, 0):  # xuống
                self.image = pygame.transform.rotate(self.original_image, 180)
            elif direction == (0, -1):  # trái
                self.image = pygame.transform.rotate(self.original_image, 90)
            elif direction == (0, 1):  # Phải
                self.image = pygame.transform.rotate(self.original_image, -90)
            self.row = new_row
            self.col = new_col

            #if self.is_at_goal() and collected_keys==num_keys:
            #    self.game_completed = True
            return True
        return False
    
    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        surface.blit(self.image, (x + (cell_width - self.image.get_width()) // 2, 
                                  y + (cell_height - self.image.get_height()) // 2))


def reset_game():
    global player_step_counter, AI_step, keys, collected_keys, algorithm_selected, game_over, player_won, ai_active, start_time, num_keys

    # Reset trạng thái người chơi
    player.reset_position()
    player_step_counter = 0

    # Reset trạng thái thuyền
    boat.row, boat.col = maze_size - 1, 0
    boat.path = None
    boat.path_index = 0

    # Random lại keys
    num_keys = random.randint(3, 5)  # Reset số lượng keys ngẫu nhiên
    keys = generate_random_keys(maze_matrix, num_keys, key_image)  # Reset danh sách keys
    collected_keys = 0  # Reset số keys đã thu thập

    # Reset các biến trạng thái trò chơi
    AI_step = 0
    algorithm_selected = None
    game_over = False
    player_won = False
    ai_active = False

    # Reset thời gian bắt đầu
    start_time = pygame.time.get_ticks()



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
def solve_maze_dfs(maze, start, goal):
    # 8 hướng di chuyển: trên, dưới, trái, phải, và 4 hướng chéo

    rows = len(maze)
    cols = len(maze[0])
    
    # Khởi tạo stack và visited set
    stack = [(start)]
    visited = {start}
    
    # Dictionary lưu đường đi
    came_from = {}
    
    while stack:
        current = stack.pop()  # Lấy phần tử cuối cùng của stack
        
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
                
                stack.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current
    
    return None  # Không tìm thấy đường đi
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

def draw_rounded_button(button_rect, text, color, font_size, border_color_outer=(186, 85, 211), border_color_inner=(255, 215, 0), border_thickness=3, radius=0, offset_x=-40):
    # Điều chỉnh vị trí của nút bằng cách dịch sang trái `offset_x` pixel
    adjusted_rect = button_rect.move(offset_x, 0)
    
    # Vẽ viền ngoài màu tím
    pygame.draw.rect(screen, border_color_outer, adjusted_rect, border_thickness + 2, border_radius=radius)
    
    # Vẽ viền trong màu vàng
    pygame.draw.rect(screen, border_color_inner, adjusted_rect.inflate(-border_thickness * 2, -border_thickness * 2), border_thickness, border_radius=radius)
    
    # Vẽ nền nút bên trong
    pygame.draw.rect(screen, color, adjusted_rect.inflate(-border_thickness * 4, -border_thickness * 4), border_radius=radius)
    
    # Vẽ chữ trên nút
    font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", font_size)
    label = font.render(text, True, Colors.WHITE)
    screen.blit(label, label.get_rect(center=adjusted_rect.center))


class CSP:
    """Mô hình CSP với miền giá trị, biến và ràng buộc."""
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, value, assignment):
        """Gán giá trị cho biến."""
        assignment[var] = value
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Hủy gán giá trị cho biến."""
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, value, assignment):
        """Đếm số xung đột của biến."""
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, value, var2, assignment[var2])
        return sum(conflict(v) for v in self.neighbors[var])

def first_unassigned_variable(assignment, csp):
    """Lựa chọn biến chưa được gán giá trị."""
    return next((var for var in csp.variables if var not in assignment), None)

def argmin_random_tie(seq, key=lambda x: x):
    """Chọn phần tử nhỏ nhất với tie-breaking ngẫu nhiên."""
    items = list(seq)
    random.shuffle(items)
    return min(items, key=key)

def count(seq):
    """Đếm số phần tử đúng trong một dãy."""
    return sum(bool(x) for x in seq)


def AC3(csp):
    """Áp dụng AC3 cho mê cung."""
    queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.curr_domains = csp.domains.copy()  # Sao chép miền giá trị ban đầu

    while queue:
        Xi, Xj = queue.pop()
        if revise(csp, Xi, Xj):
            if not csp.curr_domains[Xi]:  # Nếu miền giá trị trống, không thỏa mãn
                print(f"AC3 failure: Domain of {Xi} is empty.")
                return False
            for Xk in csp.neighbors[Xi] - {Xj}:
                queue.add((Xk, Xi))

    # Gỡ lỗi
    print("Domains after AC3:")
    for var, domain in csp.curr_domains.items():
        print(f"{var}: {domain}")
    return True




def revise(csp, Xi, Xj):
    """Loại bỏ giá trị không hợp lệ trong miền giá trị của Xi."""
    revised = False
    for x in csp.curr_domains[Xi][:]:  # Sao chép danh sách để tránh lỗi khi xóa
        if not any(csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.curr_domains[Xi].remove(x)
            revised = True
    return revised

def build_csp_from_maze(maze, start, goal):
    variables = [(r, c) for r in range(len(maze)) for c in range(len(maze[0])) if maze[r][c] == 0]
    domains = {(r, c): [(r + dr, c + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if 0 <= r + dr < len(maze) and 0 <= c + dc < len(maze[0]) and maze[r + dr][c + dc] == 0]
               for r, c in variables}
    neighbors = {(r, c): [neighbor for neighbor in domains[(r, c)] if neighbor in variables] for r, c in variables}

    # Gỡ lỗi
    print(f"Variables: {variables}")
    print(f"Domains: {domains}")
    print(f"Neighbors: {neighbors}")
    return CSP(variables, domains, neighbors, lambda A, a, B, b: a != b)




def backtracking_search(csp):
    """Tìm đường đi bằng backtracking."""
    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment

        var = first_unassigned_variable(assignment, csp)
        for value in csp.curr_domains[var]:
            if csp.nconflicts(var, value, assignment) == 0:
                csp.assign(var, value, assignment)
                result = backtrack(assignment)
                if result:
                    return result
                csp.unassign(var, assignment)

        return None  # Không tìm thấy giải pháp

    assignment = backtrack({})
    if assignment:
        print(f"Backtracking assignment: {assignment}")
        # Chuyển đổi assignment thành đường đi
        start = min(assignment.keys(), key=lambda x: (x[0], x[1]))  # Bắt đầu từ điểm nhỏ nhất
        path = []
        current = start
        while current in assignment:
            next_step = assignment[current]
            path.append((next_step[0] - current[0], next_step[1] - current[1]))
            current = next_step
        print(f"Path derived from assignment: {path}")
        return path
    print("Backtracking failed to find a solution.")
    return None


class Boat:
    def __init__(self, x, y):
        self.row = x
        self.col = y
        self.image = pygame.image.load('Image/ufo.png')
        self.image = pygame.transform.scale(self.image, (cell_width, cell_height))
        self.path = None
        self.path_index = 0
        self.algorithm_selected = None
        self.last_move_time = 0
        self.move_delay = 1000

    def update_path(self, maze, target, algorithm):
        if algorithm == "AC3+Backtracking":
            print(f"Running AC3+Backtracking for boat at ({self.row}, {self.col})")
            maze_csp = build_csp_from_maze(maze, (self.row, self.col), target)
            if AC3(maze_csp):
                self.path = backtracking_search(maze_csp)
                if self.path is None:
                    print("Backtracking did not find a solution.")
                else:
                    print(f"Path found by Backtracking: {self.path}")
            else:
                self.path = None
                print("AC3 failed to simplify the CSP.")
        elif algorithm == "BFS":
            print(f"Running BFS for boat at ({self.row}, {self.col})")
            self.path = solve_maze_bfs(maze, (self.row, self.col), target) or []
        elif algorithm == "DFS":
            print(f"Running DFS for boat at ({self.row}, {self.col})")
            self.path = solve_maze_dfs(maze, (self.row, self.col), target) or []
        elif algorithm == "A*":
            print(f"Running A* for boat at ({self.row}, {self.col})")
            self.path = solve_maze_astar(maze, (self.row, self.col), target) or []
        else:
            self.path = []  # Không tìm thấy đường đi

        self.path_index = 0
        if not self.path:
            print(f"No path found using {algorithm}. Boat remains at ({self.row}, {self.col}).")


    def move(self, maze):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_delay:
            if not self.path:
                print("Boat has no path.")
                return  # Không có đường đi
            if self.path_index < len(self.path):
                direction = self.path[self.path_index]
                next_row = self.row + direction[0]
                next_col = self.col + direction[1]
                if maze[next_row][next_col] == 0:
                    self.row = next_row
                    self.col = next_col
                    self.path_index += 1
                print(f"Boat moved to ({self.row}, {self.col})")
            else:
                print("Boat reached the end of its path.")
            self.last_move_time = current_time



    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        surface.blit(self.image, (x, y))


class Key:
    def __init__(self, x, y, image):
        self.row = x
        self.col = y
        self.image = pygame.transform.scale(image, (cell_width, cell_height))
        self.collected = False  # Trạng thái đã được thu thập hay chưa

    def draw(self, surface):
        if not self.collected:
            x = self.col * cell_width
            y = self.row * cell_height
            surface.blit(self.image, (x, y))

def generate_random_keys(maze_matrix, num_keys, key_image):
    keys = []
    rows = len(maze_matrix)
    cols = len(maze_matrix[0])

    while len(keys) < num_keys:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        if maze_matrix[row][col] == 0 and (row, col) != (0, 0) and (row, col) != (maze_size - 1, maze_size - 1):
            keys.append(Key(row, col, key_image))
    return keys

# Load key hình ảnh
key_image = pygame.image.load('Image/key.png')

# Random 3-5 keys
num_keys = random.randint(3, 5)
keys = generate_random_keys(maze_matrix, num_keys, key_image)
collected_keys = 0

button_reset = pygame.Rect(screen_width - 220, screen_height - 560, 200, 60)
button_backtracking = pygame.Rect(screen_width - 220, screen_height - 480, 200, 60) 
button_dfs = pygame.Rect(screen_width - 220, screen_height - 400, 200, 60)
button_bfs = pygame.Rect(screen_width - 220, screen_height - 320, 200, 60)
button_A = pygame.Rect(screen_width - 220, screen_height - 240, 200, 60)
button_home = pygame.Rect(screen_width - 220, screen_height - 160, 200, 60)
button_exit = pygame.Rect(screen_width - 220, screen_height - 80, 200, 60)


def display_outcome_box(text):
    # Vị trí và kích thước của bảng thông báo
    box_width, box_height = 400, 200
    box_x = (screen_width - box_width) // 2
    box_y = (screen_height - box_height) // 2

    # Vẽ bảng (hình chữ nhật) và hiển thị nội dung
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)
    
    # Hiển thị nội dung outcome_text
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)


# Add after maze initialization
player = Player(0, 0)  # Khởi tạo đối tượng người chơi tại vị trí (0, 0)
boat = Boat(maze_size - 1, 0)  # Vị trí bắt đầu của thuyền (phía dưới bên trái)
game_over = False  # Biến kiểm tra trạng thái trò chơi; False nghĩa là trò chơi vẫn đang diễn ra
player_won = False  # Biến kiểm tra xem người chơi đã thắng hay chưa; False nghĩa là người chơi chưa thắng
algorithm_selected = None  # Biến để lưu thuật toán đã chọn; None nghĩa là chưa có thuật toán nào được chọn
start_time = pygame.time.get_ticks()  # Lưu thời gian bắt đầu trò chơi
ai_active = False  # Biến kiểm tra xem AI có đang hoạt động hay không; False nghĩa là AI chưa hoạt động
auto_move_path = None  # Biến để lưu đường đi tự động; None nghĩa là chưa có đường đi nào được xác định
auto_move_index = 0  # Chỉ số cho bước di chuyển tự động; bắt đầu từ 0
AI_step = 0  # Khởi tạo AI_step để đếm số bước của thuật toán DFS
auto_move_delay = 10  # Độ trễ (ms) giữa các bước tự động
last_move_time = pygame.time.get_ticks()  # Theo dõi thời gian của lần di chuyển cuối cùng
# Initialize font
font = pygame.font.Font(None, 36)  # Khởi tạo font với kích thước 36
# Initialize player_step_counter
player_step_counter = 0  # Bộ đếm cho số bước của người chơi; bắt đầu từ 0
game_completed = False  # Biến kiểm tra xem trò chơi đã hoàn thành hay chưa; False nghĩa là trò chơi chưa hoàn thành
sound_played = False  # Biến để kiểm soát việc phát âm thanh; False nghĩa là âm thanh chưa được phát
show_image = True  # Biến kiểm soát việc hiển thị hình ảnh; True nghĩa là hình ảnh sẽ được hiển thị
ai_completed = False  # Biến kiểm tra xem AI đã hoàn thành nhiệm vụ hay chưa; False nghĩa là AI chưa hoàn thành


  # Thời gian bắt đầu hiển thị thông báo\

def ai_move(auto_move_path, auto_move_index, maze_matrix):
    if auto_move_path is not None and auto_move_index < len(auto_move_path):
        direction = auto_move_path[auto_move_index]
        player.move(direction, maze_matrix)  # Assuming player is an instance of Player
        return auto_move_index + 1
    return auto_move_index  # Return the current index if no move is made

# Vòng lặp chính
while True:

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            direction = None
            if event.key == pygame.K_LEFT:
                direction = (0, -1)  # Trái
            elif event.key == pygame.K_RIGHT:
                direction = (0, 1)   # Phải
            elif event.key == pygame.K_UP:
                direction = (-1, 0)  # Lên
            elif event.key == pygame.K_DOWN:
                direction = (1, 0)   # Xuống

            if direction:
                player.move(direction, maze_matrix)  # Call the move method of the Player class

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_reset.collidepoint(event.pos):
                print("Reset button clicked")
                reset_game()
            elif button_home.collidepoint(event.pos):
                print("Home button clicked")
                pygame.mixer.music.stop()   
                exec(open("Home.py", encoding="utf-8").read())
            if button_bfs.collidepoint(event.pos):
                print("BFS button clicked")
                algorithm_selected = "BFS"
            elif button_dfs.collidepoint(event.pos):
                print("DFS button clicked")
                algorithm_selected = "DFS"
            elif button_A.collidepoint(event.pos):
                print("A* button clicked")
                algorithm_selected = "A*"
            elif button_backtracking.collidepoint(event.pos):
                print("AC3+Backtracking button clicked")
                algorithm_selected = "AC3+Backtracking"
                boat.update_path(maze_matrix, (player.row, player.col), algorithm_selected)
            elif button_exit.collidepoint(event.pos):
                print("Exit button clicked")
                pygame.quit()
                sys.exit()  # Thoát khỏi trò chơi
            


    screen.fill((0, 0, 0))

    show_outcome = False  # Biến điều kiện để hiển thị thông báo
    outcome_time = 0
    # Check if it's time to move to the next step

    auto_move_index = ai_move(auto_move_path, auto_move_index, maze_matrix)  # Call the new AI movement function

    if auto_move_path and auto_move_index < len(auto_move_path):
        direction = auto_move_path[auto_move_index]
        player.move(direction, maze_matrix)
        auto_move_index += 1  # Move to the next step
        AI_step += 1  # Increment AI_step for each move
        pygame.time.delay(10)  # SUA TOC DO AI TAI DAY

        if auto_move_index >= len(auto_move_path):
            ai_completed = True 
            auto_move_path = None
    if elapsed_time >= 5 and algorithm_selected and not game_over:
        ai_active = True
        boat.update_path(maze_matrix, (player.row, player.col), algorithm_selected)
        boat.move(maze_matrix)
    


        # Kiểm tra nếu thuyền bắt được tên lửa
        # Kiểm tra nếu người chơi đến đích
        if player.is_at_goal():
            if collected_keys == num_keys:
                game_over = True
                player_won = True
            else:
                game_over = True
                player_won = False

        # Kiểm tra nếu thuyền bắt được người chơi
        if (boat.row, boat.col) == (player.row, player.col):
            game_over = True
            player_won = False
            game_completed = True

    # Kiểm tra nếu người chơi đi qua key
    for key in keys:
        if not key.collected and player.row == key.row and player.col == key.col:
            key.collected = True
            collected_keys += 1
    screen.blit(background_image, (0, 0))
    boat.draw(screen)
    # Vẽ các keys
    for key in keys:
        key.draw(screen)
    for planet in planets:
        planet.update()
        planet.draw(screen)

    # Vẽ mê cung
    maze.draw(screen)

    #Vẽ đích
    goal_x = (maze_size - 1) * cell_width + (cell_width - goal_rect.width) // 2
    goal_y = (maze_size - 1) * cell_height + (cell_height - goal_rect.height) // 2
    screen.blit(goal_image, (goal_x, goal_y))

    # Draw player
    player.draw(screen)
    
    # Draw AI step counter
    # Định nghĩa kích thước và màu sắc của textbox
    textbox_width = 300
    textbox_height = 50
    textbox_color = Colors.PINK  # Màu nền của textbox
    border_color = Colors.WHITE  # Màu viền của textbox
    border_thickness = 3  # Độ dày của viền

     # Textbox cho số keys đã thu thập
    # Textbox cho số keys đã thu thập
    keys_textbox_rect = pygame.Rect(screen_width - 400, 60, textbox_width, textbox_height)
    pygame.draw.rect(screen, border_color, keys_textbox_rect, border_thickness)  # Vẽ viền
    pygame.draw.rect(screen, textbox_color, keys_textbox_rect.inflate(-border_thickness*2, -border_thickness*2))  # Vẽ nền

    # Hiển thị số keys đã thu thập
    keys_text = font.render(f"Keys: {collected_keys}/{num_keys}", True, Colors.WHITE)
    keys_text_rect = keys_text.get_rect(center=keys_textbox_rect.center)  # Canh giữa văn bản trong textbox
    screen.blit(keys_text, keys_text_rect)


    draw_rounded_button(button_reset, "Reset", Colors.DARK_BLUE, 36 )
    draw_rounded_button(button_home, "Home",Colors.DARK_BLUE, 36)
    draw_rounded_button(button_bfs, "BFS", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_dfs, "DFS", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_exit, "Exit", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_A, "A*", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_backtracking, "Backtracking", Colors.DARK_BLUE, 36)
    if game_over and show_image:
        if player_won:
            screen.blit(win_imagee, (screen_width // 2 - win_image.get_width() // 2,
                                    screen_height // 2 - win_image.get_height() // 2))
            close_text = font.render(" ", True, (255, 255, 255))
            screen.blit(close_text, (close_button.x + 5, close_button.y))



    # Hiển thị thời gian còn lại trước khi AI bắt đầu
    if not ai_active and algorithm_selected is not None:
        remaining_time = max(0, 5 - elapsed_time)
        time_text = font.render(f"AI starts in: {remaining_time} s", True, Colors.WHITE)
        screen.blit(time_text, (screen_width - 250, screen_height- 640))
       
    # Cập nhật màn hình
    pygame.display.flip()
    pygame.time.delay(30)