from Math import Point2D, Vector2D

import math
import pygame

class Joint(object):
    def __init__(self, orig):
        self.offset = 30
        self.velocity = Vector2D.Vector2D(0,0)
        self.angleThreshold = 25
        
        self.position = Point2D.Point2D(orig)
        self.old_position = Point2D.Point2D(0,0)
        self.anchor = orig + Point2D.Point2D(self.offset, 0)
        self.next = None
        self.prev = None
        
    def render(self, surface):
        pygame.draw.circle(surface, (255,255,255), self.position, 5, 1)
        pygame.draw.line(surface, (255,255,255), self.position, self.anchor, 1)
        
        if self.next != None:
            self.next.render(surface)
        
    def update(self):
        vec = self.anchor - self.position
        vec = vec.GetUnit()
        vec *= self.offset
        self.anchor = self.position + vec
        
        if self.get_angle() != None:
            if not(self.get_angle() < self.angleThreshold) and not(self.get_angle() > (360 - self.angleThreshold)):
                
                prevAngle = (self.prev.anchor - self.prev.position).GetAngle()
                thisAngle = (self.anchor - self.position).GetAngle()
                
                if self.get_angle() > 180:
                    vec1 = Vector2D.UnitVectorFromAngle(thisAngle + 5)
                else:
                    vec1 = Vector2D.UnitVectorFromAngle(thisAngle - 5)
                vec1 *= self.offset
                self.anchor = self.position + vec1
        
        if self.next != None:
            self.next.set_position(self.anchor)
            self.next.update()
        
    def attach(self, joint):
        if self.next == None:
            self.next = joint
            joint.prev = self
        else:
            self.next.attach(joint)
            
    def get_angle(self):
        if self.prev != None:
            v1 = self.prev.position - self.position
            v2 = self.position - self.anchor
            
            result = v2.GetAngle() - v1.GetAngle()
            
            if result < 0:
                result += 360
            
            return result
        
    def set_position(self, new_position):
        self.old_position = self.position
        self.position = new_position

    
    
if __name__ == '__main__':
    from pygame.locals import *

    # Define the origin
    ORIGIN = (0,0)
    # Set the screen size
    SCREEN_SIZE = (640, 480)
    
    # Setup pygame display
    pygame.display.set_mode(SCREEN_SIZE)
    # Get a surface the size of the window
    screen = pygame.display.get_surface()
    # Create a buffer to render to
    buffer = pygame.Surface((640, 480))
    
    clock = pygame.time.Clock()
    
    j1 = Joint((10,10))
    
    for i in range(10):
        j = Joint((0,0))
        j1.attach(j)

    
    # Game loop
    running = True
    while running:
        clock.tick(60)
        
        buffer.fill((0,0,0))
        
        # Handle input
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                
            elif event.type == MOUSEMOTION:
                vel = j1.position - Point2D.Point2D(event.pos)
                print vel
                j1.set_position(Point2D.Point2D(event.pos))
            elif event.type == QUIT:
                running = False
                
        j1.update()
        j1.render(buffer)
        
        # Scale up buffer and draw to screen
        screen.blit(pygame.transform.scale(buffer,SCREEN_SIZE), pygame.Rect(ORIGIN,SCREEN_SIZE))
        pygame.display.flip()
