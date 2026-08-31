# Embedded file name: scripts/client/soGUI/soInventoryScreen.py
import BigWorld
import GUI
import BWPersonality
import Helpers.PyGUI as PyGUI
from soGUI import soButton
import Helpers.Listener as Listener
import soGUI
import Keys
import Helpers.BWKeyBindings as BWKeyBindings
from Helpers.BWKeyBindings import BWKeyBindingAction
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI.DraggableComponent import DraggableComponent
from soGUI.soDraggableComponent import soDraggableComponent
import math
from Items import ItemsCatalog
import ItemsUtils
import ResMgr
import soGUI.soScrollBar as soScrollBar
from soGUI.soScrollBar import soScrollBar2
from soGUI.soContextMenuComponent import soContextMenuComponent
from Helpers.BWCoroutine import *
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soItemView import soItemView, soItemSlot
import soGUI.soItemView as module_soItemView
from soPrivateStoreGUI import soPrivateStoreSlot
from soItemCache import soItemCacheSlot
from soPackageSellGUI import soPackagePaySlot
from soQuickSlotsBar import soActionSlot
from gui_const import INVENTORY
from Localization import lc
from functools import partial
from soGUI.soToolTipComponent import soToolTipComponent
from soGUI.soUserFireCache import soUserFireCacheSlot
from soGUI.soWarehouse import soWarehouseSlot
from soGUI.soCraftGUI import soCraftGUI
from soGUI.soButton import soButton
from soGUI.data import GUIEvents

def unpackItemDict(keys, values):
    zipped = zip(keys, values)
    return dict(zipped)


class guiKeyEvent(object):

    def __init__(self, key, down, mods = None):
        self.key = key
        self.down = down
        self.modifiers = mods

    def isKeyDown(self):
        return self.down


class soInventorySlot(PyGUI.Window, DraggableComponent, soToolTipComponent):
    factoryString = 'soGUI.soInventorySlot'

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        DraggableComponent.__init__(self, True, True, False)
        soToolTipComponent.__init__(self, component, None)
        component.script = self
        self.counter = None
        self.icon = None
        self.coords = (None, None)
        self.clickTime = 0.0
        self.locked = False
        self.component.focus = True
        self.component.dragFocus = True
        self.component.crossFocus = True
        self.component.dropFocus = True
        self.component.mouseButtonFocus = True
        self.onDragging = self._onDrag
        self.onBeginDrag = self._beginDrag
        self.onEndDrag = self._endDrag
        self.parentComponent = None
        self.dragProxy = None
        self.iconWidth = 0
        self.iconHeight = 0
        self.pushed = False
        self.isDragging = False
        self.slotInfo = None
        self.interfaceID = BWPersonality.GUICore.GUI_ID_INVENTORY
        self.setupSlotTexture()
        return

    def _onDrag(self):
        pass

    def _beginDrag(self):
        self.pushed = False
        if self.component.parent is not None:
            self.parentComponent = self.component.parent
            self.component.delChild(self.icon)
            self.icon.position = (GUI.mcursor().position[0], GUI.mcursor().position[1], 0.0)
            self.icon.widthMode = self.icon.heightMode = 'PIXEL'
            self.icon.width = 64
            self.icon.height = 64
            self.icon.verticalAnchor = self.icon.horizontalAnchor = 'CENTER'
            if self.counter is not None:
                self.counter.visible = False
            if hasattr(self.component, 'itemCondition'):
                self.component.itemCondition.visible = False
            if hasattr(self.component, 'itemString'):
                self.component.itemString.visible = False
            GUI.addRoot(self.icon)
        return

    def _endDrag(self):
        pass

    def setupSlotTexture(self):
        frameCmp = GUI.Simple('soGUI/maps/Controls/inventory/cellFrame.tga')
        frameCmp.horizontalPositionMode = frameCmp.verticalPositionMode = 'CLIP'
        frameCmp.widthMode = frameCmp.heightMode = 'CLIP'
        frameCmp.horizontalAnchor = 'CENTER'
        frameCmp.verticalAnchor = 'CENTER'
        frameCmp.width = 2.0
        frameCmp.height = 2.0
        frameCmp.colour = (255, 255, 255, 255)
        frameCmp.materialFX = 'BLEND'
        frameCmp.position = (0.0, 0.0, 1.0)
        self.component.addChild(frameCmp, 'backFrame')

    def empty(self, doEmpty = False):
        if self.icon is not None:
            self.icon.textureName = ''
        if self.counter is not None:
            self.counter.text = ''
        if hasattr(self.component, 'itemCondition'):
            self.component.itemCondition.text = ''
        if hasattr(self.component, 'itemString'):
            self.component.itemString.text = ''
        self.slotInfo = None
        self.toolTipID = None
        if self.isDragging:
            event = guiKeyEvent(Keys.KEY_LEFTMOUSE, False, None)
            DraggableComponent.handleMouseButtonEvent(self, self.component, event)
        self.isDragging = False
        return False

    def lockSlot(self, doLock = True):
        self.locked = doLock
        if doLock:
            self.component.mouseButtonFocus = False
            self.component.dragFocus = False
        else:
            self.component.mouseButtonFocus = True
            self.component.dragFocus = True

    def enabled(self, doEnable = False):
        return False

    def used(self, doUse = False):
        return False

    def sold(self):
        self.component.parent.script.processSlotEvent(self.component, soInventoryScreen.ACTION_SELL)

    def given(self):
        self.component.parent.script.processSlotEvent(self.component, soInventoryScreen.ACTION_GIVEAWAY)

    def equip(self):
        self.component.parent.script.processSlotEvent(self.component, soInventoryScreen.ACTION_EQUIP)

    def modify(self):
        self.component.parent.script.processSlotEvent(self.component, soInventoryScreen.ACTION_MODIFY)

    def trade(self):
        self.component.parent.script.processSlotEvent(self.component, soInventoryScreen.ACTION_TRADE)

    def toQB(self):
        self.component.parent.script.processSlotEvent(self.component, soInventoryScreen.ACTION_TOQUICKBAR)

    def toCraft(self):
        self.component.parent.script.processSlotEvent(self.component, soInventoryScreen.ACTION_CRAFT)

    def setCounter(self, count):
        if self.counter is None and count >= 0:
            self.counter = GUI.Text('')
            self.counter.verticalAnchor = 'BOTTOM'
            self.counter.horizontalAnchor = 'LEFT'
            self.counter.font = 'ruRU_calibri_default.font'
            self.counter.position = (0.0, -0.95, 0.0)
            self.counter.horizontalPositionMode = 'CLIP'
            self.counter.verticalPositionMode = 'CLIP'
            self.counter.colour = (255, 255, 65, 255)
            self.counter.visible = True
            self.component.addChild(self.counter, 'counter')
        if count < 0:
            if self.counter is not None:
                self.counter.text = ''
        else:
            self.counter.text = str(count)
        return

    def setItemCondition(self, condition):
        if not hasattr(self.component, 'itemCondition'):
            cmp = GUI.Text('')
            cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
            cmp.materialFX = 'BLEND'
            cmp.colour = (255, 255, 255, 255)
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.horizontalAnchor = 'RIGHT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.position = (1.0, -1.0, 0.0)
            self.component.addChild(cmp, 'itemCondition')
        self.component.itemCondition.text = condition

    def setItemString(self, istr):
        if not hasattr(self.component, 'itemString'):
            cmp = GUI.Text('')
            cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
            cmp.materialFX = 'BLEND'
            cmp.colour = (255, 255, 255, 255)
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.position = (-1.0, -1.0, 0.0)
            self.component.addChild(cmp, 'itemString')
        self.component.itemString.text = istr

    def setIcon(self, icon):

        def iconData():
            self.icon.verticalAnchor = 'CENTER'
            self.icon.horizontalAnchor = 'CENTER'
            self.icon.widthMode = 'CLIP'
            self.icon.heightMode = 'CLIP'
            self.icon.horizontalPositionMode = 'CLIP'
            self.icon.verticalPositionMode = 'CLIP'
            self.icon.width = 1.0
            self.icon.height = 2.0
            self.icon.materialFX = 'BLEND'
            self.icon.position = (0.0, 0.0, 0.1)
            self.icon.colour = (255, 255, 255, 255)
            self.icon.visible = True

        if self.icon is None or self.icon.parent is None:
            self.icon = GUI.Simple('')
            iconData()
            self.component.addChild(self.icon, 'icon')
        if isinstance(icon, str):
            self.icon.textureName = icon
        elif isinstance(icon, BigWorld.PyTextureProvider):
            self.icon.texture = icon
        iconData()
        self.dragProxy = self.icon
        return

    def setCoords(self, slot, bag = 0):
        self.coords = (slot, bag)

    def setSlotInfo(self, slotInfo):
        self.slotInfo = slotInfo
        self.toolTipID = slotInfo

    def handleDropEvent(self, component, dropped):
        if dropped.script.factoryString == 'soGUI.soTradeSlot':
            dropped.script.buy()
            return True
        if dropped.script.factoryString == 'soGUI.soItemSlot':
            dropped.script.take()
            return True
        if dropped.script.factoryString == 'soGUI.soInventorySlot':
            self.component.parent.script.processSlotEvent((component, dropped), soInventoryScreen.ACTION_MOVE)
            return True
        if dropped.script.factoryString == 'soGUI.soEquipSlot':
            self.component.parent.script.processSlotEvent(dropped, soInventoryScreen.ACTION_UNEQUIP)
            dropped.script.unEquiped()
            return True
        if dropped.script.factoryString == 'soGUI.soTradeSummarySlot':
            dropped.script.toInventory()
            return True
        if dropped.script.factoryString == 'soGUI.soPartSlot':
            BWPersonality.GUICore.craftEvent(soCraftGUI.EVENT_DELITEM, dropped.script.slotInfo)
        if dropped.script.factoryString == 'soGUI.soPCTradeSlot':
            dropped.script.cancelTrade()
        return True

    def handleMouseButtonEvent(self, comp, event):
        down = event.isKeyDown()
        key = event.key
        modifiers = event.modifiers
        if down:
            self.pushed = True
        else:
            if key == Keys.KEY_LEFTMOUSE and self.pushed and not self.isDragging:
                self.onLmb(comp, key, down, modifiers)
            elif key == Keys.KEY_RIGHTMOUSE and self.pushed and not self.isDragging:
                self.onRmb(comp, key, down, modifiers)
            self.pushed = False
        if self.isDragging:
            dragHandle = DraggableComponent.handleMouseButtonEvent(self, comp, event)
            return dragHandle
        return True

    def onLmb(self, comp, key, down, modifiers):
        if modifiers & Keys.MODIFIER_ALT == Keys.MODIFIER_ALT:
            self.component.parent.script.processSlotEvent(comp, soInventoryScreen.ACTION_MODIFY)
        if BWPersonality.GUICore.repairMode:
            self.component.parent.script.processSlotEvent(comp, soInventoryScreen.ACTION_REPAIR)
        if BigWorld.time() - self.clickTime <= BWPersonality.GUICore.mouseDoubleClickSpeed:
            self.onDoubleClick()
        self.clickTime = BigWorld.time()

    def onDoubleClick(self):
        self.component.parent.script.processSlotEvent(self.component, soInventoryScreen.ACTION_USE)

    def onRmb(self, comp, key, down, modifiers):
        self.component.parent.script.processSlotEvent(comp, soInventoryScreen.ACTION_CONTEXT)

    def handleDragStartEvent(self, *args):
        event = guiKeyEvent(Keys.KEY_LEFTMOUSE, True, None)
        DraggableComponent.handleMouseButtonEvent(self, self.component, event)
        self.isDragging = True
        return True

    def handleDragStopEvent(self, *args):
        event = guiKeyEvent(Keys.KEY_LEFTMOUSE, False, None)
        DraggableComponent.handleMouseButtonEvent(self, self.component, event)
        self.isDragging = False
        return True

    def handleDragEnterEvent(self, comp, dragged):
        return True

    def handleMouseEnterEvent(self, component):
        soToolTipComponent.handleMouseEnterEvent(self, component)
        if BWPersonality.GUICore.repairMode and self.slotInfo:
            GUI.mcursor().shape = 'repair'
        return True

    def handleMouseLeaveEvent(self, component):
        soToolTipComponent.handleMouseLeaveEvent(self, component)
        GUI.mcursor().shape = 'arrow'
        return True

    @BWMemberCoroutine
    def landingCheck(self):
        yield BWWaitForPeriod(0.5)
        if self.dragProxy.parent is None:
            parentScript = self.component.parent.script
        return


from soCharacterScreen import soCharacterSlot

class soInventoryScreen(PyGUI.Window, BWKeyBindings.BWActionHandler, Listener.Listenable):
    ACTION_USE = 0
    ACTION_DROP = 1
    ACTION_MOVE = 2
    ACTION_MODIFY = 3
    ACTION_EQUIP = 4
    ACTION_UNEQUIP = 5
    ACTION_TRADE = 6
    ACTION_UNTRADE = 7
    ACTION_TOQUICKBAR = 8
    ACTION_GIVEAWAY = 9
    ACTION_CRAFT = 10
    ACTION_REPAIR = 11
    ACTION_SELL = 12
    ACTION_CONTEXT = 13
    FRAME_TEXTURE = 'soGUI/maps/Controls/window_frame/genericWindowFrame2.tga'
    FRAME_TILEW = 32
    FRAME_TILEH = 32
    TOP_SHADEH = 35
    BOTTOM_SHADEH = 35
    SLOTW = 128
    SLOTH = 64
    SCROLL_W = 16
    TOP_OFFSET = 0
    LEFT_OFFSET = 5
    slotClass = soInventorySlot
    bagNumber = 0
    FILTER_WEAPONS = 0
    FILTER_ARMORS = 1
    FILTER_AMMO = 2
    FILTER_CONSUMABLES = 3
    FILTER_ARTIFACTS = 4
    FILTER_GADGETS = 5
    FILTER_PARTS = 6
    FILTER_EXPLOSIVES = 7
    FILTER_MISC = 8
    FILTER_UNKNOWN = 9
    factoryString = 'soGUI.soInventoryScreen'

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        Listener.Listenable.__init__(self)
        self.component = component
        self.component.script = self
        self.slots = []
        self.items = None
        self.component.dropFocus = True
        BWPersonality.gpd.keyBindings.addHandler(self)
        BWKeyBindings.BWActionHandler.setupActionList(self)
        self.comp = None
        self.frameCmp = None
        self.closeBtn = None
        self.itemFiltering = {soInventoryScreen.FILTER_WEAPONS: True,
         soInventoryScreen.FILTER_ARMORS: True,
         soInventoryScreen.FILTER_AMMO: True,
         soInventoryScreen.FILTER_CONSUMABLES: True,
         soInventoryScreen.FILTER_EXPLOSIVES: True,
         soInventoryScreen.FILTER_ARTIFACTS: True,
         soInventoryScreen.FILTER_GADGETS: True,
         soInventoryScreen.FILTER_MISC: True,
         soInventoryScreen.FILTER_PARTS: True,
         soInventoryScreen.FILTER_UNKNOWN: True}
        self.itemPriorities = [soInventoryScreen.FILTER_WEAPONS,
         soInventoryScreen.FILTER_ARMORS,
         soInventoryScreen.FILTER_AMMO,
         soInventoryScreen.FILTER_CONSUMABLES,
         soInventoryScreen.FILTER_EXPLOSIVES,
         soInventoryScreen.FILTER_GADGETS,
         soInventoryScreen.FILTER_ARTIFACTS,
         soInventoryScreen.FILTER_MISC,
         soInventoryScreen.FILTER_PARTS,
         soInventoryScreen.FILTER_UNKNOWN]
        self.itemMatrix = []
        self.numRows = 5
        self.numCols = 2
        self.cursor = (0, 0)
        self.maxScroll = (0, 0)
        self.setupRoot()
        self.setupFrameCmp()
        self.setupWeight()
        self.setupMoney()
        self.setupScroll()
        self.setupFilterBtns()
        return

    def setupFilterBtns(self):
        i = 0
        for filter in [self.FILTER_MISC,
         self.FILTER_CONSUMABLES,
         self.FILTER_ARMORS,
         self.FILTER_WEAPONS]:
            btn = soButton(GUI.Window())
            cmp = btn.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'RIGHT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 20
            cmp.height = 20
            cmp.position = (1.0 - soGUI.getPixelWidth(self.component) * (20 * i + 6), 1.0 - soGUI.getPixelHeight(self.component) * 6, 0.0)
            btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
            if filter == self.FILTER_WEAPONS:
                btn.initVSC('soGUI/visual_styles/filterWeapons.xml')
            elif filter == self.FILTER_ARMORS:
                btn.initVSC('soGUI/visual_styles/filterArmor.xml')
            elif filter == self.FILTER_CONSUMABLES:
                btn.initVSC('soGUI/visual_styles/filterConsumables.xml')
            elif filter == self.FILTER_MISC:
                btn.initVSC('soGUI/visual_styles/filterMisc.xml')
            else:
                btn.initVSC('soGUI/visual_styles/filterBtn.xml')
            btn.onBound()
            self.component.addChild(btn.component, 'filter' + str(filter))
            btn.setVisualState('normal')
            btn.onClick = partial(self.toggleFilter, filter)
            i += 1

    def toggleFilter(self, filter):
        if filter == self.FILTER_WEAPONS:
            self.itemFiltering[self.FILTER_WEAPONS] = not self.itemFiltering[self.FILTER_WEAPONS]
            self.itemFiltering[self.FILTER_AMMO] = not self.itemFiltering[self.FILTER_AMMO]
            self.itemFiltering[self.FILTER_PARTS] = not self.itemFiltering[self.FILTER_PARTS]
            self.itemFiltering[self.FILTER_EXPLOSIVES] = not self.itemFiltering[self.FILTER_EXPLOSIVES]
        elif filter == self.FILTER_ARMORS:
            self.itemFiltering[self.FILTER_ARMORS] = not self.itemFiltering[self.FILTER_ARMORS]
        elif filter == self.FILTER_CONSUMABLES:
            self.itemFiltering[self.FILTER_CONSUMABLES] = not self.itemFiltering[self.FILTER_CONSUMABLES]
        elif filter == self.FILTER_MISC:
            self.itemFiltering[self.FILTER_MISC] = not self.itemFiltering[self.FILTER_MISC]
            self.itemFiltering[self.FILTER_ARTIFACTS] = not self.itemFiltering[self.FILTER_ARTIFACTS]
            self.itemFiltering[self.FILTER_GADGETS] = not self.itemFiltering[self.FILTER_GADGETS]
            self.itemFiltering[self.FILTER_UNKNOWN] = not self.itemFiltering[self.FILTER_UNKNOWN]
        self.renderInventoryItems()

    def setupMarkup(self):
        pixelW = soGUI.getPixelWidth(self.component)
        pixelH = soGUI.getPixelHeight(self.component)
        for i in xrange(self.numCols - 1):
            vLine = GUI.Simple('')
            vLine.verticalPositionMode = vLine.horizontalPositionMode = 'CLIP'
            vLine.horizontalAnchor = 'CENTER'
            vLine.verticalAnchor = 'CENTER'
            vLine.widthMode = vLine.heightMode = 'PIXEL'
            vLine.colour = (255, 255, 255, 255)
            vLine.materialFX = 'BLEND'
            vLine.width = 32
            vLine.height = self.numRows * self.SLOTH
            vLine.position = (-1.0 + pixelW * (self.LEFT_OFFSET + (i + 1) * self.SLOTW), 0.0, 0.0)
            vLine.tileHeight = 32
            vLine.tileWidth = 32
            vLine.tiled = True
            vLine.textureName = 'soGUI/maps/Controls/simple_border_vertical.tga'
            vLine.visible = True
            self.component.addChild(vLine)

        for i in xrange(self.numRows - 1):
            hLine = GUI.Simple('')
            hLine.verticalPositionMode = hLine.horizontalPositionMode = 'CLIP'
            hLine.horizontalAnchor = 'LEFT'
            hLine.verticalAnchor = 'CENTER'
            hLine.widthMode = hLine.heightMode = 'PIXEL'
            hLine.colour = (255, 255, 255, 255)
            hLine.materialFX = 'BLEND'
            hLine.width = self.SLOTW * self.numCols - 1
            hLine.height = 32
            hLine.position = (-1.0 + pixelW * self.LEFT_OFFSET, 1.0 - pixelH * (self.TOP_OFFSET + self.TOP_SHADEH + (i + 1) * self.SLOTH), 0.0)
            hLine.tileHeight = 32
            hLine.tileWidth = 32
            hLine.tiled = True
            hLine.textureName = 'soGUI/maps/Controls/simple_border.tga'
            hLine.visible = True
            self.component.addChild(hLine)

    def setupRoot(self):
        self.component.textureName = ''
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.width = self.SLOTW * self.numCols + self.LEFT_OFFSET * 2 + self.SCROLL_W
        self.component.height = self.SLOTH * self.numRows + self.TOP_SHADEH + self.BOTTOM_SHADEH + self.TOP_OFFSET * 2
        self.component.dropFocus = True
        self.component.crossFocus = True
        self.component.moveFocus = True
        self.component.position = (1.0, 0.3, 0.1)
        self.component.horizontalAnchor = 'RIGHT'
        self.component.verticalAnchor = 'TOP'
        self.component.visible = False

    def setupFrameCmp(self):
        self.frameCmp = GUI.Frame2(soInventoryScreen.FRAME_TEXTURE)
        self.frameCmp.horizontalPositionMode = self.frameCmp.verticalPositionMode = 'CLIP'
        self.frameCmp.widthMode = self.frameCmp.heightMode = 'CLIP'
        self.frameCmp.horizontalAnchor = 'CENTER'
        self.frameCmp.verticalAnchor = 'CENTER'
        self.frameCmp.visible = True
        self.frameCmp.colour = (255, 255, 255, 255)
        self.frameCmp.materialFX = 'BLEND'
        self.frameCmp.width = 2.0
        self.frameCmp.height = 2.0
        self.frameCmp.position = (0.0, 0.0, 50.0)
        self.component.addChild(self.frameCmp, 'theFrame')
        GUI.reSort()

    def bindInventory(self):
        pass

    def unbindInventory(self):
        pass

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'inventory')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def setupScroll(self):
        scroll = soScrollBar2(GUI.Window(), width=16, height=300, steps=0)
        scroll.component.verticalAnchor = 'TOP'
        scroll.component.horizontalAnchor = 'RIGHT'
        scroll.component.horizontalPositionMode = 'CLIP'
        scroll.component.verticalPositionMode = 'CLIP'
        scroll.component.position = (1.0 - soGUI.getPixelWidth(self.component) * self.LEFT_OFFSET, 1.0 - soGUI.getPixelHeight(self.component) * (self.TOP_SHADEH + self.TOP_OFFSET), 0.0)
        scroll.setVisualState('normal')
        scroll.onBound()
        self.component.addChild(scroll.component, 'vScroll')

    def setupInventory(self):
        pixelW = soGUI.getPixelWidth(self.component)
        pixelH = soGUI.getPixelHeight(self.component)
        for i in xrange(self.numRows):
            slotCol = []
            for j in xrange(self.numCols):
                slot = self.slotClass(GUI.Window())
                slot.component.horizontalPositionMode = slot.component.verticalPositionMode = 'CLIP'
                slot.component.widthMode = slot.component.heightMode = 'CLIP'
                slot.component.verticalAnchor = 'TOP'
                slot.component.horizontalAnchor = 'LEFT'
                slot.component.colour = (255, 255, 255, 255)
                slot.component.materialFX = 'BLEND'
                slot.component.textureName = ''
                slot.component.width = pixelW * self.SLOTW
                slot.component.height = pixelH * self.SLOTH
                slot.component.position = (-1.0 + pixelW * (self.LEFT_OFFSET + j * self.SLOTW), 1.0 - pixelH * (self.TOP_SHADEH + self.TOP_OFFSET + self.SLOTH * i), 0.0)
                slot.component.pixelSnap = True
                slot.setCoords(i * self.numCols + j, self.bagNumber)
                slot.iconWidth = self.SLOTW
                slot.iconHeight = self.SLOTH
                slotCol.append(slot)

            self.slots.append(slotCol)

        for i in xrange(self.numRows):
            for j in xrange(self.numCols):
                self.component.addChild(self.slots[i][j].component, 'slot' + str(i * self.numCols + j))

    def onBound(self):
        PyGUI.Window.onBound(self)
        self.setupInventory()

    def processSlotEvent(self, comp, action):
        if action == soInventoryScreen.ACTION_USE or action == soInventoryScreen.ACTION_DROP:
            BWPersonality.GUICore.inventoryEvent(action, comp.script.slotInfo)
        elif action == soInventoryScreen.ACTION_MOVE:
            self.renderInventoryItems()
            BWPersonality.GUICore.inventoryEvent(action, [comp[0].script.slotInfo, comp[1].script.slotInfo])
        elif action == soInventoryScreen.ACTION_MODIFY:
            BWPersonality.GUICore.inventoryEvent(action, ItemsUtils.GetComplexItemByID(BigWorld.player(), comp.script.slotInfo))
            self.renderInventoryItems()
        elif action == soInventoryScreen.ACTION_EQUIP:
            self.renderInventoryItems()
            BWPersonality.GUICore.inventoryEvent(action, comp.script.slotInfo)
        elif action == soInventoryScreen.ACTION_UNEQUIP:
            if comp.script.slotInfo is not None:
                BWPersonality.GUICore.inventoryEvent(action, comp.script.slotInfo)
            self.renderInventoryItems()
        elif action == soInventoryScreen.ACTION_TRADE:
            self.renderInventoryItems()
        elif action == soInventoryScreen.ACTION_TOQUICKBAR:
            self.renderInventoryItems()
        elif action == soInventoryScreen.ACTION_GIVEAWAY:
            self.renderInventoryItems()
        elif action == soInventoryScreen.ACTION_CRAFT:
            self.renderInventoryItems()
        elif action == soInventoryScreen.ACTION_REPAIR:
            BWPersonality.GUICore.inventoryEvent(action, comp.script.slotInfo)
        elif action == soInventoryScreen.ACTION_SELL:
            self.renderInventoryItems()
        elif action == soInventoryScreen.ACTION_CONTEXT:
            BWPersonality.GUICore.inventoryEvent(action, comp.script.slotInfo)
        else:
            self.renderInventoryItems()
        return

    def getComponentByCoords(self, coords):
        scrolledCoords = coords[0]
        name = 'slot' + str(coords[0])
        if hasattr(self.component, name):
            return self.component.__getattribute__(name)
        else:
            return None
            return None

    def renderInventoryItems(self):
        for i in xrange(self.numRows):
            for j in xrange(self.numCols):
                self.slots[i][j].empty(True)

        for itemIndex, item in enumerate(self.items):
            item_type = item['complexItemType']
            item_id = item['complexItemID']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            item_level = item_params['Level']
            if hasattr(self.component, 'slot' + str(itemIndex - self.cursor[1] * 2)):
                cmp = getattr(self.component, 'slot' + str(itemIndex - self.cursor[1] * 2))
                iconName = item_params['IconName']
                if BWPersonality.GUICore.iconTextures is not None:
                    if iconName not in BWPersonality.GUICore.iconTextures.failedIDs:
                        if BWPersonality.GUICore.iconTextures.has_key(iconName):
                            cmp.script.setIcon(BWPersonality.GUICore.iconTextures[iconName])
                        else:
                            cmp.script.setIcon(iconName)
                else:
                    cmp.script.setIcon(iconName)
                counterTxt = ItemsUtils.GetDisplayValue(item)
                cmp.script.setCounter(counterTxt)
                cmp.script.setSlotInfo(item_id)
                itemCondition = ItemsUtils.GetItemConditionPercentString(BigWorld.player(), ItemsUtils.GetComplexItemByID(BigWorld.player(), item_id))
                cmp.script.setItemCondition(itemCondition)
                shortName = BigWorld.player().GetItemName(item, fGetShortName=True)
                cmp.script.setItemString(shortName)
                item_lock = BigWorld.player().ItemLocked(item)
                cmp.script.lockSlot(item_lock)
                if item_lock:
                    cmp.icon.colour = (50, 50, 50, 255)
                else:
                    cmp.icon.colour = (255, 255, 255, 255)
                if hasattr(cmp, 'counter'):
                    cmp.counter.visible = True
                if hasattr(cmp, 'itemCondition'):
                    cmp.itemCondition.visible = True

        return

    def update(self):
        self.items = BWPersonality.GUICore.inventoryDataSection['items']
        self.maxScroll = (0, math.ceil(len(self.items) / float(self.numCols)) - self.numRows)
        self.component.vScroll.script.setSteps(self.maxScroll[1])
        if self.cursor[1] > int(self.maxScroll[1]):
            self.cursor = (0, int(self.maxScroll[1]))
        if self.cursor[1] < 0:
            self.cursor = (0, 0)
        self.renderInventoryItems()
        if hasattr(self.component, 'weightLabel'):
            self.component.weightLabel.text = '%.2f' % BWPersonality.GUICore.inventoryDataSection['weight'][0] + ' / ' + '%.2f' % BWPersonality.GUICore.inventoryDataSection['weight'][1]
        if hasattr(self.component, 'moneyLabel'):
            self.component.moneyLabel.text = str(BWPersonality.GUICore.inventoryDataSection['money'])

    def setupWeight(self):
        self.weightIcon = GUI.Simple('')
        self.weightIcon.verticalAnchor = 'BOTTOM'
        self.weightIcon.horizontalAnchor = 'RIGHT'
        self.weightIcon.horizontalPositionMode = 'CLIP'
        self.weightIcon.verticalPositionMode = 'CLIP'
        self.weightIcon.widthMode = 'PIXEL'
        self.weightIcon.heightMode = 'PIXEL'
        self.weightIcon.position = (1.0 - soGUI.getPixelWidth(self.component) * 105, -1.0 + soGUI.getPixelHeight(self.component) * 5, 0.0)
        self.weightIcon.width = 15
        self.weightIcon.height = 15
        self.weightIcon.textureName = 'soGUI/maps/Icons/icon_weight.tga'
        self.weightIcon.visible = True
        self.component.addChild(self.weightIcon, 'weightIcon')
        self.weightLabel = GUI.Text('value / value')
        self.weightLabel.font = 'ruRU_small.font'
        self.weightLabel.horizontalAnchor = 'LEFT'
        self.weightLabel.verticalAnchor = 'BOTTOM'
        self.weightLabel.verticalPositionMode = 'CLIP'
        self.weightLabel.horizontalPositionMode = 'CLIP'
        self.weightLabel.position = (1.0 - soGUI.getPixelWidth(self.component) * 90, -1.0 + soGUI.getPixelHeight(self.component) * 5, 0.0)
        self.weightLabel.visible = True
        self.component.addChild(self.weightLabel, 'weightLabel')

    def setupMoney(self):
        self.moneyIcon = GUI.Simple('')
        self.moneyIcon.verticalAnchor = 'BOTTOM'
        self.moneyIcon.horizontalAnchor = 'RIGHT'
        self.moneyIcon.horizontalPositionMode = 'CLIP'
        self.moneyIcon.verticalPositionMode = 'CLIP'
        self.moneyIcon.widthMode = 'PIXEL'
        self.moneyIcon.heightMode = 'PIXEL'
        self.moneyIcon.position = (1.0 - soGUI.getPixelWidth(self.component) * 105, -1.0 + soGUI.getPixelHeight(self.component) * 15, 0.0)
        self.moneyIcon.width = 15
        self.moneyIcon.height = 15
        self.moneyIcon.textureName = 'soGUI/maps/Icons/icon_money.tga'
        self.moneyIcon.visible = True
        self.component.addChild(self.moneyIcon, 'moneyIcon')
        self.moneyLabel = GUI.Text('value / value')
        self.moneyLabel.font = 'ruRU_small.font'
        self.moneyLabel.horizontalAnchor = 'LEFT'
        self.moneyLabel.verticalAnchor = 'BOTTOM'
        self.moneyLabel.verticalPositionMode = 'CLIP'
        self.moneyLabel.horizontalPositionMode = 'CLIP'
        self.moneyLabel.position = (1.0 - soGUI.getPixelWidth(self.component) * 90, -1.0 + soGUI.getPixelHeight(self.component) * 15, 0.0)
        self.moneyLabel.visible = True
        self.component.addChild(self.moneyLabel, 'moneyLabel')

    def handleMouseEvent(self, cmp, event):
        dx = event.dx
        dy = event.dy
        dz = event.dz
        position = event.cursorPosition
        if dz > 0:
            self.scrollUP()
            return True
        if dz < 0:
            self.scrollDN()
            return True
        return False

    def handleDragEnterEvent(self, comp, dragged):
        return True

    def handleDropEvent(self, component, dropped):
        self.renderInventoryItems()
        return True

    def scrollUP(self):
        if self.cursor[1] > 0:
            self.cursor = (self.cursor[0], self.cursor[1] - 1)
            self.component.vScroll.script.setValue(self.cursor[1])
        self.renderInventoryItems()

    def scrollDN(self):
        if self.cursor[1] < self.maxScroll[1]:
            self.cursor = (self.cursor[0], self.cursor[1] + 1)
            self.component.vScroll.script.setValue(self.cursor[1])
        self.renderInventoryItems()

    @PyGUIEvent('vScroll', 'scrollUp')
    def scrolledUP(self):
        self.scrollUP()

    @PyGUIEvent('vScroll', 'scrollDown')
    def scrolledDN(self):
        self.scrollDN()

    @PyGUIEvent('vScroll', 'scrollMoved')
    def scrollMoved(self, newVal):
        self.cursor = (self.cursor[0], newVal)
        self.renderInventoryItems()
        self.component.vScroll.script.setValue(newVal)


class soInventorySlot2(soItemSlot):
    factoryString = 'soGUI.soInventorySlot2'
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
        cmp = GUI.Text('+')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (120, 100, 100, 230)
        cmp.materialFX = 'BLEND'
        cmp.position = (12, 16, 0.3)
        cmp.visible = False
        self.component.addChild(cmp, 'haveAttachedParts')

    def isQustItem(self):
        item_inconstant_param = unpackItemDict(self.itemData['complexItemParametresKeys'], self.itemData['complexItemParametresValues'])
        if item_inconstant_param.has_key(ItemsCatalog.IS_QUEST_ITEM) and item_inconstant_param[ItemsCatalog.IS_QUEST_ITEM] > 0:
            return True
        result = False
        for sub_item in self.itemData['itemList']:
            params = unpackItemDict(sub_item['itemParametresKeys'], sub_item['itemParametresValues'])
            result = params.get(ItemsCatalog.INC_PERSONAL_ITEM, False) or result

        return item_inconstant_param.get(ItemsCatalog.INC_PERSONAL_ITEM, False) or result

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
            isQust = self.isQustItem()
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
            item_lock = BigWorld.player().ItemLocked(self.itemData)
            item_state = ItemsUtils.GetItemConditionPercent(BigWorld.player(), self.itemData)
            if item_state <= 0.5:
                self.component.itemBroken.visible = True
            else:
                self.component.itemBroken.visible = False
            self.component.itemName.text = friendlyName
            self.component.itemCount.text = countStr
            self.lockSlot(item_lock)
            self.component.haveAttachedParts.visible = len(self.itemData['itemList'])
            self.component.itemName.colour = (175, 166, 112, 255)
            self.component.itemColored.visible = bool(ItemsUtils.getTintID(self.itemData))
            inconstantParam = ItemsUtils.GetComplexItemInconstanParams(self.itemData)
            if inconstantParam.get(ItemsCatalog.INC_ARTEFACT_DEAD, 0):
                self.component.itemName.colour = (0, 0, 0, 255)
                self.component.itemBroken.visible = True
            if isQust:
                self.component.itemName.colour = (255, 20, 20, 255)
        else:
            self.component.itemIcon.textureName = ''
            self.component.itemName.text = ''
            self.component.itemCount.text = ''
            self.component.itemBroken.visible = False
            self.component.itemColored.visible = False
            self.component.haveAttachedParts.visible = False
            self.component.itemName.colour = (175, 166, 112, 255)
            self.lockSlot(False)
        self.dragProxy.texture = self.component.itemIcon.texture
        return

    def equipItem(self):
        BWPersonality.GUICore.inventoryEvent(INVENTORY.EVENT_EQUIP, self.itemData)

    def wannaDrop(self):
        BWPersonality.GUICore.inventoryEvent(INVENTORY.EVENT_DROP, self.itemData)

    def toActionBar(self, slotN):
        BWPersonality.GUICore.inventoryEvent(INVENTORY.EVENT_TOQUICKBAR, [self.itemData, slotN])

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


class soInventoryScreen2(PyGUIBase):
    factoryString = 'soGUI.soInventoryScreen2'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.interfaceID = BWPersonality.GUICore.GUI_ID_INVENTORY
        self.filterMask = INVENTORY.FILTER_WEAPON | INVENTORY.FILTER_CONSUMABLE | INVENTORY.FILTER_ARMOR | INVENTORY.FILTER_ARMOR | INVENTORY.FILTER_MISC | INVENTORY.FILTER_QUEST | INVENTORY.FILTER_ARTIFACT
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
        cmp.position = (sW, 300, 0.5)

    def setupContent(self):
        itemView = soItemView(GUI.Window(), soInventorySlot2, slot_eventsHandler=self.slotHandler, eventsHandler=self.itemViewHandler, rowWidth=4, cols=4, hScroll=False, borderWidth=0)
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
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (18, 6, 0.3)
        cmp.text = lc('GUI.Inventory.WINDOW_CAPTION')
        self.component.addChild(cmp, 'iLabel')
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
        filterBtn.onClick = partial(self.filterHandler, INVENTORY.FILTER_ARTIFACT)
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
        filterBtn.onClick = partial(self.filterHandler, INVENTORY.FILTER_QUEST)
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
        filterBtn.onClick = partial(self.filterHandler, INVENTORY.FILTER_MISC)
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
        filterBtn.onClick = partial(self.filterHandler, INVENTORY.FILTER_ARMOR)
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
        filterBtn.onClick = partial(self.filterHandler, INVENTORY.FILTER_CONSUMABLE)
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
        filterBtn.onClick = partial(self.filterHandler, INVENTORY.FILTER_WEAPON)
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
        cmp.position = (155, 374, 0.3)
        cmp.text = u''
        self.component.addChild(cmp, 'moneyLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (118, 119, 103, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (155, 360, 0.3)
        cmp.text = u''
        self.component.addChild(cmp, 'goldLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (118, 119, 103, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (21, 374, 0.3)
        cmp.text = u''
        self.component.addChild(cmp, 'weightLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (118, 119, 103, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (21, 360, 0.3)
        cmp.text = u''
        self.component.addChild(cmp, 'slotLabel')
        cmp = GUI.Simple('soGUI/maps/Controls/inventory/money.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 8
        cmp.width = 16
        cmp.position = (134, 375, 0.9)
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
        cmp.position = (137, 361, 0.9)
        self.component.addChild(cmp, 'goldIcon')
        cmp = GUI.Simple('soGUI/maps/Controls/inventory/weight.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 10
        cmp.width = 8
        cmp.position = (8, 375, 0.9)
        self.component.addChild(cmp, 'weightIcon')
        cmp = GUI.Simple('soGUI/maps/Controls/inventory/slots.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 10
        cmp.width = 10
        cmp.position = (8, 361, 0.9)
        self.component.addChild(cmp, 'slotsIcon')
        cmp = GUI.Simple('soGUI/maps/Controls/inventory/trashcan.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 18
        cmp.width = 15
        cmp.dropFocus = True
        cmp.mapping = ((0.0, 0.0),
         (0.0, 0.5),
         (1.0, 0.5),
         (1.0, 0.0))
        cmp.position = (259, 364, 0.9)
        cmp.script = self
        self.component.addChild(cmp, 'trashCan')
        return

    def filterHandler(self, filter):
        self.filterMask = self.filterMask ^ filter
        BWPersonality.GUICore.inventoryEvent(INVENTORY.EVENT_FILTERCHANGE, self.filterMask)
        self._updateFilters()

    def slotHandler(self, event, data):
        from soGUI import soSellSlot2, soSummarySlot2
        from soGUI import soPCTradeSlot_me
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soInventorySlot2):
                return True
            elif isinstance(data[1], soUserFireCacheSlot):
                return True
            elif isinstance(data[1], soWarehouseSlot):
                print 'soWarehouseScreen  soWarehouseSlot'
                return True
            elif isinstance(data[1], soPrivateStoreSlot):
                return True
            elif isinstance(data[1], soItemCacheSlot):
                return True
            elif isinstance(data[1], soPackagePaySlot):
                return True
            elif isinstance(data[1], soCharacterSlot):
                return True
            elif isinstance(data[1], soActionSlot):
                return True
            elif isinstance(data[1], soSellSlot2):
                return True
            elif isinstance(data[1], soSummarySlot2):
                return True
            elif isinstance(data[1], soPCTradeSlot_me):
                return True
            elif data[1].factoryString == 'soGUI.soItemSlot':
                return True
            elif data[1].factoryString == 'soGUI.soPartSlot':
                return True
            else:
                return False
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soInventorySlot2):
                BWPersonality.GUICore.inventoryEvent(INVENTORY.EVENT_MOVE, [data[0].itemData, data[1].itemData])
                return True
            elif isinstance(data[1], soPrivateStoreSlot):
                data[1].cancelSell()
                return True
            elif isinstance(data[1], soItemCacheSlot):
                data[1].take()
                return True
            elif isinstance(data[1], soUserFireCacheSlot):
                data[1].take()
                return True
            elif isinstance(data[1], soWarehouseSlot):
                print 'soWarehouseScreen  soWarehouseSlot'
                data[1].take()
                return True
            elif isinstance(data[1], soPackagePaySlot):
                data[1].cancelTrade()
                return True
            elif isinstance(data[1], soCharacterSlot):
                data[1].unequip()
                return True
            elif isinstance(data[1], soActionSlot):
                data[1].remove()
                return True
            elif isinstance(data[1], soSummarySlot2):
                if BWPersonality.GUICore.tradeGUI is not None:
                    BWPersonality.GUICore.tradeGUI.handleSummaryToInventory(data[1].itemData)
                    return True
                return False
            elif isinstance(data[1], soSellSlot2):
                data[1].wannaBuy()
                return True
            elif isinstance(data[1], soPCTradeSlot_me):
                data[1].cancelItem()
                return True
            elif data[1].factoryString == 'soGUI.soEquipSlot':
                data[1].unEquiped()
                return True
            elif data[1].factoryString == 'soGUI.soItemSlot':
                data[1].take()
                return True
            elif data[1].factoryString == 'soGUI.soTradeSummarySlot':
                data[1].toInventory()
                return True
            elif data[1].factoryString == 'soGUI.soPartSlot':
                BWPersonality.GUICore.craftEvent(soCraftGUI.EVENT_DELITEM, data[1].slotInfo)
                return True
            else:
                return False
        if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
            if isinstance(data, soInventorySlot2):
                GUI.mcursor().shape = 'arrow'
                BWPersonality.GUICore.toolTipEvent(data.itemData, self.interfaceID, soToolTipComponent.EVENT_HIDE)
                return True
        if event == module_soItemView.SLOTEVENT_MOUSEENTER:
            if isinstance(data, soInventorySlot2):
                if BWPersonality.GUICore.repairMode and data.haveItem():
                    GUI.mcursor().shape = 'repair'
                BWPersonality.GUICore.toolTipEvent(data.itemData, self.interfaceID, soToolTipComponent.EVENT_SHOW)
                return True
        if event == module_soItemView.SLOTEVENT_DBLCLICK:
            if isinstance(data, soInventorySlot2):
                BWPersonality.GUICore.inventoryEvent(INVENTORY.EVENT_ACTION, data.itemData)
                return True
        if event == module_soItemView.SLOTEVENT_RCLICK:
            if isinstance(data, soInventorySlot2):
                BWPersonality.GUICore.inventoryEvent(INVENTORY.EVENT_CONTEXT, data.itemData)
                return True
        if event == module_soItemView.SLOTEVENT_LCLICK:
            if BWPersonality.GUICore.repairMode:
                BWPersonality.GUICore.inventoryEvent(INVENTORY.EVENT_REPAIR, data.itemData)
                return True
        return False

    def itemViewHandler(self, event, data):
        from soGUI import soSellSlot2, soSummarySlot2
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soInventorySlot2):
                return True
            if data[1].factoryString == 'soGUI.soEquipSlot':
                return True
            if data[1].factoryString == 'soGUI.soItemSlot':
                return True
            if data[1].factoryString == 'soGUI.soTradeSummarySlot':
                return True
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soInventorySlot2):
                return True
            if data[1].factoryString == 'soGUI.soEquipSlot':
                data[1].unEquiped()
                return True
            if data[1].factoryString == 'soGUI.soItemSlot':
                data[1].take()
                return True
            if data[1].factoryString == 'soGUI.soTradeSummarySlot':
                data[1].toInventory()
                return True
        return False

    def _updateFilters(self):
        if self.filterMask & INVENTORY.FILTER_WEAPON:
            self.component.filterWeapon.script.buttonActive = True
            self.component.filterWeapon.script._updateVisualState()
        else:
            self.component.filterWeapon.script.buttonActive = False
            self.component.filterWeapon.script._updateVisualState()
        if self.filterMask & INVENTORY.FILTER_CONSUMABLE:
            self.component.filterConsumable.script.buttonActive = True
            self.component.filterConsumable.script._updateVisualState()
        else:
            self.component.filterConsumable.script.buttonActive = False
            self.component.filterConsumable.script._updateVisualState()
        if self.filterMask & INVENTORY.FILTER_ARMOR:
            self.component.filterArmor.script.buttonActive = True
            self.component.filterArmor.script._updateVisualState()
        else:
            self.component.filterArmor.script.buttonActive = False
            self.component.filterArmor.script._updateVisualState()
        if self.filterMask & INVENTORY.FILTER_MISC:
            self.component.filterMisc.script.buttonActive = True
            self.component.filterMisc.script._updateVisualState()
        else:
            self.component.filterMisc.script.buttonActive = False
            self.component.filterMisc.script._updateVisualState()
        if self.filterMask & INVENTORY.FILTER_QUEST:
            self.component.filterQuest.script.buttonActive = True
            self.component.filterQuest.script._updateVisualState()
        else:
            self.component.filterQuest.script.buttonActive = False
            self.component.filterQuest.script._updateVisualState()
        if self.filterMask & INVENTORY.FILTER_ARTIFACT:
            self.component.filterArtifact.script.buttonActive = True
            self.component.filterArtifact.script._updateVisualState()
        else:
            self.component.filterArtifact.script.buttonActive = False
            self.component.filterArtifact.script._updateVisualState()

    def _setItems(self, items):
        self.component.itemView.script.setItems(items)

    def _setMoney(self, money):
        self.component.moneyLabel.text = str(money[0])
        self.component.goldLabel.text = str(money[1])

    def _setWeight(self, weight):
        self.component.weightLabel.text = '%.2f' % weight[0] + ' / ' + '%.2f' % weight[1]
        self.component.slotLabel.text = str(weight[2]) + ' / ' + str(weight[3])

    def _setFilterMask(self, filterMask):
        self.filterMask = filterMask
        self._updateFilters()

    def update(self):
        items = None
        money = 0
        weight = ''
        filters = 0
        if BWPersonality.GUICore.inventoryDataSection.has_key('items'):
            items = BWPersonality.GUICore.inventoryDataSection['items']
        if BWPersonality.GUICore.inventoryDataSection.has_key('money'):
            money = BWPersonality.GUICore.inventoryDataSection['money']
        if BWPersonality.GUICore.inventoryDataSection.has_key('weight'):
            weight = BWPersonality.GUICore.inventoryDataSection['weight']
        if BWPersonality.GUICore.inventoryDataSection.has_key('filters'):
            filters = BWPersonality.GUICore.inventoryDataSection['filters']
        self._setItems(items)
        self._setMoney(money)
        self._setWeight(weight)
        self._setFilterMask(filters)
        return

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'inventory')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, self.interfaceID)
        BWPersonality.GUICore.onWindowsState(self.interfaceID, self.component)
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, self.interfaceID)
        BWPersonality.GUICore.onWindowsState(self.interfaceID, self.component)

    def handleDragEnterEvent(self, cmp, dragged):
        if cmp == self.component.trashCan and isinstance(dragged.script, soInventorySlot2):
            self.component.trashCan.mapping = ((0.0, 0.5),
             (0.0, 1.0),
             (1.0, 1.0),
             (1.0, 0.5))
            return True
        return False

    def handleDragLeaveEvent(self, cmp, dragged):
        self.component.trashCan.mapping = ((0.0, 0.0),
         (0.0, 0.5),
         (1.0, 0.5),
         (1.0, 0.0))

    def handleDropEvent(self, cmp, dropped):
        self.component.trashCan.mapping = ((0.0, 0.0),
         (0.0, 0.5),
         (1.0, 0.5),
         (1.0, 0.0))
        if cmp == self.component.trashCan and isinstance(dropped.script, soInventorySlot2):
            BWPersonality.GUICore.inventoryEvent(INVENTORY.EVENT_DELETE, dropped.script.itemData)
            return True
        return False

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        cmp = self.component
        cmp.position = (sW, 300, 0.5)

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()