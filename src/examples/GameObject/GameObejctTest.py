from toast.game_object import GameObject
from toast.component import Component

class VerboseGameObject(GameObject):
    def __init__(self, name):
        GameObject.__init__(self)
        self.name = name
        
    def parentName(self):
        return self.parent.name if self.parent is not None else 'None'
        
    def update(self, milliseconds=0):
        print '<VerboseGameObject (name:' + self.name + ', parent:' + self.parentName() + ')>'
        GameObject.update(self, milliseconds)
        
    def remove(self, target):
        print 'Removing GameObject: ' + target.name + ' from GameObject: ' + self.name
        GameObject.remove(self, target)
        
class VerboseComponent(Component):
    def __init__(self, name):
        Component.__init__(self)
        self.name = name
        
    def update(self, milliseconds=0):
        print '   <VerboseComponent (name:' + self.name + ', game object:' + self.game_object.name + ')>'
        Component.update(self, milliseconds)
    
    def remove(self, target=None):
        if target is None:
            target = self
            
        print 'Removing Component: ' + target.name + ' from Component: ' + self.name
        Component.remove(self, target)
        

A = VerboseGameObject('GameObject A')
B = VerboseGameObject('GameObject B')
C = VerboseGameObject('GameObject C')

D = VerboseComponent('Component D')
E = VerboseComponent('Component E')
F = VerboseComponent('Component f')

A.add(B)
B.add(C)

A.add(D)
A.add(E)
B.add(F)

# Verify re-parenting a game object
B.remove(C)
A.add(C)

A.update()