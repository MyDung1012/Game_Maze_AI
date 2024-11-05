# Import necessary libraries
import pygame
import sys
import random
from Colors import Colors

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 1000, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game Home")

# Load sound and images
background_sound = pygame.mixer.Sound('Sound/background.wav')
slider_image = pygame.image.load('Image/Slider.png')
slider_image = pygame.transform.scale(slider_image, (280, 30))
button_image = pygame.image.load('Image/Dragger.png')
button_image = pygame.transform.scale(button_image, (30, 50))

# Load images for difficulty levels (1-10)
difficulty_images = [pygame.image.load(f'Image/Level_{i}.png') for i in range(1, 11)]
difficulty_images = [pygame.transform.scale(img, (100, 100)) for img in difficulty_images]

# Function to draw the difficulty slider
def draw_difficulty_slider(surface, x, y, width, height, min_value, max_value, current_value):
    surface.blit(slider_image, (x, y))
    slider_x = x + int((current_value - min_value) / (max_value - min_value) * width)
    surface.blit(button_image, (slider_x - 10, y - 10))
    
    # Display the image corresponding to the difficulty level
    image = difficulty_images[current_value - 1]
    surface.blit(image, (x + width + 20, y - 30))  # Adjust position as needed

# Main game loop
stars = create_stars(100)
difficulty_value = 5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if screen_width // 2 - 140 <= mouse_x <= screen_width // 2 + 140 and 280 <= mouse_y <= 310:
                difficulty_value = int((mouse_x - (screen_width // 2 - 140)) / 280 * 10) + 1

    draw_background()
    background_sound.play()

    draw_colored_text(screen, "PYGAME", (screen_width // 2, 0))
    custom_text = custom_font.render("Play with us!", True, (255, 255, 255))
    subtitle_rect = custom_text.get_rect(center=(screen_width // 2, 90))
    screen.blit(custom_text, subtitle_rect)

    difficulty_font = pygame.font.SysFont("timesnewroman", 24)
    difficulty_label = difficulty_font.render("Size: ", True, Colors.WHITE)
    screen.blit(difficulty_label, (screen_width // 2 - 230, 280))
    
    draw_difficulty_slider(screen, screen_width // 2 - 140, 280, 280, 30, 1, 10, difficulty_value)
    draw_rounded_button(screen, "START", screen_width // 2 - 100, 350, 200, 60, Colors.DARK_BLUE, 36)
    draw_rounded_button(screen, "Human", screen_width // 2 - 200, 450, 150, 30, Colors.DARK_BLUE, 24)
    draw_rounded_button(screen, "AI", screen_width // 2 + 50, 450, 150, 30, Colors.DARK_BLUE, 24)
    draw_rounded_button(screen, "Exit", screen_width - 220, screen_height - 80, 200, 60, Colors.DARK_BLUE, 36)

    for star in stars:
        if random.random() < 0.01:
            star['visible'] = not star['visible']

    pygame.display.flip()
