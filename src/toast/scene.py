import pygame
from pygame.locals import *

import toast
from toast import EventObserver
from toast import Camera
from toast.component import Component

class Scene(Component):
    def __init__(self):
        super(Scene, self).__init__()
        
        self.__keypress_observer      = EventObserver("key_press")
        self.__keyrelease_observer    = EventObserver("key_release")
        self.__mouse_press_observer   = EventObserver("mouse_press")
        self.__mouse_release_observer = EventObserver("mouse_release")
        self.__mouse_motion_observer  = EventObserver("mouse_motion")
    
        self.__clock = pygame.time.Clock()

        pygame.display.set_caption('Toast Window')
        
        self.__resolution = (320, 240)
        self.__flags = HWSURFACE | DOUBLEBUF
        pygame.display.set_mode(self.__resolution, self.__flags)
        
        self.__screen = pygame.display.get_surface()
        
        self.camera = Camera((320,240))
        self.camera.position = (160, 120)
    
        self.__running = True
        
        self.__clear_color = (0,0,0)
        
        self.__frame_count = 0
        self.__msecs = 0
        
        self.initialize_scene()
        
        for element in self:
            self.camera.add_renderable(element)
    
    def get_clear_color(self):
        return self.__clear_color
    
    def set_clear_color(self, value):
        self.__clear_color = (value[0], value[1], value[2])
        self.camera.clear_color = self.__clear_color
    
    clear_color = property(get_clear_color, set_clear_color)
    
    def get_resolution(self):
        return self.__resolution
    
    def set_resolution(self, resolution):
        self.__resolution = resolution
        pygame.display.set_mode(resolution, self.__flags)
        
    resolution = property(get_resolution, set_resolution)
    
    def initialize_scene(self):
        raise
        
    def add_keyboard_listener(self, listener):
        self.__keypress_observer.add(listener)
        self.__keyrelease_observer.add(listener)
    
    def add_mouse_motion_listener(self, listener):
        self.__mouse_motion_observer.add(listener)
        
    def add_mouse_button_listener(self, listener):
        self.__mouse_press_observer.add(listener)
        self.__mouse_release_observer.add(listener)
        
    def update(self, delta):
        for entity in self:
            if hasattr(entity, 'update'):
                entity.update(delta)
    
    def run(self):
        while self.__running:
            delta = self.__clock.tick()
            
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
                self.__keypress_observer.notify(event)
                
            elif event.type == KEYUP:
                self.__keyrelease_observer.notify(event)
                
            elif event.type == MOUSEMOTION:
                self.__mouse_motion_observer.notify(event)
                
            elif event.type == MOUSEBUTTONDOWN:
                self.__mouse_press_observer.notify(event)
                
            elif event.type == MOUSEBUTTONUP:
                self.__mouse_release_observer.notify(event)
                
            elif event.type == USEREVENT:
                self.__handle_user_events(event)
                
            elif event.type == QUIT:
                self.__running = False
                print "Average fps: " + str(self.__frame_count / (self.__msecs / 1000))
                
    def __handle_user_events(self, event):
        if event.user_type == 'CAMERAEVENT':
            self.camera.notify_event(event)
        