import pygame

from toast.game import Game
from toast.game_object import GameObject

class TileMap(GameObject):
    INVALID_TILE = -1

    def __init__(self, image_sheet, data):
        """Class Constructor
        
        imageSheet:   An ImageSheet object.
        data:         A two dimensional array.
        """
        super(TileMap, self).__init__()

        self.__image_sheet = image_sheet
        self.__data = data
        self.__map_size = (len(data[0]), len(data))
        self.__tile_size = self.__image_sheet.get_dimension()
        self.__parallax = 1.0
        self.__scroll_register = (0,0)
        self.__scroll_rate = (0,0)
        self.__position = (0, 0)
        
        self.__buffer = pygame.Surface((self.__map_size[0] * self.__tile_size[0],
                                        self.__map_size[1] * self.__tile_size[1]))
        
        self.redraw_buffer()

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
        
    @property
    def width(self):
        return self.__map_size[0]
    
    @width.setter
    def width(self, value):
        self.__map_size = (value, self.__map_size[1])
    
    @property
    def height(self):
        return self.__map_size[1]
    
    @height.setter
    def height(self, value):
        self.__map_size = (self.__map_size[0], value)
        
    def tile_id_at_index(self, index):
        x, y = index
        
        if x < 0 or y < 0:
            return None
        
        if x >= self.width or y >= self.height:
            return None
        
        try:
            return self.__data[y][x]
        except:
            print 'Invalid index: {0}'.format(index)
    
    def tile_id_at_position(self, pos, offset=(0,0)):
        
        x = int(pos[0]) / self.__tile_size[0]
        y = int(pos[1]) / self.__tile_size[1]
        
        try:
            return self.__data[y][x]
        except:
            return self
    
    def tile_id_at_pixel(self, pixel, offset=(0,0)):
        
        p = Game.camera_to_world(pixel)
        x = int(p[0]) / self.__tile_size[0]
        y = int(p[1]) / self.__tile_size[1]
        
        if x < self.width and y < self.height and x > 0 and y > 0:
            return self.__data[y][x]
        else:
            return self.INVALID_TILE
    
    def tile_index_at_pixel(self, pixel):
        p = Game.camera_to_world(pixel)
        x = int(p[0]) / self.__tile_size[0]
        y = int(p[1]) / self.__tile_size[1]
        
        return x, y
    
    def set_tile(self, index, value):
        self.__data[index[1]][index[0]] = value
        self.redraw_buffer()
    
    def tile_rect_at_index(self, index, offset=(0, 0)):
        x = (index[0] * self.__tile_size[0]) - offset[0]
        y = (index[1] * self.__tile_size[1]) - offset[1]
        
        return (x, y, self.__tile_size[0], self.__tile_size[1])
    
    def tile_rect_at_pixel(self, pixel, offset=(0, 0)):
        x = ((pixel[0] / self.__tile_size[0]) * self.__tile_size[0]) + offset[0]
        y = ((pixel[1] / self.__tile_size[1]) * self.__tile_size[1]) + offset[1]
        
        return (x, y, self.__tile_size[0], self.__tile_size[1])
    
    def get_collide_list(self, rect, predicate=None):
        result = []
        
        if predicate is None:
            predicate = lambda s, x: s.tile_id_at_index(x) >=0
        
        for index, rect in self.get_indexes_in_rect(rect):    
            if predicate(self, index):
                result.append(rect)
                    
        return result
    
    #TODO: Rename this to reflect the index, rect pairing
    def get_indexes_in_rect(self, rect):
        offset = (self.__scroll_register[0], self.__scroll_register[1])
        
        left = (rect[0] + offset[0]) / self.__tile_size[0]
        top = (rect[1] + offset[1]) / self.__tile_size[1]
        right = left + (rect[2] + self.__tile_size[0] / 2) / self.__tile_size[0]
        bottom = top + (rect[3] + self.__tile_size[1] / 2) / self.__tile_size[1]
        
        result = []
        
        for x in range(left, right + 1):
            for y in range(top, bottom + 1):
                index = (x % self.__map_size[0], y % self.__map_size[1])
                
                x1 = x * self.__tile_size[0]
                y1 = y * self.__tile_size[1]
                
                sub_rect = pygame.Rect(x1 + offset[0], y1 + offset[1], self.__tile_size[0], self.__tile_size[1])
                
                result.append((index, sub_rect))
                
        return result
    
    def draw_tile_outlines(self, surface, offset=(0, 0)):
        """Draws a black box around each tile. Handy for debugging.
        
        surface:     The surface to draw the tilemap on.
        offset:      The amount to offset the tilemap.
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
        
        #print "Drawing Area: %s x %s" % (len(range(x_begin, x_end)), len(range(y_begin, y_end)))
        
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
        super(TileMap, self).update(milliseconds)
        
        self.__scroll_register = (self.__scroll_register[0] + self.__scroll_rate[0],
                          self.__scroll_register[1] + self.__scroll_rate[1])
        
    def render(self, surface, offset=(0,0)):
        self.render_internal(surface, offset)
        #surface.blit(self.__buffer, (self.position[0] - offset[0], self.position[1] - offset[1]))
    
    
    def redraw_buffer(self):
        return
        self.__buffer = pygame.Surface((self.__map_size[0] * self.__tile_size[0],
                                self.__map_size[1] * self.__tile_size[1]))
                
        self.render_internal(self.__buffer)
        
    def render_internal(self, surface, offset=(0, 0)):
        offset = (offset[0] + self.position[0], offset[1] + self.position[1])
        
        width = surface.get_width() / self.__tile_size[0]
        height = surface.get_height() / self.__tile_size[1]
        
        x_begin = int(offset[0] / self.__tile_size[0])
        x_end = int(x_begin + width + 0.5) + 1
        
        y_begin = int(offset[1] / int(self.__tile_size[1]))
        y_end = int(y_begin + height + 0.5) + 1
        
        for y in range(y_begin, y_end):#self.__map_size[0]):
            for x in range(x_begin, x_end):#self.__map_size[1]):
                if self.tile_id_at_index((x, y)):# != TileMap.INVALID_TILE:
                    surface.blit(self.__image_sheet[self.tile_id_at_index((x, y))],
                                 self.tile_rect_at_index((x, y), offset))
        
    def render_old(self, surface, offset=(0, 0)):
        """Draws the tilemap to the given surface with the specified offset.
        
        surface:     The surface to draw the tilemap on.
        offset:      The amount to offset the tilemap.
        """

        offset = (offset[0] * self.__parallax + int(self.__scroll_register[0]), 
                  offset[1] * self.__parallax + int(self.__scroll_register[1]))

        width = surface.get_width() / self.__tile_size[0]
        height = surface.get_height() / self.__tile_size[1]

        x_begin = int(offset[0] / self.__tile_size[0])
        x_end = int(x_begin + width + 1)
        
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
                    
