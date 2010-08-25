import pygame

import toast

class Game(toast.Scene):
    def initialize_scene(self):
        self.clear_color = (98, 186, 221)
        self.resolution = (640, 480)
        
        level = toast.Level('Data/map2.xml')
        self.scene_root.append(level)
        
        self.camera = level.get_element_by_ID('Default Camera')
        
        self.add_keyboard_listener(self)

        
    key_press = lambda self, event: pygame.event.post(pygame.event.Event(pygame.QUIT))
    key_release = key_press
    
        
if __name__ == '__main__':
    g = Game()
    g.run()