"""
" * event_manager.py
" * Copyright (C) 2012 Joshua Skelton
" *                    joshua.skelton@gmail.com
" *
" * This program is free software; you can redistribute it and/or
" * modify it as you see fit.
" *
" * This program is distributed in the hope that it will be useful,
" * but WITHOUT ANY WARRANTY; without even the implied warranty of
" * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""

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
    
    def add(self, subscriber):
        self.__subscribers.append(subscriber)
        
        if hasattr(subscriber, 'parent'):
            subscriber.parent = self
        
    def notify(self, event):
        for subscriber in self.__subscribers:
            try:
                subscriber.__getattribute__(self.__target_method)(event)
            except:
                raise EventNotificationException('Subscriber: ' + str(subscriber) + ' does not implement the required method: ' + self.__target_method + '(event)')
            
    def remove(self, subscriber):
        if subscriber in self.__subscribers:
            self.__subscribers.remove(subscriber)
            
class EventNotificationException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)