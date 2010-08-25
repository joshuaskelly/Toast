from toast.event_observer import EventObserver

import pygame

running = True

class subscriber(object):
    def __init__(self):
        pass
    
    def onMouseDown(self, event):
        print event
            
    def onKeyDown(self, event):
        if event.key == K_ESCAPE:
            pygame.event.post(pygame.event.Event(QUIT))
        
from pygame.locals import *

# Define the origin
ORIGIN = (0,0)
# Set the screen size
SCREEN_SIZE = (640,480)

# Setup pygame display
pygame.display.set_mode(SCREEN_SIZE)
# Get a surface the size of the window
screen = pygame.display.get_surface()
# Create a buffer to render to
buffer = pygame.Surface((80, 60))

clock = pygame.time.Clock()

key_observer = EventObserver("onKeyDown")
mouse_observer = EventObserver("onMouseDown")

s = subscriber()


key_observer.add(s)
mouse_observer.add(s)

while running:
    clock.tick(60)
    buffer.fill((0,0,0))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            key_observer.notify(event)
            
        elif event.type == MOUSEBUTTONDOWN:
            mouse_observer.notify(event)
            
        elif event.type == QUIT:
            running = False