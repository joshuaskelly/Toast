from toast import Scene
from toast.camera import Camera
from toast.event_manager import EventManager
from toast.sprite import Sprite
from toast.resource_loader import ResourceLoader

class Crosshair(Sprite):
    def __init__(self, image_or_animation):
        super(Crosshair, self).__init__(image_or_animation)
        EventManager.subscribe(self, 'onMouseDown')
        
    def onMouseDown(self, event):
        if event.button is 3:
            self.remove()

class NewScene(Scene):
    def initialize_scene(self):
        self.clear_color = (98, 186, 221)
        self.resolution = (640, 480)
        
        c = Crosshair(ResourceLoader.load('data//crosshair.png'))
        c.position = self.camera.position
        self.add(c)
        
        EventManager.subscribe(self, 'onMouseDown')
        
    def onMouseDown(self, event):
        if event.button is 1:
            self.camera.target = Camera.camera_to_world(event.pos)
            
            c = Crosshair(ResourceLoader.load('data//crosshair.png'))
            c.position = Camera.camera_to_world(event.pos)
            c.position -= 16, 16
            self.add(c)

s = NewScene()

s.run()