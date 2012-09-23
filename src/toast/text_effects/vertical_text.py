"""
" * VerticalText.py
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

import wrapper

class VerticalText(wrapper.Wrapper):
    def __init__(self, internal):
        wrapper.Wrapper.__init__(self, internal)
    
 
    def update(self, time = 0.01667):
        """
        " * VerticalText.update
        " *    time:        The amount of time lapsed since the last call to update.
        " *    Overrides:   Wrapper.update()
        " *    Description: Orients the text vertically.
        """    
        self.internal.update(time)
        self.charList = self.internal.charList
        
        offset = 0
        
        for (_, rect) in self.charList:
            rect.left = self.position[0]
            rect.top = self.position[1] + offset
            offset += rect.height
    