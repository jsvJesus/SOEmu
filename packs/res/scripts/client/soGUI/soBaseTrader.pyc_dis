# Embedded file name: scripts/client/soGUI/soBaseTrader.py
import traceback
import BigWorld
import BWPersonality
import GUI
from soGUI.soTextField import soTextField3
from Localization import lc
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soButton import soButton, soButtonWTT
from soGUI.soTextField import soTextField3
import traceback
from Helpers.PyGUI import PyGUIEvent

class soBaseTrader(PyGUIBase):
    factoryString = 'soGUI.soBaseTrader'
    bdata = ('CLAN_NAME', 'CURRENT', 'lastPrice', 'STEP', 'COUNT')
    bNames = [ lc('soBaseTrader.%s' % x) for x in bdata ]
    WIDTH = 600
    HEIGHT = 400

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.dataText = []
        self.setupRoot()
        self.setupContent()
        self.hide()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        sW, sH = BigWorld.screenSize()
        cmp.width = sW
        cmp.height = sH
        cmp.position = ((sW - self.WIDTH) / 2, (sH - self.HEIGHT) / 2, 0.2)

    def setupContent(self):
        sW, sH = BigWorld.screenSize()
        h = sH - 70
        FRAME_TEXTURE = 'soGUI/maps/Controls/inventory/inventoryFrame2.tga'
        self.frameCmp = GUI.Frame2(FRAME_TEXTURE)
        self.frameCmp.horizontalPositionMode = self.frameCmp.verticalPositionMode = 'PIXEL'
        self.frameCmp.widthMode = self.frameCmp.heightMode = 'PIXEL'
        self.frameCmp.horizontalAnchor = 'LEFT'
        self.frameCmp.verticalAnchor = 'TOP'
        self.frameCmp.visible = True
        self.frameCmp.colour = (255, 255, 255, 255)
        self.frameCmp.materialFX = 'BLEND'
        self.frameCmp.width = self.WIDTH
        self.frameCmp.height = self.HEIGHT
        self.frameCmp.position = (0, 0, 0.5)
        self.component.addChild(self.frameCmp, 'frame1')
        closeBox = soButton(GUI.Window())
        cmp = closeBox.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (self.WIDTH - 5, 5, 0)
        cmp.script.onClick = lambda : BWPersonality.GUICore.showBasetrader(False)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        for i, item in enumerate(self.bNames):
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
            cmp.colour = (255, 255, 255, 255)
            cmp.text = item
            cmp.position = (10, 8 + (i + 1) * 25, 0.5)
            self.component.addChild(cmp, self.bdata[i])
            text = GUI.Text('')
            text.horizontalPositionMode = text.verticalPositionMode = 'PIXEL'
            text.horizontalAnchor = 'LEFT'
            text.verticalAnchor = 'TOP'
            text.font = 'ruRU_Cyrvetica_Extra_14i.font'
            text.colour = (255, 255, 255, 255)
            text.text = ''
            text.position = (200, 8 + (i + 1) * 25, 0.5)
            self.component.addChild(text, '%s_VALUE' % self.bdata[i])

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'soBaseTrader')
        self.component.visible = True
        self.component.crossFocus = True
        self.component.moveFocus = True
        self.component.mouseButtonFocus = True
        return

    def hide(self):
        self.component.visible = False
        self.component.moveFocus = False
        self.component.crossFocus = False
        self.component.mouseButtonFocus = False

    def update(self):
        if BWPersonality.GUICore.baseTraderDataSection.has_key('clanName'):
            self.component.CLAN_NAME_VALUE.text = BWPersonality.GUICore.baseTraderDataSection['clanName']