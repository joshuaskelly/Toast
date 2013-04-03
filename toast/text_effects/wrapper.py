"""
" * Wrapper.py
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

import math
from toast.component import Component

class Wrapper(Component):

    def __init__(self, internal):
        """
        " * Class Constructor
        " *    internal:    A text object to wrap around.
        " *    Description: This class provides a base class for text effect 
        " *                 wrappers. Subclasses simply need to override the Update
        " *                 method to implement the desired effect.
        """   
        super(Wrapper, self).__init__()
        
        self.internal = internal
        self.charList = []


    def update(self, time = 0.01667):
        """
        " * Wrapper.Update
        " *    time:           The amount of time lapsed since the last update.
        " *    Description:    A method that describes how the text object is 
        " *                    transformed as a function of time.
        """
        
        raise "Instances of Wrapper can not be created." 
        
    def render(self, surface, offset=(0,0)):
        self.internal.render(surface, offset)
        
    def Displacement(self, amplitude, frequency, time, phase):
        return amplitude * math.cos((2 * math.pi * frequency * time) + phase)
    
    def GetPosition(self):
        return self.internal.position
    
    def SetPosition(self, position):
        self.internal.position = position
        
    position = property(GetPosition,SetPosition)
    
    def GetTime(self):
        return self.internal.time
    
    def SetTime(self, time):
        self.internal.time = time
        
    time = property(GetTime, SetTime)