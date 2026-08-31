# Embedded file name: scripts/client/soGUI/soWarehouse.py
import BigWorld
import BWPersonality
import GUI
import soGUI
from Helpers.PyGUI import PyGUIBase
from soGUI.soItemView import soItemView, soItemSlot
import soGUI.soItemView as module_soItemView
from Items import ItemsCatalog
import ItemsUtils
from soGUI.soToolTipComponent import soToolTipComponent
from Helpers.PyGUI import PyGUIEvent
from soGUI.soButton import soButton, soButtonWTT
from soGUI.data import GUIEvents
from functools import partial
from gui_const import ITEM_CACHE
from Localization import lc
import gui_jokes
from soGUI.soEditField import soEditBox
ACTION_TAKE = ITEM_CACHE.EVENT_TAKE
ACTION_GIVE = ITEM_CACHE.EVENT_GIVE
ACTION_FILTERCHANGE = ITEM_CACHE.EVENT_FILTERCHANGE

class soWarehouseSlot(soItemSlot):
    factoryString = 'soGUI.soWarehouseSlot'
    SLOTWIDTH = 64
    SLOTHEIGHT = 64

    def __init__(self, component, slotIndex, itemData = None):
        soItemSlot.__init__(self, component, slotIndex, itemData, centerDProxy=True)
        self.item_lock_in_shop = False
        self.cache_mode = -1
        component.script = self
        self.dragProxy = self.component.dragProxy
        self.proxyHolder = self.component
        self.proxyName = 'dragProxy'
        self._onDragStart = self.onDragStart
        self._onDragStop = self.onDragStop

    def onRClick(self):
        print 'onRClick ', self.cache_mode, ItemsUtils.CACHE_MODE_SAFEBOX, self.getCache_mode()
        if BigWorld.player().cacheMode != ItemsUtils.CACHE_MODE_SAFEBOX:
            return
        if not self.itemData:
            return
        if self.itemData['fromEntityID'] != 0:
            return
        complexItemID = self.itemData['complexItemID']
        if self.item_lock_in_shop:
            actions = {('cancel_sale', complexItemID): lc('GUI.warehouse.canselSale')}
        else:
            actions = {('sale', complexItemID): c('GUI.warehouse.sale')}
        interfaceID = BWPersonality.GUICore.GUI_ID_ITEMCACHE
        BWPersonality.GUICore.showContextMenu(interfaceID, actions)

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
        cmp.width = self.SLOTWIDTH
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
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.4)
        self.component.addChild(cmp, 'itemIcon')
        cmp = GUI.Simple('soGUI/maps/Controls/Table/classified_cell.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH / 4.0
        cmp.height = self.SLOTHEIGHT / 4.0
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (1, 1, 0.4)
        self.component.addChild(cmp, 'itemLockInShop')
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
            itemCondition = ItemsUtils.GetItemConditionPercentString(BigWorld.player(), self.itemData)
            item_lock = BigWorld.player().ItemLocked(self.itemData)
            item_lock_in_shop = BigWorld.player().ItemLockedByShop(self.itemData)
            self.component.itemName.text = friendlyName
            self.component.itemCount.text = countStr
            self.item_lock_in_shop = item_lock_in_shop
            self.lockSlot(item_lock or item_lock_in_shop)
            if item_lock_in_shop:
                self.component.itemLockInShop.visible = True
        else:
            self.component.itemIcon.textureName = ''
            self.component.itemName.text = ''
            self.component.itemCount.text = ''
            self.component.itemLockInShop.visible = False
            self.lockSlot(False)
            self.item_lock_in_shop = False
        self.dragProxy.texture = self.component.itemIcon.texture
        return

    def take(self):
        BWPersonality.GUICore.itemCacheWarehouseEvent(ACTION_TAKE, self.itemData)

    def onDragStart(self):
        if self.haveItem():
            self.dragProxy.visible = True
            return True
        return False

    def onDragStop(self):
        self.dragProxy.visible = False
        return True

    def lockSlot(self, doLock):
        soItemSlot.lockSlot(self, doLock)
        if self.locked:
            self.component.itemIcon.colour = (125, 125, 125, 255)
        else:
            self.component.itemIcon.colour = (255, 255, 255, 255)


class soWarehouse(PyGUIBase):
    factoryString = 'soGUI.soWarehouse'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.interfaceID = BWPersonality.GUICore.GUI_ID_ITEMCACHE
        self.filterMask = ITEM_CACHE.FILTER_WEAPON | ITEM_CACHE.FILTER_CONSUMABLE | ITEM_CACHE.FILTER_ARMOR | ITEM_CACHE.FILTER_ARMOR | ITEM_CACHE.FILTER_MISC | ITEM_CACHE.FILTER_QUEST | ITEM_CACHE.FILTER_ARTIFACT
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        sW, sH = BigWorld.screenSize()
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 390
        cmp.width = 283
        cmp.visible = False
        cmp.textureName = ''
        cmp.position = (sW - 293, 300, 0.5)

    def setupContent(self):
        itemView = soItemView(GUI.Window(), soWarehouseSlot, slot_eventsHandler=self.slotHandler, eventsHandler=self.itemViewHandler, rowWidth=4, cols=4, hScroll=False, borderWidth=0)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (5, 30, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'itemView')
        itemView.onBound()
        itemView.setRestrictingComponent(None)
        itemView.setItems(None)
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 390
        cmp.width = 283
        cmp.position = (0, 0, 0.9)
        self.component.addChild(cmp, 'iFrame')
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
        cmp.position = (257, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        filterBtn = soButton(GUI.Window())
        filterBtn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        filterBtn.buttonActive = True
        filterBtn.onClick = partial(self.filterHandler, ITEM_CACHE.FILTER_ARTIFACT)
        cmp = filterBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (252, 6, 0.3)
        filterBtn.initVSC('soGUI/visual_styles/filterArtifact.xml')
        filterBtn.onBound()
        filterBtn.setVisualState('active')
        self.component.addChild(cmp, 'filterArtifact')
        filterBtn = soButton(GUI.Window())
        filterBtn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        filterBtn.buttonActive = True
        filterBtn.onClick = partial(self.filterHandler, ITEM_CACHE.FILTER_QUEST)
        cmp = filterBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (234, 6, 0.3)
        filterBtn.initVSC('soGUI/visual_styles/filterQuest.xml')
        filterBtn.onBound()
        filterBtn.setVisualState('active')
        self.component.addChild(cmp, 'filterQuest')
        filterBtn = soButton(GUI.Window())
        filterBtn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        filterBtn.buttonActive = True
        filterBtn.onClick = partial(self.filterHandler, ITEM_CACHE.FILTER_MISC)
        cmp = filterBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (216, 6, 0.3)
        filterBtn.initVSC('soGUI/visual_styles/filterMisc.xml')
        filterBtn.onBound()
        filterBtn.setVisualState('active')
        self.component.addChild(cmp, 'filterMisc')
        filterBtn = soButton(GUI.Window())
        filterBtn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        filterBtn.buttonActive = True
        filterBtn.onClick = partial(self.filterHandler, ITEM_CACHE.FILTER_ARMOR)
        cmp = filterBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (198, 6, 0.3)
        filterBtn.initVSC('soGUI/visual_styles/filterArmor.xml')
        filterBtn.onBound()
        filterBtn.setVisualState('active')
        self.component.addChild(cmp, 'filterArmor')
        filterBtn = soButton(GUI.Window())
        filterBtn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        filterBtn.buttonActive = True
        filterBtn.onClick = partial(self.filterHandler, ITEM_CACHE.FILTER_CONSUMABLE)
        cmp = filterBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (180, 6, 0.3)
        filterBtn.initVSC('soGUI/visual_styles/filterConsumables.xml')
        filterBtn.onBound()
        filterBtn.setVisualState('active')
        self.component.addChild(cmp, 'filterConsumable')
        filterBtn = soButton(GUI.Window())
        filterBtn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        filterBtn.buttonActive = True
        filterBtn.onClick = partial(self.filterHandler, ITEM_CACHE.FILTER_WEAPON)
        cmp = filterBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (162, 6, 0.3)
        filterBtn.initVSC('soGUI/visual_styles/filterWeapons.xml')
        filterBtn.onBound()
        filterBtn.setVisualState('active')
        self.component.addChild(cmp, 'filterWeapon')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (118, 119, 103, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (205, 374, 0.3)
        cmp.text = u'100500'
        self.component.addChild(cmp, 'moneyLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (118, 119, 103, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (205, 360, 0.3)
        cmp.text = u'100'
        self.component.addChild(cmp, 'goldLabel')
        cmp = GUI.Simple('soGUI/maps/Controls/inventory/money.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 8
        cmp.width = 16
        cmp.position = (184, 375, 0.9)
        self.component.addChild(cmp, 'moneyIcon')
        cmp = GUI.Simple('soGUI/maps/Controls/inventory/gold.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 9
        cmp.width = 11
        cmp.position = (187, 361, 0.9)
        self.component.addChild(cmp, 'goldIcon')

        def cost_check(newStr, wholeText, offset):
            full_text = wholeText[0:offset] + newStr + wholeText[offset:]
            return full_text.isdigit() and len(full_text) < 10

        edit = soEditBox(GUI.Window(), width=85, height=19, font='ruRU_Cyrvetica_Extra_14i.font', hOffset=4, vOffset=2, color=(212, 169, 113, 255))
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (5, 360, 0.9)
        if BigWorld.player().isClanLeader:
            self.component.addChild(cmp, 'moneyEdit')
        edit.onBound()
        edit.setValue(u'0')
        edit.setValidator(cost_check)
        btn = soButtonWTT(GUI.Window(), 'push_money')
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.height = 9
        cmp.width = 20
        cmp.position = (100, 375, 0.9)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp.visible = 1
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = '<<'
        if BigWorld.player().isClanLeader:
            self.component.addChild(cmp, 'moneyDeposit')
        btn = soButtonWTT(GUI.Window(), 'push_gold')
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.height = 9
        cmp.width = 20
        cmp.position = (100, 361, 0.9)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp.visible = 1
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = '<<'
        if BigWorld.player().isClanLeader:
            self.component.addChild(cmp, 'goldDeposit')
        btn = soButtonWTT(GUI.Window(), 'give_money')
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.height = 9
        cmp.width = 20
        cmp.position = (130, 375, 0.9)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp.visible = 1
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = '>>'
        if BigWorld.player().isClanLeader:
            self.component.addChild(cmp, 'moneyWithdraw')
        btn = soButtonWTT(GUI.Window(), 'give_gold')
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.height = 9
        cmp.width = 20
        cmp.position = (130, 361, 0.9)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp.visible = 1
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = '>>'
        if BigWorld.player().isClanLeader:
            self.component.addChild(cmp, 'goldWithdraw')
        return

    def slotHandler(self, event, data):
        from soGUI.soInventoryScreen import soInventorySlot2
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soInventorySlot2):
                return True
            else:
                return False
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soInventorySlot2):
                BWPersonality.GUICore.itemCacheWarehouseEvent(ACTION_GIVE, data[1].itemData)
                return True
            else:
                return False
        if event == module_soItemView.SLOTEVENT_MOUSEENTER:
            if isinstance(data, soWarehouseSlot):
                BWPersonality.GUICore.toolTipEvent(data.itemData, self.interfaceID, soToolTipComponent.EVENT_SHOW)
                return True
        return False

    def itemViewHandler(self, event, data):
        from soGUI.soInventoryScreen import soInventorySlot2
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soInventorySlot2):
                return True
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soInventorySlot2):
                return True
        return False

    def _setItems(self, items):
        self.component.itemView.script.setItems(items)

    def update(self):
        items = None
        money = 0
        weight = ''
        filters = 0
        if BWPersonality.GUICore.warehouseDataSection.has_key('items'):
            items = BWPersonality.GUICore.warehouseDataSection['items']
        if BWPersonality.GUICore.warehouseDataSection.has_key('money'):
            money = [BWPersonality.GUICore.warehouseDataSection['money'], BWPersonality.GUICore.warehouseDataSection['gold']]
        if BWPersonality.GUICore.warehouseDataSection.has_key('weight'):
            weight = BWPersonality.GUICore.warehouseDataSection['weight']
        if BWPersonality.GUICore.warehouseDataSection.has_key('filters'):
            filters = BWPersonality.GUICore.warehouseDataSection['filters']
        self._setItems(items)
        self._setMoney(money)
        self._setFilterMask(filters)
        return

    def _setMoney(self, money):
        self.component.moneyLabel.text = str(money[0])
        self.component.goldLabel.text = str(money[1])

    def _setFilterMask(self, filterMask):
        self.filterMask = filterMask
        self._updateFilters()

    def filterHandler(self, filter):
        self.filterMask = self.filterMask ^ filter
        BWPersonality.GUICore.itemCacheWarehouseEvent(ITEM_CACHE.EVENT_FILTERCHANGE, self.filterMask)
        self._updateFilters()

    def _updateFilters(self):
        if self.filterMask & ITEM_CACHE.FILTER_WEAPON:
            self.component.filterWeapon.script.buttonActive = True
            self.component.filterWeapon.script._updateVisualState()
        else:
            self.component.filterWeapon.script.buttonActive = False
            self.component.filterWeapon.script._updateVisualState()
        if self.filterMask & ITEM_CACHE.FILTER_CONSUMABLE:
            self.component.filterConsumable.script.buttonActive = True
            self.component.filterConsumable.script._updateVisualState()
        else:
            self.component.filterConsumable.script.buttonActive = False
            self.component.filterConsumable.script._updateVisualState()
        if self.filterMask & ITEM_CACHE.FILTER_ARMOR:
            self.component.filterArmor.script.buttonActive = True
            self.component.filterArmor.script._updateVisualState()
        else:
            self.component.filterArmor.script.buttonActive = False
            self.component.filterArmor.script._updateVisualState()
        if self.filterMask & ITEM_CACHE.FILTER_MISC:
            self.component.filterMisc.script.buttonActive = True
            self.component.filterMisc.script._updateVisualState()
        else:
            self.component.filterMisc.script.buttonActive = False
            self.component.filterMisc.script._updateVisualState()
        if self.filterMask & ITEM_CACHE.FILTER_QUEST:
            self.component.filterQuest.script.buttonActive = True
            self.component.filterQuest.script._updateVisualState()
        else:
            self.component.filterQuest.script.buttonActive = False
            self.component.filterQuest.script._updateVisualState()
        if self.filterMask & ITEM_CACHE.FILTER_ARTIFACT:
            self.component.filterArtifact.script.buttonActive = True
            self.component.filterArtifact.script._updateVisualState()
        else:
            self.component.filterArtifact.script.buttonActive = False
            self.component.filterArtifact.script._updateVisualState()

    def show(self, objId):
        self.objId = objId
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'itemCacheWarehouse')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, self.interfaceID)
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, self.interfaceID)

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        cmp = self.component
        cmp.position = (sW - 293, 300, 0.5)

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()

    @PyGUIEvent('moneyDeposit', 'onClick')
    def onMoneyDepositBtnClick(self):
        if BigWorld.player().isClanLeader:
            BigWorld.player().moneyDeposit(self.objId, self.component.moneyEdit.script.getRaw())
            self.component.moneyEdit.script.setValue('')

    @PyGUIEvent('goldDeposit', 'onClick')
    def onGoldDepositBtnClick(self):
        if BigWorld.player().isClanLeader:
            BigWorld.player().goldDeposit(self.objId, self.component.moneyEdit.script.getRaw())
            self.component.moneyEdit.script.setValue('')

    @PyGUIEvent('moneyWithdraw', 'onClick')
    def onMoneyWithdrawBtnClick(self):
        if BigWorld.player().isClanLeader:
            BigWorld.player().moneyWithdraw(self.objId, self.component.moneyEdit.script.getRaw())
            self.component.moneyEdit.script.setValue('')

    @PyGUIEvent('goldWithdraw', 'onClick')
    def onGoldWithdrawBtnClick(self):
        if BigWorld.player().isClanLeader:
            BigWorld.player().goldWithdraw(self.objId, self.component.moneyEdit.script.getRaw())
            self.component.moneyEdit.script.setValue('')