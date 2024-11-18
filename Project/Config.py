import pygame
import json
import sys

# Khởi tạo Pygame và màn hình
pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

font = pygame.font.Font(None, 36)
# Chiều rộng mê cung
maze_width = screen_width * 2 // 3

# Âm thanh nền
pygame.mixer.init()
pygame.mixer.music.load('Sound/8bit.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

# Giới hạn độ sâu ban đầu
initial_depth_limits = [18, 38, 58, 94, 106, 136, 164, 222, 178, 260]
try:
    with open('difficulty.txt', 'r') as f:
        maze_size = int(f.read().strip())
        if maze_size in range(10, 101, 10):  # Bội số của 10 từ 10 đến 100
            index = maze_size // 10 - 1
            initial_depth_limit = initial_depth_limits[index]
        else:
            initial_depth_limit = 100  # Giá trị mặc định
except (FileNotFoundError, ValueError) as e:
    print(f"Error reading difficulty: {e}")
    initial_depth_limit = 100  # Giá trị mặc định nếu gặp lỗi

# Tải hình ảnh và âm thanh
try:
    win_image = pygame.image.load("Image/Done.jpg")
    win_image = pygame.transform.scale(win_image, (600, 450))
    win_sound = pygame.mixer.Sound("Sound/happy.mp3")

    close_button = pygame.Rect(screen_width // 2 + win_image.get_width() // 2 - 30,
                               screen_height // 2 - win_image.get_height() // 2, 30, 30)

    win_imagee = pygame.image.load("Image/win.jpg")
    lose_image = pygame.image.load("Image/lose.jpg")
    win_image = pygame.transform.scale(win_imagee, (600, 450))
    lose_image = pygame.transform.scale(lose_image, (600, 450))
except pygame.error as e:
    print(f"Error loading images or sounds: {e}")
    sys.exit()

# Tải mê cung
try:
    with open(f"Maze/{maze_size}.txt", "r") as f:
        maze_matrix = json.load(f)
except (FileNotFoundError, SyntaxError) as e:
    print(f"Error loading maze file: {e}")
    sys.exit()

# Tính toán kích thước ô
cell_width = maze_width // len(maze_matrix[0])
cell_height = screen_height // len(maze_matrix)

# Tải các hình ảnh
try:
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
except pygame.error as e:
    print(f"Error loading additional images: {e}")
    sys.exit()
