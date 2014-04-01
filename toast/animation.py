from toast.scene_graph import Component

class Animation(Component):
    def __init__(self, key=None, frames=None):
        super(Animation, self).__init__()
        
        self.__animation_list = {}
        self.key = ''
        self.__current_image = None
        self.__index = 0
        self.__time = 0
        
        if key != None:
            self.add_animation(key, frames)
        
    def update(self, time=0):
        if self.key:
            self.__time += time
            
            self.__current_image, duration, callback = self.frame
            
            if hasattr(self.game_object, 'image'):
                self.game_object.image = self.image
            
            if self.__time > duration:
                self.__time = 0
                self.__index +=1
                
                if callback:
                    callback()
                
    def add_animation(self, key, frames):
        if not self.key:
            self.key = key
            self.__current_image = frames[0][0]
            
        self.__animation_list[key] = frames
    
    @property
    def image(self):
        """ Returns the current image of the playing animation"""
        return self.__current_image
    
    @property
    def key(self):
        """ Returns the key of the playing animation """
        return self.__current_animation
    
    @key.setter
    def key(self, value):
        self.__current_animation = value
    
    @property
    def index(self):
        """ Returns the current index of the playing animation """
        if self.__index > len(self.__animation_list[self.key]) - 1:
            self.__index = 0
            
        return self.__index
    
    @property
    def frame(self):
        """ Returns the current frame as a triple """
        animation = self.__animation_list[self.key][self.index]
        image = animation[0]
        duration = animation[1]
        callback = None
        
        if len(animation) == 3:
            callback = self.__animation_list[self.key][self.index][2]
        
        return image, duration, callback
        
    def play(self, key, start_index=None):
        self.key = key
        
        if start_index != None:
            self.__index = start_index
        
    def stop(self):
        self.key = ''
        self.__index = 0
