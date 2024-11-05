import pygame
<<<<<<< HEAD
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
=======
import sys
import random
from Colors import Colors

# Initialize pygame
pygame.init()


# Screen dimensions
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Maze Game Home")


pygame.mixer.music.load('Sound/chillmusic.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

# Load slider images
slider_image = pygame.image.load('Image/Slider.png')
slider_image = pygame.transform.scale(slider_image, (280, 30))
button_image = pygame.image.load('Image/Dragger.png')
button_image = pygame.transform.scale(button_image, (30, 50))


# Load difficulty level images (for levels 1 to 10)
difficulty_images = [pygame.image.load(f'Image/Level{i}.png') for i in range(1, 2)]
difficulty_images = [pygame.transform.scale(img, (200, 200)) for img in difficulty_images]


# Create a list of stars for the background
def create_stars(num_stars):
    stars = []
    for _ in range(num_stars):
        star = {
            'x': random.randint(0, screen_width),
            'y': random.randint(0, screen_height),
            'size': random.randint(1, 3),
            'visible': True
        }
        stars.append(star)
    return stars

# Draw background with stars
def draw_background():
    screen.fill((0, 0, 0))
    for star in stars:
        if star['visible']:
            pygame.draw.circle(screen, Colors.WHITE, (star['x'], star['y']), star['size'])

# Draw colored text
def draw_colored_text(surface, text, center):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (75, 0, 130), (238, 130, 238)]
    font = pygame.font.Font("Front/diego3d.ttf", 60)
    angle = 0
    total_width = sum(font.size(char)[0] * 1.2 for char in text)
    start_x = (screen_width - total_width) // 2
    position_y = 20

    for i, char in enumerate(text):
        char_color = colors[i % len(colors)]
        char_surface = font.render(char, True, char_color)
        char_rect = char_surface.get_rect(topleft=(start_x + angle, position_y))
        surface.blit(char_surface, char_rect)
        angle += font.size(char)[0] * 1.2

# Draw rounded button
def draw_rounded_button(surface, text, x, y, width, height, color, font_size):
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=15)
    font = pygame.font.Font("Front/04054_BeamRider3D (1).ttf", font_size)
    label = font.render(text, True, Colors.WHITE)
    text_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(label, text_rect)

# Draw the difficulty slider
def draw_difficulty_slider(surface, x, y, width, height, min_value, max_value, current_value):
    surface.blit(slider_image, (x, y))
    slider_x = x + int((current_value - min_value) / (max_value - min_value) * width)
    surface.blit(button_image, (slider_x - 10, y - 10))

    # Kiểm tra xem current_value có hợp lệ không
    if 1 <= current_value <= len(difficulty_images):
        image = difficulty_images[current_value - 1]
        surface.blit(image, (x + width + 20, y - 100))
    else:
        # Nếu không, có thể vẽ một hình ảnh mặc định hoặc không làm gì cả
        print("Current value is out of range for difficulty images.")
    
    font = pygame.font.SysFont("timesnewroman", 24, bold=True)
    value_text = font.render(f"{current_value}", True, Colors.YELLOW)
    surface.blit(value_text, (x + width + 20, y + (height // 2) - (value_text.get_height() // 2)))



# Set custom font
custom_font = pygame.font.Font("Front/UTM-Birds-Paradise.ttf", 20)
#difficulty_value = 10  # Giá trị ban đầu của thanh trượt là 10


# Main variables
stars = create_stars(100)  # Generate 100 stars
difficulty_value = 1  # Initial difficulty level

# Main game loop

# Hàm vẽ thanh trượt độ khó
"""def draw_difficulty_slider(surface, x, y, width, height, min_value, max_value, current_value):
    pygame.draw.rect(surface, Colors.YELLOW, (x, y, width, height))
    slider_x = x + int((current_value - min_value) / (max_value - min_value) * width)
    pygame.draw.rect(surface, Colors.WHITE, (slider_x - 10, y - 5, 20, height + 10))
    
    # Hiển thị giá trị hiện tại của thanh trượt
    font = pygame.font.SysFont("timesnewroman", 24, bold=True)
    value_text = font.render(f"{current_value}", True, Colors.YELLOW)
    surface.blit(value_text, (x + width + 20, y + (height // 2) - (value_text.get_height() // 2)))  # Xuất hiện bên phải thanh trượt
"""
stars = create_stars(100)

# Vòng lặp chính

>>>>>>> temp
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
<<<<<<< HEAD
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

            elif event.key == pygame.K_h:  # Nhấn B để quay lại home.py
                pygame.mixer.music.stop()
                exec(open("Home.py", encoding="utf-8").read())
            elif event.key == pygame.K_b:  # Nhấn B để chạy BFS
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
=======
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            #if screen_width // 2 - 140 <= mouse_x <= screen_width // 2 + 140 and 280 <= mouse_y <= 310:
             #   difficulty_value = int((mouse_x - (screen_width // 2 - 140)) / 280 * 10) + 1


            # Kiểm tra nếu click vào thanh trượt
            if screen_width // 2 - 140 <= mouse_x <= screen_width // 2 + 140 and 280 <= mouse_y <= 310:
                difficulty_value = ((mouse_x - (screen_width // 2 - 140)) // 28 + 1) * 10

            # Kiểm tra nếu click vào nút "Start"
            elif screen_width // 2 - 100 <= mouse_x <= screen_width // 2 + 100 and 350 <= mouse_y <= 410:
                pygame.mixer.music.stop()
 # Dừng âm thanh nền
                
                with open('difficulty.txt', 'w') as f:
                    f.write("")
                    f.write(str(difficulty_value))
                exec(open("Game.py", encoding="utf-8").read())

            # Kiểm tra nếu click vào nút "Exit"
            elif screen_width - 220 <= mouse_x <= screen_width - 20 and screen_height - 80 <= mouse_y <= screen_height - 20:
                pygame.quit()
                sys.exit()



    draw_background()  # Draw background with stars
   # background_sound.play()

    draw_colored_text(screen, "AI MAZE GAME", (screen_width // 2, 0))

    custom_text = custom_font.render("MADE BY DUNG - DUONG - TRAN", True, Colors.PINK)
    subtitle_rect = custom_text.get_rect(center=(screen_width // 2, 90))
    screen.blit(custom_text, subtitle_rect)

    difficulty_font = pygame.font.SysFont("timesnewroman", 24)
    difficulty_label = difficulty_font.render(" SIZE: ", True, Colors.WHITE)
    screen.blit(difficulty_label, (screen_width // 2 - 230, 280))

    draw_difficulty_slider(screen, screen_width // 2 - 140, 280, 280, 30, 10, 100, difficulty_value)
    draw_rounded_button(screen, "START", screen_width // 2 - 100, 350, 200, 60, Colors.DARK_BLUE, 36)
    draw_rounded_button(screen, "Exit", screen_width - 220, screen_height - 80, 200, 60, Colors.DARK_BLUE, 36)


    for star in stars:
        if random.random() < 0.01:
            star['visible'] = not star['visible']

    pygame.display.flip()
>>>>>>> temp
