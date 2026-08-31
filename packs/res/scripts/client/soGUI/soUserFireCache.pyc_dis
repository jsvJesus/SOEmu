# Embedded file name: scripts/client/soGUI/soUserFireCache.py
import BigWorld
import BWPersonality
import GUI
import soGUI
from Helpers.PyGUI import PyGUIBase
from Localization import lc
from soGUI.soScrollBar import soScrollBar2
from soDraggableComponent import soDraggableComponent
from Keys import *
from math import ceil, floor
from Helpers.BWCoroutine import *
from soGUI.soItemView import soItemView, soItemSlot
from Items import ItemsCatalog
import ItemsUtils
from soGUI.soToolTipComponent import soToolTipComponent
from Helpers.PyGUI import PyGUIEvent
from soGUI.soButton import soButton, soButtonWTT
from soGUI.data import GUIEvents
from functools import partial
from gui_const import ITEM_CACHE
from soGUI.soCheckBox import soCheckBox

class _module_soItemView(object):
    SLOTEVENT_MOUSELEAVE = 0
    SLOTEVENT_MOUSEENTER = 1
    SLOTEVENT_MOUSEMOVE = 2
    SLOTEVENT_DRAGSTART = 3
    SLOTEVENT_DRAGSTOP = 4
    SLOTEVENT_DROP = 5
    SLOTEVENT_DRAGENTER = 6
    SLOTEVENT_DRAGLEAVE = 7
    SLOTEVENT_RCLICK = 8
    SLOTEVENT_LCLICK = 9
    SLOTEVENT_DBLCLICK = 10
    EVENT_MOUSELEAVE = 0
    EVENT_MOUSEENTER = 1
    EVENT_MOUSEMOVE = 2
    EVENT_DRAGSTART = 3
    EVENT_DRAGSTOP = 4
    EVENT_DROP = 5
    EVENT_DRAGENTER = 6
    EVENT_DRAGLEAVE = 7
    EVENT_RCLICK = 8
    EVENT_LCLICK = 9
    EVENT_DBLCLICK = 10


module_soItemView = _module_soItemView()
SLOTEVENT_MOUSELEAVE = 0
SLOTEVENT_MOUSEENTER = 1
SLOTEVENT_MOUSEMOVE = 2
SLOTEVENT_DRAGSTART = 3
SLOTEVENT_DRAGSTOP = 4
SLOTEVENT_DROP = 5
SLOTEVENT_DRAGENTER = 6
SLOTEVENT_DRAGLEAVE = 7
SLOTEVENT_RCLICK = 8
SLOTEVENT_LCLICK = 9
SLOTEVENT_DBLCLICK = 10
EVENT_MOUSELEAVE = 0
EVENT_MOUSEENTER = 1
EVENT_MOUSEMOVE = 2
EVENT_DRAGSTART = 3
EVENT_DRAGSTOP = 4
EVENT_DROP = 5
EVENT_DRAGENTER = 6
EVENT_DRAGLEAVE = 7
EVENT_RCLICK = 8
EVENT_LCLICK = 9
EVENT_DBLCLICK = 10
ACTION_TAKE = ITEM_CACHE.EVENT_TAKE
ACTION_GIVE = ITEM_CACHE.EVENT_GIVE
ACTION_FILTERCHANGE = ITEM_CACHE.EVENT_FILTERCHANGE

class soUserFireCacheSlot(soItemSlot):
    factoryString = 'soGUI.soUserFireCacheSlot'
    SLOTWIDTH = 64
    SLOTHEIGHT = 64

    def __init__(self, component, slotIndex, itemData = None, mainFire = False):
        self.mainFire = mainFire
        self.mainCell_w = 251
        self.mainCell_h = 192
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
        if self.mainFire:
            cmp.width = self.mainCell_w
            cmp.height = self.mainCell_h
        else:
            cmp.width = self.SLOTWIDTH
            cmp.height = self.SLOTHEIGHT
        cmp.dragFocus = True
        cmp.dropFocus = True
        cmp.crossFocus = True
        cmp.moveFocus = True
        cmp.mouseButtonFocus = True

    def setupContent(self):
        if self.mainFire:
            self._setupContentMain()
        else:
            self._setupContentCell()

    def _setupContentMain(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/cellFrame2.tga')
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.mainCell_w
        cmp.height = self.mainCell_h
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (1, 0, 0.9)
        self.component.addChild(cmp, 'frameFireIcon')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.mainCell_w
        cmp.height = self.mainCell_h
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.4)
        cmp.visible = 1
        cmp.texture = BigWorld.PyTextureProvider('soGUI/maps/Controls/inventory/fireplace.tga')
        self.component.addChild(cmp, 'itemfireplace')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.mainCell_w
        cmp.height = self.mainCell_h
        cmp.colour = (255, 255, 255, 128)
        cmp.materialFX = 'BLEND'
        cmp.position = (32, 0, 0.5)
        cmp.visible = False
        self.component.addChild(cmp, 'dragProxy')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (5, 0, 0.3)
        self.component.addChild(cmp, 'itemName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 5, 0.3)
        self.component.addChild(cmp, 'itemCount')

    def _setupContentCell(self):
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
        cmp.width = self.SLOTWIDTH - 8
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (4, 0, 0.4)
        cmp.visible = 0
        cmp.texture = BigWorld.PyTextureProvider('soGUI/maps/Controls/inventory/cooking.tga')
        self.component.addChild(cmp, 'itemIconFrame')
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
            friendlyName = ItemsUtils.GetItemName(item_type, fGetShortName=True)
            itemCondition = ItemsUtils.GetItemConditionPercentString(BigWorld.player(), self.itemData)
            item_lock = BigWorld.player().ItemLocked(self.itemData)
            self.component.itemName.text = friendlyName
            self.component.itemCount.text = countStr
            self.lockSlot(item_lock)
        else:
            self.component.itemIcon.textureName = ''
            self.component.itemName.text = ''
            self.component.itemCount.text = ''
            self.lockSlot(False)
        self.dragProxy.texture = self.component.itemIcon.texture
        return

    def take(self):
        BWPersonality.GUICore.itemCacheUserFireEvent(ACTION_TAKE, self.itemData)

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

    def updateSlot(self, data, cook_colour):
        if self.itemData:
            complexItemID = self.itemData['complexItemID']
            complexItemType = self.itemData['complexItemType']
            if data.has_key(complexItemID):
                cook_time, alltime = data[complexItemID]
                h = int(64 * cook_time / alltime)
                self.component.itemIconFrame.position = (4, h, 0.4)
                self.component.itemIconFrame.visible = 1
                self.component.itemIconFrame.colour = cook_colour
                return
        self.component.itemIconFrame.visible = 0

    def hideItemIconFrame(self):
        self.component.itemIconFrame.visible = 0


class soItemView2(PyGUIBase):
    factoryString = 'soGUI.soItemView2'
    SCROLL_WIDTH = 16

    def __init__(self, component, slotClass, hScroll = True, vScroll = True, slot_eventsHandler = lambda event, data: False, eventsHandler = lambda event, data: False, canDrag = False, eatDrop = True, rows = 5, cols = 2, rowWidth = 3, borderWidth = 1, hInterval = 0, vInterval = 0, dx = 0, dy = 0):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.cursor = [0, 0]
        self.maxScroll = [rowWidth - cols, 0]
        self.pressed = False
        self.lastPressed = 0
        self.dragging = False
        self.dragProxy = None
        self.items = []
        self.dx = dx
        self.dy = dy
        self.hScroll = hScroll
        self.vScroll = vScroll
        self.canDrag = canDrag
        self.eatDrop = eatDrop
        self.slotClass = slotClass
        self.borderWidth = borderWidth
        self.rows = rows
        self.cols = cols
        self.hInterval = hInterval
        self.vInterval = vInterval
        self.rowWidth = rowWidth
        self.slot_eventsHandler = slot_eventsHandler
        self.eventsHandler = eventsHandler
        self.setupRoot()
        self.setupSlots()
        self.setupScrolls()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.dragFocus = self.canDrag
        cmp.dropFocus = self.eatDrop
        cmp.moveFocus = True
        cmp.crossFocus = True

    def setupSlots(self):
        vScrollW = self.SCROLL_WIDTH if self.vScroll else 0
        hScrollW = self.SCROLL_WIDTH if self.hScroll else 0
        self.component.width = self.borderWidth * 2 + vScrollW + self.slotClass.SLOTWIDTH * self.cols + self.hInterval * (self.cols - 1)
        self.component.height = self.borderWidth * 2 + hScrollW + self.slotClass.SLOTHEIGHT * self.rows + self.vInterval * (self.rows - 1)
        self.component.width = 400
        self.component.width = 400
        for i in xrange(self.rows * self.cols):
            slot = self.slotClass(GUI.Window(), i, None)
            cmp = slot.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.position.x = self.dx + self.borderWidth + (self.slotClass.SLOTWIDTH + self.hInterval) * (i % (self.cols * 1.0))
            cmp.position.y = self.dy + self.borderWidth + (self.slotClass.SLOTHEIGHT + self.vInterval) * (i // (self.cols * 1.0))
            cmp.position.z = 0.5
            slot.slotEvent = self.slot_eventsHandler
            self.component.addChild(cmp, 'slot' + str(i))

        slot = self.slotClass(GUI.Window(), 99, None, mainFire=1)
        cmp = slot.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position.x = 0
        cmp.position.y = 0
        cmp.position.z = 0.5
        slot.slotEvent = self.slot_eventsHandler
        self.component.addChild(cmp, 'mainFireSlot')
        return

    def setupScrolls(self):
        vScrollHeight = self.component.height - self.SCROLL_WIDTH if self.hScroll else self.component.height
        vScrollHeight -= self.borderWidth * 2
        scroll = soScrollBar2(GUI.Window(), width=16, height=vScrollHeight, steps=0)
        cmp = scroll.component
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.horizontalPositionMode = 'PIXEL'
        cmp.verticalPositionMode = 'PIXEL'
        cmp.visible = self.vScroll
        cmp.position = (self.component.width - self.borderWidth, self.borderWidth, 0.1)
        scroll.setVisualState('normal')
        scroll.onBound()
        self.component.addChild(cmp, 'vScroll')
        scroll.setSteps(self.maxScroll[1])
        hScrollHeight = self.component.width - self.SCROLL_WIDTH if self.vScroll else self.component.width
        hScrollHeight -= self.borderWidth * 2
        scroll = soScrollBar2(GUI.Window(), width=16, height=hScrollHeight, steps=0, horizontal=True)
        cmp = scroll.component
        cmp.verticalAnchor = 'BOTTOM'
        cmp.horizontalAnchor = 'LEFT'
        cmp.horizontalPositionMode = 'PIXEL'
        cmp.verticalPositionMode = 'PIXEL'
        cmp.visible = self.hScroll
        cmp.position = (self.borderWidth, self.component.height - self.borderWidth, 0.1)
        scroll.setVisualState('normal')
        scroll.onBound()
        self.component.addChild(cmp, 'hScroll')
        scroll.setSteps(self.maxScroll[0])

    def _applyItems(self):
        visItemCount = self.cols * self.rows
        visibleItems = []
        unvisibleCell = []
        for i in xrange(visItemCount):
            slot = getattr(self.component, 'slot' + str(i))
            if slot.script.itemData in self.items:
                visibleItems.append(slot.script.itemData)
                continue
            slot.script.setContent(None)
            slot.script.hideItemIconFrame()
            unvisibleCell.append(slot)

        emptyIndex = 0
        for item in self.items:
            if item in visibleItems:
                continue
            if unvisibleCell:
                slot = unvisibleCell.pop(0)
                slot.script.setContent(item)

        return

    def setItems(self, data):
        if data is None:
            data = []
        self.items = data
        self._updateMaxScroll()
        self._applyItems()
        return

    def updateSlotsItems(self, data, cook_colour):
        visItemCount = self.cols * self.rows
        renderedItems = 0
        firstItemIndex = (self.maxScroll[0] + self.cols) * self.cursor[1] + self.cursor[0]
        itemIndex = firstItemIndex
        while renderedItems < visItemCount and itemIndex < len(self.items):
            row = itemIndex // (self.maxScroll[0] + self.cols)
            col = itemIndex % (self.maxScroll[0] + self.cols)
            if col >= self.cursor[0] and col < self.cursor[0] + self.cols:
                item = self.items[itemIndex]
                itemSlot = getattr(self.component, 'slot{0}'.format(renderedItems))
                itemSlot.script.updateSlot(data, cook_colour)
                renderedItems += 1
            itemIndex += 1

    def _updateMaxScroll(self):
        self.maxScroll[0] = self.rowWidth - self.cols
        self.maxScroll[1] = int(ceil(len(self.items) / float(self.rowWidth))) - self.rows
        if self.maxScroll[1] < 0:
            self.maxScroll[1] = 0
        self.component.vScroll.script.setSteps(self.maxScroll[1])
        self.component.hScroll.script.setSteps(self.maxScroll[0])
        if self.cursor[1] > self.maxScroll[1]:
            self.cursor[1] = self.maxScroll[1]

    def scrollHandler(self, event, data):
        if event == 'RIGHT':
            self.cursor[0] += 1
        elif event == 'LEFT':
            self.cursor[0] -= 1
        elif event == 'hMOVE':
            self.cursor[0] = data
        if event == 'DOWN':
            self.cursor[1] += 1
        elif event == 'UP':
            self.cursor[1] -= 1
        elif event == 'vMOVE':
            self.cursor[1] = data
        if self.cursor[0] > self.maxScroll[0]:
            self.cursor[0] = self.maxScroll[0]
        if self.cursor[0] < 0:
            self.cursor[0] = 0
        if self.cursor[1] > self.maxScroll[1]:
            self.cursor[1] = self.maxScroll[1]
        if self.cursor[1] < 0:
            self.cursor[1] = 0
        self.component.vScroll.script.setValue(self.cursor[1])
        self.component.hScroll.script.setValue(self.cursor[0])
        self._applyItems()

    def onLClick(self):
        self.eventsHandler(EVENT_LCLICK, self)

    def onRClick(self):
        self.eventsHandler(EVENT_RCLICK, self)

    def onDblClick(self):
        self.eventsHandler(EVENT_DBLCLICK, self)

    def handleMouseLeaveEvent(self, cmp):
        self.eventsHandler(EVENT_MOUSELEAVE, self)
        return True

    def handleMouseEnterEvent(self, cmp):
        self.eventsHandler(EVENT_MOUSEENTER, self)
        return True

    def handleMouseEvent(self, cmp, event):
        if event.dz:
            if event.dz < 0:
                self.scrollHandler('DOWN', None)
            else:
                self.scrollHandler('UP', None)
        data = [self, event.cursorPosition, (event.dx, event.dy, event.dz)]
        self.eventsHandler(EVENT_MOUSEMOVE, data)
        return True

    def handleDragStartEvent(self, cmp):
        self.dragging = True
        self.pressed = False
        self.eventsHandler(EVENT_DRAGSTART, self)
        return True

    def handleDragStopEvent(self, cmp):
        self.dragging = False
        self.eventsHandler(EVENT_DRAGSTOP, self)
        return True

    def handleDragEnterEvent(self, cmp, dragged):
        if dragged.script is None:
            return False
        else:
            handled = self.eventsHandler(EVENT_DRAGENTER, [self, dragged.script])
            return handled

    def handleDragLeaveEvent(self, cmp, dragged):
        if dragged.script is None:
            return False
        else:
            handled = self.eventsHandler(EVENT_DRAGLEAVE, [self, dragged.script])
            return handled

    def handleDropEvent(self, cmp, dropped):
        if dropped.script is None:
            return False
        else:
            self.eventsHandler(EVENT_DROP, [self, dropped.script])
            return True

    def handleMouseButtonEvent(self, cmp, event):
        if not event.isMouseButton():
            return False
        if event.isKeyDown():
            if event.key == KEY_LEFTMOUSE or event.key == KEY_RIGHTMOUSE:
                self.pressed = True
                if BigWorld.time() - self.lastPressed <= BWPersonality.GUICore.mouseDoubleClickSpeed:
                    self.onDblClick()
                self.lastPressed = BigWorld.time()
        if event.isKeyUp():
            if event.key == KEY_LEFTMOUSE:
                self.onLClick()
            elif event.key == KEY_RIGHTMOUSE:
                self.onRClick()
        return True

    def setRestrictingComponent(self, comp):
        for i in xrange(self.rows * self.cols):
            cmp = getattr(self.component, 'slot' + str(i))
            cmp.script.setRestrictingComponent(comp)

    @PyGUIEvent('vScroll', 'scrollUp')
    def scrolledUP(self):
        self.scrollHandler('UP', None)
        return

    @PyGUIEvent('vScroll', 'scrollDown')
    def scrolledDOWN(self):
        self.scrollHandler('DOWN', None)
        return

    @PyGUIEvent('hScroll', 'scrollLeft')
    def scrolledLEFT(self):
        self.scrollHandler('LEFT', None)
        return

    @PyGUIEvent('hScroll', 'scrollRight')
    def scrolledRIGHT(self):
        self.scrollHandler('RIGHT', None)
        return

    @PyGUIEvent('vScroll', 'scrollMoved')
    def vScrollMoved(self, newVal):
        self.scrollHandler('vMOVE', newVal)

    @PyGUIEvent('hScroll', 'scrollMoved')
    def hScrollMoved(self, newVal):
        self.scrollHandler('hMOVE', newVal)


def _blinkGEnerator():
    i = 128
    while True:
        for i in range(128, 255, 60):
            yield (i,
             0,
             0,
             255)

        for i in range(255, 128, -60):
            yield (i,
             0,
             0,
             255)


class soUserFireCacheScreen(PyGUIBase):
    factoryString = 'soGUI.soUserFireCacheScreen'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        self.objId = None
        self._hd_loop = None
        component.script = self
        self.interfaceID = BWPersonality.GUICore.GUI_ID_ITEMCACHE
        self.filterMask = 0
        self._getRedBlink = _blinkGEnerator()
        self.setupRoot()
        self.setupContent()
        return

    def setupRoot(self):
        sW, sH = BigWorld.screenSize()
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 260
        cmp.width = 450
        cmp.visible = False
        cmp.textureName = ''
        cmp.position = (sW - 299, 300, 0.5)

    def setupContent(self):
        itemView = soItemView2(GUI.Window(), soUserFireCacheSlot, slot_eventsHandler=self.slotHandler, eventsHandler=self.itemViewHandler, rowWidth=3, cols=3, hScroll=0, vScroll=0, borderWidth=0, rows=3, dx=252, dy=0)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (2, 30, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 500
        cmp.width = 500
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
        cmp.height = 260
        cmp.width = 450
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
        cmp.position = (425, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (18, 6, 0.3)
        cmp.text = u''
        self.component.addChild(cmp, 'iLabel')
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
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (0, 128, 0, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (100, 200, 0.3)
        cmp.text = u'-/-'
        cmp.visible = True
        self.component.addChild(cmp, 'lifeTimeLabel')
        cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=lc('soGUICore.soGUI.STRING_FirePlacePublAccess'), font='ruRU_Cyrvetica_Extra_14i.font', labelColour=(175, 166, 112, 255)))
        cmp = cb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (20, 230, 0.3)
        cmp.visible = 1
        cmp.script.setActive()
        self.component.addChild(cmp, 'publ_access')
        cb.onBound()
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soGUICore.soGUI.STRING_UserFire_extinguish')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (340, 226, 0.3)
        self.component.addChild(cmp, 'extinguishButton')
        btn.onBound()
        btn.setVisualState('normal')
        return

    def slotHandler(self, event, data):
        from soGUI.soInventoryScreen import soInventorySlot2
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soInventorySlot2):
                return True
            else:
                return True
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soInventorySlot2):
                BWPersonality.GUICore.itemCacheUserFireEvent(ACTION_GIVE, data[1].itemData)
                return True
            else:
                return False
        if event == module_soItemView.SLOTEVENT_MOUSEENTER:
            if isinstance(data, soUserFireCacheSlot):
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
        data = BWPersonality.GUICore.itemCacheDataUserFireSection
        if data.has_key('items'):
            items = data['items']
            self._setItems(items)
        if data.has_key('slots_string'):
            self.component.slotLabel.text = data['slots_string']
        if data.has_key('caption'):
            self.component.iLabel.text = data['caption']
        if data.has_key('filters'):
            self._setFilterMask(data['filters'])

    def _setFilterMask(self, filterMask):
        self.filterMask = 0
        self._updateFilters()

    def filterHandler(self, filter):
        self.filterMask = 0
        BWPersonality.GUICore.itemCacheUserFireEvent(ITEM_CACHE.EVENT_FILTERCHANGE, self.filterMask)
        self._updateFilters()

    def _updateFilters(self):
        pass

    def show(self, objId):
        self.objId = objId
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'userFire')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, self.interfaceID)
        self.startLoopPool()
        try:
            userfire = BigWorld.entities[self.objId]
        except KeyError as e:
            return

        if userfire.isPublicAcces:
            self.component.publ_access.script.setActive()
        else:
            self.component.publ_access.script.setInactive()
        self.component.publ_access.visible = userfire.pOwnerName == BigWorld.player().name
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, self.interfaceID)
        self.endLoopPool()

    def startLoopPool(self):
        self.endLoopPool()
        self._hd_loop = BigWorld.callback(0.2, self._loop)

    def endLoopPool(self):
        if self._hd_loop:
            BigWorld.cancelCallback(self._hd_loop)
        self._hd_loop = None
        return

    def _loop(self):
        if not self.objId:
            return
        else:
            try:
                userfire = BigWorld.entities[self.objId]
            except KeyError as e:
                self.hide()
                return

            if not userfire:
                self.hide()
                return
            if not userfire.life_time is None:
                if not userfire.max_life_time is None:
                    str_time = '%0.f/%0.f' % (userfire.life_time, userfire.max_life_time)
                    userfire.life_time and self.setTime(str_time, (0, 128, 0, 255))
                    cook_colour = (255, 255, 255, 255)
                else:
                    self.setTime(str_time, self._getRedBlink.next())
                    cook_colour = (255, 0, 0, 255)
                self.component.itemView.script.updateSlotsItems(userfire.dict_items, cook_colour)
            self.startLoopPool()
            return

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        cmp = self.component
        cmp.position = (sW - 293, 300, 0.5)

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()

    @PyGUIEvent('publ_access', 'onStateChange')
    def changePublAccess(self):
        userfire = BigWorld.entities[self.objId]
        userfire.cell.setPublicAcces(self.component.publ_access.script.isChecked())

    @PyGUIEvent('extinguishButton', 'onClick')
    def extinguish(self):
        userfire = BigWorld.entities[self.objId]
        userfire.cell.extinguish()

    def setTime(self, time_str, colour):
        self.component.lifeTimeLabel.text = time_str
        self.component.lifeTimeLabel.colour = colour