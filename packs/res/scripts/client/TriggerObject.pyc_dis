# Embedded file name: scripts/client/TriggerObject.py
"""
Created on 05.10.2010

@author: muzhig
"""
import BigWorld
import FX
import Helpers.Caps
import Quest
from ModelSelector import ModelSelector
from InteractiveObject import InteractiveObject
import Constants

class TriggerObject(BigWorld.Entity, ModelSelector, InteractiveObject):

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.hasPlayer = False
        if self.activeFlags & Constants.ACTIVE_OBJECT_FLAG:
            if self.talkFlag:
                self.targetCaps = [Helpers.Caps.CAP_CAN_TALK]
        InteractiveObject.__init__(self)
        if self.qEffect:
            self.qEffect = 'sfx/' + self.qEffect
            if not self.qEffect.endswith('.xml'):
                self.qEffect = self.qEffect + '.xml'

    def onEnterWorld(self, prereqs):
        ModelSelector.onEnterWorld(self, prereqs)
        self.set_activeFlags(None)
        from PlayerAvatar import PlayerAvatar
        player = None
        for e in BigWorld.entities.values():
            if isinstance(e, PlayerAvatar):
                player = e
                break

        if player:
            for quest in e.QuestObjInfo:
                if quest['quest_type'] == Quest.TYPE_TRIGGER_ACTION and quest['object_type'] == self.quest and quest['state'] == Quest.STATE_OPENED:
                    self.appendQuestMarker()
                    return

        InteractiveObject.onEnterWorld(self)
        return

    def set_activeFlags(self, v):
        if self.activeFlags & Constants.ACTIVE_OBJECT_FLAG:
            if self.talkFlag:
                self.targetCaps = [Helpers.Caps.CAP_CAN_TALK]
        else:
            self.targetCaps = []

    def startQEffect(self):
        if self.qEffect:
            FX.bufferedOneShotEffect(self.qEffect, self.model)

    def appendQuestMarker(self):
        if Helpers.Caps.CAP_CAN_USE not in self.targetCaps:
            self.targetCaps = self.targetCaps + [Helpers.Caps.CAP_CAN_USE]

    def removeQuestMarker(self):
        if Helpers.Caps.CAP_CAN_USE in self.targetCaps:
            caps = self.targetCaps
            caps.remove(Helpers.Caps.CAP_CAN_USE)
            self.targetCaps = caps

    def set_talkFlag(self, old_value):
        InteractiveObject.set_talkFlag(self, old_value)