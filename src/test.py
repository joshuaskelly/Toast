import pygame

pygame.display.set_mode((320, 240))

def handle_input():
    pygame.event.pump()

def update():
    pass

def draw():
    pygame.display.flip()

while True:
    handle_input()
    update()
    draw()
