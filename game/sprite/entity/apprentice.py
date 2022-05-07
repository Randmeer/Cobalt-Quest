from octagon.utils.img import Texture
from octagon.sprites.entity import Entity
from octagon.utils import img

from game.sprite.particle.entity import Footstep, Die1, Die2, Damage, ManaDrop


class Apprentice(Entity):

    def __init__(self, env, pos, health=None, weapon=None, target=None):
        Entity.__init__(self, env=env, priority=2, automove=True, position=pos, automove_target=target,
                        footstep_particle=Footstep, death_particles=[Die1, Die2, ManaDrop], damage_particle=Damage)
        self.weapon = weapon
        if health is not None:
            self.health = health
        else:
            self.health = 100
        self.tex_up = Texture(img.entity["apprentice_up"], 0.2)
        self.tex_down = Texture(img.entity["apprentice_down"], 0.2)
        self.tex_right = Texture(img.entity["apprentice_right"], 0.2)
        self.tex_left = Texture(img.entity["apprentice_left"], 0.2)
        self.tex_idle = Texture(img.entity["apprentice_idle"], 0.4)
        self.image = self.tex_idle.get()
        self.rect = self.image.get_rect()
        self.velocity = 25
        self.attackcooldown = 1

    def update(self):
        self.entity_update()
        #if self.attackcooldown < 0:
        #    projectiles.append(Fireball(pos=self.hitbox.center, radians=conv_deg_rad(angle_deg(self.hitbox.center, player.hitbox.center))))
        #    self.attackcooldown = 10
        #self.attackcooldown -= delta_time