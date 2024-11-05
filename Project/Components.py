import pygame as pg
class Slider:
    def __init__(self, x, y, imgPath, scale):
        image = pg.image.load(imgPath).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.scale = scale
        self.image = pg.transform.scale(image, (int(self.scale * width), int(self.scale * height)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))