from toast.scene import Scene
from toast.game import Game
from toast.camera import Camera
from toast.event_manager import EventManager
from toast.sprite import Sprite
from toast.resource_loader import ResourceLoader

from examples.demo_game import DemoGame

class Crosshair(Sprite):
    def __init__(self, image_or_animation):
        super(Crosshair, self).__init__(image_or_animation)
        EventManager.subscribe(self, 'onMouseDown')
        
    def onMouseDown(self, event):
        if event.button is 3:
            self.remove()

class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()
        
        c = Crosshair(ResourceLoader.load('data//crosshair.png'))
        c.position = Camera.current_camera.position
        Camera.current_camera.clear_color = 255, 255, 255
        
        self.add(c)
        
        EventManager.subscribe(self, 'onMouseDown')
        
    def onMouseDown(self, event):
        if event.button is 1:
            Camera.current_camera.target = Game.camera_to_world(event.pos)
            
            c = Crosshair(ResourceLoader.load('data//crosshair.png'))
            c.position = Game.camera_to_world(event.pos)
            c.position -= 16, 16
            self.add(c)

game = DemoGame((640, 480), NewScene)
game.run()