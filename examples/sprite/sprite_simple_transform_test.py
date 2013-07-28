from toast.scene_graph import Scene
from toast.sprite import Sprite
from toast.resource_loader import ResourceLoader
from toast.animation import Animation
from toast.image_sheet import ImageSheet
from toast.camera import Camera

from examples.demo_game import DemoGame

class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()
        
        Camera.current_camera.clear_color = 20, 12, 28
        
        dimension = 32, 37
        data = ResourceLoader.load('data//player_run.png')
        sheet = ImageSheet(data, dimension)
        
        interval = 60

        run = [(sheet[i], interval) for i in range(8)]
        
        parent = Sprite(Animation('run_cycle', run))
        parent.transform.position = 160, 120
        
        child = Sprite(Animation('run_cycle', run))
        child.transform.position = 32, 32
        parent.add(child)
        
        self.add(parent)

game = DemoGame((640, 480), NewScene)
game.run()
