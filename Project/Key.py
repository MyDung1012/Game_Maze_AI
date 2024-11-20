import pygame
import random
from Config import maze_size, cell_width, cell_height
class Key:
    def __init__(self, x, y, image):
        self.row = x
        self.col = y
        self.image = pygame.transform.scale(image, (cell_width, cell_height))
        self.collected = False  # Trạng thái đã được thu thập hay chưa

    def draw(self, surface):
        if not self.collected:
            x = self.col * cell_width
            y = self.row * cell_height
            surface.blit(self.image, (x, y))

# Hàm random key
def generate_random_keys(maze_matrix, num_keys, key_image):
    keys = []
    rows = len(maze_matrix)
    cols = len(maze_matrix[0])

    while len(keys) < num_keys:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        if maze_matrix[row][col] == 0 and (row, col) != (0, 0) and (row, col) != (maze_size - 1, maze_size - 1):
            keys.append(Key(row, col, key_image))
    return keys