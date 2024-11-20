import pygame
import sys
import random
from Config import screen, screen_width, screen_height, maze_matrix, cell_width, cell_height, goal_image, goal_rect, background_image, lose_image, maze_size, win_image, key_image, font
from Player import Player
from Planets import planets
from Maze import Maze
from UI import draw_rounded_button
from Colors import Colors
from Boat import Boat
from Key import generate_random_keys
from UI import create_buttons

def ai_move(auto_move_path, auto_move_index, maze_matrix):
    if auto_move_path is not None and auto_move_index < len(auto_move_path):
        direction = auto_move_path[auto_move_index]
        player.move(direction, maze_matrix)  # Assuming player is an instance of Player
        return auto_move_index + 1
    return auto_move_index  

# Hàm reset lại game
def reset_game():
    global player_step_counter, AI_step, keys, collected_keys, algorithm_selected, game_over, player_won, ai_active, start_time, num_keys

    # Reset trạng thái người chơi
    player.reset_position()
    player_step_counter = 0

    # Reset trạng thái thuyền
    boat.row, boat.col = maze_size - 1, 0
    boat.path = None
    boat.path_index = 0

    # Random lại keys
    num_keys = random.randint(3, 5)  # Reset số lượng keys ngẫu nhiên
    keys = generate_random_keys(maze_matrix, num_keys, key_image)  # Reset danh sách keys
    collected_keys = 0  # Reset số keys đã thu thập

    # Reset các biến trạng thái trò chơi
    AI_step = 0
    algorithm_selected = None
    game_over = False
    player_won = False
    ai_active = False

    # Reset thời gian bắt đầu
    start_time = pygame.time.get_ticks()


pygame.init()
player = Player(0, 0)
boat = Boat(maze_size - 1, 0)
maze = Maze(maze_matrix)
num_keys = random.randint(3, 5)
keys = generate_random_keys(maze_matrix, num_keys, key_image)
collected_keys = 0
buttons = create_buttons(screen_width, screen_height)

game_over = False  # Biến kiểm tra trạng thái trò chơi; False nghĩa là trò chơi vẫn đang diễn ra
player_won = False  # Biến kiểm tra xem người chơi đã thắng hay chưa; False nghĩa là người chơi chưa thắng
algorithm_selected = None  # Biến để lưu thuật toán đã chọn; None nghĩa là chưa có thuật toán nào được chọn
start_time = pygame.time.get_ticks()  # Lưu thời gian bắt đầu trò chơi
ai_active = False  # Biến kiểm tra xem AI có đang hoạt động hay không; False nghĩa là AI chưa hoạt động
auto_move_delay = 10  # Độ trễ (ms) giữa các bước tự động
last_move_time = pygame.time.get_ticks()  # Theo dõi thời gian của lần di chuyển cuối cùng
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            direction = None
            if event.key == pygame.K_LEFT:
                direction = (0, -1)  # Trái
            elif event.key == pygame.K_RIGHT:
                direction = (0, 1)   # Phải
            elif event.key == pygame.K_UP:
                direction = (-1, 0)  # Lên
            elif event.key == pygame.K_DOWN:
                direction = (1, 0)   # Xuống

            if direction:
                player.move(direction, maze_matrix)  # Call the move method of the Player class

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if buttons["reset"].collidepoint(event.pos):
                print("Reset button clicked")
                reset_game()
            elif buttons["home"].collidepoint(event.pos):
                print("Home button clicked")
                pygame.mixer.music.stop()
                exec(open("Home.py", encoding="utf-8").read())
            elif buttons["bfs"].collidepoint(event.pos):
                print("BFS button clicked")
                algorithm_selected = "BFS"
            elif buttons["a_star"].collidepoint(event.pos):
                print("A* button clicked")
                algorithm_selected = "A*"
            elif buttons["backtracking"].collidepoint(event.pos):
                print("Backtracking button clicked")
                algorithm_selected = "AC3+Backtracking"
            elif buttons["exit"].collidepoint(event.pos):
                print("Exit button clicked")
                pygame.quit()
                sys.exit()

    current_time = pygame.time.get_ticks() # Lấy thời gian hiện tại
    elapsed_time = (current_time - start_time) // 1000 # Thời gian cho ai bắt đầu chạy

    if elapsed_time >= 5 and algorithm_selected and not game_over:
        ai_active = True
        boat.update_path(maze_matrix, (player.row, player.col), algorithm_selected)
        boat.move(maze_matrix)

        if player.is_at_goal():
            pygame.time.delay(3000)
            if collected_keys == num_keys:
                game_over = True
                player_won = True
            else:
                game_over = True
                player_won = False

        # Kiểm tra nếu thuyền bắt được người chơi
        if (boat.row, boat.col) == (player.row, player.col):
            game_over = True
            player_won = False
            game_completed = True
 
    for key in keys:
        if not key.collected and player.row == key.row and player.col == key.col:
            key.collected = True
            collected_keys += 1

    screen.blit(background_image, (0, 0))
    for planet in planets:
        planet.update()
        planet.draw(screen)
    goal_x = (maze_size - 1) * cell_width + (cell_width - goal_rect.width) // 2
    goal_y = (maze_size - 1) * cell_height + (cell_height - goal_rect.height) // 2
    screen.blit(goal_image, (goal_x, goal_y))
    maze.draw(screen)
    player.draw(screen)
    boat.draw(screen)
    for key in keys:
        key.draw(screen)

    draw_rounded_button(buttons["reset"], "Reset", Colors.DARK_BLUE, 36 )
    draw_rounded_button(buttons["home"], "Home",Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["bfs"], "BFS", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["exit"], "Exit", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["a_star"], "A*", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["backtracking"], "Backtracking", Colors.DARK_BLUE, 36)

    keys_textbox_rect = pygame.Rect(screen_width - 400, 60, 300, 50)
    pygame.draw.rect(screen, Colors.WHITE, keys_textbox_rect, 3)  # Vẽ viền
    pygame.draw.rect(screen, Colors.PINK, keys_textbox_rect.inflate(-3*2, -3*2))  # Vẽ nền (3: độ dày của viền)

    keys_text = font.render(f"Keys: {collected_keys}/{num_keys}", True, Colors.WHITE)
    keys_text_rect = keys_text.get_rect(center=keys_textbox_rect.center)  # Canh giữa văn bản trong textbox
    screen.blit(keys_text, keys_text_rect)

    if game_over:
        if player_won:
            screen.blit(win_image, (screen_width // 2 - win_image.get_width() // 2,
                                    screen_height // 2 - win_image.get_height() // 2))
        else:
            screen.blit(lose_image, (screen_width // 2 - lose_image.get_width() // 2,
                                    screen_height // 2 - lose_image.get_height() // 2))
    
    pygame.display.flip()
