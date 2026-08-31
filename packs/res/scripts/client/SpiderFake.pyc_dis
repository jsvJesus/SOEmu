# Embedded file name: scripts/client/SpiderFake.py
import BigWorld
import SFXer
import Math
import math
import random
import Pixie
import BWPersonality

class SpiderFake(object):
    S_MAXSTEPS = 3000
    S_MODELHEIGHT = 1.0
    S_STEP_SIZE = 0.02
    S_STEP_TIME = 0.01
    S_DAMAGE = True
    S_SPAWNMINTIME = 0.5
    S_SPAWNMAXTIME = 2.0
    S_SPAWNMIN = 1
    S_SPAWNMAX = 10
    S_CAMUP = (0.3, 0.7, 0.1)
    _timerSpTickID = 0
    _timerFakeDamageID = 0
    _timerSpSpawnID = 0
    _isShosDamage = False

    def onEnterWorld(self):
        self.spiderModelsDict = {}
        self.stepSpiders()
        self.fakeDamage()
        print 'onEnterWorld SpiderFake', self, self.id

    def startSpiderHallucianations(self):
        print 'startSpiderHallucianations'
        self._isShosDamage = True
        if not self._timerSpSpawnID:
            self.spiderHallucianationsSpawnTick()

    def stopSpiderHallucianations(self):
        print 'stopSpiderHallucianations'
        self._isShosDamage = False
        if self._timerSpSpawnID:
            BigWorld.cancelCallback(self._timerSpSpawnID)
        self._timerSpSpawnID = 0
        BigWorld.camera().uprightDirection = (0, 1, 0)

    def spiderHallucianationsSpawnTick(self):
        timeResp = random.randrange(1, 5, int=float)
        self._timerSpSpawnID = BigWorld.callback(timeResp, self.spiderHallucianationsSpawnTick)
        if not self.isInWorld:
            return
        BigWorld.camera().uprightDirection = self.S_CAMUP
        cpos = BigWorld.camera().position
        cdir = BigWorld.camera().direction
        for x in range(random.randrange(self.S_SPAWNMIN, self.S_SPAWNMAX)):
            cdir = Math.Vector3(cdir.x + random.random() / 5 * random.choice([1, -1, 0]), cdir.y + random.random() / 5 * random.choice([1, -1, 0]), cdir.z + random.random() / 5 * random.choice([1, -1, 0]))
            self.addSpider(cpos, cdir)

    def cancelSpider(self):
        self._isShosDamage = False
        BigWorld.cancelCallback(self._timerSpTickID)
        BigWorld.cancelCallback(self._timerFakeDamageID)
        BigWorld.cancelCallback(self._timerSpSpawnID)
        for model in self.spiderModelsDict:
            self.delModel(model)

        self.spiderModelsDict = {}
        BigWorld.camera().uprightDirection = (0, 1, 0)

    def fakeDamage(self):
        self._timerFakeDamageID = BigWorld.callback(random.randrange(1, 5, int=float), self.fakeDamage)
        if not self.isInWorld:
            return
        if self.S_DAMAGE and self._isShosDamage and self.spiderModelsDict:
            direct = random.randrange(0, 5)
            BWPersonality.GUICore.showDamage(random.randrange(0.5, 3, int=float), direct, 1)
            if direct < 5:
                BigWorld.camera().shake(0.1, (0.03, 0.03, 0.03))

    def addSpider(self, scrFrom, direction, distance = 30.0, scale = 1.0):
        if not self.isInWorld:
            return
        posTo = scrFrom + direction * distance
        col = BigWorld.collide(self.spaceID, scrFrom, posTo)
        if not col:
            return False
        m = BigWorld.Model('characters\\creatures\\spider\\spider.model')
        self.addModel(m)
        target_normal = SFXer.tri_normal(col[1])
        target_normal.normalise()
        matr = Math.Matrix(m.matrix)
        modeldir = matr.applyToAxis(1)
        modeldir.normalise()
        m.position = col[0]
        axis = modeldir * target_normal
        axis.normalise()
        angle = math.acos(modeldir.dot(target_normal))
        m.rotate(angle, axis, (0, 0, 0))
        matr = Math.Matrix(m.matrix)
        modeldirUp = matr.applyToAxis(1)
        m.rotate(random.random() * 6, modeldirUp, (0, 0, 0))
        rrr = random.random() / 10
        m.scale = (0.1 + rrr, 0.1 + rrr, 0.1 + rrr)
        m.spider_spawn().spider_walk_fake2()

        def addToDict():
            self.spiderModelsDict[m] = 0

        BigWorld.callback(1.0, addToDict)

    def stepSpiders(self):
        self._timerSpTickID = BigWorld.callback(self.S_STEP_TIME, self.stepSpiders)
        for model in self.spiderModelsDict.keys():
            nstep = self.spiderModelsDict[model]
            if nstep > self.S_MAXSTEPS:
                self.killSpider(model)
                continue
            nstep += 1
            matr = Math.Matrix(model.matrix)
            modeldirUp = matr.applyToAxis(1)
            modeldirF = matr.applyToAxis(2)
            modeldirUp.normalise()
            modeldirF.normalise()
            cpos = model.position + modeldirUp * self.S_MODELHEIGHT + modeldirF * self.S_STEP_SIZE
            posto = cpos - modeldirUp * self.S_MODELHEIGHT * 2
            cpos1 = model.position + modeldirUp * self.S_MODELHEIGHT
            col = BigWorld.collide(self.spaceID, cpos1, posto)
            if not col:
                col = BigWorld.collide(self.spaceID, cpos, posto)
            if not col:
                col = BigWorld.collide(self.spaceID, cpos, posto - modeldirF * self.S_STEP_SIZE)
            if col:
                lastpos = model.position
                newpos = col[0]
                if newpos.distTo(lastpos) > self.S_STEP_SIZE * 2:
                    newpos = lastpos + (newpos - lastpos) * self.S_STEP_SIZE * 2
                    nstep += 10
                model.position = newpos
                target_normal = SFXer.tri_normal(col[1])
                target_normal.normalise()
                axis = modeldirUp * target_normal
                axis.normalise()
                cos = modeldirUp.dot(target_normal)
                cos = min(cos, 1.0)
                cos = max(cos, -1.0)
                angle = math.acos(cos)
                angleV = 1 if angle > 0 else -1
                angle = min(abs(angle), 0.07) * angleV
                model.rotate(angle, axis, (0, 0, 0))
            else:
                model.rotate(model.yaw + random.random(), modeldirUp, (0, 0, 0))
                nstep += 100
            self.spiderModelsDict[model] = nstep

    def traceBulletSpiders(self, scrFrom, direction):
        for model in self.spiderModelsDict.keys():
            mpos = model.position
            cm = mpos - scrFrom
            distM = cm.length
            cm.normalise()
            d = math.acos(direction.dot(cm))
            d = math.sin(d)
            distBullet = d * distM
            if distBullet < 0.5:
                self.killSpider(model)

    def killSpider(self, model):
        if model in self.spiderModelsDict:
            del self.spiderModelsDict[model]
        particl = Pixie.create('particles/zyb_pers.xml')
        m2 = BigWorld.Model('')
        m2.position = model.position
        BigWorld.player().addModel(m2)
        m2.root.attach(particl)

        def scaleMin():
            model.scale = model.scale * 0.8

        def scaleMax():
            model.scale = model.scale * 1.2

        for x in range(2):
            BigWorld.callback(0.05 * x, scaleMax)

        for x in range(2, 22):
            BigWorld.callback(0.05 * x, scaleMin)

        BigWorld.callback(2, lambda : self.delModel(model))
        BigWorld.callback(5, lambda : self.delModel(m2))