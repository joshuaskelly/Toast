import pygame

from toast.scene_graph import GameObject
from toast.math.vector import Vector2D

from toast.fast_transform import Transform

class Camera(GameObject):
    __current_camera = None

    def __init__(self, resolution):
        """
        " * Class Constructor
        " *    imageSheet:   An ImageSheet object.
        " *    data:         A two dimensional array.
        """
        super(Camera, self).__init__()
        Camera.current_camera = self
        
        self.__viewport = pygame.Surface(resolution).convert()#.convert_alpha()
        self.__viewport.set_colorkey((255,0,255))
        self.__clear_color = None
        
        self.add(Transform())
        
    @property
    def transform(self):
        return self.get_component('Transform')    
    
    @staticmethod
    def get_current():
        return Camera.__current_camera
    
    @staticmethod
    def set_current(camera):
        Camera.__current_camera = camera
        
    current_camera = property(get_current, set_current)

    @property
    def top_left(self):
        return self.left, self.top
    
    @top_left.setter
    def top_left(self, pos):
        self.position = pos[0] + self.width / 2, pos[1] + self.height / 2
        
    @property
    def top(self):
        return self.position[1] - (self.__viewport.get_height() / 2)
    
    @property
    def left(self):
        return self.position[0] - (self.__viewport.get_width() / 2)
    
    @property
    def width(self):
        return self.__viewport.get_width()
    
    @property
    def height(self):
        return self.__viewport.get_height()
        
    @property
    def position(self):
        return self.transform.position
    
    @position.setter
    def position(self, other):
        self.transform.position = other
    
    @property
    def bounds(self):
        return self.left, self.top, self.width, self.height
    
    def get_viewport_size(self):
        return self.__viewport

    def set_viewport_size(self, dimension):
        self.__viewport = pygame.Surface(dimension).convert()

    viewport = property(get_viewport_size, set_viewport_size)
    
    def get_clear_color(self):
        return self.__clear_color

    def set_clear_color(self, value):
        self.__clear_color = (value[0], value[1], value[2])

    clear_color = property(get_clear_color, set_clear_color)

    def update(self, milliseconds=0):
        super(Camera, self).update(milliseconds)
        
    def render_scene(self, surface, scene):
        
        render_target = self.__viewport
        
        if self.clear_color:
            render_target.fill(self.clear_color)

        position = (self.position[0] - self.__viewport.get_width() / 2,
                    self.position[1] - self.__viewport.get_height() / 2)
        
        # Render and scale scene
        scene.render(render_target, (int(position[0]), int(position[1])))
        pygame.transform.scale(render_target, surface.get_size(), surface)
