import pygame
import random
import sys
import json
from Colors import Colors
from enum import Enum
from collections import deque
import heapq  # For priority queue

# Initialize pygame
pygame.init()

# Screen setup
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Constants for file paths
BACKGROUND_IMAGE = 'Image/ground.jpg'
WIN_IMAGE = 'Image/win.jpg'
LOSE_IMAGE = 'Image/lose.jpg'
ROCKET_IMAGE = 'Image/rocket.png'
PLANET_IMAGES = ['Image/planet1.png', 'Image/planet2.png', 'Image/planet3.png']
SOUND_PATH = 'Sound/8bit.mp3'

# Utility functions for loading assets
def load_image(path, size=None):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size) if size else image

def load_sound(path, volume=0.3):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    return sound

# Load assets
background_image = load_image(BACKGROUND_IMAGE, (screen_width, screen_height))
win_image = load_image(WIN_IMAGE, (600, 450))
lose_image = load_image(LOSE_IMAGE, (600, 450))
win_sound = load_sound(SOUND_PATH)

# Maze and Player classes
class Maze:
    def __init__(self, matrix):
        self.matrix = matrix
        self.cell_width = screen_width // len(matrix[0])
        self.cell_height = screen_height // len(matrix)

    def draw(self, surface):
        for row, line in enumerate(self.matrix):
            for col, cell in enumerate(line):
                x, y = col * self.cell_width, row * self.cell_height
                pygame.draw.rect(surface, Colors.YELLOW if cell else Colors.PATH, pygame.Rect(x, y, self.cell_width, self.cell_height))

class Player:
    def __init__(self, x, y):
        self.image = load_image(ROCKET_IMAGE, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.steps = 0

    def move(self, direction, maze_matrix):
        dx, dy = direction
        new_rect = self.rect.move(dx * 50, dy * 50)
        # Implement collision check here
        self.rect = new_rect

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Game loop
maze_matrix = [[0]*10 for _ in range(10)]  # Example matrix, replace with actual maze
player = Player(50, 50)  # Starting position example

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                # Define moves here for each key direction
                pass

    screen.blit(background_image, (0, 0))
    player.draw(screen)
    pygame.display.flip()
