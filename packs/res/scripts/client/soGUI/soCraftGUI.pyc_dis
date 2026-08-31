# Embedded file name: scripts/client/soGUI/soCraftGUI.py
from Localization import lc
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import BWPersonality
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soButton import soButton
from soGUI.soCheckBox import soCheckBox
from soGUI.soDropDownList import soDropDownList, soDropDownList2
from Helpers.PyGUI import PyGUIEvent
from copy import deepcopy
from Keys import *
from Helpers.PyGUI.DraggableComponent import DraggableComponent
import soGUI
from Helpers.BWCoroutine import *
from soTextField import soTextField2
from soTextField import soTxtFieldPropsStructure
from Items import ItemsCatalog
import ItemsUtils
from functools import partial

class guiKeyEvent(object):

    def __init__(self, key, down, mods = None):
        self.key = key
        self.down = down
        self.modifiers = mods

    def isKeyDown(self):
        return self.down


class soPartSlot(PyGUIBase, DraggableComponent):
    factoryString = 'soGUI.soPartSlot'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        DraggableComponent.__init__(self, True, True, False)
        component.script = self
        self.icon = None
        self.count = None
        self.setupRoot()
        self.setupFrame()
        self.setupCount()
        self.setupIcon()
        self.dragProxy = self.component.icon
        self.onBeginDrag = self._beginDrag
        self.onEndDrag = self._endDrag
        return

    def cancel(self):
        BWPersonality.GUICore.worldLayer.delChild(self.icon)
        self.component.addChild(self.icon, 'icon')
        self.icon.position = (2, 2, 0.1)

    def _beginDrag(self):
        self.component.delChild(self.icon)
        BWPersonality.GUICore.worldLayer.addChild(self.icon)

    def _endDrag(self):
        BWPersonality.GUICore.worldLayer.delChild(self.icon)
        self.component.addChild(self.icon, 'icon')
        self.icon.position = (2, 2, 0.1)

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.width = 64
        cmp.height = 64
        cmp.position = (0.0, 0.0, 0.1)
        cmp.textureName = ''
        cmp.focus = True
        cmp.dragFocus = True
        cmp.crossFocus = True
        cmp.mouseButtonFocus = True

    def setupFrame(self):
        cmp = GUI.Frame2('soGUI/maps/con_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 64
        cmp.height = 64
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.5)
        self.component.addChild(cmp, 'cellFrame')

    def setupIcon(self):
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 64
        cmp.height = 64
        cmp.position = (0, 0, 0.1)
        self.component.addChild(cmp, 'icon')
        self.icon = cmp

    def setupCount(self):
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (200, 200, 50, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_calibri_small.font'
        cmp.text = u''
        cmp.position = (1.0, -1.0, 0.05)
        self.component.addChild(cmp, 'count')
        self.count = cmp

    def handleDragStartEvent(self, *args):
        event = guiKeyEvent(KEY_LEFTMOUSE, True, None)
        DraggableComponent.handleMouseButtonEvent(self, self.component, event)
        self.isDragging = True
        return True

    def handleDragStopEvent(self, *args):
        event = guiKeyEvent(KEY_LEFTMOUSE, False, None)
        DraggableComponent.handleMouseButtonEvent(self, self.component, event)
        self.isDragging = False
        return True

    def handleDragEnterEvent(self, comp, dragged):
        return True

    def handleMouseEnterEvent(self, component):
        return True

    def handleMouseLeaveEvent(self, component):
        return True

    def setSlotInfo(self, slotInfo):
        self.slotInfo = slotInfo

    def setIcon(self, path):
        self.icon.textureName = path

    def setCount(self, count):
        if count > -1:
            self.count.text = str(count)
        else:
            self.count.text = u''

    def empty(self):
        self.setSlotInfo(None)
        self.setCount(-1)
        self.icon.textureName = ''
        return


class soCraftGUI(PyGUIBase):
    facoryString = 'soGUI.soCraftGUI'
    EVENT_SELECT = 0
    EVENT_ADDITEM = 1
    EVENT_DELITEM = 2
    EVENT_CRAFT = 3
    EVENT_CLOSE = 4
    EVENT_CLEAR = 5
    EVENT_AUTOFILL = 6

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupControls()
        self.setupSlots()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.position = (0.0, 0.0, 0.5)
        cmp.width = 428
        cmp.height = 470
        cmp.colour = (255, 255, 255, 255)
        cmp.textureName = ''
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        cmp.dropFocus = True

    def setupControls(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 428
        cmp.height = 450
        cmp.position = (0, 0, 1.2)
        self.component.addChild(cmp, 'wndFrame')
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
        topLine.width = 412
        topLine.height = 1
        topLine.position = (8, 275, 0.4)
        self.component.addChild(topLine, 'topLine')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (180, 5, 0.3)
        cmp.text = lc('GUI.CraftGUI.WINDOW_CAPTION')
        self.component.addChild(cmp, 'iLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.text = lc('soCraftGUI.soGUI.STRING_265_13')
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (8, 280, 0.9)
        self.component.addChild(cmp, 'statsLabel')
        ddl = soDropDownList2(GUI.Window(), width=402, height=29)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (12, 35, 0.4)
        self.component.addChild(cmp, 'blueprints')
        ddl.onBound()
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 200
        cmp.height = 29
        cmp.position = (8, 417, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soCraftGUI.soGUI.STRING_300_19')
        self.component.addChild(cmp, 'craftBtn')
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 200
        cmp.height = 29
        cmp.position = (219, 417, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soCraftGUI.soGUI.STRING_322_19')
        self.component.addChild(cmp, 'clearBtn')
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (401, 7, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'closeBox')
        btn.initVSC('soGUI/visual_styles/closeBox.xml')
        btn.onBound()
        btn.setVisualState('normal')
        txt = soTextField2(GUI.Window(), soTxtFieldPropsStructure(width=412, height=111, textureless=True, autoScroll=False))
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (8, 300, 0.5)
        self.component.addChild(cmp, 'textFld')
        txt.onBound()
        cmp = GUI.Simple('soGUI/maps/Controls/window_frame/craftTextFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 412
        cmp.height = 111
        cmp.position = (8, 300, 0.6)
        self.component.addChild(cmp, 'textFrame')
        cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=lc('soCraftGUI.soGUI.STRING_374_73'), labelColour=(175, 166, 112, 255)))
        cmp = cb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 246, 0.4)
        self.component.addChild(cmp, 'autofill')
        cb.onBound()
        cmp = GUI.Simple('soGUI/maps/Controls/window_frame/craftRecipeFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 201
        cmp.height = 167
        cmp.position = (10, 71, 0.6)
        self.component.addChild(cmp, 'recipeFrame')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 64
        cmp.height = 64
        cmp.position = (110, 154, 0.5)
        self.component.addChild(cmp, 'recipeIcon')

    def setupSlots(self):
        for i in xrange(3):
            for j in xrange(3):
                cmp = GUI.Simple('soGUI/maps/Controls/window_frame/craftRecipeFrame.tga')
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.width = 64
                cmp.height = 64
                cmp.position = (225 + j * 64, 71 + i * 64, 0.6)
                self.component.addChild(cmp, 'partFrame' + str(i * 3 + j))
                slot = soPartSlot(GUI.Window())
                cmp = slot.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.width = 64
                cmp.height = 64
                cmp.position = (225 + j * 64, 71 + i * 64, 0.6)
                self.component.addChild(cmp, 'partSlot' + str(i * 3 + j))

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'craftGUI')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.updateTopmostObjects()

    def update(self):
        items = BWPersonality.GUICore.craftDataSection['items']
        for i in xrange(9):
            cmp = self.component.__getattribute__('partSlot' + str(i))
            cmp.script.empty()

        for i in xrange(len(items)):
            cmp = self.component.__getattribute__('partSlot' + str(i))
            item = ItemsUtils.GetComplexItemByID(BigWorld.player(), items[i])
            item_type = item['complexItemType']
            item_id = item['complexItemID']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            item_level = item_params['Level']
            cmp.script.setSlotInfo(item['complexItemID'])
            iconName = ItemsUtils.getTextureByTint(item)
            if not iconName:
                iconName = item_params['IconName']
            cmp.script.setIcon(iconName)
            cmp.script.setCount(ItemsUtils.GetDisplayValue(item))

        if BWPersonality.GUICore.craftDataSection['autofill']:
            self.component.autofill.script.setActive()
        else:
            self.component.autofill.script.setInactive()
        recipes = BWPersonality.GUICore.craftDataSection['recipes']
        recDDL = self.component.blueprints.script
        selectedRec = recDDL.getSelection()[0]
        recDDL.clear()
        elems = []
        for recipe in recipes:
            recipeName = BigWorld.player().GetReceiptName(recipe)
            elem = [recipe, recipeName]
            elems.append(elem)

        recDDL.addElements(elems)
        recDDL.setSelectionByText(selectedRec, True, True)
        txt = self.component.textFld.script
        txt.setText(BWPersonality.GUICore.craftDataSection['description'])
        if BWPersonality.GUICore.craftDataSection.has_key('icon'):
            self.component.recipeIcon.textureName = BWPersonality.GUICore.craftDataSection['icon']
        else:
            self.component.recipeIcon.textureName = ''

    def handleDragEnterEvent(self, comp, dragged):
        return True

    def handleDropEvent(self, component, dropped):
        from soGUI.soInventoryScreen import soInventorySlot2
        if dropped.script.factoryString == 'soGUI.soInventorySlot':
            dropped.script.toCraft()
            BWPersonality.GUICore.craftEvent(self.EVENT_ADDITEM, dropped.script.slotInfo)
        if isinstance(dropped.script, soInventorySlot2):
            BWPersonality.GUICore.craftEvent(self.EVENT_ADDITEM, dropped.script.itemData)
        return True

    @PyGUIEvent('blueprints', 'onSelectedElement')
    def onRecipe(self, recID):
        BWPersonality.GUICore.craftEvent(self.EVENT_SELECT, recID)

    @PyGUIEvent('autofill', 'onStateChange')
    def onAuto(self):
        if BWPersonality.GUICore.craftDataSection is None:
            return
        else:
            state = BWPersonality.GUICore.craftDataSection['autofill']
            if self.component.autofill.script.isChecked() != state:
                BWPersonality.GUICore.craftEvent(self.EVENT_AUTOFILL, self.component.autofill.script.isChecked())
            return

    @PyGUIEvent('clearBtn', 'onClick')
    def onClear(self):
        BWPersonality.GUICore.craftEvent(self.EVENT_CLEAR, None)
        return

    @PyGUIEvent('craftBtn', 'onClick')
    def onCraft(self):
        BWPersonality.GUICore.craftEvent(self.EVENT_CRAFT, None)
        return

    @PyGUIEvent('closeBox', 'onClick')
    def onClose(self):
        BWPersonality.GUICore.craftEvent(self.EVENT_CLOSE, None)
        BWPersonality.GUICore.showCraftGUI(False)
        return