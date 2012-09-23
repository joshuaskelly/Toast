import weakref

class Component(object):
    def __init__(self):
        self.__children = []
        self.__parent = None
        self.added = False
        self.index = 0
        
    @property
    def parent(self):
        if self.__parent is None:
            return None
        
        return self.__parent()
    
    @parent.setter
    def parent(self, object):
        self.__parent = weakref.ref(object)
        
    def is_a_component(self, other=None):
        if other is not None:
            return hasattr(other,'is_a_component')
        return True
    
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
        for child in self:
            if hasattr(child, 'update'):
                child.update(milliseconds)
            
#    def render(self, surface, offset):
#        for child in self.__children:
#            if not hasattr(child, 'add_renderable') and hasattr(child, 'render'):
#                child.render(surface, offset)
            
    def add(self, child):
        if not self.is_a_component(child):
            raise ComponentException('Cannot add a child object that is not a component.')
        
        if child != None:
            self.__children.append(child)
            
            if hasattr(child, 'parent'):
                child.parent = self
            
    def remove(self, target=None):
        
        #Default to self if target is None.
        if target is None or target is self:
            if target.parent != None:
                target.parent.remove(self)
            
            for child in [x for x in self]:
                child.remove()
                
        #...otherwise remove the appropriate child.
        else:
            self.__children.remove(target)

        
class ComponentException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
        #if self in child.parent:
        #    child.parent.remove(self)