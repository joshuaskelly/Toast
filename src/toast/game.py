import pygame
from pygame.locals import DOUBLEBUF, FULLSCREEN, HWSURFACE, KEYDOWN, KEYUP, \
MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT

from toast.camera import Camera
from toast.scene import Scene
from toast.event_manager import EventManager

class Game(object):
    game_instance = None
    
    def __init__(self, resolution, initial_scene):
        if Game.game_instance is not None:
            raise GameException('Can not instantiate more than one instance of Game object')
        
        Game.game_instance = self
        
        self.__clock = pygame.time.Clock()
        pygame.display.set_caption('Toast Window')
        
        self.__resolution = resolution
        self.__flags = DOUBLEBUF #| HWSURFACE | FULLSCREEN
        pygame.display.set_mode(self.__resolution, self.__flags)
        
        pygame.mouse.set_visible(False)
        
        self.__screen = pygame.display.get_surface()
        self.camera = Camera((320,240))
        self.camera.position = (160, 120)
        
        Scene.current_scene = initial_scene()
        
        self.__running = True
        self.__frame_limit = 0
        
        self.__clear_color = (0,0,0)
        
        self.__frame_count = 0
        self.__msecs = 0
        
    @property
    def frame_limit(self):
        return self.__frame_limit
    
    @frame_limit.setter
    def frame_limit(self, max_fps):
        self.__frame_limit = max_fps
        
    @property
    def fullscreen(self):
        return (self.__flags & (HWSURFACE | FULLSCREEN)) != 0
    
    @fullscreen.setter
    def fullscreen(self, is_fullscreen):
        if is_fullscreen:
            self.__flags = self.__flags | (HWSURFACE | FULLSCREEN)
        else:
            self.__flags = self.__flags ^ (HWSURFACE | FULLSCREEN)
            
        pygame.display.set_mode(self.resolution, self.__flags)
        
    @property
    def resolution(self):
        return self.__resolution
    
    @resolution.setter
    def resolution(self, resolution):
        self.__resolution = resolution
        pygame.display.set_mode(resolution, self.__flags)
        
    def run(self):
        while self.__running:
            delta = self.__clock.tick(self.frame_limit)
            
            self.__msecs += delta
            self.__frame_count += 1
            
            camera = Camera.current_camera
            scene = Scene.current_scene
           
            camera.update(delta)
            scene.update(delta)

            camera.renderScene(self.__screen, scene)

            pygame.display.update()
            pygame.display.set_caption('Toast Window: %d fps' % self.__clock.get_fps())
            
            self.__handle_events()
                    
    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                EventManager.notify('onKeyDown', event)
                
            elif event.type == KEYUP:
                EventManager.notify('onKeyUp', event)
                
            elif event.type == MOUSEMOTION:
                EventManager.notify('onMouseMotion', event)
                
            elif event.type == MOUSEBUTTONDOWN:
                EventManager.notify('onMouseDown', event)
                
            elif event.type == MOUSEBUTTONUP:
                EventManager.notify('onMouseUp', event)
                
            elif event.type == QUIT:
                self.__running = False
                print "Average fps: " + str(self.__frame_count / (self.__msecs / 1000))
                
    @staticmethod
    def camera_to_world(coord):
        camera = Camera.current_camera
        viewport = Game.game_instance.resolution
        
        scale_x = 1.0 * camera.viewport.get_width() / viewport[0]
        scale_y = 1.0 * camera.viewport.get_height() / viewport[1]
        return (camera.position[0] + (coord[0] * scale_x) - (camera.viewport.get_width() / 2), 
                camera.position[1] + (coord[1] * scale_y) - (camera.viewport.get_height() / 2))
    
    @staticmethod
    def world_to_camera(coord):
        camera = Camera.current_camera
        viewport = Game.game_instance.resolution
        
        scale_x = 1.0 * camera.viewport.get_width() / viewport[0]
        scale_y = 1.0 * camera.viewport.get_height() / viewport[1]
        return (((camera.viewport.get_width() / 2) - camera.position[0] - coord[0]) / -scale_x, 
                (camera.position[1] - coord[1] - (camera.viewport.get_height() / 2)) / -scale_y)
        
class GameException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)