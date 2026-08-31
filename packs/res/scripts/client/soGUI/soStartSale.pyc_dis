# Embedded file name: scripts/client/soGUI/soStartSale.py
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
import random
import soGUI.soNumberBox
import soGUI.soSlotExpand

class soStartSale(PyGUIBase):
    factoryString = 'soGUI.soStartSale'
    SLOTWIDTH = 64
    SLOTHEIGHT = 64

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
        cmp.text = lc('tmplocal.strings.str35')
        cmp.multiline = True
        cmp.position = (sW / 2, 5, 0.5)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_name')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('tmplocal.strings.str36')
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
        cmp.label.text = lc('tmplocal.strings.str37')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 100
        cmp.height = 30
        cmp.position = (sW * 3 / 4.0, sH - 5, 0.5)
        cmp.script.onClick = lambda : BWPersonality.GUICore.showStartSale(0)
        self.component.addChild(cmp, 'button_cancel')
        btn.onBound()
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'default_small.font'
        cmp.colour = (125, 126, 102, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('tmplocal.strings.str38')
        cmp.position = (8, 210, 0.5)
        cmp.multiline = 0
        self.component.addChild(cmp, 'label_1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (125, 126, 102, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('tmplocal.strings.str39')
        cmp.position = (220, 194, 0.5)
        self.component.addChild(cmp, 'label_percent')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (255, 200, 120, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = u'10'
        cmp.multiline = False
        cmp.position = (220, 214, 0.5)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_tax')
        cmp = GUI.Simple('textures/default/black.jpg')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 240)
        cmp.materialFX = 'BLEND'
        cmp.width = sW / 3
        cmp.height = 29
        cmp.position = (sW * 2 / 3 - 5, 109, 0.6)
        self.component.addChild(cmp, 'frame_tax')
        slot = soGUI.soSlotExpand.soSlotExpand(GUI.Window(), sW, sH + 500, 5, 20)
        cmp = slot.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (0, 12, 0.5)
        self.component.addChild(cmp, 'slotExpand')
        slot.onBound()
        edit = soGUI.soNumberBox.soNumberBox(GUI.Window(), width=sW / 3, height=29, font='ruRU_Cyrvetica_Extra_14i.font', hOffset=5, vOffset=5)
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.position = (70, 214, 0.5)
        cmp.script.onValueChange = self._onValueChange
        cmp.script.onDefaultAction = self.apply
        self.component.addChild(cmp, 'NumberBox')
        edit.onBound()
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

    def calcTax(self, price):
        if price < 500:
            percent = 10
        elif 500 <= price < 1000:
            percent = 7
        elif 1000 <= price < 5000:
            percent = 5
        elif 5000 <= price < 10000:
            percent = 3
        else:
            percent = 2
        tax = int(price * (percent / 100.0))
        return (percent, tax)

    def apply(self):
        price = self.component.NumberBox.script.rawText
        try:
            price = int(price)
        except:
            price = 0

        if price < 10:
            ask = lc('tmplocal.strings.str40')
            gui_jokes.askUserOk(u'', colorCodes.tf3_regular_text_color + ask)
            self.component.NumberBox.script.activate(0)
            return
        CreditNumber = BigWorld.player().CreditNumber
        percent, price_tax = self.calcTax(price)
        if CreditNumber < price_tax:
            ask = lc('tmplocal.strings.str41') % (CreditNumber, price_tax)
            gui_jokes.askUserOk(u'', colorCodes.tf3_regular_text_color + ask)
            return
        BigWorld.player().itemToShop(self.item, price, self.BankName)
        BWPersonality.GUICore.showStartSale(0)

    def applyitem(self, itemData):
        self.component.slotExpand.script.applyitem(itemData)
        self.component.NumberBox.script.activate()

    def _onValueChange(self, byuser):
        price = self.component.NumberBox.script.rawText
        try:
            price = int(price)
        except:
            price = 0

        tax = int(price / 10.0)
        percent, tax = self.calcTax(price)
        if tax < 10:
            tax = 10
        self.component.label_tax.text = groupNumber(str(tax), ' ') + u'\u0440.'
        self.component.label_percent.text = lc('tmplocal.strings.str42') % percent

    def show(self, item = None, BankName = ''):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'startSale')
        self.component.visible = True
        self.component.crossFocus = True
        self.component.moveFocus = True
        self.component.NumberBox.script.clear()
        self.item = item
        self.BankName = BankName
        self.applyitem(item)
        return

    def hide(self):
        self.component.visible = False
        self.component.moveFocus = False
        self.component.crossFocus = False
        self.component.NumberBox.script.activate(0)

    def doReposition(self):
        sW, sH = BigWorld.screenSize()