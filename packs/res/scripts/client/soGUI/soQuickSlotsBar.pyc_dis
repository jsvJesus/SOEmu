# Embedded file name: scripts/client/soGUI/soQuickSlotsBar.py
from Helpers.BWCoroutine import *
from Helpers.BWKeyBindings import BWKeyBindingAction
from Helpers.PyGUI.DraggableComponent import DraggableComponent
from Items import ItemsCatalog
from functools import partial
from soGUI.soButton import soButton
import soGUI
import BigWorld
import GUI
import Helpers.BWKeyBindings as BWKeyBindings
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI import PyGUIBase
import ItemsUtils
import Keys
import BWPersonality
from soGUI.soToolTipComponent import soToolTipComponent
from soGUI.soItemView import soItemView, soItemSlot
import soGUI.soItemView as module_soItemView
from Helpers.PyGUI import PyGUIEvent

class guiKeyEvent(object):

    def __init__(self, key, down, mods = None):
        self.key = key
        self.down = down
        self.modifiers = mods

    def isKeyDown(self):
        return self.down


class soQuickSlot(soButton, DraggableComponent):
    factoryString = 'soGUI.soQuickSlot'

    def __init__(self, component, slotN):
        soButton.__init__(self, component)
        DraggableComponent.__init__(self, True, True, False)
        component.script = self
        self.component.focus = True
        self.component.dropFocus = True
        self.component.dragFocus = True
        self.component.crossFocus = True
        self.component.moveFocus = True
        self.onBeginDrag = self._beginDrag
        self.onEndDrag = self._endDrag
        self.parentComponent = None
        self.isDragging = False
        self.bindLabel = None
        self.quantityLabel = None
        self.slotNumber = slotN
        self.setupRoot()
        self.setupLabels()
        return

    def _beginDrag(self):
        self.pushed = False
        if self.component.parent is not None:
            self.parentComponent = self.component.parent
            self.component.delChild(self.myGlyph)
            self.myGlyph.position = (GUI.mcursor().position[0], GUI.mcursor().position[1], 0.0)
            self.myGlyph.widthMode = self.myGlyph.heightMode = 'PIXEL'
            self.myGlyph.width = 64
            self.myGlyph.height = 64
            self.myGlyph.verticalAnchor = self.myGlyph.horizontalAnchor = 'CENTER'
            GUI.addRoot(self.myGlyph)
        return

    def _endDrag(self):
        self.landingCheck().run()

    def setupRoot(self):
        soButton.initVSC(self, 'soGUI/visual_styles/defaultBtnEmpty.xml')
        self.dragProxy = self.myGlyph

    def setupLabels(self):
        self.bindLabel = GUI.Text(str(self.slotNumber + 3))
        cmp = self.bindLabel
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_small.font'
        cmp.colour = (255, 125, 125, 255)
        cmp.position = (5, 5, 0.1)
        self.component.addChild(cmp, 'bindLabel')
        self.quantityLabel = GUI.Text('')
        cmp = self.quantityLabel
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_small.font'
        cmp.colour = (255, 125, 125, 255)
        cmp.position = (38, 49, 0.1)
        self.component.addChild(cmp, 'quantityLabel')

    def setQuantity(self, number):
        if number >= 0:
            self.quantityLabel.text = str(number)
        else:
            self.quantityLabel.text = ''

    def handleMouseButtonEvent(self, comp, event):
        if self.isDragging:
            dragHandle = DraggableComponent.handleMouseButtonEvent(self, comp, event)
            return dragHandle
        soButton.handleMouseButtonEvent(self, comp, event)
        return True

    def handleDropEvent(self, component, dropped):
        if dropped.script.factoryString == 'soGUI.soInventorySlot':
            dropped.script.toQB()
            self.parentComponent.script.addToQB(dropped.script.slotInfo, self.slotNumber)
            return True
        if isinstance(dropped.script, soInventorySlot2):
            self.parentComponent.script.addToQB(dropped.script.itemData, self.slotNumber)
            return True
        return False

    def handleDragStartEvent(self, arg):
        event = guiKeyEvent(Keys.KEY_LEFTMOUSE, True, None)
        DraggableComponent.handleMouseButtonEvent(self, self.component, event)
        self.isDragging = True
        return True

    def handleDragStopEvent(self, arg):
        event = guiKeyEvent(Keys.KEY_LEFTMOUSE, False, None)
        DraggableComponent.handleMouseButtonEvent(self, self.component, event)
        self.isDragging = False
        return True

    def handleDragEnterEvent(self, comp, dragged):
        return True

    @BWMemberCoroutine
    def landingCheck(self):
        yield BWWaitForPeriod(0.5)
        if self.dragProxy.parent is None:
            GUI.delRoot(self.myGlyph)
            self.parentComponent.script.renderItems()
            self.parentComponent.script.delFromQB(self.slotNumber)
        return


class soQuickSlotsBar(PyGUI.PyGUIBase, BWKeyBindings.BWActionHandler):
    factoryString = 'soGUI.soQuickSlotsBar'
    numSlots = 8
    EVENT_ADD = 1
    EVENT_DELETE = 2
    EVENT_ACTIVATE = 3

    def __init__(self, component):
        PyGUI.PyGUIBase.__init__(self, component)
        BWPersonality.gpd.keyBindings.addHandler(self)
        BWKeyBindings.BWActionHandler.setupActionList(self)
        component.script = self
        self.setupRoot()
        self.setupItemSlots()

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 269
        cmp.height = 72
        cmp.position = (1.0, -1.0, 0.1)
        cmp.textureName = ''
        cmp.dropFocus = True
        frameTexture = GUI.Frame2('')
        cmp = frameTexture
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 269
        cmp.height = 72
        cmp.position = (0.0, 0.0, 1.0)
        self.component.addChild(cmp, 'frameTexture')

    def setupItemSlots(self):
        for i in xrange(self.numSlots):
            slot = soQuickSlot(GUI.Window(), i)
            cmp = slot.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 64
            cmp.height = 64
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (4.0 + i * 64, 4.0, 0.2)
            cmp.textureName = ''
            self.component.addChild(cmp, 'slot' + str(i))
            slot.myGlyph.textureName = ''
            slot.buttonDisabled = False
            slot.setVisualState('normal')
            slot.onBound()
            slot.onClick = partial(self.onSlot, i)
            slot.parentComponent = self.component

    def renderItems(self):
        for i in xrange(self.numSlots):
            item = BWPersonality.GUICore.quickSlotsDataSection[i]
            item_type = None
            item_id = None
            item_class = None
            item_params = None
            item_level = None
            if item is not None:
                item_type = item['complexItemType']
                item_id = item['complexItemID']
                item_class = ItemsCatalog.GetItemClass(item_type)
                item_params = ItemsCatalog.GetItemParam(item_type)
                item_level = item_params['Level']
            slot = self.component.__getattribute__('slot' + str(i))
            if item is not None:
                iconName = ItemsUtils.getTextureByTint(item)
                if not iconName:
                    iconName = ItemsCatalog.GetItemParam(item_type)['IconName']
                slot.script.myGlyph.textureName = iconName
                n = ItemsUtils.GetDisplayValue(item)
                if n >= 0:
                    slot.script.setQuantity(n)
            else:
                slot.script.myGlyph.textureName = ''
                slot.script.setQuantity(-1)
            slot.script.myGlyph.horizontalPositionMode = 'CLIP'
            slot.script.myGlyph.verticalPositionMode = 'CLIP'
            slot.script.myGlyph.horizontalAnchor = 'CENTER'
            slot.script.myGlyph.verticalAnchor = 'CENTER'
            slot.script.myGlyph.widthMode = 'CLIP'
            slot.script.myGlyph.heightMode = 'CLIP'
            slot.script.myGlyph.width = 2.0
            slot.script.myGlyph.height = 2.0
            slot.script.myGlyph.colour = (255.0, 255.0, 255.0, 255.0)
            slot.script.myGlyph.visible = True
            slot.script.myGlyph.position = (0.0, 0.0, 0.2)
            slot.script.myGlyph.materialFX = 'BLEND'
            if not hasattr(slot, 'glyph'):
                slot.addChild(slot.script.myGlyph, 'glyph')

        return

    def addToQB(self, id, slotN):
        BWPersonality.GUICore.quickBarEvent(self.EVENT_ADD, (slotN, id))

    def delFromQB(self, slotN):
        BWPersonality.GUICore.quickBarEvent(self.EVENT_DELETE, (slotN, None))
        return

    def useQBSlot(self, slotN):
        BWPersonality.GUICore.quickBarEvent(self.EVENT_ACTIVATE, (slotN, None))
        return

    def update(self):
        self.renderItems()

    def onSlot(self, number):
        self.useQBSlot(number)

    @BWKeyBindingAction('QB_Slot0', 0)
    @BWKeyBindingAction('QB_Slot1', 1)
    @BWKeyBindingAction('QB_Slot2', 2)
    @BWKeyBindingAction('QB_Slot3', 3)
    @BWKeyBindingAction('QB_Slot4', 4)
    @BWKeyBindingAction('QB_Slot5', 5)
    @BWKeyBindingAction('QB_Slot6', 6)
    @BWKeyBindingAction('QB_Slot7', 7)
    def quickSlotKey(self, slot, isDown = True):
        if isDown:
            self.onSlot(slot)


class soActionSlot(soItemSlot):
    factoryString = 'soGUI.soActionSlot'
    SLOTWIDTH = 64
    SLOTHEIGHT = 79
    SLOTFRAME_TEXTURE_NORMAL = BigWorld.PyTextureProvider('soGUI/maps/Controls/ActionBar/cellFrame.tga')
    SLOTFRAME_TEXTURE_HOVER = BigWorld.PyTextureProvider('soGUI/maps/Controls/ActionBar/cellFrameHover.tga')

    def __init__(self, component, slotIndex, itemData = None):
        soItemSlot.__init__(self, component, slotIndex, centerDProxy=True)
        component.script = self
        self.dragProxy = self.component.dragProxy
        self.proxyHolder = self.component
        self.proxyName = 'dragProxy'
        self._onDragStart = self.onDragStart
        self._onDragStop = self.onDragStop

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.dragFocus = True
        cmp.dropFocus = True
        cmp.crossFocus = True
        cmp.moveFocus = True
        cmp.mouseButtonFocus = True

    def setupContent(self):
        cmp = GUI.Simple('')
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.9)
        cmp.texture = self.SLOTFRAME_TEXTURE_NORMAL
        self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = 64
        cmp.colour = (255, 255, 255, 128)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, self.SLOTHEIGHT, 0.5)
        cmp.visible = False
        self.component.addChild(cmp, 'dragProxy')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = 64
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, self.SLOTHEIGHT, 0.4)
        self.component.addChild(cmp, 'itemIcon')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH - 3, self.SLOTHEIGHT - 3, 0.3)
        self.component.addChild(cmp, 'itemCount')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH / 2, 7, 0.3)
        self.component.addChild(cmp, 'itemKey')

    def _applyItemData(self):
        if self.haveItem():
            item_icon = self.itemData['icon']
            item_count = self.itemData['low_right_number']
            item_key = self.itemData['abovetext']
            if BWPersonality.GUICore.iconTextures is not None:
                if item_icon not in BWPersonality.GUICore.iconTextures.failedIDs:
                    if BWPersonality.GUICore.iconTextures.has_key(item_icon):
                        self.component.itemIcon.texture = BWPersonality.GUICore.iconTextures[item_icon]
                    else:
                        self.component.itemIcon.textureName = item_icon
            else:
                self.component.itemIcon.textureName = item_icon
            self.component.itemCount.text = item_count
            self.component.itemKey.text = item_key
        else:
            self.component.itemIcon.textureName = ''
            self.component.itemCount.text = u''
            self.component.itemKey.text = u''
            self.lockSlot(False)
        self.dragProxy.texture = self.component.itemIcon.texture
        return

    def remove(self):
        BWPersonality.GUICore.actionBarEvent(soActionBar.EVENT_REMOVE, self.slotIndex)

    def isEmptyItem(self):
        if self.itemData['icon'] == u'':
            return True
        else:
            return False

    def handleDragStartEvent(self, cmp):
        if self.isEmptyItem():
            return False
        handled = soItemSlot.handleDragStartEvent(self, cmp)
        return handled

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

    def handleMouseLeaveEvent(self, cmp):
        handled = soItemSlot.handleMouseLeaveEvent(self, cmp)
        self.component.frameCmp.texture = self.SLOTFRAME_TEXTURE_NORMAL
        return handled

    def handleMouseEnterEvent(self, cmp):
        handled = soItemSlot.handleMouseEnterEvent(self, cmp)
        self.component.frameCmp.texture = self.SLOTFRAME_TEXTURE_HOVER
        return handled


class soActionBar(PyGUIBase):
    factoryString = 'soGUI.soActionBar'
    EVENT_REMOVE = 0
    EVENT_USE = 1
    EVENT_CONTEXT = 2
    EVENT_MOVE = 3
    EVENT_BARSCROLL = 4

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.interfaceID = BWPersonality.GUICore.GUI_ID_ACTIONBAR
        self.setupRoot()
        self.setupContent()
        self.doReposition()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (20, 20, 20, 90)
        cmp.materialFX = 'BLEND'
        cmp.width = 0
        cmp.height = 79
        cmp.textureName = 'soGUI/maps/Controls/ActionBar/frame.tga'

    def setupContent(self):
        itemView = soItemView(GUI.Window(), soActionSlot, slot_eventsHandler=self.slotHandler, eventsHandler=self.itemViewHandler, rowWidth=10, cols=10, rows=1, hScroll=False, vScroll=False, borderWidth=0, hInterval=1)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (20, 0, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'itemView')
        itemView.onBound()
        itemView.setRestrictingComponent(None)
        itemView.setItems(None)
        self.component.width = cmp.width + 20
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/scrollBtnUP.xml')
        btn.setVisualState('normal')
        btn.soundControlName = 'ArrowBtn'
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 16
        cmp.height = 16
        cmp.position = (0, 0, 0.1)
        self.component.addChild(cmp, 'btnUP')
        btn.onBound()
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/scrollBtnDN.xml')
        btn.setVisualState('normal')
        btn.soundControlName = 'ArrowBtn'
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 16
        cmp.height = 16
        cmp.position = (0, self.component.height, 0.1)
        self.component.addChild(cmp, 'btnDN')
        btn.onBound()
        cmp = GUI.Simple('soGUI/maps/Controls/scroll/scrollbar.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileWidth = 16
        cmp.tileHeight = 1
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 16
        cmp.height = 47
        cmp.position = (0, 16, 0.5)
        self.component.addChild(cmp, 'backFrame')
        cmp = GUI.Text('1')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (8, self.component.height / 2, 0.3)
        self.component.addChild(cmp, 'barN')
        return

    def slotHandler(self, event, data):
        from soInventoryScreen import soInventorySlot2
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soInventorySlot2):
                return True
            if isinstance(data[1], soActionSlot):
                return True
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soInventorySlot2):
                data[1].toActionBar(data[0].slotIndex)
                return True
            if isinstance(data[1], soActionSlot):
                BWPersonality.GUICore.actionBarEvent(self.EVENT_MOVE, [data[0].slotIndex, data[1].slotIndex])
                return True
        if event == module_soItemView.SLOTEVENT_MOUSEENTER:
            if isinstance(data, soActionSlot):
                BWPersonality.GUICore.toolTipEvent(data.slotIndex, self.interfaceID, soToolTipComponent.EVENT_SHOW)
                return True
        if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
            if isinstance(data, soActionSlot):
                BWPersonality.GUICore.toolTipEvent(data.slotIndex, self.interfaceID, soToolTipComponent.EVENT_HIDE)
                return True
        if event == module_soItemView.SLOTEVENT_LCLICK:
            BWPersonality.GUICore.actionBarEvent(self.EVENT_USE, data.slotIndex)
            return True
        if event == module_soItemView.SLOTEVENT_RCLICK:
            if isinstance(data, soActionSlot):
                BWPersonality.GUICore.actionBarEvent(self.EVENT_CONTEXT, data.slotIndex)
                return True
        return False

    def itemViewHandler(self, event, data):
        return False

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'actionBar')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False

    def _updateSlots(self, data):
        self.component.itemView.script.setItems(data)

    def _updateActionBarN(self, data):
        self.component.barN.text = data

    def update(self):
        data = BWPersonality.GUICore.actionBarDataSection
        if data is not None:
            if data.has_key('slots'):
                self._updateSlots(data['slots'])
            if data.has_key('line_number'):
                self._updateActionBarN(data['line_number'])
        return

    def doReposition(self):
        sw, sh = BigWorld.screenSize()
        self.component.position.x = sw
        self.component.position.y = sh

    @PyGUIEvent('btnUP', 'onClick')
    def scrolledUP(self):
        BWPersonality.GUICore.actionBarEvent(self.EVENT_BARSCROLL, 1)

    @PyGUIEvent('btnDN', 'onClick')
    def scrolledDN(self):
        BWPersonality.GUICore.actionBarEvent(self.EVENT_BARSCROLL, -1)