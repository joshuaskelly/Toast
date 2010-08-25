import os

exampleList = os.listdir(os.getcwd())

print "Running all of the examples..."

for exampleDir in exampleList:
    if exampleDir.find('.') == -1:
        os.chdir(exampleDir)
        
        demoList = os.listdir(os.getcwd())
        for demo in demoList:
            if demo.find('.py') != -1:
                print "Running: " + demo + "..."
                execfile(demo)
        
        os.chdir('..')
