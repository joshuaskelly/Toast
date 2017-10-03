import pygame
import random

from toast.quadtree import QuadTree
from toast.scene_graph import GameObject, Scene
from toast.camera import Camera
from toast.event_manager import EventManager

from examples.demo_game import DemoGame

class QuadTreeVisualizer(GameObject):
    def __init__(self, quadtree):
        super(QuadTreeVisualizer, self).__init__()
        
        self.quadtree = quadtree
        
    def render(self, surface, offset=(0,0)):
        self.render_quadtree(surface, self.quadtree)
        
    def render_quadtree(self, surface, quadtree):
        pygame.draw.rect(surface, (255,0,0), quadtree.quadrant, 1)
        if quadtree.bucket is not []:
            for item in quadtree.bucket:
                item.render(surface)
        
        if quadtree.northwest_tree is not None:
            self.render_quadtree(surface, quadtree.northwest_tree)
        if quadtree.northeast_tree is not None:
            self.render_quadtree(surface, quadtree.northeast_tree)
        if quadtree.southwest_tree is not None:
            self.render_quadtree(surface, quadtree.southwest_tree)
        if quadtree.southeast_tree is not None:
            self.render_quadtree(surface, quadtree.southeast_tree)
        
class RectComponent(GameObject):
    def __init__(self, left, top, width, height):
        super(RectComponent, self).__init__()
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.__index = 0
        self.color = 255, 255, 255
        
    def __iter__(self):
        return self
    
    def next(self):
        if self.__index >= 4:
            self.__index = 0
            raise StopIteration
        
        self.__index += 1
        return self[self.__index - 1]
        
    def __getitem__(self, index):
        if index == 0:
            return self.left
        if index == 1:
            return self.top
        if index == 2:
            return self.width
        if index == 3:
            return self.height
        
    def render(self, surface, offset=(0,0)):
        rect = self.left, self.top, self.width, self.height
        
        pygame.draw.rect(surface, self.color, rect, 1)
        
        
class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()
        
        EventManager.subscribe(self, 'onMouseMotion')
        EventManager.subscribe(self, 'onMouseDown')
        
        Camera.current_camera.viewport = 512, 512
        Camera.current_camera.position = 256, 256
        Camera.current_camera.clear_color = 0, 0, 0
        
        w = h = 2**9
        self.region = (0,0,w,h)
        
        self.last_hits = []
        self.items = []
        
        self.use_quadtree_collision = True
        
        for _ in range(250):
            x = random.randint(0, 480)
            y = random.randint(0, 480)
            w = random.randint(4, 32)
            h = random.randint(4, 32)
            
            r = RectComponent(x,y,w,h)
            self.items.append(r)
        
        self.quadtree_visualizer = QuadTreeVisualizer(QuadTree(self.items, self.region))
        self.add(self.quadtree_visualizer)
        
    def update(self, milliseconds=0):
        super(NewScene, self).update(milliseconds)
        
        self.quadtree_visualizer.quadtree = QuadTree(self.items, self.region)
        
    def onMouseDown(self, event):
        self.use_quadtree_collision = not self.use_quadtree_collision
        if self.use_quadtree_collision:
            print('Using QuadTree Collision Detection')
        else:
            print('Using PyGame Rect Collision')
        
    def onMouseMotion(self, event):
        p = DemoGame.camera_to_world(event.pos)
        
        if self.use_quadtree_collision:
            r = (p[0], p[1], 8, 8)
            current_hits = self.quadtree_visualizer.quadtree.hit(r)
        
        else:
            r = pygame.Rect(p[0], p[1], 8, 8)
            current_hits = []
            indexes = r.collidelistall([pygame.Rect(r[0], r[1], r[2], r[3]) for r in self.items])
            for index in indexes:
                current_hits.append(self.items[index])
        
        for rect in self.last_hits:
            rect.color = 255, 255, 255
        
        for rect in current_hits:
            rect.color = 0, 255, 0
            
        self.last_hits = current_hits

game = DemoGame((512, 512), NewScene)
game.run()
