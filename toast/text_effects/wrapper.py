import math
from toast.scene_graph import Component


class Wrapper(Component):
    def __init__(self, internal):
        """This class provides a base class for text effect wrappers.
        Subclasses simply need to override the update method to implement the
        desired effect.

        :params internal: A text object to wrap around.
        """
        super(Wrapper, self).__init__()
        
        self.internal = internal
        self.char_list = []
        internal.add(self)

    def update(self, time=0.01667):
        """A method that describes how the text object is transformed as a
        function of time.

        :param time: The amount of time lapsed since the last update.
        """
        
        raise "Instances of Wrapper can not be created." 
        
    def render(self, surface, offset=(0,0)):
        self.internal.render(surface, offset)
        
    def displacement(self, amplitude, frequency, time, phase):
        return amplitude * math.cos((2 * math.pi * frequency * time) + phase)

    @property
    def position(self):
        return self.internal.position

    @position.setter
    def position(self, position):
        self.internal.position = position

    @property
    def time(self):
        return self.internal.time

    @time.setter
    def time(self, time):
        self.internal.time = time
