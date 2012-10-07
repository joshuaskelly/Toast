"""
" * sprite.py
" * Copyright (C) 2012 Joshua Skelton
" *                    joshua.skelton@gmail.com
" *
" * This program is free software; you can redistribute it and/or
" * modify it as you see fit.
" *
" * This program is distributed in the hope that it will be useful,
" * but WITHOUT ANY WARRANTY; without even the implied warranty of
" * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""

from toast.component import Component
from toast.math.vector2D import Vector2D

class Sprite(Component):
    def __init__(self, image_or_animation, position=(0,0)):
        super(Sprite, self).__init__()
        
        self.__position = Vector2D(position)
        self.__image = None
        self.__animation = None
        
        if hasattr(image_or_animation, 'add_animation'):
            self.__animation = image_or_animation
            self.add(image_or_animation)
            self.image = self.__animation.get_current_frame()
        else:
            self.image = image_or_animation
        
    @property
    def position(self):
        return self.__position
        
    @position.setter
    def position(self, value):
        self.__position = Vector2D(value[0], value[1])
        
    @property
    def image(self):
        return self.__image
    
    @image.setter
    def image(self, image):
        self.__image = image
        
    def render(self, surface, offset=(0,0)):
        
        surface.blit(self.image, self.position - offset)