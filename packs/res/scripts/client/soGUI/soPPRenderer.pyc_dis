# Embedded file name: scripts/client/soGUI/soPPRenderer.py
import BigWorld
import GUI
import BWPersonality
import soGUI
import ResMgr
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI import PyGUIBase
from random import randint
from copy import deepcopy
from PPData import *

class soPPRenderer(PyGUIBase):
    factoryString = 'soGUI.soPPRenderer'
    PP_CHAIN_PATH = 'system/post_processing/chains/'
    PP_CHAIN_EXT = '.ppchain'
    PP_MASK_PATH = 'soGUI/maps/ppmask/'
    PP_MASK_EXT = '.tga'
    CHAINS_CFG = 'system/post_processing/chains/chains_cfg.xml'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.currentPPs = []
        self.currentSysPPs = []
        self.priorities = {}
        self.setupRoot()
        self.loadPriorities()

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.width = cmp.height = 2.0
        cmp.colour = (255, 255, 255, 255)
        cmp.textureName = ''
        cmp.materialFX = 'BLEND'
        cmp.position = (0.0, 0.0, 2.1)

    def _apply(self):

        def cmpPriority(elem1, elem2):
            if not self.priorities.has_key(elem1):
                return -1
            if not self.priorities.has_key(elem2):
                return 1
            return cmp(self.priorities[elem1], self.priorities[elem2])

        import PostProcessing
        self.currentPPs.sort(cmp=cmpPriority)
        self.currentSysPPs.sort(cmp=cmpPriority)
        ppChain = self.currentSysPPs + self.currentPPs
        loadedChains = []
        for pp in ppChain:
            lchain = PostProcessing.load(self.PP_CHAIN_PATH + pp + self.PP_CHAIN_EXT)
            if lchain is not None:
                loadedChains += lchain
            else:
                print "warning, PPRenderer couldn't load a pp chain {0}".format(pp)

        PostProcessing.chain(loadedChains)
        return

    def getCurrentPPs(self):
        return self.currentPPs

    def getCurrentSysPPs(self):
        return self.currentSysPPs

    def addPP(self, ppName):
        if ppName not in self.currentPPs:
            self.currentPPs.append(ppName)
            self._apply()
            return True
        else:
            return False

    def removePP(self, ppName):
        if ppName in self.currentPPs:
            self.currentPPs.remove(ppName)
            self._apply()
            return True
        else:
            return False

    def removeAll(self):
        self.currentPPs = []
        self._apply()

    def addSysPP(self, ppName):
        if ppName not in self.currentSysPPs:
            self.currentSysPPs.append(ppName)
            self._apply()
            return True
        else:
            return False

    def removeSysPP(self, ppName):
        if ppName in self.currentSysPPs:
            self.currentSysPPs.remove(ppName)
            self._apply()
            return True
        else:
            return False

    def removeAllSys(self):
        self.currentSysPPs = []
        self._apply()

    def loadPriorities(self):
        cfgFile = ResMgr.openSection(self.CHAINS_CFG)
        priorities = cfgFile._priorities
        for index, chain in enumerate(priorities.values()):
            self.priorities[chain.asString] = index

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'PPRender')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False