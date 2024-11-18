import pygame
import random
import sys
import json
import heapq
from collections import deque
from Colors import Colors

# Khởi tạo Pygame
pygame.init()
info = pygame.display.Info()

SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
print(SCREEN_WIDTH,SCREEN_HEIGHT)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)


screen_width, screen_height = info.current_w, info.current_h
print(screen_width,screen_height)

CLOCK = pygame.time.Clock()
background_image = pygame.image.load('Image/bgbg.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


MAZE_WIDTH_RATIO = 2 / 3
MAZE_WIDTH = int(SCREEN_WIDTH * MAZE_WIDTH_RATIO)
BACKGROUND_MUSIC = 'Sound/8bit.mp3'
WIN_IMAGE_PATH = "Image/win.jpg"
LOSE_IMAGE_PATH = "Image/lose.jpg"
BACKGROUND_IMAGE_PATH = 'Image/bgbg.jpg'
PATH_IMAGE_PATH = 'Image/blockk.png'
GOAL_IMAGE_PATH = 'Image/moon.png'
PLANET_IMAGE_PATHS = ['Image/planet1.png', 'Image/planet2.png', 'Image/planet3.png']
PLAYER_IMAGE_PATH = 'Image/rocket.png'
BOAT_IMAGE_PATH = 'Image/ufo.png'
KEY_IMAGE_PATH = 'Image/key.png'
FONT_PATH = "Font/Jomplang-6Y3Jo.ttf"
FONT_SIZE = 36

# Các hướng di chuyển: lên, xuống, trái, phải
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Đọc độ khó
with open('difficulty.txt', 'r') as f:
    MAZE_SIZE = int(f.read().strip())


# Đọc ma trận maze
with open(f"Maze/{MAZE_SIZE}.txt", "r") as f:
    MAZE_MATRIX = json.load(f)

CELL_WIDTH = MAZE_WIDTH // len(MAZE_MATRIX[0])
CELL_HEIGHT = SCREEN_HEIGHT // len(MAZE_MATRIX)

# Hàm tải ảnh
def load_image(path, size=None):
    try:
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        sys.exit()

# Tải ảnh
background_image = load_image(BACKGROUND_IMAGE_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT))
path_image = load_image(PATH_IMAGE_PATH, (CELL_WIDTH, CELL_HEIGHT))
goal_image = load_image(GOAL_IMAGE_PATH, (CELL_WIDTH, CELL_HEIGHT))
win_image = load_image(WIN_IMAGE_PATH, (600, 450))
lose_image = load_image(LOSE_IMAGE_PATH, (600, 450))
planet_images = [load_image(p, (85, 64)) for p in PLANET_IMAGE_PATHS]
player_image = load_image(PLAYER_IMAGE_PATH, (CELL_WIDTH, CELL_HEIGHT))
boat_image = load_image(BOAT_IMAGE_PATH, (CELL_WIDTH, CELL_HEIGHT))
key_image = load_image(KEY_IMAGE_PATH, (CELL_WIDTH, CELL_HEIGHT))

# Tải âm thanh
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  # Phát liên tục
win_sound = pygame.mixer.Sound("Sound/happy.mp3")

# Tải font
font = pygame.font.Font(FONT_PATH, FONT_SIZE)

# Định nghĩa các lớp
class Planet:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(
            topleft=(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT - 50)))
        self.speed = random.randint(1, 5)
        self.direction = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x < -self.rect.width or self.rect.x > SCREEN_WIDTH:
            self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100)
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
            self.direction = random.choice([-1, 1])

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Maze:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])

    def draw(self, surface):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.matrix[row][col] == 1:
                    x, y = col * CELL_WIDTH, row * CELL_HEIGHT
                    surface.blit(path_image, (x, y))
                    self.draw_wall_border(surface, row, col)
        self.draw_stylized_border(surface)

    def draw_wall_border(self, surface, row, col):
        x, y = col * CELL_WIDTH, row * CELL_HEIGHT
        outer_border_color = (186, 85, 211) 
        inner_border_color = (255, 250, 150) 

        adjacent = [
            ((x, y), (x + CELL_WIDTH, y), row > 0 and self.matrix[row - 1][col] == 0),          
            ((x, y + CELL_HEIGHT), (x + CELL_WIDTH, y + CELL_HEIGHT), row < self.rows - 1 and self.matrix[row + 1][col] == 0),
            ((x, y), (x, y + CELL_HEIGHT), col > 0 and self.matrix[row][col - 1] == 0),        
            ((x + CELL_WIDTH, y), (x + CELL_WIDTH, y + CELL_HEIGHT), col < self.cols - 1 and self.matrix[row][col + 1] == 0)
        ]

        for start, end, condition in adjacent:
            if condition:
                pygame.draw.line(surface, outer_border_color, (start[0] - 1, start[1] - 1), (end[0] - 1, end[1] - 1), 3)
                pygame.draw.line(surface, inner_border_color, start, end, 2)

    def draw_stylized_border(self, surface):
        maze_width = self.cols * CELL_WIDTH
        maze_height = self.rows * CELL_HEIGHT
        corner_size = 10 

        layers = [
            ((186, 85, 211), 6),  
            ((64, 224, 208), 3)  
        ]

        for color, thickness in layers:
            pygame.draw.rect(surface, color, (0, 0, maze_width, maze_height), thickness, border_radius=corner_size)

class Player:
    def __init__(self):
        self.original_image = player_image
        self.image = self.original_image
        self.reset_position()
        self.game_completed = False 

    def reset_position(self):
        self.row = 0
        self.col = 0
        self.game_completed = False 
        self.image = self.original_image

    def is_at_goal(self):
        return self.row == MAZE_SIZE - 1 and self.col == MAZE_SIZE - 1 and collected_keys == num_keys

    def move(self, direction, maze_matrix):
        if self.game_completed:
            return False

        new_row = self.row + direction[0]
        new_col = self.col + direction[1]

        if (0 <= new_row < len(maze_matrix) and 
            0 <= new_col < len(maze_matrix[0]) and 
            maze_matrix[new_row][new_col] == 0):
            
            # Xoay ảnh người chơi dựa trên hướng di chuyển
            if direction == (-1, 0):  # Lên
                self.image = player_image
            elif direction == (1, 0):  # Xuống
                self.image = pygame.transform.rotate(player_image, 180)
            elif direction == (0, -1):  # Trái
                self.image = pygame.transform.rotate(player_image, 90)
            elif direction == (0, 1):  # Phải
                self.image = pygame.transform.rotate(player_image, -90)
            
            self.row = new_row
            self.col = new_col

            if self.is_at_goal():
                self.game_completed = True
            return True
        return False

    def draw(self, surface):
        x = self.col * CELL_WIDTH
        y = self.row * CELL_HEIGHT
        surface.blit(self.image, (x + (CELL_WIDTH - self.image.get_width()) // 2, 
                                  y + (CELL_HEIGHT - self.image.get_height()) // 2))

class Boat:
    def __init__(self):
        self.row = MAZE_SIZE - 1
        self.col = 0
        self.image = boat_image
        self.path = []
        self.path_index = 0
        self.algorithm = None
        self.last_move_time = 0
        self.move_delay = 1000  # ms

    def update_path(self, maze, target, algorithm):
        self.algorithm = algorithm
        if algorithm == "BFS":
            self.path = solve_maze_bfs(maze, (self.row, self.col), target)
        elif algorithm == "DFS":
            self.path = solve_maze_dfs(maze, (self.row, self.col), target)
        elif algorithm == "A*":
            self.path = solve_maze_astar(maze, (self.row, self.col), target)
        elif algorithm == "Backtracking":
            self.path = solve_backtracking(maze, (self.row, self.col), target)
        else:
            self.path = []
        self.path_index = 0

    def move(self, maze):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_delay:
            if self.path and self.path_index < len(self.path):
                direction = self.path[self.path_index]
                next_row = self.row + direction[0]
                next_col = self.col + direction[1]
                if maze[next_row][next_col] == 0:
                    self.row = next_row
                    self.col = next_col
                    self.path_index += 1
            self.last_move_time = current_time

    def draw(self, surface):
        x = self.col * CELL_WIDTH
        y = self.row * CELL_HEIGHT
        surface.blit(self.image, (x, y))

class Key:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.image = key_image
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            x = self.col * CELL_WIDTH
            y = self.row * CELL_HEIGHT
            surface.blit(self.image, (x, y))

# Thuật toán tìm đường
def solve_maze_bfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = {start}
    came_from = {}

    while queue:
        current = queue.popleft()
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < rows and 
                0 <= neighbor[1] < cols and 
                maze[neighbor[0]][neighbor[1]] == 0 and 
                neighbor not in visited):
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current
    return None

def solve_maze_dfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    stack = [start]
    visited = {start}
    came_from = {}

    while stack:
        current = stack.pop()
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < rows and 
                0 <= neighbor[1] < cols and 
                maze[neighbor[0]][neighbor[1]] == 0 and 
                neighbor not in visited):
                stack.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current
    return None

def solve_maze_astar(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < rows and 
                0 <= neighbor[1] < cols and 
                maze[neighbor[0]][neighbor[1]] == 0):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
    return None

def solve_backtracking(maze, start, goal):
    path = []
    visited = set()

    def backtrack(current):
        if current == goal:
            return True
        visited.add(current)
        for direction in sorted(DIRECTIONS, key=lambda d: heuristic((current[0] + d[0], current[1] + d[1]), goal)):
            next_cell = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= next_cell[0] < len(maze) and 
                0 <= next_cell[1] < len(maze[0]) and 
                maze[next_cell[0]][next_cell[1]] == 0 and 
                next_cell not in visited):
                path.append(direction)
                if backtrack(next_cell):
                    return True
                path.pop()
        return False

    if backtrack(start):
        return path
    return None

def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current != start:
        prev = came_from.get(current)
        if not prev:
            break
        direction = (current[0] - prev[0], current[1] - prev[1])
        path.append(direction)
        current = prev
    path.reverse()
    return path

def generate_random_keys(maze_matrix, num_keys):
    keys = []
    rows, cols = len(maze_matrix), len(maze_matrix[0])
    while len(keys) < num_keys:
        row, col = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if (maze_matrix[row][col] == 0 and (row, col) not in [(0, 0), (rows - 1, cols - 1)] 
            and not any(key.row == row and key.col == col for key in keys)):
            keys.append(Key(row, col))
    return keys

def draw_button(surface, rect, text, color, border_color_outer, border_color_inner, border_thickness, radius=0, offset_x=-40):
    adjusted_rect = rect.move(offset_x, 0)
    pygame.draw.rect(surface, border_color_outer, adjusted_rect, border_thickness + 2, border_radius=radius)
    pygame.draw.rect(surface, border_color_inner, adjusted_rect.inflate(-border_thickness * 2, -border_thickness * 2), border_thickness, border_radius=radius)
    pygame.draw.rect(surface, color, adjusted_rect.inflate(-border_thickness * 4, -border_thickness * 4), border_radius=radius)
    label = font.render(text, True, Colors.WHITE)
    label_rect = label.get_rect(center=adjusted_rect.center)
    surface.blit(label, label_rect)
def initialize_game():
    global player, boat, planets, num_keys, keys, collected_keys, start_time, ai_active
    player = Player()
    boat = Boat()
    planets = [Planet(img) for img in planet_images]
    num_keys = random.randint(3, 5)  # Đặt lại số lượng khóa
    keys = generate_random_keys(MAZE_MATRIX, num_keys)
    collected_keys = 0
    start_time = pygame.time.get_ticks()  # Reset start time
    ai_active = False  # Reset AI active state

# Khởi tạo các đối tượng trong game
player = Player()
boat = Boat()
planets = [Planet(img) for img in planet_images]
num_keys = random.randint(3, 5)
keys = generate_random_keys(MAZE_MATRIX, num_keys)
collected_keys = 0

# Định nghĩa các nút
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 60
BUTTON_X = SCREEN_WIDTH - 220
BUTTON_Y_START = SCREEN_HEIGHT - 560
BUTTON_SPACING = 80

buttons = {
    "Reset": pygame.Rect(BUTTON_X, BUTTON_Y_START, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Backtracking": pygame.Rect(BUTTON_X, BUTTON_Y_START + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),
    "DFS": pygame.Rect(BUTTON_X, BUTTON_Y_START + 2 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),
    "BFS": pygame.Rect(BUTTON_X, BUTTON_Y_START + 3 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),
    "A*": pygame.Rect(BUTTON_X, BUTTON_Y_START + 4 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Home": pygame.Rect(BUTTON_X, BUTTON_Y_START + 5 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Exit": pygame.Rect(BUTTON_X, BUTTON_Y_START + 6 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),
}

# Khởi tạo các đối tượng trong game
initialize_game()

# Các biến trạng thái của game
game_over = False
player_won = False
algorithm_selected = None
start_time = pygame.time.get_ticks()
ai_active = False
ai_completed = False


# Hình ảnh và nút đóng khi kết thúc game
WIN_SOUND_PLAYED = False
show_image = True
close_button = pygame.Rect(SCREEN_WIDTH // 2 + 300 - 30, SCREEN_HEIGHT // 2 - 225, 30, 30)  # Điều chỉnh dựa trên kích thước win_image

# Hàm chọn thuật toán
def select_algorithm():
    global algorithm_selected, start_time, ai_active
    # Chọn thuật toán (ví dụ: BFS)
    algorithm_selected = "BFS"  # Hoặc có thể thay đổi thành thuật toán khác
    start_time = pygame.time.get_ticks()  # Đặt lại thời gian bắt đ���u
    ai_active = False  # Đặt trạng thái AI không hoạt động

def restart_game():
    global game_over, player_won, algorithm_selected, ai_active, ai_completed
    initialize_game()  # Reset game state
    game_over = False
    player_won = False
    algorithm_selected = None
    ai_active = False
    ai_completed = False

# Vòng lặp chính của game
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
                direction = (0, -1)
            elif event.key == pygame.K_RIGHT:
                direction = (0, 1)
            elif event.key == pygame.K_UP:
                direction = (-1, 0)
            elif event.key == pygame.K_DOWN:
                direction = (1, 0)
            if direction:
                player.move(direction, MAZE_MATRIX)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for btn_text, btn_rect in buttons.items():
                if btn_rect.collidepoint(mouse_pos):
                    if btn_text == "Reset":
                        initialize_game()
                        game_over = False
                        player_won = False
                        algorithm_selected = None
                        ai_active = False
                        ai_completed = False
                    elif btn_text in ["BFS", "DFS", "A*", "Backtracking"]:
                        select_algorithm()  # Gọi hàm chọn thuật toán
                        start_time = pygame.time.get_ticks()  # Reset start time when selecting algorithm
                    elif btn_text == "Home":
                        pygame.mixer.music.stop()
                        # Không nên sử dụng exec. Thay vào đó, hãy xem xét sử dụng các module hoặc script riêng.
                        pygame.quit()
                        sys.exit()
                    elif btn_text == "Exit":
                        pygame.quit()
                        sys.exit()
            # Xử lý nút đóng trong màn hình kết quả
            if show_image and close_button.collidepoint(mouse_pos):
                show_image = False
                win_sound.stop()

    # Display the countdown timer

    # Cập nhật trạng thái game
    if algorithm_selected and not ai_active and elapsed_time >= 2:
        ai_active = True
        boat.update_path(MAZE_MATRIX, (player.row, player.col), algorithm_selected)

    if ai_active and not game_over:
        boat.move(MAZE_MATRIX)
        # Kiểm tra thuyền bắt được người chơi
        if (boat.row, boat.col) == (player.row, player.col):
            restart_game()  # Restart the game if the player collides with the boat
        # Kiểm tra người chơi đến đích
        if player.is_at_goal():
            if collected_keys == num_keys:
                game_over = True
                player_won = True
                if not WIN_SOUND_PLAYED:
                    win_sound.play()
                    WIN_SOUND_PLAYED = True
            else:
                print("You reached the goal but need to collect all keys!")

    # Thu thập keys
    for key in keys:
        if not key.collected and (player.row, player.col) == (key.row, key.col):
            key.collected = True
            collected_keys += 1

    # Vẽ mọi thứ
    SCREEN.blit(background_image, (0, 0))
    for planet in planets:
        planet.update()
        planet.draw(SCREEN)
    maze = Maze(MAZE_MATRIX)
    maze.draw(SCREEN)
    boat.draw(SCREEN)
    for key in keys:
        key.draw(SCREEN)
    # Vẽ đích
    goal_x = (MAZE_SIZE - 1) * CELL_WIDTH + (CELL_WIDTH - goal_image.get_width()) // 2
    goal_y = (MAZE_SIZE - 1) * CELL_HEIGHT + (CELL_HEIGHT - goal_image.get_height()) // 2
    SCREEN.blit(goal_image, (goal_x, goal_y))
    player.draw(SCREEN)

    # Vẽ số keys đã thu thập
    keys_text = font.render(f"Keys: {collected_keys}/{num_keys}", True, Colors.WHITE)
    keys_text_rect = keys_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    SCREEN.blit(keys_text, keys_text_rect)

    # Vẽ các nút
    for btn_text, btn_rect in buttons.items():
        draw_button(
            SCREEN, 
            btn_rect, 
            btn_text, 
            Colors.DARK_BLUE, 
            (186, 85, 211), 
            (255, 215, 0), 
            3, 
            radius=10
        )

    # Hiển thị hình ảnh kết quả
    if game_over and show_image:
        if player_won:
            SCREEN.blit(win_image, (SCREEN_WIDTH // 2 - win_image.get_width() // 2,
                                    SCREEN_HEIGHT // 2 - win_image.get_height() // 2))
        else:
            SCREEN.blit(lose_image, (SCREEN_WIDTH // 2 - lose_image.get_width() // 2,
                                     SCREEN_HEIGHT // 2 - lose_image.get_height() // 2))
        pygame.draw.rect(SCREEN, (255, 0, 0), close_button)  # Vẽ nút đỏ
        close_text = font.render("X", True, Colors.WHITE)
        close_text_rect = close_text.get_rect(center=close_button.center)
        SCREEN.blit(close_text, close_text_rect)

    # Hiển thị đếm ngược bắt đầu AI
    if not ai_active and algorithm_selected:
        remaining_time = max(0, 2 - elapsed_time)
        time_text = font.render(f"AI starts in: {remaining_time} s", True, Colors.WHITE)
        
        SCREEN.blit(time_text, (SCREEN_WIDTH - 200, 70))

    pygame.display.flip()
    CLOCK.tick(60)  # Giới hạn ở 60 FPS
