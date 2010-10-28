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
import imp

import xml.dom.minidom
import pygame

import toast


class Level(object):
    
    object_count = 0

    def __init__(self, filename):
        """
        " * Class Constructor
        " *    filename:     The path to the xml level data.
        """

        # Create a document from the xml file
        document = xml.dom.minidom.parse(filename)

        # Grab the path the the xml file
        path = filename.rpartition('/')[0] + '/'
        self.root = []
        self.names = {}

        # Create all tilemaps defined in the xml document
        self.parse_tilemaps(document, path)
        self.parse_objects(document)

    def add(self, object):
        if hasattr(object, 'update') or hasattr(object, 'render'):
            if not hasattr(object, 'add_renderable'):
                self.root.append(object)
            
        try:
            self.names[object.name] = object
        except:
            id = self.get_object_id(object)
            self.names[id] = object

    def parse_tilemaps(self, document, path = ''):
        for tilemap in document.getElementsByTagName('map'):
            # Get the image from the xml data and load it
            
            # Get the tile dimensions from the xml document
            tile_size = int(tilemap.getAttribute('tilewidth')), int(tilemap.getAttribute('tileheight'))
            
            # Get the map dimensions from the xml document
            map_size = int(tilemap.getAttribute('width')), int(tilemap.getAttribute('height'))
            
            # Get the image from the map
            image_path = tilemap.getElementsByTagName('tileset')[0].getElementsByTagName('image')[0].getAttribute('source')
            image = pygame.image.load(path + image_path)#.convert_alpha()

            # Create an ImageSheet with the previous data
            sheet = toast.ImageSheet(image, tile_size)
            
            for layer in tilemap.getElementsByTagName('layer'):
            
                # Get the tilemap data and format it
                rawdata = self.get_element_value(layer, 'data')
                rawdata = self.remove_white_space(rawdata)
                rawdata = rawdata.split(',')
                
                # Format the raw data into a 2D array
                data = []
    
                for i in range(map_size[1]):
                    row = []
                    for j in range(map_size[0]):
                        row.append(int(rawdata[(i * map_size[0]) + j]) - 1)
    
                    data.append(row)
                    
                map = toast.TileMap(sheet, data)

                self.add_attributes(map, layer)
                self.add_properties(map, layer)
                        
                self.add(map)
                #self.root[attributes['name']] = map
            
    def parse_objects(self, document):
        for group in document.getElementsByTagName('objectgroup'):
            object_group = toast.Component()
            
            for node in group.getElementsByTagName('object'):
                try:
                    object_type = str(node.attributes['type'].value)
                    
                    parse_method = getattr(self, 'parse_%s' % object_type)
                    object = parse_method(node)
                    
                    object_group.add(object)
                    
                    try:
                        self.names[object.name] = object
                    except:
                        id = self.get_object_id(object)
                        self.names[id] = object
                
                except Exception as e:
                    raise Exception(e)
                
            self.add_attributes(object_group, group)
                
            self.add(object_group)

                
    def parse_camera(self, object):
        attributes = self.get_attributes(object)
        viewport = attributes['width'], attributes['height']
        
        position = attributes['x'] + viewport[0] / 2, \
                   attributes['y'] + viewport[1] / 2
        
        camera = toast.Camera(viewport)
        camera.position = position
        camera.name = attributes['name']
        
        properties = self.get_properties(object)
        
        if 'bounds' in properties.keys():
            camera.bounds = self.get_element_by_ID(properties['bounds'])
        
        return camera
    
    
    def parse_custom(self, node):
        properties = self.get_properties(node)
        
        file = properties['script'].rpartition('/')
        file = file[len(file) - 1]
        
        name = file.rpartition('.')[0]
        
        script = imp.load_source(name, properties['script'])
        custom_object = script.get_instance()
        
        self.add_attributes(custom_object, node)
        
        return custom_object
    
    def parse_rect(self, node):
        attributes = self.get_attributes(node)
        
        x = attributes['x']
        y = attributes['y']
        width = attributes['width']
        height = attributes['height']
        name = attributes['name']
        
        rect = pygame.Rect((x, y), (width, height))
        
        if name != "":
            self.names[name] = rect
            
        return rect
    
    def get_object_id(self, object):
        id = '%s_%04d' % (object.__class__.__name__, self.object_count)
        self.object_count += 1
        
        return id
            
    def add_attributes(self, object, node):
        attributes = self.get_attributes(node)
        
        for key in attributes:
            setattr(object, key, attributes[key])
            
    def get_attributes(self, node):
        attributes = {}
        for key in node.attributes.keys():
            key = str(key)
            
            try:
                if '.' in node.attributes[key].value:
                    attributes[key] = float(node.attributes[key].value)
                else:
                    attributes[key] = int(node.attributes[key].value)
            except:
                attributes[str(key)] = str(node.attributes[key].value)
            
        return attributes
    
    def add_properties(self, object, node):
        properties = self.get_properties(node)
        
        for key in properties:
            setattr(object, key, properties[key])
            
    def get_properties(self, node):
        properties = {}
        try:
            for child in node.childNodes[1].childNodes:
                if child.__class__.__name__ != "Text":
                    child_attributes = self.get_attributes(child)
                    
                    name = child_attributes['name']
                    value = child_attributes['value']
                    
                    properties[name] = value
        except:
            return {}
                    
        return properties
    
    def update(self, delta):
        for element in self.root:
            if hasattr(element, 'update'):
                element.update(delta)
                
    def render(self, surface, offset = (0, 0)):
        for element in self.root:
            if not hasattr(element, 'add_renderable'):
                element.render(surface, offset)

    def get_element_by_ID(self, id):
        return self.names[id]

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
