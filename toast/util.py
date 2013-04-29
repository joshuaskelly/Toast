from xml.etree import ElementTree

class XMLDict(dict):
    """ A helper class that facilitates working with xml documents in a 
    read-only manner. Mostly lifted from:
    http://code.activestate.com/recipes/573463-converting-xml-to-dictionary-and-back/
    
    >>> doc = dict_from_xml('file.xml')
    >>> doc.root.children[0]
    >>> doc['root']['children'][0]
    """
    def __init__(self, initial_dict=None):
        if initial_dict is None:
            initial_dict = {}
        
        dict.__init__(self, initial_dict)
        
    def __getattr__(self, item):
        return self.__getitem__(item)
    
    def __setattr(self, item, value):
        self.__setitem__(item, value)
        
    def __str__(self):
        if self.has_key('_text'):
            return self.__getitem__('_text')
        else:
            return ''
        
def __convert(node):
    node_dict = XMLDict()
    
    if len(node.items()) > 0:
        node_dict.update(dict(node.items()))
        
    for child in node:
        new_node_dict = __convert(child)
        
        if node_dict.has_key(child.tag):
            
            if type(node_dict[child.tag]) is type([]):
                node_dict[child.tag].append(new_node_dict)
            else:
                node_dict[child.tag] = [node_dict[child.tag], new_node_dict]
                
        else:
            node_dict[child.tag] = new_node_dict
            
    if node.text is None:
        text = ''
    else:
        text = node.text.strip()
        
    if len(node_dict) > 0:
        if len(text) > 0:
            node_dict['_text'] = text
        
    else:
        node_dict = text
        
    return node_dict
        
def dict_from_xml(root):
    """ Builds and returns an XMLDict representing the given xml document.
    
    >>> doc = dict_from_xml('file.xml')
    >>> resolution = doc.config.display.resolution
    """
    if type(root) == type(''):
        root = ElementTree.parse(root).getroot()
    elif not isinstance(root, ElementTree.Element):
        raise TypeError, 'blah'
    
    return XMLDict({root.tag : __convert(root)})
