import pygame 
from Config import cell_width, cell_height
from AI import solve_maze_bfs, solve_maze_astar, backtrack_with_ac3, simulated_annealing_path

def path_to_directions(path):
    """Chuyển đổi đường đi từ tọa độ tuyệt đối sang hướng di chuyển tương đối."""
    directions = []
    for i in range(1, len(path)):
        dx = path[i][0] - path[i - 1][0]
        dy = path[i][1] - path[i - 1][1]
        directions.append((dx, dy))
    return directions

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
        self.move_delay = 150

    def update_path(self, maze, target, algorithm):
        if algorithm == "BFS":
            print(f"Running BFS for boat at ({self.row}, {self.col})")
            self.path = solve_maze_bfs(maze, (self.row, self.col), target) or []
        elif algorithm == "A*":
            print(f"Running A* for boat at ({self.row}, {self.col})")
            self.path = solve_maze_astar(maze, (self.row, self.col), target) or []
        elif algorithm == "AC3+Backtracking":
            print(f"Running AC3+Backtracking for boat at ({self.row}, {self.col})")
            absolute_path = backtrack_with_ac3(maze, (self.row, self.col), target)
            if absolute_path:
                self.path = path_to_directions(absolute_path)  # Chuyển sang hướng tương đối
                print(f"Converted path: {self.path}")
            else:
                self.path = []
                print("Backtracking returned no path.")
        elif algorithm == "Simulated Annealing":
            print(f"Running Simulated Annealing for boat at ({self.row}, {self.col})")
            self.path = simulated_annealing_path(
                maze, (self.row, self.col), target, max_iterations=1000, initial_temp=100, cooling_rate=0.99
            )
            if self.path is None:
                self.path = []
                print("Simulated Annealing did not find a path.")
            else:
                print(f"Path found by Simulated Annealing: {self.path}")

        else:
            self.path = []  # Không tìm thấy đường đi
        '''elif algorithm == "Simulated Annealing":
            print(f"Running Simulated Annealing for boat at ({self.row}, {self.col})")

            distance = abs(self.row - target[0]) + abs(self.col - target[1])
            threshold = 20  # Adjust threshold based on maze size

            if distance <= threshold:
                search_radius = 10
                region = [(r, c) for r in range(max(0, target[0] - search_radius), 
                                                min(len(maze), target[0] + search_radius + 1))
                                for c in range(max(0, target[1] - search_radius), 
                                                min(len(maze[0]), target[1] + search_radius + 1))]
            else:
                region = None  # Search globally for distant targets

            self.path = simulated_annealing_path(
                maze, (self.row, self.col), target, 
                max_iterations=5000, initial_temp=5000, cooling_rate=0.999, region=region
            )

            if self.path:
                print(f"Path found by Simulated Annealing: {self.path}")
            else:
                print("Simulated Annealing returned no path.")'''



        
        #else:
         #   self.path = []  # Không tìm thấy đường đi

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
                if 0 <= next_row < len(maze) and 0 <= next_col < len(maze[0]) and maze[next_row][next_col] == 0:
                    self.row = next_row
                    self.col = next_col
                    self.path_index += 1
            
                print(f"Boat moved to ({self.row}, {self.col})")
            else:
                print("Boat reached the end of its path.")
            self.last_move_time = current_time
        print(len(self.path))
    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        surface.blit(self.image, (x, y))