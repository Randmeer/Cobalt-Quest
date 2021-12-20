import random
import time
import pygame
import QuickJSON

import utils
from utils import globs, mp_scene, mp_screen, get_setting, render_text, rta_dual, angle_deg, conv_deg_rad, set_global_defaults, cout
from utils.images import images
from render.sprites import gui, dagger
from render import camera
from logic.gui.overlay import pause_screen, show_inventory, end_screen
from render.sprites import block
from render.sprites.entity import player, apprentice
from render.sprites.projectile import shuriken, arrow
from render.sprites.particle_cloud import ParticleCloud

class Floor:

    def __init__(self, window):
        """
        game logic for a single floor of a dungeon

        main functions:
        load() --> loads floor json
        save() --> saves floor json
        start_loop() --> starts game loop
        end_loop() --> ends game loop

        local functions:
        single_loop() --> runs update and render functions
        update() --> updates objects, handles input
        render() --> renders objects
        """
        set_global_defaults()
        self.window = window
        self.surface = pygame.Surface(globs.SIZE, pygame.SRCALPHA)
        self.floorjson = QuickJSON.QJSON(path=f"./data/savegames/{get_setting('current_savegame')}/dungeons/{globs.dungeon_str}/{globs.floor_str}.json")
        self.invjson = QuickJSON.QJSON(f"./data/savegames/{get_setting('current_savegame')}/inventory.json")
        self.guisprite = gui.IngameGUI(invjson=self.invjson)
        self.clock = pygame.time.Clock()

    def load(self):
        """
        loads the json of the respective floor and creates all the specified
        block & entity classes and the player class
        """
        self.blocks, self.entitys, self.particles, self.projectiles, self.melee, self.events = [], [], [], [], [], []
        self.now, self.prev_time, self.delta_time = 0, 0, 0
        self.cooldown, self.sidelength = 0.5, 0
        self.player, self.scene = None, None
        self.run = True
        self.click = False

        # load floor json
        self.floorjson.load()
        self.invjson.load()
        self.sidelength = self.floorjson["size"] * 16 * 2
        self.player = player.Player(particles=self.particles, pos=(self.floorjson["player"][0], self.floorjson["player"][1]), health=self.invjson["health"], mana=self.invjson["mana"])
        # read and convert blocks to Block()'s in list
        blocks = list(self.floorjson["blocks"])
        for i in range(self.floorjson["size"] * 2):
            for j in range(self.floorjson["size"] * 2):
                if blocks[i][j] != 0:
                    x, y = j - self.floorjson["size"], i - self.floorjson["size"]
                    if x < 0 and y < 0:
                        pass
                    elif x > 0 and y < 0:
                        x += 1
                    elif x > 0 and y > 0:
                        x += 1
                        y += 1
                    elif x < 0 and y > 0:
                        y += 1
                    self.blocks.append(block.Block(block=blocks[i][j], pos=(x, y)))

        # read and convert entitys to Entity()'s in list
        for i in self.floorjson["entitys"]:
            if i[0] == "apprentice":
                self.entitys.append(apprentice.Apprentice(particles=self.particles, pos=(i[1][0], i[1][1]), health=i[2], weapon=i[3], floorjson=self.floorjson))

        # create scene and set camera target
        self.scene = camera.Scene(sidelength=self.sidelength)
        self.scene.camera.follow(target=self.player)

        self.particles.append(ParticleCloud(center=(self.sidelength / 2, 0), radius=self.sidelength*2,
                      color=(255, 0, 0), colorvariation=100, spawnregion=(2, self.sidelength), velocity=1,
                      priority=0, no_debug=True, distribution=0.1, emitter=True, particles_per_second=100))

    def save(self):
        self.floorjson["entitys"] = []
        for i in self.entitys:
            self.floorjson["entitys"].append(["apprentice", [i.position[0], i.position[1]], i.health, i.weapon])
        self.floorjson["player"] = self.player.position
        self.floorjson.save()
        self.guisprite.save_hotbar()
        self.invjson["health"] = self.player.health
        self.invjson["mana"] = self.player.mana
        self.invjson.save()

    def end_loop(self):
        self.run = False

    def update(self):
        """
        updates the game surface and handles user input
        """
        # calculate delta time
        self.now = time.time()
        self.delta_time = self.now - self.prev_time
        self.prev_time = self.now
        if self.cooldown > 0:
            self.cooldown -= self.delta_time

        # update objects
        self.click = False
        mp = mp_scene(scene=self.scene)
        self.scene.update(playerentity=self.player, delta_time=self.delta_time, blocks=self.blocks, entitys=self.entitys, particles=self.particles, projectiles=self.projectiles, melee=self.melee)
        self.guisprite.update(player=self.player)

        if self.player.health <= 0:
            self.invjson["health"] = 100
            self.invjson["deaths"] += 1
            self.invjson.save()
            end_screen(window=self.window, background=self.surface.copy(), end="defeat")
            self.end_loop()

        # handle events
        key = pygame.key.get_pressed()
        self.events = list(pygame.event.get())
        for event in self.events:
            # quitevent
            if event.type == pygame.QUIT:
                self.end_loop()
                globs.quitgame = True
            # buttonevents
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT and self.cooldown <= 0:
                    if self.guisprite.hotbar[self.guisprite.slot][1] == "dagger":
                        utils.play_sound('swing')
                        self.melee.append(dagger.Stab(playerpos=self.player.hitbox.center, mousepos=mp))
                        self.cooldown += 0.25
                    if self.guisprite.hotbar[self.guisprite.slot][2] > 0:
                        if self.guisprite.hotbar[self.guisprite.slot][1] == "shuriken":
                            utils.play_sound('swing')
                            self.projectiles.append(shuriken.Shuriken(exploding=True, pos=self.player.hitbox.center, radians=conv_deg_rad(angle_deg(self.player.hitbox.center, mp))))
                            self.cooldown += 0.25
                        elif self.guisprite.hotbar[self.guisprite.slot][1] == "bow":
                            utils.play_sound('swing')
                            self.projectiles.append(arrow.Arrow(pos=self.player.hitbox.center, radians=conv_deg_rad(angle_deg(self.player.hitbox.center, mp))))
                            self.cooldown += 1
                        self.guisprite.hotbar[self.guisprite.slot][2] -= 1
                elif event.button == pygame.BUTTON_RIGHT and self.cooldown <= 0:
                    if self.guisprite.hotbar[self.guisprite.slot][1] == "dagger":
                        utils.play_sound('swing')
                        self.melee.append(dagger.Swing(playerpos=self.player.hitbox.center, mousepos=mp))
                        self.cooldown += 0.5
                elif event.button == pygame.BUTTON_WHEELUP:
                    self.guisprite.set_selectangle(self.guisprite.slot - 1)
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    self.guisprite.set_selectangle(self.guisprite.slot + 1)
            # keyevents
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen(window=self.window, background=self.surface)
                    self.prev_time = time.time()
                elif event.key == pygame.K_e:
                    self.surface.blit(images["background"], (0, 0))
                    self.scene.draw(self.surface)
                    self.guisprite.save_hotbar()
                    show_inventory(window=self.window, background=self.surface)
                    self.guisprite.load_hotbar()
                    self.guisprite.update(player=self.player)
                    self.prev_time = time.time()
                elif event.key == pygame.K_SPACE and self.player.mana > 0:
                    self.player.dash()
                elif event.key == pygame.K_b:
                    if key[pygame.K_F3]:
                        globs.soft_debug = not globs.soft_debug
                        cout("soft_debug = " + str(globs.soft_debug))
                elif event.key == pygame.K_h:
                    if key[pygame.K_F3]:
                        globs.hard_debug = not globs.hard_debug
                        cout("hard_debug = " + str(globs.hard_debug))
                elif event.key == pygame.K_g:
                    if key[pygame.K_F3]:
                        globs.render_all = not globs.render_all
                        cout("render_all = " + str(globs.render_all))
                elif event.key == pygame.K_f:
                    if key[pygame.K_F3]:
                        globs.fps_meter = not globs.fps_meter
                        cout("fps_meter = " + str(globs.fps_meter))
                elif event.key == pygame.K_e:
                    pass
                elif event.key == pygame.K_1:
                    self.guisprite.set_selectangle(0)
                elif event.key == pygame.K_2:
                    self.guisprite.set_selectangle(1)
                elif event.key == pygame.K_3:
                    self.guisprite.set_selectangle(2)
                elif event.key == pygame.K_4:
                    self.guisprite.set_selectangle(3)
                elif event.key == pygame.K_5:
                    self.guisprite.set_selectangle(4)
                elif event.key == pygame.K_6:
                    self.guisprite.set_selectangle(5)
                elif event.key == pygame.K_x:
                    self.save()
                    print("game saved")

        # end loop if exittomenu order is detected
        if globs.exittomenu:
            self.end_loop()
            globs.menu = True

    def render(self):
        """
        renders the gui and game surface
        """

        if globs.hard_debug:
            surface = pygame.Surface(self.window.get_size())
            surface.blit(pygame.transform.scale(images["background"], self.window.get_size()), (0, 0))
            self.scene.draw(surface)
            render_text(window=surface, text=str(round(self.clock.get_fps())) + "", pos=(surface.get_width() - 60 , 20), color=globs.WHITE, size=20)
        else:
            self.surface.blit(images["background"], (0, 0))
            self.scene.draw(self.surface)
            self.guisprite.draw(self.surface, self.clock)
            render_text(window=self.surface, text=str(round(self.clock.get_fps())) + "", pos=rta_dual(0.92, 0.02), color=globs.WHITE)
            surface = pygame.transform.scale(self.surface, globs.res_size)

        self.window.blit(surface, (0, 0))
        pygame.display.update()

    def single_loop(self):
        """
        method performs a single iteration of the game loop. This can be overridden to add extra functionality before and
        after the game loop and render. call update() to perform a raw iteration and and render() to render stuff out
        """
        self.render()
        self.update()

    def start_loop(self):
        self.prev_time = time.time()
        self.run = True
        while self.run:
            self.clock.tick(60)
            self.single_loop()
            #print("")
            #print(len(self.particles))
            #print(len(self.blocks))
            #print(len(self.entitys))
            #print(len(self.melee))
            #print(len(self.projectiles))
            #print(self.delta_time)
