import pygame
import random
import sys
from Colors import Colors

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
screen_width, screen_height = 800, 600
maze_width = screen_width * 2 // 3  # Mê cung chiếm 2/3 màn hình bên trái
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Background with Floating Planets and Maze")

#âm thanh 
background_sound = pygame.mixer.Sound('Sound/game1.wav')
# Ma trận 
maze_matrix = [
    [1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,1,1,0,0,0,0,1,1,1,1,1,1,1],
    [1,0,1,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1],
    [1,0,1,0,1,1,0,0,0,1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,1,1,1],
    [1,0,0,1,1,0,0,0,0,1,1,0,0,0,1,1,0,1,1,1,1,1,1,1,0,0,0,0,1,1],
    [1,0,0,1,1,0,0,0,0,1,1,0,1,1,1,1,0,1,1,0,0,1,1,1,1,1,0,0,1,1],
    [1,0,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1,1,0,0,1,1,1,1,1,0,0,1,1],
    [1,0,0,1,1,0,1,1,1,1,1,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1],
    [1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,0,1],
    [1,0,0,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,1,1,0,1],
    [1,0,0,1,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0,1],
    [1,0,0,1,1,0,0,1,0,0,1,1,0,0,1,1,0,0,1,0,0,1,1,0,0,1,1,1,1,1],
    [1,0,0,1,1,1,1,1,0,0,1,1,0,0,1,1,0,0,1,0,0,1,1,0,0,1,1,1,1,1],
    [1,0,0,1,1,1,1,1,0,0,1,1,0,0,1,1,0,0,1,0,0,1,1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1]
]

# Kích thước của từng ô trong mê cung
cell_width = maze_width // len(maze_matrix[0])  # Tính kích thước ô dựa trên chiều rộng mê cung
cell_height = screen_height // len(maze_matrix)

# Tải hình nền không gian
try:
    background_image = pygame.image.load('Image/ground.jpg')
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

# Hàm vẽ nút
def draw_button(surface, text, x, y, width, height, color, font_size):
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=15)
    font = pygame.font.SysFont("Front/04054_BeamRider3D (1).ttf", font_size)
    label = font.render(text, True, Colors.BLACK)
    text_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(label, text_rect)

# Tạo danh sách hành tinh
planets = [Planet(planet_images[i], random.randint(0, screen_width), random.randint(0, screen_height - 50)) for i in range(3)]

# Khởi tạo mê cung
maze = Maze(maze_matrix)

# Kích thước và vị trí của các nút
button_width, button_height = 120, 40
button_y_start = screen_height - button_height - 20  # Vị trí y cho nút
button_spacing = 10  # Khoảng cách giữa các nút
buttons = [
    ("Thuật toán", button_y_start),
    ("Thuật toán", button_y_start + button_height + button_spacing),
    ("Restart", button_y_start + 2 * (button_height + button_spacing)),
    ("Stop", button_y_start + 3 * (button_height + button_spacing)),
    ("Continue", button_y_start + 4 * (button_height + button_spacing)),
    ("Exit", button_y_start + 5 * (button_height + button_spacing)),
]

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    background_sound.play()
    # Vẽ nền không gian
    screen.blit(background_image, (0, 0))

    for planet in planets:
        planet.update()
        planet.draw(screen)

    # Vẽ mê cung
    maze.draw(screen)

    # Vẽ các nút
    for i, (text, y) in enumerate(buttons):
       # draw_button(screen, screen_width - button_width - 20, y, button_width, button_height, text)
        draw_button(screen, "DFS", screen_width - 170, 250, 150, 30, Colors.PURPLE, 24)
        draw_button(screen, "BFS", screen_width - 170, 300, 150, 30, Colors.PURPLE, 24)
        draw_button(screen, "RESTART", screen_width - 170, 350, 150, 30, Colors.DARK_BLUE, 24)
        draw_button(screen, "STOP", screen_width - 170, 400, 150, 30, Colors.DARK_BLUE, 24)
        draw_button(screen, "CONTINUTE", screen_width - 170, 450, 150, 30, Colors.DARK_BLUE, 24)
        draw_button(screen, "EXIT", screen_width - 170, 500, 150, 30, Colors.YELLOW, 24)

    # Cập nhật màn hình
    pygame.display.flip()
    pygame.time.delay(30)
