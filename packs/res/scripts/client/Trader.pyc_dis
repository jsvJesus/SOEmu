# Embedded file name: scripts/client/Trader.py
import BigWorld
import GUI
import StalkerModel
import Helpers.Caps
from SingleEntityTimedLight import SingleEntityTimedLight

class Trader(SingleEntityTimedLight):

    def __init__(self):
        if Helpers.Caps.CAP_CAN_TRADE not in self.targetCaps:
            self.targetCaps += [Helpers.Caps.CAP_CAN_TRADE]

    def set_Assortment(self, old_value):

        def redraw_player_table(enteredTrap, handle):
            if enteredTrap:
                BigWorld.player().NeedToUpdateTradeInterface(self.id)

        BigWorld.addPot(self.matrix, 6.0, redraw_player_table)