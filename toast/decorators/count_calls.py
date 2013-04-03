class CountCalls(object):
    def __init__(self, func):
        self.__function = func
        self.__calls = 0
        
    def __call__(self, *args):
        self.__calls += 1
        return self.__function(*args)
        
    def __del__(self):
        print('%d call%s made to %s' % (self.__calls, 's' if self.__calls > 1 else '', self.__function.__name__))
        
    def __repr__(self):
        return str(self.__function)
    
    def __name__(self):
        return self.__function.__name__
    
    def __doc__(self):
        return self.__function.__doc__
        
if __name__ == '__main__':
    
    @CountCalls
    def foo():
        pass
    
    foo()
    foo()