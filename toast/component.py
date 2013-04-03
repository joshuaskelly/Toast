import weakref

class Component(object):
    def __init__(self):
        self.__game_object = None
        self.added = False
        self.index = 0
        
    @property
    def game_object(self):
        return None if self.__game_object is None else self.__game_object()
    
    @game_object.setter
    def game_object(self, other):
        self.__game_object = weakref.ref(other)
        
    def is_a_component(self, other=None):
        return hasattr(other, 'is_a_component') if other is not None else True
    
    def awake(self):
        pass
    
    def update(self, milliseconds=0):
        pass
            
    def remove(self):
        """ Removes component from parent. """
        self.game_object.remove(self)
            
class ComponentException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
