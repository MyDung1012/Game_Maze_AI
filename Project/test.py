import pygame
import sys
from Config import screen, screen_width, screen_height, maze_matrix, cell_width, cell_height, goal_image, goal_rect, background_image, win_imagee, lose_image, close_button, win_sound, maze_size, initial_depth_limit, win_image
from Player import Player
from Planets import planets
from Maze import Maze
from UI import draw_rounded_button, display_outcome_box, create_buttons
from AI import AI
from Colors import Colors
from UI import thongbao

initial_depth_limits = [18, 38, 58, 94, 106, 136, 164, 222, 178, 260]
# Khởi tạo các đối tượng và biến
pygame.init()
font = pygame.font.Font(None, 36)

# Tạo người chơi
player = Player(0, 0, cell_width, cell_height, 'Image/rocket.png', len(maze_matrix))

# Tạo mê cung
maze = Maze(maze_matrix)

# Tạo danh sách nút
buttons = create_buttons()

# Trạng thái của trò chơi
auto_move_path = None
auto_move_index = 0
AI_step = 0
auto_move_delay = 100
last_move_time = pygame.time.get_ticks()
player_step_counter = 0
game_completed = False
sound_played = False
show_image = True
ai_completed = False

# Vòng lặp chính
running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP1 or event.key == pygame.K_1:
                if player.move((1,-1), maze_matrix):  # Down-Left
                    player_step_counter += 1
            elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                if player.move((1, 0), maze_matrix):   # Down
                    player_step_counter += 1
            elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                if player.move((1, 1), maze_matrix):   # Down-Right
                    player_step_counter += 1
            elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                if player.move((0, -1), maze_matrix):  # Left
                    player_step_counter += 1
            elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                if player.move((0, 1), maze_matrix):   # Right
                    player_step_counter += 1
            elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                if player.move((-1,-1), maze_matrix): # Up-Left
                    player_step_counter += 1
            elif event.key == pygame.K_KP8 or event.key == pygame.K_8:
                if player.move((-1, 0), maze_matrix):  # Up
                    player_step_counter += 1
            elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                if player.move((-1,1), maze_matrix):  # Up-Right
                    player_step_counter += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if buttons["reset"].collidepoint(event.pos):
                print("Reset button clicked")
                player.reset_game()
                player_step_counter = 0  # Reset player step counter
                AI_step = 0
            elif buttons["home"].collidepoint(event.pos):
                print("Home button clicked")
                pygame.mixer.music.stop()   
                exec(open("Home.py", encoding="utf-8").read())
            elif buttons["bfs"].collidepoint(event.pos):
                print("BFS button clicked")
                player.reset_position()
                AI_step = 0
                auto_move_path = AI.solve_maze_bfs(maze_matrix, (player.row, player.col), (maze_size - 1, maze_size - 1))
                auto_move_index = 0
            elif buttons["a_star"].collidepoint(event.pos):
                print("A* button clicked")
                player.reset_position()
                AI_step = 0
                auto_move_path = AI.solve_maze_astar(maze_matrix, (player.row, player.col), (maze_size - 1, maze_size - 1))
                auto_move_index = 0
            elif buttons["dfs"].collidepoint(event.pos):
                player.reset_position()
                AI_step = 0
                auto_move_path = AI.solve_maze_dfs(maze_matrix, (player.row, player.col), (maze_size - 1, maze_size - 1))
                auto_move_index = 0
                print("DFS button clicked")
            elif buttons["backtracking"].collidepoint(event.pos):
                print(f"Initial Depth Limit: {initial_depth_limit}")
                player.reset_position()
                AI_step = 0
                auto_move_path = AI.solve_backtracking(maze_matrix, (player.row, player.col), (maze_size - 1, maze_size - 1), initial_depth_limit )
                auto_move_index = 0
                print("Backtracking with AC3 button clicked")
            elif buttons["exit"].collidepoint(event.pos):
                print("Exit button clicked")
                pygame.quit()
                sys.exit()  # Thoát khỏi trò chơi
            
        if event.type == pygame.MOUSEBUTTONDOWN: #and show_image:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            # Kiểm tra nếu chuột nhấn vào nút đóng
                if close_button.collidepoint(mouse_x, mouse_y):
                    show_image = False  # Ẩn hình ảnh
                    win_sound.stop()

    screen.fill((0, 0, 0))

    show_outcome = False  # Biến điều kiện để hiển thị thông báo
    outcome_time = 0
    # Check if it's time to move to the next step
    if auto_move_path and auto_move_index < len(auto_move_path):
        direction = auto_move_path[auto_move_index]
        player.move(direction, maze_matrix)
        auto_move_index += 1  # Move to the next step
        AI_step += 1  # Increment AI_step for each move
        pygame.time.delay(100)  # Delay of 0.1 seconds (100 milliseconds)

        if auto_move_index >= len(auto_move_path):
            ai_completed = True 
            auto_move_path = None


    screen.blit(background_image, (0, 0))

    for planet in planets:
        planet.update()
        planet.draw(screen)

    # Vẽ mê cung
    maze.draw(screen)

    #Vẽ đích
    goal_x = (maze_size - 1) * cell_width + (cell_width - goal_rect.width) // 2
    goal_y = (maze_size - 1) * cell_height + (cell_height - goal_rect.height) // 2
    screen.blit(goal_image, (goal_x, goal_y))

    # Draw player
    player.draw(screen)
    
    # Draw AI step counter
    # Định nghĩa kích thước và màu sắc của textbox
    textbox_width = 300
    textbox_height = 50
    textbox_color = Colors.PINK  # Màu nền của textbox
    border_color = Colors.WHITE  # Màu viền của textbox
    border_thickness = 3  # Độ dày của viền

    # Textbox cho số bước của AI
    ai_textbox_rect = pygame.Rect(screen_width - 400, 60, textbox_width, textbox_height)
    pygame.draw.rect(screen, border_color, ai_textbox_rect, border_thickness)  # Vẽ viền
    pygame.draw.rect(screen, textbox_color, ai_textbox_rect.inflate(-border_thickness*2, -border_thickness*2))  # Vẽ nền

    # Hiển thị số bước của AI
    ai_step_text = font.render(f"AI Steps: {AI_step}", True, Colors.WHITE)
    ai_text_rect = ai_step_text.get_rect(center=ai_textbox_rect.center)  # Canh giữa văn bản trong textbox
    screen.blit(ai_step_text, ai_text_rect)

    # Textbox cho số bước của người chơi
    player_textbox_rect = pygame.Rect(screen_width - 400, 140, textbox_width, textbox_height)
    pygame.draw.rect(screen, border_color, player_textbox_rect, border_thickness)  # Vẽ viền
    pygame.draw.rect(screen, textbox_color, player_textbox_rect.inflate(-border_thickness*2, -border_thickness*2))  # Vẽ nền

    # Hiển thị số bước của người chơi
    step_text = font.render(f"Steps: {player_step_counter}", True, Colors.WHITE)
    step_text_rect = step_text.get_rect(center=player_textbox_rect.center)  # Canh giữa văn bản trong textbox
    screen.blit(step_text, step_text_rect)


    draw_rounded_button(buttons["reset"], "Reset", Colors.DARK_BLUE, 36 )
    draw_rounded_button(buttons["home"], "Home",Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["bfs"], "BFS", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["dfs"], "DFS", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["exit"], "Exit", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["a_star"], "A*", Colors.DARK_BLUE, 36)
    draw_rounded_button(buttons["backtracking"], "Backtracking", Colors.DARK_BLUE, 36)

    # Hiển thị thông báo hoàn thành
    font = pygame.font.Font(None, 36)
    game_completed = False
    
    if player.is_at_goal():
        game_completed = True
    
    # Hiển thị hướng dẫn
    
    if ai_completed and player_step_counter > 0:
        if AI_step + (maze_size * 0.2) > player_step_counter:
            outcome_text = "YOU WIN!!!"
        elif AI_step + (maze_size * 0.2) < player_step_counter:
            outcome_text = "YOU LOSE!!!"
        else:
            outcome_text = "DRAW!!!"

        if outcome_text == "YOU WIN!!!" and show_image:
            screen.blit(win_imagee, (screen_width // 2 - win_image.get_width() // 2,
                                    screen_height // 2 - win_image.get_height() // 2))
            pygame.draw.rect(screen, (255, 0, 0), close_button)  # Vẽ nút đỏ
            close_text = font.render("X", True, (255, 255, 255))
            screen.blit(close_text, (close_button.x + 5, close_button.y))
        elif outcome_text == "YOU LOSE!!!" and show_image:
                screen.blit(lose_image, (screen_width // 2 - lose_image.get_width() // 2,
                                        screen_height // 2 - lose_image.get_height() // 2))
                pygame.draw.rect(screen, (255, 0, 0), close_button)  # Vẽ nút đỏ
                close_text = font.render("X", True, (255, 255, 255))
                screen.blit(close_text, (close_button.x + 5, close_button.y))

    elif AI_step == 0 and player_step_counter > 0:
        outcome_text = "CHOOSE AI ALGORITHM"
    elif AI_step == 0 and player_step_counter == 0:
        outcome_text = "IT'S YOUR TURN"
    thongbao(outcome_text)

       
    # Cập nhật màn hình
    pygame.display.flip()
    pygame.time.delay(30)