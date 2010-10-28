class Impostor(object):
    
    def __init_(self, other):
        pass
    
    def load(self, other):
        for attr in dir(other):
            if attr != '__class__':
                setattr(self, attr, getattr(other, attr))
