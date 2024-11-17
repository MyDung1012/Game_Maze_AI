
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

# Tải hình ảnh kết quả
win_imagee = pygame.image.load("Image/win.jpg")
lose_image = pygame.image.load("Image/lose.jpg")

# Điều chỉnh kích thước hình ảnh nếu cần
win_image = pygame.transform.scale(win_imagee, (600, 450))
lose_image = pygame.transform.scale(lose_image, (600, 450))


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
        #player.reset_position()

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

def solve_backtracking(maze, start, goal):
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
    
    def heuristic(cell):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    # Lưu vị trí đã ghé qua để tránh lặp lại
    visited = set()
    # Cache để lưu lại các đường cụt
    failed_paths = set()

    path = []

    def backtrack(current):
        # Nếu đã đến đích, trả về True
        if current == goal:
            return True

        # Đánh dấu vị trí đã thăm
        visited.add(current)

        # Sắp xếp các hướng đi theo khoảng cách tới đích
        sorted_directions = sorted(directions, key=lambda d: heuristic((current[0] + d[0], current[1] + d[1])))

        for direction in sorted_directions:
            next_cell = (current[0] + direction[0], current[1] + direction[1])

            # Kiểm tra tính hợp lệ của ô tiếp theo
            if (0 <= next_cell[0] < len(maze) and 0 <= next_cell[1] < len(maze[0]) and
                    maze[next_cell[0]][next_cell[1]] == 0 and next_cell not in visited):

                # Thêm bước đi vào đường đi
                path.append(direction)
                
                # Nếu tìm được đường đi đến đích, kết thúc
                if backtrack(next_cell):
                    return True

                # Quay lui nếu không tìm được đường đi
                path.pop()

        # Đánh dấu đường cụt để tránh đi lại lần nữa
        visited.remove(current)
        failed_paths.add(current)
        return False

    # Chạy backtracking từ điểm bắt đầu
    if backtrack(start):
        return path  # Trả về danh sách các bước di chuyển
    else:
        return None  # Không tìm thấy đường đi
