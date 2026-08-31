# Embedded file name: scripts/client/soGUI/soNews.py
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
ofset = 40

class soNews(PyGUIBase):
    factoryString = 'soGUI.soNews'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.isVisible = False
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        sW, sH = BigWorld.screenSize()
        cmp.width = sW - ofset * 2
        cmp.height = sH - ofset * 2
        cmp.position = (ofset, ofset, 0.2)
        cmp.visible = False

    def setupContent(self):
        sW, sH = self.component.width, self.component.height
        w = sW - 20
        h = sH - 70
        posw = 0
        cmpt = GUI.Frame2('soGUI/maps/charCreation/fon_tisnenie.tga')
        cmpt.widthMode = cmpt.heightMode = 'PIXEL'
        cmpt.horizontalPositionMode = cmpt.verticalPositionMode = 'CLIP'
        cmpt.horizontalAnchor = cmpt.verticalAnchor = 'CENTER'
        cmpt.width = sW
        cmpt.height = sH
        cmpt.position = (0.0, 0.0, 0.5)
        cmpt.visible = True
        cmpt.colour = (255, 255, 255, 240)
        cmpt.materialFX = 'BLEND'
        self.component.addChild(cmpt, 'frame1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Verdana_21.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('soBulletinBoard.news')
        cmp.multiline = True
        cmp.position = (sW / 2, 10, 0.5)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_name')
        txt = soTextField3(GUI.Window(), width=w - 2, height=h - 20, textWidth=-1, hScroll=False, vScroll=True, hideScroll=1, borderWidth=6, vOffset=30, hOffset=50, textureless=0, autosize=0)
        txt.DEFAULT_FONT = 'ruRU_calibri_large.font'
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (posw, 51, 0)
        cmp.visible = 1
        txt.onBound()
        self.component.addChild(cmp, 'textNews')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.width = 200
        cmp.height = 40
        cmp.textureName = ''
        cmp.position = (sW / 2, sH - 30, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.label.text = lc('soBulletinBoard.next')
        self.component.addChild(cmp, 'acceptBtn')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnOption.xml')
        btn.onClick = self.hide
        btn.onBound()
        btn._updateVisualState()
        cmp.label.position = (0, 0.1, 0.1)

    def show(self, text):
        self.textData = text
        self.isVisible = True
        if self.component.parent is None:
            BWPersonality.GUICore.generalLayer.addChild(self.component, 'soNews')
        self.component.visible = True
        self.component.textNews.script.setText(text)
        self.component.crossFocus = True
        self.component.moveFocus = True
        self.component.mouseButtonFocus = True
        return

    def hide(self):
        self.isVisible = False
        self.component.visible = False
        self.component.moveFocus = False
        self.component.crossFocus = False
        self.component.mouseButtonFocus = False

    def doReposition(self):
        BWPersonality.GUICore.generalLayer.delChild('soNews')
        self.setupRoot()
        self.setupContent()
        if self.isVisible:
            self.show(self.textData)
        else:
            self.hide()

    def handleMouseLeaveEvent(self, cmp):
        return True

    def handleMouseEnterEvent(self, cmp):
        return True

    def handleMouseEvent(self, cmp, event):
        dz = event.dz
        position = event.cursorPosition
        if dz > 0:
            self.component.textNews.script.scrolledUP()
            return True
        if dz < 0:
            self.component.textNews.script.scrolledDOWN()
            return True
        return False

    def scrollCurentTab(self, up):
        cmp = getattr(self.component, self.curentTab, None)
        if not cmp:
            return
        else:
            if up:
                cmp.script.scrolledUP()
            else:
                cmp.script.scrolledDOWN()
            return