# Embedded file name: scripts/client/soGUI/soHelpGUIs.py
import BigWorld
import GUI
import soGUI
import BWPersonality
from Helpers.PyGUI import PyGUIBase
from soGUI.soTextField import soTextField3

class soTutorialGUI(PyGUIBase):
    factoryString = 'soGUI.soTutorialGUI'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 300
        cmp.height = 400
        cmp.textureName = ''
        cmp.visible = False
        cmp.position.z = 0.1

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/tt_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.5)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.addChild(cmp, 'frameCmp')
        txt = soTextField3(GUI.Window(), width=280, textWidth=-1, hScroll=False, vScroll=True, hideScroll=True, borderWidth=0, vOffset=0, hOffset=0, textureless=True, autosize=True)
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (15, 15, 0.2)
        self.component.addChild(cmp, 'textOut')
        txt.onBound()

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'tutorialGUI')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False

    def update(self):
        data = BWPersonality.GUICore.tutorialDataSection
        x = data[0][0]
        y = data[0][1]
        if isinstance(x, int):
            self.component.horizontalPositionMode = 'PIXEL'
            self.component.horizontalAnchor = 'LEFT'
        elif isinstance(x, float):
            self.component.horizontalPositionMode = 'CLIP'
            self.component.horizontalAnchor = 'CENTER'
        if isinstance(y, int):
            self.component.verticalPositionMode = 'PIXEL'
            self.component.verticalAnchor = 'TOP'
        elif isinstance(y, float):
            self.component.verticalPositonMode = 'CLIP'
            self.component.verticalAnchor = 'CENTER'
        self.component.position.x = x
        self.component.position.y = y
        txt = data[1]
        self.component.textOut.script.setText(txt)
        self.component.width = self.component.textOut.width + 30
        self.component.height = self.component.textOut.height + 30