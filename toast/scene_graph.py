"""
The scene_graph module provides two core data structures that form the 
foundation of how the scene is presented and manipulated. Chief of these is 
the GameObject, which can be any entity with an audio or visual  
representation. Paired with the GameObject is the Component, which implements
behavior for the GameObject. A number of Components may be attached to a
GameObject to describe complex behavior.
"""
import weakref

class Component(object):
    """The Component object serves as a base class for implementing behavior 
    for GameObjects. The attached GameObject is accessed via the game_object 
    property, and is manipulated during the Component's update method.
    Multiple Components can be added to a GameObject and behave in a composite 
    manner.
    
    >>> p = PlayerObject()
    >>> p.add(PlayerControllerComponent())
    >>> p.add(BlinkWhenHealthLessThan(10))
    """
    def __init__(self):
        self.__game_object = None
        self.added = False
        self.index = 0
        
    @property
    def game_object(self):
        """The GameObject the Component is attached to.
        
        :returns: GameObject. -- The GameObject the Component is attached to.
        """
        return None if self.__game_object is None else self.__game_object()
    
    @game_object.setter
    def game_object(self, other):
        """Set the GameObject to the given.
        
        :returns: GameObject. -- The GameObject the Component is attached to.
        """
        self.__game_object = weakref.ref(other)
        
    def is_a_component(self, other=None):
        """Determines if the given object is a Component.
        
        :param other: Any object. Self if other is None.
        :type other: object.
        :returns: bool. -- True if other or self is a Component object.
        """
        return hasattr(other, 'is_a_component') if other is not None else True
    
    def awake(self):
        """Called when added to a GameObject, but after the Scene has been
        constructed.
        """
        pass
    
    def update(self, milliseconds=0):
        """
        :param milliseconds: The timestep for the current update cycle.
        :type milliseconds: int.
        """
        pass
    
class ComponentException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)

class GameObject(object):
    """The GameObject serves as a base class for implementing entites in the 
    game. This can be any entity that has an audio or visual representation. 
    GameObject behavior is implemented via Components which promotes 
    modularity and composition. GameObjects may be added as children to other 
    GameObjects.
    
    >>> p = PlanetObject()
    >>> s = SatelliteObject()
    >>> m = MoonObject()
    >>>
    >>> s.add(OrbitBehavior(p, 10)
    >>> m.add(OrbitBehavior(p, 50)
    >>>
    >>> p.add(s)
    >>> p.add(m)
    """
    def __init__(self):
        self.__children = []
        self.__components = []
        self.__parent = None
        self.added = False
        self.index = 0
        
    @property
    def children(self):
        """A list of the child GameObjects.
        
        :returns: list. -- A list of child GameObjects.
        """
        return self.__children
    
    @property
    def components(self):
        """A list of attached Components.
        
        :returns: list. -- A list of attached Components.
        """
        return self.__components
    
    @property
    def parent(self):
        """The parent GameObject.
        
        :returns: GameObject. -- The parent of this GameObject.
        """
        return None if self.__parent is None else self.__parent()
    
    @parent.setter
    def parent(self, other):
        if other is not None:
            self.__parent = weakref.ref(other)
        else:
            self.__parent = None
        
    def is_a_game_object(self, other=None):
        """Determines if the given object is a GameObject.
        
        :param other: Any object. Self if other is None.
        :type other: object.
        :returns: bool. -- True if other or self is a GameObject.
        """
        return hasattr(other, 'is_a_game_object') if other is not None else True
    
    def awake(self):
        """ Called when added to a GameObject, but after the Scene has been
        constructed.
        """
        for child in self.children:
            child.awake()
    
    def update(self, milliseconds=0):
        """
        :param milliseconds: The timestep for the current update cycle.
        :type milliseconds: int.
        """
        for component in self.components:
            component.update(milliseconds)
            
        for child in self.children:
            child.update(milliseconds)
            
    def add(self, child):
        """Adds the given GameOjbect as a child.
        
        :param child: Adds a GameObject as a child.
        :type child: GameObject.
        """
        if child is None:
            return
        
        if hasattr(child, 'is_a_component'):
            self.__add_component(child)
            child.awake()
            
        elif hasattr(child, 'is_a_game_object'):
            self.__add_child(child)
            
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
        
    def remove(self, child=None):
        """Removes the given object or self if no parameters are supplied.
        
        :param child: Removes the given GameObject or self if child is None.
        :type child: GameObject.
        """
        if child is None or child is self:
            if self.parent:
                self.parent.remove(self)
        
        elif hasattr(child, 'is_a_component'):
            self.__remove_component(child)
            
        else:
            self.__remove_child(child)
            
    def __remove_component(self, component):
        self.components.remove(component)
    
    def __remove_child(self, child):
        self.__children.remove(child)
        child.parent = None
        
    def get_component(self, class_name):
        """Get the first Component with the given class name.
        
        :param class_name: The class name of the Component to return.
        :type class_name: string.
        :returns: Component. -- The first Component with the given class name.
        """
        for component in self.components:
            if component.__class__.__name__ == class_name:
                return component
            
    def get_child(self, class_name):
        """Gets the first GameObject with the given class name.
        
        :param class_name: The class name of the GameObject to return.
        :type class_name: string.
        :returns: Component. -- The first GameObject with the given class name.
        """
        for child in self.children:
            if child.__class__.__name__ == class_name:
                return child
    
class GameObjectException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
    
class Scene(GameObject):
    """ Scene docstring. """
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
        """Draw the scene to the given Surface.
        
        :param surface: A target surface to render the Scene to.
        :type surface: pygame.Surface.
        :param offset: The amount to dipslace the Scene. Mostly used by the Camera.
        :type offset: tuple.
        """
        for child in [c for c in self.children if hasattr(c, 'render')]:
            child.render(surface, offset)