import pygame
from Config import screen_width, screen_height, screen, font
from Colors import Colors


def draw_rounded_button(button_rect, text, color, font_size, border_color_outer=Colors.PURPLE_2, border_color_inner=Colors.LIGHT_YELLOW, border_thickness=3, radius=0, offset_x=-40):
    # Điều chỉnh vị trí của nút bằng cách dịch sang trái `offset_x` pixel
    adjusted_rect = button_rect.move(offset_x, 0)
    
    pygame.draw.rect(screen, border_color_outer, adjusted_rect, border_thickness + 2, border_radius=radius)
    
    pygame.draw.rect(screen, border_color_inner, adjusted_rect.inflate(-border_thickness * 2, -border_thickness * 2), border_thickness, border_radius=radius)
    
    pygame.draw.rect(screen, color, adjusted_rect.inflate(-border_thickness * 4, -border_thickness * 4), border_radius=radius)
    
    font = pygame.font.Font("Font/Jomplang-6Y3Jo.ttf", font_size)
    label = font.render(text, True, Colors.WHITE)
    screen.blit(label, label.get_rect(center=adjusted_rect.center))


import pygame

# Thiết lập các nút
def create_buttons(screen_width, screen_height):
    buttons = {
        "reset": pygame.Rect(screen_width - 220, screen_height - 560, 200, 60),
        "backtracking": pygame.Rect(screen_width - 220, screen_height - 480, 200, 60),
        "dfs": pygame.Rect(screen_width - 220, screen_height - 400, 200, 60),
        "bfs": pygame.Rect(screen_width - 220, screen_height - 320, 200, 60),
        "a_star": pygame.Rect(screen_width - 220, screen_height - 240, 200, 60),
        "home": pygame.Rect(screen_width - 220, screen_height - 160, 200, 60),
        "exit": pygame.Rect(screen_width - 220, screen_height - 80, 200, 60)
    }
    return buttons
