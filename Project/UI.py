import pygame
from Config import screen_width, screen_height, screen, font
from Colors import Colors


def draw_rounded_button(button_rect, text, color, font_size, border_color_outer=(186, 85, 211), border_color_inner=(255, 215, 0), border_thickness=3, radius=0, offset_x=-40):
    # Điều chỉnh vị trí của nút bằng cách dịch sang trái `offset_x` pixel
    adjusted_rect = button_rect.move(offset_x, 0)
    
    # Vẽ viền ngoài màu tím
    pygame.draw.rect(screen, border_color_outer, adjusted_rect, border_thickness + 2, border_radius=radius)
    
    # Vẽ viền trong màu vàng
    pygame.draw.rect(screen, border_color_inner, adjusted_rect.inflate(-border_thickness * 2, -border_thickness * 2), border_thickness, border_radius=radius)
    
    # Vẽ nền nút bên trong
    pygame.draw.rect(screen, color, adjusted_rect.inflate(-border_thickness * 4, -border_thickness * 4), border_radius=radius)
    
    # Vẽ chữ trên nút
    font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", font_size)
    label = font.render(text, True, Colors.WHITE)
    screen.blit(label, label.get_rect(center=adjusted_rect.center))


def display_outcome_box(screen, text, font):
    """Hiển thị hộp thông báo kết quả."""
    box_width, box_height = 400, 200
    box_x = (screen_width - box_width) // 2
    box_y = (screen_height - box_height) // 2

    # Vẽ bảng thông báo
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)

    # Hiển thị nội dung
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)

def thongbao(outcome_text):
    instructions_win = font.render(outcome_text, True, Colors.WHITE)
    instructions_win_rect = instructions_win.get_rect()
    instructions_win_rect.topleft = (screen_width - 300, 250)
    screen.blit(instructions_win, instructions_win_rect)

def create_buttons():
    """Tạo và trả về danh sách các nút bấm."""
    button_reset = pygame.Rect(screen_width - 220, screen_height - 560, 200, 60)
    button_backtracking = pygame.Rect(screen_width - 220, screen_height - 480, 200, 60)
    button_dfs = pygame.Rect(screen_width - 220, screen_height - 400, 200, 60)
    button_bfs = pygame.Rect(screen_width - 220, screen_height - 320, 200, 60)
    button_A = pygame.Rect(screen_width - 220, screen_height - 240, 200, 60)
    button_home = pygame.Rect(screen_width - 220, screen_height - 160, 200, 60)
    button_exit = pygame.Rect(screen_width - 220, screen_height - 80, 200, 60)
    return {
        "reset": button_reset,
        "backtracking": button_backtracking,
        "dfs": button_dfs,
        "bfs": button_bfs,
        "a_star": button_A,
        "home": button_home,
        "exit": button_exit
    }
