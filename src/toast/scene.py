import pygame
from pygame.locals import DOUBLEBUF, HWSURFACE, KEYDOWN, KEYUP, \
MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT

from toast import EventManager
from toast import Camera
from toast.component import Component

class Scene(Component):
    currentScene = None
    
    def __init__(self):
        super(Scene, self).__init__()
        Scene.currentScene = self
    
        self.__clock = pygame.time.Clock()

        pygame.display.set_caption('Toast Window')
        
        self.__resolution = (320, 240)
        self.__flags = HWSURFACE | DOUBLEBUF
        pygame.display.set_mode(self.__resolution, self.__flags)
        
        self.__screen = pygame.display.get_surface()
        
        self.camera = Camera((320,240))
        self.camera.position = (160, 120)
    
        self.__running = True
        self.__frame_limit = 0
        
        self.__clear_color = (0,0,0)
        
        self.__frame_count = 0
        self.__msecs = 0
        
        self.initialize_scene()
    
    def get_clear_color(self):
        return self.__clear_color
    
    def set_clear_color(self, value):
        self.__clear_color = (value[0], value[1], value[2])
        self.camera.clear_color = self.__clear_color
    
    clear_color = property(get_clear_color, set_clear_color)
    
    @property
    def frame_limit(self):
        return self.__frame_limit
    
    @frame_limit.setter
    def frame_limit(self, value):
        self.__frame_limit = value
    
    def get_resolution(self):
        return self.__resolution
    
    def set_resolution(self, resolution):
        self.__resolution = resolution
        pygame.display.set_mode(resolution, self.__flags)
        
    resolution = property(get_resolution, set_resolution)
    
    def initialize_scene(self):
        raise
    
    def run(self):
        while self.__running:
            delta = self.__clock.tick(self.__frame_limit)
            
            self.__msecs += delta
            self.__frame_count += 1
            
            self.update(delta)
                    
            #self.__screen.fill(self.clear_color)
            self.camera.render(self.__screen)
            
            pygame.display.flip()
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
                
            elif event.type == 24:
                pygame.time.Clock().tick()
                
            elif event.type == QUIT:
                self.__running = False
                print "Average fps: " + str(self.__frame_count / (self.__msecs / 1000))
        