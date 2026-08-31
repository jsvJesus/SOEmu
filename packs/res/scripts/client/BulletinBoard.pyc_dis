# Embedded file name: scripts/client/BulletinBoard.py
import BigWorld
import Math
import Pixie
import random
import ItemsUtils
import time
import GUI
from Localization import lc
from ItemHolder import ItemHolder
from Helpers.Caps import CAP_OPEN_BULLETIN_BOARD

class BulletinBoard(BigWorld.Entity):
    """" client/BulletinBoard """
    DEFAULT_MODEL = 'models/entities/bulletin_board_01_lod1.model'

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.targetCaps = [CAP_OPEN_BULLETIN_BOARD]
        self.name = lc('soBulletinBoard.EntityName')

    def onEnterWorld(self, prereqs):
        self.model = BigWorld.Model(self.DEFAULT_MODEL)
        BigWorld.addShadowEntity(self)
        self.targetFullBounds = True

    def onLeaveWorld(self):
        BigWorld.delShadowEntity(self)