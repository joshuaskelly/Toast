from toast import Scene
from toast.sprite import Sprite
from toast.resource_loader import ResourceLoader
from toast.event_manager import EventManager
from toast.game import Game
from toast.component_pool import ComponentPool

from examples.demo_game import DemoGame

class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()
        
        EventManager.subscribe(self, 'onMouseDown')
        
        self.pool = ComponentPool(Sprite, (ResourceLoader.load('data/crosshair.png'),), 10)
        self.add(self.pool)
        
    def onMouseDown(self, event):
        if event.button is 1:
            sprite = self.pool.getNextAvailable()
            sprite.position = Game.camera_to_world(event.pos)
            sprite.position -= 16, 16
            
game = DemoGame((640, 480), NewScene)
game.run()
