import pygame

import toast
from toast.gui.percent_bar import PercentBar
from toast.math.math_helper import MathHelper

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

data = pygame.image.load('Data/bar.png')
sheet = toast.ImageSheet(data, (51, 8))

bar1 = PercentBar(sheet[0], sheet[3])
bar2 = PercentBar(sheet[1], sheet[4])
bar2.position = (0, 9)
bar3 = PercentBar(sheet[2], sheet[5])
bar3.position = (0, 18)

x = 0
y = 0

step = 0.1

# Game loop
running = True
while running:
    clock.tick(60)
    buffer.fill((0,0,0))
    
    bar1.render(buffer)
    bar2.render(buffer)
    bar3.render(buffer)
    
    # Scale up buffer and draw to screen
    screen.blit(pygame.transform.scale(buffer,SCREEN_SIZE),pygame.Rect(ORIGIN,SCREEN_SIZE))
    pygame.display.flip()

    # Handle input
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            x, y = event.pos[0], event.pos[1]
            x = x / float(SCREEN_SIZE[0])
            y = y / float(SCREEN_SIZE[1])
            

            
        elif event.type == QUIT:
            running = False
            
    bar1.current = MathHelper.Lerp(bar1.current, x, step)
    bar2.current = MathHelper.Lerp(bar2.current, y, step)
    bar3.current = MathHelper.Lerp(bar3.current, (x + y) / 2.0, step)