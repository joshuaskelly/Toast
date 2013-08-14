from toast.math.vector import Vector2D
from toast.math.matrix import MatrixHelper
from toast.scene_graph import Component

class Transform(Component):
    def __init__(self):
        super(Transform, self).__init__()
        
        self.__local_matrix = None
        self.global_matrix = None
        
        self.__position = Vector2D.Zero()
        self.__rotation = 0
        self.__scale = Vector2D(1.0, 1.0)
        
    @property
    def matrix(self):
        if self.__local_matrix == None:
            t = MatrixHelper.translation_matrix(int(self.__position[0]), int(self.__position[1]))
            r = MatrixHelper.rotation_matrix(self.__rotation)
            s = MatrixHelper.scale_matrix(self.__scale[0], self.__scale[1])
            
            self.__local_matrix = t * r * s
            
        if self.global_matrix == None:
            if hasattr(self.game_object.parent, 'transform'):
                p = self.game_object.parent.transform.matrix
                self.global_matrix = p * self.__local_matrix
            else:
                return self.__local_matrix
            
        return self.global_matrix
    
    def mark_dirty(self):
        if not self.game_object:
            return
        
        self.global_matrix = None
        self.__local_matrix = None
        
        for child_transform in [c.transform for c in self.game_object.children]:
            child_transform.mark_dirty()
    
    @property
    def position(self):
        return Vector2D(self.matrix[0][2], self.matrix[1][2])
    
    @position.setter
    def position(self, other):
        self.__position = Vector2D(other[0], other[1])
        self.mark_dirty()
        
    @property
    def rotation(self):
        a = self.matrix * Vector2D(1, 0)
        b = self.position
        return (a - b).angle
    
    @rotation.setter
    def rotation(self, rotation):
        self.__rotation = rotation * 0.0174532925
        self.mark_dirty()
        
    @property
    def scale(self):
        sx = (self.matrix * Vector2D(1, 0)) - self.position
        sy = (self.matrix * Vector2D(0, 1)) - self.position
        
        return Vector2D(sx.magnitude, sy.magnitude)
    
    @scale.setter
    def scale(self, scale):
        self.__scale = scale
        self.mark_dirty()
        
    @property
    def forward(self):
        f = Vector2D.from_angle(self.rotation)
        f[1] = -f[1]
        return f
    
    @property
    def right(self):
        r = Vector2D.from_angle(self.rotation - 90.0)
        r[1] = -r[1]
        return r
    
    @property
    def offset(self):
        return self.__offset
    
    def look_at(self, pos):
        angle = (pos - self.position).angle
        self.rotation = -angle