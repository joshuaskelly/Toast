import pygame

from toast.scene_graph import GameObject
from toast.event_manager import EventManager
from toast.math import lerp
from toast.math.vector import Vector2D

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
        
        self.__position = Vector2D(0, 0)
        self.__viewport = pygame.Surface(resolution).convert()#.convert_alpha()
        self.__viewport.set_colorkey((255,0,255))
        self.__clear_color = None
        self.__tracking_strength = 0.1
        
        EventManager.subscribe(self, 'onCameraEvent')
        
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
        
    @property
    def top(self):
        return self.__position[1] - (self.__viewport.get_height() / 2)
    
    @property
    def left(self):
        return self.__position[0] - (self.__viewport.get_width() / 2)
    
    @property
    def width(self):
        return self.__viewport.get_width()
    
    @property
    def height(self):
        return self.__viewport.get_height()
        
    def get_position(self):
        return self.__position

    def set_position(self, value):
        self.__position = Vector2D(value[0], value[1])

    position = property(get_position, set_position)
    
    @property
    def bounds(self):
        return self.left, self.top, self.width, self.height
    
    def get_viewport_size(self):
        return self.__viewport

    def set_viewport_size(self, dimension):
        self.__viewport = pygame.Surface((dimension[0], dimension[1]), pygame.SRCALPHA, 32)

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

        position = (self.__position[0] - self.__viewport.get_width() / 2,
                    self.__position[1] - self.__viewport.get_height() / 2)
        
        # Render and scale scene
        scene.render(render_target, (int(position[0]), int(position[1])))
        pygame.transform.scale(render_target, surface.get_size(), surface)
