# Embedded file name: scripts/client/soGUI/soPCTradeScreen.py
import GUI
import soGUI
import Helpers.PyGUI as PyGUI
import BWPersonality
import BigWorld
from soGUI.soButton import soButton, soButtonWTT
from soGUI.soEditField import soEditField2
from Helpers.PyGUI import PyGUIEvent
from Helpers.BWCoroutine import *
from Items import ItemsCatalog
import ItemsUtils
from soGUI.soItemView import soItemView, soItemSlot
import soGUI.soItemView as module_soItemView
from soGUI.soToolTipComponent import soToolTipComponent
from Helpers.PyGUI import PyGUIBase
from soGUI.soEditField import soEditBox
from gui_const import PC_TRADE, GUI_ID
from Localization import lc

class soPCTradeSlot(soItemSlot):
    factoryString = 'soGUI.soPCTradeSlot'
    SLOTWIDTH = 128
    SLOTHEIGHT = 64

    def __init__(self, component, slotIndex, itemData = None):
        soItemSlot.__init__(self, component, slotIndex, itemData, centerDProxy=True)
        component.script = self
        self.dragProxy = self.component.dragProxy
        self.proxyHolder = self.component
        self.proxyName = 'dragProxy'
        self._onDragStart = self.onDragStart
        self._onDragStop = self.onDragStop

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.dragFocus = True
        cmp.dropFocus = True
        cmp.crossFocus = True
        cmp.moveFocus = True
        cmp.mouseButtonFocus = True

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/cellFrame2.tga')
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.9)
        self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 64
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 128)
        cmp.materialFX = 'BLEND'
        cmp.position = (32, 0, 0.5)
        cmp.visible = False
        self.component.addChild(cmp, 'dragProxy')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 64
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (32, 0, 0.4)
        self.component.addChild(cmp, 'itemIcon')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (5, self.SLOTHEIGHT - 5, 0.3)
        self.component.addChild(cmp, 'itemName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH - 5, self.SLOTHEIGHT - 5, 0.3)
        self.component.addChild(cmp, 'itemCondition')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH - 5, 5, 0.3)
        self.component.addChild(cmp, 'itemCount')

    def _applyItemData(self):
        if self.haveItem():
            item_type = self.itemData['complexItemType']
            item_id = self.itemData['complexItemID']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            item_level = item_params['Level']
            iconName = ItemsUtils.getTextureByTint(self.itemData)
            if not iconName:
                iconName = item_params['IconName']
            if BWPersonality.GUICore.iconTextures is not None:
                if iconName not in BWPersonality.GUICore.iconTextures.failedIDs:
                    if BWPersonality.GUICore.iconTextures.has_key(iconName):
                        self.component.itemIcon.texture = BWPersonality.GUICore.iconTextures[iconName]
                    else:
                        self.component.itemIcon.textureName = iconName
            else:
                self.component.itemIcon.textureName = iconName
            countStr = ItemsUtils.GetDisplayValue(self.itemData)
            friendlyName = ItemsUtils.GetItemName(item_type, fGetShortName=True, tintItem=self.itemData)
            itemCondition = ItemsUtils.GetItemConditionPercentString(None, self.itemData)
            item_lock = BigWorld.player().ItemLocked(self.itemData)
            self.component.itemName.text = friendlyName
            self.component.itemCount.text = countStr
            self.component.itemCondition.text = itemCondition
            self.lockSlot(item_lock)
        else:
            self.component.itemIcon.textureName = ''
            self.component.itemName.text = ''
            self.component.itemCount.text = ''
            self.component.itemCondition.text = ''
            self.lockSlot(False)
        self.dragProxy.texture = self.component.itemIcon.texture
        return

    def cancelItem(self):
        BWPersonality.GUICore.pcTradeEvent(self.itemData, soPCTradeScreen.EVENT_ITEMCANCEL)

    def onDragStart(self):
        if self.haveItem() and self.slotIndex % 2:
            self.dragProxy.visible = True
            return True
        return False

    def onDragStop(self):
        self.dragProxy.visible = False
        return True

    def onRClick(self):
        if self.slotIndex % 2:
            soItemSlot.onRClick(self)

    def onDblClick(self):
        if self.slotIndex % 2:
            soItemSlot.onDblClick(self)

    def lockSlot(self, doLock):
        soItemSlot.lockSlot(self, doLock)
        if self.locked:
            self.component.itemIcon.colour = (125, 125, 125, 255)
        else:
            self.component.itemIcon.colour = (255, 255, 255, 255)


class soPCTradeScreen(PyGUI.Window):
    factoryString = 'soGUI.soPCTradeScreen'
    INTERFACE_WIDTH = 389
    INTERFACE_HEIGHT = 439
    HEADFRAME_WIDTH = 381
    HEADFRAME_HEIGHT = 113
    ITEMFRAME_WIDTH = 265
    ITEMFRAME_HEIGHT = 369
    SLOT_WIDTH = 128
    SLOT_HEIGHT = 64
    EVENT_MONEYSET = 0
    EVENT_ITEMOFFER = 1
    EVENT_ITEMCANCEL = 2
    EVENT_ACCEPT = 3
    EVENT_CANCEL = 4
    EVENT_ABORT = 5
    EVENT_CONTEXT = 6

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        component.script = self
        self.acceptBtn = None
        self.cancelBtn = None
        self.editBox = None
        self.playerSlots = []
        self.otherSlots = []
        self.interfaceID = BWPersonality.GUICore.GUI_ID_PCTRADE
        self.setupRoot()
        self.setupBtns()
        self.setupPictures()
        self.setupCaption()
        self.setupTradeElements()
        self.setupItems()
        return

    def setupRoot(self):
        self.component.horizontalPositionMode = self.component.verticalPositionMode = 'CLIP'
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.horizontalAnchor = 'CENTER'
        self.component.verticalAnchor = 'CENTER'
        self.component.colour = (255, 255, 255, 255)
        self.component.materialFX = 'BLEND'
        self.component.width = self.INTERFACE_WIDTH
        self.component.height = self.INTERFACE_HEIGHT
        self.component.position = (0.0, 0.0, 0.0)
        self.component.textureName = ''
        self.component.visible = False

        def setupFrames():
            headFrame = GUI.Frame2('soGUI/maps/con_frame.tga')
            headFrame.colour = (255, 255, 255, 255)
            headFrame.materialFX = 'BLEND'
            headFrame.widthMode = headFrame.heightMode = 'PIXEL'
            headFrame.width = self.HEADFRAME_WIDTH
            headFrame.height = self.HEADFRAME_HEIGHT
            headFrame.horizontalPositionMode = headFrame.verticalPositionMode = 'PIXEL'
            headFrame.horizontalAnchor = 'LEFT'
            headFrame.verticalAnchor = 'TOP'
            headFrame.position = (0, 8, 1.0)
            self.component.addChild(headFrame, 'headFrame')
            itemFrame = GUI.Frame2('soGUI/maps/con_frame.tga')
            itemFrame.colour = (255, 255, 255, 255)
            itemFrame.materialFX = 'BLEND'
            itemFrame.widthMode = itemFrame.heightMode = 'PIXEL'
            itemFrame.width = self.ITEMFRAME_WIDTH
            itemFrame.height = self.ITEMFRAME_HEIGHT
            itemFrame.horizontalPositionMode = itemFrame.verticalPositionMode = 'PIXEL'
            itemFrame.horizontalAnchor = 'LEFT'
            itemFrame.verticalAnchor = 'TOP'
            itemFrame.position = (58, 70, 0.9)
            self.component.addChild(itemFrame, 'itemFrame')

        def setupMarkUp():
            topLine = GUI.Simple('soGUI/maps/Colours/darkGrey.tga')
            topLine.tiled = True
            topLine.tileWidth = 1
            topLine.tileHeight = 1
            topLine.colour = (255, 255, 255, 255)
            topLine.materialFX = 'BLEND'
            topLine.verticalPositionMode = topLine.horizontalPositionMode = 'PIXEL'
            topLine.widthMode = topLine.heightMode = 'PIXEL'
            topLine.verticalAnchor = 'TOP'
            topLine.horizontalAnchor = 'LEFT'
            topLine.pixelSnap = False
            topLine.width = 377
            topLine.height = 1
            topLine.position = (2, 32, 0.1)
            self.component.addChild(topLine, 'topLine')
            bottomLine = GUI.Simple('soGUI/maps/Colours/darkGrey.tga')
            bottomLine.tiled = True
            bottomLine.tileWidth = 1
            bottomLine.tileHeight = 1
            bottomLine.colour = (255, 255, 255, 255)
            bottomLine.materialFX = 'BLEND'
            bottomLine.verticalPositionMode = bottomLine.horizontalPositionMode = 'PIXEL'
            bottomLine.widthMode = bottomLine.heightMode = 'PIXEL'
            bottomLine.verticalAnchor = 'TOP'
            bottomLine.horizontalAnchor = 'LEFT'
            bottomLine.pixelSnap = False
            bottomLine.width = 261
            bottomLine.height = 1
            bottomLine.position = (60, 394, 0.1)
            self.component.addChild(bottomLine, 'bottomLine')
            vertLine = GUI.Simple('soGUI/maps/Colours/darkGrey.tga')
            vertLine.tiled = True
            vertLine.tileWidth = 1
            vertLine.tileHeight = 1
            vertLine.colour = (255, 255, 255, 255)
            vertLine.materialFX = 'BLEND'
            vertLine.verticalPositionMode = vertLine.horizontalPositionMode = 'PIXEL'
            vertLine.widthMode = vertLine.heightMode = 'PIXEL'
            vertLine.verticalAnchor = 'TOP'
            vertLine.horizontalAnchor = 'LEFT'
            vertLine.pixelSnap = False
            vertLine.width = 1
            vertLine.height = 322
            vertLine.position = (190, 72, 0.1)
            self.component.addChild(vertLine, 'vertLine')

        setupFrames()
        setupMarkUp()
        GUI.reSort()

    def setupBtns(self):
        self.acceptBtn = soButton(GUI.Window())
        cmp = self.acceptBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (79, 401, 0.1)
        self.acceptBtn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        self.acceptBtn.onBound()
        self.acceptBtn.setVisualState('normal')
        cmp.label.text = lc('soPCTradeScreen.soGUI.STRING_425_19')
        self.component.addChild(cmp, 'acceptBtn')
        self.cancelBtn = soButton(GUI.Window())
        cmp = self.cancelBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (201, 401, 0.1)
        self.cancelBtn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        self.cancelBtn.onBound()
        self.cancelBtn.setVisualState('normal')
        cmp.label.text = lc('soPCTradeScreen.soGUI.STRING_443_19')
        self.component.addChild(cmp, 'cancelBtn')
        closeBox = soButton(GUI.Window())
        cmp = closeBox.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (371, 0, 0.1)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        btn = soButtonWTT(GUI.Window(), 'PC_trade_enter_money')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 19
        cmp.height = 21
        cmp.position = (302, 44, 0.1)
        btn.initVSC('soGUI/visual_styles/btnMoneyEnter.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = u''
        self.component.addChild(cmp, 'enterMoney')

    def setupPictures(self):
        playerPicture = GUI.Simple('soGUI/maps/avatar_unavailable.tga')
        playerPicture.horizontalPositionMode = playerPicture.verticalPositionMode = 'PIXEL'
        playerPicture.widthMode = playerPicture.heightMode = 'PIXEL'
        playerPicture.horizontalAnchor = 'LEFT'
        playerPicture.verticalAnchor = 'TOP'
        playerPicture.width = 54
        playerPicture.height = 84
        playerPicture.position = (324, 34, 0.1)
        self.component.addChild(playerPicture, 'playerPicture')
        otherPicture = GUI.Simple('soGUI/maps/avatar_unavailable.tga')
        otherPicture.horizontalPositionMode = otherPicture.verticalPositionMode = 'PIXEL'
        otherPicture.widthMode = otherPicture.heightMode = 'PIXEL'
        otherPicture.horizontalAnchor = 'LEFT'
        otherPicture.verticalAnchor = 'TOP'
        otherPicture.width = 54
        otherPicture.height = 84
        otherPicture.position = (3, 34, 0.1)
        self.component.addChild(otherPicture, 'otherPicture')

    def setupItems(self):
        itemView = soItemView(GUI.Window(), soPCTradeSlot, slot_eventsHandler=self.slotHandler, eventsHandler=self.itemViewHandler, rowWidth=2, hScroll=False, vScroll=False, borderWidth=0)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (62, 73, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'itemView')
        itemView.onBound()
        itemView.setRestrictingComponent(None)
        itemView.setItems(None)
        return

    def setupTradeElements(self):
        leftFrame = GUI.Frame2('soGUI/maps/Controls/CharScreen/stats_head_frame.tga')
        leftFrame.horizontalPositionMode = leftFrame.verticalPositionMode = 'PIXEL'
        leftFrame.widthMode = leftFrame.heightMode = 'PIXEL'
        leftFrame.horizontalAnchor = 'LEFT'
        leftFrame.verticalAnchor = 'TOP'
        leftFrame.colour = (255, 255, 255, 255)
        leftFrame.materialFX = 'BLEND'
        leftFrame.width = 130
        leftFrame.height = 33
        leftFrame.position = (59, 35, 0.8)
        self.component.addChild(leftFrame, 'leftFrame')
        rightFrame = GUI.Frame2('soGUI/maps/Controls/CharScreen/stats_head_frame.tga')
        rightFrame.horizontalPositionMode = rightFrame.verticalPositionMode = 'PIXEL'
        rightFrame.widthMode = rightFrame.heightMode = 'PIXEL'
        rightFrame.horizontalAnchor = 'LEFT'
        rightFrame.verticalAnchor = 'TOP'
        rightFrame.colour = (255, 255, 255, 255)
        rightFrame.materialFX = 'BLEND'
        rightFrame.width = 130
        rightFrame.height = 33
        rightFrame.position = (192, 35, 0.8)
        self.component.addChild(rightFrame, 'rightFrame')
        otherMoney = GUI.Text('')
        otherMoney.horizontalPositionMode = otherMoney.verticalPositionMode = 'PIXEL'
        otherMoney.horizontalAnchor = 'LEFT'
        otherMoney.verticalAnchor = 'TOP'
        otherMoney.colour = (175, 166, 112, 255)
        otherMoney.materialFX = 'BLEND'
        otherMoney.font = 'ruRU_calibri_default.font'
        otherMoney.text = '0'
        otherMoney.position = (83, 42, 0.1)
        self.component.addChild(otherMoney, 'otherMoney')
        myMoney = GUI.Text('')
        myMoney.horizontalPositionMode = myMoney.verticalPositionMode = 'PIXEL'
        myMoney.horizontalAnchor = 'LEFT'
        myMoney.verticalAnchor = 'TOP'
        myMoney.colour = (175, 166, 112, 255)
        myMoney.materialFX = 'BLEND'
        myMoney.font = 'ruRU_calibri_default.font'
        myMoney.text = '00000'
        myMoney.position = (197, 42, 0.1)
        self.component.addChild(myMoney, 'myMoney')
        leftIcon = GUI.Simple('soGUI/maps/Controls/inventory/moneyIcon.tga')
        leftIcon.horizontalPositionMode = leftIcon.verticalPositionMode = 'PIXEL'
        leftIcon.widthMode = leftIcon.heightMode = 'PIXEL'
        leftIcon.horizontalAnchor = 'LEFT'
        leftIcon.verticalAnchor = 'TOP'
        leftIcon.colour = (255, 255, 255, 255)
        leftIcon.materialFX = 'BLEND'
        leftIcon.width = 12
        leftIcon.height = 15
        leftIcon.position = (63, 44, 0.5)
        self.component.addChild(leftIcon, 'leftIcon')

    def setupCaption(self):
        playerName = GUI.Text('')
        playerName.horizontalPositionMode = playerName.verticalPositionMode = 'CLIP'
        playerName.horizontalAnchor = 'RIGHT'
        playerName.verticalAnchor = 'BOTTOM'
        playerName.font = 'ruRU_calibri_default.font'
        playerName.colour = (255, 100, 100, 255)
        playerName.materialFX = 'BLEND'
        playerName.text = BigWorld.player().name
        playerName.position = (1.0 - soGUI.getPixelWidth(self.component) * 29, 1.0 - soGUI.getPixelHeight(self.component) * 30, 0.1)
        self.component.addChild(playerName, 'playerName')
        otherName = GUI.Text('')
        otherName.horizontalPositionMode = otherName.verticalPositionMode = 'CLIP'
        otherName.horizontalAnchor = 'LEFT'
        otherName.verticalAnchor = 'BOTTOM'
        otherName.font = 'ruRU_calibri_default.font'
        otherName.colour = (255, 100, 100, 255)
        otherName.materialFX = 'BLEND'
        otherName.text = lc('soPCTradeScreen.soGUI.STRING_642_19')
        otherName.position = (-1.0 + soGUI.getPixelWidth(self.component) * 20, 1.0 - soGUI.getPixelHeight(self.component) * 30, 0.1)
        self.component.addChild(otherName, 'otherName')

    def slotHandler(self, event, data):
        from soGUI.soInventoryScreen import soInventorySlot2
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soInventorySlot2):
                return True
            else:
                return False
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soInventorySlot2):
                BWPersonality.GUICore.pcTradeEvent(self.EVENT_ITEMOFFER, data[1].itemData)
                return True
            else:
                return False
        if event == module_soItemView.SLOTEVENT_MOUSEENTER:
            if isinstance(data, soPCTradeSlot):
                BWPersonality.GUICore.toolTipEvent([data.itemData, data.slotIndex], self.interfaceID, soToolTipComponent.EVENT_SHOW)
                return True
        if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
            if isinstance(data, soPCTradeSlot):
                BWPersonality.GUICore.toolTipEvent([data.itemData, data.slotIndex], self.interfaceID, soToolTipComponent.EVENT_HIDE)
                return True
        if event == module_soItemView.SLOTEVENT_DBLCLICK:
            if isinstance(data, soPCTradeSlot):
                BWPersonality.GUICore.pcTradeEvent(self.EVENT_ITEMCANCEL, data.itemData)
                return True
        if event == module_soItemView.SLOTEVENT_RCLICK:
            if isinstance(data, soPCTradeSlot):
                BWPersonality.GUICore.pcTradeEvent(self.EVENT_CONTEXT, data.itemData)
                return True
        return False

    def itemViewHandler(self, event, data):
        from soGUI.soInventoryScreen import soInventorySlot2
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soInventorySlot2):
                return True
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soInventorySlot2):
                BWPersonality.GUICore.pcTradeEvent(self.EVENT_ITEMOFFER, data[1].itemData)
                return True
        return False

    def applyItems(self):
        if BWPersonality.GUICore.tradeDataSection is None:
            return
        else:
            items = BWPersonality.GUICore.tradeDataSection[1]
            self.component.itemView.script.setItems(items)
            return

    def show(self):
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'PCtrade')
        self.update()
        return

    def hide(self):
        self.abortTrade()
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def update(self):
        self.applyItems()
        if not BWPersonality.GUICore.tradeDataSection:
            return
        self.component.otherName.text = BWPersonality.GUICore.tradeDataSection[0]
        myMoney = str(BWPersonality.GUICore.tradeDataSection[2][0])
        _myMoney = u''
        hisMoney = str(BWPersonality.GUICore.tradeDataSection[2][1])
        _hisMoney = u''
        charCtr = 0
        for i in xrange(len(hisMoney) - 1, -1, -1):
            if charCtr % 3 == 0 and charCtr > 0:
                _hisMoney = u' ' + _hisMoney
            _hisMoney = hisMoney[i] + _hisMoney
            charCtr += 1

        charCtr = 0
        for i in xrange(len(myMoney) - 1, -1, -1):
            if charCtr % 3 == 0 and charCtr > 0:
                _myMoney = u' ' + _myMoney
            _myMoney = myMoney[i] + _myMoney
            charCtr += 1

        self.component.otherMoney.text = _hisMoney
        self.component.myMoney.text = _myMoney
        if BWPersonality.GUICore.tradeDataSection[3][0]:
            self.component.playerName.colour = (100, 255, 100, 255)
        else:
            self.component.playerName.colour = (255, 100, 100, 255)
        if BWPersonality.GUICore.tradeDataSection[3][1]:
            self.component.otherName.colour = (100, 255, 100, 255)
        else:
            self.component.otherName.colour = (255, 100, 100, 255)

    def offerItem(self, itemDict):
        BWPersonality.GUICore.pcTradeEvent(self.EVENT_ITEMOFFER, itemDict)

    def cancelItem(self, itemDict):
        BWPersonality.GUICore.pcTradeEvent(self.EVENT_ITEMCANCEL, itemDict)

    def acceptTrade(self):
        BWPersonality.GUICore.pcTradeEvent(self.EVENT_ACCEPT, None)
        return

    def cancelTrade(self):
        BWPersonality.GUICore.pcTradeEvent(self.EVENT_CANCEL, None)
        return

    def abortTrade(self):
        BWPersonality.GUICore.pcTradeEvent(self.EVENT_ABORT, None)
        return

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()

    @PyGUIEvent('acceptBtn', 'onClick')
    def onAccept(self):
        self.acceptTrade()

    @PyGUIEvent('cancelBtn', 'onClick')
    def onCancel(self):
        self.cancelTrade()

    @PyGUIEvent('enterMoney', 'onClick')
    def onMoney(self):
        BWPersonality.GUICore.pcTradeEvent(self.EVENT_MONEYSET, None)
        return


class soPCTradeSlot_me(soItemSlot):
    factoryString = 'soGUI.soPCTradeSlot_me'
    SLOTWIDTH = 64
    SLOTHEIGHT = 64

    def __init__(self, component, slotIndex, itemData = None):
        soItemSlot.__init__(self, component, slotIndex, itemData, centerDProxy=True)
        component.script = self
        self.dragProxy = self.component.dragProxy
        self.proxyHolder = self.component
        self.proxyName = 'dragProxy'
        self._onDragStart = self.onDragStart
        self._onDragStop = self.onDragStop

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.dragFocus = True
        cmp.dropFocus = False
        cmp.crossFocus = True
        cmp.moveFocus = True
        cmp.mouseButtonFocus = True

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/cellFrame2.tga')
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.9)
        self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 128)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.5)
        cmp.visible = False
        self.component.addChild(cmp, 'dragProxy')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.4)
        self.component.addChild(cmp, 'itemIcon')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (5, self.SLOTHEIGHT - 5, 0.3)
        self.component.addChild(cmp, 'itemName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH - 5, 5, 0.3)
        self.component.addChild(cmp, 'itemCount')

    def _applyItemData(self):
        if self.haveItem():
            item_type = self.itemData['complexItemType']
            item_id = self.itemData['complexItemID']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            item_level = item_params['Level']
            iconName = item_params['IconName']
            if BWPersonality.GUICore.iconTextures is not None:
                if iconName not in BWPersonality.GUICore.iconTextures.failedIDs:
                    if BWPersonality.GUICore.iconTextures.has_key(iconName):
                        self.component.itemIcon.texture = BWPersonality.GUICore.iconTextures[iconName]
                    else:
                        self.component.itemIcon.textureName = iconName
            else:
                self.component.itemIcon.textureName = iconName
            countStr = ItemsUtils.GetDisplayValue(self.itemData)
            friendlyName = ItemsUtils.GetItemName(item_type, fGetShortName=True, tintItem=self.itemData)
            itemCondition = ItemsUtils.GetItemConditionPercentString(None, self.itemData)
            self.component.itemName.text = friendlyName
            if itemCondition:
                self.component.itemCount.text = itemCondition
            if countStr:
                self.component.itemCount.text = countStr
        else:
            self.component.itemIcon.textureName = ''
            self.component.itemName.text = ''
            self.component.itemCount.text = ''
        self.dragProxy.texture = self.component.itemIcon.texture
        return

    def cancelItem(self):
        BWPersonality.GUICore.pcTradeEvent(PC_TRADE.EVENT_DELITEM, self.itemData)

    def onDragStart(self):
        if self.haveItem():
            self.dragProxy.visible = True
            return True
        return False

    def onDragStop(self):
        self.dragProxy.visible = False
        return True


class soPCTradeSlot_he(soItemSlot):
    factoryString = 'soGUI.soPCTradeSlot_he'
    SLOTWIDTH = 64
    SLOTHEIGHT = 64

    def __init__(self, component, slotIndex, itemData = None):
        soItemSlot.__init__(self, component, slotIndex, itemData, centerDProxy=True)
        component.script = self

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.dragFocus = False
        cmp.dropFocus = False
        cmp.crossFocus = True
        cmp.moveFocus = True
        cmp.mouseButtonFocus = True

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/cellFrame2.tga')
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.9)
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
        cmp.position = (0, 0, 0.4)
        self.component.addChild(cmp, 'itemIcon')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (5, self.SLOTHEIGHT - 5, 0.3)
        self.component.addChild(cmp, 'itemName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH - 5, 5, 0.3)
        self.component.addChild(cmp, 'itemCount')

    def _applyItemData(self):
        if self.haveItem():
            item_type = self.itemData['complexItemType']
            item_id = self.itemData['complexItemID']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            item_level = item_params['Level']
            iconName = ItemsUtils.getTextureByTint(self.itemData)
            if not iconName:
                iconName = item_params['IconName']
            if BWPersonality.GUICore.iconTextures is not None:
                if iconName not in BWPersonality.GUICore.iconTextures.failedIDs:
                    if BWPersonality.GUICore.iconTextures.has_key(iconName):
                        self.component.itemIcon.texture = BWPersonality.GUICore.iconTextures[iconName]
                    else:
                        self.component.itemIcon.textureName = iconName
            else:
                self.component.itemIcon.textureName = iconName
            countStr = ItemsUtils.GetDisplayValue(self.itemData)
            friendlyName = ItemsUtils.GetItemName(item_type, fGetShortName=True, tintItem=self.itemData)
            itemCondition = ItemsUtils.GetItemConditionPercentString(None, self.itemData)
            self.component.itemName.text = friendlyName
            if itemCondition:
                self.component.itemCount.text = itemCondition
            if countStr:
                self.component.itemCount.text = countStr
        else:
            self.component.itemIcon.textureName = ''
            self.component.itemName.text = ''
            self.component.itemCount.text = ''
        return


class soPCTradeScreen2(PyGUIBase):
    factoryString = 'soGUI.soPCTradeScreen2'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.interfaceID = GUI_ID.GUI_ID_PCTRADE
        self.setupRoot()
        self.setupPlayerWnd()
        self.setupHisWnd()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        cmp.dropFocus = True
        cmp.width = 332
        cmp.height = 554
        cmp.position = (250, 50, 0.3)

    def setupPlayerWnd(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 332
        cmp.height = 304
        cmp.position = (0, 245, 0.5)
        self.component.addChild(cmp, 'playerWnd')
        wnd = cmp
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 2.0
        cmp.width = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        wnd.addChild(cmp, 'dFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (18, 15, 0.3)
        cmp.text = u'_not_set_'
        wnd.addChild(cmp, 'pName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 40, 0.3)
        cmp.text = lc('GUI.InterPlayerTrade.MONEY_OUT_LABEL')
        wnd.addChild(cmp, 'mLabel')
        cmp = GUI.Frame2('soGUI/maps/Controls/pcTrade/confirm_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 219
        cmp.width = 324
        cmp.position = (4, 28, 0.1)
        cmp.visible = False
        cmp.dragFocus = True
        cmp.dropFocus = True
        cmp.mouseButtonFocus = True
        cmp.script = self
        wnd.addChild(cmp, 'confirm')
        edit = soEditBox(GUI.Window(), width=85, height=19, font='ruRU_Cyrvetica_Extra_14i.font', hOffset=4, vOffset=2)
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (110, 29, 0.5)
        wnd.addChild(cmp, 'edit')
        edit.onBound()
        edit.setValue(u'0')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (205, 40, 0.3)
        cmp.text = lc('GUI.InterPlayerTrade.GOLD_IN_LABEL')
        wnd.addChild(cmp, 'goldLabel')
        edit = soEditBox(GUI.Window(), width=85, height=19, font='ruRU_Cyrvetica_Extra_14i.font', hOffset=4, vOffset=2, color=(212, 169, 113, 255))
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (230, 29, 0.5)
        wnd.addChild(cmp, 'goldEdit')
        edit.onBound()
        edit.setValue(u'0')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 324
        cmp.height = 1
        cmp.position = (5, 51, 0.9)
        wnd.addChild(cmp, 'line1')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 326
        cmp.height = 1
        cmp.position = (3, 249, 0.9)
        wnd.addChild(cmp, 'line2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (166, 259, 0.3)
        cmp.text = u'empty'
        wnd.addChild(cmp, 'info_msg')
        btn = soButton(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (7, 271, 0.4)
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onBound()
        btn.onClick = self.onOfferBtn
        cmp.label.text = lc('GUI.InterPlayerTrade.MAKE_OFFER_BUTTON_LABEL')
        btn._updateVisualState()
        wnd.addChild(cmp, 'offerBtn')
        btn = soButton(GUI.Window(''))
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.buttonActive = False
        btn.buttonDisabled = True
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (116, 271, 0.4)
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onBound()
        btn.onClick = self.onConfirmBtn
        cmp.label.text = lc('GUI.InterPlayerTrade.CONFIRM_BUTTON_LABEL')
        btn._updateVisualState()
        wnd.addChild(cmp, 'confirmBtn')
        btn = soButton(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (225, 271, 0.4)
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onBound()
        btn.buttonDisabled = True
        btn.onClick = self.onCancelBtn
        cmp.label.text = lc('GUI.InterPlayerTrade.CANCEL_BUTTON_LABEL')
        btn._updateVisualState()
        wnd.addChild(cmp, 'cancelBtn')
        itemView = soItemView(GUI.Window(), soPCTradeSlot_me, slot_eventsHandler=self.mySlotHandler, eventsHandler=self.myIVHandler, rows=3, cols=5, rowWidth=5, hScroll=False, vScroll=False, borderWidth=0)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (6, 53, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        wnd.addChild(cmp, 'itemView')
        itemView.onBound()
        itemView.setRestrictingComponent(None)
        itemView.setItems(None)
        return

    def setupHisWnd(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 332
        cmp.height = 248
        cmp.position = (0, 0, 0.5)
        self.component.addChild(cmp, 'hisWnd')
        wnd = cmp
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 2.0
        cmp.width = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        wnd.addChild(cmp, 'dFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (18, 15, 0.3)
        cmp.text = u'_not_set_'
        wnd.addChild(cmp, 'hisName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (90, 39, 0.3)
        cmp.text = lc('GUI.InterPlayerTrade.MONEY_IN_LABEL')
        wnd.addChild(cmp, 'mLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (100, 39, 0.3)
        cmp.text = u'0' + lc('GUI.InterPlayerTrade.ruble_in_label')
        wnd.addChild(cmp, 'mCount')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (200, 39, 0.3)
        cmp.text = u'0' + lc('GUI.InterPlayerTrade.GOLD_IN_LABEL')
        wnd.addChild(cmp, 'gCount')
        cmp = GUI.Frame2('soGUI/maps/Controls/pcTrade/confirm_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 216
        cmp.width = 324
        cmp.position = (4, 28, 0.1)
        cmp.visible = False
        wnd.addChild(cmp, 'confirm')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 324
        cmp.height = 1
        cmp.position = (6, 48, 0.9)
        wnd.addChild(cmp, 'line1')
        itemView = soItemView(GUI.Window(), soPCTradeSlot_he, slot_eventsHandler=self.hisSlotHandler, eventsHandler=self.hisIVHandler, rows=3, cols=5, rowWidth=5, hScroll=False, vScroll=False, borderWidth=0)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (6, 50, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        wnd.addChild(cmp, 'itemView')
        itemView.onBound()
        itemView.setRestrictingComponent(None)
        itemView.setItems(None)
        closeBox = soButton(GUI.Window())
        cmp = closeBox.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (308, 6, 0.2)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox._updateVisualState()
        closeBox.onClick = self.onCloseBox
        wnd.addChild(cmp, 'closeBox')
        return

    def mySlotHandler(self, event, data):
        if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
            BWPersonality.GUICore.toolTipEvent([PC_TRADE.SOURCE_PLAYER, data.itemData], self.interfaceID, soToolTipComponent.EVENT_HIDE)
            return True
        if event == module_soItemView.SLOTEVENT_MOUSEENTER:
            BWPersonality.GUICore.toolTipEvent([PC_TRADE.SOURCE_PLAYER, data.itemData], self.interfaceID, soToolTipComponent.EVENT_SHOW)
            return True
        if event == module_soItemView.SLOTEVENT_DBLCLICK:
            BWPersonality.GUICore.pcTradeEvent(PC_TRADE.EVENT_ACTION, [PC_TRADE.SOURCE_PLAYER, data.itemData])
            return True
        if event == module_soItemView.SLOTEVENT_RCLICK:
            BWPersonality.GUICore.pcTradeEvent(PC_TRADE.EVENT_CONTEXT, [PC_TRADE.SOURCE_PLAYER, data.itemData])
            return True
        return False

    def myIVHandler(self, event, data):
        from soGUI.soInventoryScreen import soInventorySlot2
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soInventorySlot2):
                return True
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soInventorySlot2):
                BWPersonality.GUICore.pcTradeEvent(PC_TRADE.EVENT_ADDITEM, data[1].itemData)
                return True
        return False

    def hisSlotHandler(self, event, data):
        if event == module_soItemView.SLOTEVENT_RCLICK:
            BWPersonality.GUICore.pcTradeEvent(PC_TRADE.EVENT_CONTEXT, [PC_TRADE.SOURCE_CONTRACTOR, data.itemData])
            return True
        if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
            BWPersonality.GUICore.toolTipEvent([PC_TRADE.SOURCE_CONTRACTOR, data.itemData], self.interfaceID, soToolTipComponent.EVENT_HIDE)
            return True
        if event == module_soItemView.SLOTEVENT_MOUSEENTER:
            BWPersonality.GUICore.toolTipEvent([PC_TRADE.SOURCE_CONTRACTOR, data.itemData], self.interfaceID, soToolTipComponent.EVENT_SHOW)
            return True
        return False

    def hisIVHandler(self, event, data):
        return False

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'pc_trade')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        BWPersonality.GUICore.pcTradeEvent(PC_TRADE.EVENT_ABORT, None)
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        return

    def update(self):
        data = BWPersonality.GUICore.tradeDataSection
        if data is None:
            return
        else:
            if data.has_key('player_items'):
                self.component.playerWnd.itemView.script.setItems(data['player_items'])
            if data.has_key('contractor_items'):
                self.component.hisWnd.itemView.script.setItems(data['contractor_items'])
            if data.has_key('player_name'):
                self.component.playerWnd.pName.text = data['player_name']
            if data.has_key('contractor_name'):
                self.component.hisWnd.hisName.text = data['contractor_name']
            if data.has_key('player_money'):
                self.component.playerWnd.edit.script.setValue(data['player_money'])
            if data.has_key('contractor_money'):
                self.component.hisWnd.mCount.text = data['contractor_money']
            if data.has_key('player_gold'):
                self.component.playerWnd.goldEdit.script.setValue(data['player_gold'])
            if data.has_key('contractor_gold'):
                self.component.hisWnd.gCount.text = data['contractor_gold'] + lc('GUI.InterPlayerTrade.GOLD_IN_LABEL')
            if data.has_key('player_confirmation'):
                self.component.playerWnd.confirm.visible = data['player_confirmation']
                self.component.playerWnd.offerBtn.script.buttonDisabled = data['player_confirmation']
                self.component.playerWnd.cancelBtn.script.buttonDisabled = not data['player_confirmation']
                self.component.playerWnd.offerBtn.script._updateVisualState()
                self.component.playerWnd.cancelBtn.script._updateVisualState()
                if data['player_confirmation']:
                    if self.component.playerWnd.edit.script.active:
                        self.component.playerWnd.edit.script.activate(False)
                self._updateConfirmationAvailability()
            if data.has_key('transaction_confirmed'):
                self.component.playerWnd.confirmBtn.script.buttonActive = data['transaction_confirmed']
                self.component.playerWnd.confirmBtn.script._updateVisualState()
            if data.has_key('contractor_confirmation'):
                self.component.hisWnd.confirm.visible = data['contractor_confirmation']
                self._updateConfirmationAvailability()
            if data.has_key('input_validator'):
                self.component.playerWnd.edit.script.setValidator(data['input_validator'])
            if data.has_key('input_gold_validator'):
                self.component.playerWnd.goldEdit.script.setValidator(data['input_gold_validator'])
            if data.has_key('message'):
                self.component.playerWnd.info_msg.text = data['message']
            return

    def _updateConfirmationAvailability(self):
        if self.component.playerWnd.confirm.visible and self.component.hisWnd.confirm.visible:
            self.component.playerWnd.confirmBtn.script.buttonDisabled = False
        else:
            self.component.playerWnd.confirmBtn.script.buttonDisabled = True
        self.component.playerWnd.confirmBtn.script._updateVisualState()

    def onOfferBtn(self):
        self.component.playerWnd.edit.script.activate(False)
        self.component.playerWnd.goldEdit.script.activate(False)
        BWPersonality.GUICore.pcTradeEvent(PC_TRADE.EVENT_OFFER, None)
        return

    def onConfirmBtn(self):
        BWPersonality.GUICore.pcTradeEvent(PC_TRADE.EVENT_CONFIRM, None)
        return

    def onCancelBtn(self):
        BWPersonality.GUICore.pcTradeEvent(PC_TRADE.EVENT_CANCEL, None)
        return

    def onCloseBox(self):
        self.hide()

    @PyGUIEvent('playerWnd.edit', 'onActive')
    def onEditFocus(self, active):
        if not active:
            BWPersonality.GUICore.pcTradeEvent(PC_TRADE.EVENT_MONEYSET, self.component.playerWnd.edit.script.getRaw())

    @PyGUIEvent('playerWnd.goldEdit', 'onActive')
    def onGoldEditFocus(self, active):
        if not active:
            BWPersonality.GUICore.pcTradeEvent(PC_TRADE.EVENT_GOLDSET, self.component.playerWnd.goldEdit.script.getRaw())