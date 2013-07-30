from toast.scene_graph import Component
from toast.math.vector import Vector2D
from toast.math.matrix import MatrixHelper

class Transform(Component):
    """Assists with positioning of GameObjects and all it's attached children 
    with transforms. On changing of position, those children will re-position 
    themselves relative to their parent's position.
    """
    
    def __init__(self, *position):
        """
        :param position: The initial position for the transform.
        :type position: tuple.
        """
        super(Transform, self).__init__()
        
        if position is ():
            self.__local_position = Vector2D.Zero()
        else:
            self.__local_position = Vector2D(position)
            
        self.__local_rotation = 0
        self.__local_scale = Vector2D(1, 1)
            
    @property
    def parent(self):
        """Gets the parent of the GameObject. 
        
        :returns: GameObject -- The parent of the parent GameObject.
        """
        return self.game_object.parent if self.game_object else None
        
    @property
    def position(self):
        """Gets the transform position. 
        
        :returns: Vector2D -- The transform position in world space.
        """
        if self.parent and hasattr(self.parent, 'transform'):
            return self.parent.transform.position + self.__local_position
        else:
            return self.local_position
    
    @position.setter
    def position(self, other):
        """Sets the position in world space.
        
        :param other: The new position.
        :type other: tuple.
        
        """
        if self.parent and hasattr(self.parent, 'transform'):
            self.__local_position = self.parent.get_component('Transform').position + other
        else:
            self.local_position = other
            
        self.mark_dirty()
        
    @property
    def local_position(self):
        """Gets the position relative to the GameObject's parent. 
        
        :returns: Vector2D -- The transform's position in local space.
        """
        return self.__local_position
    
    @local_position.setter
    def local_position(self, other):
        """Sets the position relative to the GameObject's parent. 
        
        :param other: The new position in the GameObject's parent's local space.
        :type other: tuple.
        
        """
        self.__local_position = Vector2D(other[0], other[1])
        self.mark_dirty()
        
    def mark_dirty(self):
        if not self.game_object:
            return
        
        for child_transform in [c.transform for c in self.game_object.children if hasattr(c, 'transform')]:
            child_transform.mark_dirty()
        
    def look_at(self, pos):
        angle = (pos - self.position).angle
        self.rotation = -angle
        
    @property
    def forward(self):
        return Vector2D.from_angle(self.rotation)
        
    @property
    def rotation(self):
        return self.__local_rotation
    
    @rotation.setter
    def rotation(self, angle_in_degrees):
        self.__local_rotation = angle_in_degrees
    
    @property
    def scale(self):
        return self.__local_scale
    
    @scale.setter
    def scale(self, new_scale):
        self.__local_scale = Vector2D(new_scale[0], new_scale[1])
        
    @property
    def matrix(self):
        return MatrixHelper.translation_matrix(self.position[0], self.position[1])
