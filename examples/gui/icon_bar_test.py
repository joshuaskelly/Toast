import pygame

from toast.image_sheet import ImageSheet
from toast.gui.icon_bar import IconBar

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
buffer = pygame.Surface((160,120))

clock = pygame.time.Clock()

data = pygame.image.load('Data/hud.png').convert()
data.set_colorkey((255, 0, 255))

sheet = ImageSheet(data, (16, 13))

bar = IconBar(6, sheet[0], sheet[1])
bar.spacing = 6


# Game loop
running = True
while running:
    clock.tick(60)
    buffer.fill((0,0,0))
    
    bar.render(buffer)
    
    # Scale up buffer and draw to screen
    screen.blit(pygame.transform.scale(buffer,SCREEN_SIZE),pygame.Rect(ORIGIN,SCREEN_SIZE))
    pygame.display.flip()

    # Handle input
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:
                bar.current -= 1
            elif event.key == K_RIGHT:
                bar.current += 1
        elif event.type == QUIT:
            running = False