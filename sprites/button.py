import pygame
from utils import relToAbs
from utils import relToAbsDual
from utils import renderText
from utils import getTextRect


class Button(pygame.sprite.Sprite):

    def __init__(self, relwidth, relheight, textcontent, relpos, textcolor=(75, 75, 75), reltextsize=0.1, textsize=50,
                 relborder=0.02, bordercolor=(255, 255, 255), innercolor=(194, 205, 209)):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface(relToAbsDual(relwidth, relheight))
        self.surface.fill(bordercolor)
        self.innerarea = pygame.Surface(relToAbsDual(relwidth - relborder, relheight - relborder))
        self.innerarea.fill(innercolor)
        self.surface.blit(self.innerarea, (relToAbsDual(relborder / 2, relborder / 2)))
        self.button = self.surface
        self.text = textcontent
        self.textcolor = textcolor
        self.reltextsize = reltextsize
        self.textsize = relToAbs(reltextsize)
        self.rect = self.surface.get_rect()
        self.relposx = relpos[0]
        self.relposy = relpos[1]
        self.relwidth = relwidth
        self.relheight = relheight
        self.rect.x = relToAbs(relpos[0])
        self.rect.y = relToAbs(relpos[1])
        self.textrect = getTextRect(textcontent, textsize)
        self.textrect.center = self.rect.center

    def resize(self):
        self.button = pygame.transform.scale(self.surface, relToAbsDual(self.relwidth, self.relheight))
        self.rect = self.button.get_rect()
        self.rect.x = relToAbs(self.relposx)
        self.rect.y = relToAbs(self.relposy)
        self.textsize = relToAbs(self.reltextsize)
        self.textrect = getTextRect(self.text, self.textsize)
        self.textrect.center = self.rect.center

    def draw(self, window):
        window.blit(self.button, self.rect)
        renderText(window=window, text=self.text, position=self.textrect, color=self.textcolor, size=self.textsize)
