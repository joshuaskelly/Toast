import os
import pygame

from toast.Decorators.memoize import Memoize

IMAGE_FILE_EXTENSIONS = ['PNG', 'GIF', 'BMP', 'JPG', 'TGA', 'TIF', 'GIF']
SOUND_FILE_EXTENSIONS = ['OGG', 'WAV']

class ResourceLoader(object):
    __shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state

    @Memoize
    def load(filename):
        extension = filename.rsplit('.').pop().upper()

        if extension in IMAGE_FILE_EXTENSIONS:
            return pygame.image.load(os.path.join(filename))
        
        elif extension in SOUND_FILE_EXTENSIONS:
            return pygame.mixer.Sound(os.path.join(filename))
        
        else:
            return open(os.path.join(filename), 'w')
        
class Resource(object):
    def load(self, other):
        pass