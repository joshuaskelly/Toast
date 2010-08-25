import toast
import pygame

class Game(toast.Scene):
    def initialize_scene(self):
        self.clear_color = (98, 186, 221)
        self.resolution = (640, 480)
        
        level = toast.Level('Data/map2.xml')
        
        self.tilemap = level.get_element_by_ID('Ground')
        
        self.camera = level.get_element_by_ID('Default Camera')
        
        self.scene_root.append(level)
        
        self.add_mouse_button_listener(self)
        
    def mouse_press(self, event):
        pos = map((lambda x: x / 2), event.pos)
        
        rect = self.tilemap.tile_rect_at_pixel(pos)
        d = DrawRect(rect[0], rect[1], rect[2], rect[3])
        
        print self.tilemap.tile_id_at_pixel(pos)
        
        self.camera.add_renderable(d)
    
    def mouse_release(self, event):
        pass

class DrawRect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def render(self, surface, offset):
        pygame.draw.rect(surface, (255,0,0), (self.x, self.y, self.width, self.height), 1)
if __name__ == '__main__':
    g = Game()
    g.run()