from toast.component import Component
from toast.math.vector2D import Vector2D

class Transform(Component):
    def __init__(self):
        super(Transform, self).__init__()
        self.__local_position = Vector2D.Zero()
        
    @property
    def position(self):
        """ Returns the world position as a Vector2D. """
        if self.parent.parent and hasattr(self.parent.parent, 'transform'):
            return self.parent.parent.get_component('Transform').position + self.__local_position
        else:
            return self.local_position
    
    @position.setter
    def position(self, other):
        """ Sets the position in world space.
        
        Arguments:
        other -- A position in world space.
        
        """
        if self.parent.parent and hasattr(self.parent.parent, 'transform'):
            self.__local_position = self.parent.parent.get_component('Transform').position - other
        else:
            self.local_position = other
        
    @property
    def local_position(self):
        """ Returns the position relative to it's parent's parent as a Vector2D. """
        return self.__local_position
    
    @local_position.setter
    def local_position(self, other):
        """ Sets the position in local(relative to it's parent) space.
        
        Arguments:
        other -- A position in local space.
        
        """
        self.__local_position = Vector2D(other[0], other[1])
        