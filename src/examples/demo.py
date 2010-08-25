import pygame

class Demo(object):
    def __init__(self, resolution, scale=1):
        self.__render_list = []
        self.__update_list = []
        
        # Setup pygame display
        pygame.display.set_mode((resolution[0] * scale, resolution[1] * scale))
        # Get a surface the size of the window
        self.screen = pygame.display.get_surface()
        self.resolution = resolution
        self.buffer = pygame.Surface(self.resolution)
        self.render_target = self.screen
        self.offset = (0, 0)
        
        if scale != 1:
            self.render_target = self.buffer
        
        # Get the pygame clock
        self.clock = pygame.time.Clock()
    
    def add_renderable(self, renderable):
        if hasattr(renderable, 'render'):
            self.__render_list.append(renderable)
        else:
            print('Warning: ' + str(renderable) + 'is not a renderable object')
            
        if hasattr(renderable, 'update'):
            self.__update_list.append(renderable)
            
    def run(self):
        # Game loop
        running = True
        while running:
            self.clock.tick(60)
            self.render_target.fill((0,0,0))
            
            for renderable in self.__update_list:
                renderable.update()
            
            for renderable in self.__render_list:
                renderable.render(self.render_target, self.offset)
            
            # Scale up buffer and draw to screen
            if self.render_target != self.screen:
                self.screen.blit(pygame.transform.scale(self.render_target, (self.screen.get_width(), self.screen.get_height())), (0,0) )
            pygame.display.flip()
        
            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        pass
