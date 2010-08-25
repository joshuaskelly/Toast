import toast
from toast import Scene

class NewScene(Scene):
    def initialize_scene(self):
        level = toast.Level('Data/map.xml')
        self.scene_root.append(level)
        
        self.clear_color = (98, 186, 221)
        self.resolution = (640, 480)
    

s = NewScene()

s.run()