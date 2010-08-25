import re

LABEL = 0
COMMAND = 1
OFFSET1 = 2
LOCATION1 = 3

pattern =   """ ([a-zA-Z]+:)?
                \s*
                (LD|ADD)
                \s*
                ([0-9])?[(]?(R[0-9])[)]?,?
            """
            
commands = []
commands.append("Loop: LD R1")
commands.append("ADD 0(R2),")

instructions = []

for command in commands:
    instructions.append(re.search(pattern, command, re.VERBOSE).groups())
    
for inst in instructions:
    print inst

