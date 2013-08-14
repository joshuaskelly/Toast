import pygame

from toast.scene_graph import GameObject
from toast.fast_transform import Transform
from toast.math.vector import Vector2D

class Sprite(GameObject):
    def __init__(self, image_or_animation, position=(0,0)):
        super(Sprite, self).__init__()
        
        self.add(Transform())
        self.transform.position = position
        
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
    
    def change_transform_type(self, new_type):
        x, y = self.transform.position
        self.remove(self.transform)
        
        t = new_type()
        t.position = x, y
        
        self.add(t)
        
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
        # If not visible, don't draw
        if not self.visible:
            return
        
        image = self.image
        w, h = image.get_size()
        
        # Handle scaling if needed
        if self.transform.scale != (1, 1):
            sw = self.transform.scale[0] * w
            sh = self.transform.scale[1] * h
            image = pygame.transform.scale(image, (int(sw), int(sh)))
        
        # Handle rotation if needed
        if self.transform.rotation:
            image = pygame.transform.rotate(image, int(-self.transform.rotation))
            
        # Calculate center
        hw, hh = image.get_size()
        hw = hw / 2
        hh = hh / 2
        
        pos = Vector2D(int(self.transform.position[0]), int(self.transform.position[1]))
        
        # Draw image to surface
        surface.blit(image, pos - (hw, hh) - offset)
        
        # Draw children
        for child in [c for c in self.children if hasattr(c, 'render')]:
                child.render(surface, offset)
