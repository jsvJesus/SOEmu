# Embedded file name: scripts/client/soGUI/soCharacterPicker.py
import GUI
import BigWorld
import BWPersonality
from Helpers.PyGUI import PyGUIBase
from gui_const import CHAR_PICKER
from soGUI.soButton import soButton, soButtonWTT
from Localization import lc
from functools import partial
from time import time
from Keys import *
from DummyRotating import DummyRotating
charSlotTexture = BigWorld.PyTextureProvider('soGUI/maps/charCreation/fon_tisnenie.tga')
charSlotTexture_selected = BigWorld.PyTextureProvider('soGUI/maps/charCreation/fon_tisnenie_select.tga')

def cleanup():
    del charSlotTexture
    del charSlotTexture_selected


class soCharacterSlot(PyGUIBase):
    factoryString = 'soGUI.soCharacterSlot'
    name_color = {'normal': (160, 160, 150, 255),
     'selected': (255, 255, 255, 255),
     'deleted': (80, 80, 80, 255)}
    info_color = {'normal': (108, 108, 108, 255),
     'selected': (160, 160, 150, 255),
     'deleted': (0, 0, 0, 255)}

    def __init__(self, component, charID):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.deleted = False
        self.selected = False
        self.isempty = False
        self.charID = charID
        self.ts = time()
        self.lastPressed = 0
        self.setupRoot()
        self.setupContent()
        self._updateVisuals()

    def setupRoot(self):
        comp = self.component
        comp.widthMode = comp.heightMode = 'PIXEL'
        comp.colour = (255, 255, 255, 255)
        comp.materialFX = 'BLEND'
        comp.width = 240
        comp.height = 32

    def setupContent(self):
        comp = GUI.Frame2('')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'CLIP'
        comp.widthMode = comp.heightMode = 'CLIP'
        comp.horizontalAnchor = 'CENTER'
        comp.verticalAnchor = 'CENTER'
        comp.colour = (255, 255, 255, 255)
        comp.materialFX = 'BLEND'
        comp.width = comp.height = 2.0
        comp.position = (0.0, 0.0, 0.9)
        comp.script = self
        comp.mouseButtonFocus = True
        self.component.addChild(comp, 'framecomp')
        comp = GUI.Text('')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.horizontalAnchor = 'LEFT'
        comp.verticalAnchor = 'CENTER'
        comp.colour = self.name_color['normal']
        comp.materialFX = 'BLEND'
        comp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        comp.position = (9, 16, 0.5)
        self.component.addChild(comp, 'nameLabel')
        comp = GUI.Text('')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.horizontalAnchor = 'LEFT'
        comp.verticalAnchor = 'CENTER'
        comp.colour = self.info_color['normal']
        comp.materialFX = 'BLEND'
        comp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        comp.position = (9, 31, 0.5)
        self.component.addChild(comp, 'infoLabel1')
        comp = GUI.Text('')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.horizontalAnchor = 'LEFT'
        comp.verticalAnchor = 'CENTER'
        comp.colour = self.info_color['normal']
        comp.materialFX = 'BLEND'
        comp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        comp.position = (9, 46, 0.5)
        self.component.addChild(comp, 'infoLabel2')
        comp = GUI.Text('')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.horizontalAnchor = 'RIGHT'
        comp.verticalAnchor = 'CENTER'
        comp.colour = self.name_color['normal']
        comp.materialFX = 'BLEND'
        comp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        comp.position = (220.0, 16.0, 0.4)
        comp.visible = False
        self.component.addChild(comp, 'timer')

    def setCharData(self, data):
        if data.has_key('states'):
            selectState = data['states'].get(CHAR_PICKER.SLOT_STATE_SELECTED)
            if selectState is not None:
                self.select(selectState, True)
            emptyState = data['states'].get(CHAR_PICKER.SLOT_STATE_EMPTY)
            if emptyState is not None:
                self.empty(emptyState)
        self.delete(data['time'] > 0)
        if data.has_key('name'):
            self.component.nameLabel.text = data['name']
        if data.has_key('info1'):
            self.component.infoLabel1.text = data['info1']
        if data.has_key('info2'):
            self.component.infoLabel2.text = data['info2']
        if data.has_key('time'):
            if not self.isempty and self.deleted:
                self.component.timer.text = self.getStringtime(data['time'])
        return

    def getStringtime(self, t):
        days = int(t / 60 / 60 / 24)
        hour = int(t / 60 / 60)
        min = int(t / 60)
        if days > 0:
            return str(days) + lc('GUI.General.DAYS_SHORTENING')
        elif hour > 0:
            return str(hour) + lc('GUI.General.HOURS_SHORTENING')
        else:
            return str(min) + lc('GUI.General.MINUTES_SHORTENING')

    def _updateVisuals(self):
        if self.selected:
            self.component.framecomp.texture = charSlotTexture_selected
            self.component.nameLabel.colour = self.name_color['selected']
            self.component.infoLabel1.colour = self.info_color['selected']
            self.component.infoLabel2.colour = self.info_color['selected']
        else:
            self.component.framecomp.texture = charSlotTexture
            self.component.nameLabel.colour = self.name_color['normal']
            self.component.infoLabel1.colour = self.info_color['normal']
            self.component.infoLabel2.colour = self.info_color['normal']
        if self.isempty:
            self.component.nameLabel.visible = False
            self.component.infoLabel1.visible = False
            self.component.infoLabel2.visible = False
            self.component.timer.visible = True
            self.component.timer.font = 'ruRU_Cyrvetica_Extra_14i.font'
            self.component.timer.text = lc('GUI.CharacterPicker.EMPTY_CHARACTER_SLOT')
            self.component.framecomp.texture = charSlotTexture
        else:
            self.component.nameLabel.visible = True
            self.component.infoLabel1.visible = True
            self.component.infoLabel2.visible = True
            self.component.timer.visible = False
            self.component.timer.font = 'ruRU_Cyrvetica_Extra_14i.font'
        if self.deleted:
            self.component.nameLabel.colour = self.name_color['deleted']
            self.component.infoLabel1.colour = self.info_color['deleted']
            self.component.infoLabel2.colour = self.info_color['deleted']
            self.component.timer.visible = True
        else:
            self.component.timer.visible = False

    def select(self, doSelect = True, silent = False):
        self.selected = doSelect
        self._updateVisuals()
        self.onSelect(self.charID, silent)

    def delete(self, doDelete = True):
        self.deleted = doDelete
        self._updateVisuals()

    def empty(self, doEmpty = True):
        self.isempty = doEmpty
        self._updateVisuals()

    def onSelect(self, id, silent):
        return None

    def fini(self):
        self.clearAllChildren(self.component)
        self.component.script = None
        self.component = None
        return

    def handleMouseButtonEvent(self, comp, event):
        key = event.key
        down = event.isKeyDown()
        if event.key == KEY_LEFTMOUSE:
            if event.isKeyDown():
                self.onSelect(self.charID, False)
                if BigWorld.time() - self.lastPressed <= BWPersonality.GUICore.mouseDoubleClickSpeed:
                    self.onUse(self.charID, False)
                self.lastPressed = BigWorld.time()
                return True
        return False

    def onUse(self, id, silent):
        return None


class soCharacterPickGUI(PyGUIBase):
    factoryString = 'soGUI.soCharacterPickGUI'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.char_panning = False
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        comp = self.component
        comp.horizontalPositionMode = comp.verticalPositionMode = 'CLIP'
        comp.widthMode = comp.heightMode = 'CLIP'
        comp.horizontalAnchor = comp.verticalAnchor = 'CENTER'
        comp.colour = (255, 255, 255, 255)
        comp.materialFX = 'BLEND'
        comp.visible = False
        comp.width = comp.height = 2.0
        comp.position = (0.0, 0.0, 0.5)
        comp.focus = True
        comp.mouseButtonFocus = True
        comp.moveFocus = True

    def setupContent(self):
        sw, sh = BigWorld.screenSize()
        comp = GUI.Simple('soGUI/maps/Login/frame_menu.dds')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.widthMode = comp.heightMode = 'PIXEL'
        comp.horizontalAnchor = 'RIGHT'
        comp.verticalAnchor = 'TOP'
        comp.colour = (255, 255, 255, 255)
        comp.filterType = 'LINEAR'
        comp.materialFX = 'BLEND'
        comp.width = 300
        comp.height = sh
        comp.position = (sw, 0, 0.25)
        comp.mouseButtonFocus = True
        self.component.addChild(comp, 'decoStripesRight')
        comp = GUI.Simple('soGUI/maps/Login/frame_menu.dds')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.widthMode = comp.heightMode = 'PIXEL'
        comp.horizontalAnchor = 'LEFT'
        comp.verticalAnchor = 'TOP'
        comp.colour = (255, 255, 255, 255)
        comp.filterType = 'LINEAR'
        comp.materialFX = 'BLEND'
        comp.width = 300
        comp.height = sh
        comp.position = (0, 0, 0.8)
        comp.mouseButtonFocus = True
        self.component.addChild(comp, 'decoStripesLeft')
        comp = GUI.Simple('soGUI/maps/Colours/white.tga')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.widthMode = comp.heightMode = 'PIXEL'
        comp.horizontalAnchor = 'LEFT'
        comp.verticalAnchor = 'TOP'
        comp.colour = (74, 74, 74, 255)
        comp.materialFX = 'BLEND'
        comp.width = 2
        comp.height = sh
        comp.position = (299, 0, 0.4)
        self.component.addChild(comp, 'vLineL')
        comp = GUI.Simple('soGUI/maps/Colours/white.tga')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.widthMode = comp.heightMode = 'PIXEL'
        comp.horizontalAnchor = 'RIGHT'
        comp.verticalAnchor = 'TOP'
        comp.colour = (74, 74, 74, 255)
        comp.materialFX = 'BLEND'
        comp.width = 2
        comp.height = sh
        comp.position = (sw - 299, 0, 0.4)
        self.component.addChild(comp, 'vLineR')
        comp = GUI.Frame2('soGUI/maps/Login/blackout_1.tga')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.widthMode = comp.heightMode = 'PIXEL'
        comp.horizontalAnchor = 'LEFT'
        comp.verticalAnchor = 'TOP'
        comp.colour = (255, 255, 255, 255)
        comp.filterType = 'LINEAR'
        comp.materialFX = 'BLEND'
        comp.width = sw - 600
        comp.height = sh
        comp.position = (300, 0, 0.7)
        self.component.addChild(comp, 'bBG')
        comp = GUI.Text('')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.horizontalAnchor = 'CENTER'
        comp.verticalAnchor = 'CENTER'
        comp.colour = (160, 160, 150, 255)
        comp.materialFX = 'BLEND'
        comp.font = 'ruRU_Verdana_21.font'
        comp.text = lc('GUI.CharacterPicker.CHARACTER_LIST_CAPTION')
        comp.position = (150, 50, 0.4)
        self.component.addChild(comp, 'charListCpt')
        btn = soButton(GUI.Window())
        btn.onClick = self.onPlayBtn
        comp = btn.component
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.widthMode = comp.heightMode = 'PIXEL'
        comp.horizontalAnchor = 'CENTER'
        comp.verticalAnchor = 'BOTTOM'
        comp.width = 200
        comp.height = 21
        comp.textureName = ''
        comp.position = (150, sh - 99, 0.1)
        comp.colour = (255, 255, 255, 255)
        comp.materialFX = 'BLEND'
        comp.label.text = lc('GUI.CharacterPicker.PLAY_BUTTON_LABEL')
        self.component.addChild(comp, 'playBtn')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        btn.onBound()
        btn._updateVisualState()
        btn = soButton(GUI.Window())
        btn.onClick = self.onBackBtn
        comp = btn.component
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.widthMode = comp.heightMode = 'PIXEL'
        comp.horizontalAnchor = 'CENTER'
        comp.verticalAnchor = 'BOTTOM'
        comp.width = 200
        comp.height = 21
        comp.textureName = ''
        comp.position = (150, sh - 59, 0.1)
        comp.colour = (255, 255, 255, 255)
        comp.materialFX = 'BLEND'
        comp.label.text = lc('GUI.CharacterPicker.BACK_TO_MAIN_BUTTON_LABEL')
        self.component.addChild(comp, 'backBtn')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        btn.onBound()
        btn._updateVisualState()
        btn = soButton(GUI.Window())
        btn.onClick = self.onDelResBtn
        comp = btn.component
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.widthMode = comp.heightMode = 'PIXEL'
        comp.horizontalAnchor = 'LEFT'
        comp.verticalAnchor = 'TOP'
        comp.width = 183
        comp.height = 36
        comp.textureName = ''
        comp.position = (58, 70, 0.1)
        comp.colour = (255, 255, 255, 255)
        comp.materialFX = 'BLEND'
        comp.label.text = lc('GUI.CharacterPicker.DELETE_CHARACTER_BUTTON_LABEL')
        self.component.addChild(comp, 'del_res_Char')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnOption.xml')
        btn.onBound()
        btn._updateVisualState()
        btn = soButton(GUI.Window())
        btn.onClick = self.onNewBtn
        comp = btn.component
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.widthMode = comp.heightMode = 'PIXEL'
        comp.horizontalAnchor = 'LEFT'
        comp.verticalAnchor = 'TOP'
        comp.width = 183
        comp.height = 36
        comp.textureName = ''
        comp.position = (58, 110, 0.1)
        comp.colour = (255, 255, 255, 255)
        comp.materialFX = 'BLEND'
        comp.label.text = lc('GUI.CharacterPicker.NEW_CHARACTER_BUTTON_LABEL')
        self.component.addChild(comp, 'newChar')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnOption.xml')
        btn.onBound()
        btn._updateVisualState()
        btn = soButtonWTT(GUI.Window(), 'premium_button')
        btn.onClick = self.onActivatePremium
        comp = btn.component
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.widthMode = comp.heightMode = 'PIXEL'
        comp.horizontalAnchor = 'LEFT'
        comp.verticalAnchor = 'TOP'
        comp.width = 245
        comp.height = 36
        comp.textureName = ''
        comp.position = (sw - 268, sh - 230, 0.1)
        comp.colour = (255, 255, 255, 255)
        comp.materialFX = 'BLEND'
        comp.label.text = lc('GUI.CharacterPicker.activatePremium')
        self.component.addChild(comp, 'activatePremium')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnOptionGold.xml')
        btn.onBound()
        btn._updateVisualState()

    def onActivatePremium(self):
        BWPersonality.GUICore.charPickerEvent(CHAR_PICKER.EVENT_PREMIUM, {})

    def _clearCharacterSummary(self):
        for name, child in self.component.children:
            if name.startswith('char_summary_'):
                self.component.delChild(child)

    def _repositionChSummary(self):
        sw, sh = BigWorld.screenSize()
        for name, child in self.component.children:
            if name.startswith('char_summary_caption'):
                child.position.x = sw - 268
            elif name.startswith('char_summary_val'):
                child.position.x = sw - 30

    def setCharacterSummary(self, data):
        sw, sh = BigWorld.screenSize()
        if data is None:
            data = []
        self._clearCharacterSummary()
        for index, entry in enumerate(data):
            indent = 0
            colour = (160, 160, 150, 255)
            font = 'ruRU_Cyrvetica_Extra_14i.font'
            if index > 5:
                indent = sh - 310
                colour = (222, 185, 120, 255)
                font = 'ruRU_Cyrvetica_Extra_14i.font'
            comp = GUI.Text('')
            comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
            comp.horizontalAnchor = 'LEFT'
            comp.verticalAnchor = 'CENTER'
            comp.colour = colour
            comp.font = font
            comp.materialFX = 'BLEND'
            comp.text = entry[0]
            comp.position = (sw - 268, 32 + 17 * index + indent, 0.2)
            self.component.addChild(comp, 'char_summary_caption{0}'.format(index))
            comp = GUI.Text('')
            comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
            comp.horizontalAnchor = 'RIGHT'
            comp.verticalAnchor = 'CENTER'
            comp.colour = colour
            comp.font = font
            comp.materialFX = 'BLEND'
            comp.text = entry[1]
            comp.position = (sw - 30, 32 + 17 * index + indent, 0.2)
            self.component.addChild(comp, 'char_summary_val{0}'.format(index))

        return

    def setGold(self):
        sw, sh = BigWorld.screenSize()
        indent = sh - 310
        colour = (222, 185, 120, 255)
        font = 'ruRU_Cyrvetica_Extra_14i.font'
        comp = GUI.Text('')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.horizontalAnchor = 'LEFT'
        comp.verticalAnchor = 'CENTER'
        comp.colour = colour
        comp.font = font
        comp.materialFX = 'BLEND'
        comp.text = lc('soCharacterScreen.soGUI.GoldCreditNumber')
        comp.position = (sw - 268, 32 + 136 + indent, 0.2)
        self.component.addChild(comp, 'char_summary_caption{0}'.format(8))
        comp = GUI.Text('')
        comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
        comp.horizontalAnchor = 'RIGHT'
        comp.verticalAnchor = 'CENTER'
        comp.colour = colour
        comp.font = font
        comp.materialFX = 'BLEND'
        comp.text = str(BWPersonality.GUICore.goldCost)
        comp.position = (sw - 30, 32 + 136 + indent, 0.2)
        self.component.addChild(comp, 'char_summary_val{0}'.format(8))

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.menuLayer.addChild(self.component, 'charPicker')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def selectSlot(self, charID):
        for name, child in self.component.children:
            if name.startswith('char_slot_'):
                if child.script.charID != charID:
                    child.script.selected = False
                    child.script._updateVisuals()
                else:
                    child.script.selected = True
                    child.script._updateVisuals()

        charSlot = getattr(self.component, 'char_slot_{0}'.format(charID), None)
        self.renameButton(charSlot.script.deleted)
        return

    def onSlotSelect(self, charID, silent):
        if not silent:
            BWPersonality.GUICore.charPickerEvent(CHAR_PICKER.EVENT_SELECT, {'id': charID})
        self.selectSlot(charID)

    def onSlotUse(self, charID, silent):
        if not silent:
            BWPersonality.GUICore.charPickerEvent(CHAR_PICKER.EVENT_USE, {'id': charID})

    def _getYForNewSlot(self):
        y = 3
        for name, child in self.component.children:
            if name.startswith('char_slot_'):
                if child.position.y > y:
                    y = child.position.y

        return y + 32

    def _rearrangeSlots(self):

        def comp_slots(slotA, slotB):
            return cmp(slotA.script.ts, slotB.script.ts)

        comps = []
        for name, child in self.component.children:
            if name.startswith('char_slot_'):
                comps.append(child)

        comps.sort(comp_slots)
        for i, comp in enumerate(comps):
            comp.position.y = 70 + 32 * i

        if comps:
            self.component.del_res_Char.position.y = comps[-1].position.y + 105
            self.component.newChar.position.y = comps[-1].position.y + 63

    def removeCharacter(self, id):
        charSlot = getattr(self.component, 'char_slot_{0}'.format(id), None)
        if charSlot is not None:
            charSlot.script.fini()
            self.component.delChild(charSlot)
        self._rearrangeSlots()
        return

    def clearCharacters(self):
        for name, child in self.component.children:
            if name.startswith('char_slot_'):
                child.script.fini()
                self.component.delChild(child)

        self._rearrangeSlots()

    def setCharacter(self, id, data):
        charSlot = getattr(self.component, 'char_slot_{0}'.format(id), None)
        if charSlot is not None:
            charSlot.script.setCharData(data)
        else:
            slot = soCharacterSlot(GUI.Window(), id)
            slot.setCharData(data)
            slot.onSelect = self.onSlotSelect
            slot.onUse = self.onSlotUse
            comp = slot.component
            comp.horizontalPositionMode = comp.verticalPositionMode = 'PIXEL'
            comp.horizontalAnchor = 'LEFT'
            comp.verticalAnchor = 'TOP'
            comp.position.x = 30
            comp.position.y = self._getYForNewSlot()
            comp.position.z = 0.3
            self.component.addChild(comp, 'char_slot_{0}'.format(id))
            if data['states'].get(CHAR_PICKER.SLOT_STATE_SELECTED):
                self.selectSlot(id)
        self._rearrangeSlots()
        return

    def renameButton(self, isDeleted):
        if isDeleted:
            self.component.del_res_Char.label.text = lc('GUI.CharacterPicker.RESTORE_CHARACTER_BUTTON_LABEL')
            self.component.playBtn.script.setDisabledState(True)
        else:
            self.component.del_res_Char.label.text = lc('GUI.CharacterPicker.DELETE_CHARACTER_BUTTON_LABEL')
            self.component.playBtn.script.setDisabledState(False)

    def onDelResBtn(self):
        if self.component.del_res_Char.label.text == lc('GUI.CharacterPicker.RESTORE_CHARACTER_BUTTON_LABEL'):
            BWPersonality.GUICore.charPickerEvent(CHAR_PICKER.EVENT_RESTORE, {})
        else:
            BWPersonality.GUICore.charPickerEvent(CHAR_PICKER.EVENT_DELETE, {})

    def onNewBtn(self):
        BWPersonality.GUICore.charPickerEvent(CHAR_PICKER.EVENT_NEW, {})

    def onPlayBtn(self):
        BWPersonality.GUICore.charPickerEvent(CHAR_PICKER.EVENT_PLAY, {})

    def onBackBtn(self):
        BWPersonality.GUICore.charPickerEvent(CHAR_PICKER.EVENT_BACK, {})

    def handleKeyEvent(self, event):
        key = event.key
        char = event.character
        mods = event.modifiers
        down = event.isKeyDown()
        if key in (KEY_RETURN, KEY_NUMPADENTER) and down:
            BWPersonality.GUICore.charPickerEvent(CHAR_PICKER.EVENT_PLAY, {})
            return True
        if key == KEY_LEFTMOUSE:
            if down and self._checkIfCanPan():
                self.char_panning = True
            else:
                self.char_panning = False
            return True
        return False

    def _checkIfCanPan(self):
        pos = GUI.mcursor().position
        return True

    def handleMouseEvent(self, cmp, event):
        if cmp == self.component:
            if self.char_panning:
                BWPersonality.GUICore.charPickerEvent(CHAR_PICKER.EVENT_MODELPAN, {'dx': event.dx,
                 'dy': event.dy})
                DummyRotating().rotate(event.dx)
                return True
        return False

    def doReposition(self):
        sw, sh = BigWorld.screenSize()
        self._repositionChSummary()
        self.component.decoStripesRight.height = sh
        self.component.decoStripesRight.position.x = sw
        self.component.decoStripesLeft.height = sh
        self.component.vLineL.height = sh
        self.component.vLineR.position.x = sw - 299
        self.component.vLineR.height = sh
        self.component.bBG.width = sw - 600
        self.component.bBG.height = sh
        self.component.playBtn.position.y = sh - 99
        self.component.backBtn.position.y = sh - 59