from toast import Scene

class NewScene(Scene):
    def initialize_scene(self):
        self.clear_color = (98, 186, 221)
        self.resolution = (640, 480)

s = NewScene()

s.run()