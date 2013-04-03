from toast.game import Game

class Timer(object):
    def __init__(self, interval):
        self.__interval = interval
        self.reset()
        
    def is_time_up(self):
        return Game.time() > self.__time_up
    
    def reset(self):
        self.__time_up = Game.time() + self.__interval