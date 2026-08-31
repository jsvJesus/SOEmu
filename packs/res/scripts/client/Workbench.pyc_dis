# Embedded file name: scripts/client/Workbench.py
import BigWorld
import Math
import Pixie
import random
import ItemsUtils
import time
import GUI
from Localization import lc
from ItemHolder import ItemHolder
from Helpers.Caps import CAP_OPEN_WORKBENCH
import WorkbenchUtil

class Workbench(BigWorld.Entity):
    """" client/Workbench """

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.targetCaps = [CAP_OPEN_WORKBENCH]
        self.name = u'?????'

    def onEnterWorld(self, prereqs):
        self._redraw_Model()
        BigWorld.addShadowEntity(self)
        self.targetFullBounds = True

    def onLeaveWorld(self):
        BigWorld.delShadowEntity(self)

    def set_workbenchType(self, old):
        self._redraw_Model()

    def _redraw_Model(self):
        modelname = WorkbenchUtil.getNameModel(self.workbenchType)
        self.model = BigWorld.Model(modelname)
        self.name = WorkbenchUtil.getName(self.workbenchType)