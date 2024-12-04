import numpy as np
import pygame
import pickle
import os
from collections import deque
import json
import time

pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
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
    cell_size = 25  # Kích thước mỗi ô (đã phóng to)
    current_state = maze.start_position
    is_done = False
    episode_reward = 0
    path = [current_state]
    steps = 0  # Biến để lưu số bước

    if visualize:
        pygame.init()
        screen = pygame.display.set_mode((maze.maze_width * cell_size + 300, maze.maze_height * cell_size))  # Thêm không gian cho bộ đếm
        pygame.display.set_caption(f"TRAINING EPISODES - Current Episode: {current_episode + 1}")
        clock = pygame.time.Clock()
        background_image = pygame.image.load('Image/bgbg.jpg')  # Tải hình ảnh nền
        background_image = pygame.transform.scale(background_image, (maze.maze_width * cell_size, maze.maze_height * cell_size))  # Thay đổi kích thước
        side_background = pygame.image.load('Image/bl.png')  # Tải hình ảnh nền bên phải
        side_background = pygame.transform.scale(side_background, (300, maze.maze_height * cell_size))  # Thay đổi kích thước
        ddt_image = pygame.image.load('Image/by ddt.png')  # Tải hình ảnh "by DDT"
        ddt_image = pygame.transform.scale(ddt_image, (270, 200))  # Thay đổi kích thước hình ảnh nếu cần
        font = pygame.font.Font(None, 36)  # Khởi tạo font

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
        steps += 1  # Tăng số bước
        if train:
            agent.update_q_table(current_state, action, next_state, reward)
        current_state = next_state

        if visualize:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return episode_reward, len(path), path

            screen.blit(background_image, (0, 0))  # Vẽ hình ảnh nền chính
            for y in range(maze.maze_height):
                for x in range(maze.maze_width):
                    if maze.maze[y][x] == 1:  # Nếu là ô tường
                        wall_image = pygame.image.load('Image/blockk.png')  # Tải hình ảnh tường
                        wall_image = pygame.transform.scale(wall_image, (cell_size, cell_size))  # Thay đổi kích thước
                        screen.blit(wall_image, (x * cell_size, y * cell_size))  # Vẽ hình ảnh tường

            key_image = pygame.image.load('Image/key.png')  # Tải hình ảnh điểm bắt đầu
            key_image = pygame.transform.scale(key_image, (cell_size, cell_size))  # Thay đổi kích thước
            screen.blit(key_image, (maze.start_position[1] * cell_size, maze.start_position[0] * cell_size))  # Vẽ hình ảnh điểm bắt đầu
            moon_image = pygame.image.load('Image/moon.png')  # Tải hình ảnh đích
            moon_image = pygame.transform.scale(moon_image, (cell_size, cell_size))  # Thay đổi kích thước
            screen.blit(moon_image, (maze.goal_position[1] * cell_size, maze.goal_position[0] * cell_size))  # Vẽ hình ảnh đích
            rocket_image = pygame.image.load('Image/ufo.png')  # Tải hình ảnh rocket
            rocket_image = pygame.transform.scale(rocket_image, (cell_size, cell_size))  # Thay đổi kích thước
            screen.blit(rocket_image, (current_state[1] * cell_size, current_state[0] * cell_size))  # Vẽ hình ảnh rocket

            # Vẽ nền bên phải cho số bước và phần thưởng
            screen.blit(side_background, (maze.maze_width * cell_size, 0))  # Vẽ nền bên phải

            # Hiển thị số episode, số bước và phần thưởng
            episode_text = font.render(f'Episode: {current_episode + 1}', True, (255, 255, 255))  # Màu trắng
            steps_text = font.render(f'Steps: {steps}', True, (255, 255, 255))  # Màu trắng
            reward_text = font.render(f'Reward: {episode_reward}', True, (255, 255, 255))  # Màu trắng
            screen.blit(episode_text, (maze.maze_width * cell_size + 10, 10))  # Vị trí hiển thị số episode
            screen.blit(steps_text, (maze.maze_width * cell_size + 10, 50))  # Vị trí hiển thị số bước
            screen.blit(reward_text, (maze.maze_width * cell_size + 10, 90))  # Vị trí hiển thị phần thưởng

            # Vẽ hình ảnh "by DDT" ở góc dưới bên phải
            screen.blit(ddt_image, (maze.maze_width * cell_size + 10, maze.maze_height * cell_size - 250))  # Vị trí góc dưới bên phải

            pygame.display.flip()


    if visualize:
        pygame.time.delay(1000)  # Tạm dừng trong 1000 ms (1 giây)
        pygame.quit()
    return episode_reward, len(path), path
# Huấn luyện tác nhân với trực quan hóa từng episode
def continue_training(agent, maze, load_path="q_table_updated_1.pkl", save_path="q_table_updated_1.pkl", additional_episodes=100, visualize_interval=20):
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


with open(f"Maze/30.txt", 'r') as f:
    maze_layout = np.array(json.load(f))

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
