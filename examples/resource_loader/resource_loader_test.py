import pygame
import toast
from pygame.locals import *

from toast.animation import Animation
from toast.image_sheet import ImageSheet
from toast.resource_loader import ResourceLoader

# Define the origin
ORIGIN = (0,0)
# Set the screen size
SCREEN_SIZE = (256, 256)

# Setup pygame display
pygame.display.set_mode(SCREEN_SIZE)
# Get a surface the size of the window
screen = pygame.display.get_surface()
# Create a buffer to render to
buffer = pygame.Surface((43, 43))

# Define the sub-image dimension.
dimension = (40,43)

data = ResourceLoader.load('Data/run.png')


# Create the image sheet object.
sheet = ImageSheet(data, dimension)

target = sheet[0]

interval = 80

run = [(sheet[0], interval), 
       (sheet[1], interval), 
       (sheet[2], interval), 
       (sheet[3], interval), 
       (sheet[4], interval), 
       (sheet[5], interval), 
       (sheet[6], interval), 
       (sheet[7], interval)]

anim = Animation('run_cycle', run)
anim.play('run_cycle')

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    clock.tick(60)
    
    buffer.fill((98,186,221))
    
    buffer.blit(target,(0,0))
    anim.update(16)
    target = anim.get_current_frame()

    # Scale up buffer and draw to screen
    screen.blit(pygame.transform.scale(buffer,SCREEN_SIZE), pygame.Rect(ORIGIN,SCREEN_SIZE))

    pygame.display.flip()

    # Handle input
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            anim.stop()
            if event.key == K_ESCAPE:
                running = False
                
        elif event.type == QUIT:
            running = False

        if event.type == KEYUP:
            anim.play('run_cycle')