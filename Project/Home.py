import pygame
import sys
import random
from Colors import Colors

# Khởi tạo pygame
pygame.init()

# Lấy kích thước màn hình hiện tại
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Maze Game Home")

# Âm thanh
background_sound = pygame.mixer.Sound('Sound/chillmusic.mp3')

# Tạo màu nền hồng
def draw_background():
    screen.fill((0, 0, 0))
    for star in stars:
        if star['visible']:
            pygame.draw.circle(screen, Colors.WHITE, (star['x'], star['y']), star['size'])

# Tạo danh sách ngôi sao
def create_stars(num_stars):
    stars = []
    for _ in range(num_stars):
        star = {
            'x': random.randint(0, screen_width),
            'y': random.randint(0, screen_height),
            'size': random.randint(1, 3),
            'visible': True
        }
        stars.append(star)
    return stars

# Hàm vẽ chữ với màu sắc khác nhau
def draw_colored_text(surface, text, center):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (75, 0, 130), (238, 130, 238)]
    font = pygame.font.Font("Front/diego3d.ttf", 60)
    angle = 0
    total_width = sum(font.size(char)[0] * 1.2 for char in text)
    start_x = (screen_width - total_width) // 2
    position_y = 20

    for i, char in enumerate(text):
        char_color = colors[i % len(colors)]
        char_surface = font.render(char, True, char_color)
        char_rect = char_surface.get_rect(topleft=(start_x + angle, position_y))
        surface.blit(char_surface, char_rect)
        angle += font.size(char)[0] * 1.2

# Hàm vẽ nút với góc bo tròn
def draw_rounded_button(surface, text, x, y, width, height, color, font_size):
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=15)
    font = pygame.font.SysFont("Front/04054_BeamRider3D (1).ttf", font_size)
    label = font.render(text, True, Colors.WHITE)
    text_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(label, text_rect)

custom_font = pygame.font.Font("Front/UTM-Birds-Paradise.ttf", 20)
difficulty_value = 10  # Giá trị ban đầu của thanh trượt là 10

# Hàm vẽ thanh trượt độ khó
def draw_difficulty_slider(surface, x, y, width, height, min_value, max_value, current_value):
    pygame.draw.rect(surface, Colors.YELLOW, (x, y, width, height))
    slider_x = x + int((current_value - min_value) / (max_value - min_value) * width)
    pygame.draw.rect(surface, Colors.WHITE, (slider_x - 10, y - 5, 20, height + 10))
    
    # Hiển thị giá trị hiện tại của thanh trượt
    font = pygame.font.SysFont("timesnewroman", 24, bold=True)
    value_text = font.render(f"{current_value}", True, Colors.YELLOW)
    surface.blit(value_text, (x + width + 20, y + (height // 2) - (value_text.get_height() // 2)))  # Xuất hiện bên phải thanh trượt

stars = create_stars(100)

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Kiểm tra nếu click vào thanh trượt
            if screen_width // 2 - 140 <= mouse_x <= screen_width // 2 + 140 and 280 <= mouse_y <= 310:
                difficulty_value = ((mouse_x - (screen_width // 2 - 140)) // 28 + 1) * 10

            # Kiểm tra nếu click vào nút "Start"
            elif screen_width // 2 - 100 <= mouse_x <= screen_width // 2 + 100 and 350 <= mouse_y <= 410:
                pygame.mixer.Sound.stop(background_sound)  # Dừng âm thanh nền
                exec(open("Game.py", encoding="utf-8").read())

            # Kiểm tra nếu click vào nút "Exit"
            elif screen_width - 220 <= mouse_x <= screen_width - 20 and screen_height - 80 <= mouse_y <= screen_height - 20:
                pygame.quit()
                sys.exit()

    draw_background()

    background_sound.play()
    draw_colored_text(screen, "AI MAZE GAME", (screen_width // 2, 0))

    custom_text = custom_font.render("MADE BY DUNG - DUONG - TRAN", True, Colors.PINK)
    subtitle_rect = custom_text.get_rect(center=(screen_width // 2, 90))
    screen.blit(custom_text, subtitle_rect)

    difficulty_font = pygame.font.SysFont("timesnewroman", 24)
    difficulty_label = difficulty_font.render(" SIZE: ", True, Colors.WHITE)
    screen.blit(difficulty_label, (screen_width // 2 - 230, 280))

    draw_difficulty_slider(screen, screen_width // 2 - 140, 280, 280, 30, 10, 100, difficulty_value)
    draw_rounded_button(screen, "START", screen_width // 2 - 100, 350, 200, 60, Colors.DARK_BLUE, 36)
    draw_rounded_button(screen, "Exit", screen_width - 220, screen_height - 80, 200, 60, Colors.DARK_BLUE, 36)

    for star in stars:
        if random.random() < 0.01:
            star['visible'] = not star['visible']

    pygame.display.flip()
