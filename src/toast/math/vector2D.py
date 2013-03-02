from math import sqrt, degrees, atan2, cos, sin, radians

class Vector2D(object):
    def __init__(self, xOrDouble, y = None):
        if y == None:
            self.x = xOrDouble[0]
            self.y = xOrDouble[1]
        else:
            self.x = xOrDouble
            self.y = y
            
    def __len__(self):
        return 2
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError('Error: Index {0} is out of range.'.format(index))
        
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError('Error: Index {0} is out of range.'.format(index))
        
    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, (self.x, self.y))
    
    def __eq__(self, other):
        if hasattr(other, '__getitem__') and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False
        
    def __ne__(self, other):
        if hasattr(other, '__getitem__') and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True
        
    def __nonzero__(self):
        return self.x or self.y
    
    def __add__(self, other):
        return Vector2D(self.x + other[0], self.y + other[1])
    
    __radd__ = __add__
    
    def __sub__(self, other):
        if hasattr(other, '__getitem__') and len(other) == 2:
            return Vector2D(self.x - other[0], self.y - other[1])
        
    def __rsub__(self, other):
        if hasattr(other, '__getitem__') and len(other) == 2:
            return Vector2D(other[0] - self.x , other[1] - self.y)
        
    def __mul__(self, scalar):
        """ Returns the product of self by other. 
        
        Arguments:
        scalar -- Strictly a scalar value.
        
        """
        if not isinstance(scalar, (int, float, long)):
            if hasattr(scalar, 'Dot'):
                raise TypeError('Unable to multiply Vector2D by type \'{0}\'. Did you mean Dot() or Cross()?'.format(scalar.__class__.__name__))
            else:
                raise TypeError('Unable to multiply Vector2D by type \'{0}\'.'.format(scalar.__class__.__name__))
        
        return Vector2D(self.x * scalar, self.y * scalar)
        
    __rmul__ = __mul__
    
    def __div__(self, scalar):
        """ Returns the quotient of self by other. 
        
        Arguments:
        scalar -- Strictly a scalar value.
        
        """
        if hasattr(scalar, '__getitem__') and len(scalar) == 2:
            raise TypeError('Division of two vectors is not well-defined.')
       
        return Vector2D(self.x / scalar, self.y / scalar)
        
    def __neg__(self):
        return Vector2D( -self.x , -self.y)
    
    def __pos__(self):
        return Vector2D( self.x , self.y)
    
    def Dot(self, other):
        """ Returns the dot product of self by other """
        return float(self.x * other[0] + self.y * other[1])
        
    def Cross(self, other):
        """ Returns the cross product of self by other. """
        return Vector2D(0, 0, self.x * other[1] - self.y * other[0])
    
    def Magnitude(self):
        """ Returns the length of this vector. """
        return sqrt(self.Dot(self))
    
    def MagnitudeSquared(self):
        """ Returns the length of this vector in square space. """
        return self.Dot(self)
    
    def Normalized(self):
        """ Returns a unit vector in the direction of this vector. """
        length = self.Magnitude()
        if length != 0:
            return self / length
        return Vector2D(self)
    
    def GetAngle(self):
        """ Returns the angle of this vector. """
        if self.x == self.y == 0:
            return 0
        else:
            return degrees(atan2(self.y, self.x))
        
    def GetPerpendicular(self):
        return Vector2D(-self.y, self.x)
    
    @staticmethod
    def Zero():
        """ Returns a vector of length zero. """
        return Vector2D(0, 0)
    
    @staticmethod
    def UnitVectorFromAngle(angle):
        """ Returns a unit vector in the direction of angle. """
        return Vector2D(cos(radians(angle)), sin(radians(angle)))

i = Vector2D(1,0)

j = Vector2D(0,1)


