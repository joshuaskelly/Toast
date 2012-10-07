import new

from toast.component import Component, ComponentException

class ComponentPool(Component):
    def __init__(self, class_name, default_args=(), initial_size=0):
        super(ComponentPool, self).__init__()
        self.__class_name = class_name
        self.__default_args = default_args
        
        #Hijack parent class' child list.
        self.__children = self._Component__children
        
        for _ in range(initial_size):
            instance = self.__getNewInstance(*default_args)
            instance.dead = True
            
    def __len__(self):
        return len(self.__children)
        
    def update(self, milliseconds=0):
        for child in self.__children:
            if hasattr(child, 'update') and not child.dead:
                child.update(milliseconds)
                
    def render(self, surface, offset=(0,0)):
        for child in self.__children:
            if hasattr(child, 'render') and not child.dead:
                child.render(surface, offset)
    
    def add(self, child):
        raise ComponentException('Cannot add a child to a Component Pool.')
    
    def __add(self, child):
        if not self.is_a_component(child):
            raise ComponentException('Cannot add a child object that is not a component.')
        
        if child != None:
            self.__children.append(child)
            
            if hasattr(child, 'parent'):
                child.parent = self
    
    def __getNewInstance(self, *args):
        instance = self.__class_name(*args)
        instance.dead = False
        #instance.remove = new.instancemethod(override_remove, instance, None)
        self.__add(instance)
        
        return instance
    
    def getNextAvailable(self):
        for child in self.__children:
            if child.dead:
                child.dead = False
                return child
            
        return self.__getNewInstance(*self.__default_args)
    
    def has_child_alive(self):
        return len([child for child in self.__children if not child.dead]) != 0
            
    
def override_remove(self, target=None):
    self.dead = True