# Embedded file name: scripts/client/Throwable.py
import BigWorld
import BWPersonality
import GUI
import Pixie
from Math import Vector3, Matrix
from ThrowingData import Throwing, ThrowTypes
from FX_extension import PersistentSFX
import random
from functools import partial

class Throwable:

    def __init__(self):
        self.last_distance = 99999
        self.isAnomaly = False
        self.isJumped = False

    def prerequisites(self):
        return [self.getModelName()]

    def onLeaveWorld(self):
        pass

    def onEnterWorld(self, prereqs):
        model = prereqs[self.getModelName()]
        if not isinstance(model, BigWorld.Model):
            self.model = BigWorld.Model('')
        else:
            self.model = model
        self.model.visible = False
        if self.clientEntityID and self.ownerID == BigWorld.player().id:
            return
        try:
            thrower = BigWorld.entities[self.ownerID]
            thrower.onThrowingEntityAppears(self)
        except KeyError:
            pass

    def startAnomalyEffectHit2(self, anomalyEntityID, anomalyPos, anomalyRadius):
        anomaly = BigWorld.entity(anomalyEntityID)
        if anomaly:
            self.anomaly_position = anomaly.position
            aconfig = anomaly.get_state_config()
            self.anomaly_radius = aconfig['radius'] ** 2
        else:
            self.anomaly_position = anomalyPos
            self.anomaly_radius = anomalyRadius ** 2
        if self.fromServer:
            self.anomaly_timer = BigWorld.callback(0.3, self.CheckIsAnomaly)
        else:
            self.anomaly_timer = BigWorld.callback(0.1, self.CheckIsAnomaly)

    def CheckIsAnomaly(self):
        dist = self.model.position.distSqrTo(self.anomaly_position)
        if dist <= self.anomaly_radius or self.last_distance < dist:
            self.startAnomalyEffHit()
        else:
            if not self.model.motors:
                self.startAnomalyEffHit()
                return
            self.last_distance = dist
            self.anomaly_timer = BigWorld.callback(0.05, self.CheckIsAnomaly)

    def startAnomalyEffHit(self):
        self.anomalyEffHit()

    def anomalyEffHit(self):
        position = self.model.position
        self.isAnomaly = True
        particl = Pixie.create('particles/zyb_pers.xml')
        p = BigWorld.player()
        direction = (0, 0, 0)
        properties = {}
        self.tmp_ent_id = BigWorld.createEntity('EmptyEntity', p.spaceID, 0, p.position, direction, properties)
        ent = BigWorld.entity(self.tmp_ent_id)
        m = BigWorld.Model('')
        m.position = position
        m.root.attach(particl)
        ent.models = [m]

        def removeAnomalyHitEff(eid):
            BigWorld.destroyEntity(eid)

        BigWorld.callback(10, partial(removeAnomalyHitEff, self.tmp_ent_id))
        self.model.visible = False

    def removeAnomalyHitEff(self):
        BigWorld.destroyEntity(self.tmp_ent_id)

    def GraviJumpStone(self):
        self.isAnomaly = True
        self.isJumped = True
        self.eff = Pixie.create('particles/jetpack_flame01.xml')
        self.model.root.attach(self.eff)
        self.bouncer2 = bouncer = BigWorld.Bouncer()
        bouncer.vx = self.velocity[0]
        bouncer.vy = 10
        bouncer.vz = self.velocity[2]
        bouncer.tripTime = 200
        bouncer.timeSlice = 0.03333
        self.model.motors = (self.bouncer2,)
        elasticity = 0.2
        radius = 0.1
        maxBounces = 0
        startPosition = self.model.position
        finalPosition = self.model.position
        timeBeforeFlyEnd, reachTime = self.bouncer2.calcPath(startPosition, startPosition, (0, 0, 0), elasticity, radius, maxBounces)
        BigWorld.callback(timeBeforeFlyEnd, self.onFlyEnd)

    def throw(self):
        throwData = Throwing[self.throwingType]
        self.model.visible = True
        modelSFX = throwData['modelSFX']
        if modelSFX is not None:
            self.__sfx = PersistentSFX(throwData['modelSFX'], self.model)
            self.__sfx.play()
        particles = throwData['particles']
        if particles:
            particl = Pixie.create(particles)
            self.model.root.attach(particl)
        self.bouncer = BigWorld.Bouncer()
        self.bouncer.vx = self.velocity[0]
        self.bouncer.vy = self.velocity[1]
        self.bouncer.vz = self.velocity[2]
        self.bouncer.tripTime = throwData['tripTime']
        self.bouncer.timeSlice = throwData['timeSlice']
        elasticity = throwData['elasticity']
        radius = throwData['radius']
        maxBounces = throwData['maxBounces']
        if self.fromServer:
            timeBeforeFlyEnd = self.bouncer.estimatePath(self.startPosition, elasticity, radius, maxBounces)
            if self.anomalyEntityID:
                self.startAnomalyEffectHit2(self.anomalyEntityID, self.posHitAnomaly, self.radiusHitAnomaly)
        else:
            timeBeforeFlyEnd = self.bouncer.estimatePath(self.startPosition, elasticity, radius, maxBounces)
        self.model.motors = (self.bouncer,)
        if timeBeforeFlyEnd <= self.bouncer.tripTime:
            BigWorld.callback(timeBeforeFlyEnd, self.onFlyEnd)
        else:
            BigWorld.callback(self.bouncer.tripTime, self.onFlyEnd)
        try:
            self.model.ShotFly()
        except:
            pass

        return

    def hideStone(self):
        self.model.visible = False

    def onFlyEnd(self):
        if self.throwingType == ThrowTypes.GRENADE_MOLOTOV and not self.fromServer:
            self.explodeMolotov()
            return
        if self.isAnomaly and self.isJumped:
            clientSourcePos = self.model.position
            serverSourcePos = self.model.position
            destPos = self.model.position
            self.bouncer.updatePath(clientSourcePos, serverSourcePos)
            self.bouncer2.updatePath(clientSourcePos, serverSourcePos)
            return
        try:
            if not self.isAnomaly:
                self.model.motors = []
        except Exception as ex:
            pass

        try:
            self.model.ShotFly.stop()
        except Exception as ex:
            pass

        try:
            self.model.ShotLay()
        except Exception as ex:
            pass

    def thrownFromThisClient(self):
        return self.ownerID == BigWorld.player().id and self.clientEntityID != 0

    def removeClientEntity(self):
        if self.thrownFromThisClient():
            try:
                clientGrenade = BigWorld.entities[self.clientEntityID]
                BigWorld.destroyEntity(self.clientEntityID)
            except KeyError:
                pass

    def getModelName(self):
        try:
            return Throwing[self.throwingType].get('modelName', '')
        except Exception as ex:
            print 'Throwable.getModelName:', ex

        return ''

    def showID(self):
        text = GUI.Text(str(self.id))
        text.explicitSize = True
        text.size = (0, 0.4)
        text.colour = (255, 205, 149, 245)
        text.filterType = 'LINEAR'
        text.verticalAnchor = 'BOTTOM'
        text.position = (0, 0.1 + random.random(), 0)
        atch = GUI.Attachment()
        atch.component = text
        atch.faceCamera = True
        self.text_atch = atch
        self.model.root.attach(atch)