from toast import Scene
from toast.sprite import Sprite
from toast.resource_loader import ResourceLoader
from toast.event_manager import EventManager
from toast.camera import Camera
from toast.component_pool import ComponentPool

class NewScene(Scene):
    def initialize_scene(self):
        self.clear_color = 98, 186, 221
        self.resolution = 640, 480
        EventManager.subscribe(self, 'onMouseDown')
        
        self.pool = ComponentPool(Sprite, (ResourceLoader.load('data/crosshair.png'),), 10)
        self.add(self.pool)
        
    def onMouseDown(self, event):
        if event.button is 1:
            sprite = self.pool.getNextAvailable()
            sprite.position = Camera.camera_to_world(event.pos)
            sprite.position -= 16, 16
            
s = NewScene()
s.run()
