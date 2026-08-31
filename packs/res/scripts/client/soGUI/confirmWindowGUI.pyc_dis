# Embedded file name: scripts/client/soGUI/confirmWindowGUI.py
import BigWorld
import BWPersonality
import GUI
import traceback
from Localization import lc
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soButton import soButton, soButtonWTT
import soGUI.soNumberBox
from soGUI.soEditField import soEditBox
import DataManagerConst

class confirmWindowGUI(PyGUIBase):
    factoryString = 'soGUI.confirmWindowGUI'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
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
        cmp.width = sW
        cmp.height = sH
        cmp.position = (0, 0, 0.1)

    def setupContent(self):
        sW, sH = BigWorld.screenSize()
        cmp = GUI.Simple('textures/default/black.jpg')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 150)
        cmp.materialFX = 'BLEND'
        cmp.width = sW
        cmp.height = sH
        cmp.position = (0, 0, 0.5)
        cmp.visible = True
        self.component.addChild(cmp, 'frameBG')
        framW = 600
        framH = 400
        framePosW = sW / 2 - framW / 2
        framePosH = sH / 2 - framH / 2
        FRAME_TEXTURE = 'soGUI/maps/Controls/inventory/inventoryFrame2.tga'
        self.frameCmp = GUI.Frame2(FRAME_TEXTURE)
        self.frameCmp.horizontalPositionMode = self.frameCmp.verticalPositionMode = 'PIXEL'
        self.frameCmp.widthMode = self.frameCmp.heightMode = 'PIXEL'
        self.frameCmp.horizontalAnchor = 'LEFT'
        self.frameCmp.verticalAnchor = 'TOP'
        self.frameCmp.visible = True
        self.frameCmp.colour = (220, 220, 220, 255)
        self.frameCmp.materialFX = 'BLEND'
        self.frameCmp.width = framW
        self.frameCmp.height = framH
        self.frameCmp.position = (framePosW, framePosH, 0.2)
        self.frameCmp.visible = True
        self.component.addChild(self.frameCmp, 'frameWindow')
        cmp = GUI.Text('Stalker Online GUARD')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.multiline = True
        cmp.position = (sW / 2, framePosH + 6, 0.1)
        cmp.multiline = True
        self.component.addChild(cmp, 'caption')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'system_small.font'
        cmp.text = lc('confirmWindowGUI.message.BYEMAIL').format('xxx@xx.com')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.multiline = True
        cmp.position = (sW / 2, framePosH + 30, 0.1)
        cmp.multiline = True
        self.component.addChild(cmp, 'label')
        edit = soEditBox(GUI.Window(), width=150, height=30, font='ruRU_Cyrvetica_Extra_14i.font', hOffset=3, vOffset=2)
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.position = (sW / 2 - 70, framePosH + 105, 0.1)
        self.component.addChild(cmp, 'NumberBox')
        edit.onBound()
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('confirmWindowGUI.message.OK')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 100
        cmp.height = 30
        cmp.position = (sW / 2 + 85, framePosH + 105, 0.1)
        cmp.script.onClick = self.clickOk
        cmp.script.setDisabledState(False)
        self.component.addChild(cmp, 'button_ok')
        btn.onBound()
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'system_small.font'
        cmp.text = lc('confirmWindowGUI.message.COUNT').format(3)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.multiline = True
        cmp.position = (sW / 2, framePosH + 105 + 30, 0.1)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_COUNT')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'system_small.font'
        cmp.text = lc('confirmWindowGUI.message.RESEND')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.multiline = True
        cmp.position = (sW / 2, framePosH + 105 + 30 + 60, 0.1)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_resend')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('confirmWindowGUI.message.RESENDBUT')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 140
        cmp.height = 30
        cmp.position = (sW / 2, framePosH + 105 + 30 + 60 + 60, 0.1)
        cmp.script.onClick = self.clickresend
        cmp.script.setDisabledState(False)
        self.component.addChild(cmp, 'button_resend')
        btn.onBound()

    def clickOk(self):
        key = self.component.NumberBox.script.rawText
        if not key:
            self.component.NumberBox.script._soNumberBox__showErrorInput()
            return
        account = BigWorld.player()
        account.base.confirmAccount(key.encode('utf8'))
        self.component.button_ok.script.setDisabledState(True)
        BigWorld.callback(2, lambda : self.component.button_ok.script.setDisabledState(False))

    def clickresend(self):
        print 'RESENDBUT'
        account = BigWorld.player()
        account.base.reSendValidateKey()
        self.component.button_resend.script.setDisabledState(True)
        BigWorld.callback(2, lambda : self.component.button_resend.script.setDisabledState(False))

    def show(self, needConfirmIDCount, needConfirmIDUser, msg):
        BWPersonality.GUICore.generalLayer.delChild('confirmWimdowGUI')
        if self.component.parent is None:
            BWPersonality.GUICore.generalLayer.addChild(self.component, 'confirmWimdowGUI')
        self.component.visible = True
        self.component.crossFocus = True
        self.component.moveFocus = True
        self.component.label_COUNT.text = lc('confirmWindowGUI.message.COUNT').format(needConfirmIDCount)
        if needConfirmIDUser == DataManagerConst.VALIDATE_TYPE_NEED_CODE_EMAIL:
            lsstr = 'confirmWindowGUI.message.BYEMAIL'
        else:
            lsstr = 'confirmWindowGUI.message.BYSMS'
        self.component.label.text = lc(lsstr).format(msg)
        self.component.NumberBox.script.clear()
        return

    def hide(self):
        self.component.visible = False
        self.component.moveFocus = False
        self.component.crossFocus = False

    def handleMouseLeaveEvent(self, cmp):
        return True

    def handleMouseEnterEvent(self, cmp):
        return True

    def handleMouseEvent(self, cmp, event):
        return False

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.width = sW
        self.component.height = sH
        self.component.frameBG.width = sW
        self.component.frameBG.height = sH

    def updateInfo(self):
        pass