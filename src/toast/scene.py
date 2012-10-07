from toast.component import Component

class Scene(Component):
    currentScene = None
    
    def __init__(self):
        super(Scene, self).__init__()
        
        if Scene.currentScene is None:
            Scene.currentScene = self
