import pygame
from data.utils import absToRel
from data.utils import relToAbs


class Outline(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.scale(pygame.image.load("data/textures/outline.png"), (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.relposx = 0.0
        self.relposy = 0.0

    def draw(self, window):
        self.relposx = round(number=(round((absToRel(pygame.mouse.get_pos()[0]) - 0.05) / 0.1) * 0.1), ndigits=1)
        self.relposy = round(number=(round((absToRel(pygame.mouse.get_pos()[1]) - 0.05) / 0.1) * 0.1), ndigits=1)
        self.rect.x = relToAbs(self.relposx)
        self.rect.y = relToAbs(self.relposy)
        window.blit(self.image, self.rect)
