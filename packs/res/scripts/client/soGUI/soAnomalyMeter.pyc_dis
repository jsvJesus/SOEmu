# Embedded file name: scripts/client/soGUI/soAnomalyMeter.py
import BigWorld
import GUI
import BWPersonality
import Helpers.PyGUI as PyGUI
import soGUI

class soAnomalyMeter(PyGUI.PyGUIBase):
    factoryString = 'soGUI.soAnomalyMeter'
    baseTextureName = 'soGUI/maps/Controls/AnomalyMeter/anomalyMeter'

    def __init__(self, component):
        PyGUI.PyGUIBase.__init__(self, component)
        component.script = self
        self.levelCount = 9
        self.levelTextures = {}
        self.setupRoot()
        self.setupMeter()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 113
        cmp.height = 79
        cmp.position = (0, 37, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        cmp.textureName = ''

    def setupMeter(self):
        for i in xrange(self.levelCount):
            cmp = GUI.Window()
            cmp.textureName = self.baseTextureName + '_' + str(i) + '.tga'
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.pixelSnap = True
            cmp.filterType = 'LINEAR'
            cmp.width = 113
            cmp.height = 79
            cmp.position = (-1.0, 1.0, 0.1)
            cmp.visible = False
            self.component.addChild(cmp, 'level' + str(i))
            self.levelTextures[i] = cmp

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'AnomalyMeter')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False

    def setThreatLevel(self, lvl):
        if lvl < 0:
            self.component.visible = False
        if self.levelTextures.has_key(lvl):
            for texture in self.levelTextures:
                self.levelTextures[texture].visible = False

            self.levelTextures[lvl].visible = True