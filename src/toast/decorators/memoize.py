class memoize(object):
    def __init__(self, function):
        self.__function = function
        self.__cache = {}
        
    def __call__(self, *args):
        try:
            return self.__cache[args]
        
        except KeyError:
            self.__cache[args] = value = self.__function(*args)
            return value
        
        except TypeError:
            return self.__function(*args)

    def __repr__(self):
        return str(self.__function)
    
    def __name__(self):
        return self.__function.__name__
    
    def __doc__(self):
        return self.__function.__doc__
    
if __name__ == '__main__':
    from count_calls import CountCalls
    # To see the benefit of memoization try removing the memoize decorator
    # from the fib function below.
    
    @CountCalls
    @memoize
    def fib(n):
        if n in (0, 1):
            return n
        else:
            return fib(n - 1) + fib(n - 2)
        
    for x in range (300):
        print('fib(%d): %d' % (x, fib(x)))