# Embedded file name: scripts/client/__debug/__init__.py
import BWPersonality
from MatrixSwarmTest import Pixie_MatrixSwarm_Tester
import MatrixSwarmTest_config as MST_config

def matrixSwarmTest():
    pmt = Pixie_MatrixSwarm_Tester(MST_config.particle_path)
    BWPersonality.GUICore.setDebugBtn(1, 'Reload particle', 235, 15, w=100, h=21, callBack=pmt.load)