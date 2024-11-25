import pygame
import random
from Config import screen_width, screen_height, planet_images  

class Planet:
    def __init__(self, image, x, y):
        self.image = pygame.transform.scale(image, (85, 64))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.speed = random.randint(1, 5)
        self.direction = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x < -self.rect.width or self.rect.x > screen_width:
            self.rect.x = random.randint(screen_width, screen_width + 100)
            self.rect.y = random.randint(0, screen_height - self.rect.height)
            self.direction = random.choice([-1, 1])

    def draw(self, surface):
        surface.blit(self.image, self.rect)

planets = [Planet(planet_images[i], random.randint(0, screen_width), random.randint(0, screen_height - 70)) for i in range(3)]

