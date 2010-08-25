import pygame

def get_instance():
    return Test()

class Test(object):
    def __init__(self):
        self.image = pygame.image.load('Data/player.png')
    
    def update(self, delta):
        pass
        
    def render(self, surface, offset):
        surface.blit(self.image, (self.x - offset[0], self.y - offset[1]))