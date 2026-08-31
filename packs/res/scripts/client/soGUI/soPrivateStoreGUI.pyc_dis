# Embedded file name: scripts/client/soGUI/soPrivateStoreGUI.py
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
from Localization import lc
EVENT_SELLITEM = 0
EVENT_CANCELITEM = 1
EVENT_CONFIRM = 2
EVENT_ABORT = 3

class soPrivateStoreSlot(soItemSlot):
    factoryString = 'soGUI.soPrivateStoreSlot'
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
            itemCondition = ItemsUtils.GetItemConditionPercentString(BigWorld.player(), ItemsUtils.GetComplexItemByID(BigWorld.player(), item_id, getNotAppruved=True))
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

    def cancelSell(self):
        BWPersonality.GUICore.privateStoreEvent(EVENT_CANCELITEM, self.itemData)

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


class soPrivateStoreScreen(PyGUIBase):
    factoryString = 'soGUI.soPrivateStoreScreen'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.interfaceID = BWPersonality.GUICore.GUI_ID_PRIVATESTORE
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
        itemView = soItemView(GUI.Window(), soPrivateStoreSlot, slot_eventsHandler=self.slotHandler, eventsHandler=self.itemViewHandler, rowWidth=2, hScroll=False, borderWidth=0)
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
        cmp.text = lc('soPrivateStoreGUI.soGUI.STRING_241_13')
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
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 64
        cmp.height = 29
        cmp.position = (39, 357, 0.3)
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = lc('soPrivateStoreGUI.soGUI.STRING_278_19')
        self.component.addChild(cmp, 'confirmBtn')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 64
        cmp.height = 29
        cmp.position = (178, 357, 0.3)
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = lc('soPrivateStoreGUI.soGUI.STRING_298_19')
        self.component.addChild(cmp, 'cancelBtn')
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
                BWPersonality.GUICore.privateStoreEvent(EVENT_SELLITEM, data[1].itemData)
                return True
            else:
                return False
        if event == module_soItemView.SLOTEVENT_MOUSEENTER:
            if isinstance(data, soPrivateStoreSlot):
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
        items = BWPersonality.GUICore.privateStoreDataSection
        self._setItems(items)

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'privateStore')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        cmp = self.component
        cmp.position = (sW - 293, 300, 0.5)

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        BWPersonality.GUICore.privateStoreEvent(EVENT_ABORT, None)
        self.hide()
        return

    @PyGUIEvent('confirmBtn', 'onClick')
    def onConfirmBtn(self):
        BWPersonality.GUICore.privateStoreEvent(EVENT_CONFIRM, None)
        return

    @PyGUIEvent('cancelBtn', 'onClick')
    def onCancelBtn(self):
        BWPersonality.GUICore.privateStoreEvent(EVENT_ABORT, None)
        self.hide()
        return