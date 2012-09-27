from toast import Scene
from toast.sprite import Sprite
from toast.animation import Animation
from toast.image_sheet import ImageSheet
from toast.resource_loader import ResourceLoader
from toast.event_manager import EventManager
from toast.camera import Camera
from toast.emitter import Emitter

class Particle(Sprite):
    def __init__(self, image, lifetime):
        super(Particle, self).__init__(image)
        self.__counter = 0
        self.__lifetime = int(lifetime)
        
        sheet = ImageSheet(ResourceLoader.load('data//puffs.png'), (32, 32))
        
        puff = [(sheet[0], int(lifetime * 0.2)),
                (sheet[1], int(lifetime * 0.2)),
                (sheet[2], int(lifetime * 0.15)),
                (sheet[3], int(lifetime * 0.45))]
        
        self.animation = Animation('puff', puff)
        #animation.play()
        self.add(self.animation)
        
    def update(self, milliseconds=0):
        super(Particle, self).update(milliseconds)
        
        self.__counter += milliseconds
        
        if self.__counter > self.__lifetime:
            self.__counter = 0
            self.remove()

class NewScene(Scene):
    def initialize_scene(self):
        self.clear_color = 98, 186, 221
        self.resolution = 640, 480
        EventManager.subscribe(self, 'onMouseMotion')
        self.__cursor_pos = 0, 0
        
        self.emitter = Emitter(Particle, (ImageSheet(ResourceLoader.load('data//puffs.png'), (32, 32))[0], 100), 20, self.onCreate)
        self.add(self.emitter)
        
    def onMouseMotion(self, event):
        self.__cursor_pos = event.pos
            
    def onCreate(self, emitter, particle):
        particle.position = Camera.camera_to_world(self.__cursor_pos)
        particle.position -= 16, 16
        particle.animation.play('puff', 0)

s = NewScene()
s.run()
