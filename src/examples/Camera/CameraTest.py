import pygame
from pygame.locals import *

import toast

try:
    import psyco
    psyco.full()
except:
    raise 'Psyco not found.'

# Define the origin
ORIGIN = (0, 0)
# Set the screen size
SCREEN_SIZE = (640, 480)

# Setup pygame display
pygame.display.set_mode(SCREEN_SIZE)

# Get a surface the size of the window
screen = pygame.display.get_surface()

# Create a level from an xml file
level = toast.Level('Data/map.tmx')

# Create a camera to render our scene
camera = level.get_element_by_ID('default camera')
# Add the level to the render list of the camera
camera.add_renderable(level)
camera.clear_color = (98, 186, 221)

position = camera.position

# Get the clock
clock = pygame.time.Clock()

offset = (0, 0)

# Game loop
running = True
while running:
    # Cap the frames at 60 per second
    clock.tick(60)
    
    screen.fill((98,186,221))
    
    camera.render(screen)
    position = (position[0] + 1, position[1])
    camera.position = position
    
    pygame.display.flip()
    
    # Handle input
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                
        elif event.type == MOUSEMOTION:
            scale = event.pos[0]
            camera.viewport = (scale, scale * 3/4)
                
        elif event.type == QUIT:
            running = False