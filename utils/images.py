import json
import random

import time
from json import JSONDecodeError

import pygame

tex_dir = './resources/textures/'

class Texture:
    """
    Class is used to manage animation and textures. when creating a Texture object give it the path of the image
    (default path is the texture folder) and it will automatically search for a file name like the image but with a
    .json suffix if it finds none the class will always return the loaded image. if it doeas however it will check for 
    a following structure:
    {
    "time": 1
    "randomized": false,
    "random_start": false,
    "frames": [
            {
                "index": 5,
                "time": 1
            }
        ]
    }
    "time" is obligatory and determines the default timeout in seconds
    
    "randomized" is not obligatory and will shuffle all undeclared indexes in "frames". Is False by default
    
    "random_start" will try to break up the synchronisation between same animations by setting the time_reference back 
    by a few seconds and thus starting from a random frame 
    
    "frames" represents the flow in wich each image will be shown. the items inside the list must correspond to the 
    stacked images inside the .png or it will throw a TextureError.the order of the items is the chronological order
    of the animation itself.The list itself must not be present. we will generate one using default times.same goes for 
    the items inside the list. as long as the number of items is correct any missing argument inside can be autogenerated 
    using default times and indexes.
    
    "index" represents the image index inside the stacked image.png
    
    "time" represents the timeout for this animation frame
    """
    def __init__(self, path: str, single_run=False, set_height=False):
        self.init_time = time.time()
        self.single_run = single_run
        self.iterations = 0
        self.path = path
        self.stop = False
        self.seth_bool = False
        if set_height == False:
            pass
        else:
            self.seth_bool = True
            self.seth_value = set_height

        try:
            self.image = pygame.image.load(self.path)
        except Exception:
            raise TextureError(f'unable to load file from {self.path} directory')
        self.has_json = True

        try:
            self.script = json.load(open(self.path.replace('.png', '.json')))

            self.height, self.width = self.image.get_height(), self.image.get_width()
            if self.seth_bool:
                #self.height, self.width = self.seth_value, self.image.get_width()
                self.frame_count = self.height // self.seth_value
                print(self.frame_count)
            else:
                self.frame_count = self.height // self.width

            try:
                self.default_time = self.script['time']
            except Exception:
                raise TextureError(f'image JSON must have valid "time" attribute')

            try:
                self.randomized = self.script['randomized']
            except KeyError:
                self.randomized = False
            
            try:
                self.randomized = self.script['random_start']
            except KeyError:
                self.randomized = False

            self.single_loop_time = self.frame_count * self.default_time

            if self.seth_bool:
                self.images = [self.image.subsurface((0, self.seth_value * i, self.width, self.seth_value)) for i in range(self.frame_count)]
            else:
                self.images = [self.image.subsurface((0, self.width * i, self.width, self.width)) for i in range(self.frame_count)]

            try:
                self.frame_list = self.script['frames']
                print('made it here')

                if len(self.frame_list) != self.frame_count:
                    raise TextureError(f'image number ({self.frame_count}) and script items ({len(self.frame_list)}) are incoherent')

                self.single_loop_time = 0
                empty = []
                for i in self.frame_list:
                    if 'time' not in i:
                        i['time'] = self.default_time
                    if 'index' not in i:
                        if self.randomized:
                            empty.append(self.frame_list.index(i))
                        else:
                            i['index'] = self.frame_list.index(i)

                if self.randomized:
                    indexes = random.sample(empty, len(empty))
                    for i in indexes:
                        self.frame_list[i]['index'] = empty[indexes.index(i)]

                for i in self.frame_list:
                    self.single_loop_time += i['time']
                self.init_time -= random.uniform(0, self.single_loop_time)

            except KeyError:
                self.frame_list = [{"index": i, "time": self.default_time} for i in range(self.frame_count)]

        except JSONDecodeError:
            self.has_json = False
            print(f"unable to find json for {self.path}")

    def get(self):
        """
        get is used to get the image to display. it will automatically pick the right one based on the time it was initialized
        :return: 
        """
        if self.stop: return False
        if self.has_json:
            now = time.time()
            delta_time = now - self.init_time
            delta_time %= self.single_loop_time

            for i in range(len(self.frame_list)):
                if delta_time - self.frame_list[i]['time'] <= 0:
                    if self.single_run:
                        iters = self.iterations
                        self.iterations = i
                        if i < iters:
                            self.stop = True
                            return False
                    return self.images[self.frame_list[i]['index']]
                delta_time -= self.frame_list[i]['time']
        else:
            return self.image

pygame.display.init()

background_dungeon_tx = {
    "northern_plains": pygame.image.load(tex_dir + "bg_dg_northern_plains.png").convert_alpha(),
    "southern_plains": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "tundra": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "meadow": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "snowy_tundra": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "desert": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "mushroom_island": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "steppe": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "ocean": pygame.image.load(tex_dir + "background.png").convert_alpha(),
    "volcano_island": pygame.image.load(tex_dir + "background.png").convert_alpha()
}

map_dungeon_tx = {
    "northern_plains": {
        0: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        1: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        2: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
    },
    "southern_plains": {
        0: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        1: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        2: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
    },
    "tundra": {
        0: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        1: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        2: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
    },
    "meadow": {
        0: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        1: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        2: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
    },
    "snowy_tundra": {
        0: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        1: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        2: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
    },
    "desert": {
        0: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        1: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        2: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
    },
    "mushroom_island": {
        0: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        1: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        2: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
    },
    "steppe": {
        0: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        1: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        2: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
    },
    "ocean": {
        0: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        1: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        2: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
    },
    "volcano_island": {
        0: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        1: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
        2: pygame.image.load(tex_dir + "map_dg_northern_plains.png").convert_alpha(),
    },
}

block_tx = {
    1: pygame.image.load(tex_dir + "cobblestone.png").convert_alpha(),
    2: pygame.image.load(tex_dir + "stone_bricks.png").convert_alpha(),
}

item_ol = {
    "weapon": pygame.image.load(tex_dir + "weapon.png").convert_alpha(),
}

item_tx = {
    "dagger": pygame.image.load(tex_dir + "dagger.png").convert_alpha(),
    "katana": pygame.image.load(tex_dir + "cross.png").convert_alpha(),             # X
    "bow": pygame.image.load(tex_dir + "bow.png").convert_alpha(),
    "shuriken": pygame.image.load(tex_dir + "shuriken.png").convert_alpha(),
    "unset": None,
    "rande": pygame.image.load(tex_dir + "rande.png").convert_alpha()
}

scene_test_tx = pygame.image.load(tex_dir + "debug_scene.png").convert_alpha()

bg_gui_tx = pygame.image.load(tex_dir + "background_menu.png").convert_alpha()
bg_tx = pygame.image.load(tex_dir + "background.png").convert_alpha()

Elia03_tx = pygame.image.load(tex_dir + "3lia03.png").convert_alpha()
brick_tx = pygame.image.load(tex_dir + "brick.png").convert_alpha()
broken_heart_tx = pygame.image.load(tex_dir + "broken_heart.png").convert_alpha()
chest_tx = pygame.image.load(tex_dir + "chest.png").convert_alpha()
cross_tx = pygame.image.load(tex_dir + "cross.png").convert_alpha()
crosshair_tx = pygame.image.load(tex_dir + "crosshair.png").convert_alpha()
damage_tx = pygame.image.load(tex_dir + "damage.png").convert_alpha()
damage_player_tx = pygame.image.load(tex_dir + "damage_player.png").convert_alpha()
defeat_tx = pygame.image.load(tex_dir + "defeat.png").convert_alpha()
empty_tx = pygame.image.load(tex_dir + "empty.png").convert_alpha()
gui_background_tx = pygame.image.load(tex_dir + "gui_background.png").convert_alpha()
gui_template_tx = pygame.image.load(tex_dir + "gui_template.png").convert_alpha()
heart_tx = pygame.image.load(tex_dir + "heart.png").convert_alpha()
ichkeksi_tx = pygame.image.load(tex_dir + "ichkeksi.png").convert_alpha()
icon_tx = pygame.image.load(tex_dir + "icon.png").convert_alpha()
icon_big_tx = pygame.image.load(tex_dir + "icon_big.png").convert_alpha()
lava_tx = pygame.image.load(tex_dir + "lava.png").convert_alpha()
level_selection_tx = pygame.image.load(tex_dir + "level_selection.png").convert_alpha()
logo_tx = pygame.image.load(tex_dir + "logo.png").convert_alpha()
menu_tx = pygame.image.load(tex_dir + "menu.png").convert_alpha()
menu_mode_1_tx = pygame.image.load(tex_dir + "menu_mode_1.png").convert_alpha()
menu_mode_2_tx = pygame.image.load(tex_dir + "menu_mode_2.png").convert_alpha()
menu_mode_3_tx = pygame.image.load(tex_dir + "menu_mode_3.png").convert_alpha()
mud_tx = pygame.image.load(tex_dir + "mud.png").convert_alpha()
outline_tx = pygame.image.load(tex_dir + "outline.png").convert_alpha()
overlay_tx = pygame.image.load(tex_dir + "overlay.png").convert_alpha()
pause_menu_tx = pygame.image.load(tex_dir + "pause_menu.png").convert_alpha()
rande_tx = pygame.image.load(tex_dir + "rande.png").convert_alpha()
sandstone_tx = pygame.image.load(tex_dir + "sandstone.png").convert_alpha()
selection_tx = pygame.image.load(tex_dir + "selection.png").convert_alpha()
settings_menu_tx = pygame.image.load(tex_dir + "settings_menu.png").convert_alpha()
tick_tx = pygame.image.load(tex_dir + "tick.png").convert_alpha()
title_screen_tx = pygame.image.load(tex_dir + "title_screen.png").convert_alpha()
victory_tx = pygame.image.load(tex_dir + "victory.png").convert_alpha()
wall_tx = pygame.image.load(tex_dir + "wall.png").convert_alpha()
web_tx = pygame.image.load(tex_dir + "web.png").convert_alpha()
wert32_tx = pygame.image.load(tex_dir + "wert32.png").convert_alpha()

import utils

def frame_list_sorter(e):
    return e['index']

class TextureError(utils.DefaultError):

    def __init__(self, errmsg):
        utils.DefaultError.__init__(errmsg)
