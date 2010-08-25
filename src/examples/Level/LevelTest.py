import pygame
from pygame.locals import *

import toast

# Define the origin
ORIGIN = (0,0)
# Set the screen size
SCREEN_SIZE = (640, 480)

# Setup pygame display
pygame.display.set_mode(SCREEN_SIZE)
# Get a surface the size of the window
screen = pygame.display.get_surface()
# Create a buffer to render to
buffer = pygame.Surface((320, 240))

# Create a level from an xml file
level = toast.Level('Data/map.xml')

# Get the clock
clock = pygame.time.Clock()

offset = (0,0)

# Game loop
running = True
while running:
    # Cap the frames at 60 per second
    clock.tick(60)
    
    # Fill the buffer with blue
    buffer.fill((98,186,221))
    
    # Draw the level
    level.render(buffer, offset)
    offset = (offset[0] + 1, 0)
        
    # Scale up buffer and draw to screen
    screen.blit(pygame.transform.scale(buffer,SCREEN_SIZE), pygame.Rect(ORIGIN,SCREEN_SIZE))
    pygame.display.flip()
    
    # Handle input
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                
        elif event.type == QUIT:
            running = False