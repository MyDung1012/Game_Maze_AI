import pygame
import sys
from Config import screen, screen_width, screen_height, background_image, font
from Player import Player
import json
from UI import create_buttons, draw_rounded_button
from Planets import planets
from Colors import Colors


maze_size = 30
with open(f"Maze/30.txt", 'r') as f:
    maze_matrix = json.load(f)
maze_width = screen_width * 2 // 3
cell_width = maze_width // len(maze_matrix[0])
cell_height = screen_height // len(maze_matrix)

path_image = pygame.image.load("Image/blockk.png")
path_image = pygame.transform.scale(path_image, (cell_width, cell_height))

def __init__(self, matrix):
        self.matrix = matrix

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
        outer_border_color = Colors.PURPLE_2
        inner_border_color = Colors.LIGHT_YELLOW

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
            ((Colors.PURPLE_2), 6),  
            ((Colors.LIGHT_YELLOW), 3)  
        ]

        for i, (color, thickness) in enumerate(layers):
            offset = i * 1 
            pygame.draw.rect(surface, color, (offset, offset, maze_width - 1 * offset, maze_height - 1 * offset), thickness, border_radius=corner_size)

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

goal_image = pygame.image.load("Image/moon.png")
goal_image = pygame.transform.scale(goal_image, (cell_width, cell_height))
goal_rect = goal_image.get_rect()
# Khởi tạo các đối tượng
maze = Maze(maze_matrix)
player = Player(0, 0)  # Vị trí ban đầu của Player
goal_position = (29, 29)  # Đích đến ở góc dưới bên phải

# Hàm vẽ đích đến
def draw_goal(surface, position):
    goal_x = position[1] * cell_width
    goal_y = position[0] * cell_height
    surface.blit(goal_image, (goal_x, goal_y))

buttons = create_buttons(screen_width, screen_height)

# Vòng lặp chính
def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                direction = None
                if event.key == pygame.K_UP:
                    direction = (-1, 0)
                elif event.key == pygame.K_DOWN:
                    direction = (1, 0)
                elif event.key == pygame.K_LEFT:
                    direction = (0, -1)
                elif event.key == pygame.K_RIGHT:
                    direction = (0, 1)

                if direction:
                    player.move(direction, maze_matrix)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["game"].collidepoint(event.pos):
                    print("Game button clicked")
                    exec(open("Game.py", encoding="utf-8").read())
                elif buttons["exit"].collidepoint(event.pos):
                    print("Exit button clicked")
                    pygame.quit()
                    sys.exit()

        # Kiểm tra nếu player đến đích
        if player.row == goal_position[0] and player.col == goal_position[1]:
            print("You reached the goal!")
            running = False

        # Vẽ màn hình
        screen.blit(background_image, (0, 0))

        reward = pygame.Rect(screen_width - 400, 60, 300, 50)
        pygame.draw.rect(screen, Colors.WHITE, reward, 3)  # Vẽ viền
        pygame.draw.rect(screen, Colors.PINK, reward.inflate(-3*2, -3*2)) 

        keys_text = font.render(f"Reward", True, Colors.WHITE)
        keys_text_rect = keys_text.get_rect(center=reward.center)  # Canh giữa văn bản trong textbox
        screen.blit(keys_text, keys_text_rect)

        draw_rounded_button(buttons["exit"], "Exit", Colors.DARK_BLUE, 36)
        draw_rounded_button(buttons["game"], "GAME", Colors.DARK_BLUE, 36)
        draw_rounded_button(buttons["start"], "START", Colors.DARK_BLUE, 36)
        draw_rounded_button(buttons["stop"], "STOP", Colors.DARK_BLUE, 36)
        for planet in planets:
            planet.update()
            planet.draw(screen)
        maze.draw(screen)
        draw_goal(screen, goal_position)
        player.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
