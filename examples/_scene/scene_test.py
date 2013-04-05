from toast.scene_graph import Scene

from examples.demo_game import DemoGame

class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()

game = DemoGame((640, 480), NewScene)
game.run()
