import pygame

blank_pixel = pygame.Color(0, 255, 255, 255)
empty_pixel = pygame.Color(0, 0, 0, 0)

class ImageSheet(object):
    """
    " * ImageSheet
    " *
    """

    COLORKEY = (255, 0, 255)

    def __init__(self, surface, dimension, keys = None):
        """Class Constructor
        
        surface:      A surface to be partitioned into sub-images.
        dimension:    A tuple of the form (width, height).
        keys:         A list of string identifiers for each sub-image.
                      If none is provided, defaults to filename + index.
        """

        # Set the surface.
        self.__image_sheet = surface

        self.__image_sheet.set_colorkey(ImageSheet.COLORKEY)

        self.__dimension = dimension
        
        # Create a dictionary to hold the sub-images.
        self.__image_dict = {}
        self.__empty_dict = {}

        if keys != None:
            self.__frame_list = keys
        else:
            self.__frame_list = []

        # Determine number of steps needed
        height = self.__image_sheet.get_height() / self.__dimension[1]
        width = self.__image_sheet.get_width() / self.__dimension[0]

        # Build the dictionary
        for y in range(height):
            for x in range(width):
                i = x * dimension[0]
                j = y * dimension[1]

                frame_ID = ""

                index = ((y * width) + x)

                try:
                    frame_ID = self.__frame_list[index]
                except:
                    frame_ID = 'FRAME_' + str(index)
                    self.__frame_list.append(frame_ID)

                self.__image_dict[frame_ID] = \
                self.__image_sheet.subsurface(pygame.Rect(i, j,
                                                          self.__dimension[0],
                                                          self.__dimension[1])).copy()
                                                          
                bounding_rect = self.__image_dict[frame_ID].get_bounding_rect()
                
                self.__empty_dict[frame_ID] = bounding_rect.width == 0 or bounding_rect.height == 0
                        
    def __getitem__(self, key):
        try:
            return self.__image_dict[key]
        except:
            return self.__image_dict[self.__frame_list[key]]
        
    def is_blank(self, frame):
        try:
            return self.__empty_dict[frame]
        except:
            return self.__empty_dict[self.__frame_list[frame]]

    def get_dimension(self):
        return self.__dimension
