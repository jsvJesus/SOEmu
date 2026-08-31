# Embedded file name: scripts/common/WorkbenchUtil.py
from Localization import lc
TYPE_WORKBENCH_NONE = 0
TYPE_WORKBENCH_NOOB = 1
TYPE_WORKBENCH_CHEMICAL = 2
TYPE_WORKBENCH_PRO = 3
TYPE_WORKBENCH_ELECTRICAL = 4
MODELS = {TYPE_WORKBENCH_NOOB: 'models/entities/craft_table01.model',
 TYPE_WORKBENCH_CHEMICAL: 'models/entities/containers/medical_bag_01_entity.model',
 TYPE_WORKBENCH_PRO: 'models/props/streetobjects/Billboard_01_lod1.model',
 TYPE_WORKBENCH_ELECTRICAL: 'models/entities/containers/electronics_pile_02_entity.model'}
LSNAMES = {TYPE_WORKBENCH_NOOB: lc('Workbench.names.TYPE_WORKBENCH_NOOB'),
 TYPE_WORKBENCH_CHEMICAL: lc('Workbench.names.TYPE_WORKBENCH_CHEMICAL'),
 TYPE_WORKBENCH_PRO: lc('Workbench.names.TYPE_WORKBENCH_PRO'),
 TYPE_WORKBENCH_ELECTRICAL: lc('Workbench.names.TYPE_WORKBENCH_ELECTRICAL')}
ERRORMODEL = 'models/entities/containers/bag.model'

def getNameModel(wtype):
    return MODELS.get(wtype, ERRORMODEL)


def getName(wtype):
    return LSNAMES.get(wtype, '???')