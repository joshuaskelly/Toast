from toast import Scene

class NewScene(Scene):
    def initialize_scene(self):
        self.clear_color = (98, 186, 221)
        self.resolution = (640, 480)
        
        #TODO: JOSHUA: Add something renderable to the scene.

s = NewScene()

s.run()