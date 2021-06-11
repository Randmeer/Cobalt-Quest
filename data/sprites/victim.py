import math

import pygame, random
from data import globals, utils
from data.utils import relToAbsDual
from data.utils import relToAbs
from data.utils import absToRel


class Victim(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((100, 100))
        self.original_image = pygame.image.load("data/textures/IchKeksi.png")
        self.image = pygame.transform.scale(pygame.image.load("data/textures/IchKeksi.png"), (relToAbsDual(0.1, 0.1)))
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        # self.floatx = 0
        # self.floaty = 0
        self.direction = random.randint(1, 4)
        self.onscreen = True
        self.velocity = globals.difficulty
        self.health = globals.victimhealthpointsmax
        self.breakcooldown = 0
        self.relposx = 0
        self.relposy = 0

    def summon(self):
        if self.onscreen:
            position = random.randint(relToAbs(0.1), relToAbs(0.9))

            if self.direction == 1:
                self.rect.center = (position, relToAbs(0.1) * -1)
                self.relposx = absToRel(position - relToAbs(0.05))
                self.relposy = absToRel(relToAbs(0.1) * -1 - relToAbs(0.05))

            elif self.direction == 3:
                self.rect.center = (position, relToAbs(1.1))
                self.relposx = absToRel(position - relToAbs(0.05))
                self.relposy = absToRel(relToAbs(1.1) - relToAbs(0.05))

            elif self.direction == 2:
                self.rect.center = (relToAbs(1.1), position)
                self.relposx = absToRel(relToAbs(1.1) - relToAbs(0.05))
                self.relposy = absToRel(position - relToAbs(0.05))

            elif self.direction == 4:
                self.rect.center = (relToAbs(0.1) * -1, position)
                self.relposx = absToRel(relToAbs(0.1) * -1 - relToAbs(0.05))
                self.relposy = absToRel(position - relToAbs(0.05))

    def update(self, player, click, webgroup, delta_time):
        if self.onscreen:

            collidemouse = self.rect.collidepoint(pygame.mouse.get_pos())
            collideweb = pygame.sprite.spritecollideany(self, webgroup)
            collideplayer = self.rect.colliderect(player.rect)
            collidereach = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)

            if collideweb:
                if self.breakcooldown > globals.victimbreakcooldownmax:
                    collideweb.kill()
                    self.breakcooldown = 0
                self.breakcooldown += 1
                self.velocity = 0.05 * delta_time
            else:
                self.velocity = 0.1 * delta_time

            if self.direction == 1:
                self.relposy += self.velocity

            elif self.direction == 2:
                self.relposx -= self.velocity

            elif self.direction == 3:
                self.relposy -= self.velocity

            elif self.direction == 4:
                self.relposx += self.velocity

            self.rect.x = relToAbs(self.relposx)
            self.rect.y = relToAbs(self.relposy)

            if self.rect.centerx > relToAbs(1.1) or self.rect.centerx < relToAbs(
                    0.1) * -1 or self.rect.centery > relToAbs(1.1) or self.rect.centery < relToAbs(
                0.1) * -1:
                self.kill()
                self.rect = None
                self.onscreen = False
                self.health = -1
                globals.victimsmissed += 1

            # THIS IS THE FINAL CODE
            if collidemouse and click and collidereach <= relToAbs(player.reach):
                self.health -= 1
                globals.damagesum += 1
                utils.playSound('hit')
            # UNCOMMENT AFTER

            # TEMPORARY CODE TO KILL VICTIMS FASTER
            # if collidemouse:
            #    self.health -= 1
            #    globals.damagesum += 1
            #    utils.playSound('hit')
            # REMOVE AFTER

            if collideplayer and globals.damagecooldown >= globals.maxcooldown:
                globals.playerhealthpoints -= 1
                globals.damagecooldown = 0
                utils.playSound('hurt')

            if self.health == 0:
                self.kill()
                self.rect = None
                globals.victimskilled += 1
                self.onscreen = False

            #print("x: " + str(round(self.relposx, 2)))
            #print("y: " + str(round(self.relposy, 2)))

    def draw(self, window):
        window.blit(self.image, self.rect)
