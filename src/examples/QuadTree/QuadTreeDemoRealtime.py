import pygame

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
        self.render_quadtree(surface, 0, self.quadtree)
        
    def render_quadtree(self, surface,color, quadtree):
        pygame.draw.rect(surface, (color,color,color), quadtree.quadrant, 0)
        pygame.draw.rect(surface, (255 - color,255 - color,255 - color), quadtree.quadrant, 1)
        
        if quadtree.northwest_tree:
            self.render_quadtree(surface, color + 32, quadtree.northwest_tree)
        if quadtree.northeast_tree:
            self.render_quadtree(surface, color + 32, quadtree.northeast_tree)
        if quadtree.southwest_tree:
            self.render_quadtree(surface, color + 32, quadtree.southwest_tree)
        if quadtree.southeast_tree:
            self.render_quadtree(surface, color + 32, quadtree.southeast_tree)
    
class NewScene(Scene):
    def __init__(self):
        super(NewScene, self).__init__()
        EventManager.subscribe(self, 'onMouseMotion')
        
        Camera.current_camera.viewport = 512, 512
        Camera.current_camera.position = 256, 256
        
        w = h = 512
        region = (0,0,w,h)
        
        self.quadtree_visualizer = QuadTreeVisualizer(QuadTree([], region))
        self.add(self.quadtree_visualizer)
        
    def onMouseMotion(self, event):
        p = DemoGame.camera_to_world(event.pos)
        r = (p[0], p[1], 1, 1)
        
        self.quadtree_visualizer.quadtree = QuadTree([r], (0,0,512,512))

game = DemoGame((512, 512), NewScene)
game.run()
