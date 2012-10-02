from toast import Scene
from toast.sprite import Sprite
from toast.animation import Animation
from toast.image_sheet import ImageSheet
from toast.resource_loader import ResourceLoader
from toast.event_manager import EventManager
from toast.camera import Camera
from toast.emitter import Emitter
from toast.math.vector2D import Vector2D
import random

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

class NewScene(Scene):
    def initialize_scene(self):
        self.clear_color = 33, 33, 33
        self.resolution = 640, 480
        EventManager.subscribe(self, 'onMouseMotion')
        
        self.emitter = Emitter(Particle, (ImageSheet(ResourceLoader.load('data//puffs.png'), (32, 32))[0], 1000), 40, self.onCreate)
        self.add(self.emitter)
        
        e = Emitter(Particle, (ImageSheet(ResourceLoader.load('data//puffs.png'), (32, 32))[0], 1000), 40, self.onCreate)
        e.position = 32, 208
        self.add(e)
        
        f = Emitter(Particle, (ImageSheet(ResourceLoader.load('data//puffs.png'), (32, 32))[0], 1000), 40, self.onCreate)
        f.position = 288, 208
        self.add(f)
        
    def onMouseMotion(self, event):
        self.emitter.position = Camera.camera_to_world(event.pos)
            
    def onCreate(self, emitter, particle):
        particle.position = Vector2D(emitter.position) - (16, 16)
        particle.position += (random.random() - 0.5) * 2.0 * 8, (random.random() - 0.5) * 2.0 * 16
        particle.animation.play('puff', 0)
        if (random.random() < 0.3):
            particle.lifetime = random.randint(1000, 1800)

s = NewScene()
s.run()