# Embedded file name: scripts/common/AnomalyCommon.py
import BigWorld
import bwdecorators
from Config import Anomalies as Cfg

class AnomalyCommon:
    """Anomaly methods which are the same on cell and client."""

    @bwdecorators.callableOnGhost
    def get_config(self, param = None):
        if param is None:
            return Cfg.get_config(self.anomalyType)
        else:
            return Cfg.get_config(self.anomalyType)[param]
            return

    @bwdecorators.callableOnGhost
    def get_state_config(self, state = None):
        if state is None:
            return self.get_config('states')[self.state]
        else:
            return self.get_config('states')[state]
            return