import pygame
from Config import cell_width, cell_height, path_image, maze_matrix

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


