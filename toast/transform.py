from toast.scene_graph import Component
from toast.math.vector import Vector2D

class Transform(Component):
    def __init__(self, *position):
        super(Transform, self).__init__()
        
        if position is ():
            self.__local_position = Vector2D.Zero()
        else:
            self.__local_position = Vector2D(position)
            
    @property
    def grandparent(self):
        """ Returns the parent of the parent. """
        return self.game_object.parent if self.game_object else None
        
    @property
    def position(self):
        """ Returns the world position as a Vector2D. """
        if self.grandparent and hasattr(self.grandparent, 'transform'):
            return self.grandparent.transform.position + self.__local_position
        else:
            return self.local_position
    
    @position.setter
    def position(self, other):
        """ Sets the position in world space.
        
        Arguments:
        other -- A position in world space.
        
        """
        if self.grandparent and hasattr(self.grandparent, 'transform'):
            self.__local_position = self.grandparent.get_component('Transform').position - other
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
        