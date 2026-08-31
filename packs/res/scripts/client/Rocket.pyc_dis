# Embedded file name: scripts/client/Rocket.py
"""
Created on 05.10.2010

@author: muzhig
"""
import BigWorld, Pixie
from Math import Vector3
from Damager import Damager
from FX_extension import DisposedOneShotSFX
from Config import Rocket as Cfg

class Rocket(BigWorld.Entity, Damager):

    def __init__(self):
        self.shot = None
        return

    def prerequisites(self):
        return [self.get_model(), self.get_trail_sfx()]

    def onEnterWorld(self, prereqs):
        self.cell.go()
        self.prereqs = prereqs
        self.filter = BigWorld.AvatarFilter()
        self.preloadedModel = prereqs[self.get_model()]
        self.model = BigWorld.Model('characters/items/weapons/attach/node_rocket_rpg7_launched_lod1.model')
        self.preloadedModel.visible = False

    def onLeaveWorld(self):
        pass

    def launch(self):
        self.model.node('HP_barrel').attach(self.prereqs[self.get_trail_sfx()])
        self.model.visible = True

    def explode(self, position):
        self.model.visible = False
        DisposedOneShotSFX(self.get_explode_sfx()).play(position)

    def get_model(self):
        return Cfg.get_model(self.itemType)

    def get_trail_sfx(self):
        return Cfg.get_trail_sfx(self.itemType)

    def get_explode_sfx(self):
        return Cfg.get_explode_sfx(self.itemType)