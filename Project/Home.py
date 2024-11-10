import pygame
import sys
import random
from Colors import Colors


pygame.init()


info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Maze Game Home")


# âm thanh
pygame.mixer.music.load('Sound/chillmusic.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

# Hình độ khó
slider_image = pygame.image.load('Image/Slider.jpg')
slider_image = pygame.transform.scale(slider_image, (280, 30))
button_image = pygame.image.load('Image/Dragger.jpg')
button_image = pygame.transform.scale(button_image, (30, 50))

# Load slider images
slider_image = pygame.image.load('Image/Slider.jpg')
slider_image = pygame.transform.scale(slider_image, (280, 30))
button_image = pygame.image.load('Image/Dragger.jpg')
button_image = pygame.transform.scale(button_image, (30, 50))


# Load difficulty level images (for levels 1 to 10)
difficulty_images = [pygame.image.load(f'Image/Level{i}.png') for i in range(1, 2)]
difficulty_images = [pygame.transform.scale(img, (200, 200)) for img in difficulty_images]

# Hàm vẽ nền
def draw_background():
    screen.fill((0, 0, 0))
    for star in stars:
        if star['visible']:
            pygame.draw.circle(screen, Colors.WHITE, (star['x'], star['y']), star['size'])

# tạo các ngôi sao trên nền
def create_stars(num_stars):
    stars = []
    for _ in range(num_stars):
        star = {
            'x': random.randint(0, screen_width),
            'y': random.randint(0, screen_height),
            'size': random.randint(1, 2),
            'visible': True
        }
        stars.append(star)
    return stars


# Vẽ nền với ngôi sao
def draw_background():
    screen.fill((0, 0, 0))
    for star in stars:
        if star['visible']:
            pygame.draw.circle(screen, Colors.WHITE, (star['x'], star['y']), star['size'])


# Draw colored text
def draw_colored_text(surface, text, center):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (75, 0, 130), (238, 130, 238)]
    font = pygame.font.Font("Font/diego3d.ttf", 60)
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

# Draw rounded button
def draw_rounded_button(surface, text, x, y, width, height, color, font_size):
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=15)
    font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", font_size)
    label = font.render(text, True, Colors.WHITE)
    text_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(label, text_rect)

# Draw the difficulty slider
def draw_difficulty_slider(surface, x, y, width, height, min_value, max_value, current_value):
    surface.blit(slider_image, (x, y))
    slider_x = x + int((current_value - min_value) / (max_value - min_value) * width)
    surface.blit(button_image, (slider_x - 10, y - 10))

    # Kiểm tra xem current_value có hợp lệ không
    '''if 1 <= current_value <= len(difficulty_images):
        image = difficulty_images[current_value - 1]
        surface.blit(image, (x + width + 20, y - 100))
    else:
        # Nếu không, có thể vẽ một hình ảnh mặc định hoặc không làm gì cả
        print("Current value is out of range for difficulty images.")'''
    
    font = pygame.font.SysFont("timesnewroman", 20, bold=True)
    value_text = font.render(f"{current_value}", True, Colors.YELLOW)
    surface.blit(value_text, (x + width + 20, y + (height // 2) - (value_text.get_height() // 2)))

import pygame

# Hàm để chia nhỏ văn bản thành các dòng phù hợp với chiều rộng
def text_wrap(text, font, max_width):
    words = text.split()
    wrapped_lines = []
    line = ""

    for word in words:
        test_line = f"{line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            wrapped_lines.append(line)
            line = word
    if line:
        wrapped_lines.append(line)
    return wrapped_lines

def draw_instruction_popup(current_page):
    popup_width, popup_height = 600, 400
    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2

    pygame.draw.rect(screen, Colors.YELLOW_BLACK, (popup_x, popup_y, popup_width, popup_height), border_radius=15)
    
    # Sử dụng phông chữ Times New Roman với kích thước 36
    font = pygame.font.SysFont("timesnewroman", 22)

    # Chia văn bản thành các trang
    pages = [
        [
            "MAZE AI GAME - KHÁM PHÁ VÀ CHINH PHỤC.",
            "",
            "Chào mừng bạn đến với Maze AI Game! Đây là trò chơi nơi bạn sẽ được trải nghiệm và thử thách bản thân qua một mê cung được xây dựng thông minh bằng các thuật toán trí tuệ nhân tạo. Game sử dụng các thuật toán nổi tiếng như BFS (Tìm kiếm theo chiều rộng), DFS (Tìm kiếm theo chiều sâu) và A*, giúp người chơi định hướng và tìm đường thoát một cách hiệu quả.",
        ],
        [
            "HƯỚNG DẪN DI CHUYỂN",
            "8 - Di chuyển lên trên",
            "2 - Di chuyển xuống dưới",
            "4 - Di chuyển qua trái",
            "6 - Di chuyển qua phải",
            "7 - Di chuyển lên xéo bên trái",
            "9 - Di chuyển lên xéo bên phải",
            "1 - Di chuyển xuống xéo trái",
            "3 - Di chuyển xuống xéo phải",
        ],
        [
            "QUY TẮC TRÒ CHƠI",
            "",
            "Khi bạn đã hoàn thành trò chơi. Hãy nhấn lựa chọn một thuật toán AI bất kỳ. Bạn sẽ thắng nếu số bước đi của bạn ít hơn số bước đi của AI",
            "",
            "",
            "CHƠI VUI!",
        ]
    ]

    centered_lines = [
        "MAZE AI GAME - KHÁM PHÁ VÀ CHINH PHỤC.",
        "HƯỚNG DẪN DI CHUYỂN",
        "QUY TẮC TRÒ CHƠI",
        "CHƠI VUI!",
    ]

    # Hiển thị văn bản của trang hiện tại
    lines = pages[current_page]
    y_offset = popup_y + 20  # Vị trí bắt đầu cho dòng đầu tiên

    for line in lines:
        # Loại bỏ các dòng trống chỉ chứa khoảng trắng
        if line.strip():  # Chỉ xử lý dòng có chứa ký tự không phải khoảng trắng
            wrapped_lines = text_wrap(line, font, popup_width - 40)
        
            for wrapped_line in wrapped_lines:
                instruction_text = font.render(wrapped_line, True, Colors.WHITE)
                
                # Kiểm tra nếu dòng hiện tại cần căn giữa
                if wrapped_line.strip() in centered_lines:
                    text_rect = instruction_text.get_rect(center=(popup_x + popup_width // 2, y_offset))  # Căn giữa
                else:
                    text_rect = instruction_text.get_rect(topleft=(popup_x + 10, y_offset))  # Căn trái
                
                screen.blit(instruction_text, text_rect)
                y_offset += font.get_height() + 5  # Tăng y_offset để dòng tiếp theo xuống dưới
        else:
            y_offset += font.get_height() + 10  # Điều chỉnh khoảng cách giữa các đoạn văn nếu dòng trống


    # Nếu chưa phải trang cuối, vẽ nút mũi tên để chuyển trang
    if current_page < len(pages) - 1:
        draw_rounded_button(screen, "Next >", popup_x + popup_width - 100, popup_y + popup_height - 60, 80, 40, Colors.RED, 24)
    else:
        # Nếu là trang cuối cùng, vẽ nút CLOSE
        draw_rounded_button(screen, "CLOSE", popup_x + popup_width - 100, popup_y + popup_height - 60, 80, 40, Colors.RED, 24)

    # Trả về tọa độ và kích thước popup
    return popup_x, popup_y, popup_width, popup_height




# Set custom font
custom_font = pygame.font.Font("Font/UTM-Birds-Paradise.ttf", 20)
#difficulty_value = 10  # Giá trị ban đầu của thanh trượt là 10


# Main variables
#stars = create_stars(10000)  # Generate 1000 stars
difficulty_value = 10  # Initial difficulty level

# Main game loop

stars = create_stars(500)
slider_length = 300
show_instruction = False  



# Vòng lặp chính
current_page = 0 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Kiểm tra nếu click vào thanh trượt
            if screen_width // 2 - slider_length // 2 <= mouse_x <= screen_width // 2 + slider_length // 2 and 580 <= mouse_y <= 610:
                difficulty_value = max(10, min(100, round((mouse_x - (screen_width // 2 - slider_length // 2)) / slider_length * 10) * 10))
            # Kiểm tra nếu click vào nút "Start"
            elif screen_width // 2 - 100 <= mouse_x <= screen_width // 2 + 100 and 650 <= mouse_y <= 710:
                pygame.mixer.music.stop()
   

                with open('difficulty.txt', 'w') as f:
                    f.write("")
                    f.write(str(difficulty_value))
                exec(open("Game.py", encoding="utf-8").read())
            # Kiểm tra nếu click vào nút "Exit"
            elif screen_width - 220 <= mouse_x <= screen_width - 20 and screen_height - 80 <= mouse_y <= screen_height - 20:
                pygame.quit()
                sys.exit()
            elif not show_instruction and 0 <= mouse_x <= 200 and screen_height - 80 <= mouse_y <= screen_height - 20:
                show_instruction = True  # Hiển thị bảng thông báo
                current_page = 0  # Đặt lại trang về trang đầu tiên
            
                # Gọi hàm vẽ popup để lấy tọa độ popup
            popup_x, popup_y, popup_width, popup_height = draw_instruction_popup(current_page)
                
                # Nếu nhấn vào nút "Next >", chuyển sang trang tiếp theo
            if current_page < 2:  # Kiểm tra nếu chưa phải trang cuối
                if popup_x + popup_width - 100 <= mouse_x <= popup_x + popup_width - 20 and popup_y + popup_height - 60 <= mouse_y <= popup_y + popup_height - 20:
                        current_page += 1  # Chuyển sang trang tiếp theo
            else:  # Trang cuối cùng, nút CLOSE
                if popup_x + popup_width - 100 <= mouse_x <= popup_x + popup_width - 20 and popup_y + popup_height - 60 <= mouse_y <= popup_y + popup_height - 20:
                        show_instruction  = False  # Đóng bảng



    draw_background()  # Draw background with stars
   # background_sound.play()


    #draw_colored_text(screen, "AI MAZE GAME", (screen_width // 2, 0))

    # Tải hình ảnh logo
    logo_image = pygame.image.load('Image/logo.png')
    logo_image = pygame.transform.scale(logo_image, (600, 394))  # Thay đổi kích thước logo theo ý muốn

    logo_x = (screen_width - logo_image.get_width()) // 2 # Dời logo xuống dưới một chút
    logo_y = 40  # Điều chỉnh giá trị này để dời logo xuống (số càng lớn càng xuống dưới)
    screen.blit(logo_image, (logo_x, logo_y))

    # Thêm BY DUNG-DUONG-TRAN
    additional_image = pygame.image.load('Image/by DDT.png')  # Thay đổi đường dẫn tới ảnh của bạn
    additional_image = pygame.transform.scale(additional_image, (600, 50))  # Thay đổi kích thước ảnh theo ý muốn
    # Đặt vị trí của ảnh dưới logo
    additional_x = (screen_width - additional_image.get_width()) // 2
    additional_y = logo_y + logo_image.get_height() + 5  # Đặt ảnh dưới logo với khoảng cách 20 pixel
    screen.blit(additional_image, (additional_x, additional_y))

    difficulty_font = pygame.font.SysFont("timesnewroman", 24)
    difficulty_label = difficulty_font.render(" SIZE: ", True, Colors.WHITE)
    screen.blit(difficulty_label, (screen_width // 2 - 230, 580))

    draw_difficulty_slider(screen, screen_width // 2 - 140, 580, 280, 30, 10, 100, difficulty_value)

    draw_rounded_button(screen, "START", screen_width // 2 - 100, 650, 200, 60, Colors.DARK_BLUE, 36)
    draw_rounded_button(screen, "EXIT", screen_width - 220, screen_height - 80, 200, 60, Colors.DARK_BLUE, 36)
    draw_rounded_button(screen, "INSTRUCTION", 0, screen_height - 80, 200, 60, Colors.DARK_BLUE, 36)

    if show_instruction:
        draw_instruction_popup(current_page)

    for star in stars:
        if random.random() < 0.01:
            star['visible'] = not star['visible']

    pygame.display.flip()