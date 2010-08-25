class EventObserver(object):
    def __init__(self, method):
        self.__subscribers = []
        self.__target_method = method
    
    def add(self, subscriber):
        self.__subscribers.append(subscriber)
        
    def notify(self, event):
        for subscriber in self.__subscribers:
            subscriber.__getattribute__(self.__target_method)(event)