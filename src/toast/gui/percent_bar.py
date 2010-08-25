"""
" * animation.py
" * Copyright (C) 2009 Joshua Skelton
" *                    joshua.skelton@gmail.com
" *
" * This program is free software; you can redistribute it and/or
" * modify it as you see fit.
" *
" * This program is distributed in the hope that it will be useful,
" * but WITHOUT ANY WARRANTY; without even the implied warranty of
" * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""

class PercentBar(object):
    def __init__(self, background, foreground):
        self.__current = 1.0
        self.background = background
        self.foreground = foreground
        self.position = (0, 0)
        self.spacing = 0
        
    def set_current(self, value):
        self.__current = value
        if self.__current < 0.0:
            self.__current = 0.0
        elif self.__current > 1.0:
            self.__current = 1.0
        
    def get_current(self):
        return self.__current
    
    current = property(get_current, set_current)
    
    def render(self, surface, offset=(0,0)):
        surface.blit(self.background, self.position)
        surface.blit(self.foreground, self.position, (0, 0, self.foreground.get_width() * self.current, self.foreground.get_height()))
