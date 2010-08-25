"""
" * animation.py
" * Copyright (C) 2008 Joshua Skelton
" *                    joshua.skelton@gmail.com
" *
" * This program is free software; you can redistribute it and/or
" * modify it as you see fit.
" *
" * This program is distributed in the hope that it will be useful,
" * but WITHOUT ANY WARRANTY; without even the implied warranty of
" * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""
import pygame


import time

from pygame.locals import *

class Animation(pygame.Surface):
    
    def __init__(self, key=None, anim=None):
        dim = (anim[0][0].get_width(),
               anim[0][0].get_height())

        pygame.Surface.__init__(self,dim)

        self.__animation_list = {}
        
        self.__running = True
        
        self.__time = 0
        
        self.__current_animation = ''
        self.__current_frame = None
        self.__index = 0
        self.target = None
        self.mode = 1
        
        if key != None:
            self.add_animation(key, anim)
        
        #self.start()
        
    def update(self, time=0):
        if self.__current_animation != '':
            if self.__index > len(self.__animation_list[self.__current_animation]) - 1:
                self.__index = 0
                
            self.__time += time
            
            self.__current_frame, duration = self.__animation_list[self.__current_animation][self.__index]
            
            if self.__time > duration:
                self.__time -= duration
                
                #sl = len(self.__animation_list[self.__current_animation]) - 1
                
                self.__index +=1
                
        
    def run(self):
        return
        while self.__running:
            if self.__current_animation != '':

                if self.__index > len(self.__animation_list[self.__current_animation]) - 1:
                    self.__index = 0
                    
                frame, seconds = self.__animation_list[self.__current_animation][self.__index]
                
                self.__current_frame = frame
                
                time.sleep(seconds)
                
                self.__index += 1

    def add_animation(self, key, animation):
        if self.__current_animation == '':
            self.__current_animation = key
            
        if self.__current_frame == None:
            self.__current_frame = animation[0][0]
            
        self.__animation_list[key] = animation
        
    def get_current_frame(self):
        return self.__current_frame
    
    def get_current_index(self):
        if self.__index > len(self.__animation_list[self.__current_animation]) - 1:
            self.__index = 0
            
        return self.__index
    
    def get_current_animation(self):
        return self.__current_animation
        
    def play(self, anim, start_frame=None):
        self.__current_animation = anim
        
        if start_frame != None:
            self.__index = start_frame
        
    def stop(self):
        self.__current_animation = ''
        self.__index = 0
        
    def goto_and_play(self, frame, anim):
        self.__index = frame
        self.__current_animation = anim