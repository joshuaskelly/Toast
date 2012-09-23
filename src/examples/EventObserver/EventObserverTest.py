import pygame
from pygame.locals import K_ESCAPE, QUIT

from toast import Scene
from toast import EventManager

class EventSubscriber(object):
    def __init__(self):
        EventManager.subscribe(self, 'onMySpecialEvent')
        EventManager.subscribe(self, 'onKeyDown')
        EventManager.subscribe(self, 'onMouseDown')
        
    def onMouseDown(self, event):
        print event
        if event.button is 1:
            EventManager.notify('onMySpecialEvent', None)
        
    def onKeyDown(self, event):
        print event
        if event.key == K_ESCAPE:
            pygame.event.post(pygame.event.Event(QUIT))
            
    def onMySpecialEvent(self, event):
        print 'Called my special event!'

class NewScene(Scene):
    def initialize_scene(self):
        self.clear_color = (98, 186, 221)
        self.resolution = (640, 480)
        
        self.subscriber = EventSubscriber()

s = NewScene()

s.run()