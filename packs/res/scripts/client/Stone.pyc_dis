# Embedded file name: scripts/client/Stone.py
import BigWorld
from Throwable import Throwable
import Pixie
import GUI

class Stone(BigWorld.Entity, Throwable):

    def __init__(self):
        BigWorld.Entity.__init__(self)
        Throwable.__init__(self)

    def onExistenceOver(self):
        self.removeClientEntity()

    def startAnomalyEffectHit(self, anomalyEntityID, anomalyPos, anomalyRadius):
        self.startAnomalyEffectHit2(anomalyEntityID, anomalyPos, anomalyRadius)