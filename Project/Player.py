import pygame
import sys

class Player:
    def __init__(self, x, y, cell_width, cell_height, image_path, maze_size):
        self.x = x
        self.y = y
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.maze_size = maze_size
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image
        self.game_completed = False

        try:
            self.original_image = pygame.transform.scale(self.original_image, (cell_width, cell_height))
            self.image = self.original_image
        except pygame.error as e:
            print(f"Error loading rocket image: {e}")
            sys.exit()

        self.reset_position()

    def reset_position(self):
        self.row = 0
        self.col = 0
        self.game_completed = False
        self.image = self.original_image

    def is_at_goal(self):
        return self.row == self.maze_size - 1 and self.col == self.maze_size - 1

    def reset_game(self):
        global game_completed, sound_played, show_image, player_step_counter
        game_completed = False
        sound_played = False
        show_image = True
        player_step_counter = 0
        self.reset_position()

    def move(self, direction, maze_matrix):
        if self.game_completed:
            return False

        new_row = self.row + direction[0]
        new_col = self.col + direction[1]

        if (0 <= new_row < len(maze_matrix) and 
            0 <= new_col < len(maze_matrix[0]) and 
            maze_matrix[new_row][new_col] == 0):

            # Cập nhật hình ảnh dựa trên hướng di chuyển
            direction_angle = {
                (-1, 0): 0,    # lên
                (1, 0): 180,   # xuống
                (0, -1): 90,   # trái
                (0, 1): -90,   # phải
                (-1, -1): 45,  # xéo trái lên
                (1, -1): 135,  # xéo trái xuống
                (-1, 1): -45,  # xéo phải lên
                (1, 1): -135   # xéo phải xuống
            }
            if direction in direction_angle:
                self.image = pygame.transform.rotate(self.original_image, direction_angle[direction])

            self.row = new_row
            self.col = new_col

            if self.is_at_goal():
                self.game_completed = True
            return True
        return False

    def draw(self, surface):
        x = self.col * self.cell_width
        y = self.row * self.cell_height
        surface.blit(self.image, (x + (self.cell_width - self.image.get_width()) // 2, 
                                  y + (self.cell_height - self.image.get_height()) // 2))
