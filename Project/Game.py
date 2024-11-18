import pygame
import random
import sys
from Colors import Colors
from enum import Enum
import json
from collections import deque 
import heapq  

pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

maze_width = screen_width * 2 // 3

# Âm thanh nền
pygame.mixer.music.load('Sound/8bit.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

initial_depth_limits = [18, 38, 58, 94, 106, 136, 164, 222, 178, 260]
try:
    with open('difficulty.txt', 'r') as f:
        maze_size = int(f.read().strip())
        # Kiểm tra maze_size nằm trong khoảng 10, 20, ..., 100
        if maze_size in range(10, 101, 10):  # Kiểm tra xem maze_size có phải bội số của 10 từ 10 đến 100
            index = maze_size // 10 - 1  # Tính chỉ số tương ứng
            initial_depth_limit = initial_depth_limits[index]
        else:
            initial_depth_limit = 100  # Giá trị mặc định nếu maze_size ngoài phạm vi
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


try:
    with open(f"Maze/{maze_size}.txt", "r") as f:
        maze_matrix = json.load(f)
except (FileNotFoundError, SyntaxError) as e:
    print(f"Error loading maze file: {e}")
    sys.exit()

cell_width = maze_width // len(maze_matrix[0])
cell_height = screen_height // len(maze_matrix) 

try:
    background_image = pygame.image.load('Image/bgbg.jpg')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    sys.exit()

try:
    path_image = pygame.image.load('Image/blockk.png') 
    path_image = pygame.transform.scale(path_image, (cell_width, cell_height))
except pygame.error as e:
    print(f"Error loading path image: {e}")
    sys.exit()

goal_image = pygame.image.load('Image/moon.png')
goal_image = pygame.transform.scale(goal_image, (cell_width, cell_height))
goal_rect = goal_image.get_rect()
try:
    planet_images = [
        pygame.image.load('Image/planet1.png'), 
        pygame.image.load('Image/planet2.png'), 
        pygame.image.load('Image/planet3.png')  
    ]
except pygame.error as e:
    print(f"Error loading planet images: {e}")
    sys.exit()

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
        global game_completed, sound_played, show_image, player_step_counter
        game_completed = False
        sound_played = False
        show_image = True
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
            elif direction == (-1, -1):# xéo trái lên
                self.image = pygame.transform.rotate(self.original_image, 45)
            elif direction == (1, -1):# xéo trái xuống
                self.image = pygame.transform.rotate(self.original_image, 135)
            elif direction == (-1, 1):# xéo phải lên
                self.image = pygame.transform.rotate(self.original_image, -45)
            elif direction == (1, 1): # xéo phải xuống
                self.image = pygame.transform.rotate(self.original_image, -135)
                
            self.row = new_row
            self.col = new_col

            if self.is_at_goal():
                self.game_completed = True
            return True
        return False
    
    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        surface.blit(self.image, (x + (cell_width - self.image.get_width()) // 2, 
                                  y + (cell_height - self.image.get_height()) // 2))

def solve_maze_bfs(maze, start, goal):
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


def solve_backtracking(maze, start, goal, initial_depth_limit):
    # Directions for movement
    directions = [
        (-1, 0),  # up
        (1, 0),   # down
        (0, -1),  # left
        (0, 1),   # right
        #(-1, -1), # up-left
        #(-1, 1),  # up-right
        #(1, -1),  # down-left
        #(1, 1)    # down-right
    ]
    
    # Initialize depth limits and constraints for recursion
    depth_limit = initial_depth_limit
    max_depth_limit = 1000
    max_backtracks = 10000
    stepIDS = 50

    # Heuristic function to estimate distance to the goal
    def heuristic(cell):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    path = []  # To store the current path

    # Simplified AC-3 for debugging
    def ac3_constraints(current):
        # Just return True for debugging to bypass constraints
        return True

    # Main backtracking function with depth and backtrack limits
    def backtrack(current, depth, visited, backtracks):
        # Debug: Print current position and depth
        print(f"Visiting {current}, depth {depth}, backtracks {backtracks}")

        # Check if we've exceeded the depth or backtrack limits
        if depth > depth_limit or backtracks >= max_backtracks:
            print(f"Depth or backtrack limit reached at {current}")
            return False

        # Check if we reached the goal
        if current == goal:
            print("Goal reached!")
            return True

        visited.add(current)
        
        # Sort directions based on distance to goal
        sorted_directions = sorted(directions, key=lambda d: heuristic((current[0] + d[0], current[1] + d[1])))

        for direction in sorted_directions:
            next_cell = (current[0] + direction[0], current[1] + direction[1])

            # Check validity of the next cell
            if (0 <= next_cell[0] < len(maze) and 
                0 <= next_cell[1] < len(maze[0]) and 
                maze[next_cell[0]][next_cell[1]] == 0 and 
                next_cell not in visited):

                # Apply simplified AC-3 constraint for debugging
                if ac3_constraints(next_cell):
                    path.append(direction)
                    
                    # Recur with updated depth and backtrack count
                    if backtrack(next_cell, depth + 1, visited, backtracks):
                        return True

                    # Backtrack if the current path doesn't lead to a solution
                    path.pop()
                    backtracks += 1  # Increase backtrack count after unsuccessful attempt

        visited.remove(current)  # Clean up visited for this path
        return False

    # Iteratively increase depth limit if no solution found
    while depth_limit <= max_depth_limit:
        print(f"Trying depth limit {depth_limit}")
        visited = set()  # Reset visited set for each new depth limit attempt
        if backtrack(start, 0, visited, 0):
            print("Path found!")
            return path  # Return the successful path
        else:
            print("No path found, increasing depth limit")
            depth_limit += stepIDS  # Increment depth limit for iterative deepening

    print("No solution found within depth and backtrack limits.")
    return None  # Return None if no path is found



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
def thongbao(outcome_text):
    instructions_win = font.render(outcome_text, True, Colors.WHITE)
    instructions_win_rect = instructions_win.get_rect()
    instructions_win_rect.topleft = (screen_width - 300, 250)
    screen.blit(instructions_win, instructions_win_rect)

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
ai_completed = False


  # Thời gian bắt đầu hiển thị thông báo\



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
            elif button_backtracking.collidepoint(event.pos):
                player.reset_position()
                AI_step = 0
                auto_move_path = solve_backtracking(maze_matrix, (player.row, player.col), (maze_size - 1, maze_size - 1), initial_depth_limit )
                auto_move_index = 0
                print("Backtracking with AC3 button clicked")
            elif button_exit.collidepoint(event.pos):
                print("Exit button clicked")
                pygame.quit()
                sys.exit()  # Thoát khỏi trò chơi
            
        if event.type == pygame.MOUSEBUTTONDOWN: #and show_image:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            # Kiểm tra nếu chuột nhấn vào nút đóng
                if close_button.collidepoint(mouse_x, mouse_y):
                    show_image = False  # Ẩn hình ảnh
                    win_sound.stop()

    screen.fill((0, 0, 0))

    show_outcome = False  # Biến điều kiện để hiển thị thông báo
    outcome_time = 0
    # Check if it's time to move to the next step
    if auto_move_path and auto_move_index < len(auto_move_path):
        direction = auto_move_path[auto_move_index]
        player.move(direction, maze_matrix)
        auto_move_index += 1  # Move to the next step
        AI_step += 1  # Increment AI_step for each move
        pygame.time.delay(100)  # Delay of 0.1 seconds (100 milliseconds)

        if auto_move_index >= len(auto_move_path):
            ai_completed = True 
            auto_move_path = None


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
    # Định nghĩa kích thước và màu sắc của textbox
    textbox_width = 300
    textbox_height = 50
    textbox_color = Colors.PINK  # Màu nền của textbox
    border_color = Colors.WHITE  # Màu viền của textbox
    border_thickness = 3  # Độ dày của viền

    # Textbox cho số bước của AI
    ai_textbox_rect = pygame.Rect(screen_width - 400, 60, textbox_width, textbox_height)
    pygame.draw.rect(screen, border_color, ai_textbox_rect, border_thickness)  # Vẽ viền
    pygame.draw.rect(screen, textbox_color, ai_textbox_rect.inflate(-border_thickness*2, -border_thickness*2))  # Vẽ nền

    # Hiển thị số bước của AI
    ai_step_text = font.render(f"AI Steps: {AI_step}", True, Colors.WHITE)
    ai_text_rect = ai_step_text.get_rect(center=ai_textbox_rect.center)  # Canh giữa văn bản trong textbox
    screen.blit(ai_step_text, ai_text_rect)

    # Textbox cho số bước của người chơi
    player_textbox_rect = pygame.Rect(screen_width - 400, 140, textbox_width, textbox_height)
    pygame.draw.rect(screen, border_color, player_textbox_rect, border_thickness)  # Vẽ viền
    pygame.draw.rect(screen, textbox_color, player_textbox_rect.inflate(-border_thickness*2, -border_thickness*2))  # Vẽ nền

    # Hiển thị số bước của người chơi
    step_text = font.render(f"Steps: {player_step_counter}", True, Colors.WHITE)
    step_text_rect = step_text.get_rect(center=player_textbox_rect.center)  # Canh giữa văn bản trong textbox
    screen.blit(step_text, step_text_rect)


    draw_rounded_button(button_reset, "Reset", Colors.DARK_BLUE, 36 )
    draw_rounded_button(button_home, "Home",Colors.DARK_BLUE, 36)
    draw_rounded_button(button_bfs, "BFS", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_dfs, "DFS", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_exit, "Exit", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_A, "A*", Colors.DARK_BLUE, 36)
    draw_rounded_button(button_backtracking, "Backtracking", Colors.DARK_BLUE, 36)

    # Hiển thị thông báo hoàn thành
    font = pygame.font.Font(None, 36)
    game_completed = False
    
    if player.is_at_goal():
        game_completed = True
    
    # Hiển thị hướng dẫn
    
    if ai_completed and player_step_counter > 0:
        if AI_step + (maze_size * 0.2) > player_step_counter:
            outcome_text = "YOU WIN!!!"
        elif AI_step + (maze_size * 0.2) < player_step_counter:
            outcome_text = "YOU LOSE!!!"
        else:
            outcome_text = "DRAW!!!"

        if outcome_text == "YOU WIN!!!" and show_image:
            screen.blit(win_imagee, (screen_width // 2 - win_image.get_width() // 2,
                                    screen_height // 2 - win_image.get_height() // 2))
            pygame.draw.rect(screen, (255, 0, 0), close_button)  # Vẽ nút đỏ
            close_text = font.render("X", True, (255, 255, 255))
            screen.blit(close_text, (close_button.x + 5, close_button.y))
        elif outcome_text == "YOU LOSE!!!" and show_image:
                screen.blit(lose_image, (screen_width // 2 - lose_image.get_width() // 2,
                                        screen_height // 2 - lose_image.get_height() // 2))
                pygame.draw.rect(screen, (255, 0, 0), close_button)  # Vẽ nút đỏ
                close_text = font.render("X", True, (255, 255, 255))
                screen.blit(close_text, (close_button.x + 5, close_button.y))

    elif AI_step == 0 and player_step_counter > 0:
        outcome_text = "CHOOSE AI ALGORITHM"
    elif AI_step == 0 and player_step_counter == 0:
        outcome_text = "IT'S YOUR TURN"
    thongbao(outcome_text)

       
    # Cập nhật màn hình
    pygame.display.flip()
    pygame.time.delay(30)