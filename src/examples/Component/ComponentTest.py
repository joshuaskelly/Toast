from toast.component import Component

class VerboseComponet(Component):
    def __init__(self, name):
        Component.__init__(self)
        self.name = name
        
    def update(self, milliseconds=0):
        print '<VerboseComponent (name:' + self.name + ', parent:' + self.parentName() + ')>'
        Component.update(self, milliseconds)
        
    def parentName(self):
        if self.parent != None:
            return self.parent.name
        return 'None'
    
    def remove(self, target=None):
        if target is None:
            target = self
            
        print 'Removing Component: ' + target.name + ' from Component: ' + self.name
        Component.remove(self, target)

A = VerboseComponet('ComponentA')
B = VerboseComponet('ComponentB')
C = VerboseComponet('ComponentC')

A.add(B)
B.add(C)


print 'Before:'
A.update()
    
print ''

B.remove(C)
print ''

print 'After:'
A.update()