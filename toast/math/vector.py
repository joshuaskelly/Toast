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
        """Returns two as that is the length of a Vector2D as an iterable.
        
        :returns: int. -- The length of the Vector2D as an iterable object.
        """
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
        """Determines if one vector is equal to the other.
        
        :param other: A Vector2D to check for equality.
        :type other: Vector2D.
        :returns: bool. -- True if each x and y are equal.
        """
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
        """Performs vector addition.
        
        :param other: The RHS Vector2D.
        :type other: Vector2D
        :returns: Vector2D. -- The result of this vector added to other.
        """
        return Vector2D(self.x + other[0], self.y + other[1])
    
    __radd__ = __add__
    
    def __sub__(self, other):
        """Performs vector subtraction.
        
        :param other: The RHS Vector2D.
        :type other: Vector2D
        :returns: Vector2D. -- The result of this vector subtracted from other.
        """
        if hasattr(other, '__getitem__') and len(other) == 2:
            return Vector2D(self.x - other[0], self.y - other[1])
        
    def __rsub__(self, other):
        if hasattr(other, '__getitem__') and len(other) == 2:
            return Vector2D(other[0] - self.x , other[1] - self.y)
        
    def __mul__(self, scalar):
        """Performs scalar multiplication.
        
        :param scalar: A scalar.
        :type scalar: numbers.Real
        :returns: Vector2D. -- The product of scalar multiplication.
        """
        if not isinstance(scalar, (int, float, long)):
            if hasattr(scalar, 'dot'):
                raise TypeError('Unable to multiply Vector2D by type \'{0}\'. Did you mean dot() or cross()?'.format(scalar.__class__.__name__))
            else:
                raise TypeError('Unable to multiply Vector2D by type \'{0}\'.'.format(scalar.__class__.__name__))
        
        return Vector2D(self.x * scalar, self.y * scalar)
        
    __rmul__ = __mul__
    
    def __div__(self, scalar):
        """Performs scalar division.
        
        :param scalar: A scalar.
        :type scalar: numbers.Real
        :returns: Vector2D. -- The product of scalar division.
        """
        if hasattr(scalar, '__getitem__') and len(scalar) == 2:
            raise TypeError('Division of two vectors is not well-defined.')
       
        return Vector2D(self.x / scalar, self.y / scalar)
        
    def __neg__(self):
        """Performs unary negation.
        
        :returns: Vector2D. -- This vector negated.
        """
        return Vector2D( -self.x , -self.y)
    
    def __pos__(self):
        """Performs unary plus.
        
        :returns: Vector2D. -- This vector.
        """
        return Vector2D(self.x , self.y)
    
    def dot(self, other):
        """Performs a dot product.
        
        :param other: The RHS Vector2D.
        :type other: Vector2D.
        :returns: The dot product of this by other.
        """
        return float(self.x * other[0] + self.y * other[1])
        
    def cross(self, other):
        """Performs a cross product.
        
        :param other: The RHS Vector2D.
        :type other: Vector2D.
        :returns: The cross product of this by other.
        """
        return Vector2D(0, 0, self.x * other[1] - self.y * other[0])
    
    @property
    def magnitude(self):
        """The length of this vector. """
        return sqrt(self.dot(self))
    
    @property
    def magnitude_squared(self):
        """The length of this vector in square space. """
        return self.dot(self)
    
    def normalized(self):
        """Gets a unit vector in the direction of this vector. 
        
        :returns: Vector2D -- A vector of length one in the direction of this.
        """
        length = self.magnitude
        if length != 0:
            return self / length
        return Vector2D(self)
    
    @property
    def angle(self):
        """ Gets the angle of this vector with respect to Vector2D(1, 0).
        
        :returns: float -- The angle of this vector with respect to Vector2D(1, 0).
        """
        if self.x == self.y == 0:
            return 0
        else:
            return degrees(atan2(self.y, self.x))
    
    @staticmethod
    def from_angle(angle_in_degrees):
        """ Gets a unit vector in the direction of angle from Vector2D(1, 0).
        
        :param angle_in_degrees: The desired angle with respect to Vector2D(1, 0).
        :type angle_in_degrees: float.
        :returns: Vector2D -- In the desired angle with respect to Vector2D(1, 0).
        """
        return Vector2D(cos(radians(angle_in_degrees)), \
                        sin(radians(angle_in_degrees))).normalized()
    
    @staticmethod
    def Zero():
        """Gets a vector of length zero. Useful for comparisons.
        
        :returns: Vector2D -- The zero vector.
        """
        return Vector2D(0, 0)
