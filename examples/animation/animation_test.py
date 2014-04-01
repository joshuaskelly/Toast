from toast.scene_graph import Scene
from toast.image_sheet import ImageSheet
from toast.sprite import Sprite
from toast.resource_loader import ResourceLoader
from toast.animation import Animation

from examples.demo_game import DemoGame

class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()
        
        dimension = (32, 37)
        data = ResourceLoader.load('data//player_run.png')
        sheet = ImageSheet(data, dimension)
        
        interval = 80

        run = [(sheet[i], interval) for i in range(8)]
        
        for i in range(8):
            animation = Animation('run_cycle', run)
            animation.play('run_cycle', i)
            
            staticSprite = Sprite(sheet[i])
            staticSprite.position = (i + 1) * 32 + 16, 84
            self.add(staticSprite)
            
            animatedSprite = Sprite(animation)
            animatedSprite.position = (i + 1) * 32 + 16, 148
            self.add(animatedSprite)

game = DemoGame((640, 480), NewScene)
game.run()