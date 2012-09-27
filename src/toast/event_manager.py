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
    
    def add(self, subscriber):
        self.__subscribers.append(weakref.ref(subscriber))
        
    def notify(self, event):
        cleanup_list = []
        
        for subscriber in self.__subscribers:
            if hasattr(subscriber(), self.__target_method):
                subscriber().__getattribute__(self.__target_method)(event)
            else:
                if subscriber() is None:
                    cleanup_list.append(subscriber)
                    continue
                raise EventNotificationException('Subscriber: ' + str(subscriber()) + ' does not implement the required method: ' + self.__target_method + '(event)')
            
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
    