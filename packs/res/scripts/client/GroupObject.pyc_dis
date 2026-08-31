# Embedded file name: scripts/client/GroupObject.py
"""
Created on 05.10.2010

@author: muzhig
"""
import BigWorld
from ModelSelector import ModelSelector
import Helpers.Caps

class GroupObject(BigWorld.Entity, ModelSelector):

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.targetCaps.append(Helpers.Caps.CAP_CAN_GATHER_GROUP)