import pygame

import utils
from utils import globs
from utils.images import background_texture, logo_texture


def showTitleScreen(window):
    print("TITLE SCREEN START")
    utils.setGlobalDefaults()
    rndebugAccess = 0

    def draw():
        og_surface = pygame.Surface(globs.SIZE)
        og_surface.blit(background_texture, (0, 0))
        og_surface.blit(logo_texture, (og_surface.get_width()/2-logo_texture.get_width()/2, og_surface.get_height()/2-logo_texture.get_height()/2))
        version_rect = utils.getTextRect(f"v {globs.VERSION}", font="debug", size=10)
        version_rect.bottomleft = utils.rta_dual_height(0.02, 0.98)
        studio_rect = utils.getTextRect("Rande Studios", font="debug", size=10)
        studio_rect.bottomright = (utils.rta_width(1) - utils.rta_height(0.02), utils.rta_height(0.98))
        utils.renderText(og_surface, f"v {globs.VERSION}", version_rect, (16, 16, 16), font="debug", size=10)
        utils.renderText(og_surface, "Rande Studios", studio_rect, (16, 16, 16), font="debug", size=10)
        surface = pygame.transform.scale(og_surface, globs.res_size)
        window.blit(surface, (0, 0))
        pygame.display.update()
    draw()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                globs.menu = True
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r or event.key == pygame.K_ESCAPE:
                    pass
                # the following statement lets the user use the CMD-Q (macOS) or ALT-F4 (windows) -shortcut.
                elif event.key == globs.COMMAND or event.key == pygame.K_q or event.key == globs.ALT or event.key == globs.KEY_F4:
                    pass
                else:
                    globs.menu = True
                    run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            rndebugAccess = rndebugAccess + 1
        if not keys[pygame.K_r]:
            rndebugAccess = 0

        if rndebugAccess == 150:
            print("ACCESS GRANTED")
            globs.rndebug = True
            run = False

    utils.playSound('click')
    print("TITLE SCREEN END")
