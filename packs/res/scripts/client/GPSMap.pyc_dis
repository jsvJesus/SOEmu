# Embedded file name: scripts/client/GPSMap.py
import BWPersonality
import BigWorld
import ResMgr
import soGUI
import Math
from MapNotes import MapNotes

class GPSMap:

    def __init__(self, space_name):
        self.spacesDataDict = {}
        self.InitSpaceData(space_name)
        self.currentSpace = space_name

    def GetSpaceLoadedParams(self, space_name):
        if space_name == None:
            space_name = self.currentSpace
        if self.spacesDataDict.has_key(space_name):
            return self.spacesDataDict[space_name]
        else:
            self.InitSpaceData(space_name)
            return self.spacesDataDict[space_name]
            return

    def InitSpaceData(self, space_name):
        max_x, min_x, max_y, min_y = self.GetSpaceSize(space_name)
        self.spacesDataDict[space_name] = dict(max_x=max_x, min_x=min_x, max_y=max_y, min_y=min_y)

    def GetSpaceSize(self, space_name):
        CHUNK_SIZE = 100.0
        settings_path = space_name
        settings_path += '/space.settings'
        print 'settings_path', settings_path
        space_settings = ResMgr.openSection(settings_path)
        if space_settings != None:
            max_x = (space_settings['bounds']['maxX'].asInt + 1) * CHUNK_SIZE
            min_x = abs(space_settings['bounds']['minX'].asInt * CHUNK_SIZE)
            max_y = (space_settings['bounds']['maxY'].asInt + 1) * CHUNK_SIZE
            min_y = abs(space_settings['bounds']['minY'].asInt * CHUNK_SIZE)
        else:
            max_x, min_x, max_y, min_y = (0, 0, 0, 0)
        return (max_x,
         min_x,
         max_y,
         min_y)

    def GetObjectRelativeCoords(self, position, space_name = None):
        space_param_dict = self.GetSpaceLoadedParams(space_name)
        max_x, min_x, max_y, min_y = (space_param_dict['max_x'],
         space_param_dict['min_x'],
         space_param_dict['max_y'],
         space_param_dict['min_y'])
        if max_x == 0 or min_x == 0 or max_y == 0.0 or min_y == 0.0:
            return (0.0, 0.0)
        x_player = position[0]
        y_player = position[2]
        rel_x_player = (x_player + min_x) / (max_x + min_x) * 2.0 - 1.0
        rel_y_player = (y_player + min_y) / (max_y + min_y) * 2.0 - 1.0
        return (rel_x_player, rel_y_player)

    def GetObjectAbsouluteCoords(self, x_player, y_player, space_name = None):
        space_param_dict = self.GetSpaceLoadedParams(space_name)
        max_x, min_x, max_y, min_y = (space_param_dict['max_x'],
         space_param_dict['min_x'],
         space_param_dict['max_y'],
         space_param_dict['min_y'])
        x_vector = (x_player + 1) * (max_x + min_x) / 2.0 - min_x
        y_vector = (y_player + 1) * (max_y + min_y) / 2.0 - min_y
        return Math.Vector3(x_vector, 0, y_vector)

    def GetMapMarks(self, player_position, NotesStruct):
        player_relative_coords = self.GetObjectRelativeCoords(player_position)
        player_mark = (self.currentSpace,
         MapNotes.TYPE_PLAYER,
         player_relative_coords,
         0.0,
         (255, 128, 64, 255))
        data = {'marks': {}}
        for index, note in enumerate(NotesStruct):
            coords = self.GetObjectRelativeCoords(note['position'], note['spaceName'])
            data['marks'][index] = (note['spaceName'],
             note['flags'],
             coords,
             0.0,
             (255, 128, 64, 255))

        data['marks'][len(data['marks'].items())] = player_mark
        return data