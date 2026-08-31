# Embedded file name: scripts/client/BaseFlag.py
__author__ = 'Madcat'
import BigWorld
from ModelSelector import ModelSelector
from Math import Vector3
from time import time
import Clan
import Constants

class BaseFlag(BigWorld.Entity, ModelSelector):
    client_capture_progress = 0.0
    correcting = 0.0
    SYNC_PERIOD = 4.0
    CALC_PERIOD = 0.1
    FLAG_LEVEL_SGT = 0
    FLAG_LEVEL_PVT = 1
    FLAG_LEVEL_CPL = 2
    pre = None

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.model = BigWorld.Model(self.MODELS[self.FLAGPOLE_AND_FLAG_MODEL])
        if not self.isReinfPoint:
            const = self.SIGN_STAR_1
            if self.level == Clan.FLAG_LEVEL_CPL:
                const = self.SIGN_STAR_2
            elif self.level == Clan.FLAG_LEVEL_SGT:
                const = self.SIGN_STAR_3
            model = BigWorld.Model(self.MODELS[const])
            self.addModel(model)
            self.models[0].position = self.position

    def onEnterWorld(self, prereqs):
        self.pre = prereqs
        self.setFlagSkin()
        self.model.Wave()
        self.model.RaisedUp()
        if self.capture_progress < 1.0:
            cur_pos = self.model.Raise().lastFrame * self.capture_progress
            frame_rate = self.model.Raise().lastFrame / self.time
            to_pos = self.model.Raise().lastFrame
            self.model.Raise(0, None, False, cur_pos, to_pos, frame_rate)
        return

    def startCaptureProgress(self):
        frame_rate = self.model.Raise().lastFrame / self.time
        self.model.Raise(0, None, False, 0, self.model.Raise().lastFrame, frame_rate)
        return

    def setFlagSkin(self):
        player = BigWorld.player()
        clanID = player.cellClanID
        if self.state in [Clan.FLAG_STATE_CAPTURED,
         Clan.FLAG_STATE_PROTECTED,
         Clan.FLAG_STATE_IN_DEFENDING,
         Clan.FLAG_STATE_DEFENSELESS]:
            if self.clanID == clanID:
                if self.isReinfPoint:
                    self.model.pasted__lambert43_skinned = 'Default'
                else:
                    self.model.pasted__lambert43_skinned = 'flag_blue'
                return
            if self.isReinfPoint:
                self.model.pasted__lambert43_skinned = 'shield_red'
            else:
                self.model.pasted__lambert43_skinned = 'flag_red'
        elif self.state == Clan.FLAG_STATE_IN_CAPTIVITY:
            if clanID == self.winning_clan:
                if self.isReinfPoint:
                    self.model.pasted__lambert43_skinned = 'Default'
                else:
                    self.model.pasted__lambert43_skinned = 'flag_blue'
                return
            if self.isReinfPoint:
                self.model.pasted__lambert43_skinned = 'shield_red'
            else:
                self.model.pasted__lambert43_skinned = 'flag_red'
        else:
            if clanID in self.enemies:
                if self.isReinfPoint:
                    self.model.pasted__lambert43_skinned = 'Default'
                else:
                    self.model.pasted__lambert43_skinned = 'flag_blue'
                return
            if self.isReinfPoint:
                self.model.pasted__lambert43_skinned = 'shield_red'
            else:
                self.model.pasted__lambert43_skinned = 'flag_red'

    def set_state(self, old_value):
        self.setFlagSkin()

    def set_enemies(self, old_value):
        self.setFlagSkin()

    def set_clanID(self, old_value):
        self.setFlagSkin()

    def set_winning_clan(self, old_value):
        self.setFlagSkin()