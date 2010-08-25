class Physics(object):
    shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.shared_state
        self.__name = ""
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value