import pygame

from utils.images import outline_texture
from utils.__init__ import absToRel, rta_dual, relToAbs


def rel_pos(ind):
    return round(number=(round((absToRel(pygame.mouse.get_pos()[ind]) - 0.05) / 0.1) * 0.1), ndigits=1)

class Outline(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.scale(outline_texture, rta_dual(0.1, 0.1))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.relposx = self.relposy = 0.0

    def resize(self):
        self.image = pygame.transform.scale(self.original_image, (rta_dual(0.1, 0.1)))

    def draw(self, window):
        self.relposx, self.relposy = rel_pos(0), rel_pos(1)
        self.rect.x, self.rect.y = relToAbs(self.relposx), relToAbs(self.relposy)
        window.blit(self.image, self.rect)