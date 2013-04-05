import new

from toast.scene_graph import GameObject, GameObjectException

class GameObjectPool(GameObject):
    def __init__(self, class_name, default_args=(), initial_size=0):
        super(GameObjectPool, self).__init__()
        self.__class_name = class_name
        self.__default_args = default_args
        
        #Hijack parent class' child list.
        self.__children = self._GameObject__children
        self.__limit_instances = False
        
        if initial_size > 0:
            self.__limit_instances = True
            
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
        raise GameObjectException('Cannot add a child to a Component Pool.')
    
    def __add(self, child):
        if not self.is_a_game_object(child):
            raise GameObjectException('Cannot add a child object that is not a game object.')
        
        if child != None:
            self.__children.append(child)
            
            if hasattr(child, 'parent'):
                child.parent = self
    
    def __getNewInstance(self, *args):
        instance = self.__class_name(*args)
        instance.dead = False
        
        if self.__limit_instances:
            instance.remove = new.instancemethod(override_remove, instance, None)
            
        self.__add(instance)
        
        return instance
    
    def getNextAvailable(self):
        """ Returns first-available non-dead child. If you are limiting the
        number of instances created, this can possibly return None.
        """
        for child in self.__children:
            if child.dead:
                child.dead = False
                return child
        
        if self.__limit_instances:
            return None
        else:
            return self.__getNewInstance(*self.__default_args)
        
    @property
    def children(self):
        """ Returns a list of non-dead children. """
        return [child for child in self.__children if not child.dead]
    
    def has_child_alive(self):
        """ Returns true if at least one child is not dead. """
        for child in self.children:
            if not child.dead:
                return True
        
        return False
    
def override_remove(self, target=None):
    self.dead = True