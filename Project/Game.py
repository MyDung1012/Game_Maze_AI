import pygame
import random
import sys
from Colors import Colors
from enum import Enum
import json
from collections import deque  # Thêm deque cho BFS


# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
maze_width = screen_width * 2 // 3  # Mê cung chiếm 2/3 màn hình bên trái

#âm thanh 
pygame.mixer.music.load('Sound/8bit.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()
try:
    with open('difficulty.txt', 'r') as f:
        maze_size = int(f.read().strip())
except (FileNotFoundError, ValueError) as e:
    print(f"Error reading difficulty: {e}")
    maze_size = 10  # Default size

# Load maze matrix
try:
    with open(f"maze/{maze_size}.txt", "r") as f:
        maze_matrix = json.load(f)
except (FileNotFoundError, SyntaxError) as e:
    print(f"Error loading maze file: {e}")
    sys.exit()
# Kích thước của từng ô trong mê cung
cell_width = maze_width // len(maze_matrix[0])  # Tính kích thước ô dựa trên chiều rộng mê cung
cell_height = screen_height // len(maze_matrix)
try:
    # Lấy kích thước màn hình từ pygame display surface
    screen_width, screen_height = pygame.display.get_surface().get_size()
    
    # Tải và scale hình nền trực tiếp theo kích thước màn hình
    background_image = pygame.image.load('Image/ground.jpg')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    sys.exit()

# Tải hình ảnh đường đi
try:
    path_image = pygame.image.load('Image/gray-wall.jpg')  # Đường đi sẽ sử dụng hình ảnh này
    path_image = pygame.transform.scale(path_image, (cell_width, cell_height))  # Điều chỉnh kích thước hình ảnh đường đi
except pygame.error as e:
    print(f"Error loading path image: {e}")
    sys.exit()

# Hình ảnh hành tinh
try:
    planet_images = [
        pygame.image.load('Image/planet1.png'),  # Hành tinh 1
        pygame.image.load('Image/planet2.png'),  # Hành tinh 2
        pygame.image.load('Image/planet3.png')   # Hành tinh 3
    ]
except pygame.error as e:
    print(f"Error loading planet images: {e}")
    sys.exit()

# Lớp Hành tinh
class Planet:
    def __init__(self, image, x, y):
        self.image = pygame.transform.scale(image, (85, 64))  # Điều chỉnh kích thước
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.randint(1, 5)
        self.direction = random.choice([-1, 1])  # Di chuyển trái hoặc phải

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x < -self.rect.width or self.rect.x > screen_width:
            self.rect.x = random.randint(screen_width, screen_width + 100)
            self.rect.y = random.randint(0, screen_height - self.rect.height)
            self.direction = random.choice([-1, 1])

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Lớp Mê cung
class Maze:
    def __init__(self, matrix):
        self.matrix = matrix

    def draw(self, surface):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                x = col * cell_width
                y = row * cell_height
                if self.matrix[row][col] == 1:
                    # Không vẽ gì cho ô 1 (trong suốt), chỉ vẽ viền vàng
                    self.draw_borders(surface, row, col, x, y)
                else:
                    # Vẽ đường đi bằng hình ảnh đường đi
                    surface.blit(path_image, (x, y))

    def draw_borders(self, surface, row, col, x, y):
        # Kiểm tra các ô lân cận (trái, phải, trên, dưới) xem có giá trị 1 hay không
        top = row > 0 and self.matrix[row - 1][col] == 1
        bottom = row < len(self.matrix) - 1 and self.matrix[row + 1][col] == 1
        left = col > 0 and self.matrix[row][col - 1] == 1
        right = col < len(self.matrix[row]) - 1 and self.matrix[row][col + 1] == 1

        # Vẽ viền xung quanh nếu ô hiện tại là 1
        if not top:
            pygame.draw.line(surface, Colors.YELLOW, (x, y), (x + cell_width, y), 2)  # Viền trên
        if not bottom:
            pygame.draw.line(surface, Colors.YELLOW, (x, y + cell_height), (x + cell_width, y + cell_height), 2)  # Viền dưới
        if not left:
            pygame.draw.line(surface, Colors.YELLOW, (x, y), (x, y + cell_height), 2)  # Viền trái
        if not right:
            pygame.draw.line(surface, Colors.YELLOW, (x + cell_width, y), (x + cell_width, y + cell_height), 2)  # Viền phải


# Tạo danh sách hành tinh
planets = [Planet(planet_images[i], random.randint(0, screen_width), random.randint(0, screen_height - 50)) for i in range(3)]

# Khởi tạo mê cung
maze = Maze(maze_matrix)



# Lớp Player
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (1, -1)
    DOWN_LEFT = (-1, 1)
    DOWN_RIGHT = (1, 1)

class Player:
    def __init__(self, row, col):
        self.reset_position()
        self.game_completed = False  # Thêm biến trạng thái mới
        
    def reset_position(self):
        self.row = 0
        self.col = 0
        self.steps = 0
        self.game_completed = False  # Reset trạng thái game khi restart
    
    def is_at_goal(self):
        return self.row == maze_size - 1 and self.col == maze_size - 1   # Kiểm tra vị trí đích

    def move(self, direction, maze_matrix):
        # Nếu game đã hoàn thành, không cho phép di chuyển
        if self.game_completed:
            return False
            
        new_row = self.row + direction[1]
        new_col = self.col + direction[0]
        
        # In ra để debug
        print(f"Trying to move to: row={new_row}, col={new_col}")
        
        if (0 <= new_row < len(maze_matrix) and 
            0 <= new_col < len(maze_matrix[0]) and 
            maze_matrix[new_row][new_col] == 1):
            self.row = new_row
            self.col = new_col
            self.steps += 1
            # Kiểm tra xem người chơi đã đến đích chưa
            if self.is_at_goal():
                self.game_completed = True
            return True
        return False
    
    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        player_color = Colors.RED
        player_size = min(cell_width, cell_height) // 2
        center_x = x + cell_width // 2
        center_y = y + cell_height // 2
        pygame.draw.circle(surface, player_color, (center_x, center_y), player_size)

# Add after maze initialization
player = Player(0, 0)  # Changed from Player(1, 1)
def solve_maze_bfs(maze_matrix, start, goal):
    rows, cols = len(maze_matrix), len(maze_matrix[0])
    queue = deque([(start[0], start[1], [])])  # Hàng đợi BFS lưu tọa độ và đường đi hiện tại
    visited = set()  # Tập hợp các vị trí đã ghé qua
    directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

    while queue:
        row, col, path = queue.popleft()
        
        if (row, col) == goal:
            return path  # Trả về đường đi đã tìm được đến đích

        for direction in directions:
            new_row, new_col = row + direction.value[1], col + direction.value[0]
            
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                maze_matrix[new_row][new_col] == 1 and
                (new_row, new_col) not in visited):
                
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, path + [direction.value]))  # Thêm bước di chuyển vào đường đi

    return None  # Trả về None nếu không tìm thấy đường đi

# Initialize auto_move_path, auto_move_index, and AI_step
auto_move_path = None
auto_move_index = 0
AI_step = 0  # Initialize AI_step to count DFS steps

# Initialize font
font = pygame.font.Font(None, 36)  # Add this line to initialize the font

# Initialize player_step_counter
player_step_counter = 0  # Separate counter for player's manual steps

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP1:
                if player.move((-1, 1), maze_matrix):  # Down-Left
                    player_step_counter += 1
            elif event.key == pygame.K_KP2:
                if player.move((0, 1), maze_matrix):   # Down
                    player_step_counter += 1
            elif event.key == pygame.K_KP3:
                if player.move((1, 1), maze_matrix):   # Down-Right
                    player_step_counter += 1
            elif event.key == pygame.K_KP4:
                if player.move((-1, 0), maze_matrix):  # Left
                    player_step_counter += 1
            elif event.key == pygame.K_KP6:
                if player.move((1, 0), maze_matrix):   # Right
                    player_step_counter += 1
            elif event.key == pygame.K_KP7:
                if player.move((-1, -1), maze_matrix): # Up-Left
                    player_step_counter += 1
            elif event.key == pygame.K_KP8:
                if player.move((0, -1), maze_matrix):  # Up
                    player_step_counter += 1
            elif event.key == pygame.K_KP9:
                if player.move((1, -1), maze_matrix):  # Up-Right
                    player_step_counter += 1
            elif event.key == pygame.K_r:  # Nhấn R để restart
                player.reset_position()
            elif event.key == pygame.K_n:
                player.reset_position()
                player_step_counter = 0  # Reset player step counter
                AI_step = 0
            elif event.key == pygame.K_ESCAPE:  # Nhấn ESC để thoát
                pygame.quit()
                sys.exit()

            elif event.key == pygame.K_h:  # Nhấn H để quay lại home.py
                pygame.mixer.music.stop()
                exec(open("Home.py", encoding="utf-8").read())
            elif event.key == pygame.K_b:  # Nhấn B để chạy BFS
                player.reset_position()
                auto_move_path = solve_maze_bfs(maze_matrix, (player.row, player.col), (maze_size - 1, maze_size - 1))
                auto_move_index = 0

    if auto_move_path and auto_move_index < len(auto_move_path):
        direction = auto_move_path[auto_move_index]
        player.move(direction, maze_matrix)
        auto_move_index += 1  # Move to the next step
        AI_step += 1  # Increment AI_step for each move

    screen.blit(background_image, (0, 0))

    for planet in planets:
        planet.update()
        planet.draw(screen)

    # Vẽ mê cung
    maze.draw(screen)

    # Draw player
    player.draw(screen)
    
    # Draw AI step counter
    ai_step_text = font.render(f"AI Steps: {AI_step}", True, Colors.WHITE)
    screen.blit(ai_step_text, (screen_width - 300, 150))  # Display above player steps

    # Draw player step counter
    step_text = font.render(f"Steps: {player_step_counter}", True, Colors.WHITE)
    screen.blit(step_text, (screen_width - 300, 200))

    # Vẽ điểm đích
    goal_x = (maze_size - 1) * cell_width + cell_width // 2
    goal_y = (maze_size - 1) * cell_height + cell_height // 2

    pygame.draw.circle(screen, Colors.GREEN, (goal_x, goal_y), min(cell_width, cell_height) // 2)
    
    # Hiển thị thông báo hoàn thành
    font = pygame.font.Font(None, 36)
    game_completed = False
    
    if player.is_at_goal():
        game_completed = True
    


        
    # Hiển thị hướng dẫn
    instructions_restart = font.render("R: Restart", True, Colors.WHITE)
    instructions_restart_rect = instructions_restart.get_rect()
    instructions_restart_rect.topleft = (screen_width - 300, 250)
    screen.blit(instructions_restart, instructions_restart_rect)

    instructions_exit = font.render("ESC: Exit", True, Colors.WHITE)
    instructions_exit_rect = instructions_exit.get_rect()
    instructions_exit_rect.topleft = (screen_width - 300, 300)
    screen.blit(instructions_exit, instructions_exit_rect)

    instructions_back = font.render("H: Home", True, Colors.WHITE)
    instructions_back_rect = instructions_back.get_rect()
    instructions_back_rect.topleft = (screen_width - 300, 350)
    screen.blit(instructions_back, instructions_back_rect)

    instructions_new = font.render("N: New", True, Colors.WHITE)
    instructions_new_rect = instructions_new.get_rect()
    instructions_new_rect.topleft = (screen_width - 300, 400)
    screen.blit(instructions_new, instructions_new_rect)


    instructions_bfs = font.render("B: BFS", True, Colors.WHITE)
    instructions_bfs_rect = instructions_bfs.get_rect()
    instructions_bfs_rect.topleft = (screen_width - 300, 450)
    screen.blit(instructions_bfs, instructions_bfs_rect)



    if game_completed:
        instructions_win = font.render("DONE!!!", True, Colors.WHITE)
        instructions_win_rect = instructions_win.get_rect()
        instructions_win_rect.topleft = (screen_width - 300, 100)
        screen.blit(instructions_win, instructions_win_rect)
    # Cập nhật màn hình
    pygame.display.flip()
    pygame.time.delay(30)
