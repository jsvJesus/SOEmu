# Embedded file name: scripts/client/ModelSelector.py
import BigWorld
import ResMgr
DEFAULT_MODEL = 0

class ModelSelector:
    FLAG_MODEL = 50
    FLAGPOLE_MODEL = 51
    FLAGPOLE_AND_FLAG_MODEL = 28
    SIGN_STAR_1 = 29
    SIGN_STAR_2 = 30
    SIGN_STAR_3 = 40
    MODELS = {}
    source = ResMgr.openSection('scripts/client/data/editor.xml')
    for item in source.values():
        MODELS[item['value'].asInt] = item['path'].asString

    def prerequisites(self):
        return [self.MODELS[self.modelSelect]]

    def setObstacleModel(self):
        self.model = BigWorld.PyModelObstacle(self.MODELS[self.modelSelect], self.matrix, 0)

    def setNormalModel(self, prereqs = None):
        if prereqs is None:
            self.model = BigWorld.Model(self.MODELS[self.modelSelect])
        else:
            self.model = prereqs[self.MODELS[self.modelSelect]]
        return

    def onEnterWorld(self, prereqs):
        self.setNormalModel(prereqs)