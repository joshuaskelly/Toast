import toast
from toast import Scene

class NewScene(Scene):
    def initialize_scene(self):
        level = toast.Level('Data/map.tmx')
        self.add(level)
        
        self.clear_color = (98, 186, 221)
        self.resolution = (640, 480)
        
        self.camera = level.get_element_by_ID('default camera')
    

s = NewScene()

s.run()