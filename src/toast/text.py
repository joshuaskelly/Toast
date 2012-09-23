"""
" * text.py
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

from toast.component import Component

class Text(Component):

    def __init__(self, font, message):
        """
        " * Class Constructor
        " *    font:        A BitmapFont object.
        " *    message:     A string.
        """
        super(Text, self).__init__()

        self.font = font
        self.message = message
        self.__position = (0, 0)
        self.__time = 0

        self.charList = []
        self.positionList = []

        left = 0
        top = 0
        # Build the list of characters
        for char in message:
            image = self.font.render(char)
            rect = image.get_rect()
            rect.left = left
            rect.top = top
            self.charList.append((image, rect))
            self.positionList.append((left, top))
            left += rect.width

    def update(self, time = 0.1667):
        self.time += time

        left = 0
        index = 0
        for (_, rect) in self.charList:
            rect.left = self.position[0] + self.positionList[index][0]
            rect.top = self.position[1] + self.positionList[index][1]
            left += rect.width
            index += 1

    def render(self, surface, offset=(0,0)):
        for (image, rect) in self.charList:
            surface.blit(image, rect)

    def GetPosition(self):
        return self.__position

    def SetPosition(self, position):
        self.__position = position

    position = property(GetPosition, SetPosition)

    def GetTime(self):
        return self.__time

    def SetTime(self, time):
        self.__time = time

    time = property(GetTime, SetTime)
