# Embedded file name: scripts/client/Boids.py
import BigWorld
import random
MODELS = ['characters\\creatures\\crow\\crow.model']

class Boids(BigWorld.Entity):

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.filter = BigWorld.BoidsFilter()
        self.filter.speed = self.boidsVelocity / 10
        self.filter.approachRadius = self.approachRadius
        self.filter.collisionFraction = self.collisionFraction
        self.filter.influenceRadius = self.influenceRadius

    def prerequisites(self):
        list = []
        for i in xrange(self.boidsCount):
            list.append(MODELS[self.boidsModel])

        return list

    def onEnterWorld(self, prereqs):
        boidModels = prereqs.values()
        for model in boidModels:
            model.outsideOnly = 1
            self.addModel(model)
            model.Flap(-5 * random.random())

    def onLeaveWorld(self):
        self.models = []