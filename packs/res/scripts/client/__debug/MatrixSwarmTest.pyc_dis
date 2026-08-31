# Embedded file name: scripts/client/__debug/MatrixSwarmTest.py
import BigWorld
import ResMgr
import Pixie
from Math import Vector3

def _getMatrixSwarm(particle):
    for action in particle.actions:
        if action.__class__.__name__ == 'MatrixSwarmPSA':
            return action


class Pixie_MatrixSwarm_Tester:

    def __init__(self, particlePath):
        self.particlePath = particlePath
        self.models = []
        self.pixies = []
        self.load()

    def getModel(self, pos):
        m = BigWorld.Model('helpers/models/unit_sphere.model')
        BigWorld.player().addModel(m)
        m.position = pos
        self.models.append(m)
        return m

    def getPixie(self):
        p = Pixie.create(self.particlePath)
        self.pixies.append(p)
        return p

    def removeResources(self):
        pl = BigWorld.player()
        for pixie in self.pixies:
            try:
                pl.model.root.detach(pixie)
            except ValueError:
                pass
            except TypeError:
                pass

        for model in self.models:
            try:
                pl.delModel(model)
            except TypeError:
                pass
            except ValueError:
                pass

    def load(self):
        pl = BigWorld.player()
        self.removeResources()
        ResMgr.purge(self.particlePath, True)
        pixie = self.getPixie()
        if pixie.__class__.__name__ == 'MetaParticleSystem':
            systems = [ pixie.system(i) for i in xrange(pixie.nSystems()) ]
        else:
            systems = [pixie]
        horizModelsDist = 8
        distFromPlayer = 3
        vertShift = 1
        for particle in systems:
            horizShift = 0
            matrixSwarm = _getMatrixSwarm(particle)
            m1 = self.getModel(pl.position + Vector3(distFromPlayer, vertShift, horizShift - horizModelsDist / 2))
            m2 = self.getModel(pl.position + Vector3(distFromPlayer, vertShift, horizShift + horizModelsDist / 2))
            matrixSwarm.targets = [m2.root]
            m1.root.attach(particle)
            vertShift += 1.5

    def __call__(self):
        pass