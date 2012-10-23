from toast import Scene

from examples.demo_game import DemoGame

class NewScene(Scene):
    def initialize_scene(self):
        pass

game = DemoGame((640, 480), NewScene)
game.run()
