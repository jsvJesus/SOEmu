# Embedded file name: scripts/client/soGUI/soTradeInterface.py
import BWPersonality
import BigWorld
import GUI
import Helpers.PyGUI as PygUI
import soGUI
from Helpers.BWCoroutine import *
from Keys import *
import Helpers.Listener as Listener
from Avatar import PlayerAvatar
from Items import ItemsCatalog
import ItemsUtils
import math
import Keys
from copy import deepcopy
from Helpers.PyGUI import PyGUIEvent
from soGUI.soInventoryScreen import soInventorySlot
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soButton import soButton, soButtonWTT, soButtonWFT
from functools import partial
from soGUI import soToolTipComponent
from soGUI.soItemView import soItemView, soItemSlot
import soGUI.soItemView as module_soItemView
from gui_const import NPC_VENDOR
from Localization import lc
import webbrowser

class soTradeSlot(soGUI.soInventorySlot):
    factoryString = 'soGUI.soTradeSlot'

    def __init__(self, component):
        soGUI.soInventorySlot.__init__(self, component)
        component.script = self
        self.component.dropFocus = False
        self.component.mouseButtonFocus = True
        self.slotInfo = None
        self.interfaceID = soGUI.soGUICore.GUI_ID_NPCTRADE
        return

    def buy(self):
        self.component.parent.script.processTradeEvent(self.component, soTradeInterface.ACTION_BUY)

    def setSlotInfo(self, slotInfo):
        soGUI.soInventorySlot.setSlotInfo(self, slotInfo)
        self.interfaceID = BWPersonality.GUICore.GUI_ID_NPCTRADE

    def onRmb(self, comp, key, down, modifiers):
        self.component.parent.script.processTradeEvent(comp, soTradeInterface.ACTION_CONTEXT)

    def onLmb(self, comp, key, down, modifiers):
        if BigWorld.time() - self.clickTime <= BWPersonality.GUICore.mouseDoubleClickSpeed:
            self.onDoubleClick()
        self.clickTime = BigWorld.time()

    def handleMouseButtonEvent(self, comp, event):
        soGUI.soInventorySlot.handleMouseButtonEvent(self, comp, event)
        if event.key == Keys.KEY_RIGHTMOUSE and event.isKeyDown():
            self.component.parent.script.processTradeEvent(comp, soTradeInterface.ACTION_CONTEXT)
            return True
        return False

    def handleDragStopEvent(self, *args):
        soGUI.soInventorySlot.handleDragStopEvent(self, args)
        self.component.parent.script.renderTradeItems()
        return True

    def onDoubleClick(self):
        self.buy()

    def returnToParent(self):
        self.component.parent.script.renderTradeItems()


class soTradeInterface(soGUI.soInventoryScreen2):
    ACTION_BUY = 0
    ACTION_SELL = 1
    ACTION_CANCELSELL = 2
    ACTION_CANCELBUY = 3
    ACTION_CONFIRM = 4
    ACTION_RESET = 5
    ACTION_MODE = 6
    ACTION_CONTEXT = 7
    factoryString = 'soGUI.soTradeInterface'
    slotClass = soTradeSlot
    bagNumber = 0
    topOffset = 5
    leftOffset = 5

    def __init__(self, component):
        soGUI.soInventoryScreen.__init__(self, component)
        component.script = self
        self.component.dropFocus = True
        self.items = None
        self.evaluator = lambda : 0
        return

    def setupRoot(self):
        soGUI.soInventoryScreen.setupRoot(self)
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalAnchor = 'LEFT'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.position = (0, 56, 0.3)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.visible = True

    def renderTradeItems(self):
        for i in xrange(self.numRows):
            for j in xrange(self.numCols):
                self.slots[i][j].empty(True)

        sortedWeapons = {}
        sortedClothes = {}
        sortedArtifacts = {}
        sortedConsumables = {}
        sortedGadgets = {}
        sortedParts = {}
        sortedAmmo = {}
        sortedExplosives = {}
        sortedMisc = {}
        sortedUnknown = {}
        itemIndex = 0
        for item in self.items:
            item_class = ItemsCatalog.GetItemClass(item)
            item_params = ItemsCatalog.GetItemParam(item)
            item_level = item_params['Level']
            if item_class == ItemsCatalog.WEAPON:
                sortedWeapons[item, item_level] = itemIndex
            elif item_class == ItemsCatalog.CLOTH:
                sortedClothes[item, item_level] = itemIndex
            elif item_class == ItemsCatalog.ARTIFACT:
                sortedArtifacts[item, item_level] = itemIndex
            elif item_class == ItemsCatalog.GADGET:
                sortedGadgets[item, item_level] = itemIndex
            elif item_class == ItemsCatalog.BUFF:
                sortedConsumables[item, item_level] = itemIndex
            elif item_class == ItemsCatalog.PART:
                sortedParts[item, item_level] = itemIndex
            elif item_class == ItemsCatalog.AMMO:
                sortedAmmo[item, item_level] = itemIndex
            elif item_class == ItemsCatalog.EXPLOSION:
                sortedExplosives[item, item_level] = itemIndex
            elif item_class == ItemsCatalog.LOOT:
                sortedMisc[item, item_level] = itemIndex
            else:
                sortedUnknown[item, item_level] = itemIndex
            itemIndex += 1

        renderList = []

        def itemComparison(itemA, itemB):
            if itemA[1] > itemB[1]:
                return 1
            if itemA[1] == itemB[1]:
                return 0
            if itemA[1] < itemB[1]:
                return -1

        for priority in self.itemPriorities:
            if priority == soGUI.soInventoryScreen.FILTER_WEAPONS:
                renderList.append(sortedWeapons)
            elif priority == soGUI.soInventoryScreen.FILTER_ARMORS:
                renderList.append(sortedClothes)
            elif priority == soGUI.soInventoryScreen.FILTER_EXPLOSIVES:
                renderList.append(sortedExplosives)
            elif priority == soGUI.soInventoryScreen.FILTER_AMMO:
                renderList.append(sortedAmmo)
            elif priority == soGUI.soInventoryScreen.FILTER_CONSUMABLES:
                renderList.append(sortedConsumables)
            elif priority == soGUI.soInventoryScreen.FILTER_ARTIFACTS:
                renderList.append(sortedArtifacts)
            elif priority == soGUI.soInventoryScreen.FILTER_GADGETS:
                renderList.append(sortedGadgets)
            elif priority == soGUI.soInventoryScreen.FILTER_MISC:
                renderList.append(sortedMisc)
            elif priority == soGUI.soInventoryScreen.FILTER_PARTS:
                renderList.append(sortedParts)
            elif priority == soGUI.soInventoryScreen.FILTER_UNKNOWN:
                renderList.append(sortedUnknown)

        itemsLine = []
        for itemDict in renderList:
            sortedItems = itemDict.keys()
            sortedItems.sort(cmp=itemComparison)
            for item in sortedItems:
                a = itemDict[item]
                itemsLine.append(a)

        self.itemMatrix = []
        for i in xrange(math.ceil(len(itemsLine) / float(self.numCols))):
            itemRow = []
            for j in xrange(self.numCols):
                if i * self.numCols + j <= len(itemsLine) - 1:
                    itemRow.append(itemsLine[i * self.numCols + j])

            self.itemMatrix.append(itemRow)

        for i in xrange(self.numRows):
            for j in xrange(self.numCols):
                if hasattr(self.component, 'slot' + str(i * self.numCols + j)):
                    cmp = self.component.__getattribute__('slot' + str(i * self.numCols + j))
                    if (self.cursor[1] + i) * self.numCols + (self.cursor[0] + j) <= len(itemsLine) - 1:
                        cmp.script.setIcon(ItemsCatalog.GetItemParam(self.items[self.itemMatrix[self.cursor[1] + i][self.cursor[0] + j]])['IconName'])
                        cmp.script.setCounter(self.evaluator(self.items[self.itemMatrix[self.cursor[1] + i][self.cursor[0] + j]]))
                        cmp.script.setSlotInfo(self.items[self.itemMatrix[self.cursor[1] + i][self.cursor[0] + j]])
                        if hasattr(cmp, 'counter'):
                            cmp.counter.visible = True
                    else:
                        cmp.script.empty(True)

    def update(self):
        trader_assortment = BWPersonality.GUICore.vendorDataSection[0]
        evaluator = BWPersonality.GUICore.vendorDataSection[1]
        self.items = trader_assortment
        self.evaluator = evaluator
        self.renderTradeItems()
        self.maxScroll = (0, len(self.itemMatrix) - self.numRows)
        self.component.vScroll.script.setSteps(self.maxScroll[1])
        if self.maxScroll[1] == 0:
            self.cursor = (0, 0)

    def processTradeEvent(self, cmp, action):
        if action == soTradeInterface.ACTION_SELL:
            BWPersonality.GUICore.tradeEvent(action, cmp.script.itemData)
        elif action == soTradeInterface.ACTION_BUY:
            BWPersonality.GUICore.tradeEvent(action, cmp.script.slotInfo)
        elif action == soTradeInterface.ACTION_CONTEXT:
            BWPersonality.GUICore.tradeEvent(action, cmp.script.slotInfo)

    def handleDropEvent(self, component, dropped):
        if dropped.script.factoryString == 'soGUI.soInventorySlot':
            dropped.script.sold()
            self.processTradeEvent(dropped, soTradeInterface.ACTION_SELL)
        if isinstance(dropped.script, soInventorySlot2):
            self.processTradeEvent(dropped, soTradeInterface.ACTION_SELL)
        if dropped.script.factoryString == 'soGUI.soTradeSummarySlot':
            dropped.script.toTrade()
        if dropped.script.factoryString == 'soGUI.soTradeSlot':
            self.renderTradeItems()
        return True

    def setupWeight(self):
        pass

    def setupMoney(self):
        pass

    def setupFilterBtns(self):
        pass

    def scrollUP(self):
        if self.cursor[1] > 0:
            self.cursor = (self.cursor[0], self.cursor[1] - 1)
            self.component.vScroll.script.setValue(self.cursor[1])
        self.renderTradeItems()

    def scrollDN(self):
        if self.cursor[1] < self.maxScroll[1]:
            self.cursor = (self.cursor[0], self.cursor[1] + 1)
            self.component.vScroll.script.setValue(self.cursor[1])
        self.renderTradeItems()

    @PyGUIEvent('vScroll', 'scrollMoved')
    def scrollMoved(self, newVal):
        self.cursor = (self.cursor[0], newVal)
        self.renderTradeItems()
        self.component.vScroll.script.setValue(newVal)


class soTradeSummarySlot(soGUI.soInventorySlot):
    factoryString = 'soGUI.soTradeSummarySlot'

    def __init__(self, component):
        soGUI.soInventorySlot.__init__(self, component)
        component.script = self
        self.onEndDrag = self._endDrag
        self.interfaceID = soGUI.soGUICore.GUI_ID_NPCTRADESUMMARY

    def setSlotInfo(self, slotInfo):
        soGUI.soInventorySlot.setSlotInfo(self, slotInfo)
        self.interfaceID = BWPersonality.GUICore.GUI_ID_NPCTRADESUMMARY

    def toInventory(self):
        if self.component.parent.script.mode == soNPCTradeGUI.MODE_SELL:
            BWPersonality.GUICore.tradeEvent(soTradeInterface.ACTION_CANCELSELL, self.slotInfo)

    def toTrade(self):
        if self.component.parent.script.mode == soNPCTradeGUI.MODE_BUY:
            BWPersonality.GUICore.tradeEvent(soTradeInterface.ACTION_CANCELBUY, self.slotInfo)

    def handleDragStopEvent(self, *args):
        handled = soGUI.soInventorySlot.handleDragStopEvent(self, *args)
        self.component.parent.script.applyItems()
        return handled

    def onDoubleClick(self):
        if self.component.parent.script.mode == soNPCTradeGUI.MODE_SELL:
            self.toInventory()
        elif self.component.parent.script.mode == soNPCTradeGUI.MODE_BUY:
            self.toTrade()

    def _endDrag(self):
        pass


class soTradeSummaryInterface(PyGUIBase):
    factoryString = 'soGUI.soTradeSummaryInterface'
    TAB_BUY = 0
    TAB_SELL = 1

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.slots = []
        self.items = []
        self.mode = soNPCTradeGUI.MODE_BUY
        self.setupRoot()
        self.setupTabs()
        self.setupSlots()
        self.setupBtns()
        self.setupOutcomeLabel()
        self.switchToTab(soTradeSummaryInterface.TAB_BUY)

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 355
        cmp.height = 468
        cmp.position = (253, 0, 0.2)
        cmp.textureName = ''
        cmp.dropFocus = True
        cmp = GUI.Window('soGUI/maps/Controls/trade/frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 355
        cmp.height = 445
        cmp.position = (0, 23, 0.9)
        self.component.addChild(cmp, 'frame')

    def setupTabs(self):
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 172
        cmp.height = 26
        cmp.position = (5, 0, 1.0)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        btn.onClick = partial(self.switchToTab, self.TAB_BUY)
        self.component.addChild(cmp, 'buyTab')
        cmp.label.text = lc('soTradeInterface.soGUI.STRING_446_19')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 172
        cmp.height = 26
        cmp.position = (179, 0, 1.0)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        btn.onClick = partial(self.switchToTab, self.TAB_SELL)
        self.component.addChild(cmp, 'sellTab')
        cmp.label.text = lc('soTradeInterface.soGUI.STRING_471_19')

    def setupSlots(self):
        for i in xrange(5):
            slotRow = []
            for j in xrange(2):
                slot = soTradeSummarySlot(GUI.Window())
                cmp = slot.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.position = (50 + j * 128, 65 + i * 64, 0.5)
                cmp.width = 128
                cmp.height = 64
                cmp.dropFocus = False
                slot.iconWidth = 128
                slot.iconHeight = 64
                slotRow.append(slot)

            self.slots.append(slotRow)

        for i in xrange(5):
            for j in xrange(2):
                self.component.addChild(self.slots[i][j].component, 'slot' + str(i * 2 + j))

    def setupBtns(self):
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 100
        cmp.height = 29
        cmp.position = (60, 432, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'confirmBtn')
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soTradeInterface.soGUI.STRING_518_19')
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 100
        cmp.height = 29
        cmp.position = (188, 432, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'resetBtn')
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soTradeInterface.soGUI.STRING_541_19')
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/closeBox.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (333, 31, 0.2)
        self.component.addChild(cmp, 'closeBox')
        btn.onBound()
        btn.setVisualState('normal')

    def setupOutcomeLabel(self):
        cmp = GUI.Text('')
        cmp.font = 'ruRU_calibri_default.font'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (177, 412, 0.6)
        cmp.colourFormatting = True
        cmp.multiline = False
        cmp.text = lc('soTradeInterface.soGUI.STRING_576_13')
        self.component.addChild(cmp, 'outcomeLbl')

    def applyItems(self):
        for i in xrange(5):
            for j in xrange(2):
                self.slots[i][j].empty(True)

        if BWPersonality.GUICore.vendorDataSection:
            self.items = BWPersonality.GUICore.vendorDataSection[2]
        else:
            return
        if self.items is None:
            return
        else:
            if self.mode == soNPCTradeGUI.MODE_SELL:
                for itemindex, item_id in enumerate(self.items):
                    item = ItemsUtils.GetComplexItemByID(BigWorld.player(), item_id)
                    item_type = item['complexItemType']
                    item_id = item['complexItemID']
                    item_class = ItemsCatalog.GetItemClass(item_type)
                    item_params = ItemsCatalog.GetItemParam(item_type)
                    item_level = item_params['Level']
                    cmp = self.component.__getattribute__('slot' + str(itemindex))
                    cmp.script.setIcon(item_params['IconName'])
                    cmp.script.setCounter(ItemsUtils.GetDisplayValue(item))
                    cmp.script.setSlotInfo(item['complexItemID'])

            elif self.mode == soNPCTradeGUI.MODE_BUY:
                for itemindex, item_type in enumerate(self.items):
                    item_class = ItemsCatalog.GetItemClass(item_type)
                    item_params = ItemsCatalog.GetItemParam(item_type)
                    item_level = item_params['Level']
                    cmp = self.component.__getattribute__('slot' + str(itemindex))
                    cmp.script.setIcon(item_params['IconName'])
                    cmp.script.setCounter(-1)
                    cmp.script.setSlotInfo(item_type)

            return

    def processTradeEvent(self, cmp, action):
        if action == soTradeInterface.ACTION_SELL:
            BWPersonality.GUICore.tradeEvent(action, cmp.script.itemData)
        elif action == soTradeInterface.ACTION_BUY:
            BWPersonality.GUICore.tradeEvent(action, cmp.script.slotInfo)

    def handleDropEvent(self, component, dropped):
        if dropped.script.factoryString == 'soGUI.soInventorySlot':
            self.processTradeEvent(dropped, soTradeInterface.ACTION_SELL)
            dropped.script.sold()
        if isinstance(dropped.script, soInventorySlot2):
            self.processTradeEvent(dropped, soTradeInterface.ACTION_SELL)
        if dropped.script.factoryString == 'soGUI.soTradeSlot':
            dropped.script.buy()
        if dropped.script.factoryString == 'soGUI.soTradeSummarySlot':
            self.applyItems()
        return True

    def handleDragEnterEvent(self, comp, dragged):
        return True

    def update(self):
        mode = BWPersonality.GUICore.vendorDataSection[3]
        self.mode = mode
        self.items = BWPersonality.GUICore.vendorDataSection[2]
        self.applyItems()
        self.component.outcomeLbl.text = lc('soTradeInterface.soGUI.STRING_653_35') + str(BWPersonality.GUICore.vendorDataSection[4])
        if mode == soNPCTradeGUI.MODE_BUY:
            self.component.buyTab.position.z = 0.5
            self.component.sellTab.position.z = 1.0
            self.component.buyTab.script.buttonActive = True
            self.component.buyTab.script.setVisualState('active')
            self.component.sellTab.script.buttonActive = False
            self.component.sellTab.script.setVisualState('normal')
        if mode == soNPCTradeGUI.MODE_SELL:
            self.component.buyTab.position.z = 1.0
            self.component.sellTab.position.z = 0.5
            self.component.sellTab.script.buttonActive = True
            self.component.sellTab.script.setVisualState('active')
            self.component.buyTab.script.buttonActive = False
            self.component.buyTab.script.setVisualState('normal')
        GUI.reSort()

    def switchToTab(self, tab):
        if tab == self.TAB_BUY:
            if tab != self.mode:
                BWPersonality.GUICore.tradeEvent(soTradeInterface.ACTION_MODE, soNPCTradeGUI.MODE_BUY)
            self.component.buyTab.script.buttonActive = True
            self.component.buyTab.script.setVisualState('active')
        if tab == self.TAB_SELL:
            if tab != self.mode:
                BWPersonality.GUICore.tradeEvent(soTradeInterface.ACTION_MODE, soNPCTradeGUI.MODE_SELL)
            self.component.sellTab.script.buttonActive = True
            self.component.sellTab.script.setVisualState('active')
        GUI.reSort()

    @PyGUIEvent('confirmBtn', 'onClick')
    def confirmBtnClicked(self):
        BWPersonality.GUICore.tradeEvent(soTradeInterface.ACTION_CONFIRM, None)
        return

    @PyGUIEvent('resetBtn', 'onClick')
    def resetBtnClicked(self):
        BWPersonality.GUICore.tradeEvent(soTradeInterface.ACTION_RESET, None)
        return

    @PyGUIEvent('closeBox', 'onClick')
    def closeBoxClicked(self):
        BWPersonality.GUICore.showTrade(False)


class soNPCTradeGUI(PyGUIBase):
    factoryString = 'soGUI.soNPCTradeGUI'
    MODE_BUY = 0
    MODE_SELL = 1
    MODE_SELL_FOR_MONEY = 2
    MODE_SELL_FOR_GOLD = 3
    MAX_TRADE_ITEM = 10

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupTrade()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 608
        cmp.height = 468
        cmp.visible = False
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'

    def setupTrade(self):
        tradeGUI = soTradeInterface(GUI.Window())
        tradeSummary = soTradeSummaryInterface(GUI.Window())
        tradeGUI.onBound()
        tradeSummary.onBound()
        self.component.addChild(tradeGUI.component, 'tradeGUI')
        self.component.addChild(tradeSummary.component, 'transitGUI')

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'NPCtrade')
        if hasattr(BWPersonality.GUICore.worldLayer, 'inventory'):
            inventory = BWPersonality.GUICore.worldLayer.inventory
            inventory.horizontalPositionMode = inventory.verticalPositionMode = 'PIXEL'
            self.component.position = inventory.position
            self.component.position.x -= 253
            self.component.position.y -= 56
        self.component.visible = True
        self.component.tradeGUI.script.cursor = (0, 0)
        self.component.tradeGUI.vScroll.script.setValue(0)
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def update(self):
        self.component.transitGUI.script.update()
        self.component.tradeGUI.script.update()


class soSellSlot2(soItemSlot):
    factoryString = 'soGUI.soSellSlot2'
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
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (5, self.SLOTHEIGHT - 18, 0.3)
        self.component.addChild(cmp, 'itemPrice')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH - 5, 5, 0.3)
        self.component.addChild(cmp, 'itemCount')

    def setContent(self, data):
        if data == self.itemData:
            return
        else:
            if data:
                self.itemData = data
            else:
                self.itemData = None
            self._applyItemData()
            return

    def _applyItemData(self):
        if self.haveItem():
            item_type = self.itemData[0]['complexItemType']
            item_id = self.itemData[0]['complexItemID']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            item_level = item_params['Level']
            item_price = self.itemData[1]
            iconName = ItemsUtils.getTextureByTint(self.itemData[0])
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
            countStr = ItemsUtils.GetDisplayValue(self.itemData[0])
            friendlyName = ItemsUtils.GetItemName(item_type, fGetShortName=True, tintItem=self.itemData[0])
            self.component.itemName.text = friendlyName
            self.component.itemCount.text = countStr
            self.component.itemPrice.text = item_price
        else:
            self.component.itemIcon.textureName = ''
            self.component.itemName.text = ''
            self.component.itemCount.text = ''
            self.component.itemPrice.text = ''
        self.dragProxy.texture = self.component.itemIcon.texture
        return

    def wannaBuy(self):
        BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_WANNABUY, self.itemData[0])

    def onDragStart(self):
        if self.haveItem():
            self.dragProxy.visible = True
            return True
        return False

    def onDragStop(self):
        self.dragProxy.visible = False
        return True


class soSummarySlot2(soItemSlot):
    factoryString = 'soGUI.soSummarySlot2'
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
        cmp = GUI.Simple('soGUI/maps/Controls/inventory/bfg_slot.tga')
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
        self.component.addChild(cmp, 'itemForGold')
        cmp = GUI.Simple('soGUI/maps/Icons/icon_item_painted.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.component.width / 5
        cmp.height = self.component.height / 5
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.component.width, cmp.height / 2, 0.7)
        cmp.visible = 0
        self.component.addChild(cmp, 'itemColored')
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
            item_state = ItemsUtils.GetItemConditionPercent(BigWorld.player(), self.itemData)
            self.component.itemColored.visible = bool(ItemsUtils.getTintID(self.itemData))
            if item_state <= 0.5:
                self.component.itemBroken.visible = True
            else:
                self.component.itemBroken.visible = False
            self.component.itemName.text = friendlyName
            self.component.itemCount.text = countStr
            self.component.itemForGold.visible = self.itemData.get('forGold', False)
        else:
            self.component.itemIcon.textureName = ''
            self.component.itemName.text = ''
            self.component.itemCount.text = ''
            self.component.itemBroken.visible = False
            self.component.itemColored.visible = False
            self.component.itemForGold.visible = False
        self.dragProxy.texture = self.component.itemIcon.texture
        return

    def onDragStart(self):
        if self.haveItem():
            self.dragProxy.visible = True
            return True
        return False

    def onDragStop(self):
        self.dragProxy.visible = False
        return True


class soTradeGUI2(PyGUIBase):
    factoryString = 'soGUI.soTradeGUI2'
    EVENT_WANNABUY = 0
    EVENT_CONTEXT = 1
    EVENT_ACTION = 2
    EVENT_CLEAR = 3
    EVENT_APPLY = 4
    EVENT_CANCEL = 5
    EVENT_FILTER = 6
    EVENT_MODE = 7
    EVENT_WANNASELL = 8
    FILTER_WEAPON = 1
    FILTER_CONSUMABLE = 2
    FILTER_ARMOR = 4
    FILTER_MISC = 8
    FILTER_ARTIFACT = 32
    FILTER_GOLD = 64
    MODE_BUY = 0
    MODE_SELL = 1
    MODE_SELL_FOR_MONEY = 2
    MODE_SELL_FOR_GOLD = 3

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.filterMask = NPC_VENDOR.FILTER_WEAPON | NPC_VENDOR.FILTER_CONSUMABLE | NPC_VENDOR.FILTER_ARMOR | NPC_VENDOR.FILTER_ARMOR | NPC_VENDOR.FILTER_MISC | NPC_VENDOR.FILTER_ARTIFACT | NPC_VENDOR.FILTER_GOLD
        self.interfaceID = BWPersonality.GUICore.GUI_ID_NPCTRADE
        self.mode = NPC_VENDOR.MODE_BUY
        self.modeSell = NPC_VENDOR.MODE_SELL_FOR_MONEY
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 348
        cmp.height = 535
        cmp.visible = False
        cmp.script.dropFocus = True
        cmp.position.z = 0.5

    def setupContent(self):
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
        self.component.addChild(cmp, 'tFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (18, 6, 0.3)
        cmp.text = lc('GUI.Vendor.WINDOW_CAPTION')
        self.component.addChild(cmp, 'tLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (174, 485, 0.3)
        cmp.text = lc('GUI.Vendor.PRICE_LABEL')
        self.component.addChild(cmp, 'cost')
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
        cmp.position = (323, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        btn = soButtonWFT(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 74
        cmp.height = 21
        cmp.position = (8, 33, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/charScreenTab.xml')
        btn.onBound()
        btn._updateVisualState()
        btn.onClick = partial(self.setSellMode, NPC_VENDOR.MODE_SELL_FOR_MONEY)
        cmp.label.text = lc('GUI.Vendor.MONEY_LABEL')
        self.component.addChild(cmp, 'moneyTab')
        btn = soButtonWFT(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 100
        cmp.height = 21
        cmp.position = (85, 33, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/charScreenTab.xml')
        btn.onBound()
        btn._updateVisualState()
        btn.onClick = partial(self.setSellMode, NPC_VENDOR.MODE_SELL_FOR_GOLD)
        cmp.label.text = lc('GUI.Vendor.GOLD_LABEL')
        self.component.addChild(cmp, 'goldTab')
        btn = soButtonWFT(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 74
        cmp.height = 21
        cmp.position = (8, 257, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/charScreenTab.xml')
        btn.onBound()
        btn.buttonActive = True
        btn._updateVisualState()
        btn.onClick = partial(self.setMode, NPC_VENDOR.MODE_BUY)
        cmp.label.text = lc('GUI.Vendor.BUY_TAB_LABEL')
        self.component.addChild(cmp, 'buyTab')
        btn = soButtonWFT(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 74
        cmp.height = 21
        cmp.position = (85, 257, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/charScreenTab.xml')
        btn.onBound()
        btn._updateVisualState()
        btn.onClick = partial(self.setMode, NPC_VENDOR.MODE_SELL)
        cmp.label.text = lc('GUI.Vendor.SELL_TAB_LABEL')
        self.component.addChild(cmp, 'sellTab')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onClick = self.toSite
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.Vendor.toSite')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 117
        cmp.height = 29
        cmp.position = (10, 502, 0.3)
        self.component.addChild(cmp, 'toSiteBtn')
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
        cmp.label.text = lc('GUI.Vendor.CONFIRM_BUTTON_LABEL')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (135, 502, 0.3)
        self.component.addChild(cmp, 'applyBtn')
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
        cmp.label.text = lc('GUI.Vendor.CLEAR_BUTTON_LABEL')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (240, 502, 0.3)
        self.component.addChild(cmp, 'cancelBtn')
        btn.onBound()
        btn.setVisualState('normal')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 342
        cmp.height = 1
        cmp.position = (3, 474, 0.8)
        self.component.addChild(cmp, 'line1')
        cmp = GUI.Frame2('soGUI/maps/Controls/CharScreen/eqDecFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 340
        cmp.height = 196
        cmp.position = (4, 57, 0.8)
        self.component.addChild(cmp, 'dFrame1')
        cmp = GUI.Frame2('soGUI/maps/Controls/CharScreen/eqDecFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 340
        cmp.height = 196
        cmp.position = (4, 277, 0.8)
        self.component.addChild(cmp, 'dFrame2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (254, 265, 0.3)
        cmp.text = u''
        self.component.addChild(cmp, 'slotUsageLabel')
        filterBtn = soButtonWTT(GUI.Window(), 'NPC_trade_filter_artifact')
        filterBtn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        filterBtn.buttonActive = True
        filterBtn.onClick = partial(self.filterHandler, NPC_VENDOR.FILTER_ARTIFACT)
        cmp = filterBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (166, 6, 0.3)
        filterBtn.initVSC('soGUI/visual_styles/filterArtifact.xml')
        filterBtn.onBound()
        filterBtn.setVisualState('active')
        self.component.addChild(cmp, 'filterArtifact')
        filterBtn = soButtonWTT(GUI.Window(), 'NPC_trade_filter_artifact')
        filterBtn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        filterBtn.buttonActive = True
        filterBtn.onClick = partial(self.filterHandler, NPC_VENDOR.FILTER_MISC)
        cmp = filterBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (184, 6, 0.3)
        filterBtn.initVSC('soGUI/visual_styles/filterMisc.xml')
        filterBtn.onBound()
        filterBtn.setVisualState('active')
        self.component.addChild(cmp, 'filterMisc')
        filterBtn = soButtonWTT(GUI.Window(), 'NPC_trade_filter_artifact')
        filterBtn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        filterBtn.buttonActive = True
        filterBtn.onClick = partial(self.filterHandler, NPC_VENDOR.FILTER_ARMOR)
        cmp = filterBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (202, 6, 0.3)
        filterBtn.initVSC('soGUI/visual_styles/filterArmor.xml')
        filterBtn.onBound()
        filterBtn.setVisualState('active')
        self.component.addChild(cmp, 'filterArmor')
        filterBtn = soButtonWTT(GUI.Window(), 'NPC_trade_filter_artifact')
        filterBtn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        filterBtn.buttonActive = True
        filterBtn.onClick = partial(self.filterHandler, NPC_VENDOR.FILTER_CONSUMABLE)
        cmp = filterBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (220, 6, 0.3)
        filterBtn.initVSC('soGUI/visual_styles/filterConsumables.xml')
        filterBtn.onBound()
        filterBtn.setVisualState('active')
        self.component.addChild(cmp, 'filterConsumable')
        filterBtn = soButtonWTT(GUI.Window(), 'NPC_trade_filter_artifact')
        filterBtn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        filterBtn.buttonActive = True
        filterBtn.onClick = partial(self.filterHandler, NPC_VENDOR.FILTER_WEAPON)
        cmp = filterBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (238, 6, 0.3)
        filterBtn.initVSC('soGUI/visual_styles/filterWeapons.xml')
        filterBtn.onBound()
        filterBtn.setVisualState('active')
        self.component.addChild(cmp, 'filterWeapon')
        itemView = soItemView(GUI.Window(), soSellSlot2, slot_eventsHandler=self._sellSlotHandler, eventsHandler=self._sellIVHandler, rowWidth=5, cols=5, rows=3, hScroll=False, borderWidth=0)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (6, 59, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'sellIV')
        itemView.onBound()
        itemView.setRestrictingComponent(None)
        itemView.setItems(None)
        itemView = soItemView(GUI.Window(), soSummarySlot2, slot_eventsHandler=self._summarySlotHandler, eventsHandler=self._summaryIVHnalder, rowWidth=5, cols=5, rows=3, hScroll=False, borderWidth=0)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (6, 279, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'summIV')
        itemView.onBound()
        itemView.setRestrictingComponent(None)
        itemView.setItems(None)
        return

    def handleDropEvent(self, cmp, dropped):
        from soGUI.soInventoryScreen import soInventorySlot2
        if isinstance(dropped.script, soInventorySlot2):
            self.setMode(NPC_VENDOR.MODE_SELL)
            BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_WANNASELL, dropped.script.itemData)
            return True
        return False

    def toSite(self):
        webbrowser.open('http://www.stalker.so/user/')

    def setSellMode(self, mode):
        self.component.moneyTab.script.buttonActive = False
        self.component.goldTab.script.buttonActive = False
        if self.modeSell != mode:
            self.modeSell = mode
            BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_SELL_MODE, self.modeSell)
        if self.modeSell == NPC_VENDOR.MODE_SELL_FOR_MONEY:
            self.component.moneyTab.script.buttonActive = True
        elif self.modeSell == NPC_VENDOR.MODE_SELL_FOR_GOLD:
            self.component.goldTab.script.buttonActive = True
        self.component.moneyTab.script._updateVisualState()
        self.component.goldTab.script._updateVisualState()

    def setMode(self, mode):
        self.component.buyTab.script.buttonActive = False
        self.component.sellTab.script.buttonActive = False
        if self.mode != mode:
            self.mode = mode
            BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_MODE, self.mode)
        if self.mode == NPC_VENDOR.MODE_BUY:
            self.component.buyTab.script.buttonActive = True
        elif self.mode == NPC_VENDOR.MODE_SELL:
            self.component.sellTab.script.buttonActive = True
        self.component.buyTab.script._updateVisualState()
        self.component.sellTab.script._updateVisualState()

    def _sellSlotHandler(self, event, data):
        if event == module_soItemView.SLOTEVENT_MOUSEENTER:
            if isinstance(data, soSellSlot2):
                if data.haveItem():
                    BWPersonality.GUICore.toolTipEvent([data.itemData[0], NPC_VENDOR.UPPER_REGION, self.mode], self.interfaceID, soToolTipComponent.EVENT_SHOW)
                return True
        if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
            if isinstance(data, soSellSlot2):
                if data.haveItem():
                    BWPersonality.GUICore.toolTipEvent([data.itemData[0], NPC_VENDOR.UPPER_REGION, self.mode], self.interfaceID, soToolTipComponent.EVENT_HIDE)
                return True
        if event == module_soItemView.SLOTEVENT_DBLCLICK:
            if isinstance(data, soSellSlot2):
                BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_ACTION, [data.itemData[0], NPC_VENDOR.UPPER_REGION, self.mode])
                return True
        if event == module_soItemView.SLOTEVENT_RCLICK:
            if isinstance(data, soSellSlot2):
                BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_CONTEXT, data.itemData[0])
                return True
        return False

    def _sellIVHandler(self, event, data):
        from soGUI.soInventoryScreen import soInventorySlot2
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soSummarySlot2) or isinstance(data[1], soInventorySlot2):
                return True
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soSummarySlot2):
                if self.mode == NPC_VENDOR.MODE_BUY:
                    BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_CANCEL, data[1].itemData)
                    return True
            if isinstance(data[1], soInventorySlot2):
                if self.mode == NPC_VENDOR.MODE_BUY:
                    self.setMode(NPC_VENDOR.MODE_SELL)
                    BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_WANNASELL, data[1].itemData)
                    return True
                if self.mode == NPC_VENDOR.MODE_SELL:
                    BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_WANNASELL, data[1].itemData)
                    return True
        return False

    def handleSummaryToInventory(self, itemData):
        if self.mode == NPC_VENDOR.MODE_SELL:
            BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_CANCEL, itemData)

    def _summarySlotHandler(self, event, data):
        if event == module_soItemView.SLOTEVENT_MOUSEENTER:
            if isinstance(data, soSummarySlot2):
                if data.haveItem():
                    BWPersonality.GUICore.toolTipEvent([data.itemData, NPC_VENDOR.LOWER_REGION, self.mode], self.interfaceID, soToolTipComponent.EVENT_SHOW)
                    return True
        if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
            if isinstance(data, soSummarySlot2):
                if data.haveItem():
                    BWPersonality.GUICore.toolTipEvent([data.itemData, NPC_VENDOR.LOWER_REGION, self.mode], self.interfaceID, soToolTipComponent.EVENT_HIDE)
                    return True
        if event == module_soItemView.SLOTEVENT_DBLCLICK:
            if isinstance(data, soSummarySlot2):
                BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_ACTION, [data.itemData, NPC_VENDOR.LOWER_REGION, self.mode])
                return True
        if event == module_soItemView.SLOTEVENT_RCLICK:
            if isinstance(data, soSummarySlot2):
                BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_CONTEXT, data.itemData)
                return True
        return False

    def _summaryIVHnalder(self, event, data):
        from soGUI.soInventoryScreen import soInventorySlot2
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soInventorySlot2) or isinstance(data[1], soSellSlot2):
                return True
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soInventorySlot2):
                if self.mode == NPC_VENDOR.MODE_BUY:
                    self.setMode(NPC_VENDOR.MODE_SELL)
                    BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_WANNASELL, data[1].itemData)
                    return True
                if self.mode == NPC_VENDOR.MODE_SELL:
                    BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_WANNASELL, data[1].itemData)
                    return True
            if isinstance(data[1], soSellSlot2):
                if self.mode == NPC_VENDOR.MODE_BUY:
                    BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_WANNABUY, data[1].itemData[0])
                    return True
                if self.mode == NPC_VENDOR.MODE_SELL:
                    self.setMode(NPC_VENDOR.MODE_BUY)
                    BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_WANNABUY, data[1].itemData[0])
                    return True
        return False

    def update(self):
        data = BWPersonality.GUICore.vendorDataSection
        if data is None:
            return
        else:
            if data.has_key('items'):
                self.component.sellIV.script.setItems(data['items'])
            if data.has_key('transit'):
                self.component.summIV.script.setItems(data['transit'])
            if data.has_key('mode'):
                self.setMode(data['mode'])
            if data.has_key('outcome'):
                self.component.cost.text = lc('GUI.Vendor.OUTCOME_LABEL') + u' ' + data['outcome']
            if data.has_key('slot_usage'):
                self.component.slotUsageLabel.text = data['slot_usage']
            if data.has_key('filters'):
                self._setFilterMask(data['filters'])
            return

    def filterHandler(self, filter):
        self.filterMask = self.filterMask ^ filter
        BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_FILTER, self.filterMask)
        self._updateFilters()

    def _setFilterMask(self, filterMask):
        self.filterMask = filterMask
        self._updateFilters()

    def _updateFilters(self):
        if self.filterMask & self.FILTER_WEAPON:
            self.component.filterWeapon.script.buttonActive = True
            self.component.filterWeapon.script._updateVisualState()
        else:
            self.component.filterWeapon.script.buttonActive = False
            self.component.filterWeapon.script._updateVisualState()
        if self.filterMask & self.FILTER_CONSUMABLE:
            self.component.filterConsumable.script.buttonActive = True
            self.component.filterConsumable.script._updateVisualState()
        else:
            self.component.filterConsumable.script.buttonActive = False
            self.component.filterConsumable.script._updateVisualState()
        if self.filterMask & self.FILTER_ARMOR:
            self.component.filterArmor.script.buttonActive = True
            self.component.filterArmor.script._updateVisualState()
        else:
            self.component.filterArmor.script.buttonActive = False
            self.component.filterArmor.script._updateVisualState()
        if self.filterMask & self.FILTER_MISC:
            self.component.filterMisc.script.buttonActive = True
            self.component.filterMisc.script._updateVisualState()
        else:
            self.component.filterMisc.script.buttonActive = False
            self.component.filterMisc.script._updateVisualState()
        if self.filterMask & self.FILTER_ARTIFACT:
            self.component.filterArtifact.script.buttonActive = True
            self.component.filterArtifact.script._updateVisualState()
        else:
            self.component.filterArtifact.script.buttonActive = False
            self.component.filterArtifact.script._updateVisualState()

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'NPCTrade')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        self.doReposition()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def doReposition(self):
        if BWPersonality.GUICore.inventoryGUI is not None:
            cmp = BWPersonality.GUICore.inventoryGUI.component
            self.component.position.x = cmp.position.x - cmp.width - 20
            self.component.position.y = cmp.position.y - (self.component.height - cmp.height)
        return

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()

    @PyGUIEvent('applyBtn', 'onClick')
    def onApply(self):
        BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_APPLY, None)
        return

    @PyGUIEvent('cancelBtn', 'onClick')
    def onClear(self):
        BWPersonality.GUICore.tradeEvent(NPC_VENDOR.EVENT_CLEAR, None)
        return