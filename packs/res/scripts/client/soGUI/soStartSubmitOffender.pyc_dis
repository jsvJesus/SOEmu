# Embedded file name: scripts/client/soGUI/soStartSubmitOffender.py
import BigWorld
import GUI
import BWPersonality
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.PyGUI import PyGUIEvent
from Localization import lc
from soGUI.soButton import soButton, soButtonWTT
from Items import ItemsCatalog
import ItemsUtils
import gui_jokes
import colorCodes
from utils import groupNumber
import soGUI.soNumberBox

class soStartSubmitOffender(PyGUIBase):
    factoryString = 'soGUI.soStartSale'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 410.0
        cmp.height = 256.0
        cmp.position = (cmp.width - 20, cmp.height, 0.0)

    def setupContent(self):
        sW = self.component.width
        sH = self.component.height
        FRAME_TEXTURE = 'soGUI/maps/Controls/inventory/inventoryFrame2.tga'
        self.frameCmp = GUI.Frame2(FRAME_TEXTURE)
        self.frameCmp.horizontalPositionMode = self.frameCmp.verticalPositionMode = 'PIXEL'
        self.frameCmp.widthMode = self.frameCmp.heightMode = 'PIXEL'
        self.frameCmp.horizontalAnchor = 'LEFT'
        self.frameCmp.verticalAnchor = 'TOP'
        self.frameCmp.visible = True
        self.frameCmp.colour = (255, 255, 255, 255)
        self.frameCmp.materialFX = 'BLEND'
        self.frameCmp.width = sW
        self.frameCmp.height = sH
        self.frameCmp.position = (0, 0, 0.9)
        self.component.addChild(self.frameCmp, 'frame1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('tmplocal.strings.str43')
        cmp.multiline = True
        cmp.position = (sW / 2, 5, 0.5)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_capt')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('tmplocal.strings.str44')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 120
        cmp.height = 30
        cmp.position = (sW / 4, sH - 5, 0.5)
        cmp.script.onClick = self.apply
        self.component.addChild(cmp, 'button_ok')
        btn.onBound()
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('tmplocal.strings.str45')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 100
        cmp.height = 30
        cmp.position = (sW * 3 / 4.0, sH - 5, 0.5)
        cmp.script.onClick = self.hide
        self.component.addChild(cmp, 'button_cancel')
        btn.onBound()
        toup = -40
        tor = 30
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'default_small.font'
        cmp.colour = (125, 126, 102, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('tmplocal.strings.str46')
        cmp.position = (8, toup + 170, 0.5)
        cmp.multiline = 0
        self.component.addChild(cmp, 'label_m')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'default_small.font'
        cmp.colour = (125, 126, 102, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('tmplocal.strings.str47')
        cmp.position = (8, toup + 210, 0.5)
        cmp.multiline = 0
        self.component.addChild(cmp, 'label_1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'default_small.font'
        cmp.colour = (125, 126, 102, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('tmplocal.strings.str48')
        cmp.position = (8, toup + 250, 0.5)
        cmp.multiline = 0
        self.component.addChild(cmp, 'label_3')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (125, 126, 102, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('tmplocal.strings.str49')
        cmp.position = (tor + 220, toup + 190, 0.5)
        self.component.addChild(cmp, 'label_2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (255, 200, 120, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = u'10'
        cmp.multiline = False
        cmp.position = (tor + 220, toup + 214, 0.5)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_tax')
        cmp = GUI.Text(lc('tmplocal.strings.str50'))
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (125, 126, 102, 255)
        cmp.materialFX = 'BLEND'
        cmp.multiline = False
        cmp.position = (8, 55, 0.5)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_killerName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_16i.font'
        cmp.colour = (250, 250, 170, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = u'killerName'
        cmp.multiline = False
        cmp.position = (tor + 70, 60, 0.5)
        cmp.multiline = True
        self.component.addChild(cmp, 'killerName')
        edit = soGUI.soNumberBox.soNumberBox(GUI.Window(), width=sW / 3, height=29, font='ruRU_Cyrvetica_Extra_14i.font', hOffset=5, vOffset=5)
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.position = (tor + 70, toup + 214, 0.5)
        cmp.script.onValueChange = self._onValueChange
        cmp.script.onDefaultAction = self.apply
        self.component.addChild(cmp, 'NumberBox')
        edit.onBound()
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_16i.font'
        cmp.colour = (255, 200, 120, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('tmplocal.strings.str51')
        cmp.multiline = False
        cmp.position = (tor + 70, toup + 250, 0.5)
        cmp.multiline = True
        self.component.addChild(cmp, 'allcost')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_16i.font'
        cmp.colour = (255, 200, 120, 150)
        cmp.materialFX = 'BLEND'
        cmp.text = groupNumber(str(BigWorld.player().CreditNumber), ' ') + u'\u0440.'
        cmp.multiline = False
        cmp.position = (tor + 70, toup + 170, 0.5)
        cmp.multiline = True
        self.component.addChild(cmp, 'mymoney')
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
        cmp.position = (sW - 6, 6, 0.3)
        closeBox.onClick = self.hide
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')

    def apply(self):
        price = self.component.NumberBox.script.rawText
        try:
            price = int(price)
        except:
            price = 0

        if price < 1000:
            ask = lc('tmplocal.strings.str52')
            gui_jokes.askUserOk(u'', colorCodes.tf3_regular_text_color + ask)
            self.component.NumberBox.script.activate(0)
            return
        CreditNumber = BigWorld.player().CreditNumber
        price_tax = int(price * 0.05)
        if CreditNumber < price_tax + price:
            ask = lc('tmplocal.strings.str53') % (CreditNumber, price_tax + price)
            gui_jokes.askUserOk(u'', colorCodes.tf3_regular_text_color + ask)
            return
        BigWorld.player().submitOffender(price)
        self.hide()

    def _onValueChange(self, byuser):
        price = self.component.NumberBox.script.rawText
        try:
            price = int(price)
        except:
            price = 0

        tax = int(price * 0.05)
        if tax < 10:
            tax = 10
        CreditNumber = BigWorld.player().CreditNumber
        self.component.mymoney.text = groupNumber(str(CreditNumber), ' ') + u'\u0440.'
        self.component.label_tax.text = groupNumber(str(tax), ' ') + u'\u0440.'
        self.component.allcost.text = groupNumber(str(tax + price), ' ') + u'\u0440.'
        if CreditNumber < tax + price:
            self.component.allcost.colour = (255, 100, 100, 255)
        else:
            self.component.allcost.colour = (255, 200, 120, 255)

    def show(self, killerName = u'AFAFAF'):
        print 'show:', [killerName], type(killerName)
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'startSumbitOffHanter')
        self.component.visible = True
        self.component.crossFocus = True
        self.component.moveFocus = True
        self.component.killerName.text = killerName
        self.killerName = killerName
        self.component.NumberBox.script.clear()
        self.component.NumberBox.script.activate()
        return

    def hide(self):
        self.component.visible = False
        self.component.moveFocus = False
        self.component.crossFocus = False
        self.component.NumberBox.script.activate(0)

    def doReposition(self):
        sW, sH = BigWorld.screenSize()