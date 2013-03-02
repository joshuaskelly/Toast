import weakref

class Component(object):
    def __init__(self):
        self.__children = []
        self.__parent = None
        self.added = False
        self.index = 0
        
    @property
    def children(self):
        return self.__children
        
    @property
    def parent(self):
        return None if self.__parent is None else self.__parent()
    
    @parent.setter
    def parent(self, other):
        self.__parent = weakref.ref(other)
        
    def is_a_component(self, other=None):
        return hasattr(other, 'is_a_component') if other is not None else True
    
    def update(self, milliseconds=0):
        for child in [c for c in self.__children if hasattr(c, 'update')]:
            child.update(milliseconds)
            
    def add(self, child):
        """ Adds child component. """
        if child is None:
            return
        
        if not self.is_a_component(child):
            message = 'Cannot add a child object that is not a component.'
            raise ComponentException(message)
        
        if child.parent is not None:
            message = 'Cannot add component. {0} is already a child of: {1}'
            message.format(child.__class__.__name__, \
                           child.parent.__class__.__name__)
            raise ComponentException(message)
        
        self.__children.append(child)
        
        if hasattr(child, 'parent'):
            child.parent = self
            
    def remove(self, target=None):
        """ Removes target from self or self from parent. """
        if (target is None or target is self) and self.parent is not None:
            self.parent.remove(self)
                
        else:
            self.__children.remove(target)
            
    def get_component(self, class_name):
        """ Returns first child component with specified class name. """
        for child in self.__children:
            if child.__class__.__name__ == class_name:
                return child
            
    def __del__(self):
        return
        print 'Deleting instance of: {0}'.format(self.__class__.__name__)
            
class ComponentException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
