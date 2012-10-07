import pygame
from pygame.locals import K_f, K_ESCAPE, QUIT

from toast.game import Game
from toast.event_manager import EventManager

class DemoGame(Game):
    def __init__(self, resolution, initial_scene):
        super(DemoGame, self).__init__(resolution, initial_scene)
        
        EventManager.subscribe(self, 'onKeyDown')
        
    def onKeyDown(self, event):
        if event.key == K_f:
            self.fullscreen = not self.fullscreen
            
        elif event.key == K_ESCAPE:
            pygame.event.post(pygame.event.Event(QUIT))
