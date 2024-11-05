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

# Load sound
background_sound = pygame.mixer.Sound('Sound/background.wav')

# Load slider images
slider_image = pygame.image.load('Image/Slider.png')
slider_image = pygame.transform.scale(slider_image, (280, 30))
button_image = pygame.image.load('Image/Dragger.png')
button_image = pygame.transform.scale(button_image, (30, 50))

# Load difficulty level images (for levels 1 to 10)
difficulty_images = [pygame.image.load(f'Image/Level{i}.png') for i in range(1, 2)]
difficulty_images = [pygame.transform.scale(img, (200, 200)) for img in difficulty_images]

# Create a list of stars for the background
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

# Draw background with stars
def draw_background():
    screen.fill((0, 0, 0))
    for star in stars:
        if star['visible']:
            pygame.draw.circle(screen, Colors.WHITE, (star['x'], star['y']), star['size'])

# Draw colored text
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

# Draw rounded button
def draw_rounded_button(surface, text, x, y, width, height, color, font_size):
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=15)
    font = pygame.font.Font("Front/04054_BeamRider3D (1).ttf", font_size)
    label = font.render(text, True, Colors.WHITE)
    text_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(label, text_rect)

# Draw the difficulty slider
def draw_difficulty_slider(surface, x, y, width, height, min_value, max_value, current_value):
    surface.blit(slider_image, (x, y))
    slider_x = x + int((current_value - min_value) / (max_value - min_value) * width)
    surface.blit(button_image, (slider_x - 10, y - 10))
    # Display the image corresponding to the difficulty level
    image = difficulty_images[current_value - 1]
    surface.blit(image, (x + width + 20, y - 100))  # Adjust position as needed

# Set custom font
custom_font = pygame.font.Font("Front/UTM-Birds-Paradise.ttf", 20)

# Main variables
stars = create_stars(100)  # Generate 100 stars
difficulty_value = 1  # Initial difficulty level

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if screen_width // 2 - 140 <= mouse_x <= screen_width // 2 + 140 and 280 <= mouse_y <= 310:
                difficulty_value = int((mouse_x - (screen_width // 2 - 140)) / 280 * 10) + 1

    draw_background()  # Draw background with stars
    background_sound.play()
    draw_colored_text(screen, "PYGAME", (screen_width // 2, 0))
    custom_text = custom_font.render("Play with us!", True, (255, 255, 255))
    subtitle_rect = custom_text.get_rect(center=(screen_width // 2, 90))
    screen.blit(custom_text, subtitle_rect)

    # Draw the label and difficulty slider
    difficulty_font = pygame.font.SysFont("timesnewroman", 24)
    difficulty_label = difficulty_font.render("Size: ", True, Colors.WHITE)
    screen.blit(difficulty_label, (screen_width // 2 - 230, 280))
    draw_difficulty_slider(screen, screen_width // 2 - 140, 280, 280, 30, 1, 10, difficulty_value)

    # Draw buttons
    draw_rounded_button(screen, "START", screen_width // 2 - 100, 350, 200, 60, Colors.DARK_BLUE, 36)
    draw_rounded_button(screen, "Human", screen_width // 2 - 200, 450, 150, 30, Colors.DARK_BLUE, 24)
    draw_rounded_button(screen, "AI", screen_width // 2 + 50, 450, 150, 30, Colors.DARK_BLUE, 24)
    draw_rounded_button(screen, "Exit", screen_width - 220, screen_height - 80, 200, 60, Colors.DARK_BLUE, 36)

    # Update stars for twinkling effect
    for star in stars:
        if random.random() < 0.01:
            star['visible'] = not star['visible']

    pygame.display.flip()
