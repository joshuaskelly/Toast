from toast.component import Component

A = Component()
B = Component()
C = Component()

A.add(B)
A.add(C)

print 'Before:'
for subcomponent in A:
    print subcomponent

print ""

print 'After:'
A.remove(B)

del B
del C

for subcomponent in A:
    print subcomponent