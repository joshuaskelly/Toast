"""
TimeMap.py
Copyright (C) 2009 Joshua Skelton
                joshua.skelton@gmail.com

This program is free software; you can redistribute it and/or
modify it as you see fit.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

History:
   2010-07-08 - Refactor to make module more 'pythonic.' It would appear that I
                managed to also gain a small improvement in performance.
   
"""

import pygame

class TileMap(object):
    """
    TileMap
    """
    
    INVALID_TILE = -1

    def __init__(self, image_sheet, data):
        """
        Class Constructor
           imageSheet:   An ImageSheet object.
           data:         A two dimensional array.
        """

        self.__image_sheet = image_sheet
        self.__data = data
        self.__map_size = (len(data[0]), len(data))
        self.__tile_size = self.__image_sheet.get_dimension()
        self.__parallax = 1.0
        self.__scroll_register = (0,0)
        self.__scroll_rate = (0,0)
        self.__position = (0, 0)
        

    @property
    def parallax(self):
        return self.__parallax
    
    @parallax.setter
    def parallax(self, value):
        self.__parallax = value
        
    @property
    def scroll_rate(self):
        return self.__scroll_rate
    
    @scroll_rate.setter
    def scroll_rate(self, rate):
        self.__scroll_rate = (rate[0], rate[1])
    
    @property
    def scrollx(self):
        return self.scroll_rate[0]
    
    @scrollx.setter
    def scrollx(self, value):
        self.scroll_rate = (value, self.scroll_rate[1])
    
    @property
    def scrolly(self):
        return self.scroll_rate[1]
    
    @scrolly.setter
    def scrolly(self, value):
        self.__scroll_rate = (self.scroll_rate[0], value)
        
    @property
    def position(self):
        return self.__position
    
    @position.setter
    def position(self, value):
        self.__position = (value[0], value[1])
        
    def tile_id_at_index(self, index):
        x = index[0] % self.__map_size[0]
        y = index[1] % self.__map_size[1]
        
        return self.__data[y][x]
    
    def tile_id_at_pixel(self, pixel, offset=(0,0)):
        x = pixel[0] / self.__tile_size[0]
        y = pixel[1] / self.__tile_size[1]
        
        return self.__data[y][x]
    
    def tile_rect_at_index(self, index, offset=(0, 0)):
        x = (index[0] * self.__tile_size[0]) - offset[0]
        y = (index[1] * self.__tile_size[1]) - offset[1]
        
        return (x, y, self.__tile_size[0], self.__tile_size[1])
    
    def tile_rect_at_pixel(self, pixel, offset=(0, 0)):
        x = ((pixel[0] / self.__tile_size[0]) * self.__tile_size[0]) + offset[0]
        y = ((pixel[1] / self.__tile_size[1]) * self.__tile_size[1]) + offset[1]
        
        return (x, y, self.__tile_size[0], self.__tile_size[1])

    def draw_tile_outlines(self, surface, offset=(0, 0)):
        """
        draw_tile_outlines
           surface:     The surface to draw the tilemap on.
           offset:      The amount to offset the tilemap.
           
           description: Draws a black box around each tile. Handy for debugging.
        """

        #offset = (offset[0] * self.__parallax + int(self.__scroll_register[0]), 
        #          offset[1] * self.__parallax + int(self.__scroll_register[1]))

        width = surface.get_width() / self.__tile_size[0]
        height = surface.get_height() / self.__tile_size[1]

        rect = pygame.Rect((0, 0), self.__tile_size)

        x_begin = int(offset[0] / self.__tile_size[0])
        x_end = int(x_begin + width + 1)

        y_begin = int(offset[1] / int(self.__tile_size[1]))
        y_end = int(y_begin + height + 1)
        
        print "Drawing Area: %s x %s" % (len(range(x_begin, x_end)), len(range(y_begin, y_end)))
        
        num_tiles = 0
        
        # Draw the tilemap
        for y in range(y_begin, y_end):
            for x in range(x_begin, x_end):
                rect.topleft = ((x * self.__tile_size[0]) - offset[0],
                                (y * self.__tile_size[1]) - offset[1])

                dx = (x % len(self.__data[0]))
                dy = (y % len(self.__data))
                
                if not self.__image_sheet.is_blank(self.__data[dy][dx]):
                    num_tiles += 1
                    #surface.blit(self.__image_sheet[self.__data[dy][dx]], rect)
                    pygame.draw.rect(surface, (64, 64, 64), rect, 1)
                    
                    

    def update(self, milliseconds=16):
        self.__scroll_register = (self.__scroll_register[0] + self.__scroll_rate[0],
                          self.__scroll_register[1] + self.__scroll_rate[1])
        
    def render_fixed(self, surface, offset=(0, 0)):
        offset = (offset[0] + self.position[0], offset[1] + self.position[1])
        for y in range(self.__map_size[0]):
            for x in range(self.__map_size[1]):
                if self.tile_id_at_index((x, y)) != TileMap.INVALID_TILE:
                    surface.blit(self.__image_sheet[self.tile_id_at_index((x, y))],
                                 self.tile_rect_at_index((x, y), offset))
        
    def render(self, surface, offset=(0, 0)):
        """
        render
           surface:     The surface to draw the tilemap on.
           offset:      The amount to offset the tilemap.
        """

        offset = (offset[0] * self.__parallax + int(self.__scroll_register[0]), 
                  offset[1] * self.__parallax + int(self.__scroll_register[1]))

        width = surface.get_width() / self.__tile_size[0]
        height = surface.get_height() / self.__tile_size[1]

        x_begin = int(offset[0] / self.__tile_size[0])
        x_end = int(x_begin + width + 1)
        
#        tiles_x = map((lambda x: x * self.__tile_size[0]), range(surface.get_width() / self.__tile_size[0]))
#        tiles_y = map((lambda y: y * self.__tile_size[1]), range(surface.get_height() / self.__tile_size[1]))
        
        y_begin = int(offset[1] / int(self.__tile_size[1]))
        y_end = int(y_begin + height + 1)
        
        # Draw the tilemap
        for y in range(y_begin, y_end):
            for x in range(x_begin, x_end):
                
                # Check if we need to draw this tile.
                if self.tile_id_at_index((x, y)) != TileMap.INVALID_TILE:
                    
                    # Draw the tile at is location
                    surface.blit(self.__image_sheet[self.tile_id_at_index((x, y))],
                                 self.tile_rect_at_index((x, y), offset))
                    
        #self.draw_tile_outlines(surface, offset)
                    
