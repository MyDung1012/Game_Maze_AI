import pygame
import random
import sys
from Colors import Colors
from enum import Enum
import json
from collections import deque  # For BFS
import heapq  # Use heapq for priority queue

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
win_sound = pygame.mixer.Sound("Sound/happy.mp3")
close_button = pygame.Rect(screen_width // 2 + win_image.get_width() // 2 - 30,
                                   screen_height // 2 - win_image.get_height() // 2, 30, 30)

# Load maze matrix
try:
    with open(f"Maze/{maze_size}.txt", "r") as f:
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
            
        new_row = self.row + direction[0]
        new_col = self.col + direction[1]
        
        # Kiểm tra tọa độ mới có hợp lệ và là đường đi hay không
        if (0 <= new_row < len(maze_matrix) and 
            0 <= new_col < len(maze_matrix[0]) and 
            maze_matrix[new_row][new_col] == 0):
            
            # Xác định góc xoay dựa trên hướng di chuyển
            if direction == (-1, 0):  # lên
                self.image = pygame.transform.rotate(self.original_image, 0)
            elif direction == (1, 0):  # xuống
                self.image = pygame.transform.rotate(self.original_image, 180)
            elif direction == (0, -1):  # trái
                self.image = pygame.transform.rotate(self.original_image, 90)
            elif direction == (0, 1):  # Phải
                self.image = pygame.transform.rotate(self.original_image, -90)
            elif direction == (-1, -1):# xéo trái lên
                self.image = pygame.transform.rotate(self.original_image, 45)
            elif direction == (1, -1):# xéo trái xuống
                self.image = pygame.transform.rotate(self.original_image, 135)
            elif direction == (-1, 1):# xéo phải lên
                self.image = pygame.transform.rotate(self.original_image, -45)
            elif direction == (1, 1): # xéo phải xuống
                self.image = pygame.transform.rotate(self.original_image, -135)
                
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

def solve_maze_bfs(maze, start, goal):
    # 8 hướng di chuyển: trên, dưới, trái, phải, và 4 hướng chéo
    directions = [
        (-1, 0),  # lên
        (1, 0),   # xuống
        (0, -1),  # trái
        (0, 1),   # phải
        (-1, -1), # trên-trái
        (-1, 1),  # trên-phải
        (1, -1),  # dưới-trái
        (1, 1)    # dưới-phải
    ]
    
    rows = len(maze)
    cols = len(maze[0])
    
    # Khởi tạo queue và visited set
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
    directions = [
        (-1, 0),  # lên
        (1, 0),   # xuống
        (0, -1),  # trái
        (0, 1),   # phải
        (-1, -1), # trên-trái
        (-1, 1),  # trên-phải
        (1, -1),  # dưới-trái
        (1, 1)    # dưới-phải
    ]
    
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
    # 8 hướng di chuyển: trên, dưới, trái, phải, và 4 hướng chéo
    directions = [
        (-1, 0),  # lên
        (1, 0),   # xuống
        (0, -1),  # trái
        (0, 1),   # phải
        (-1, -1), # trên-trái
        (-1, 1),  # trên-phải
        (1, -1),  # dưới-trái
        (1, 1)    # dưới-phải
    ]
    
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
            
            # Kiểm tra điều kiện hợp lệ
            if (neighbor[0] < 0 or neighbor[0] >= rows or 
                neighbor[1] < 0 or neighbor[1] >= cols or
                maze[neighbor[0]][neighbor[1]] == 1 or  # 0 là tường
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

def draw_rounded_button(button_rect, text, color, font_size,  radius=15):
    # Vẽ nền nút với bo góc
    pygame.draw.rect(screen, color, button_rect, border_radius=radius)
    font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", font_size)
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

# Initialize auto_move_path, auto_move_index, and AI_step
auto_move_path = None
auto_move_index = 0
AI_step = 0  # Initialize AI_step to count DFS steps
auto_move_delay = 100   # Delay in milliseconds between automatic steps
last_move_time = pygame.time.get_ticks()  # Track the last move time

# Initialize font
font = pygame.font.Font(None, 36)  # Add this line to initialize the font

# Initialize player_step_counter
player_step_counter = 0  # Separate counter for player's manual steps

#font = pygame.font.Font(None, 36)
game_completed = True
sound_played = False  # Biến để kiểm soát việc phát âm thanh
show_image = True
def thongbao(outcome_text):
    instructions_win = font.render(outcome_text, True, Colors.WHITE)
    instructions_win_rect = instructions_win.get_rect()
    instructions_win_rect.topleft = (screen_width - 300, 100)
    screen.blit(instructions_win, instructions_win_rect)
# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                if player.move((1,-1), maze_matrix):  # Down-Left
                    player_step_counter += 1
            elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                if player.move((1, 0), maze_matrix):   # Down
                    player_step_counter += 1
            elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                if player.move((1, 1), maze_matrix):   # Down-Right
                    player_step_counter += 1
            elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                if player.move((0, -1), maze_matrix):  # Left
                    player_step_counter += 1
            elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                if player.move((0, 1), maze_matrix):   # Right
                    player_step_counter += 1
            elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                if player.move((-1,-1), maze_matrix): # Up-Left
                    player_step_counter += 1
            elif event.key == pygame.K_KP8 or event.key == pygame.K_8:
                if player.move((-1, 0), maze_matrix):  # Up
                    player_step_counter += 1
            elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                if player.move((-1,1), maze_matrix):  # Up-Right
                    player_step_counter += 1
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
                player.reset_position()
                AI_step = 0
                auto_move_path = solve_maze_bfs(maze_matrix, (player.row, player.col), (maze_size - 1, maze_size - 1))
                auto_move_index = 0
            elif button_A.collidepoint(event.pos):
                print("A* button clicked")
                player.reset_position()
                AI_step = 0
                auto_move_path = solve_maze_astar(maze_matrix, (player.row, player.col), (maze_size - 1, maze_size - 1))
                auto_move_index = 0
            elif button_dfs.collidepoint(event.pos):
                player.reset_position()
                AI_step = 0
                auto_move_path = solve_maze_dfs(maze_matrix, (player.row, player.col), (maze_size - 1, maze_size - 1))
                auto_move_index = 0
                print("DFS button clicked")
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


    # Check if it's time to move to the next step
    if auto_move_path and auto_move_index < len(auto_move_path):
        direction = auto_move_path[auto_move_index]
        player.move(direction, maze_matrix)
        auto_move_index += 1  # Move to the next step
        AI_step += 1  # Increment AI_step for each move
        pygame.time.delay(100)  # Delay of 0.1 seconds (100 milliseconds)

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
    
    if AI_step > 0 and player_step_counter > 0:
        if AI_step - (maze_size * 0.2) < player_step_counter:
            outcome_text = "YOU WIN!!!"
        elif AI_step - (maze_size * 0.2) > player_step_counter:
            outcome_text = "YOU LOSE!!!"
        else:
            outcome_text = "DRAW!!!"
    elif AI_step == 0 and player_step_counter > 0:
        outcome_text = "CHOOSE AI ALGORITHM"
    elif AI_step == 0 and player_step_counter == 0:
        outcome_text = "IT'S YOUR TURN"
    thongbao(outcome_text)

    if game_completed and show_image:
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

       
    # Cập nhật màn hình
    pygame.display.flip()
    pygame.time.delay(30)
