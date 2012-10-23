from toast.component import Component

class Scene(Component):
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
