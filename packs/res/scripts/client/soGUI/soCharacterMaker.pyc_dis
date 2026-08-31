# Embedded file name: scripts/client/soGUI/soCharacterMaker.py
import BigWorld
import BWPersonality
from Localization import lc
import GUI
from Helpers.PyGUI import PyGUIBase
from gui_const import GUI_ID, CHAR_MAKER
from soGUI.soTextField import soTextField3
from soGUI.soButton import soButton
from soGUI.soSlider import soSlider
from soGUI.soEditField import soEditBox
import ResMgr
from functools import partial
from Helpers.PyGUI import PyGUIEvent
from random import randint
from Keys import *
from DummyRotating import DummyRotating
import json
CONFIG_FILE = 'scripts/client/data/charMakerCfg.json'

class soCustomizationElement(PyGUIBase):
    factoryString = 'soGUI.soCustomizationElement'

    def __init__(self, component, data, choiceGroup):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.data = data
        self.choiceGroup = choiceGroup
        self.varCount = len(data.keys())
        self.currVar = 1
        self.setupRoot()
        self.setupContent()
        self.setVar(1)

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 240
        cmp.height = 43

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/charCreation/fon_tisnenie.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'decFrame')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 32
        cmp.height = 32
        cmp.position = (6, 5, 0.5)
        self.component.addChild(cmp, 'icon')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (160, 160, 150, 255)
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.materialFX = 'BLEND'
        cmp.position = (47, 13, 0.4)
        self.component.addChild(cmp, 'caption')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (160, 160, 150, 255)
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.materialFX = 'BLEND'
        cmp.position = (231, 13, 0.4)
        self.component.addChild(cmp, 'counter')
        slider = soSlider(GUI.Window(), width=184, height=8, steps=self.varCount, style='soGUI/visual_styles/settings_Slider.xml', default_settings_width=175)
        slider.onValueChanged = self._onSliderValue
        slider.onTargetChanged = self._onSliderTarget
        cmp = slider.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (47, 22, 0.3)
        self.component.addChild(cmp, 'slider')

    def setVar(self, varN, byUser = False):
        self.component.slider.script.setStep(varN - 1, byUser)
        self._applyVar()

    def _applyVar(self):
        if self.currVar:
            self.component.caption.text = lc(self.data[unicode(self.currVar)][u'caption'])
            self.component.counter.text = u'{0}/{1}'.format(self.currVar, self.varCount)
            self.component.icon.textureName = self.data[unicode(self.currVar)][u'icon']

    def _onSliderValue(self, step, val):
        if self.currVar == step + 1:
            return
        self.currVar = step + 1
        self._applyVar()
        BWPersonality.GUICore.charMakerEvent(CHAR_MAKER.EVENT_APPEARANCE, {'choiceGroup': self.choiceGroup,
         'var': self.data[unicode(self.currVar)]})

    def _onSliderTarget(self, step):
        if self.currVar == step + 1:
            return
        self.currVar = step + 1
        self._applyVar()
        BWPersonality.GUICore.charMakerEvent(CHAR_MAKER.EVENT_APPEARANCE, {'choiceGroup': self.choiceGroup,
         'var': self.data[unicode(self.currVar)]})

    def getMaxVar(self):
        return self.component.slider.script.steps

    def getCurrentChoice(self):
        return self.data[unicode(self.currVar)]


class soCharacterMakerGUI(PyGUIBase):
    factoryString = 'soGUI.soCharacterMakerGUI'
    hint_colors = {CHAR_MAKER.HINT_TYPE_NORMAL: (160,
                                   160,
                                   150,
                                   255),
     CHAR_MAKER.HINT_TYPE_ERROR: (208,
                                  90,
                                  32,
                                  255),
     CHAR_MAKER.HINT_TYPE_OK: (94,
                               202,
                               57,
                               255)}

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.interfaceID = GUI_ID.GUI_ID_CHARCREATE
        self.firstWnd = None
        self.secondWnd = None
        self.thirdWnd = None
        self.curStage = CHAR_MAKER.STAGE_1
        self.char_panning = False
        self.config = None
        self._loadConfig()
        self.setupRoot()
        self.setupShared()
        self.setupFirstStage()
        self.setupSecondStage()
        self.setupThirdStage()
        self.setCharacterSummary([])
        sw, sh = BigWorld.screenSize()
        self.relativ_300px = 1 - 600.0 / sw
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.visible = False
        cmp.position = (0.0, 0.0, 0.5)
        cmp.focus = True
        cmp.moveFocus = True

    def setupShared(self):
        sw, sh = BigWorld.screenSize()
        cmp = GUI.Simple('soGUI/maps/Login/frame_menu.dds')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.filterType = 'LINEAR'
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = sh
        cmp.position = (sw, 0, 0.25)
        self.component.addChild(cmp, 'decoStripesRight')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.width = 200
        cmp.height = 21
        cmp.textureName = ''
        cmp.position = (150, sh - 99, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.label.text = lc('GUI.CharacterMaker.NEXT_BUTTON_LABEL')
        self.component.addChild(cmp, 'nextBtn')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        btn.onClick = partial(self.onStageSwitchBtn, True)
        btn.onBound()
        btn._updateVisualState()
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.width = 200
        cmp.height = 21
        cmp.textureName = ''
        cmp.position = (150, sh - 59, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.label.text = lc('GUI.CharacterMaker.CANCEL_BUTTON_LABEL')
        self.component.addChild(cmp, 'cancelBtn')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        btn.onClick = partial(self.onStageSwitchBtn, False)
        btn.onBound()
        btn._updateVisualState()

    def setupFirstStage(self):
        sw, sh = BigWorld.screenSize()
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.2)
        cmp.visible = True
        self.component.addChild(cmp, 'firstWnd')
        self.firstWnd = cmp
        cmp = GUI.Simple('soGUI/maps/Login/frame_menu.dds')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.filterType = 'LINEAR'
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = sh
        cmp.position = (0, 0, 0.8)
        self.firstWnd.addChild(cmp, 'decoStripesLeft')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (74, 74, 74, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2
        cmp.height = sh
        cmp.position = (299, 0, 0.4)
        self.firstWnd.addChild(cmp, 'vLineL')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (74, 74, 74, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2
        cmp.height = sh
        cmp.position = (sw - 299, 0, 0.4)
        self.firstWnd.addChild(cmp, 'vLineR')
        cmp = GUI.Frame2('soGUI/maps/Login/blackout_1.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.filterType = 'LINEAR'
        cmp.materialFX = 'BLEND'
        cmp.width = sw - 600
        cmp.height = sh
        cmp.position = (300, 0, 0.7)
        self.firstWnd.addChild(cmp, 'bBG')
        cmp = GUI.Frame2('soGUI/maps/charCreation/fon_tisnenie.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 240
        cmp.height = 130
        cmp.position = (30, 43, 0.3)
        self.firstWnd.addChild(cmp, 'genderChoiceFrame')
        cmp = GUI.Frame2('soGUI/maps/charCreation/fon_tisnenie.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 240
        cmp.height = 130
        cmp.position = (30, 216, 0.3)
        self.firstWnd.addChild(cmp, 'factionChoiceFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (160, 160, 150, 255)
        cmp.font = 'ruRU_Verdana_21.font'
        cmp.materialFX = 'BLEND'
        cmp.text = lc('GUI.CharacterMaker.GENDER_CHOICE_LABEL')
        cmp.position = (42, 63, 0.2)
        self.firstWnd.addChild(cmp, 'genderChoiceLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (160, 160, 150, 255)
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.materialFX = 'BLEND'
        cmp.text = lc('GUI.CharacterMaker.GENDER_MALE')
        cmp.position = (42, 92, 0.2)
        self.firstWnd.addChild(cmp, 'genderMaleLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (160, 160, 150, 255)
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.materialFX = 'BLEND'
        cmp.text = lc('GUI.CharacterMaker.GENDER_FEMALE')
        cmp.position = (258, 92, 0.2)
        self.firstWnd.addChild(cmp, 'genderFemaleLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (160, 160, 150, 255)
        cmp.font = 'ruRU_Verdana_21.font'
        cmp.materialFX = 'BLEND'
        cmp.text = lc('GUI.CharacterMaker.ORIGINATION_CHOICE_LABEL')
        cmp.position = (42, 237, 0.2)
        self.firstWnd.addChild(cmp, 'originChoiceLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (160, 160, 150, 255)
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.materialFX = 'BLEND'
        cmp.text = lc('GUI.CharacterMaker.ORIGINATION_FOREIGN')
        cmp.position = (42, 262, 0.2)
        self.firstWnd.addChild(cmp, 'originationLabelForeign')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (160, 160, 150, 255)
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.materialFX = 'BLEND'
        cmp.text = lc('GUI.CharacterMaker.ORIGINATION_LOCAL')
        cmp.position = (258, 262, 0.2)
        self.firstWnd.addChild(cmp, 'originationLabelLocal')
        txt = soTextField3(GUI.Window(), width=240, height=435, textWidth=-1, hScroll=False, vScroll=False, hideScroll=False, borderWidth=0, vOffset=0, hOffset=0, textureless=True, autosize=False)
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (30, 375, 0.2)
        self.firstWnd.addChild(cmp, 'description')
        txt.onBound()
        txt.setText(u'')
        btn = soButton(GUI.Window())
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.buttonActive = True
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 97
        cmp.height = 56
        cmp.textureName = ''
        cmp.position = (42, 104, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.firstWnd.addChild(cmp, 'genderMaleBtn')
        btn.initVSC('soGUI/visual_styles/createBtnMan.xml')
        btn.onClick = partial(self.onGenderBtn, 'male')
        btn.onBound()
        btn._updateVisualState()
        btn = soButton(GUI.Window())
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 97
        cmp.height = 56
        cmp.textureName = ''
        cmp.position = (161, 104, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.firstWnd.addChild(cmp, 'genderFemaleBtn')
        btn.initVSC('soGUI/visual_styles/createBtnWoman.xml')
        btn.onClick = partial(self.onGenderBtn, 'female')
        btn.onBound()
        btn._updateVisualState()
        btn = soButton(GUI.Window())
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 97
        cmp.height = 56
        cmp.textureName = ''
        cmp.position = (161, 277, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.firstWnd.addChild(cmp, 'originLocalBtn')
        btn.initVSC('soGUI/visual_styles/createBtnKoren.xml')
        btn.onClick = partial(self.onOriginBtn, 'local')
        btn.onBound()
        btn._updateVisualState()
        btn = soButton(GUI.Window())
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.buttonActive = True
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 97
        cmp.height = 56
        cmp.textureName = ''
        cmp.position = (42, 277, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.firstWnd.addChild(cmp, 'originForeignBtn')
        btn.initVSC('soGUI/visual_styles/createBtnPrishl.xml')
        btn.onClick = partial(self.onOriginBtn, 'foreign')
        btn.onBound()
        btn._updateVisualState()

    def setupSecondStage(self):
        sw, sh = BigWorld.screenSize()
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.2)
        cmp.visible = False
        self.component.addChild(cmp, 'secondWnd')
        self.secondWnd = cmp
        cmp = GUI.Simple('soGUI/maps/Login/frame_menu.dds')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.filterType = 'LINEAR'
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = sh
        cmp.position = (0, 0, 0.8)
        self.secondWnd.addChild(cmp, 'decoStripesLeft')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (74, 74, 74, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2
        cmp.height = sh
        cmp.position = (299, 0, 0.4)
        self.secondWnd.addChild(cmp, 'vLineL')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (74, 74, 74, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2
        cmp.height = sh
        cmp.position = (sw - 299, 0, 0.4)
        self.secondWnd.addChild(cmp, 'vLineR')
        cmp = GUI.Frame2('soGUI/maps/Login/blackout_1.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.filterType = 'LINEAR'
        cmp.materialFX = 'BLEND'
        cmp.width = sw - 600
        cmp.height = sh
        cmp.position = (300, 0, 0.7)
        self.secondWnd.addChild(cmp, 'bBG')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Verdana_21.font'
        cmp.colour = (160, 160, 150, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('GUI.CharacterMaker.APPEARANCE_CAPTION')
        cmp.position = (30, 38, 0.4)
        self.secondWnd.addChild(cmp, 'appearanceCaption')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Verdana_21.font'
        cmp.colour = (160, 160, 150, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('GUI.CharacterMaker.Equipment')
        cmp.position = (30, 137, 0.4)
        self.secondWnd.addChild(cmp, 'EquipmntCaption')
        choiceH = 0
        if self.config:
            keys = self.config.keys()
            keys.sort()
            for index, choiceGroup in enumerate(keys):
                if index == 0:
                    choiceH = 59 + 72 * index
                else:
                    choiceH = 79 + 72 * index
                choiceElem = soCustomizationElement(GUI.Window(), self.config[choiceGroup], choiceGroup)
                cmp = choiceElem.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.position = (30, choiceH, 0.4)
                self.secondWnd.addChild(cmp, 'choice_{0}'.format(choiceGroup))

        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 145
        cmp.height = 36
        cmp.textureName = ''
        cmp.position = (125, choiceH + 72, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.label.text = lc('GUI.CharacterMaker.RANDOM_CUSTOMIZATION_BUTTON_LABEL')
        self.secondWnd.addChild(cmp, 'randomizeBtn')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnOption.xml')
        btn.onClick = self.onRandomizeBtn
        btn.onBound()
        btn._updateVisualState()

    def setupThirdStage(self):
        sw, sh = BigWorld.screenSize()
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.2)
        cmp.visible = False
        self.component.addChild(cmp, 'thirdWnd')
        self.thirdWnd = cmp
        cmp = GUI.Simple('soGUI/maps/Login/frame_menu.dds')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.filterType = 'LINEAR'
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = sh
        cmp.position = (0, 0, 0.8)
        self.thirdWnd.addChild(cmp, 'decoStripesLeft')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (74, 74, 74, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2
        cmp.height = sh
        cmp.position = (299, 0, 0.4)
        self.thirdWnd.addChild(cmp, 'vLineL')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (74, 74, 74, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2
        cmp.height = sh
        cmp.position = (sw - 299, 0, 0.4)
        self.thirdWnd.addChild(cmp, 'vLineR')
        cmp = GUI.Frame2('soGUI/maps/Login/blackout_1.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.filterType = 'LINEAR'
        cmp.materialFX = 'BLEND'
        cmp.width = sw - 600
        cmp.height = sh
        cmp.position = (300, 0, 0.7)
        self.thirdWnd.addChild(cmp, 'bBG')
        edit = soEditBox(GUI.Window(), width=240, height=23, font='ruRU_Cyrvetica_Extra_14i.font', hOffset=3, vOffset=2)
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (30, 35, 0.5)
        self.thirdWnd.addChild(cmp, 'nameEdit')
        edit.onValueChange = self.onEditValue
        edit.onBound()
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (160, 160, 150, 255)
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.materialFX = 'BLEND'
        cmp.text = u''
        cmp.position = (150, 73, 0.2)
        self.thirdWnd.addChild(cmp, 'nameAccessHint')
        txt = soTextField3(GUI.Window(), width=240, height=600, textWidth=-1, hScroll=False, vScroll=False, hideScroll=False, borderWidth=0, vOffset=0, hOffset=0, textureless=True, autosize=False)
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (30, 100, 0.2)
        self.thirdWnd.addChild(cmp, 'description')
        txt.onBound()

    def show(self, stage):
        if self.component.parent is None:
            BWPersonality.GUICore.menuLayer.addChild(self.component, 'charMaker')
        self.component.visible = True
        self.setStage(stage)
        return

    def hide(self):
        self.component.visible = False

    def _loadConfig(self):
        dataSection = ResMgr.openSection(CONFIG_FILE)
        self.config = json.loads(dataSection.asBinary)

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
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'CENTER'
            cmp.colour = (160, 160, 150, 255)
            cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
            cmp.materialFX = 'BLEND'
            cmp.text = entry[0]
            cmp.position = (sw - 268, 30 + 17 * index, 0.2)
            self.component.addChild(cmp, 'char_summary_caption{0}'.format(index))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'RIGHT'
            cmp.verticalAnchor = 'CENTER'
            cmp.colour = (160, 160, 150, 255)
            cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
            cmp.materialFX = 'BLEND'
            cmp.text = entry[1]
            cmp.position = (sw - 30, 30 + 17 * index, 0.2)
            self.component.addChild(cmp, 'char_summary_val{0}'.format(index))

        return

    def setFirstDescription(self, text):
        self.firstWnd.description.script.setText(text)

    def setThirdDescription(self, text):
        self.thirdWnd.description.script.setText(text)

    def setNicknameHint(self, text, type):
        self.thirdWnd.nameAccessHint.text = text
        self.thirdWnd.nameAccessHint.colour = self.hint_colors[type]

    def setNicknameValidator(self, validator):
        self.thirdWnd.nameEdit.script.setValidator(validator)

    def setStage(self, stage):
        if stage == self.curStage or stage not in [CHAR_MAKER.STAGE_1, CHAR_MAKER.STAGE_2, CHAR_MAKER.STAGE_3]:
            return
        self.firstWnd.visible = False
        self.secondWnd.visible = False
        self.thirdWnd.visible = False
        self.curStage = stage
        if stage == CHAR_MAKER.STAGE_1:
            self.firstWnd.visible = True
            self.component.nextBtn.label.text = lc('GUI.CharacterMaker.NEXT_BUTTON_LABEL')
            self.component.cancelBtn.label.text = lc('GUI.CharacterMaker.CANCEL_BUTTON_LABEL')
            self.thirdWnd.nameEdit.script.activate(False)
        elif stage == CHAR_MAKER.STAGE_2:
            self.secondWnd.visible = True
            self.component.nextBtn.label.text = lc('GUI.CharacterMaker.NEXT_BUTTON_LABEL')
            self.component.cancelBtn.label.text = lc('GUI.CharacterMaker.BACK_BUTTON_LABEL')
            self.thirdWnd.nameEdit.script.activate(False)
        elif stage == CHAR_MAKER.STAGE_3:
            self.thirdWnd.visible = True
            self.component.nextBtn.label.text = lc('GUI.CharacterMaker.FINISH_BUTTON_LABEL')
            self.component.cancelBtn.label.text = lc('GUI.CharacterMaker.BACK_BUTTON_LABEL')
            self.thirdWnd.nameEdit.script.activate(True)
        BWPersonality.GUICore.charMakerEvent(CHAR_MAKER.EVENT_STAGESWITCH, {'stage': stage})

    def doResposition(self):
        sw, sh = BigWorld.screenSize()
        self.component.decoStripesRight.height = sh
        self.component.decoStripesRight.position.x = sw
        self.component.nextBtn.position.y = sh - 99
        self.component.cancelBtn.position.y = sh - 59
        self.firstWnd.decoStripesLeft.height = sh
        self.firstWnd.vLineL.height = sh
        self.firstWnd.vLineR.height = sh
        self.firstWnd.vLineR.position = (sw - 299, 0, 0.4)
        self.firstWnd.bBG.width = sw - 600
        self.firstWnd.bBG.height = sh
        self.secondWnd.decoStripesLeft.height = sh
        self.secondWnd.vLineL.height = sh
        self.secondWnd.vLineR.height = sh
        self.secondWnd.vLineR.position = (sw - 299, 0, 0.4)
        self.secondWnd.bBG.width = sw - 600
        self.secondWnd.bBG.height = sh
        self.thirdWnd.decoStripesLeft.height = sh
        self.thirdWnd.vLineL.height = sh
        self.thirdWnd.vLineR.height = sh
        self.thirdWnd.vLineR.position = (sw - 299, 0, 0.4)
        self.thirdWnd.bBG.width = sw - 600
        self.thirdWnd.bBG.height = sh
        self._repositionChSummary()

    def onGenderBtn(self, btn):
        self.firstWnd.genderMaleBtn.script.buttonActive = False
        self.firstWnd.genderFemaleBtn.script.buttonActive = False
        if btn == 'male':
            self.firstWnd.genderMaleBtn.script.buttonActive = True
            BWPersonality.GUICore.charMakerEvent(CHAR_MAKER.EVENT_GENDER_CHOICE, {'gender': CHAR_MAKER.GENDER_MALE})
        elif btn == 'female':
            self.firstWnd.genderFemaleBtn.script.buttonActive = True
            BWPersonality.GUICore.charMakerEvent(CHAR_MAKER.EVENT_GENDER_CHOICE, {'gender': CHAR_MAKER.GENDER_FEMALE})
        self.firstWnd.genderMaleBtn.script._updateVisualState()
        self.firstWnd.genderFemaleBtn.script._updateVisualState()

    def onOriginBtn(self, btn):
        self.firstWnd.originLocalBtn.script.buttonActive = False
        self.firstWnd.originForeignBtn.script.buttonActive = False
        if btn == 'local':
            self.firstWnd.originLocalBtn.script.buttonActive = True
            BWPersonality.GUICore.charMakerEvent(CHAR_MAKER.EVENT_ORIGINATION_CHOICE, {'origination': CHAR_MAKER.ORIGINATION_LOCALS})
        elif btn == 'foreign':
            self.firstWnd.originForeignBtn.script.buttonActive = True
            BWPersonality.GUICore.charMakerEvent(CHAR_MAKER.EVENT_ORIGINATION_CHOICE, {'origination': CHAR_MAKER.ORIGINATION_FOREIGNERS})
        self.firstWnd.originLocalBtn.script._updateVisualState()
        self.firstWnd.originForeignBtn.script._updateVisualState()

    def onStageSwitchBtn(self, forward = True):
        if forward:
            if self.curStage + 1 in [CHAR_MAKER.STAGE_1, CHAR_MAKER.STAGE_2, CHAR_MAKER.STAGE_3]:
                self.setStage(self.curStage + 1)
            elif self.curStage == CHAR_MAKER.STAGE_3:
                BWPersonality.GUICore.charMakerEvent(CHAR_MAKER.EVENT_FINISH, {})
        else:
            BWPersonality.GUICore.charMakerEvent(CHAR_MAKER.EVENT_CANCEL, {})

    def onEditValue(self, byUser):
        nick = self.thirdWnd.nameEdit.script.getRaw()
        BWPersonality.GUICore.charMakerEvent(CHAR_MAKER.EVENT_NICKNAME, {'nick': nick})

    def onRandomizeBtn(self):
        for name, child in self.secondWnd.children:
            if name.startswith('choice_'):
                maxLim = child.script.getMaxVar()
                child.script.setVar(randint(1, maxLim), True)

    def getCurrentAppearance(self):
        retval = {}
        if self.config:
            keys = self.config.keys()
            for choiceGroup in keys:
                setter_obj = getattr(self.component.secondWnd, 'choice_{0}'.format(choiceGroup)).script
                retval[choiceGroup] = setter_obj.getCurrentChoice()

        return retval

    def handleKeyEvent(self, event):
        key = event.key
        down = event.isKeyDown()
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
        if self.char_panning:
            DummyRotating().rotate(event.dx)
            return True
        return False