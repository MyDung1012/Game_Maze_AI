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

# Tải hình ảnh và âm thanh complete
win_image = pygame.image.load("Image/Done.jpg") 
win_image = pygame.transform.scale(win_image, (600, 450))
win_sound = pygame.mixer.Sound("Sound/chucmung.wav")
close_button = pygame.Rect(screen_width // 2 + win_image.get_width() // 2 - 30,
                                   screen_height // 2 - win_image.get_height() // 2, 30, 30)

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

goal_image = pygame.image.load('Image/moon.png')
goal_image = pygame.transform.scale(goal_image, (cell_width, cell_height))  # Resize to cell dimensions
goal_rect = goal_image.get_rect()
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
                if self.matrix[row][col] == 0: #sua gia tri duong di o day
                    # Không vẽ gì cho ô 1 (tường), chỉ vẽ viền vàng
                    self.draw_borders(surface, row, col, x, y)
                else:
                    # Vẽ đường đi bằng hình ảnh đường đi
                    surface.blit(path_image, (x, y))

    def draw_borders(self, surface, row, col, x, y):
        # Vẽ viền xung quanh nếu ô hiện tại là ô ngoài cùng
        if row == 0:  # Viền trên cùng
            pygame.draw.line(surface, Colors.YELLOW, (x, y), (x + cell_width, y), 2)
        if row == maze_size - 1:  # Viền dưới cùng
            pygame.draw.line(surface, Colors.YELLOW, (x, y + cell_height), (x + cell_width, y + cell_height), 2)
        if col == 0:  # Viền trái cùng
            pygame.draw.line(surface, Colors.YELLOW, (x, y), (x, y + cell_height), 2)
        if col == maze_size - 1:  # Viền phải cùng
            pygame.draw.line(surface, Colors.YELLOW, (x + cell_width, y), (x + cell_width, y + cell_height), 2)


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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.original_image = pygame.image.load('Image/rocket.png')# (Khai báo hình ảnh ban đầu ở đây, ví dụ: pygame.image.load("path/to/image.png"))
        self.image = self.original_image
        self.reset_position()
        self.game_completed = False  # Trạng thái game đã hoàn thành
        try:
            self.original_image = pygame.transform.scale(self.original_image, (cell_width, cell_height))
            self.image = self.original_image  # Hình ảnh hiện tại
        except pygame.error as e:
            print(f"Error loading rocket image: {e}")
            sys.exit()

    def reset_position(self):
        self.row = 0
        self.col = 0
        self.game_completed = False  # Reset trạng thái game khi restart
        self.image = self.original_image  # Đặt lại hình ảnh ban đầu
    
    def is_at_goal(self):
        return self.row == maze_size - 1 and self.col == maze_size - 1  # Kiểm tra vị trí đích
    
    def reset_game(self):
        global game_completed, sound_played, show_image, player_step_counter
        game_completed = False
        sound_played = False
        show_image = True
        player_step_counter = 0
        player.reset_position()

    def move(self, direction, maze_matrix):
        # Nếu game đã hoàn thành, không cho phép di chuyển
        if self.game_completed:
            return False
            
        new_row = self.row + direction[1]
        new_col = self.col + direction[0]
        
        # Kiểm tra tọa độ mới có hợp lệ và là đường đi hay không
        if (0 <= new_row < len(maze_matrix) and 
            0 <= new_col < len(maze_matrix[0]) and 
            maze_matrix[new_row][new_col] == 0):
            
            # Xác định góc xoay dựa trên hướng di chuyển
            if direction == (-1, 0):  # Trái
                self.image = pygame.transform.rotate(self.original_image, 90)
            elif direction == (1, 0):  # Phải
                self.image = pygame.transform.rotate(self.original_image, -90)
            elif direction == (0, -1):  # Lên
                self.image = pygame.transform.rotate(self.original_image, 0)
            elif direction == (0, 1):  # Xuống
                self.image = pygame.transform.rotate(self.original_image, 180)
                
            # Cập nhật vị trí
            self.row = new_row
            self.col = new_col

            # Kiểm tra xem người chơi đã đến đích chưa
            if self.is_at_goal():
                self.game_completed = True
            return True
        return False
    
    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        # Vẽ hình ảnh tên lửa tại vị trí trung tâm của ô hiện tại
        surface.blit(self.image, (x + (cell_width - self.image.get_width()) // 2, 
                                  y + (cell_height - self.image.get_height()) // 2))



def draw_rounded_button(button_rect, text, color, font_size,  radius=15):
    # Vẽ nền nút với bo góc
    pygame.draw.rect(screen, color, button_rect, border_radius=radius)
    font = pygame.font.Font("Front/Jomplang-6Y3Jo.ttf", font_size)
    label = font.render(text, True, Colors.WHITE)
    text_rect = label.get_rect(center=button_rect.center)
    screen.blit(label, text_rect)

button_reset = pygame.Rect(screen_width - 220, screen_height - 480, 200, 60)
button_dfs = pygame.Rect(screen_width - 220, screen_height - 400, 200, 60)
button_bfs = pygame.Rect(screen_width - 220, screen_height - 320, 200, 60)
button_A = pygame.Rect(screen_width - 220, screen_height - 240, 200, 60)
button_home = pygame.Rect(screen_width - 220, screen_height - 160, 200, 60)
button_exit = pygame.Rect(screen_width - 220, screen_height - 80, 200, 60)
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
            
            if (0 <= new_row < rows and  #
                0 <= new_col < cols and #
                maze_matrix[new_row][new_col] == 0 and #
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

#font = pygame.font.Font(None, 36)
game_completed = True
sound_played = False  # Biến để kiểm soát việc phát âm thanh
show_image = True

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                if player.move((-1, 1), maze_matrix):  # Down-Left
                    player_step_counter += 1
            elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                if player.move((0, 1), maze_matrix):   # Down
                    player_step_counter += 1
            elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                if player.move((1, 1), maze_matrix):   # Down-Right
                    player_step_counter += 1
            elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                if player.move((-1, 0), maze_matrix):  # Left
                    player_step_counter += 1
            elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                if player.move((1, 0), maze_matrix):   # Right
                    player_step_counter += 1
            elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                if player.move((-1, -1), maze_matrix): # Up-Left
                    player_step_counter += 1
            elif event.key == pygame.K_KP8 or event.key == pygame.K_8:
                if player.move((0, -1), maze_matrix):  # Up
                    player_step_counter += 1
            elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                if player.move((1, -1), maze_matrix):  # Up-Right
                    player_step_counter += 1
            elif event.key == pygame.K_r:  # Nhấn R để restart
                player.reset_position()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_reset.collidepoint(event.pos):
                print("Reset button clicked")
                player.reset_game()
                player_step_counter = 0  # Reset player step counter
                AI_step = 0
            elif button_home.collidepoint(event.pos):
                print("Home button clicked")
                pygame.mixer.music.stop()   
                exec(open("Home.py", encoding="utf-8").read())
            elif button_bfs.collidepoint(event.pos):
                print("BFS button clicked")
                auto_move_path = solve_maze_bfs(maze_matrix, (player.row, player.col), (maze_size - 1, maze_size - 1))
                auto_move_index = 0
            elif button_dfs.collidepoint(event.pos):
                print("DFS button clicked")
                # Thêm mã để chạy thuật toán DFS
            elif button_exit.collidepoint(event.pos):
                print("Exit button clicked")
                pygame.quit()
                sys.exit()  # Thoát khỏi trò chơi
        if event.type == pygame.MOUSEBUTTONDOWN and show_image:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            # Kiểm tra nếu chuột nhấn vào nút đóng
                if close_button.collidepoint(mouse_x, mouse_y):
                    show_image = False  # Ẩn hình ảnh
                    win_sound.stop()
    screen.fill((0, 0, 0))

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

    #Vẽ đích
    goal_x = (maze_size - 1) * cell_width + (cell_width - goal_rect.width) // 2
    goal_y = (maze_size - 1) * cell_height + (cell_height - goal_rect.height) // 2
    screen.blit(goal_image, (goal_x, goal_y))

    # Draw player
    player.draw(screen)
    
    # Draw AI step counter
    ai_step_text = font.render(f"AI Steps: {AI_step}", True, Colors.WHITE)
    screen.blit(ai_step_text, (screen_width - 300, 150))  # Display above player steps

    # Draw player step counter
    step_text = font.render(f"Steps: {player_step_counter}", True, Colors.WHITE)
    screen.blit(step_text, (screen_width - 300, 200))

    draw_rounded_button(button_reset, "Reset", Colors.DARK_BLUE, 36 )
    draw_rounded_button(button_home, "Home",Colors.DARK_BLUE, 36)
    draw_rounded_button(button_bfs, "BFS", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_dfs, "DFS", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_exit, "Exit", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_A, "A*", Colors.DARK_BLUE, 36)
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



    if  game_completed and show_image:
        # Phát âm thanh một lần duy nhất
        if not sound_played:
            win_sound.play()
            sound_played = True
        
        # Hiển thị hình ảnh ở giữa màn hình
        screen.blit(win_image, (screen_width // 2 - win_image.get_width() // 2,
                                screen_height // 2 - win_image.get_height() // 2))

        pygame.draw.rect(screen, (255, 0, 0), close_button)  # Vẽ nút đỏ
        close_text = font.render("X", True, (255, 255, 255))
        screen.blit(close_text, (close_button.x + 5, close_button.y))

        # Hiển thị thông báo "DONE!!!"
        instructions_win = font.render("DONE!!!", True, (255, 255, 255))
        instructions_win_rect = instructions_win.get_rect()
        instructions_win_rect.topleft = (screen_width - 300, 100)
        screen.blit(instructions_win, instructions_win_rect)
       
    # Cập nhật màn hình
    pygame.display.flip()
    pygame.time.delay(30)
