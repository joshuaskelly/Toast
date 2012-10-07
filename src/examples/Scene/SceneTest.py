from toast import Scene

from examples.demo_game import DemoGame

class NewScene(Scene):
    def initialize_scene(self):
        self.clear_color = (98, 186, 221)
        self.resolution = (640, 480)

game = DemoGame((640, 480), NewScene)
game.run()
