# Embedded file name: scripts/client/Grenade.py
"""
Created on 05.10.2010

@author: muzhig
"""
from functools import partial
from random import random
import BigWorld
import BWPersonality
from Math import Vector3
import FX
from Damager import Damager
import SFXer
import ItemsUtils
from Items import ItemsCatalog
from Throwable import Throwable
from ThrowingData import Throwing
from utils_bw import packDict, unpackDict, if_not_destroyed
from ThrowingData import Throwing, ThrowTypes

class Grenade(BigWorld.Entity, Throwable, Damager):

    def __init__(self):
        BigWorld.Entity.__init__(self)
        Throwable.__init__(self)

    def onLeaveWorld(self):
        self.removeClientEntity()
        if hasattr(self, 'sPersistentSFX'):
            self.sPersistentSFX.stop()
            self.sPersistentSFX.detach()
            del self.sPersistentSFX

    def explodeMolotov(self):
        self.bouncer = None
        self.model.visible = False
        throwingData = Throwing[self.throwingType]
        explode_sfx = throwingData.get('explodeSFX')
        if explode_sfx:
            explosion_model = BigWorld.Model('')
            explosion_model.position = self.model.position
            self.addModel(explosion_model)
            s = FX.Persistent(explode_sfx)
            s.attach(explosion_model)
            self.explosion_model = explosion_model
            self.sPersistentSFX = s
            FX.OneShot(explode_sfx).go(explosion_model)
        return

    def explode(self, victims):
        if self.throwingType == ThrowTypes.GRENADE_MOLOTOV:
            if self.fromServer and self.ownerID == BigWorld.player().id:
                return
        self.bouncer = None
        self.model.visible = False
        self.removeClientEntity()
        throwingData = Throwing[self.throwingType]
        explode_sfx = throwingData.get('explodeSFX')
        if explode_sfx:
            explosion_model = BigWorld.Model('')
            explosion_model.position = self.position
            self.addModel(explosion_model)
            if throwingData.get('isFXPersistent'):
                s = FX.Persistent(explode_sfx)
                s.attach(explosion_model)
            else:
                FX.OneShot(explode_sfx).go(explosion_model)
        for victimID in victims:
            victim = BigWorld.entities[victimID]
            coin = random()
            if victim.__class__.__name__ == 'Avatar':
                normal = victim.position - self.position
                normal.normalise()
                normal = victim.position + (0, 0.9, 0) - self.position - (0, 0.1, 0)
                normal.normalise()
                SFXer.BodyHit(victim.position + Vector3(0, 0.9 + coin * 0.1, 0), victim, normal, -normal)
                normal = victim.position + (0, 1.2, 0) - self.position - (0, 0.1, 0)
                normal.normalise()
                SFXer.BodyHit(victim.position + Vector3(0, 1.1 + coin * 0.2, 0), victim, normal, -normal)
                normal = victim.position + (0, 1.5, 0) - self.position - (0, 0.1, 0)
                normal.normalise()
                SFXer.BodyHit(victim.position + Vector3(0, 1.5 + coin * 0.3, 0), victim, normal, -normal)
            else:
                normal = victim.position + (0, 0.2, 0) - self.position
                normal.normalise()
                SFXer.BodyHit(victim.position + Vector3(0, 0.1 + coin * 0.1, 0), victim, normal, -normal)

        if self.thrownFromThisClient():
            try:
                thrower = BigWorld.entities[self.ownerID]
                thrower.onGrenadeExploded(self)
            except KeyError:
                pass

        return

    def updatePath(self, serverPos, destPos):
        if self.isDestroyed:
            return
        if self.thrown:
            self.bouncer.updatePath(serverPos, destPos)
        else:
            BigWorld.callback(0.1, partial(self.updatePath, serverPos, destPos))