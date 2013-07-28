from toast.scene_graph import GameObject
from toast.fast_transform import Transform

class Sprite(GameObject):
    def __init__(self, image_or_animation, position=(0,0)):
        super(Sprite, self).__init__()
        
        self.add(Transform(*position))
        
        self.__image = None
        self.__animation = None
        self.__visibility = True
        
        if hasattr(image_or_animation, 'add_animation'):
            self.__animation = image_or_animation
            self.add(image_or_animation)
            self.image = self.__animation.get_current_frame()
        else:
            self.image = image_or_animation
        
    @property
    def transform(self):
        return self.get_component('Transform')
        
    @property
    def position(self):
        return self.transform.position
        
    @position.setter
    def position(self, value):
        self.transform.position = value
        
    @property
    def visible(self):
        return self.__visibility
    
    @visible.setter
    def visible(self, value):
        self.__visibility = value
        
    @property
    def image(self):
        return self.__image
    
    @image.setter
    def image(self, image):
        self.__image = image
        
    def render(self, surface, offset=(0,0)):
        if not self.visible:
            return
        
        surface.blit(self.image, self.position - offset)
        
        for child in [c for c in self.children if hasattr(c, 'render')]:
                child.render(surface, offset)
