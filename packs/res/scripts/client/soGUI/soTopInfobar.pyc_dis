# Embedded file name: scripts/client/soGUI/soTopInfobar.py
import BigWorld
import BWPersonality
import GUI
import soGUI
import Helpers.PyGUI as PyGUI
import Helpers.Listener as Listener
from Helpers.BWCoroutine import *
import time

class soTopInfobar(PyGUI.Window):
    factoryString = 'soGUI.soTopInfobar'
    onlineCountOffset = 50
    fragCountOffset = 150
    localTimeOffset = 150
    frameOffset = 200
    onlineCountTextureName = 'soGUI/maps/Icons/onlineCount.tga'
    fragCountTextureName = 'soGUI/maps/Icons/frags.tga'
    timeTextureName = 'soGUI/maps/Icons/time.tga'

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        component.script = self
        self.onlineCountIcon = None
        self.fragCountIcon = None
        self.localTimeIcon = None
        self.onlineCountLabel = None
        self.fragCountLabel = None
        self.localTimeLabel = None
        self.setupLabels()
        return

    def bindInfobar(self):
        BigWorld.player().addListener('setInfobarOnline', self.updateOnline)

    @BWMemberCoroutine
    def updateTime(self):
        while self.component.visible:
            yield BWWaitForPeriod(1.0)
            tm = time.localtime()
            self.localTimeLabel.text = str(tm.tm_hour) + ':' + str(tm.tm_min)

    def updateFrags(self, count):
        self.fragCountLabel.text = str(count)

    def updateOnline(self, count):
        self.onlineCountLabel.text = str(count)

    def setupFrame(self):
        self.component.verticalAnchor = 'TOP'
        self.component.horizontalAnchor = 'LEFT'
        self.component.verticalPositionMode = 'CLIP'
        self.component.horizontalPositionMode = 'CLIP'
        self.component.widthMode = 'PIXEL'
        self.component.heightMode = 'PIXEL'
        self.component.position = (-1.0 + soGUI.getPixelWidth(self.component.parent) * soTopInfobar.frameOffset, 1.0, 0.0)
        self.component.width = 600
        self.component.height = 40
        self.component.textureName = 'soGUI/maps/Controls/top_info.tga'

    def setupIcons(self):
        self.onlineCountIcon = GUI.Simple(soTopInfobar.onlineCountTextureName)
        self.onlineCountIcon.verticalAnchor = 'CENTER'
        self.onlineCountIcon.horizontalAnchor = 'LEFT'
        self.onlineCountIcon.widthMode = 'PIXEL'
        self.onlineCountIcon.heightMode = 'PIXEL'
        self.onlineCountIcon.verticalPositionMode = 'CLIP'
        self.onlineCountIcon.horizontalPositionMode = 'CLIP'
        self.onlineCountIcon.position = (-1.0 + soGUI.getPixelWidth(self.component) * soTopInfobar.onlineCountOffset, 0.0, 0.0)
        self.onlineCountIcon.width = 35
        self.onlineCountIcon.height = 35
        self.onlineCountIcon.visible = True
        self.component.addChild(self.onlineCountIcon, 'onlineIcon')
        self.fragCountIcon = GUI.Simple(soTopInfobar.fragCountTextureName)
        self.fragCountIcon.verticalAnchor = 'CENTER'
        self.fragCountIcon.horizontalAnchor = 'LEFT'
        self.fragCountIcon.widthMode = 'PIXEL'
        self.fragCountIcon.heightMode = 'PIXEL'
        self.fragCountIcon.verticalPositionMode = 'CLIP'
        self.fragCountIcon.horizontalPositionMode = 'CLIP'
        self.fragCountIcon.position = (self.onlineCountIcon.position[0] + soGUI.getPixelWidth(self.component) * soTopInfobar.fragCountOffset, 0.0, 0.0)
        self.fragCountIcon.width = 35
        self.fragCountIcon.height = 35
        self.fragCountIcon.visible = True
        self.component.addChild(self.fragCountIcon, 'gragIcon')
        self.localTimeIcon = GUI.Simple(soTopInfobar.timeTextureName)
        self.localTimeIcon.verticalAnchor = 'CENTER'
        self.localTimeIcon.horizontalAnchor = 'LEFT'
        self.localTimeIcon.widthMode = 'PIXEL'
        self.localTimeIcon.heightMode = 'PIXEL'
        self.localTimeIcon.verticalPositionMode = 'CLIP'
        self.localTimeIcon.horizontalPositionMode = 'CLIP'
        self.localTimeIcon.position = (self.fragCountIcon.position[0] + soGUI.getPixelWidth(self.component) * soTopInfobar.fragCountOffset, 0.0, 0.0)
        self.localTimeIcon.width = 35
        self.localTimeIcon.height = 35
        self.localTimeIcon.visible = True
        self.component.addChild(self.localTimeIcon, 'timeIcon')

    def setupLabels(self):
        self.onlineCountLabel = GUI.Text('value')
        self.onlineCountLabel.verticalAnchor = 'TOP'
        self.onlineCountLabel.horizontalAnchor = 'RIGHT'
        self.onlineCountLabel.widthMode = 'PIXEL'
        self.onlineCountLabel.heightMode = 'PIXEL'
        self.onlineCountLabel.verticalPositionMode = 'CLIP'
        self.onlineCountLabel.horizontalPositionMode = 'CLIP'
        self.onlineCountLabel.position = (1.0, 1.0, 0.0)
        self.onlineCountLabel.font = 'ruRU_calibri_default.font'
        self.onlineCountLabel.visible = True
        GUI.addRoot(self.onlineCountLabel)