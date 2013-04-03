import pygame
from toast.math.math_helper import MathHelper

class Gradient(object):
    @staticmethod
    def createVerticalGradient(dimension, *stops):
        surf = pygame.Surface(dimension)
        width, height = dimension
        
        num_stops = len(stops)
        
        for h in range(height):
            step = float(h) / (height)
            
            # Caclulate the array index
            i = min(int(step * (num_stops - 1)), num_stops - 1)
            
            # Adjust the step to properly blend between the gradient stops.
            grad_step = step * (num_stops - 1) - i
            
            r = MathHelper.Lerp(stops[i][0], stops[i+1][0], grad_step)
            g = MathHelper.Lerp(stops[i][1], stops[i+1][1], grad_step)
            b = MathHelper.Lerp(stops[i][2], stops[i+1][2], grad_step)
            
            pygame.draw.line(surf, (r,g,b), (0, h), (width, h))
            
        return surf
    
    @staticmethod
    def createHorizontalGradient(dimension, *stops):
        surf = pygame.Surface(dimension)
        width, height = dimension
        
        num_stops = len(stops)
        
        for w in range(width):
            step = float(w) / (width)
            
            # Caclulate the array index
            i = min(int(step * (num_stops - 1)), num_stops - 1)
            
            # Adjust the step to properly blend between the gradient stops.
            grad_step = step * (num_stops - 1) - i
            
            r = MathHelper.Lerp(stops[i][0], stops[i+1][0], grad_step)
            g = MathHelper.Lerp(stops[i][1], stops[i+1][1], grad_step)
            b = MathHelper.Lerp(stops[i][2], stops[i+1][2], grad_step)
            
            pygame.draw.line(surf, (r,g,b), (w, 0), (w, height))
            
        return surf