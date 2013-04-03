from toast.scene import Scene
from toast.gradient import Gradient
from toast.sprite import Sprite

import pygame

from examples.demo_game import DemoGame

class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()
        
        # Create a simple black to white gradient.
        surf = Gradient.createVerticalGradient((32, 208), (255,255,255), (0,0,0))
        self.add(Sprite(surf, (16, 16)))
        
        # Create a low-res and upscale it for a retro effect.
        surf = Gradient.createVerticalGradient((1, 26), (255,221,0), (255,221,0), (58,209,131), (32,169,131), (32,169,131), (17,115,117), (64,18,60), (64,18,60), (64,18,60))
        surf = pygame.transform.scale(surf, (32, 208))
        self.add(Sprite(surf, (64, 16)))
        
        # Create regular multi-stop gradient
        surf = Gradient.createVerticalGradient((32, 208), (255,237,171),(255,237,171), (255,224,137), (249,182,114), (252,136,97), (174,58,71), (174,58,71))
        self.add(Sprite(surf, (112, 16)))
        
        # Create simple black to white gradient
        surf = Gradient.createHorizontalGradient((144, 32), (255,255,255), (0,0,0))
        self.add(Sprite(surf, (160, 16)))
        
        # Create a low-res and upscale it for a retro effect.
        surf = Gradient.createHorizontalGradient((12, 32), (246,177,73), (246,177,73), (248,87,45), (223,42,51), (162,37,67), (107,49,45), (107,49,45), (107,49,45))
        surf = pygame.transform.scale(surf, (144, 32))
        self.add(Sprite(surf, (160, 64)))
        
game = DemoGame((640, 480), NewScene)
game.run()