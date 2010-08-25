import sys

import xml.dom.minidom

from toast.component import Component

current_module = sys.modules['map']

def load_map(filename):
    return parse(xml.dom.minidom.parse(filename))

def parse(node):
    return getattr(current_module, 'parse_%s' % node.__class__.__name__)(node)

def parse_Document(node):
    return parse(node.documentElement)

def parse_Element(node):
    return getattr(current_module, 'handle_%s' % node.tagName)(node)

def parse_Text(node):
    pass

def handle_map(node):
    return get_new_component(node)

def handle_tileset(node):
    return get_new_component(node)
    

def handle_layer(node):
    return get_new_component(node)

def handle_objectgroup(node):
    return get_new_component(node)

def handle_image(node):
    return get_new_component(node)
    
def get_new_component(node):
    component = Component()
    
    add_attributes(component, node)
    add_children(component, node)
    
    return component

def add_children(object, node):
    for child in node.childNodes:
        child = parse(child)
        object.add(child)
        
def add_attributes(object, node):
    attributes = get_attributes(node)
    
    for key in attributes:
        setattr(object, key, attributes[key])
        
def get_attributes(node):
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
    
    return node