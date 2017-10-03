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


class IconBar(object):
    LEFT_TO_RIGHT = (1, 0)
    RIGHT_TO_LEFT = (-1, 0)
    TOP_TO_BOTTOM = (0, 1)
    BOTTOM_TO_TOP = (0, -1)
    
    def __init__(self, total, full, empty):
        self.__total = total
        self.__current = total
        self.full = full
        self.empty = empty
        self.position = (0, 0)
        self.direction = IconBar.LEFT_TO_RIGHT
        self.spacing = 0
        
    def set_current(self, value):
        self.__current = value
        if self.__current < 0:
            self.__current = 0
        elif self.__current > self.__total:
            self.__current = self.__total
        
    def get_current(self):
        return self.__current
    
    current = property(get_current, set_current)
    
    def set_total(self, value):
        self.__total = value
        
    def get_total(self):
        return self.__total
    
    total = property(get_total, set_total)
    
    def render(self, surface, offset=(0,0)):
        for i in range(self.total):
            pos = ( self.position[0] + (i * self.direction[0] * (self.full.get_width() + self.spacing)),
                    self.position[1] + (i * self.direction[1] * (self.full.get_height() + self.spacing)))
            
            if i < self.current:
                surface.blit(self.full, pos)
            else:
                surface.blit(self.empty, pos)
