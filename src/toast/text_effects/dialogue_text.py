"""
" * DialogueText.py
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

import Wrapper

class DialogueText(Wrapper.Wrapper):
    def __init__(self, internal):
        Wrapper.Wrapper.__init__(self, internal)
        self.delay = 1
        
    def Update(self, time = 0.01667):
        self.internal.Update(time)
        self.charList = self.internal.charList
        
        index = 0;
        
        for (image, rect) in self.charList:
            if self.time > (self.delay * index):
                pass
            else:
                rect.left = -rect.width
                rect.top = -rect.height
                
            index += 1