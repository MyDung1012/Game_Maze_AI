import pygame
import random
import sys
from Colors import Colors
from enum import Enum
import json
from collections import deque
import heapq

pygame.init()

# Thiết lập màn hình
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# mở ma trận
with open('difficulty.txt', 'r') as f:
    maze_size = int(f.read().strip())
with open(f"Maze/{maze_size}.txt", 'r') as f:
    maze_matrix = json.load(f)

maze_width = screen_width * 2 // 3
cell_width = maze_width // len(maze_matrix[0])
cell_height = screen_height // len(maze_matrix)

# Thêm các hình ảnh
background_image = pygame.image.load("Image/bgbg.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

win_image = pygame.image.load("Image/win.jpg")
win_image = pygame.transform.scale(win_image, (600, 450))

lose_image = pygame.image.load("Image/lose.jpg")
lose_image = pygame.transform.scale(lose_image, (600, 450))

path_image = pygame.image.load("Image/blockk.png")
path_image = pygame.transform.scale(path_image, (cell_width, cell_height))

goal_image = pygame.image.load("Image/moon.png")
goal_image = pygame.transform.scale(goal_image, (cell_width, cell_height))
goal_rect = goal_image.get_rect()

key_image = pygame.image.load('Image/key.png')

planet_images = [
    pygame.image.load('Image/planet1.png'),
    pygame.image.load('Image/planet2.png'),
    pygame.image.load('Image/planet3.png')
]

# Tải âm thanh
pygame.mixer.music.load('Sound/8bit.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

font = pygame.font.Font(None, 36)
# Lớp các hành tinh
class Planet:
    def __init__(self, image, x, y):
        self.image = pygame.transform.scale(image, (85, 64))
        self.rect = self.image.get_rect(topleft=(x,y))
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

planets = [Planet(planet_images[i], random.randint(0, screen_width), random.randint(0, screen_height - 70)) for i in range(3)]

# Lớp vẽ mê cung 
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
        outer_border_color = Colors.PURPLE_2
        inner_border_color = Colors.LIGHT_YELLOW

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
            ((Colors.PURPLE_2), 6),  
            ((Colors.LIGHT_YELLOW), 3)  
        ]

        for i, (color, thickness) in enumerate(layers):
            offset = i * 1 
            pygame.draw.rect(surface, color, (offset, offset, maze_width - 1 * offset, maze_height - 1 * offset), thickness, border_radius=corner_size)


# Lớp thiết kế người chơi (tên lửa)
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.original_image = pygame.image.load('Image/rocket.png')
        self.original_image = pygame.transform.scale(self.original_image, (cell_width, cell_height))
        self.image = self.original_image
        self.reset_position()
        self.game_completed = False 

    def reset_position(self):
        self.row = 0
        self.col = 0
        self.game_completed = False 
        self.image = self.original_image
    
    def is_at_goal(self):
        return self.row == maze_size - 1 and self.col == maze_size - 1 
    
    def move(self, direction, maze_matrix):
        if self.is_at_goal():
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

            return True
        return False
    
    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        surface.blit(self.image, (x + (cell_width - self.image.get_width()) // 2, 
                                  y + (cell_height - self.image.get_height()) // 2))
        

# Hàm di chuyển bằng AI (Boat)
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
        if algorithm == "Backtracking":
            print(f"Running Backtracking for boat at ({self.row}, {self.col})")
            self.path = solve_maze_backtracking(maze, (self.row, self.col), target) or []
        elif algorithm == "BFS":
            print(f"Running BFS for boat at ({self.row}, {self.col})")
            self.path = solve_maze_bfs(maze, (self.row, self.col), target) or []
        elif algorithm == "A*":
            print(f"Running A* for boat at ({self.row}, {self.col})")
            self.path = solve_maze_astar(maze, (self.row, self.col), target) or []
        elif algorithm == "Simulated Annealing":
            print(f"Running Simulated Annealing for boat at ({self.row}, {self.col})")
            self.path = solve_maze_simulated_annealing(maze, (self.row, self.col), target) or []
        else:
            self.path = []  # Không tìm thấy đường đi

        self.path_index = 0
        if not self.path:
            print(f"No path found using {algorithm}. Boat remains at ({self.row}, {self.col}).")


    '''def move(self, maze):
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
            self.last_move_time = current_time'''
    
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

                # Chỉ di chuyển nếu bước tiếp theo là hợp lệ
                if 0 <= next_row < len(maze) and 0 <= next_col < len(maze[0]) and maze[next_row][next_col] == 0:
                    self.row = next_row
                    self.col = next_col
                    self.path_index += 1
                    print(f"Boat moved to ({self.row}, {self.col})")
                else:
                    print(f"Boat cannot move to ({next_row}, {next_col}).")
            else:
                print("Boat reached the end of its path.")
            self.last_move_time = current_time




    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        surface.blit(self.image, (x, y))

# Lớp key
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

# Hàm random key
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

# Hàm ai di chuyển
def ai_move(auto_move_path, auto_move_index, maze_matrix):
    if auto_move_path is not None and auto_move_index < len(auto_move_path):
        direction = auto_move_path[auto_move_index]
        player.move(direction, maze_matrix)  # Assuming player is an instance of Player
        return auto_move_index + 1
    return auto_move_index  

# Hàm reset lại game
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

# Vẽ nút 
def draw_rounded_button(button_rect, text, color, font_size, border_color_outer=Colors.PURPLE_2, border_color_inner=Colors.LIGHT_YELLOW, border_thickness=3, radius=0, offset_x=-40):
    # Điều chỉnh vị trí của nút bằng cách dịch sang trái `offset_x` pixel
    adjusted_rect = button_rect.move(offset_x, 0)
    
    pygame.draw.rect(screen, border_color_outer, adjusted_rect, border_thickness + 2, border_radius=radius)
    
    pygame.draw.rect(screen, border_color_inner, adjusted_rect.inflate(-border_thickness * 2, -border_thickness * 2), border_thickness, border_radius=radius)
    
    pygame.draw.rect(screen, color, adjusted_rect.inflate(-border_thickness * 4, -border_thickness * 4), border_radius=radius)
    
    font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", font_size)
    label = font.render(text, True, Colors.WHITE)
    screen.blit(label, label.get_rect(center=adjusted_rect.center))

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

def solve_maze_backtracking(maze, start, goal):
    """
    Thuật toán Backtracking để tìm đường đi từ start đến goal.
    """
    rows, cols = len(maze), len(maze[0])
    path = []  # Lưu các bước đi [(dx, dy)]
    visited = set()

    def backtrack(position):
        if position == goal:
            return True  # Tìm thấy đích

        row, col = position
        visited.add(position)

        # Thử tất cả các hướng (lên, xuống, trái, phải)
        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            next_position = (new_row, new_col)

            # Kiểm tra tính hợp lệ của ô tiếp theo
            if (0 <= new_row < rows and
                0 <= new_col < cols and
                maze[new_row][new_col] == 0 and  # 0 là đường đi
                next_position not in visited):  # Chưa thăm
                path.append((dx, dy))
                if backtrack(next_position):
                    return True
                # Nếu không tìm thấy đường, quay lui
                path.pop()

        # Gỡ trạng thái đã thăm khi quay lui
        visited.remove(position)
        return False

    if backtrack(start):
        return path
    return None  # Không tìm thấy đường đi

import math
import random

def solve_maze_simulated_annealing(maze, start, goal, initial_temp=100, cooling_rate=0.99, max_steps=1000):
    """
    Tìm đường đi trong mê cung bằng thuật toán Simulated Annealing.
    
    Args:
        maze (list): Ma trận mê cung.
        start (tuple): Vị trí bắt đầu (row, col).
        goal (tuple): Vị trí đích (row, col).
        initial_temp (float): Nhiệt độ ban đầu.
        cooling_rate (float): Tỷ lệ làm mát (giảm nhiệt độ).
        max_steps (int): Số bước tối đa.

    Returns:
        list: Đường đi từ start đến goal hoặc None nếu không tìm thấy.
    """
    current_state = start
    current_path = []
    temperature = initial_temp

    def calculate_cost(state):
        """Hàm đánh giá trạng thái dựa trên khoảng cách Manhattan đến goal."""
        return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

    def get_neighbors(state):
        """Trả về danh sách các trạng thái hàng xóm hợp lệ."""
        neighbors = []
        for dx, dy in directions:
            new_row, new_col = state[0] + dx, state[1] + dy
            if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] == 0:
                neighbors.append((new_row, new_col))
        return neighbors

    for step in range(max_steps):
        if current_state == goal:
            return current_path  # Đã tìm thấy đích

        neighbors = get_neighbors(current_state)
        if not neighbors:
            break  # Không còn trạng thái hợp lệ để thử

        next_state = random.choice(neighbors)
        cost_diff = calculate_cost(next_state) - calculate_cost(current_state)

        if cost_diff < 0 or random.random() < math.exp(-cost_diff / temperature):
            current_state = next_state
            current_path.append((next_state[0] - current_state[0], next_state[1] - current_state[1]))

        temperature *= cooling_rate  # Giảm nhiệt độ

    return None  # Không tìm thấy đường đi


button_reset = pygame.Rect(screen_width - 220, screen_height - 560, 200, 60)
button_backtracking = pygame.Rect(screen_width - 220, screen_height - 480, 200, 60) 
button_simulated_annealing = pygame.Rect(screen_width - 220, screen_height - 400, 200, 60)
button_bfs = pygame.Rect(screen_width - 220, screen_height - 320, 200, 60)
button_A = pygame.Rect(screen_width - 220, screen_height - 240, 200, 60)
button_home = pygame.Rect(screen_width - 220, screen_height - 160, 200, 60)
button_exit = pygame.Rect(screen_width - 220, screen_height - 80, 200, 60)

close_button = pygame.Rect(screen_width // 2 + win_image.get_width() // 2 - 30,
                           screen_height // 2 - win_image.get_height() // 2, 30, 30)


player = Player(0, 0)
boat = Boat(maze_size - 1, 0)
maze = Maze(maze_matrix)
num_keys = random.randint(3, 5)
keys = generate_random_keys(maze_matrix, num_keys, key_image)
collected_keys = 0

game_over = False  # Biến kiểm tra trạng thái trò chơi; False nghĩa là trò chơi vẫn đang diễn ra
player_won = False  # Biến kiểm tra xem người chơi đã thắng hay chưa; False nghĩa là người chơi chưa thắng
algorithm_selected = None  # Biến để lưu thuật toán đã chọn; None nghĩa là chưa có thuật toán nào được chọn
start_time = pygame.time.get_ticks()  # Lưu thời gian bắt đầu trò chơi
ai_active = False  # Biến kiểm tra xem AI có đang hoạt động hay không; False nghĩa là AI chưa hoạt động
auto_move_delay = 10  # Độ trễ (ms) giữa các bước tự động
last_move_time = pygame.time.get_ticks()  # Theo dõi thời gian của lần di chuyển cuối cùng
while True:
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
            elif button_A.collidepoint(event.pos):
                print("A* button clicked")
                algorithm_selected = "A*"
            elif button_backtracking.collidepoint(event.pos):
                print("AC3+Backtracking button clicked")
                algorithm_selected = "Backtracking"
            elif button_simulated_annealing.collidepoint(event.pos):
                print("Simulated Annealing button clicked")
                algorithm_selected = "Simulated Annealing"
                boat.update_path(maze_matrix, (player.row, player.col), algorithm_selected)
                boat.update_path(maze_matrix, (player.row, player.col), algorithm_selected)
            elif button_exit.collidepoint(event.pos):
                print("Exit button clicked")
                pygame.quit()
                sys.exit() 

    current_time = pygame.time.get_ticks() # Lấy thời gian hiện tại
    elapsed_time = (current_time - start_time) // 1000 # Thời gian cho ai bắt đầu chạy

    if elapsed_time >= 5 and algorithm_selected and not game_over:
        ai_active = True
        boat.update_path(maze_matrix, (player.row, player.col), algorithm_selected)
        boat.move(maze_matrix)

        if player.is_at_goal():
            pygame.time.delay(3000)
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
 
    for key in keys:
        if not key.collected and player.row == key.row and player.col == key.col:
            key.collected = True
            collected_keys += 1

    screen.blit(background_image, (0, 0))
    for planet in planets:
        planet.update()
        planet.draw(screen)
    goal_x = (maze_size - 1) * cell_width + (cell_width - goal_rect.width) // 2
    goal_y = (maze_size - 1) * cell_height + (cell_height - goal_rect.height) // 2
    screen.blit(goal_image, (goal_x, goal_y))
    maze.draw(screen)
    player.draw(screen)
    boat.draw(screen)
    for key in keys:
        key.draw(screen)

    draw_rounded_button(button_reset, "Reset", Colors.DARK_BLUE, 36 )
    draw_rounded_button(button_home, "Home",Colors.DARK_BLUE, 36)
    draw_rounded_button(button_bfs, "BFS", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_simulated_annealing, "Simulated Annealing", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_exit, "Exit", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_A, "A*", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_backtracking, "Backtracking", Colors.DARK_BLUE, 36)

    keys_textbox_rect = pygame.Rect(screen_width - 400, 60, 300, 50)
    pygame.draw.rect(screen, Colors.WHITE, keys_textbox_rect, 3)  # Vẽ viền
    pygame.draw.rect(screen, Colors.PINK, keys_textbox_rect.inflate(-3*2, -3*2))  # Vẽ nền (3: độ dày của viền)

    keys_text = font.render(f"Keys: {collected_keys}/{num_keys}", True, Colors.WHITE)
    keys_text_rect = keys_text.get_rect(center=keys_textbox_rect.center)  # Canh giữa văn bản trong textbox
    screen.blit(keys_text, keys_text_rect)

    if game_over:
        if player_won:
            screen.blit(win_image, (screen_width // 2 - win_image.get_width() // 2,
                                    screen_height // 2 - win_image.get_height() // 2))
        else:
            screen.blit(lose_image, (screen_width // 2 - lose_image.get_width() // 2,
                                    screen_height // 2 - lose_image.get_height() // 2))
    
    pygame.display.flip()
