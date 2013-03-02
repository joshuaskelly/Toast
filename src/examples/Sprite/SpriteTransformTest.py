from toast.scene import Scene
from toast.image_sheet import ImageSheet
from toast.sprite import Sprite
from toast.resource_loader import ResourceLoader
from toast.event_manager import EventManager
from toast.camera import Camera

from examples.demo_game import DemoGame

class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()
        EventManager.subscribe(self, 'onMouseMotion')
        
        Camera.current_camera.clear_color = 98, 186, 221
        
        dimension = 32, 37
        data = ResourceLoader.load('data//player_run.png')
        sheet = ImageSheet(data, dimension)
        
        self.sprite = Sprite(sheet[0])
        self.add(self.sprite)
        
        # Add a child sprite to self.sprite's local space
        self.sprite.add(Sprite(sheet[4], (32, 32)))
        
    def onMouseMotion(self, event):
        self.sprite.transform.position = DemoGame.camera_to_world(event.pos)

game = DemoGame((640, 480), NewScene)
game.run()
