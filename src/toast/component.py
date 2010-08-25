class Component(object):
    def __init__(self):
        self.__children = []
        self.index = 0
    
    def __iter__(self):
        return self
    
    def next(self):
        if self.index >= len(self.__children):
            self.index = 0
            raise StopIteration
        
        self.index += 1
        return self.__children[self.index - 1]
    
    def __getitem__(self, key):
        return self.__children[key]
    
    def update(self, milliseconds=0):
        for child in self.__children:
            try:
                child.update(milliseconds)
            except:
                pass
            
    def render(self, surface, offset):
        for child in self.__children:
            if not hasattr(child, 'add_renderable') and hasattr(child, 'render'):
                child.render(surface, offset)
            
    def add(self, child):
        #if hasattr(child, 'update'):
        if child != None:
            self.__children.append(child)
            
    def remove(self, child):
        self.__children.remove(child)