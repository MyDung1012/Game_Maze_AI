import pygame
import sys
from Config import cell_width, cell_height, maze_size


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.original_image = pygame.image.load('Image/rocket.png')
        self.original_image = pygame.transform.scale(self.original_image, (cell_width, cell_height))
        self.image = self.original_image
        self.reset_position()
        self.game_completed = False 
        #self.image = pygame.transform.scale(player_image, (cell_width, cell_height))

    def reset_position(self):
        self.row = 0
        self.col = 0
        self.game_completed = False 
        self.image = self.original_image
    
    def is_at_goal(self):
        return self.row == maze_size - 1 and self.col == maze_size - 1 
    
    def move(self, direction, maze_matrix):
        if self.is_at_goal():
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
            self.row = new_row
            self.col = new_col

            return True
        return False
    
    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        surface.blit(self.image, (x + (cell_width - self.image.get_width()) // 2, 
                                  y + (cell_height - self.image.get_height()) // 2))