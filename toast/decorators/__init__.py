class call_if(object):
    def __init__(self, cond):
        self.condition = cond

    def __call__(self, func):
        def inner(*args, **kwargs):
            if getattr(args[0], self.condition):
                return func(*args, **kwargs)
            else:
                return None
        return inner