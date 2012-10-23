from toast.component import Component
from toast.transform import Transform
from toast.decorators.memoize import memoize

class Sprite(Component):
    def __init__(self, image_or_animation, position=(0,0)):
        super(Sprite, self).__init__()
        
        self.add(Transform())
        self.transform.position = position
        
        self.__image = None
        self.__animation = None
        
        if hasattr(image_or_animation, 'add_animation'):
            self.__animation = image_or_animation
            self.add(image_or_animation)
            self.image = self.__animation.get_current_frame()
        else:
            self.image = image_or_animation
        
    @property
    @memoize
    def transform(self):
        return self.get_component('Transform')
        
    @property
    def position(self):
        return self.transform.position
        
    @position.setter
    def position(self, value):
        self.transform.position = value
        
    @property
    def image(self):
        return self.__image
    
    @image.setter
    def image(self, image):
        self.__image = image
        
    def render(self, surface, offset=(0,0)):
        for child in self.children:
            if hasattr(child, 'render'):
                child.render(surface, offset)
                
        surface.blit(self.image, self.position - offset)
