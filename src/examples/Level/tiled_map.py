import xml.dom.minidom
import pygame

import toast

def load_map(filename):
    builder = Builder(filename)
    map = builder.build()
    return map

class Builder(object):
    def __init__(self, filename):
        """
        " * Class Constructor
        " *    filename:     The path to the xml level data.
        """
        
        self.load_document(filename)
        self.path = filename.rpartition('/')[0] + '/'
        
    def build(self):
        self.map = TiledMap()
        self.parse(self.document)
        return self.map
        
    def load_document(self, filename):
        self.document = xml.dom.minidom.parse(filename)
        
    def parse(self, node):
        parse_method = getattr(self, 'parse_%s' % node.__class__.__name__)
        parse_method(node)
        
    def parse_Document(self, node):
        self.parse(node.documentElement)
        
    def parse_Element(self, node):
        handler_method = getattr(self, 'handle_%s' % node.tagName)
        handler_method(node)
        
    def parse_Text(self, node):
        pass
        
    def handle_map(self, node):
        attributes = self.get_attributes(node)
        
        for key in attributes:
            setattr(self.map, key, attributes[key])
        
        for child in node.childNodes:
            self.parse(child)
            
    def handle_tileset(self, node):
        attributes = self.get_attributes(node)
        
        for child in node.childNodes:
            self.parse(child)
            
        self.add_tiles_to_map((attributes['tilewidth'], attributes['tileheight']))
            
    def add_tiles_to_map(self, dimensions):
        sheet = toast.ImageSheet(self.current_element, dimensions)
        
        for tile in sheet:
            self.map.tiles.append(tile)

    def handle_layer(self, node):
        for child in node.childNodes:
            self.parse(child)
        
    def handle_image(self, node):
        self.current_element = pygame.image.load(self.path + str(node.attributes['source'].value))
        
    def handle_properties(self, node):
        for child in node.childNodes:
            self.parse(child)
            
    def handle_property(self, node):
        for attr in self.get_attributes(node):
            print attr
        
    def handle_data(self, node):
        print node
        
    def handle_objectgroup(self, node):
        for child in node.childNodes:
            self.parse(child)
            
    def handle_object(self, node):
        for child in node.childNodes:
            self.parse(child)
            
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
        

class TiledMap(toast.Component):
    def __init__(self):
        toast.Component.__init__(self)
        
        self.tiles = [None]
    
class TiledLayer(toast.Component):
    def __init__(self):
        toast.Component.__init__(self)