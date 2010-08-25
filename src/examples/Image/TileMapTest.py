import pygame
import toast

from pygame.locals import *

# Define the origin
ORIGIN = (0,0)
# Set the screen size
SCREEN_SIZE = (256, 256)

# Setup pygame display
pygame.display.set_mode(SCREEN_SIZE)
# Get a surface the size of the window
screen = pygame.display.get_surface()
# Create a buffer to render to
buffer = pygame.Surface((128, 128))

# Define the sub-image dimension.
dimension = (32,32)

# Load the image from a file.
data = pygame.image.load("Data/tiles.png")

# Create the image sheet object.
sheet = toast.ImageSheet(data, dimension)

# Define the tilemap data.
data = [[0,1,2,3],
        [3,0,1,2],
        [2,3,0,1],
        [1,2,3,0]]

map = toast.TileMap(sheet, data)
map.position = (16, 16)

clock = pygame.time.Clock()

frame = 0

# Game loop
running = True
while running:
    clock.tick(60)
    
    buffer.fill((98,186,221))
    
    # Simulate parallax
    map.render_fixed(buffer, (0, 0))
    
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

