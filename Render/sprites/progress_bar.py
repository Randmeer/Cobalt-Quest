import pygame
from utils.__init__ import relToAbsDual, relToAbs, renderText, getTextRect

# ProgressBar class is unfinished, working on it. ~Rande

class ProgressBar:
    def __init__(self, icon, maxvalue: int, colors: ((int, int, int), (int, int, int)), relsize: (float, float), textanchor="left"):
        self.icon = icon
        self.maxvalue = maxvalue
        self.activecolor, self.passivecolor = colors[0], colors[1]
        self.relsize = relsize
        self.rect = pygame.Rect
        self.resize()
        self.set(value=50)

    def set(self, value):
        self.value = value
        self.surf.fill(self.activecolor)
        self.surf.blit(self.passivesurf, ((self.value / self.maxvalue) * self.surf.get_width(), 0))
        self.image = pygame.Surface(relToAbsDual(self.relsize[0]+0.175, self.relsize[1]), pygame.SRCALPHA)
        self.image.blit(self.surf, relToAbsDual(0.175, 0))
        renderText(self.image, "50", (0, 0), (255, 255, 255), self.relsize[1]*700)
        self.image.blit(self.icon, relToAbsDual(0.1, 0))

    def get(self):
        return self.image

    def resize(self):
        self.passivesurf = pygame.Surface(relToAbsDual(self.relsize[0], self.relsize[1]), pygame.SRCALPHA)
        self.passivesurf.fill(self.passivecolor)
        self.surf = pygame.Surface(relToAbsDual(self.relsize[0], self.relsize[1]), pygame.SRCALPHA)
        self.icon = pygame.transform.scale(self.icon, relToAbsDual(self.relsize[1], self.relsize[1]))
