from toast.util import dict_from_xml

if __name__ == '__main__':
    path = 'data/test.xml'
    
    doc = dict_from_xml(path)
    print(doc.map.tilemap[1].name)