# Embedded file name: scripts/client/soGUI/soCharacterManagmentGUI.py
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import BWPersonality
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soButton import soButton
from soGUI.soEditField import soEditField2
from copy import deepcopy
from Keys import *
from functools import partial
from Localization import lc

class soCharacterManagmentGUI(PyGUIBase):
    factoryString = 'soGUI.soCharacterManagmentGUI'
    EVENT_PLAY = 0
    EVENT_SCREENCLICK = 1
    EVENT_DELETE = 2
    EVENT_LOGOFF = 3
    EVENT_NEWCHAR = 4
    EVENT_MAKECHAR = 5
    EVENT_CANCELMAKE = 6
    EVENT_SELECTPART = 7
    EVENT_RENAME = 8
    MODE_SELECT = 0
    MODE_CREATE = 1

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.currentMode = soCharacterManagmentGUI.MODE_SELECT
        self.setupRoot()
        self.setupSelectFrame()
        self.setupCreateFrame()
        self.CSdata = None
        self.headData = None
        self.beardData = None
        self.skinData = None
        self.legsData = None
        self.chestData = None
        self.currentSelections = [0,
         0,
         0,
         0,
         0]
        self.slotMap = {0: 'HEAD',
         1: 'BEARD',
         2: 'SKINCOLOR',
         3: 'LEGS',
         4: 'CHEST'}
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (-1.0, 1.0, 0.1)
        cmp.mouseButtonFocus = True
        cmp.focus = True

    def setupSelectFrame(self):
        sW, sH = BigWorld.screenSize()
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.1)
        cmp.textureName = ''
        self.component.addChild(cmp, 'selectFrame')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 150
        cmp.height = 30
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.CharacterManagment.START_GAME_BUTTON_LABEL')
        cmp.position = (sW / 2.0, sH - 100, 0.0)
        self.component.selectFrame.addChild(cmp, 'playBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 250
        cmp.height = 30
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.CharacterManagment.CREATE_CHARACTER_BUTTON_LABEL')
        cmp.position = (50, sH - 100, 0.0)
        self.component.selectFrame.addChild(cmp, 'createNewBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 250
        cmp.height = 30
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.CharacterManagment.EXIT_TO_MAIN_MENU_BUTTON_LABEL')
        cmp.position = (50, sH - 55, 0.0)
        self.component.selectFrame.addChild(cmp, 'toMain')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 120
        cmp.height = 30
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.CharacterManagment.DELETE_CHARACTER_BUTTON_LABEL')
        cmp.position = (sW / 2.0, sH - 55, 0.0)
        self.component.selectFrame.addChild(cmp, 'delBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 120
        cmp.height = 30
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.CharacterManagment.RENAME_CHARACTER_BUTTON_LABEL')
        cmp.position = (sW / 2.0 + 180, sH - 100, 0.0)
        cmp.visible = False
        self.component.selectFrame.addChild(cmp, 'renameBtn')
        btn.onBound()
        btn.setVisualState('normal')
        cmp = GUI.Text('')
        cmp.font = 'ruRU_calibri_large.font'
        cmp.colour = (190, 230, 165, 255)
        cmp.materialFX = 'BLEND'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.position = (sW / 2.0, 100, 1.0)
        cmp.text = u''
        self.component.selectFrame.addChild(cmp, 'nameLabel')

    def setupCreateFrame(self):
        sW, sH = BigWorld.screenSize()
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 500
        cmp.height = 700
        cmp.position = (sW / 2.0 - 155, sH / 2.0, 0.1)
        cmp.textureName = ''
        cmp.visible = False
        self.component.addChild(cmp, 'createFrame')
        edit = soEditField2(GUI.Window(), width=311, height=29, font='ruRU_calibri_default.font')
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (0, 0, 0.1)
        self.component.createFrame.addChild(cmp, 'nameInput')
        for i in xrange(5):
            cmp = GUI.Frame2('soGUI/maps/Controls/window_frame/windowFrame1.tga')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 130
            cmp.height = 99
            cmp.position = (370, 0 + 105 * i, 0.4)
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            self.component.createFrame.addChild(cmp, 'backFrame' + str(i))
            cmp = GUI.Frame2('soGUI/maps/Controls/window_frame/windowFrame1.tga')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 122
            cmp.height = 72
            cmp.position = (374, 4 + 105 * i, 0.3)
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            self.component.createFrame.addChild(cmp, 'iconFrame' + str(i))
            cmp = GUI.Simple('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 65
            cmp.height = 65
            cmp.position = (402, 8 + 105 * i, 0.3)
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            self.component.createFrame.addChild(cmp, 'icon' + str(i))
            cmp = GUI.Simple('soGUI/maps/Controls/window_frame/charGUINameFrame.tga')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 121
            cmp.height = 18
            cmp.position = (374, 77 + 105 * i, 0.5)
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            self.component.createFrame.addChild(cmp, 'nameFrame' + str(i))
            btn = soButton(GUI.Window())
            cmp = btn.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 18
            cmp.height = 18
            cmp.position = (374, 77 + 105 * i, 0.1)
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            self.component.createFrame.addChild(cmp, 'leftBtn' + str(i))
            btn.initVSC('soGUI/visual_styles/arrow_left.xml')
            btn.onBound()
            btn.setVisualState('normal')
            btn.onClick = partial(self.processSelection, 'left', i)
            btn = soButton(GUI.Window())
            cmp = btn.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 18
            cmp.height = 18
            cmp.position = (478, 77 + 105 * i, 0.1)
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            self.component.createFrame.addChild(cmp, 'rightBtn' + str(i))
            btn.initVSC('soGUI/visual_styles/arrow_right.xml')
            btn.onBound()
            btn.setVisualState('normal')
            btn.onClick = partial(self.processSelection, 'right', i)
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_small.font'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (435, 85 + 105 * i, 0.3)
            cmp.text = u''
            self.component.createFrame.addChild(cmp, 'selectionLabel' + str(i))

        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (0, 671, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.CharacterManagment.CREATE_CHARACTER_CONFIRM_BUTTON_LABEL')
        self.component.createFrame.addChild(cmp, 'applyBtn')
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (210, 671, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.CharacterManagment.CREATE_CHARACTER_CANCEL_BUTTON_LABEL')
        self.component.createFrame.addChild(cmp, 'cancelBtn')
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onBound()
        btn.setVisualState('normal')

    def show(self, mode = MODE_SELECT):
        if self.component.parent is None:
            BWPersonality.GUICore.menuLayer.addChild(self.component, 'characterManager')
        self.component.visible = True
        self.setMode(mode)
        return

    def hide(self):
        self.component.visible = False

    def setToDefault(self, redraw = False):
        self.currentSelections = [0,
         0,
         0,
         0,
         0]
        self.component.createFrame.nameInput.script.clear()
        if redraw:
            self.updateCharCreate(True, True, True, True, True)

    def setMode(self, mode = MODE_SELECT):
        self.currentMode = mode
        if mode == self.MODE_SELECT:
            self.component.createFrame.visible = False
            self.component.createFrame.nameInput.script.setActive(False)
            self.component.selectFrame.visible = True
        if mode == self.MODE_CREATE:
            self.setToDefault(True)
            self.component.createFrame.visible = True
            self.component.createFrame.nameInput.script.setActive(True)
            self.component.selectFrame.visible = False

    def updateCharCreate(self, head = True, beard = True, skin = True, legs = True, chest = True):
        if head:
            self.component.createFrame.selectionLabel0.text = self.headData[self.currentSelections[0]][0]
            self.component.createFrame.icon0.textureName = self.headData[self.currentSelections[0]][1]
        if beard:
            self.component.createFrame.selectionLabel1.text = self.beardData[self.currentSelections[1]][0]
            self.component.createFrame.icon1.textureName = self.beardData[self.currentSelections[1]][1]
        if skin:
            self.component.createFrame.selectionLabel2.text = self.skinData[self.currentSelections[2]][0]
            self.component.createFrame.icon2.textureName = self.skinData[self.currentSelections[2]][1]
        if legs:
            self.component.createFrame.selectionLabel3.text = self.legsData[self.currentSelections[3]][0]
            self.component.createFrame.icon3.textureName = self.legsData[self.currentSelections[3]][1]
        if chest:
            self.component.createFrame.selectionLabel4.text = self.chestData[self.currentSelections[4]][0]
            self.component.createFrame.icon4.textureName = self.chestData[self.currentSelections[4]][1]

    def updateCharSelect(self):
        if self.CSdata is None or len(self.CSdata) < 1:
            return
        else:
            self.component.selectFrame.nameLabel.text = self.CSdata[0]
            if self.CSdata[1] > 0:
                self.component.selectFrame.renameBtn.visible = True
            else:
                self.component.selectFrame.renameBtn.visible = False
            return

    def update(self):
        head, beard, skin, legs, chest = (False,
         False,
         False,
         False,
         False)
        if self.CSdata != BWPersonality.GUICore.characterManagerDataSection['selection']:
            self.CSdata = deepcopy(BWPersonality.GUICore.characterManagerDataSection['selection'])
            self.updateCharSelect()
        if BWPersonality.GUICore.characterManagerDataSection['creation'] is not None:
            if self.headData != BWPersonality.GUICore.characterManagerDataSection['creation']['HEAD']:
                self.headData = deepcopy(BWPersonality.GUICore.characterManagerDataSection['creation']['HEAD'])
                if len(self.headData) > 0:
                    head = True
                    self.component.createFrame.leftBtn0.script.buttonDisabled = False
                    self.component.createFrame.leftBtn0.script.setVisualState('normal')
                    self.component.createFrame.rightBtn0.script.buttonDisabled = False
                    self.component.createFrame.rightBtn0.script.setVisualState('normal')
                else:
                    self.component.createFrame.leftBtn0.script.buttonDisabled = True
                    self.component.createFrame.leftBtn0.script.setVisualState('buttonDisabled')
                    self.component.createFrame.rightBtn0.script.buttonDisabled = True
                    self.component.createFrame.rightBtn0.script.setVisualState('buttonDisabled')
                self.currentSelections[0] = 0
            if self.beardData != BWPersonality.GUICore.characterManagerDataSection['creation']['BEARD']:
                self.beardData = deepcopy(BWPersonality.GUICore.characterManagerDataSection['creation']['BEARD'])
                if len(self.beardData) > 0:
                    beard = True
                    self.component.createFrame.leftBtn1.script.buttonDisabled = False
                    self.component.createFrame.leftBtn1.script.setVisualState('normal')
                    self.component.createFrame.rightBtn1.script.buttonDisabled = False
                    self.component.createFrame.rightBtn1.script.setVisualState('normal')
                else:
                    self.component.createFrame.leftBtn1.script.buttonDisabled = True
                    self.component.createFrame.leftBtn1.script.setVisualState('disabled')
                    self.component.createFrame.rightBtn1.script.buttonDisabled = True
                    self.component.createFrame.rightBtn1.script.setVisualState('disabled')
                self.currentSelections[1] = 0
            if self.skinData != BWPersonality.GUICore.characterManagerDataSection['creation']['SKINCOLOR']:
                self.skinData = deepcopy(BWPersonality.GUICore.characterManagerDataSection['creation']['SKINCOLOR'])
                if len(self.skinData) > 0:
                    skin = True
                    self.component.createFrame.leftBtn2.script.buttonDisabled = False
                    self.component.createFrame.leftBtn2.script.setVisualState('normal')
                    self.component.createFrame.rightBtn2.script.buttonDisabled = False
                    self.component.createFrame.rightBtn2.script.setVisualState('normal')
                else:
                    self.component.createFrame.leftBtn2.script.buttonDisabled = True
                    self.component.createFrame.leftBtn2.script.setVisualState('disabled')
                    self.component.createFrame.rightBtn2.script.buttonDisabled = True
                    self.component.createFrame.rightBtn2.script.setVisualState('disabled')
                self.currentSelections[2] = 0
            if self.legsData != BWPersonality.GUICore.characterManagerDataSection['creation']['LEGS']:
                self.legsData = deepcopy(BWPersonality.GUICore.characterManagerDataSection['creation']['LEGS'])
                if len(self.legsData) > 0:
                    legs = True
                    self.component.createFrame.leftBtn3.script.buttonDisabled = False
                    self.component.createFrame.leftBtn3.script.setVisualState('normal')
                    self.component.createFrame.rightBtn3.script.buttonDisabled = False
                    self.component.createFrame.rightBtn3.script.setVisualState('normal')
                else:
                    self.component.createFrame.leftBtn3.script.buttonDisabled = True
                    self.component.createFrame.leftBtn3.script.setVisualState('disabled')
                    self.component.createFrame.rightBtn3.script.buttonDisabled = True
                    self.component.createFrame.rightBtn3.script.setVisualState('disabled')
                self.currentSelections[3] = 0
            if self.chestData != BWPersonality.GUICore.characterManagerDataSection['creation']['CHEST']:
                self.chestData = deepcopy(BWPersonality.GUICore.characterManagerDataSection['creation']['CHEST'])
                if len(self.chestData) > 0:
                    chest = True
                    self.component.createFrame.leftBtn4.script.buttonDisabled = False
                    self.component.createFrame.leftBtn4.script.setVisualState('normal')
                    self.component.createFrame.rightBtn4.script.buttonDisabled = False
                    self.component.createFrame.rightBtn4.script.setVisualState('normal')
                else:
                    self.component.createFrame.leftBtn4.script.buttonDisabled = True
                    self.component.createFrame.leftBtn4.script.setVisualState('disabled')
                    self.component.createFrame.rightBtn4.script.buttonDisabled = True
                    self.component.createFrame.rightBtn4.script.setVisualState('disabled')
                self.currentSelections[4] = 0
        self.updateCharCreate(head, beard, skin, legs, chest)
        return

    def handleMouseButtonEvent(self, comp, event):
        key = event.key
        down = event.isKeyDown()
        pos = event.cursorPosition
        if key == KEY_LEFTMOUSE:
            if down:
                if self.currentMode == self.MODE_SELECT:
                    BWPersonality.GUICore.characterManagerEvent(self.EVENT_SCREENCLICK, pos)
                    return True
        return False

    def processSelection(self, direction = 'right', slotN = 0):
        data = None
        head, beard, skin, legs, chest = (False,
         False,
         False,
         False,
         False)
        if slotN == 0:
            data = self.headData
            head = True
        elif slotN == 1:
            data = self.beardData
            beard = True
        elif slotN == 2:
            data = self.skinData
            skin = True
        elif slotN == 3:
            data = self.legsData
            legs = True
        elif slotN == 4:
            data = self.chestData
            chest = True
        else:
            return False
        if data is not None:
            min = 0
            max = len(data) - 1
            if direction == 'right':
                if self.currentSelections[slotN] + 1 <= max:
                    self.currentSelections[slotN] += 1
                    data = (self.slotMap[slotN], self.currentSelections[slotN])
                    BWPersonality.GUICore.characterManagerEvent(self.EVENT_SELECTPART, data)
            if direction == 'left':
                if self.currentSelections[slotN] - 1 >= min:
                    self.currentSelections[slotN] -= 1
                    data = (self.slotMap[slotN], self.currentSelections[slotN])
                    BWPersonality.GUICore.characterManagerEvent(self.EVENT_SELECTPART, data)
            self.updateCharCreate(head, beard, skin, legs, chest)
        return

    def handleKeyEvent(self, event):
        key = event.key
        char = event.character
        mods = event.modifiers
        down = event.isKeyDown()
        if BWPersonality.GUICore.queueGUI is not None:
            if BWPersonality.GUICore.queueGUI.component.visible or BWPersonality.GUICore.characterReciever:
                return False
        if key in (KEY_RETURN, KEY_NUMPADENTER):
            if down:
                if self.currentMode == self.MODE_SELECT:
                    BWPersonality.GUICore.characterManagerEvent(self.EVENT_PLAY, None)
                elif self.currentMode == self.MODE_CREATE:
                    data = {'selections': {self.slotMap[0]: self.currentSelections[0],
                                    self.slotMap[1]: self.currentSelections[1],
                                    self.slotMap[2]: self.currentSelections[2],
                                    self.slotMap[3]: self.currentSelections[3],
                                    self.slotMap[4]: self.currentSelections[4]},
                     'input': self.component.createFrame.nameInput.script.getValue()}
                    BWPersonality.GUICore.characterManagerEvent(self.EVENT_MAKECHAR, data)
        return False

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        cmp = self.component.selectFrame.playBtn
        cmp.position = (sW / 2.0, sH - 100, 0.0)
        cmp = self.component.selectFrame.createNewBtn
        cmp.position = (50, sH - 100, 0.0)
        cmp = self.component.selectFrame.toMain
        cmp.position = (50, sH - 55, 0.0)
        cmp = self.component.selectFrame.delBtn
        cmp.position = (sW / 2.0, sH - 55, 0.0)
        cmp = self.component.selectFrame.renameBtn
        cmp.position = (sW / 2.0 + 180, sH - 100, 0.0)
        cmp = self.component.selectFrame.nameLabel
        cmp.position = (sW / 2.0, 100, 1.0)
        cmp = self.component.createFrame
        cmp.position = (sW / 2.0 - 155, sH / 2.0, 0.1)

    @PyGUIEvent('selectFrame.playBtn', 'onClick')
    def playBtnClicked(self):
        BWPersonality.GUICore.characterManagerEvent(self.EVENT_PLAY, None)
        return

    @PyGUIEvent('selectFrame.delBtn', 'onClick')
    def delBtnClicked(self):
        BWPersonality.GUICore.characterManagerEvent(self.EVENT_DELETE, None)
        return

    @PyGUIEvent('selectFrame.renameBtn', 'onClick')
    def renameBtnClicked(self):
        BWPersonality.GUICore.characterManagerEvent(self.EVENT_RENAME, None)
        return

    @PyGUIEvent('selectFrame.toMain', 'onClick')
    def mainBtnClicked(self):
        BWPersonality.GUICore.characterManagerEvent(self.EVENT_LOGOFF, None)
        return

    @PyGUIEvent('selectFrame.createNewBtn', 'onClick')
    def newCharBtnClicked(self):
        BWPersonality.GUICore.characterManagerEvent(self.EVENT_NEWCHAR, None)
        return

    @PyGUIEvent('createFrame.applyBtn', 'onClick')
    def applyBtnClicked(self):
        data = {'selections': {self.slotMap[0]: self.currentSelections[0],
                        self.slotMap[1]: self.currentSelections[1],
                        self.slotMap[2]: self.currentSelections[2],
                        self.slotMap[3]: self.currentSelections[3],
                        self.slotMap[4]: self.currentSelections[4]},
         'input': self.component.createFrame.nameInput.script.getValue()}
        BWPersonality.GUICore.characterManagerEvent(self.EVENT_MAKECHAR, data)

    @PyGUIEvent('createFrame.cancelBtn', 'onClick')
    def cancelBtnClicked(self):
        BWPersonality.GUICore.characterManagerEvent(self.EVENT_CANCELMAKE, None)
        return