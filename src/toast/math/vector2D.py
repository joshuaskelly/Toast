"""
" * Vector2D.py
" * Copyright (C) 2009 Joshua Skelton
" *                    joshua.skelton@gmail.com
" *
" * This program is free software; you can redistribute it and/or
" * modify it as you see fit.
" *
" * This program is distributed in the hope that it will be useful,
" * but WITHOUT ANY WARRANTY; without even the implied warranty of
" * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
" *
"""
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
            raise IndexError('Error: Index ' + str(index) + ' is out of range.')
        
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError('Error: Index ' + str(index) + ' is out of range.')
        
    def __repr__(self):
        return 'Vector2D(%s, %s)' % (self.x,self.y)
    
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
        
    def __mul__(self, other):
            """
            " * Scalar Multiplication
            " *   other  Stricly a scalar.
            """
            if hasattr(other, '__getitem__') and len(other) == 2:
                raise "Ambiguity: Use Dot() or Cross() to compute the respective products."
            
            return Vector2D(self.x * other, self.y * other)
        
    __rmul__ = __mul__
    
    def __div__(self, other):
            """
            " * Scalar Division
            " *   other  Stricly a scalar
            """
            if hasattr(other, '__getitem__') and len(other) == 2:
                raise "Ambiguity: Division of two vectors is not well-defined."
           
            return Vector2D(self.x / other, self.y / other)
        
    def __neg__(self):
        return Vector2D( -self.x , -self.y)
    
    def __pos__(self):
        return Vector2D( self.x , self.y)
    
    def Dot(self, other):
            """
            " * Dot Product
            " *   other  A vector or triple
            """
            return float(self.x * other[0] + self.y * other[1])
        
    def Cross(self, other):
            """
            " * Cross Product
            " *   other  A vector or triple
            """
            return Vector2D(0, 0, self.x * other[1] - self.y * other[0])
    
    def GetLength(self):
        return sqrt(self.Dot(self))
    
    def GetUnit(self):
        """
        " * GetUnit
        " *   Returns: A vector of length one in the direction of self.
        """
        length = self.GetLength()
        if length != 0:
            return self / length
        return Vector2D(self)
    
    GetNormalized = GetUnit
    
    def GetAngle(self):
        if self.x == self.y == 0:
            return 0
        else:
            return degrees(atan2(self.y, self.x))
        
    def GetPerpendicular(self):
        return Vector2D(-self.y, self.x)
    
    @property
    @staticmethod
    def Zero():
        return Vector2D(0, 0)
    
    @staticmethod
    def UnitVectorFromAngle(angle):
        r = radians(angle)
        c = cos(r)
        s = sin(r)
        
        return Vector2D(c, s)

i = Vector2D(1,0)

j = Vector2D(0,1)


