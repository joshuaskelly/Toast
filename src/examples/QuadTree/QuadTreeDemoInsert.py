import pygame
import random

from toast.quadtree import QuadTree
from toast.component import Component
from toast.scene import Scene
from toast.camera import Camera
from toast.event_manager import EventManager

from examples.demo_game import DemoGame

class QuadTreeVisualizer(Component):
    def __init__(self, quadtree):
        super(QuadTreeVisualizer, self).__init__()
        
        self.quadtree = quadtree
        
    def render(self, surface, offset=(0,0)):
        self.render_quadtree(surface, self.quadtree)
        
    def render_quadtree(self, surface, quadtree):
        pygame.draw.rect(surface, (255,0,0), quadtree.quadrant, 1)

        
        if quadtree.northwest_tree:
            self.render_quadtree(surface, quadtree.northwest_tree)
        if quadtree.northeast_tree:
            self.render_quadtree(surface, quadtree.northeast_tree)
        if quadtree.southwest_tree:
            self.render_quadtree(surface, quadtree.southwest_tree)
        if quadtree.southeast_tree:
            self.render_quadtree(surface, quadtree.southeast_tree)
            
        if quadtree.bucket is not []:
            for item in quadtree.bucket:
                item.render(surface)
            
class RectComponent(Component):
    def __init__(self, left, top, width, height):
        super(RectComponent, self).__init__()
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        
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
        pygame.draw.rect(surface, (255,255,255), rect, 1)
        
class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()
        EventManager.subscribe(self, 'onMouseDown')
        
        Camera.current_camera.viewport = 512, 512
        Camera.current_camera.position = 256, 256
        
        w = h = 2**9
        region = (0,0,w,h)
        
        self.quadtree = QuadTree([], region)
        
        self.add(QuadTreeVisualizer(self.quadtree))
        
    def onMouseDown(self, event):
        if event.button is 1:
            p = DemoGame.camera_to_world(event.pos)
            
            d = 2 ** random.randint(1,5)
            self.quadtree.insert(RectComponent(p[0], p[1], d, d))

game = DemoGame((512, 512), NewScene)
game.run()
