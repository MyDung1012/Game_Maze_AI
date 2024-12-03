import pygame
import json
import sys

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