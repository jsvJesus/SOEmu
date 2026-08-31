# Embedded file name: scripts/client/Thrower.py
import BigWorld
from ThrowingData import Throwing

class Thrower:

    def __init__(self):
        pass

    def throw(self, throwingType, entity_params, position, velocity):
        throwData = Throwing[throwingType]
        throwing_params = {'throwingType': throwingType,
         'ownerID': self.id,
         'clientEntityID': 0,
         'fromServer': False,
         'startPosition': position,
         'velocity': velocity}
        entity_params.update(throwing_params)
        entityID = BigWorld.createEntity(throwData['entityClassName'], self.spaceID, 0, position, (0, 0, 0), entity_params)
        return entityID

    def onThrowingEntityAppears(self, entity):
        entity.throw()