import weakref

class Component(object):
    __component_list = []
    
    def __init__(self, object_to_wrap=None):
        self.__children = []
        self.__parent = None
        self.added = False
        self.index = 0
        
        self.__component_list.append(self)
            
        
    @property
    def parent(self):
        if self.__parent is None:
            return None
        
        return self.__parent()
    
    @parent.setter
    def parent(self, object):
        self.__parent = weakref.ref(object)
        
    def is_a_component(self):
        return True
    
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
        if child != None:
            #Handle the case of adding a non-component. Should this even be
            #supported?
            if child not in self.__component_list:
                self.__component_list.append(child)
            
            self.__children.append(weakref.ref(child))
            
            if hasattr(child, 'parent'):
                child.parent = self
            
    def remove(self, target=None):
        
        #Default to self if target is None.
        if target == None:
            target = self
            
        #Check if the object we're trying to remove is valid
        if (target not in Component.__component_list) and (weakref.ref(target) not in self.__children):
            raise ComponentException('Error: Trying to remove a component not in the scenegraph.')
        
        if target in Component.__component_list:
            Component.__component_list.remove(target)
        
        #If removing this component...
        if self is target:
            if target.parent != None:
                target.parent.remove(target)
            
            for child in [x for x in self]:
                child.remove()
        #...otherwise remove the appropriate child.
        else:
            self.__children.remove(weakref.ref(target))

        
class ComponentException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
        #if self in child.parent:
        #    child.parent.remove(self)