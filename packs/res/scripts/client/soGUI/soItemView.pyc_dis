# Embedded file name: scripts/client/soGUI/soItemView.py
import BigWorld
import GUI
import BWPersonality
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.PyGUI import PyGUIEvent
from functools import partial
from soGUI.soScrollBar import soScrollBar2
from soDraggableComponent import soDraggableComponent
from Keys import *
from math import ceil, floor
from Helpers.BWCoroutine import *
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

class soItemSlot(PyGUIBase, soDraggableComponent):
    factoryString = 'soGUI.soItemSlot'
    SLOTWIDTH = 0
    SLOTHEIGHT = 0

    def __init__(self, component, slotIndex, itemData = None, centerDProxy = False):
        soDraggableComponent.__init__(self, component, centerDProxy=centerDProxy)
        PyGUIBase.__init__(self, component)
        component.script = self
        self.pressed = False
        self.locked = False
        self.busy = False
        self.cache_mode = -2
        self.lastPressed = 0
        self.itemData = itemData
        self.slotIndex = slotIndex
        self.setupRoot()
        self.setupContent()

    def getCache_mode(self):
        return self.cache_mode

    def setCache_mode(self, cache_mode):
        self.cache_mode = cache_mode

    def setupRoot(self):
        return None

    def setupContent(self):
        return None

    def setContent(self, data):
        self.slotEvent(SLOTEVENT_MOUSELEAVE, self)
        if data is not None and dict(data) == self.itemData:
            return
        else:
            if data:
                self.itemData = dict(data)
            else:
                self.itemData = None
            self._applyItemData()
            return

    def slotEvent(self, event, data):
        return False

    def fini(self):
        return None

    def reset(self):
        pass

    def update(self, data):
        return None

    def _applyItemData(self):
        return None

    def haveItem(self):
        if self.itemData is None:
            return False
        else:
            return True
            return

    def lockSlot(self, doLock = True):
        self.locked = doLock

    def slotBusy(self, busy = True):
        self.busy = busy

    def onLClick(self):
        self.slotEvent(SLOTEVENT_LCLICK, self)

    def onRClick(self):
        self.slotEvent(SLOTEVENT_RCLICK, self)

    def onDblClick(self):
        self.slotEvent(SLOTEVENT_DBLCLICK, self)

    def handleMouseLeaveEvent(self, cmp):
        self.slotEvent(SLOTEVENT_MOUSELEAVE, self)
        return True

    def handleMouseEnterEvent(self, cmp):
        self.slotEvent(SLOTEVENT_MOUSEENTER, self)
        return True

    def handleMouseEvent(self, cmp, event):
        if not self.dragging:
            return False
        soDraggableComponent.handleMouseEvent(self, cmp, event)
        data = [self, event.cursorPosition, (event.dx, event.dy, event.dz)]
        self.slotEvent(SLOTEVENT_MOUSEMOVE, data)
        return True

    def handleDragStartEvent(self, cmp):
        if self.locked:
            return False
        self.pressed = False
        soDraggableComponent.handleDragStartEvent(self, cmp)
        self.slotEvent(SLOTEVENT_DRAGSTART, self)
        return True

    def handleDragStopEvent(self, cmp):
        soDraggableComponent.handleDragStopEvent(self, cmp)
        self.slotEvent(SLOTEVENT_DRAGSTOP, self)
        return True

    def handleDragEnterEvent(self, cmp, dragged):
        if dragged.script is None:
            return False
        else:
            handled = self.slotEvent(SLOTEVENT_DRAGENTER, [self, dragged.script])
            return handled

    def handleDragLeaveEvent(self, cmp, dragged):
        if dragged.script is None:
            return False
        else:
            handled = self.slotEvent(SLOTEVENT_DRAGLEAVE, [self, dragged.script])
            return handled

    def handleDropEvent(self, cmp, dropped):
        if dropped.script is None:
            return False
        else:
            self.slotEvent(SLOTEVENT_DROP, [self, dropped.script])
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
        if event.isKeyUp() and self.pressed:
            if event.key == KEY_LEFTMOUSE:
                self.onLClick()
            elif event.key == KEY_RIGHTMOUSE:
                self.onRClick()
        return True


class soItemView(PyGUIBase):
    factoryString = 'soGUI.soItemView'
    SCROLL_WIDTH = 16

    def __init__(self, component, slotClass, hScroll = True, vScroll = True, slot_eventsHandler = lambda event, data: False, eventsHandler = lambda event, data: False, canDrag = False, eatDrop = True, rows = 5, cols = 2, rowWidth = 3, borderWidth = 1, hInterval = 0, vInterval = 0):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.cursor = [0, 0]
        self.maxScroll = [rowWidth - cols, 0]
        self.pressed = False
        self.lastPressed = 0
        self.dragging = False
        self.dragProxy = None
        self.items = []
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
        for i in xrange(self.rows * self.cols):
            slot = self.slotClass(GUI.Window(), i, None)
            cmp = slot.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.position.x = self.borderWidth + (self.slotClass.SLOTWIDTH + self.hInterval) * (i % (self.cols * 1.0))
            cmp.position.y = self.borderWidth + (self.slotClass.SLOTHEIGHT + self.vInterval) * (i // (self.cols * 1.0))
            cmp.position.z = 0.5
            slot.slotEvent = self.slot_eventsHandler
            self.component.addChild(cmp, 'slot' + str(i))

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

    def setCacheMode(self, cache_mode):
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
                itemSlot.script.setCache_mode(cache_mode)
                renderedItems += 1
            itemIndex += 1

    def _applyItems(self):
        visItemCount = self.cols * self.rows
        for i in xrange(visItemCount):
            slot = getattr(self.component, 'slot' + str(i))
            slot.script.setContent(None)

        renderedItems = 0
        firstItemIndex = (self.maxScroll[0] + self.cols) * self.cursor[1] + self.cursor[0]
        itemIndex = firstItemIndex
        while renderedItems < visItemCount and itemIndex < len(self.items):
            row = itemIndex // (self.maxScroll[0] + self.cols)
            col = itemIndex % (self.maxScroll[0] + self.cols)
            if col >= self.cursor[0] and col < self.cursor[0] + self.cols:
                item = self.items[itemIndex]
                itemSlot = getattr(self.component, 'slot{0}'.format(renderedItems))
                itemSlot.script.setContent(item)
                renderedItems += 1
            itemIndex += 1

        return

    def setItems(self, data, StoredItemsInShop = None):
        if data is None:
            data = []
        self.items = data
        self._updateMaxScroll()
        self._applyItems()
        return

    def updateSlotsItems(self, data):
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
                itemSlot.script.updateSlot(data)
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