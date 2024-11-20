import pygame 
from Config import cell_width, cell_height
from AI import solve_maze_bfs, solve_maze_astar

class Boat:
    def __init__(self, x, y):
        self.row = x
        self.col = y
        self.image = pygame.image.load('Image/ufo.png')
        self.image = pygame.transform.scale(self.image, (cell_width, cell_height))
        self.path = None
        self.path_index = 0
        self.algorithm_selected = None
        self.last_move_time = 0
        self.move_delay = 1000

    def update_path(self, maze, target, algorithm):
        '''if algorithm == "AC3+Backtracking":
            print(f"Running AC3+Backtracking for boat at ({self.row}, {self.col})")
            maze_csp = build_csp_from_maze(maze, (self.row, self.col), target)
            if AC3(maze_csp):
                self.path = backtracking_search(maze_csp)
                if self.path is None:
                    print("Backtracking did not find a solution.")
                else:
                    print(f"Path found by Backtracking: {self.path}")
            else:
                self.path = None
                print("AC3 failed to simplify the CSP.")'''
        if algorithm == "BFS":
            print(f"Running BFS for boat at ({self.row}, {self.col})")
            self.path = solve_maze_bfs(maze, (self.row, self.col), target) or []
        elif algorithm == "A*":
            print(f"Running A* for boat at ({self.row}, {self.col})")
            self.path = solve_maze_astar(maze, (self.row, self.col), target) or []
        else:
            self.path = []  # Không tìm thấy đường đi

        self.path_index = 0
        if not self.path:
            print(f"No path found using {algorithm}. Boat remains at ({self.row}, {self.col}).")


    def move(self, maze):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_delay:
            if not self.path:
                print("Boat has no path.")
                return  # Không có đường đi
            if self.path_index < len(self.path):
                direction = self.path[self.path_index]
                next_row = self.row + direction[0]
                next_col = self.col + direction[1]
                if maze[next_row][next_col] == 0:
                    self.row = next_row
                    self.col = next_col
                    self.path_index += 1
                print(f"Boat moved to ({self.row}, {self.col})")
            else:
                print("Boat reached the end of its path.")
            self.last_move_time = current_time

    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        surface.blit(self.image, (x, y))