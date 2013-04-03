from toast.game_object import GameObject

class Scene(GameObject):
    __current_scene = None
    
    def __init__(self):
        super(Scene, self).__init__()
        
        if Scene.current_scene is None:
            Scene.current_scene = self

    @staticmethod      
    def get_current():
        return Scene.__current_scene
    
    @staticmethod
    def set_current(scene):
        Scene.__current_scene = scene
        
    current_scene = property(get_current, set_current)
    
    def render(self, surface, offset=(0,0)):
        for child in [c for c in self.children if hasattr(c, 'render')]:
            child.render(surface, offset)
