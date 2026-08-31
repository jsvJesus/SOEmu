# Embedded file name: scripts/client/soGUI/soShopTabl.py
import traceback
import BigWorld
import BWPersonality
import GUI
from soGUI.soTextField import soTextField3
from Localization import lc
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soButton import soButton, soButtonWTT
from soGUI.soTextField import soTextField3
from Helpers.PyGUI import PyGUIEvent
import soGUI.soSlotExpand
import soGUI.soNumberBox
from soGUI.soCheckBox import soCheckBox
from Items import ItemsCatalog
from ItemsUtils import filterItemConst
from soGUI.soRadioButton import soRadioButton2, soRadioButton, RadioButtonPropsStructure
from utils import groupNumber
import ItemsUtils
import random
import soGUI.soProofOfPurchaseInShop
filtersKeys = [('WEAPON', False, False),
 ('PISTOL', True, True),
 ('SUB_MACHINE_GUN', True, True),
 ('ASSAULT_RIFLE', True, True),
 ('SNIPER_RIFLE', True, True),
 ('RIFLE', True, True),
 ('SHOTGUN', True, True),
 ('MACHINE_GUN', True, True),
 ('ROCKET_LAUNCHER', True, True),
 (None, True, False),
 ('CLOTH', False, False),
 ('HEAD', True, True),
 ('SHIRT', True, True),
 ('HANDS', True, True),
 ('PANTS', True, True),
 ('BOOTS', True, True),
 ('ARMOR', True, True),
 ('HAT', True, True),
 ('MASK', True, True),
 ('BACKPACK', True, True),
 (None, True, False),
 ('AMMO', True, False),
 ('EXPLOSION', True, False),
 ('ARTIFACT', True, False),
 ('GADGET', True, False),
 ('BUFF', True, False),
 ('PART', True, False),
 ('LOOT', True, False)]
from NPCs import NPCs
_NPCs = NPCs()
import soGUI.soWindowBar

class RowItem(PyGUIBase):
    SLOTWIDTH = 59
    SLOTHEIGHT = 59
    SUBSLOTWIDTH = 32
    SUBSLOTHEIGHT = 32
    MAXSUBICONS = 5

    def __init__(self, component, width, height, position, buyHandler):
        component.script = self
        PyGUIBase.__init__(self, component)
        self.width = width
        self.height = height
        self._dw = 2
        self._dh = 2
        self.buyHandler = buyHandler
        self.position = position
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
        cmp.width = self.width
        cmp.height = self.height
        cmp.position = self.position
        cmp = GUI.Simple('textures/default/bright_gray.jpg')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 100)
        cmp.materialFX = 'BLEND'
        cmp.width = self.component.width
        cmp.height = 1
        cmp.position = (0, self.height, 0.9)
        cmp.visible = 1
        self.component.addChild(cmp, 'frame1')

    def setupContent(self):
        cmp = GUI.Text('itemprice')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'default_small.font'
        cmp.colour = (200, 200, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.width / 4, 35 + self._dh, 0.3)
        self.component.addChild(cmp, 'itemprice')
        addbox_x = 40
        cmp = GUI.Text(lc('tmplocal.strings.str19'))
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 255, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (addbox_x + self.width * 8 / 15.0, 5 + self._dh, 0.3)
        self.component.addChild(cmp, 'username')
        cmp = GUI.Text(lc('tmplocal.strings.str20'))
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (100, 100, 100, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (addbox_x + self.width * 8 / 15.0 - 5, 5 + self._dh, 0.3)
        self.component.addChild(cmp, 'username_label')
        cmp = GUI.Text('bank')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (addbox_x + self.width * 8 / 15.0, 30 + self._dh, 0.3)
        self.component.addChild(cmp, 'bank')
        cmp = GUI.Text(lc('tmplocal.strings.str21'))
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (100, 100, 100, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (addbox_x + self.width * 8 / 15.0 - 5, 30 + self._dh, 0.3)
        self.component.addChild(cmp, 'bank_label')
        cmp = GUI.Text('12:50')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.width * 4 / 4.0, 5 + self._dh, 0.3)
        self.component.addChild(cmp, 'itemtime')
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/cellFrame2.tga')
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0 + self._dw, 0 + self._dh, 0.9)
        self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0 + self._dw, 0 + self._dh, 0.4)
        self.component.addChild(cmp, 'itemIcon')
        cmp = GUI.Simple('soGUI/maps/Controls/inventory/broken.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.7)
        cmp.visible = False
        self.component.addChild(cmp, 'itemBroken')
        cmp = GUI.Simple('soGUI/maps/Icons/icon_item_painted.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH / 5
        cmp.height = self.SLOTHEIGHT / 5
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH, cmp.height / 2, 0.7)
        cmp.visible = 0
        self.component.addChild(cmp, 'itemColored')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (5 + self._dw, self.SLOTHEIGHT - 5 + self._dh, 0.3)
        self.component.addChild(cmp, 'itemName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH - 5 + self._dw, 5 + self._dh, 0.3)
        self.component.addChild(cmp, 'itemCount')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'default_small.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH + 5 + self._dw, 5 + self._dh, 0.3)
        self.component.addChild(cmp, 'itemBigName')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('tmplocal.strings.str22')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 100
        cmp.height = 30
        cmp.position = (self.width, 20 + self._dh, 0.5)
        cmp.script.onClick = self._buy
        self.component.addChild(cmp, 'button_buy')
        btn.onBound()
        for subicon in range(self.MAXSUBICONS):
            subpos = (3 + self.SLOTWIDTH + (self.SUBSLOTWIDTH + 1) * subicon + self._dw, self._dh + self.SLOTWIDTH, 0.9)
            cmp = GUI.Frame2('soGUI/maps/Controls/inventory/cellFrame2.tga')
            cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.width = self.SUBSLOTWIDTH
            cmp.height = self.SUBSLOTHEIGHT
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = subpos
            self.component.addChild(cmp, 'subframeCmp_%s' % subicon)
            cmp = GUI.Simple('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.width = self.SUBSLOTWIDTH
            cmp.height = self.SUBSLOTHEIGHT
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = subpos
            self.component.addChild(cmp, 'subitemIcon_%s' % subicon)

    def _buy(self):
        self.buyHandler(item=self.itemData, BankName=self.bank, username=self.username, price=self.price)

    def setItem(self, itemData, price = 0, bank = '', username = '', timelost = 0):
        self.itemData = itemData
        self.price = price
        self.bank = bank
        self.username = username
        for subicon in range(self.MAXSUBICONS):
            subframeCmp = getattr(self.component, 'subframeCmp_%s' % subicon)
            subitemIcon = getattr(self.component, 'subitemIcon_%s' % subicon)
            subframeCmp.visible = False
            subitemIcon.visible = False

        if not itemData:
            self.component.itemName.text = ''
            self.component.itemCount.text = ''
            self.component.itemBigName.text = ''
            self.component.itemprice.text = ''
            self.component.username.text = ''
            self.component.bank.text = ''
            self.component.itemtime.text = ''
            self.component.itemBroken.visible = False
            self.component.itemColored.visible = False
            self.component.username_label.visible = False
            self.component.bank_label.visible = False
            self.component.itemIcon.visible = False
            self.component.button_buy.visible = False
            return
        else:
            self.component.itemIcon.visible = True
            self.component.button_buy.visible = True
            self.component.username_label.visible = True
            self.component.bank_label.visible = True
            self.component.itemprice.text = lc('tmplocal.strings.str23') + groupNumber(price, ' ') + u'\u0440.'
            self.component.username.text = username
            bankName = _NPCs.names_by_npcName.get(bank, '???')
            self.component.bank.text = bankName
            self.component.itemtime.text = lc('tmplocal.strings.str24') + str(timelost) + lc('tmplocal.strings.str25')
            item_type = itemData['complexItemType']
            item_id = itemData['complexItemID']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            item_level = item_params['Level']
            iconName = ItemsUtils.getTextureByTint(self.itemData)
            if not iconName:
                iconName = ItemsCatalog.GetItemParam(item_type)['IconName']
            if BWPersonality.GUICore.iconTextures is not None:
                if iconName not in BWPersonality.GUICore.iconTextures.failedIDs:
                    if BWPersonality.GUICore.iconTextures.has_key(iconName):
                        self.component.itemIcon.texture = BWPersonality.GUICore.iconTextures[iconName]
                    else:
                        self.component.itemIcon.textureName = iconName
            else:
                self.component.itemIcon.textureName = iconName
            countStr = ItemsUtils.GetDisplayValue(itemData)
            countInt = int(countStr) if countStr.isdigit() else 0
            friendlyName = ItemsUtils.GetItemName(item_type, fGetShortName=True, tintItem=self.itemData)
            bigName = ItemsUtils.GetItemName(item_type, fGetShortName=False, tintItem=self.itemData)
            price = int(item_params.get('price', 0))
            self.component.itemName.text = ''
            self.component.itemCount.text = countStr
            self.component.itemBigName.text = bigName
            item_state = ItemsUtils.GetItemConditionPercent(BigWorld.player(), itemData)
            if item_state <= 0.5:
                self.component.itemBroken.visible = True
            else:
                self.component.itemBroken.visible = False
            self.component.itemColored.visible = bool(ItemsUtils.getTintID(self.itemData))
            inconstantParam = ItemsUtils.GetComplexItemInconstanParams(itemData)
            if inconstantParam.get(ItemsCatalog.INC_ARTEFACT_DEAD, 0):
                self.component.itemBroken.visible = True
            itemList = itemData['itemList']
            for subiconI, subitem in enumerate(itemList):
                sub_item_type = subitem['itemType']
                sub_itemParam = ItemsCatalog.GetItemParam(sub_item_type)
                subprice = int(sub_itemParam.get('price', 0))
                subframeCmp = getattr(self.component, 'subframeCmp_%s' % subiconI)
                subitemIcon = getattr(self.component, 'subitemIcon_%s' % subiconI)
                subframeCmp.visible = True
                subitemIcon.visible = True
                iconName = sub_itemParam['IconName']
                if BWPersonality.GUICore.iconTextures is not None:
                    if iconName not in BWPersonality.GUICore.iconTextures.failedIDs:
                        if BWPersonality.GUICore.iconTextures.has_key(iconName):
                            subitemIcon.texture = BWPersonality.GUICore.iconTextures[iconName]
                        else:
                            subitemIcon.textureName = iconName
                else:
                    subitemIcon.textureName = iconName

            return


class soShopTabl(PyGUIBase):

    def __init__(self, component, w, h, posw, row):
        PyGUIBase.__init__(self, component)
        component.script = self
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = w
        cmp.height = h
        self.filterW = 200
        self.w = w
        self.h = h
        self.row = row
        self.posw = posw
        self._rows = []
        self.cbs = []
        self._waitserver = False
        self.page_start = 0
        self.last_index_item = 0
        self.old_page_start = 0
        self.old_last_index_item = 0
        self.all_index_item = 0
        self.activeWindowID = None
        self.activeWindowIDMoved = None
        self.setupContent()
        self.setupFiltersContent()
        self.setupRows()
        self.setupBar()
        return

    def setupContent(self):
        tmpw = 330
        navigatepos = 5
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = u'|<'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 30
        cmp.height = 22
        cmp.position = (tmpw + 12, self.h + navigatepos, 0.5)
        cmp.script.onClick = self.buttonFindClick
        self.component.addChild(cmp, 'button_home')
        btn.onBound()
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = u'<'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 30
        cmp.height = 22
        cmp.position = (tmpw + 60, self.h + navigatepos, 0.5)
        cmp.script.onClick = self.buttonLeftClick
        self.component.addChild(cmp, 'button_left')
        btn.onBound()
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = u'>'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 30
        cmp.height = 22
        cmp.position = (tmpw + 60 + 32, self.h + navigatepos, 0.5)
        cmp.script.onClick = self.buttonRightClick
        self.component.addChild(cmp, 'button_right')
        btn.onBound()
        edit = soGUI.soNumberBox.soNumberBox(GUI.Window(), width=50, height=22, font='ruRU_Cyrvetica_Extra_10i.font', hOffset=5, vOffset=5)
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.position = (tmpw + 110, self.h + navigatepos, 0.5)
        cmp.script.onDefaultAction = self.goto
        self.component.addChild(cmp, 'NumberBox')
        edit.onBound()
        cmp = GUI.Text('---')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (255, 200, 120, 200)
        cmp.materialFX = 'BLEND'
        cmp.multiline = True
        cmp.position = (tmpw + 165, self.h - 25 + navigatepos, 1)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_page')
        cmp = GUI.Text(lc('tmplocal.strings.str26'))
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (100, 100, 100, 255)
        cmp.materialFX = 'BLEND'
        cmp.multiline = True
        cmp.position = (tmpw + 165 + 90, self.h - 25 + navigatepos + 5, 1)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_info_beta')

    def setupFiltersContent(self):
        cmp = GUI.Simple('textures/default/bright_gray.jpg')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 128)
        cmp.materialFX = 'BLEND'
        cmp.width = 1
        cmp.height = self.h - 22
        cmp.position = (self.posw + self.w - self.filterW, 0, 0.2)
        cmp.visible = 1
        self.component.addChild(cmp, 'frame_f_right')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('tmplocal.strings.str27')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = self.filterW - 10
        cmp.height = 30
        cmp.position = (self.w, self.h - 35, 0.2)
        cmp.script.onClick = self.buttonFindClick
        self.component.addChild(cmp, 'button_f_update')
        btn.onBound()
        font = 'Label.font'
        for index, (name, selectable, colored) in enumerate(filtersKeys):
            if not name:
                continue
            cmp = GUI.Text(filterItemConst['LC_' + name])
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.font = font
            cmp.colour = (255, 200, 120, 255)
            cmp.position = (self.posw + self.w - self.filterW + 32, index * 18, 0.1)
            if not selectable:
                cmp.position = (self.posw + self.w - self.filterW + 32, index * 18, 0.1)
            if colored:
                cmp.colour = (10, 200, 120, 200)
                cmp.font = 'ruRU_calibri_small.font'
            cmp.materialFX = 'BLEND'
            cmp.multiline = 0
            self.component.addChild(cmp, 'label_f_%s' % index)
            if not selectable:
                continue
            cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=u'', font=font, labelColour=(175, 166, 112, 255)))
            cmp = cb.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (self.posw + self.w - self.filterW + 10, index * 18, 0.1)
            cmp.visible = 1
            cmp.script.setActive()
            self.component.addChild(cmp, 'CheckBox_%s' % index)
            cb.onBound()
            self.cbs.append((cb, filterItemConst[name]))

        sortBy = [(0, lc('tmplocal.strings.str28')),
         (1, lc('tmplocal.strings.str29')),
         (2, lc('tmplocal.strings.str30')),
         (3, lc('tmplocal.strings.str31'))]
        for sortindex, caption in sortBy:
            rb = soRadioButton2(GUI.Window(), btnW=18, btnH=18, radioGroup='radiogr_sortBy', labelText=caption, bvisual_styles='soGUI/visual_styles/radioButton.xml')
            rb.onBound()
            cmp = rb.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.position = (self.w - self.filterW + 5, self.h - 65 - sortindex * 20, 0.2)
            self.component.addChild(cmp, 'radio_%s' % sortindex)
            rb.setActive()

    def getIndexSortBy(self):
        for index in range(4):
            cmp = getattr(self.component, 'radio_%s' % index, None)
            if cmp and cmp.script.isChecked():
                return index

        print 'getIndexSortBy = no isChecked? wtf7'
        return 0

    def setupBar(self):
        self.bar_width = self.component.width - self.filterW
        self.bar_posY = 29
        self.wbar = soGUI.soWindowBar.soWindowBar(GUI.Window(), self.bar_width, 27, self)
        cmp = self.wbar.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.position = (1, self.bar_posY, 0.9)
        self.component.addChild(cmp, 'wbar')
        self.wbar.onBound()

    def getFiler(self):
        tags = []
        for cb, tag in self.cbs:
            if cb.isChecked():
                tags.append(tag)

        return tags

    def setupRows(self):
        rowh = int(self.h / (self.row + 1.0))
        drowh = int(rowh + 2)
        roww = int(self.w - self.filterW - self.posw) - 1
        for index in range(self.row):
            position = (int(self.posw), 28 + int(drowh * index), 0.5)
            cb = RowItem(GUI.Window(), roww, rowh, position, self.buyDialog)
            cmp = cb.component
            cb.setItem(None)
            self.component.addChild(cmp, 'sub_row_%s' % index)
            cb.onBound()
            self._rows.append(cb)

        return

    def goto(self):
        newStartPage = self.component.NumberBox.script.rawText
        if newStartPage.isdigit():
            page_start = int(newStartPage)
            page_len = self.row
            tags = self.getFiler()
            sortFlag = self.getIndexSortBy()
            forward = 1
            BigWorld.player().getShopCatalogFiltered(sortFlag, forward, page_start, page_len, tags)

    def updatePage(self):
        tags = self.getFiler()
        sortFlag = self.getIndexSortBy()
        BigWorld.player().getShopCatalogFiltered(sortFlag, 1, self.page_start, self.row, tags)

    def buttonFindClick(self):
        tags = self.getFiler()
        sortFlag = self.getIndexSortBy()
        forward = 1
        BigWorld.player().getShopCatalogFiltered(sortFlag, forward, 0, self.row, tags)

    def buttonRightClick(self):
        tags = self.getFiler()
        sortFlag = self.getIndexSortBy()
        forward = 1
        if self.page_start > self.last_index_item:
            startfrom = self.page_start
        else:
            startfrom = self.last_index_item
        BigWorld.player().getShopCatalogFiltered(sortFlag, forward, startfrom, self.row, tags)

    def buttonLeftClick(self):
        tags = self.getFiler()
        sortFlag = self.getIndexSortBy()
        forward = 0
        if self.page_start < self.last_index_item:
            startfrom = self.page_start
        else:
            startfrom = self.last_index_item
        BigWorld.player().getShopCatalogFiltered(sortFlag, forward, startfrom, self.row, tags)

    def setData(self, data):
        dataitems = data['data']
        self.old_page_start = self.page_start
        self.old_last_index_item = self.last_index_item
        self.page_start = page_start = data['page_start']
        self.last_index_item = last_index_item = data['last_index_item']
        self.all_index_item = all_index_item = data['all_index_item']
        self.component.label_page.text = '%s-%s/%s' % (page_start, last_index_item + 1, all_index_item)
        for cb, item in map(lambda a, b: (a, b), self._rows, dataitems):
            if item:
                username, compxitem, price, bank, timelost = item
                cb.setItem(compxitem, price, bank, username.decode('utf8'), timelost)
            else:
                cb.setItem(None)

        return

    def buyDialog(self, item = None, BankName = '', username = '', price = 0):
        windowID = str(item['complexItemID']) + str(hash(username))
        tmp_gui = self.wbar.getWindowByID(windowID)
        if not tmp_gui:
            tmp_gui = soGUI.soProofOfPurchaseInShop.soProofOfPurchaseInShop(GUI.Window(), self.callbackEnter, windowID, self.updatePage)
            self.wbar.addWindow(windowID, tmp_gui, username)
        tmp_gui.show(item=item, BankName=BankName, username=username, price=price)
        self.wbar.topWindow(windowID)

    def callbackEnter(self, enter, wid):
        if enter:
            self.activeWindowID = wid
            return
        else:
            if self.activeWindowID == wid:
                self.activeWindowID = None
            return

    def handleKeyEvent(self, event):
        if event.key == 256:
            if event.isKeyDown():
                self.activeWindowIDMoved = self.activeWindowID
                self.wbar.topWindow(self.activeWindowIDMoved)
            else:
                self.activeWindowIDMoved = None
            return True
        else:
            return False

    def scrolledUP(self):
        pass

    def scrolledDOWN(self):
        pass

    def show(self):
        self.component.moveFocus = True
        self.component.crossFocus = True
        self.component.focus = True
        self.buttonFindClick()

    def handleMouseEvent(self, cmp, event):
        if self.activeWindowIDMoved:
            dx = event.dx
            dy = event.dy
            dz = event.dz
            window = self.wbar.getWindowByID(self.activeWindowIDMoved)
            if not window:
                return True
            x, y, z = window.component.position
            window.component.position = (x + dx, y + dy, z)
            return False
        return True