import random

class ShakeEffect(object):
    def __init__(self, camera, magnitude, duration):
        self.__camera = camera
        self.__magnitude = magnitude
        self.__duration = int(duration * 1000)
        
    def update(self, milliseconds=0):
        self.__duration -= milliseconds
        
        if self.__duration < 0:
            self.__camera.remove(self)
        
        x = self.__camera.position[0] + random.randint(-self.__magnitude, self.__magnitude)
        y = self.__camera.position[1] + random.randint(-self.__magnitude, self.__magnitude)
        
        new_pos = (x, y)
        
        self.__camera.position = new_pos
    
    def render(self, surface, offset):
        pass