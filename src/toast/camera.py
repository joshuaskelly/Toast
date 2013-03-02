import pygame

from toast.game_object import GameObject
from toast.camera_effects.shake_effect import ShakeEffect
from toast.event_manager import EventManager
from toast.math.math_helper import MathHelper
from toast.math.vector2D import Vector2D

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
        self.__target = None
        self.__bounds = None
        self.__tracking_strength = 0.1
        
        EventManager.subscribe(self, 'onCameraEvent')
        
    def get_target(self):
        return self.__target
        
    def set_target(self, target):
        self.__target = target
        
    target = property(get_target, set_target)
    
    @staticmethod
    def get_current():
        return Camera.__current_camera
    
    @staticmethod
    def set_current(camera):
        Camera.__current_camera = camera
        
    current_camera = property(get_current, set_current)

    @property
    def top_left(self):
        return (self.__position[0] - (self.__viewport.get_width() / 2),
                self.__position[1] - (self.__viewport.get_height() / 2))
        
    def get_position(self):
        return self.__position

    def set_position(self, value):
        self.__position = Vector2D(value[0], value[1])

    position = property(get_position, set_position)
    
    def get_bounds(self):
        return self.__bounds
    
    def set_bounds(self, value):
        if value != None:
            self.__bounds = pygame.Rect(value[0], value[1], value[2], value[3])
        else:
            self.__bounds = None

    bounds = property(get_bounds, set_bounds)
    
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

    def update(self, delta):
        if self.target != None:
            dest = None
            
            try:
                dest = self.target.position
            except:
                dest = self.target
                
            self.position = MathHelper.Lerp(self.position, dest, self.__tracking_strength * (delta / 1000.0) * 60)
                
        self.handle_out_of_bounds()
        
        super(Camera, self).update(delta)
        
    def handle_out_of_bounds(self):
        if self.bounds != None:
            rect = self.viewport.get_rect()
            rect.center = self.position
            
            if rect.left < self.bounds.left:
                rect.left = self.bounds.left
                self.position = rect.center
                
            elif rect.right > self.bounds.right:
                rect.right = self.bounds.right
                self.position = rect.center
                
            if rect.top < self.bounds.top:
                rect.top = self.bounds.top
                self.position = rect.center
            
            elif rect.bottom > self.bounds.bottom:
                rect.bottom = self.bounds.bottom
                self.position = rect.center
        
    def renderScene(self, surface, scene):
        """
        " * Camera.renderScene
        """
        
        render_target = self.__viewport
        
        if self.clear_color:
            render_target.fill(self.clear_color)

        position = (self.__position[0] - self.__viewport.get_width() / 2,
                    self.__position[1] - self.__viewport.get_height() / 2)
        
        for element in scene.children:
            if hasattr(element, 'render'):
                element.render(render_target, (int(position[0]), int(position[1])))

        SCREEN_SIZE = (surface.get_width(), surface.get_height())

        pygame.transform.scale(render_target, SCREEN_SIZE, surface)
            
    def onCameraEvent(self, event):
        if event.action == 'set_target':
            self.__target = event.target
            
        elif event.action == 'effect':
            if event.effect == 'shake':
                e = ShakeEffect(self, event.magnitude, event.duration)
                
                self.add(e)
