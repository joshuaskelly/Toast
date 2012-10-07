import pygame
from pygame.locals import K_ESCAPE, QUIT

from toast import Scene
from toast import EventManager

from examples.demo_game import DemoGame

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
    def __init__(self):
        super(NewScene, self).__init__()
        
        self.subscriber = EventSubscriber()

game = DemoGame((640, 480), NewScene)
game.run()
