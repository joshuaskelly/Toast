from toast.scene_graph import Scene, Component
from toast.game import Game
from toast.camera import Camera
from toast.event_manager import EventManager
from toast.sprite import Sprite
from toast.resource_loader import ResourceLoader
from toast.math.vector import Vector2D
from toast.math import lerp

from examples.demo_game import DemoGame

class Crosshair(Sprite):
    def __init__(self, image_or_animation):
        super(Crosshair, self).__init__(image_or_animation)
        EventManager.subscribe(self, 'onMouseDown')
        
    def onMouseDown(self, event):
        if event.button is 3:
            self.remove()
            
class CameraTrackingBehavior(Component):
    def __init__(self):
        super(CameraTrackingBehavior, self).__init__()
        self.__target = Vector2D.Zero()
        self.tracking_strength = 0.0125
        
    def update(self, milliseconds=0):
        self.game_object.transform.position = lerp(self.game_object.transform.position, self.__target, self.tracking_strength)
        
    @property
    def target(self):
        return self.__target
    
    @target.setter
    def target(self, other):
        self.__target = Vector2D(other[0], other[1])

class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()
        EventManager.subscribe(self, 'onMouseDown')
        
        Camera.current_camera.clear_color = 0, 0, 0
        
        tracker = CameraTrackingBehavior()
        Camera.current_camera.add(tracker)
        
    def onMouseDown(self, event):
        if event.button is 1:
            Camera.current_camera.get_component('CameraTrackingBehavior').target = Game.camera_to_world(event.pos)
            
            c = Crosshair(ResourceLoader.load('data//crosshair.png'))
            c.position = Game.camera_to_world(event.pos)
            self.add(c)

game = DemoGame((640, 480), NewScene)
game.run()