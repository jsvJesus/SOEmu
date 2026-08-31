# Embedded file name: scripts/client/FireWorks.py
import BigWorld
import Math
import Pixie
import random
import ItemsUtils
import time
import Pixie
import FX
import traceback

class FireWorks(BigWorld.Entity):
    """" client/FireWorks """
    MODEL_NAME = 'models/props/ng/fireworks_01_lod1.model'
    SOUND_BOOMS = 'environment/fireworks/booms'
    SOUND_FIRELINE = 'environment/fireworks/fireline'
    SOUND_ROCKETSTART = 'environment/fireworks/rocketstart'

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.modelFuseS = None
        return

    def onEnterWorld(self, prereqs):
        self.model = BigWorld.Model(self.MODEL_NAME)
        self.modelFuse = BigWorld.Model('')
        self.model.node('HP_flare').attach(self.modelFuse)
        self.PFuse = Pixie.create('particles/fireworks_fuse_white.xml')
        if self.fuseIsBurning:
            self.set_fuseIsBurning(333)

    def set_fuseIsBurning(self, old):
        if self.fuseIsBurning:
            self.model.visible = True
            self.modelFuse.root.attach(self.PFuse)
            self.modelFuseS = BigWorld.Model('')
            BigWorld.addModel(self.modelFuseS, self.spaceID)
            self.modelFuseS.position = self.position
            self.modelFuseS.playSound(self.SOUND_FIRELINE)
        else:
            self.modelFuse.root.detach(self.PFuse)
            if self.modelFuseS:
                BigWorld.delModel(self.modelFuseS)
                self.modelFuseS = None
            self.model.visible = False
        return

    def onLeaveWorld(self):
        self._delHelpsModels()

    def startFire(self, endPos, isColision):
        self.endPos = endPos
        self.isColision = isColision
        self.flyModel = BigWorld.Model('')
        self.explodeModel = BigWorld.Model('')
        self.FWtrain = Pixie.create('particles/fireworks_sparks.xml')
        BigWorld.addModel(self.flyModel, self.spaceID)
        BigWorld.addModel(self.explodeModel, self.spaceID)
        self.explodeModel.position = self.endPos
        self.flyModel.position = self.position
        self.flyModel.root.attach(self.FWtrain)
        self.onFly()
        self.model.playSound(self.SOUND_ROCKETSTART)

    def onFly(self):
        if self.flyModel.position[1] >= self.endPos[1]:
            self.flyEnd()
            return
        dH = self.fwspeed * 0.02
        self.flyModel.position = self.flyModel.position + (0, dH, 0)
        self.flyid = BigWorld.callback(0.02, self.onFly)

    def flyEnd(self):
        try:
            self.FWtrain.system(0).actions[0].sleepPeriod = 2.0
        except:
            traceback.print_exc()

        BigWorld.callback(2.0, lambda : BigWorld.delModel(self.flyModel))
        if self.isColision:
            self.explodeModel.position = self.explodeModel.position - (0, 0.5, 0)
            BigWorld.callback(0.01, self.explode)
            return
        BigWorld.callback(0.6, self.explode)

    def explode(self):
        if self.isColision:
            explode_sfx = 'sfx/grenade_explode.xml'
            FX.OneShot(explode_sfx).go(self.explodeModel)
            return
        lasttime = 0.0
        for i in range(self.number):
            lasttime += random.randrange(0.1, 0.6, int=float)
            BigWorld.callback(lasttime, self.randomExpl)

    def randomExpl(self):
        mexpl = BigWorld.Model('')
        BigWorld.addModel(mexpl, self.spaceID)
        r = self.radius
        if r > 0:
            r3 = (random.randrange(-r, r, int=float), random.randrange(-r / 2, r / 2, int=float), random.randrange(-r, r, int=float))
        else:
            r3 = (0, 0, 0)
        mexpl.position = self.explodeModel.position + r3
        names = '\n\t\t\t\tfx_expanding_sprite02\n\t\t\t\tfw_green_white_burst\n\t\t\t\tfw_purple_burst\n\t\t\t\tfw_red_green_burst\n\t\t\t\tfw_red_yellow_burst\n\t\t\t\tfw_white_jitter_burst\n\t\t\t\tfw_white_sparse_burst'.split()
        part = Pixie.create('particles/%s.xml' % random.choice(names))
        mexpl.root.attach(part)
        BigWorld.callback(0.3, lambda mexpl = mexpl: self._soundPlay(mexpl))

    def _soundPlay(self, model):
        model.playSound(self.SOUND_BOOMS)
        model.scale = (5, 5, 5)
        BigWorld.callback(0.5, lambda model = model: self._scaleOff(model))
        BigWorld.callback(4.0, lambda model = model: self.delExpl(model))

    def _scaleOff(self, model):
        model.scale = (0.1, 10, 0.1)

    def delExpl(self, model):
        BigWorld.delModel(model)

    def _delHelpsModels(self):
        try:
            BigWorld.delModel(self.flyModel)
        except Exception as e:
            pass

        try:
            BigWorld.delModel(self.explodeModel)
        except Exception as e:
            pass

        if self.modelFuseS:
            try:
                BigWorld.delModel(self.modelFuseS)
            except Exception as e:
                pass