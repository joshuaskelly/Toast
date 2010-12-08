from toast.component import Component

A = Component()
B = Component(A)
C = Component()

A.add(B)
A.add(C)


print 'Before:'
print A
for subcomponent in A:
    print subcomponent
    for S in subcomponent:
        print S

print ""

#C.remove(C)

print 'After:'
#A.remove(C)

#del B
#del C
print A
for subcomponent in A:
    print subcomponent
    for S in subcomponent:
        print S
    
print
print 'Cleanup:'
A.remove()