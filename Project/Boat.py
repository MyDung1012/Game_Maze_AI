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
        self.step_count = 0
        self.start_position = (x, y)  # Lưu vị trí bắt đầu
        self.end_position = None      # Lưu vị trí cuối cùng

    def update_path(self, maze, target, algorithm):
        if algorithm == "BFS":
            print(f"Running BFS for boat at ({self.row}, {self.col})")
            self.path = solve_maze_bfs(maze, (self.row, self.col), target) or []
        elif algorithm == "A*":
            #print(f"Running A* for boat at ({self.row}, {self.col})")
            self.path = solve_maze_astar(maze, (self.row, self.col), target) or []
        elif algorithm == "AC3+Backtracking":
           # print(f"Running AC3+Backtracking for boat at ({self.row}, {self.col})")
            absolute_path = backtrack_with_ac3(maze, (self.row, self.col), target)
            if absolute_path:
                self.path = path_to_directions(absolute_path)  # Chuyển sang hướng tương đối
              #  print(f"Converted path: {self.path}")
            else:
                self.path = []
                #print("Backtracking returned no path.")
        elif algorithm == "Simulated Annealing":
           # print(f"Running Simulated Annealing for boat at ({self.row}, {self.col})")
            self.path = simulated_annealing_path(
                maze, (self.row, self.col), target, max_iterations=1000, initial_temp=100, cooling_rate=0.99
            )
            if self.path is None:
                self.path = []
            #    print("Simulated Annealing did not find a path.")

        else:
            self.path = []  # Không tìm thấy đường đi
            print(f"No path found using {algorithm}. Boat remains at {self.end_position}.")


        
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
<<<<<<< HEAD
            
                print(f"Boat moved to ({self.row}, {self.col})")
=======
                    self.step_count += 1  # Cập nhật số bước
                    print(f"Boat moved to ({self.row}, {self.col}), Step Count: {self.step_count}")
                else:
                    print("Boat cannot move to the next cell.")
>>>>>>> cb0f2cb112ef04e746b6fd819be043a15a225e89
            else:
                # Cập nhật vị trí cuối cùng
                self.end_position = (self.row, self.col)
                print(f"Boat reached the end of its path at {self.end_position}.")
            self.last_move_time = current_time
<<<<<<< HEAD
        print(len(self.path))
=======





>>>>>>> cb0f2cb112ef04e746b6fd819be043a15a225e89
    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        surface.blit(self.image, (x, y))