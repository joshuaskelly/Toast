import pygame
from pygame.locals import *

from toast.physics import Physics

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

p = Physics()
p.name = 'Bob'

d = Physics()
print d.name

rect_list = []

rect_list.append(pygame.Rect(0, 220, 20, 20))

# Get the clock
clock = pygame.time.Clock()

offset = (0,0)

# Game loop
running = True
while running:
    # Cap the frames at 60 per second
    clock.tick(60)
    
    # Fill the buffer with blue
    buffer.fill((0,0,0))

    for rect in rect_list:
        pygame.draw.rect(buffer, (255, 0, 0), rect, 1)
        
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
            
