import numpy as np
import pygame
import pickle
import os
from collections import deque
class Maze:
    def __init__(self, maze, start_position, goal_position):
        self.maze = maze
        self.maze_height = maze.shape[0]
        self.maze_width = maze.shape[1]
        self.start_position = start_position    
        self.goal_position = goal_position
class QLearningAgent:
    def __init__(self, maze, learning_rate=0.1, discount_factor=0.9, exploration_start=1.0, exploration_end=0.01, num_episodes=100):
        self.q_table = np.zeros((maze.maze_height, maze.maze_width, 4))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_start = exploration_start
        self.exploration_end = exploration_end
        self.num_episodes = num_episodes
    def get_exploration_rate(self, current_episode):
        return max(self.exploration_end, self.exploration_start * (self.exploration_end / self.exploration_start) ** (current_episode / self.num_episodes))
    def get_action(self, state, current_episode):
        exploration_rate = self.get_exploration_rate(current_episode)
        if np.random.rand() < exploration_rate:
            return np.random.randint(4)
        else:
            return np.argmax(self.q_table[state])
    def update_q_table(self, state, action, next_state, reward):
        best_next_action = np.argmax(self.q_table[next_state])
        self.q_table[state][action] += self.learning_rate * (
            reward + self.discount_factor * self.q_table[next_state][best_next_action] - self.q_table[state][action]
        )
    # Lưu bảng Q vào file
    def save_q_table(self, file_path):
        if os.path.exists(file_path):  # Nếu file tồn tại
            with open(file_path, 'rb') as file:
                old_q_table = pickle.load(file)  # Tải Q-table cũ
            # Cộng dồn giá trị từ Q-table mới
            self.q_table = np.maximum(self.q_table, old_q_table)  # Chọn giá trị lớn nhất từ hai bảng
        # Lưu lại Q-table đã kết hợp
        with open(file_path, 'wb') as file:
            pickle.dump(self.q_table, file)
        print(f"Q-table updated and saved to {file_path}")
    # Tải bảng Q từ file
    def load_q_table(self, file_path):
        with open(file_path, 'rb') as file:
            self.q_table = pickle.load(file)
        print(f"Q-table loaded from {file_path}")
def finish_episode(agent, maze, current_episode, train=True, visualize=False):
    cell_size = 20  # Kích thước mỗi ô
    current_state = maze.start_position
    is_done = False
    episode_reward = 0
    path = [current_state]
    if visualize:
        pygame.init()
        screen = pygame.display.set_mode((maze.maze_width * cell_size, maze.maze_height * cell_size))
        pygame.display.set_caption(f"TRAINING EPISODES - Current Episode: {current_episode + 1}")
        clock = pygame.time.Clock()
    while not is_done:
        action = agent.get_action(current_state, current_episode)
        next_state = (current_state[0] + actions[action][0], current_state[1] + actions[action][1])
        if (
            next_state[0] < 0 or next_state[0] >= maze.maze_height or
            next_state[1] < 0 or next_state[1] >= maze.maze_width or
            maze.maze[next_state[0]][next_state[1]] == 1
        ):
            reward = -10
            next_state = current_state
        elif next_state == maze.goal_position:
            path.append(next_state)
            reward = 100
            is_done = True
        else:
            path.append(next_state)
            reward = -1
        episode_reward += reward
        if train:
            agent.update_q_table(current_state, action, next_state, reward)
        current_state = next_state
        if visualize:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return episode_reward, len(path), path

            screen.fill((255, 255, 255))
            for y in range(maze.maze_height):
                for x in range(maze.maze_width):
                    color = (0, 0, 0) if maze.maze[y][x] == 1 else (255, 255, 255)
                    pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
            for pos in path:
                pygame.draw.rect(screen, (0, 0, 255), (pos[1] * cell_size, pos[0] * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, (255, 0, 0), (maze.start_position[1] * cell_size, maze.start_position[0] * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, (0, 255, 0), (maze.goal_position[1] * cell_size, maze.goal_position[0] * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, (0, 255, 0), (current_state[1] * cell_size, current_state[0] * cell_size, cell_size, cell_size))
            pygame.display.flip()
            if current_episode == 0:
                clock.tick(5000)
            elif current_episode <=20:
                clock.tick(100)
            else:
                clock.tick(10)
    if visualize:
        pygame.quit()
    return episode_reward, len(path), path
# Huấn luyện tác nhân với trực quan hóa từng episode
def continue_training(agent, maze, load_path="q_table_updated_1.pkl", save_path="q_table_updated_1.pkl", additional_episodes=50, visualize_interval=10):
    global episode
    # Tải bảng Q từ file nếu có
    if os.path.exists(load_path):
        agent.load_q_table(load_path)
    else:
        print(f"No Q-table found at {load_path}, starting fresh.")

    # Huấn luyện thêm các episode
    for episode in range(additional_episodes):
        visualize = (episode % visualize_interval == 0)
        reward, steps, _ = finish_episode(agent, maze, current_episode=episode, train=True, visualize=visualize)
        print(f"Episode {episode+1}/{additional_episodes}: Reward = {reward}, Steps = {steps}")
    
    # Lưu lại bảng Q sau khi huấn luyện
    agent.save_q_table(save_path)


# Kiểm tra tác nhân
def test_agent(agent, maze, load_path="q_table_updated_1.pkl", visualize=True):
    import os
    # Tải bảng Q từ file
    if os.path.exists(load_path):
        agent.load_q_table(load_path)
    else:
        print(f"No Q-table found at {load_path}, testing on a fresh agent.")

    # Kiểm tra tác nhân với bảng Q hiện tại
    reward, steps, path = finish_episode(agent, maze, current_episode=200, train=False, visualize=visualize)
    print("Path:", path)
    print("Total reward:", reward)
    print("Steps:", steps)



def solve_maze_bfs(maze, start, goal):

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
            step = 0
            while current in came_from:
                prev = came_from[current]
                path.append((current[0] , current[1] ))
                current = prev
                step+=1
            path.reverse()
            return step,path
            
        # Kiểm tra tất cả các hướng có thể đi
        for dx, dy in actions:
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
# Define maze layout
maze_layout = np.array([
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0],
[1,1,1,1,1,0,1,0,0,1,1,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
[0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,0,1,1,1,0,0,0,1,1,0,0,0],
[0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0],
[0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0],
[0,0,1,1,0,0,0,1,0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0],
[0,0,1,0,1,1,0,1,1,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0],
[0,0,1,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,1,0],
[0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,1,0,0,0,1,1,1,1,1,0,0,0,0],
[0,0,0,0,0,1,0,0,0,0,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0],
[0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0,0,1,0],
[0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1,0],
[0,1,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,1,0],
[0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
[0,0,0,1,1,0,0,0,1,0,0,0,1,1,1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0],
[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0],
[0,0,0,0,0,0,1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0],
[1,1,1,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0],
[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1],
[0,0,0,1,0,0,0,1,1,1,1,1,0,0,1,1,0,1,1,0,0,1,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0],
[1,0,0,1,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0],
[0,0,1,1,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,0,1,1],
[1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
[1,0,0,1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
])
start = (0, 0)
goal = (29, 29)
# Initialize maze and agent
maze = Maze(maze_layout, start, goal)
agent = QLearningAgent(maze)
# Define possible actions (up, down, left, right)
actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
agent = QLearningAgent(maze)
continue_training(agent, maze, load_path="q_table_updated_1.pkl", save_path="q_table_updated_1.pkl", additional_episodes=100)



print("solve with RL")

test_agent(agent, maze, load_path="q_table_updated_1.pkl", visualize=True)

print("solve with bfs")
a,b = solve_maze_bfs(maze_layout,start,goal)
print(a)
print(b)