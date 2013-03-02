from toast.game_object_pool import GameObjectPool
from toast.math.vector2D import Vector2D

class Emitter(GameObjectPool):
    def __init__(self, particle_class_name, default_args=(), frequency=0, on_particle_create=None):
        super(Emitter, self).__init__(particle_class_name, default_args)
        
        self.__frequency = frequency
        self.__counter = 0
        self.__on_particle_create = on_particle_create
        self.position = Vector2D(0, 0)
        self.is_emitting = True
        
    def update(self, milliseconds=0):
        super(Emitter, self).update(milliseconds)
        
        if self.is_emitting:
            self.__counter += milliseconds
            
            if self.__counter >= self.__frequency:
                self.__counter = 0
                
                particle = self.getNextAvailable()
                
                if self.__on_particle_create is not None:
                    self.__on_particle_create(self, particle)
            
