from toast.image_sheet import ImageSheet
from toast.resource_loader import ResourceLoader
from toast.scene_graph import GameObject, Scene
from toast.tile_map import TileMap
from toast.camera import Camera
from toast.util import dict_from_xml

class OgmoProject(object):
    """The OgmoProject class loads Ogmo project definitions from an oep file
    and provides the ability to load Ogmo levels as a Scene.
    
    >>> project = OgmoProject('SimpleGame.oep')
    >>> level = project.load_level('LevelOne.oel')
    """
    def __init__(self, oep_file):
        self.__data = dict_from_xml(oep_file)
        
        # Build layer definitions dict
        self.__layer_definitions = {}
        
        for layer in self.__data.project.LayerDefinitions.LayerDefinition:
            new_def = {}
            
            layer_name = layer.Name
            new_def['xsi:type'] = layer['{http://www.w3.org/2001/XMLSchema-instance}type']
            new_def['Grid'] = int(layer.Grid.Width), int(layer.Grid.Height)
            new_def['ScrollFactor'] = int(layer.ScrollFactor.X), int(layer.ScrollFactor.Y)
            
            if new_def['xsi:type'] == 'TileLayerDefinition':
                new_def['ExportMode'] = layer.ExportMode
            
            self.__layer_definitions[layer_name] = new_def
        
        # Build tileset dict
        self.__tilesets = {}
        for tileset in self.__data.project.Tilesets.Tileset:
            new_tileset = {}
            
            tileset_name = tileset.Name
            new_tileset['FilePath'] = tileset.FilePath
            new_tileset['TileSize'] = int(tileset.TileSize.Width), int(tileset.TileSize.Height)
            new_tileset['TileSep'] = int(tileset.TileSep)
            
            self.__tilesets[tileset_name] = new_tileset
        
    @property
    def version(self):
        return self.__data.project.OgmoVersion
    
    @property
    def name(self):
        return self.__data.project.Name
    
    @property
    def background_color(self):
        color = self.__data.project.BackgroundColor
        return int(color.R), int(color.G), int(color.B)
    
    @property
    def grid_color(self):
        color = self.__data.project.GridColor
        return int(color.R), int(color.G), int(color.B)
    
    @property
    def level_default_size(self):
        size = self.__data.project.LevelDefaultSize
        return int(size.Width), int(size.Height)
    
    @property
    def level_minimum_size(self):
        size = self.__data.project.LevelMinimumSize
        return int(size.Width), int(size.Height)
    
    @property
    def level_maximum_size(self):
        size = self.__data.project.LevelMaximumSize
        return int(size.Width), int(size.Height)
    
    @property
    def filename(self):
        return self.__data.project.Filename
    
    @property
    def angle_mode(self):
        return self.__data.project.AngleMode
    
    @property
    def camera_enabled(self):
        return bool(self.__data.project.CameraEnabled)
    
    @property
    def camera_size(self):
        size = self.__data.project.CameraSize
        return int(size.Width), int(size.Height)
    
    @property
    def export_camera_position(self):
        return bool(self.__data.project.ExportCameraPosition)
    
    @property
    def layer_definitions(self):
        return self.__layer_definitions
    
    @property
    def tilesets(self):
        return self.__tilesets
    
    def load_level(self, oel_file):
        """Loads an Ogmo level file and returns a Scene built from the 
        definitions.
        
        :param oel_file: The Ogmo level to load.
        :type oel_file: A filepath.
        """
        rel_path = '/'.join(oel_file.split('/')[:len(oel_file.split('/')) - 1])
        level_data = dict_from_xml(oel_file)
        
        level = Scene()
        
        for key in level_data.level:
            if key in self.layer_definitions:
                xsi_type = self.layer_definitions[key]['xsi:type']
                
                if xsi_type == 'TileLayerDefinition':
                    tile_layer = level_data.level[key]
                    
                    export_mode = tile_layer.exportMode
                    data = []
                    
                    if export_mode == 'CSV':
                        rows = str(tile_layer).split('\n')
                        
                        for row in rows:
                            data.append(map(int, row.split(',')))
                    
                    dimension = self.layer_definitions[key]['Grid']
                    path = self.tilesets[tile_layer.tileset]['FilePath']
                    
                    surf = ResourceLoader.load(rel_path + '/' + path)
                    sheet = ImageSheet(surf, dimension)
                    tilemap = TileMap(sheet, data)
                    
                    level.add(tilemap)
                
                elif xsi_type == 'EntityLayerDefinition':
                    level.add(GameObject())
                    
            elif key == 'camera':
                camera = Camera(self.camera_size)
                camera.top_left = int(level_data.level.camera.x), int(level_data.level.camera.y)
                
                level.add(camera)
            
            elif key == 'width':
                level.width = int(level_data.level[key])
                
            elif key == 'height':
                level.width = int(level_data.level[key])
                
            else:
                setattr(level, key, level_data.level[key])
        
        return level
