# 86 fps 10/27/2012
#106 fps 3/1/2013

from toast.scene import Scene
from toast.sprite import Sprite
from toast.animation import Animation
from toast.component import Component
from toast.image_sheet import ImageSheet
from toast.resource_loader import ResourceLoader
from toast.emitter import Emitter
from toast.math.vector2D import Vector2D
from toast.gradient import Gradient

import random
import pygame

import psyco
psyco.full()

from examples.demo_game import DemoGame

class EndGameAfter(Component):
    def __init__(self, milliseconds=0):
        super(EndGameAfter, self).__init__()
        self.__counter = 0;
        self.__lifetime = milliseconds
        
    def update(self, milliseconds=0):
        super(EndGameAfter, self).update(milliseconds)
        
        self.__counter += milliseconds
        
        if self.__counter > self.__lifetime:
            pygame.event.post(pygame.event.Event(pygame.locals.QUIT))

class Particle(Sprite):
    def __init__(self, image, lifetime):
        super(Particle, self).__init__(image)
        self.__counter = 0
        self.lifetime = int(lifetime)
        self.__velocity = Vector2D.UnitVectorFromAngle(random.randrange(80.0, 100.0)) * -1.65
        
        sheet = ImageSheet(ResourceLoader.load('data//puffs.png'), (32, 32))
        
        puff = [(sheet[0], int(lifetime * 0.1)),
                (sheet[1], int(lifetime * 0.15)),
                (sheet[2], int(lifetime * 0.3)),
                (sheet[3], int(lifetime * 2.0))]
        
        self.animation = Animation('puff', puff)
        self.add(self.animation)
        
    def update(self, milliseconds=0):
        super(Particle, self).update(milliseconds)
        
        self.position += self.__velocity * (milliseconds / 1000.0) * 60
        self.__counter += milliseconds
        
        if self.__counter > self.lifetime:
            self.__counter = 0
            self.remove()

class EmitterPerformanceTest(Scene):
    def __init__(self):
        super(EmitterPerformanceTest, self).__init__()
        
        bg = Gradient.createVerticalGradient((20, 15), (255,255,255), (228, 139, 165), (111,86,117))
        bg = pygame.transform.scale(bg, (320, 240))
        self.add(Sprite(bg))
        
        num_emitters = 8
        for i in range(num_emitters):
            e = Emitter(Particle, (ImageSheet(ResourceLoader.load('data//puffs.png'), (32, 32))[0], 1000), 40, self.onCreate)
            e.position = 32 + (i * (256 / (num_emitters - 1))), 208
            self.add(e)
        
        self.add(EndGameAfter(1000 * 30))
        
    def onCreate(self, emitter, particle):
        particle.position = Vector2D(emitter.position) - (16, 16)
        particle.position += (random.random() - 0.5) * 2.0 * 8, (random.random() - 0.5) * 2.0 * 16
        particle.animation.play('puff', 0)
        if (random.random() < 0.3):
            particle.lifetime = random.randint(1000, 1800)

game = DemoGame((640, 480), EmitterPerformanceTest)
game.run()
