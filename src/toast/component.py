import weakref

class Component(object):
    __component_list = []
    
    def __init__(self):
        self.__children = []
        self.__parent = None
        self.index = 0
        
    @property
    def parent(self):
        return self.__parent()
    
    @parent.setter
    def parent(self, object):
        self.__parent = weakref.ref(object)
    
    def __iter__(self):
        return self
    
    def next(self):
        if self.index >= len(self.__children):
            self.index = 0
            raise StopIteration
        
        self.index += 1
        return self.__children[self.index - 1]()
    
    def __getitem__(self, key):
        return self.__children[key]()
    
    def update(self, milliseconds=0):
        #for child in [x for x in self.__children if hasattr(x, 'update')]:
        for child in self:
            if hasattr(child, 'update'):
                child.update(milliseconds)
            
    def render(self, surface, offset):
        for child in self.__children:
            if not hasattr(child(), 'add_renderable') and hasattr(child(), 'render'):
                child().render(surface, offset)
            
    def add(self, child):
        #if hasattr(child, 'update'):
        if child != None:
            if child in self.__component_list:
                raise ComponentException('Error: Trying to add a duplicate component.')
                
            self.__component_list.append(child)
                
            self.__children.append(weakref.ref(child))
            
            if hasattr(child, 'parent'):
                child.parent = self
            
    def remove(self, child):
        if child not in self.__component_list:
            raise ComponentException('Error: Trying to remove a component not in the scenegraph.')
            
        self.__component_list.remove(child)
        self.__children.remove(weakref.ref(child))

        
class ComponentException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
        #if self in child.parent:
        #    child.parent.remove(self)