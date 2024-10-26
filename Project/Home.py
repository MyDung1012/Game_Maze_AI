import pygame
import sys
import random
from Colors import Colors

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
screen_width, screen_height = 1000, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game Home")

# Âm thanh
background_sound = pygame.mixer.Sound('Sound/background.wav')

# Tạo màu nền hồng
def draw_background():
    # Vẽ nền màu đen
    screen.fill((0, 0, 0))

    # Vẽ ngôi sao
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
            'size': random.randint(1, 3),  # Kích thước ngôi sao ngẫu nhiên
            'visible': True
        }
        stars.append(star)
    return stars

# Hàm vẽ chữ với màu sắc khác nhau
def draw_colored_text(surface, text, center):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (75, 0, 130), (238, 130, 238)]
    font = pygame.font.Font("Front/diego3d.ttf", 60)  # Sử dụng phông chữ 'diego3d.ttf'
    angle = 0

    # Tính toán chiều rộng tổng cộng của chữ
    total_width = sum(font.size(char)[0] * 1.2 for char in text)  # Tính chiều rộng với khoảng cách giữa các ký tự
    start_x = (screen_width - total_width) // 2  # Tính vị trí bắt đầu căn giữa

    # Điều chỉnh vị trí Y để di chuyển lên trên
    position_y = 20  # Thay đổi giá trị này để di chuyển lên hoặc xuống

    for i, char in enumerate(text):
        char_color = colors[i % len(colors)]
        char_surface = font.render(char, True, char_color)
        char_rect = char_surface.get_rect(topleft=(start_x + angle, position_y))  # Điều chỉnh vị trí y để nhích lên
        surface.blit(char_surface, char_rect)
        angle += font.size(char)[0] * 1.2  # Điều chỉnh khoảng cách giữa các ký tự

# Hàm vẽ nút với góc bo tròn
def draw_rounded_button(surface, text, x, y, width, height, color, font_size):
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=15)
    font = pygame.font.SysFont("Front/04054_BeamRider3D (1).ttf", font_size)
    label = font.render(text, True, Colors.WHITE)
    text_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(label, text_rect)

custom_font = pygame.font.Font("Front/UTM-Birds-Paradise.ttf", 20)

# Tạo biến độ khó
difficulty_value = 5  # Giá trị độ khó ban đầu

# Tạo hàm vẽ thanh trượt độ khó
def draw_difficulty_slider(surface, x, y, width, height, min_value, max_value, current_value):
    # Vẽ thanh trượt vàng
    pygame.draw.rect(surface, Colors.YELLOW, (x, y, width, height))
    
    # Tính toán vị trí của nút trượt dựa trên giá trị hiện tại
    slider_x = x + int((current_value - min_value) / (max_value - min_value) * width)
    
    # Vẽ nút trượt màu trắng
    pygame.draw.rect(surface, Colors.WHITE, (slider_x - 10, y - 5, 20, height + 10))  # Nút trượt có chiều rộng 20 pixel và nhô lên

# Tạo ngôi sao
stars = create_stars(100)  # Tạo 100 ngôi sao

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
                difficulty_value = int((mouse_x - (screen_width // 2 - 140)) / 280 * 10) + 1  # Cập nhật giá trị độ khó

    draw_background()  # Vẽ nền với ngôi sao nhấp nháy

    background_sound.play()
    # Vẽ tiêu đề với phông chữ mới
    draw_colored_text(screen, "PYGAME", (screen_width // 2, 0))  # Nhích lên vị trí y

    # Vẽ dòng chữ
    custom_text = custom_font.render("Play with us!", True, (255, 255, 255))
    subtitle_rect = custom_text.get_rect(center=(screen_width // 2, 90))  # Nhích lên
    screen.blit(custom_text, subtitle_rect)

    # Vẽ thanh trượt độ khó
    difficulty_font = pygame.font.SysFont("timesnewroman", 24)
    difficulty_label = difficulty_font.render("Size: ", True, Colors.WHITE)
    screen.blit(difficulty_label, (screen_width // 2 - 230, 280))  # Vẽ chữ "Độ khó" nằm trước thanh trượt

    # Vẽ thanh trượt độ khó với giá trị hiện tại
    draw_difficulty_slider(screen, screen_width // 2 - 140, 280, 280, 30, 1, 10, difficulty_value)

    # Vẽ nút bắt đầu
    draw_rounded_button(screen, "START", screen_width // 2 - 100, 350, 200, 60, Colors.DARK_BLUE, 36)

    # Vẽ các nút lựa chọn
    draw_rounded_button(screen, "Human", screen_width // 2 - 200, 450, 150, 30, Colors.DARK_BLUE, 24)
    draw_rounded_button(screen, "AI", screen_width // 2 + 50, 450, 150, 30, Colors.DARK_BLUE, 24)

    # Vẽ nút thoát
    draw_rounded_button(screen, "Exit", screen_width - 220, screen_height - 80, 200, 60, Colors.DARK_BLUE, 36)

    # Cập nhật trạng thái của ngôi sao để tạo hiệu ứng nhấp nháy
    for star in stars:
        if random.random() < 0.01:  # 1% cơ hội để mỗi ngôi sao nhấp nháy
            star['visible'] = not star['visible']

    pygame.display.flip()
