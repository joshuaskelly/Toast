"""
" * Level.py
" * Copyright (C) 2009 Joshua Skelton
" *                    joshua.skelton@gmail.com
" *
" * This program is free software; you can redistribute it and/or
" * modify it as you see fit.
" *
" * This program is distributed in the hope that it will be useful,
" * but WITHOUT ANY WARRANTY; without even the implied warranty of
" * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""

import xml.dom.minidom
import pygame

import toast


class Level(object):

    def __init__(self, filename):
        """
        " * Class Constructor
        " *    filename:     The path to the xml level data.
        """

        # Create a document from the xml file
        document = xml.dom.minidom.parse(filename)

        # Grab the path the the xml file
        path = filename.rpartition('/')[0] + '/'
        self.root = {}

        # Create all tilemaps defined in the xml document
        self.parse_tilemaps(document, path)
        self.parse_cameras(document)

    def parse_tilemaps(self, document, path = ''):
        for tilemap in document.getElementsByTagName('tilemap'):
            # Get the image from the xml data and load it
            
            image = pygame.image.load(path + self.get_element_value(tilemap, 'image')).convert_alpha()

            # Get the tile dimensions from the xml document
            dimension = self.get_element_value(tilemap, 'tilesize')
            dimension = (int(dimension.split(',')[0]),
                         int(dimension.split(',')[1]))
            
            # Get the scroll rate
            try:
                scroll_rate = self.get_element_value(tilemap, 'scroll')
                scroll_rate = (float(scroll_rate.split(',')[0]),
                               float(scroll_rate.split(',')[1]))
            except:
                scroll_rate = (0, 0)

            # Create a ImageSheet with the previous data
            sheet = toast.ImageSheet(image, dimension)

            # Get the tilemap data and format it
            rawdata = self.get_element_value(tilemap, 'data')
            rawdata = self.remove_white_space(rawdata)
            rawdata = rawdata.split(',')

            # Get the parallax value
            try:
                parallax = float(self.get_element_value(tilemap, 'parallax'))
            except:
                # No parallax value specified in xml document. Default to 1.0
                parallax = 1.0

            # Get the dimension of the tilemap(in tiles)
            height = int(self.get_element_value(tilemap, 'height'))
            width = int(self.get_element_value(tilemap, 'width'))
            data = []

            for i in range(height):
                row = []
                for j in range(width):
                    row.append(int(rawdata[(i * width) + j]))

                data.append(row)

            map = toast.TileMap(sheet, data)
            map.parallax = parallax
            map.scroll_rate = scroll_rate

            self.root[str(tilemap.getAttribute('id'))] = map

    def parse_cameras(self, document):
        for camera in document.getElementsByTagName('camera'):
            position = self.get_element_value(camera, 'position')
            position = (int(position.split(',')[0]),
                        int(position.split(',')[1]))

            resolution = self.get_element_value(camera, 'viewport')
            resolution = (int(resolution.split(',')[0]),
                          int(resolution.split(',')[1]))
            
            bounds = None
            try:
                bounds = self.get_element_value(camera, 'bounds')
                bounds = (int(bounds.split(',')[0]),
                          int(bounds.split(',')[1]),
                          int(bounds.split(',')[2]),
                          int(bounds.split(',')[3]))
            except:
                bounds = None

            cam = toast.Camera(resolution)
            cam.position = position
            cam.bounds = bounds

            self.root[str(camera.getAttribute('id'))] = cam

    def update(self, delta):
        for element in [self.root[element] for element in self.root]:
            if hasattr(element, 'update'):
                element.update(delta)
                
    def render(self, surface, offset = (0, 0)):
        for element in [self.root[element] for element in self.root]:
            if not hasattr(element, 'add_renderable'):
                element.render(surface, offset)

    def get_element_by_ID(self, id):
        return self.root[id]

    def get_element_value(self, node, tag):
        target = node.getElementsByTagName(tag)[0]
        value = target.childNodes[0].nodeValue.strip('"')
        return str(value)

    def remove_white_space(self, string):
        result = ""
        for char in string:
            if char.isdigit() or char == ',':
                result += char

        return result
