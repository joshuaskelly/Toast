import weakref

class EventManager(object):
    __events = {}
        
    @staticmethod
    def subscribe(subscriber, method):
        if method not in EventManager.__events:
            EventManager.__events[method] = EventObserver(method)
            
        EventManager.__events[method].add(subscriber)

    @staticmethod
    def notify(method, event):
        if method in EventManager.__events:
            EventManager.__events[method].notify(event)
            
class EventObserver(object):
    def __init__(self, method):
        self.__subscribers = []
        self.__target_method = method
        self.__is_notifying_subscribers = False
        self.__subscribers_to_add = []
    
    def add(self, subscriber):
        if self.__is_notifying_subscribers:
            self.__subscribers_to_add.append(subscriber)
        else:
            self.__subscribers.append(weakref.ref(subscriber))
        
    def notify(self, event):
        cleanup_list = []
        
        self.__is_notifying_subscribers = True
        for subscriber in self.__subscribers:
            if hasattr(subscriber(), self.__target_method):
                subscriber().__getattribute__(self.__target_method)(event)
            else:
                if subscriber() is None:
                    cleanup_list.append(subscriber)
                    continue
                raise EventNotificationException('Subscriber: ' + str(subscriber()) + ' does not implement the required method: ' + self.__target_method + '(event)')
        self.__is_notifying_subscribers = False
        
        # Add any new subscribers now that we are done notifying
        for subscriber in self.__subscribers_to_add:
            self.add(subscriber)
            
        self.__subscribers_to_add = []
        
        if len(cleanup_list) > 0:
            for g in cleanup_list:
                self.__subscribers.remove(g)
            
    def remove(self, subscriber):
        if subscriber in self.__subscribers:
            self.__subscribers.remove(subscriber)
            
class EventNotificationException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
    