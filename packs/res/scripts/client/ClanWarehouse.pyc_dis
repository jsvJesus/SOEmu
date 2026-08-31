# Embedded file name: scripts/client/ClanWarehouse.py
import BigWorld
import Math
import Pixie
import random
import ItemsUtils
import time
import GUI
from Localization import lc
from ItemHolder import ItemHolder
from Helpers.Caps import CAP_CAN_OPEN_AND_EXPLORE_USER_FIRE
import BWPersonality

class ClanWarehouse:
    """" client/ClanWarehouse """

    def __init__(self):
        pass

    def set_storedClanItems(self, old_value):
        BigWorld.player().NeedToUpdateItemCache()

    def setNested_storedClanItems(self, path, oldValue):
        BigWorld.player().NeedToUpdateItemCache()

    def getStoredItems(self, clanID):
        for warehouse in self.storedClanItems:
            if warehouse.clanID == clanID:
                return warehouse

    def showClanManagerNPCGUI(self):
        BWPersonality.GUICore.showClanManagerNPCGUI(True, self.id)
        BWPersonality.GUICore.setClanManagerNPCData({'name': self.npcName,
         'cost': '2000000'})