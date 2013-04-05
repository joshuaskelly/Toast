import weakref

class Component(object):
    def __init__(self):
        self.__game_object = None
        self.added = False
        self.index = 0
        
    @property
    def game_object(self):
        return None if self.__game_object is None else self.__game_object()
    
    @game_object.setter
    def game_object(self, other):
        self.__game_object = weakref.ref(other)
        
    def is_a_component(self, other=None):
        return hasattr(other, 'is_a_component') if other is not None else True
    
    def awake(self):
        pass
    
    def update(self, milliseconds=0):
        pass
    
class ComponentException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)

class GameObject(object):
    def __init__(self):
        self.__children = []
        self.__components = []
        self.__parent = None
        self.added = False
        self.index = 0
        
    @property
    def children(self):
        return self.__children
    
    @property
    def components(self):
        return self.__components
    
    @property
    def parent(self):
        return None if self.__parent is None else self.__parent()
    
    @parent.setter
    def parent(self, other):
        if other is not None:
            self.__parent = weakref.ref(other)
        else:
            self.__parent = None
        
    def is_a_game_object(self, other=None):
        return hasattr(other, 'is_a_game_object') if other is not None else True
    
    def awake(self):
        for child in self.children:
            child.awake()
    
    def update(self, milliseconds=0):
        for component in self.components:
            component.update(milliseconds)
            
        for child in self.children:
            child.update(milliseconds)
            
    def add(self, child_or_component):
        """ Adds either a child game object, or a component """
        if child_or_component is None:
            return
        
        if hasattr(child_or_component, 'is_a_component'):
            self.__add_component(child_or_component)
            child_or_component.awake()
            
        elif hasattr(child_or_component, 'is_a_game_object'):
            self.__add_child(child_or_component)
            
        else:
            message = 'Cannot add an object that is not either a component or game object.'
            raise GameObjectException(message)
        
    def __add_component(self, component):
        if component.game_object is not None:
            message = 'Cannot add component. {0} has already been added to: {1}'
            message.format(component.__class__.__name__,
                           component.game_object.__class__.__name__)
            raise ComponentException(message)
        
        self.components.append(component)
        component.game_object = self
        
    def __add_child(self, child):
        if child.parent is not None:
            message = 'Cannot add game object. {0} is already a child of {1}'
            message.format(child.__class__.__name__, \
                           child.parent.__class__.__name__)
            raise GameObjectException(message)
        
        self.children.append(child)
        child.parent = self
        
    def remove(self, child_or_component=None):
        """ Removes either a child game object, or a component """
        if child_or_component is None or child_or_component is self:
            if self.parent:
                self.parent.remove(self)
        
        elif hasattr(child_or_component, 'is_a_component'):
            self.__remove_component(child_or_component)
            
        else:
            self.__remove_child(child_or_component)
            
    def __remove_component(self, component):
        self.components.remove(component)
    
    def __remove_child(self, child):
        self.__children.remove(child)
        child.parent = None
        
    def get_component(self, class_name):
        """ Returns first component with specified class name. """
        for component in self.components:
            if component.__class__.__name__ == class_name:
                return component
            
    def get_child(self, class_name):
        """ Returns first component with specified class name. """
        for child in self.children:
            if child.__class__.__name__ == class_name:
                return child
    
class GameObjectException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
    
class Scene(GameObject):
    __current_scene = None
    
    def __init__(self):
        super(Scene, self).__init__()
        
        if Scene.current_scene is None:
            Scene.current_scene = self

    @staticmethod      
    def get_current():
        return Scene.__current_scene
    
    @staticmethod
    def set_current(scene):
        Scene.__current_scene = scene
        
    current_scene = property(get_current, set_current)
    
    def render(self, surface, offset=(0,0)):
        for child in [c for c in self.children if hasattr(c, 'render')]:
            child.render(surface, offset)