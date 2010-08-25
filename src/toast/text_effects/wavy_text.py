"""
" * WavyText.py
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

import pygame
import math

import wrapper

class WavyText(wrapper.Wrapper):
    def __init__(self, internal):
        wrapper.Wrapper.__init__(self, internal)
        self.amplitude = self.internal.charList[0][1].height / 2
        self.frequency = 1
        self.phaseStep = 1
    
    """
    " * WavyText.Update
    " *    time:        The amount of time lapsed since the last call to update.
    " *    Overrides:   Wrapper.Update()
    " *    Description: A simple harmonic motion function.
    """     
    def update(self, time = 0.01667):
        self.internal.update(time)
        self.charList = self.internal.charList
        
        phase = 0
        
        for (image, rect) in self.charList:
            rect.top += self.Displacement(self.amplitude, self.frequency, self.internal.time, phase)
            phase -= self.phaseStep
    
    """
    " * WavyText.displacement
    " *    Returns: Vertical displacement
    " *    Description: A simple harmonic motion function.
    """            
    def Displacement(self, amplitude, frequency, time, phase):
        return amplitude * math.cos((2 * math.pi * frequency * time) + phase)
    