import math
import wrapper


class WavyText(wrapper.Wrapper):
    def __init__(self, internal):
        wrapper.Wrapper.__init__(self, internal)
        self.amplitude = self.internal.char_list[0][1].height / 2
        self.frequency = 1
        self.phaseStep = 1
    
    def update(self, time=16):
        """A simple harmonic motion function.

        :param time: The amount of time lapsed since the last call to update.
        """

        self.internal._update_chars(time)
        self.char_list = self.internal.char_list
        
        phase = 0
        
        for (_, rect) in self.char_list:
            rect.top += self.displacement(self.amplitude, self.frequency, self.internal.time / 1000.0, phase)
            phase -= self.phaseStep

    def displacement(self, amplitude, frequency, time, phase):
        """A simple harmonic motion function.
        :returns: Vertical displacement
        """

        return amplitude * math.cos((2 * math.pi * frequency * time) + phase)
