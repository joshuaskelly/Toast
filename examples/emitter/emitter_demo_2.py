from toast.scene_graph import Component, Scene
from toast.sprite import Sprite
from toast.animation import Animation
from toast.image_sheet import ImageSheet
from toast.resource_loader import ResourceLoader
from toast.event_manager import EventManager
from toast.game import Game
from toast.emitter import Emitter
from toast.math.vector import Vector2D
from toast.gradient import Gradient
from toast.timer import Timer

import random
import pygame

from examples.demo_game import DemoGame

import psyco
psyco.full()

class DestroyAfter(Component):
    def __init__(self, milliseconds):
        super(DestroyAfter, self).__init__()
        self.__life_timer = Timer(milliseconds)
        
    def update(self, milliseconds=0):
        super(DestroyAfter, self).update(milliseconds)
            
        if self.__life_timer.is_time_up():
            self.__life_timer.reset()
            self.game_object.remove()

class Particle(Sprite):
    def __init__(self, image, lifetime):
        super(Particle, self).__init__(image)
        self.__velocity = Vector2D.from_angle(random.randrange(80, 100)) * -1.35
        
        sheet = ImageSheet(ResourceLoader.load('data//puffs.png'), (32, 32))
        
        puff = [(sheet[3], int(lifetime * 0.2)),
                (sheet[2], int(lifetime * 0.1)),
                (sheet[1], int(lifetime * 0.3)),
                (sheet[0], int(lifetime * 2.0))]
        
        self.animation = Animation('puff', puff)
        self.add(self.animation)
        self.add(DestroyAfter(lifetime))
        
    def update(self, milliseconds=0):
        super(Particle, self).update(milliseconds)
        
        self.position += self.__velocity * (milliseconds / 1000.0) * 60
            
class PuffEmitter(Emitter):
    def __init__(self, lifetime):
        super(PuffEmitter, self).__init__(Particle, (ImageSheet(ResourceLoader.load('data//puffs.png'), (32, 32))[3], 300), 20, self.onCreate)
        self.__counter = 0
        self.lifetime = lifetime
        self.position = Vector2D(0, 0)
        self.velocity = Vector2D(0, 0)
        
    def update(self, milliseconds=0):
        super(PuffEmitter, self).update(milliseconds)
        self.__counter += milliseconds
        
        gravity = 450.0
        self.velocity += (Vector2D(0, gravity) * (milliseconds / 1000.0))
        self.position += (self.velocity * (milliseconds / 1000.0))
        
        if self.__counter > self.lifetime:
            self.is_emitting = False
            
            if not self.has_child_alive():
                self.remove()
        
    def onCreate(self, emitter, particle):
        particle.position = Vector2D(emitter.position)
        particle.position += (random.random() - 0.5) * 2.0 * 8, (random.random() - 0.5) * 2.0 * 16
        particle.animation.play('puff', 0)

class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()
        EventManager.subscribe(self, 'onMouseDown')
        
        bg = Gradient.createVerticalGradient((20, 15), (255,255,255), (228, 139, 165), (111,86,117))
        bg = pygame.transform.scale(bg, (320, 240))
        self.add(Sprite(bg, (160, 120)))
        
    def onMouseDown(self, event):
        if event.button == 1:
            num_puffs = 8.0
            for i in range(int(num_puffs) + 1):
                theta = 0 + (360 * (i / num_puffs))
                
                e = PuffEmitter(2000)
                e.position = Vector2D(Game.camera_to_world(event.pos))
                e.velocity = Vector2D.from_angle(theta) * -180.0
                self.add(e)
        
game = DemoGame((640, 480), NewScene)
game.run()