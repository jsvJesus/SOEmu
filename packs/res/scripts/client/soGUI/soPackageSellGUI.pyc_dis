# Embedded file name: scripts/client/soGUI/soPackageSellGUI.py
import BigWorld
import soGUI
from Helpers.PyGUI import PyGUIBase
import BWPersonality
import GUI
from soGUI.soItemView import soItemView, soItemSlot
import soGUI.soItemView as module_soItemView
from soGUI.soList import soList
from soGUI.soList import ListPropsStructure
from soGUI.soButton import soButton
from Helpers.PyGUI import PyGUIEvent
from soGUI.soCheckBox import soCheckBox
from Items import ItemsCatalog
import ItemsUtils
from soGUI.soToolTipComponent import soToolTipComponent
from Localization import lc
from gui_const import PACKAGE_SELL
EVENT_PACKSELECT = PACKAGE_SELL.EVENT_PACKSELECT
EVENT_ITEMADD = PACKAGE_SELL.EVENT_ITEMADD
EVENT_ITEMREMOVE = PACKAGE_SELL.EVENT_ITEMREMOVE
EVENT_BUY = PACKAGE_SELL.EVENT_BUY
EVENT_CLEAR = PACKAGE_SELL.EVENT_CLEAR
EVENT_AUTOFILL = PACKAGE_SELL.EVENT_AUTOFILL
EVENT_HIDEUNAFFORDABLE = PACKAGE_SELL.EVENT_HIDEUNAFFORDABLE
EVENT_ITEMCONTEXT = PACKAGE_SELL.EVENT_ITEMCONTEXT
EVENT_CLOSE = PACKAGE_SELL.EVENT_CLOSE

class soPackageRewardSlot(soItemSlot):
    factoryString = 'soGUI.soPackageRewardSlot'
    SLOTWIDTH = 64
    SLOTHEIGHT = 64

    def __init__(self, component, slotIndex, itemData = None):
        soItemSlot.__init__(self, component, slotIndex, itemData, centerDProxy=True)
        component.script = self
        self.dragProxy = self.component.dragProxy
        self.proxyHolder = self.component
        self.proxyName = 'dragProxy'

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
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
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (5, self.SLOTHEIGHT - 5, 0.3)
        self.component.addChild(cmp, 'itemName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
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
            self.component.itemName.text = friendlyName
            self.component.itemCount.text = countStr
        else:
            self.component.itemIcon.textureName = ''
            self.component.itemName.text = ''
            self.component.itemCount.text = ''
        self.dragProxy.texture = self.component.itemIcon.texture
        return


class soPackagePaySlot(soItemSlot):
    factoryString = 'soGUI.soPackagePaySlot'
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
        self.fake = False

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.crossFocus = True
        cmp.dragFocus = True
        cmp.dropFocus = True
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
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (5, self.SLOTHEIGHT - 5, 0.3)
        self.component.addChild(cmp, 'itemName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
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
            item_fake = BigWorld.player().IsItemFake(self.itemData)
            self.component.itemName.text = friendlyName
            self.component.itemCount.text = countStr
            self.fakeSlot(item_fake)
        else:
            self.component.itemIcon.textureName = ''
            self.component.itemName.text = ''
            self.component.itemCount.text = ''
        self.dragProxy.texture = self.component.itemIcon.texture
        return

    def onDragStart(self):
        if self.haveItem():
            if not self.fake:
                self.dragProxy.visible = True
                return True
        return False

    def onDragStop(self):
        self.dragProxy.visible = False
        return True

    def cancelTrade(self):
        BWPersonality.GUICore.packageSellEvent(EVENT_ITEMREMOVE, self.itemData)

    def fakeSlot(self, doFake):
        self.fake = doFake
        if self.fake:
            self.component.itemIcon.colour = (255, 255, 255, 125)
        else:
            self.component.itemIcon.colour = (255, 255, 255, 255)


class soPackageSellScreen(PyGUIBase):
    factoryString = 'soGUI.soPackageSellScreen'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.interfaceID = BWPersonality.GUICore.GUI_ID_PACKAGESELL
        self.setupRoot()
        self.setupContent()
        self._alignWnd()

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 350
        cmp.height = 489
        cmp.visible = False

    def setupContent(self):
        itemView = soItemView(GUI.Window(), soPackageRewardSlot, slot_eventsHandler=self.rewardSlotHandler, eventsHandler=self.rewardItemViewHandler, rowWidth=2, rows=3, cols=2, vScroll=True, hScroll=False, borderWidth=0)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (199, 34, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'rewardItemView')
        itemView.onBound()
        itemView.setRestrictingComponent(None)
        itemView.setItems(None)
        itemView = soItemView(GUI.Window(), soPackagePaySlot, slot_eventsHandler=self.paySlotHandler, eventsHandler=self.payItemViewHandler, rowWidth=5, cols=5, rows=3, vScroll=True, hScroll=False, borderWidth=0)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (7, 256, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'payItemView')
        itemView.onBound()
        itemView.setRestrictingComponent(None)
        itemView.setItems(None)
        list = soList(GUI.Window(), soGUI.ListPropsStructure(width=190, height=190, isMultiSel=False, selectCallBack=self._onPackListElem, sorted=False))
        cmp = list.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (7, 35, 0.4)
        self.component.addChild(cmp, 'packages')
        list.onBound()
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
        cmp.position = (326, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=lc('GUI.PackageSellGUI.HIDE_UNAFFORDABLE_LABEL'), font='ruRU_Cyrvetica_Extra_10i.font', labelColour=(175, 166, 112, 255)))
        cmp = cb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (204, 232, 0.4)
        self.component.addChild(cmp, 'hideUnaffordable')
        cb.onBound()
        cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=lc('GUI.PackageSellGUI.AUTOFILL_LABEL'), font='ruRU_Cyrvetica_Extra_10i.font', labelColour=(175, 166, 11, 255)))
        cmp = cb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 461, 0.4)
        self.component.addChild(cmp, 'autofill')
        cb.onBound()
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.PackageSellGUI.CONFIRM_BUTTON_LABEL')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (114, 456, 0.5)
        self.component.addChild(cmp, 'buyBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.PackageSellGUI.CLEAR_BUTTON_LABEL')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (239, 456, 0.5)
        self.component.addChild(cmp, 'clearBtn')
        btn.onBound()
        btn.setVisualState('normal')
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 489
        cmp.width = 350
        cmp.position = (0, 0, 0.9)
        self.component.addChild(cmp, 'iFrame')
        cmp = GUI.Frame2('soGUI/maps/Controls/packSell/decFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 197
        cmp.width = 342
        cmp.position = (4, 31, 0.8)
        self.component.addChild(cmp, 'topDFrame')
        cmp = GUI.Frame2('soGUI/maps/Controls/packSell/decFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 198
        cmp.width = 342
        cmp.position = (4, 253, 0.8)
        self.component.addChild(cmp, 'botDFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (18, 15, 0.3)
        cmp.text = lc('GUI.PackageSellGUI.WINDOW_CAPTION')
        self.component.addChild(cmp, 'psLabel')
        cmp = GUI.Simple('soGUI/maps/Controls/packSell/header.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 21
        cmp.width = 101
        cmp.position = (9, 233, 0.8)
        self.component.addChild(cmp, 'header')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (59, 244, 0.3)
        cmp.text = lc('GUI.PackageSellGUI.FOR_EXCHANGE_LABEL')
        self.component.addChild(cmp, 'payLabel')
        return

    def rewardSlotHandler(self, event, data):
        if event == module_soItemView.SLOTEVENT_MOUSEENTER:
            if isinstance(data, soPackageRewardSlot):
                BWPersonality.GUICore.toolTipEvent(data.itemData, self.interfaceID, soToolTipComponent.EVENT_SHOW)
                return True
        if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
            if isinstance(data, soPackageRewardSlot):
                BWPersonality.GUICore.toolTipEvent(data.itemData, self.interfaceID, soToolTipComponent.EVENT_HIDE)
                return True
        if event == module_soItemView.SLOTEVENT_RCLICK:
            if isinstance(data, soPackageRewardSlot):
                BWPersonality.GUICore.packageSellEvent(PACKAGE_SELL.EVENT_ITEMCONTEXT, [data.itemData, PACKAGE_SELL.REWARD_ITEM])
                return True

    def rewardItemViewHandler(self, event, data):
        return False

    def paySlotHandler(self, event, data):
        from soInventoryScreen import soInventorySlot2
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soInventorySlot2):
                return True
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soInventorySlot2):
                BWPersonality.GUICore.packageSellEvent(EVENT_ITEMADD, data[1].itemData)
        if event == module_soItemView.SLOTEVENT_MOUSEENTER:
            if isinstance(data, soPackagePaySlot):
                BWPersonality.GUICore.toolTipEvent(data.itemData, self.interfaceID, soToolTipComponent.EVENT_SHOW)
                return True
        if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
            if isinstance(data, soPackagePaySlot):
                BWPersonality.GUICore.toolTipEvent(data.itemData, self.interfaceID, soToolTipComponent.EVENT_HIDE)
                return True
        if event == module_soItemView.SLOTEVENT_DBLCLICK:
            if isinstance(data, soPackagePaySlot):
                BWPersonality.GUICore.packageSellEvent(EVENT_ITEMREMOVE, data.itemData)
                return True
        if event == module_soItemView.SLOTEVENT_RCLICK:
            if isinstance(data, soPackagePaySlot):
                BWPersonality.GUICore.packageSellEvent(PACKAGE_SELL.EVENT_ITEMCONTEXT, [data.itemData, PACKAGE_SELL.PAY_ITEM])
                return True
        return False

    def payItemViewHandler(self, event, data):
        return False

    def _onPackListElem(self):
        selection = self.component.packages.script.getSelection()[-1]
        data = self.component.packages.script.getAttachment(selection)
        BWPersonality.GUICore.packageSellEvent(EVENT_PACKSELECT, data)

    def _alignWnd(self):
        invCmp = getattr(BWPersonality.GUICore.worldLayer, 'inventory', None)
        sW, sH = BigWorld.screenSize()
        if not invCmp:
            psX = (sW + self.component.width) / 2.0
            psY = (sH + self.component.height) / 2.0
            self.component.position = (psX, psY, 0.5)
            return
        else:
            iX = invCmp.position.x - invCmp.width - 150
            iY = invCmp.position.y + invCmp.height
            self.component.position = (iX, iY, 0.5)
            return

    def _updatePacks(self, data):
        self.component.packages.script.clear()
        for pack in data:
            isLast = pack == data[-1]
            self.component.packages.script.addElement(pack[1], pack[0], not isLast)

    def _updateReward(self, data):
        self.component.rewardItemView.script.setItems(data)

    def _updatePay(self, data):
        self.component.payItemView.script.setItems(data)

    def update(self):
        data = BWPersonality.GUICore.packageSellDataSection
        if data.has_key('hideUnaffordable'):
            if data['hideUnaffordable']:
                self.component.hideUnaffordable.script.setActive()
            else:
                self.component.hideUnaffordable.script.setInactive()
        if data.has_key('autofill'):
            if data['autofill']:
                self.component.autofill.script.setActive()
            else:
                self.component.autofill.script.setInactive()
        if data.has_key('packs'):
            self._updatePacks(data['packs'])
        if data.has_key('rewardItems'):
            self._updateReward(data['rewardItems'])
        if data.has_key('payItems'):
            self._updatePay(data['payItems'])

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'packageSell')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        sendEvent = self.component.visible
        self.component.visible = False
        if sendEvent:
            BWPersonality.GUICore.packageSellEvent(EVENT_CLOSE, None)
        BWPersonality.GUICore.setBestCursor()
        return

    @PyGUIEvent('hideUnaffordable', 'onStateChange', 0)
    @PyGUIEvent('autofill', 'onStateChange', 1)
    def onCBs(self, cbN):
        if cbN == 0:
            state = self.component.hideUnaffordable.script.isChecked()
            BWPersonality.GUICore.packageSellEvent(EVENT_HIDEUNAFFORDABLE, state)
        elif cbN == 1:
            state = self.component.autofill.script.isChecked()
            BWPersonality.GUICore.packageSellEvent(EVENT_AUTOFILL, state)

    @PyGUIEvent('buyBtn', 'onClick')
    def onBuyBtn(self):
        BWPersonality.GUICore.packageSellEvent(EVENT_BUY, None)
        return

    @PyGUIEvent('clearBtn', 'onClick')
    def onClearBtn(self):
        BWPersonality.GUICore.packageSellEvent(EVENT_CLEAR, None)
        return

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()