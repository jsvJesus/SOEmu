# Embedded file name: scripts/client/InteractiveObject.py
"""
Created on 13.07.2010

@author: Madcat
"""
import BigWorld
import Dialog
import Helpers.Caps

class InteractiveObject:

    def __init__(self):
        pass

    def onEnterWorld(self):
        if self.talkFlag and Helpers.Caps.CAP_CAN_TALK not in self.targetCaps:
            self.targetCaps += [Helpers.Caps.CAP_CAN_TALK]

    def set_talkFlag(self, old_value):
        if self.talkFlag:
            if Helpers.Caps.CAP_CAN_TALK not in self.targetCaps:
                self.targetCaps += [Helpers.Caps.CAP_CAN_TALK]
        elif Helpers.Caps.CAP_CAN_TALK in self.targetCaps:
            caps = list(self.targetCaps)
            caps.remove(Helpers.Caps.CAP_CAN_TALK)
            self.targetCaps = caps