import pygame

class BitmapFont(object):

    def __init__(self, surface, dimension, sample_string):
        """
        " * Class Constructor
        " *    filename:     The path to the font bitmap.
        " *    dimension:    A tuple of the form (width, height).
        " *    sampleString: A string containing the character values. Left to
        " *                  right, top to bottom.
        """

        # Load font image
        self.font_sheet = surface

        self.dimension = dimension

        # Create an empty dictionary to map the char value to a surface
        self.font_dict = {}

        # Determine number of steps needed
        height = self.font_sheet.get_height() / self.dimension[1]
        width = self.font_sheet.get_width() / self.dimension[0]

        # Build the dictionary
        for y in range(height):
            for x in range(width):
                i = x * dimension[0]
                j = y * dimension[1]

                self.font_dict[sample_string[((y * width) + x)]] = \
                self.font_sheet.subsurface(pygame.Rect(i, j, self.dimension[0],
                                                       self.dimension[1]))

    def render(self, text):
        """
        " * BitmapFont.render
        " *    text:    This is the text to render.
        " *    Returns: A surface
        """

        # Create a surface that will hold the rendered text.
        font_buffer = pygame.Surface((len(text) * self.dimension[0],
                                    self.dimension[1]), pygame.SRCALPHA, 32)

        # Go through each character in string and draw it to the font buffer
        index = 0
        for char in text:
            try:
                font_buffer.blit(self.font_dict[char],
                                 pygame.Rect(index, 0, self.dimension[0],
                                             self.dimension[1]))
            except:
                # Unable to find char in dictionary.
                if char.isupper():
                    try:
                        font_buffer.blit(self.font_dict[char.lower()],
                                         pygame.Rect(index, 0,
                                                     self.dimension[0],
                                                     self.dimension[1]))
                    except:
                        raise IndexError("Missing glyph: '{0}'".format(str(char)))
                elif char.islower():
                    try:
                        font_buffer.blit(self.font_dict[char.upper()],
                                         pygame.Rect(index, 0,
                                                     self.dimension[0],
                                                     self.dimension[1]))
                    except:
                        raise IndexError("Missing glyph: '{0}'".format(str(char)))
                else:
                    raise IndexError("Missing glyph: '{0}'".format(str(char)))

            index += self.dimension[0]


        return font_buffer
