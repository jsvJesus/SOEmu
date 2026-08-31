# Embedded file name: scripts/client/soGUI/soProofOfPurchaseInShop.py
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
import traceback
import colorCodes
from utils import groupNumber
from soDraggableComponent import soDraggableComponent
from copy import copy
import CharacterUtils
from Perks import PerkList
from CharacterUtils import CharacterConst
import msgbox_templates
import math
import soGUI.soSlotExpand
import random
from NPCs import NPCs
_NPCs = NPCs()

class soProofOfPurchaseInShop(PyGUIBase):
    factoryString = 'soGUI.soProofOfPurchaseInShop'
    SLOTWIDTH = 64
    SLOTHEIGHT = 64

    def __init__(self, component, callbackEnter, windowID, updatePageCallback):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupContent()
        self.isMyDragging = False
        self.callbackEnter = callbackEnter
        self.windowID = windowID
        self.updatePageCallback = updatePageCallback

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
        cmp.position = (cmp.width - 20 + random.randint(-10, 10), cmp.height + random.randint(-10, 10), 0.09)

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
        self.frameCmp.colour = (220, 220, 220, 255)
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
        cmp.text = lc('tmplocal.strings.str8')
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
        cmp.label.text = lc('tmplocal.strings.str9')
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
        cmp.label.text = lc('tmplocal.strings.str10')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 100
        cmp.height = 30
        cmp.position = (sW * 3 / 4.0, sH - 5, 0.5)
        cmp.script.onClick = self.closeWindow
        self.component.addChild(cmp, 'button_cancel')
        btn.onBound()
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (255, 200, 120, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = u'10'
        cmp.position = (sW - 50, sH * 3 / 5 + 5, 0.5)
        cmp.multiline = 0
        self.component.addChild(cmp, 'label_price')
        cmp = GUI.Text(lc('tmplocal.strings.str11'))
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (255, 200, 120, 128)
        cmp.materialFX = 'BLEND'
        cmp.position = (20, sH * 3 / 5 + 45, 0.5)
        cmp.multiline = 1
        self.component.addChild(cmp, 'label_WARNING')
        cmp = GUI.Text(u'username')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 255, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (sW - 10, 80, 0.5)
        cmp.multiline = 1
        self.component.addChild(cmp, 'label_sellerName')
        cmp = GUI.Text(u'bankname')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (sW - 10, 100, 0.5)
        cmp.multiline = 1
        self.component.addChild(cmp, 'label_bankname')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (240, 186, 122, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('tmplocal.strings.str12')
        cmp.multiline = True
        cmp.position = (sW - 10, sH * 2 / 5 + 15, 0.5)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_info')
        edit = soGUI.soSlotExpand.soSlotExpand(GUI.Window(), sW, sH, 5, 20)
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (0, 12, 0.9)
        cmp.width = sW
        cmp.height = sH
        self.component.addChild(cmp, 'slotExpand')
        edit.onBound()
        infoButton = soButton(GUI.Window())
        cmp = infoButton.component
        infoButton.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = u'?'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 20
        cmp.height = 20
        cmp.position = (5, 100, 0.5)
        cmp.script.onClick = self.showInfo
        self.component.addChild(cmp, 'button_infoButton')
        infoButton.onBound()
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
        closeBox.onClick = self.closeWindow
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        hideBox = soButton(GUI.Window())
        cmp = hideBox.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (sW - 27, 6, 0.3)
        hideBox.onClick = self.hideWindow
        hideBox.initVSC('soGUI/visual_styles/toTray.xml')
        hideBox.onBound()
        hideBox.setVisualState('normal')
        self.component.addChild(cmp, 'hide_Box')

    def apply(self):
        global nnn
        CreditNumber = BigWorld.player().CreditNumber
        price_tax = int(self.price / 10.0)
        if CreditNumber < price_tax:
            ask = lc('tmplocal.strings.str13') % (CreditNumber, price_tax)
            gui_jokes.askUserOk(u'', colorCodes.tf3_regular_text_color + ask)
            return
        if self.username.startswith('virtual_'):
            nnn = 0

            def foo(event):
                global nnn
                nnn += 1
                if event == gui_jokes.askUserYesNo.YES:
                    asks = lc('tmplocal.strings.str14') * nnn
                    ask = lc('tmplocal.strings.str15') % asks
                    gui_jokes.askUserYesNo(u'', colorCodes.tf3_regular_text_color + ask, foo)
                else:
                    nnn = 0

            ask = lc('tmplocal.strings.str16')
            gui_jokes.askUserYesNo(u'', colorCodes.tf3_regular_text_color + ask, foo)
            self.closeWindow()
            return
        complexItemID = self.item['complexItemID']
        sellerAvatarName = self.username.encode('utf8')
        BigWorld.player().buyItemFromShop(sellerAvatarName, complexItemID, self.price, self.BankName)
        self.closeWindow()
        self.updatePageCallback()

    def applyitem(self, itemData):
        self.component.slotExpand.script.applyitem(itemData)
        self.component.label_price.text = lc('tmplocal.strings.str17') + groupNumber(str(self.price), ' ') + lc('tmplocal.strings.str18')

    def showInfo(self):
        player = BigWorld.player()
        info_text = player.GetItemInfoText(self.item['complexItemType'], self.item)
        info_text = getInfo(self.item, False) + '\n\n' + info_text
        msgbox_templates.text_and_ok('Inventory.ItemInfo', lc('Inventory.client.INFO'), colorCodes.tf3_regular_text_color + info_text)

    def show(self, item = None, BankName = '', username = '', price = 0):
        self.component.visible = True
        self.component.crossFocus = True
        self.component.moveFocus = True
        self.component.mouseButtonFocus = True
        if item:
            self.item = item
            self.username = username
            self.BankName = BankName
            self.price = price
            self.applyitem(item)
            self.component.label_sellerName.text = username
            self.component.label_name.text = username
            bank = _NPCs.names_by_npcName.get(BankName, '???')
            self.component.label_bankname.text = bank
            string = getInfo(item).strip()
            if string:
                string = string.split('\n')
                string.sort(key=lambda a: len(a))
                string = '\n'.join(string)
            self.component.label_info.text = string
        self.w_onShow(self.windowID)

    def hide(self):
        self.component.visible = False
        self.component.moveFocus = False
        self.component.crossFocus = False
        self.component.focus = False

    def closeWindow(self):
        self.hide()
        self.w_onClose(self.windowID)

    def hideWindow(self):
        self.hide()
        self.w_onHide(self.windowID)

    def doReposition(self):
        sW, sH = BigWorld.screenSize()

    def w_onHide(self, wID):
        pass

    def w_onShow(self, wID):
        pass

    def w_onClose(self, wID):
        pass

    def handleMouseEnterEvent(self, comp):
        self.callbackEnter(True, self.windowID)
        self.component.frame1.colour = (255, 255, 255, 255)
        return True

    def handleMouseLeaveEvent(self, comp):
        self.callbackEnter(False, self.windowID)
        self.component.frame1.colour = (220, 220, 220, 255)
        return True


def getInfo(item, short = True):
    player = BigWorld.player()
    item_type = item['complexItemType']
    item_param = ItemsCatalog.GetItemParam(item_type)
    item_class = ItemsCatalog.GetItemClass(item_type)
    item_inconstant_param = ItemsUtils.GetComplexItemInconstanParams(item)
    string = u''
    if item_class == ItemsCatalog.WEAPON:
        string += u'\n' + lc('Inventory.client.STATE').format(ItemsUtils.GetItemConditionPercentString(None, None, short, item_param, item_inconstant_param))
        if item_inconstant_param[ItemsCatalog.INC_IS_BROKEN] > 0:
            string += u'\n' + lc('Inventory.client.WEAPON_JAMMED')
    elif item_class == ItemsCatalog.CLOTH:
        string += u'\n' + lc('Inventory.client.STATE').format(ItemsUtils.GetItemConditionPercentString(None, None, short, item_param, item_inconstant_param))
        if item_inconstant_param[ItemsCatalog.INC_CONDITION_VALUE] == 0:
            string += u'\n' + lc('Inventory.client.ITEM_BROKEN')
    elif item_class == ItemsCatalog.ARTIFACT:
        power_time = ItemsUtils.GetArtefactDepleetionTime(item, item_param, player.timeServerDiff)
        if power_time == None:
            string += u'\n' + lc('Inventory.client.ARTIFACT_CHARGE_FULL')
        elif power_time < 0.0:
            string += u'\n' + lc('Inventory.client.ARTIFACT_CHARGE_DEPLEETED')
        else:
            string += u'\n' + lc('Inventory.client.ARTIFACT_CHARGE_REMAINING') % timeToString(power_time)
    if ItemsUtils.IsQuestItem(item, item_inconstant_param):
        quest_name = player.getQTitle(item_inconstant_param[ItemsCatalog.IS_QUEST_ITEM])
        if quest_name:
            string += u'\n' + lc('Inventory.client.BELONGS_TO_QUEST') % quest_name
        else:
            string += u'\n' + lc('Inventory.client.QUEST_ITEM')
    item_ttl = ItemsUtils.GetItemDestroyTime(item, item_param)
    if item_ttl is not None:
        string += u'\n' + lc('Inventory.client.ITEM_TIME_TO_LIVE').format(timeToString(item_ttl))
    return string


def timeToString(secs):
    if secs < 0:
        return u''
    hours = math.floor(secs / 3600.0)
    minutes = math.floor((secs - hours * 3600.0) / 60.0)
    seconds = secs - (hours * 3600.0 + minutes * 60.0)
    outH = str(int(hours)) if hours > 9 else u'0' + str(int(hours))
    outM = str(int(minutes)) if minutes > 9 else u'0' + str(int(minutes))
    outS = str(int(seconds)) if seconds > 9 else u'0' + str(int(seconds))
    hours = int(hours)
    if hours > 0:
        day = hours / 24
        hour = hours % 24
        if day:
            return u'%s' % day + lc('Inventory.client.DAY') + u' %02d' % hour + lc('Inventory.client.HOURS')
        return u'' + outH + lc('Inventory.client.HOURS')
    if minutes > 0:
        return u'' + outM + lc('Inventory.client.MINUTES')
    if seconds >= 0:
        return u'' + outS + lc('Inventory.client.SECONDS')
    return u''