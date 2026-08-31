# Embedded file name: scripts/client/soGUI/soQueueScreen.py
from Localization import lc
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import BWPersonality
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.PyGUI import PyGUIEvent
from soGUI.soButton import soButton
from Keys import *
from soGUI.soTextField import soTextField3

class soQueueScreen(PyGUIBase):
    factoryString = 'soGUI.soQueueScreen'
    EVENT_CANCEL = 0

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupFrame()

    def setupRoot(self):
        cmp = self.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.0)
        cmp.colour = (255, 255, 255, 128)
        cmp.materialFX = 'BLEND'
        cmp.tileWidth = 1
        cmp.tileHeight = 1
        cmp.tiled = True
        cmp.textureName = 'soGUI/maps/Colours/black.bmp'
        cmp.mouseButtonFocus = True
        cmp.focus = True
        cmp.crossFocus = True
        cmp = GUI.Window()
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.width = 460
        cmp.height = 120
        cmp.position = (0.0, 0.0, 0.0)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'frameHolder')

    def setupFrame(self):
        cmp = GUI.Frame2('soGUI/maps/con_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 1.0)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.frameHolder.addChild(cmp, 'frameCmp')
        txt = soTextField3(GUI.Window(), width=450, height=80, textWidth=-1, hScroll=False, vScroll=False, hideScroll=False, borderWidth=0, vOffset=0, hOffset=0, textureless=True, autosize=False)
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (5, 5, 0.2)
        self.component.frameHolder.addChild(cmp, 'lbl')
        txt.onBound()
        txt.setText(u'<alignment=center>jsdfhgjsdhgfjsagdjfhg sjdfgsjdfhgsjdh fgjshdfgjshdfjshfgjsfd<n>sadfasdfasdfasdfsadfasfd')
        cancelBtn = soButton(GUI.Window())
        cancelBtn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cancelBtn.onBound()
        cancelBtn.component.label.text = lc('soQueueScreen.soGUI.STRING_105_35')
        cmp = cancelBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 90
        cmp.height = 28
        cmp.position = (230, 70, 0.5)
        self.component.frameHolder.addChild(cmp, 'cancelBtn')

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.menuLayer.addChild(self.component)
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False

    def update(self):
        self.component.frameHolder.lbl.script.setText(BWPersonality.GUICore.queueDataSection)

    def handleKeyEvent(self, event):
        key = event.key
        char = event.character
        mods = event.modifiers
        down = event.isKeyDown()
        if key == KEY_ESCAPE:
            if down:
                BWPersonality.GUICore.queueEvent(self.EVENT_CANCEL, None)
        return True

    @PyGUIEvent('frameHolder.cancelBtn', 'onClick')
    def onCancelBtnClick(self):
        BWPersonality.GUICore.queueEvent(self.EVENT_CANCEL, None)
        return