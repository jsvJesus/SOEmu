# Embedded file name: scripts/client/soGUI/choiceTeam.py
import BigWorld
import BWPersonality
import GUI
import Scaleform
import Keys
import Helpers.PyGUI as PyGUI
import weakref
from bwdebug import *
import soGUI.ScaleformDemo

class choiceTeamGUI(PyGUI.PyGUIBase):
    calb = None

    def __init__(self):
        path = 'scaleformUI/choiceTeam.swf'
        self.flashClip = soGUI.ScaleformDemo.ScaleformDemo.create(path, 0.0)
        cmp = self.flashClip
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2.7
        cmp.height = 2
        w, h = BigWorld.screenSize()
        cmp.position = (w / 2, 0.1, 0.1)
        GUI.reSort()
        cmp.focus = 1
        cmp.mouseButtonFocus = 1
        cmp.visible = 0
        BWPersonality.GUICore.generalLayer.delChild('choiceTeamWindow')
        BWPersonality.GUICore.generalLayer.addChild(self.flashClip, 'choiceTeamWindow')
        self.flashClip.script.setExternalInterfaceCallback(self.externalInterfaceHandler)
        self.bk = Background(GUI.Window())
        self.bk.onBound()
        BWPersonality.GUICore.generalLayer.reSort()

    def isVisible(self):
        return self.flashClip.visible

    def externalInterfaceHandler(self, cmd, args):
        if cmd == 'choiceTeam':
            print 'choiceTeam', args[0]
            self.hide()
            BigWorld.player().base.changeTeam(int(args[0]))

    def show(self, blackBG):
        self.flashClip.visible = True
        self.bk.show(blackBG)

    def hide(self):
        self.flashClip.visible = False
        self.bk.hide()


class Background(PyGUI.PyGUIBase):
    factoryString = 'soGUI.Background'

    def __init__(self, component):
        PyGUI.PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 0, 0, 150)
        cmp.materialFX = 'BLEND'
        cmp.textureName = 'soGUI/maps/Colours/black.bmp'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        cmp.visible = False

    def setupContent(self):
        pass

    def show(self, blackBG):
        if self.component.parent is None:
            BWPersonality.GUICore.generalLayer.delChild('selectMapBack')
            BWPersonality.GUICore.generalLayer.addChild(self.component, 'selectMapBack')
        self.component.visible = True
        if blackBG:
            self.component.colour = (255, 0, 0, 255)
        else:
            self.component.colour = (255, 0, 0, 150)
        return

    def hide(self):
        self.component.visible = False