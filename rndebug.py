import pygame
import globals
import utils

ESCAPE = 27

elia_texture = pygame.image.load("textures/3lia03.png")
ichkeksi_texture = pygame.image.load("textures/ichkeksi.png")
damage_texture = pygame.image.load("textures/damage.png")
outline_texture = pygame.image.load("textures/outline.png")
crosshair_texture = pygame.image.load("textures/crosshair.png")
text_1 = pygame.image.load("textures/1.png")
text_2 = pygame.image.load("textures/2.png")
text_3 = pygame.image.load("textures/3.png")
background_texture = pygame.image.load("textures/background.png")
title_screen_texture = pygame.image.load("textures/title_screen.png")
level_selection_texture = pygame.image.load("textures/level_selection.png")
menu_texture = pygame.image.load("textures/menu.png")
web_texture = pygame.image.load("textures/Web.png")

# debugscreen
def showRNDebug():
    window = utils.setupWindow()
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == ESCAPE:
                    run = False
                    globals.titlescreen = True
                    utils.playSound('click')

        window.fill((0, 0, 0))
        window.blit(elia_texture, (0, 0))
        window.blit(ichkeksi_texture, (10, 0))
        window.blit(damage_texture, (20, 0))
        window.blit(outline_texture, (30, 0))
        window.blit(crosshair_texture, (40, 0))
        window.blit(text_1, (50, 0))
        window.blit(text_2, (60, 0))
        window.blit(text_3, (70, 0))
        window.blit(background_texture, (0, 10))
        window.blit(title_screen_texture, (100, 10))
        window.blit(menu_texture, (200, 10))
        window.blit(level_selection_texture, (300, 10))
        window.blit(web_texture, (0, 140))

        pygame.display.update()