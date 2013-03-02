import os
import pygame

from toast.decorators.memoize import memoize

IMAGE_FILE_EXTENSIONS = ['PNG', 'GIF', 'BMP', 'JPG', 'TGA', 'TIF', 'GIF']
SOUND_FILE_EXTENSIONS = ['OGG', 'WAV']

class ResourceLoader(object):
    @staticmethod
    @memoize
    def load(filename):
        extension = filename.rsplit('.').pop().upper()

        if extension in IMAGE_FILE_EXTENSIONS:
            try:
                image = pygame.image.load(os.path.join(filename)).convert()
                image.set_colorkey((255, 0, 255))
                return image
            except:
                raise ResourceException('Failed to load: %(resource)s.' % \
                                        {"resource": filename})
        
        elif extension in SOUND_FILE_EXTENSIONS:
            try:
                return pygame.mixer.Sound(os.path.join(filename))
            except:
                raise ResourceException('Failed to load: %(resource)s.' % \
                                        {"resource": filename})
        
        else:
            return open(os.path.join(filename), 'w')
        
class ResourceException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)