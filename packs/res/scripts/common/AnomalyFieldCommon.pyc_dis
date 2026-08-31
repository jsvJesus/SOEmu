# Embedded file name: scripts/common/AnomalyFieldCommon.py
import BigWorld
import bwdecorators
from Config import AnomalyFields as Cfg

class AnomalyFieldCommon:
    """AnomalyField methods which are the same on cell and client."""

    @bwdecorators.callableOnGhost
    def get_anomaly_config(self, cell_x, cell_z, param_name = None):
        return Cfg.get_anomaly_config(self.pattern_id, self.group_id, cell_x, cell_z, param_name)

    @bwdecorators.callableOnGhost
    def each_cell(self):
        for x in xrange(Cfg.getCellsXNum(self.pattern_id)):
            for z in xrange(Cfg.getCellsZNum(self.pattern_id)):
                yield (x, z)