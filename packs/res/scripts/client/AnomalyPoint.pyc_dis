# Embedded file name: scripts/client/AnomalyPoint.py
import BigWorld
import random
import Config
import Config.Anomalies
from utils_bw import get_enum_from_alias_widget

class AnomalyPoint(BigWorld.UserDataObject):

    def getAllowedAnomalyTypes(self):
        """Return allowed anomaly types."""
        result = []
        terrain_anomalies = Config.Anomalies.get_anomalies_for_terrain(random.randint(1, 94))
        for anomaly_id in terrain_anomalies:
            result.append(anomaly_id)

        return result

    def __init__(self):
        BigWorld.UserDataObject.__init__(self)
        BigWorld.createEntity('Anomaly', BigWorld.player().spaceID, 0, self.position, self.direction, {'anomalyType': random.choice(self.getAllowedAnomalyTypes()),
         'state': 1})