# Embedded file name: scripts/client/Container.py
"""
from Localization import lc
Created on 17.08.2010

@author: muzhig
"""
import BigWorld
from ItemHolder import ItemHolder
from Helpers.Caps import CAP_CAN_OPEN_AND_EXPLORE
import ItemsUtils
import ResMgr
from Localization import lc

class Container(BigWorld.Entity, ItemHolder):
    DEFAULT_POINT_MODEL = 'models\\bolvan\\sfera.model'
    MODELS = {}
    source = ResMgr.openSection('scripts/user_data_object_defs/ItemSpawnPointUDO.def')
    source = source['Properties']['modelSelect']['Widget']
    for item in source.values():
        MODELS[item['value'].asInt] = 'models\\entities\\containers\\' + item['display'].asString

    def __init__(self):
        self.targetCaps = [CAP_CAN_OPEN_AND_EXPLORE]

    def prerequisites(self):
        if self.modelSelect:
            return [self.MODELS[self.modelSelect]]
        else:
            return self.DEFAULT_POINT_MODEL

    def onEnterWorld(self, prereq):
        self.setNormalModel(prereq)
        if self.containerName:
            self.name = self.containerName
        else:
            self.name = self.GetContainerName(self.modelSelect)

    def GetContainerName(self, container_type):
        poll_str = 'Container.Names.TYPE_' + str(container_type)
        return lc(poll_str)

    def setNormalModel(self, prereqs = None):
        if prereqs is None:
            if self.modelSelect:
                self.model = BigWorld.Model(self.MODELS[self.modelSelect])
            else:
                return self.DEFAULT_POINT_MODEL
        elif self.modelSelect:
            self.model = prereqs[self.MODELS[self.modelSelect]]
        else:
            return self.DEFAULT_POINT_MODEL
        return

    def set_CarryingItems(self, old_value):

        def redraw_player_cache(enteredTrap, handle):
            if enteredTrap:
                BigWorld.player().NeedToUpdateItemCache()

        BigWorld.addPot(self.matrix, ItemsUtils.EXTRACTION_RANGE, redraw_player_cache)

    def onLeaveWorld(self):

        def close_player_cache(enteredTrap, handle):
            if enteredTrap:
                BigWorld.player().NeedToCloseItemCache(self)

        BigWorld.addPot(self.matrix, ItemsUtils.EXTRACTION_RANGE, close_player_cache)