import pygame
from collections import deque
import heapq

class AI:
    def __init__(self):
        pass

    @staticmethod
    def solve_maze_bfs(maze, start, goal):
        directions = [
            (-1, 0),  # lên
            (1, 0),   # xuống
            (0, -1),  # trái
            (0, 1),   # phải
            #(-1, -1), # trên-trái
            #(-1, 1),  # trên-phải
            #(1, -1),  # dưới-trái
            #(1, 1)    # dưới-phải
        ]
        
        rows = len(maze)
        cols = len(maze[0])
        
        queue = deque([(start)])
        visited = {start}
        
        # Dictionary lưu đường đi
        came_from = {}
        
        while queue:
            current = queue.popleft()
            
            if current == goal:
                # Tái tạo đường đi
                path = []
                while current in came_from:
                    prev = came_from[current]
                    path.append((current[0] - prev[0], current[1] - prev[1]))
                    current = prev
                path.reverse()
                return path
                
            # Kiểm tra tất cả các hướng có thể đi
            for dx, dy in directions:
                next_row = current[0] + dx
                next_col = current[1] + dy
                neighbor = (next_row, next_col)
                
                # Kiểm tra điều kiện hợp lệ
                if (0 <= next_row < rows and 
                    0 <= next_col < cols and 
                    maze[next_row][next_col] == 0 and  # 0 là đường đi
                    neighbor not in visited):
                    
                    queue.append(neighbor)
                    visited.add(neighbor)
                    came_from[neighbor] = current
        
        return None  # Không tìm thấy đường đi

    @staticmethod
    def solve_maze_dfs(maze, start, goal):
    # 8 hướng di chuyển: trên, dưới, trái, phải, và 4 hướng chéo
        directions = [
            (-1, 0),  # lên
            (1, 0),   # xuống
            (0, -1),  # trái
            (0, 1),   # phải
            #(-1, -1), # trên-trái
            #(-1, 1),  # trên-phải
            #(1, -1),  # dưới-trái
            #(1, 1)    # dưới-phải
        ]
        
        rows = len(maze)
        cols = len(maze[0])
        
        # Khởi tạo stack và visited set
        stack = [(start)]
        visited = {start}
        
        # Dictionary lưu đường đi
        came_from = {}
        
        while stack:
            current = stack.pop()  # Lấy phần tử cuối cùng của stack
            
            if current == goal:
                # Tái tạo đường đi
                path = []
                while current in came_from:
                    prev = came_from[current]
                    path.append((current[0] - prev[0], current[1] - prev[1]))
                    current = prev
                path.reverse()
                return path
                
            # Kiểm tra tất cả các hướng có thể đi
            for dx, dy in directions:
                next_row = current[0] + dx
                next_col = current[1] + dy
                neighbor = (next_row, next_col)
                
                # Kiểm tra điều kiện hợp lệ
                if (0 <= next_row < rows and 
                    0 <= next_col < cols and 
                    maze[next_row][next_col] == 0 and  # 0 là đường đi
                    neighbor not in visited):
                    
                    stack.append(neighbor)
                    visited.add(neighbor)
                    came_from[neighbor] = current
        
        return None  # Không tìm thấy đường đi


    @staticmethod
    def heuristic(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    @staticmethod
    def solve_maze_astar(maze, start, goal):
        directions = [
            (-1, 0),  # lên
            (1, 0),   # xuống
            (0, -1),  # trái
            (0, 1),   # phải
            #(-1, -1), # trên-trái
            #(-1, 1),  # trên-phải
            #(1, -1),  # dưới-trái
            #(1, 1)    # dưới-phải
        ]
        
        rows = len(maze)
        cols = len(maze[0])
        
        # Tập đóng và tập mở
        closed_set = set()
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        # Lưu đường đi
        came_from = {}
        
        # g_score[n] là chi phí từ start đến node n
        g_score = {start: 0}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            
            if current == goal:
                # Tái tạo đường đi
                path = []
                while current in came_from:
                    prev = came_from[current]
                    path.append((current[0] - prev[0], current[1] - prev[1]))
                    current = prev
                path.reverse()
                return path
                
            closed_set.add(current)
            
            # Kiểm tra tất cả các hướng có thể đi
            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                
                # Kiểm tra điều kiện hợp lệ
                if (neighbor[0] < 0 or neighbor[0] >= rows or 
                    neighbor[1] < 0 or neighbor[1] >= cols or
                    maze[neighbor[0]][neighbor[1]] == 1 or  # 1 là tường
                    neighbor in closed_set):
                    continue
                    
                tentative_g_score = g_score[current] + 1
                
                if (neighbor not in g_score or 
                    tentative_g_score < g_score[neighbor]):
                    
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + AI.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
        
        return None  # Không tìm thấy đường đi

    @staticmethod
    def solve_backtracking(maze, start, goal, initial_depth_limit):
    # Directions for movement
        directions = [
            (-1, 0),  # up
            (1, 0),   # down
            (0, -1),  # left
            (0, 1),   # right
            #(-1, -1), # up-left
            #(-1, 1),  # up-right
            #(1, -1),  # down-left
            #(1, 1)    # down-right
        ]
        
        # Initialize depth limits and constraints for recursion
        depth_limit = initial_depth_limit
        max_depth_limit = 1000
        max_backtracks = 10000
        stepIDS = 50

        # Heuristic function to estimate distance to the goal
        def heuristic(cell):
            return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

        path = []  # To store the current path

        # Simplified AC-3 for debugging
        def ac3_constraints(current):
            # Just return True for debugging to bypass constraints
            return True

        # Main backtracking function with depth and backtrack limits
        def backtrack(current, depth, visited, backtracks):
            # Debug: Print current position and depth
            print(f"Visiting {current}, depth {depth}, backtracks {backtracks}")

            # Check if we've exceeded the depth or backtrack limits
            if depth > depth_limit or backtracks >= max_backtracks:
                print(f"Depth or backtrack limit reached at {current}")
                return False

            # Check if we reached the goal
            if current == goal:
                print("Goal reached!")
                return True

            visited.add(current)
            
            # Sort directions based on distance to goal
            sorted_directions = sorted(directions, key=lambda d: heuristic((current[0] + d[0], current[1] + d[1])))

            for direction in sorted_directions:
                next_cell = (current[0] + direction[0], current[1] + direction[1])

                # Check validity of the next cell
                if (0 <= next_cell[0] < len(maze) and 
                    0 <= next_cell[1] < len(maze[0]) and 
                    maze[next_cell[0]][next_cell[1]] == 0 and 
                    next_cell not in visited):

                    # Apply simplified AC-3 constraint for debugging
                    if ac3_constraints(next_cell):
                        path.append(direction)
                        
                        # Recur with updated depth and backtrack count
                        if backtrack(next_cell, depth + 1, visited, backtracks):
                            return True

                        # Backtrack if the current path doesn't lead to a solution
                        path.pop()
                        backtracks += 1  # Increase backtrack count after unsuccessful attempt

            visited.remove(current)  # Clean up visited for this path
            return False

        # Iteratively increase depth limit if no solution found
        while depth_limit <= max_depth_limit:
            print(f"Trying depth limit {depth_limit}")
            visited = set()  # Reset visited set for each new depth limit attempt
            if backtrack(start, 0, visited, 0):
                print("Path found!")
                return path  # Return the successful path
            else:
                print("No path found, increasing depth limit")
                depth_limit += stepIDS  # Increment depth limit for iterative deepening

        print("No solution found within depth and backtrack limits.")
        return None  # Return None if no path is found
            
