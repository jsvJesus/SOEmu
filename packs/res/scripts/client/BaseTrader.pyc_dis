# Embedded file name: scripts/client/BaseTrader.py
import BigWorld
import BWPersonality
import GUI
import StalkerModel
import Helpers.Caps
from SingleEntityTimedLight import SingleEntityTimedLight

class BaseTrader(SingleEntityTimedLight):

    def __init__(self):
        if Helpers.Caps.CAP_BASE_TRADE not in self.targetCaps:
            self.targetCaps += [Helpers.Caps.CAP_BASE_TRADE]