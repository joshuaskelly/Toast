import pygame
import toast

from toast.text_effects import wavy_text

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
buffer = pygame.Surface((320,240))

# Read the alphabet string from a file.
alphaArray = open("Data/anomaly.dat","r").readline()
# Define the font dimensions
fontDimension = (32,32)
# Create bitmap font object
font = toast.BitmapFont("Data/anomaly.png", fontDimension, alphaArray)

# Create the text object
text = toast.Text(font,"Wavy Text")
# Wrap the text object with an effect
effect = wavy_text.WavyText(text)

# Set the text object's position
effect.position = (16, 88)

# Get the pygame clock
clock = pygame.time.Clock()


# Game loop
running = True
while running:
    clock.tick(60)
    buffer.fill((0,0,0))
    
    # Update the text object
    effect.update()

    # Draw to buffer
    effect.render(buffer)
    
    # Scale up buffer and draw to screen
    screen.blit(pygame.transform.scale(buffer,SCREEN_SIZE),pygame.Rect(ORIGIN,SCREEN_SIZE))
    pygame.display.flip()

    # Handle input
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            else:
                pass