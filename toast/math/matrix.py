from math import sin, cos

from toast.math.vector import Vector2D

class Matrix3x3(object):
    def __init__(self, *rows):
        self.__data = rows
        
    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self.__data)
        
    def __getitem__(self, i):
        return self.__data[i]
                
    def __len__(self):
        return 9
                
    def __mul__(self, other):
        try:
            length = len(other)
            
            if length == 2:
                return self.__vector_multiplication(other)
            elif length == 9:
                return self.__matrix_multiplication(other)
            else:
                raise _
            
        except:
            raise TypeError('can\'t multiply Matrix3x3 by type \'{0}\''.format(other.__class__.__name__))
            
    def __scalar_multiplication(self, scalar):
        return Matrix3x3([i * scalar for i in self.__data[0]], \
                         [j * scalar for j in self.__data[1]], \
                         [k * scalar for k in self.__data[2]])
    
    def __vector_multiplication(self, other):
        other = other[0], other[1], 1
        return Vector2D([sum([i * x for i, x in zip(self.__data[0], other)]), \
                         sum([j * y for j, y in zip(self.__data[1], other)])])
    
    def __matrix_multiplication(self, other):
        a = self
        b = other
        
        a00 = a[0][0]
        a01 = a[0][1]
        a02 = a[0][2]
        a10 = a[1][0]
        a11 = a[1][1]
        a12 = a[1][2]
        
        b00 = b[0][0]
        b01 = b[0][1]
        b02 = b[0][2]
        b10 = b[1][0]
        b11 = b[1][1]
        b12 = b[1][2]
        
        return Matrix3x3([a00*b00 + a01*b10, a00*b01 + a01*b11, a00*b02 + a01*b12 + a02], \
                         [a10*b00 + a11*b10, a10*b01 + a11*b11, a10*b02 + a11*b12 + a12], \
                         [0, 0, 1])
    
    def __rmul__(self, other):
        if isinstance(other, (int,float,long)):
            return self.__scalar_multiplication(other)
        raise TypeError('can\'t right multiply Matrix3x3 by a non-scalar type')
    
    @staticmethod
    def Identity():
        return Matrix3x3([1,0,0], \
                         [0,1,0], \
                         [0,0,1])
            

if __name__ == '__main__':
    a = ([1, 0, 0])
    b = ([2, 0, 1])
    
    m = Matrix3x3.Identity()
    
    v = Vector2D(2, 2)
    
    print m
    print 3 * m
    
class MatrixHelper(object):
    @staticmethod
    def rotation_matrix(theta):
        return Matrix3x3([ cos(theta), sin(theta), 0], \
                         [-sin(theta), cos(theta), 0], \
                         [0, 0, 1])
        
    @staticmethod
    def scale_matrix(scale_x, scale_y=None):
        if scale_y is None:
            scale_y = scale_x
            
        return Matrix3x3([scale_x, 0, 0], \
                         [0, scale_y, 0], \
                         [0, 0, 1])
        
    @staticmethod
    def translation_matrix(x, y):
        return Matrix3x3([1, 0, x], \
                         [0, 1, y], \
                         [0, 0, 1])