# Embedded file name: scripts/client/soGUI/soSkillScreen.py
import GUI
import soGUI
import Helpers.PyGUI as PyGUI
import BigWorld
import BWPersonality
import CharacterUtils
from soGUI.soButton import soButton, soButtonWTT, soButtonWFT
import Helpers.PyGUI.TextStyles as TextStyles
import Helpers.PyGUI.Utils as Utils
from Helpers.PyGUI.VisualStateComponent import VisualState
from soGUI.soVisualStateComponent import soVisualStateComponent
from soGUI.soToolTipComponent import soToolTipComponent
from soGUI.soScrollBar import soScrollBar
from soGUI.soDropDownList import soDropDownList
from soGUI.soTextField import soTextField
from soGUI.soList import soList2, soList2ElementBase
from soGUI.soItemView import soItemView, soItemSlot
import soGUI.soItemView as module_soItemView
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI import PyGUIBase
from Helpers.BWCoroutine import *
from CharacterUtils import CharacterConst
from soGUI.soEditField import soEditBox
from soGUI.soTextField import soTextField3
import CharacterUtils
from functools import partial
from gui_const import LEVELING, GUI_ID
from Keys import *
from Localization import lc
import math
from math import floor, ceil

class soSkillScreen(PyGUI.Window):
    factoryString = 'soGUI.soSkillScreen'
    EVENT_SELECT = 0
    EVENT_LEARNSKILL = 1
    EVENT_LEARNFEAT = 2

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        component.script = self
        self.skillData = {}
        self.currentTree = None
        self.currentSkill = None
        self.currentFeat = None
        self.treeNames = {'Combat': lc('soSkillScreen.soGUI.STRING_66_16'),
         'Other': lc('soSkillScreen.soGUI.STRING_67_15')}
        self.skillNames = {'LightWeapon': lc('soSkillScreen.soGUI.STRING_71_21'),
         'AssaultRifles': lc('soSkillScreen.soGUI.STRING_72_23'),
         'HeavyWeapon': lc('soSkillScreen.soGUI.STRING_73_21'),
         'Rifles': lc('soSkillScreen.soGUI.STRING_74_16'),
         'Throwing': lc('soSkillScreen.soGUI.STRING_75_18'),
         'ShootingOnMove': lc('soSkillScreen.soGUI.STRING_76_24'),
         'Metabolism': lc('soSkillScreen.soGUI.STRING_77_20'),
         'Medicine': lc('soSkillScreen.soGUI.STRING_78_18'),
         'Repair': lc('soSkillScreen.soGUI.STRING_79_16'),
         'Modification': lc('soSkillScreen.soGUI.STRING_80_22'),
         'Luck': lc('soSkillScreen.soGUI.STRING_81_14'),
         'Neatness': lc('soSkillScreen.soGUI.STRING_82_18'),
         'Packing': lc('soSkillScreen.soGUI.STRING_83_17'),
         'Sportsmanship': lc('soSkillScreen.soGUI.STRING_84_23')}
        self.setupRoot()
        self.setupDDLists()
        self.setupBtns()
        self.setupInfoField()
        self.setupLabels()
        self.selTree('Combat')
        self.update()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 470
        cmp.height = 236
        cmp.position = (0.0, 0.0, 0.1)
        cmp.textureName = ''
        BigWorld.player().playerGUI.addChild(cmp, 'skillGUI')
        BigWorld.player().playerGUI.script.onBound()
        mainFrame = GUI.Frame2('soGUI/maps/Controls/skills/skillFrame.tga')
        mainFrame.colour = (255, 255, 255, 255)
        mainFrame.materialFX = 'BLEND'
        mainFrame.horizontalPositionMode = mainFrame.verticalPositionMode = 'PIXEL'
        mainFrame.widthMode = mainFrame.heightMode = 'PIXEL'
        mainFrame.horizontalAnchor = 'LEFT'
        mainFrame.verticalAnchor = 'TOP'
        mainFrame.width = 463
        mainFrame.height = 229
        mainFrame.position = (0, 7, 0.9)
        cmp.addChild(mainFrame, 'mainFrame')

    def setupDDLists(self):
        cmp = GUI.Window()
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 223
        cmp.height = 150
        cmp.position = (16, 25, 0.1)
        treeDDL = soDropDownList(cmp, soGUI.DropDownListPropsStructure(DDLWidth=223, DDLHeight=150, btnW=29, btnH=29, DDLElemHeight=18))
        treeDDL.onBound()
        self.component.addChild(cmp, 'treeDDL')
        cmp = GUI.Window()
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 223
        cmp.height = 150
        cmp.position = (16, 67, 0.2)
        skillDDL = soDropDownList(cmp, soGUI.DropDownListPropsStructure(DDLWidth=223, DDLHeight=150, btnW=29, btnH=29, DDLElemHeight=18))
        self.component.addChild(cmp, 'skillDDL')
        skillDDL.onBound()
        cmp = GUI.Window()
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 223
        cmp.height = 120
        cmp.position = (16, 109, 0.3)
        featDDL = soDropDownList(cmp, soGUI.DropDownListPropsStructure(DDLWidth=223, DDLHeight=120, btnW=29, btnH=29, DDLElemHeight=18))
        self.component.addChild(cmp, 'featDDL')
        featDDL.onBound()

    def setupBtns(self):
        closeBox = soButton(GUI.Window())
        cmp = closeBox.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (452, 0, 0.1)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        learnBtnSkill = soButton(GUI.Window())
        cmp = learnBtnSkill.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 64
        cmp.height = 29
        cmp.position = (247, 67, 0.1)
        learnBtnSkill.initVSC('soGUI/visual_styles/defaultBtn.xml')
        learnBtnSkill.buttonDisabled = True
        learnBtnSkill.onBound()
        learnBtnSkill.setVisualState('disabled')
        cmp.label.text = lc('soSkillScreen.soGUI.STRING_228_19')
        self.component.addChild(cmp, 'learnBtnSkill')
        learnBtnFeat = soButton(GUI.Window())
        cmp = learnBtnFeat.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 64
        cmp.height = 29
        cmp.position = (247, 109, 0.1)
        learnBtnFeat.initVSC('soGUI/visual_styles/defaultBtn.xml')
        learnBtnFeat.buttonDisabled = True
        learnBtnFeat.onBound()
        learnBtnFeat.setVisualState('disabled')
        cmp.label.text = lc('soSkillScreen.soGUI.STRING_248_19')
        self.component.addChild(cmp, 'learnBtnFeat')

    def setupInfoField(self):
        txtComp = GUI.Window()
        cmp = txtComp
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalAnchor = 'LEFT'
        cmp.width = 428
        cmp.height = 72
        cmp.position = (17, 152, 0.4)
        txt = soTextField(cmp, True)
        txt.textFrame.textureName = ''
        txt.frameTopOffset = 0
        txt.frameLeftOffset = 0
        self.component.addChild(txt.component, 'infoText')
        txt.doLayout()
        txt.onBound()
        txt.delText()
        txt.addText(u'', False)

    def setupLabels(self):
        level = GUI.Text('')
        level.horizontalPositionMode = level.verticalPositionMode = 'PIXEL'
        level.horizontalAnchor = 'LEFT'
        level.verticalAnchor = 'TOP'
        level.colour = (175, 166, 112, 255)
        level.materialFX = 'BLEND'
        level.font = 'ruRU_calibri_default.font'
        level.text = lc('soSkillScreen.soGUI.STRING_287_15')
        level.position = (317, 26, 0.1)
        self.component.addChild(level, 'level')
        exp = GUI.Text('')
        exp.horizontalPositionMode = exp.verticalPositionMode = 'PIXEL'
        exp.horizontalAnchor = 'LEFT'
        exp.verticalAnchor = 'TOP'
        exp.colour = (175, 166, 112, 255)
        exp.materialFX = 'BLEND'
        exp.font = 'ruRU_calibri_default.font'
        exp.text = lc('soSkillScreen.soGUI.STRING_301_13')
        exp.position = (317, 41, 0.1)
        self.component.addChild(exp, 'exp')
        skillPoints = GUI.Text('')
        skillPoints.horizontalPositionMode = skillPoints.verticalPositionMode = 'PIXEL'
        skillPoints.horizontalAnchor = 'LEFT'
        skillPoints.verticalAnchor = 'TOP'
        skillPoints.colour = (175, 166, 112, 255)
        skillPoints.materialFX = 'BLEND'
        skillPoints.font = 'ruRU_calibri_default.font'
        skillPoints.text = lc('soSkillScreen.soGUI.STRING_315_21')
        skillPoints.position = (317, 74, 0.1)
        self.component.addChild(skillPoints, 'skillPoints')
        FeatPoints = GUI.Text('')
        FeatPoints.horizontalPositionMode = FeatPoints.verticalPositionMode = 'PIXEL'
        FeatPoints.horizontalAnchor = 'LEFT'
        FeatPoints.verticalAnchor = 'TOP'
        FeatPoints.colour = (175, 166, 112, 255)
        FeatPoints.materialFX = 'BLEND'
        FeatPoints.font = 'ruRU_calibri_default.font'
        FeatPoints.text = lc('soSkillScreen.soGUI.STRING_329_20')
        FeatPoints.position = (317, 116, 0.1)
        self.component.addChild(FeatPoints, 'FeatPoints')

    def selTree(self, treeName):
        self.component.learnBtnSkill.script.buttonDisabled = True
        self.component.learnBtnSkill.script.setVisualState('disabled')
        self.component.learnBtnFeat.script.buttonDisabled = True
        self.component.learnBtnFeat.script.setVisualState('disabled')
        self.currentTree = treeName
        self.component.skillDDL.script.setSelection('')
        self.component.featDDL.script.setSelection('')
        skills = BWPersonality.GUICore.skillsDataSection[treeName][0]
        self.component.treeDDL.script.setSelection(self.treeNames[treeName])
        self.component.skillDDL.script.clear()
        self.component.featDDL.script.clear()
        for skill in skills.keys():
            self.component.skillDDL.script.addElement(self.skillNames[skill])

        BWPersonality.GUICore.skillEvent(treeName, self.EVENT_SELECT)

    def selSkill(self, skillName):
        self.component.learnBtnFeat.script.buttonDisabled = True
        self.component.learnBtnFeat.script.setVisualState('disabled')
        self.component.featDDL.script.setSelection('')
        availableFeats = BWPersonality.GUICore.skillsDataSection[self.currentTree][0][skillName]['AviablePerks']
        self.component.featDDL.script.clear()
        for feat in availableFeats:
            self.component.featDDL.script.addElement(BigWorld.player().GetPerkName(feat))

        self.component.skillDDL.script.setSelection(self.skillNames[skillName])
        if self.component.skillDDL.script.getSelection() != '' and BWPersonality.GUICore.skillsDataSection[self.currentTree][3] > 0:
            self.component.learnBtnSkill.script.buttonDisabled = False
            self.component.learnBtnSkill.script.setVisualState('normal')
        self.currentSkill = skillName
        BWPersonality.GUICore.skillEvent(skillName, self.EVENT_SELECT)

    def selFeat(self, feat):
        if self.component.featDDL.script.getSelection() != '' and BWPersonality.GUICore.skillsDataSection[self.currentTree][4] > 0:
            self.component.learnBtnFeat.script.buttonDisabled = False
            self.component.learnBtnFeat.script.setVisualState('normal')
        self.currentFeat = feat
        BWPersonality.GUICore.skillEvent(feat, self.EVENT_SELECT)

    def show(self):
        self.component.visible = True
        if self.component.parent is None:
            BigWorld.player().playerGUI.addChild(self.component, 'skillGUI')
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def setInfo(self, text):
        txt = self.component.infoText.script
        txt.delText()
        txt.addText(text, False)

    def update(self):
        if self.currentTree is not None:
            self.selTree(self.currentTree)
        if self.currentSkill is not None:
            self.selSkill(self.currentSkill)
        for tree in BWPersonality.GUICore.skillsDataSection:
            self.component.treeDDL.script.addElement(self.treeNames[tree])

        if self.currentTree is not None:
            self.selTree(self.currentTree)
        if self.currentSkill is not None:
            self.selSkill(self.currentSkill)
        if self.currentFeat is not None:
            self.selFeat(self.currentFeat)
        if self.currentTree is None:
            return
        else:
            EXP = BWPersonality.GUICore.skillsDataSection[self.currentTree][1]
            LVL = BWPersonality.GUICore.skillsDataSection[self.currentTree][2]
            SPs = BWPersonality.GUICore.skillsDataSection[self.currentTree][3]
            FPs = BWPersonality.GUICore.skillsDataSection[self.currentTree][4]
            self.component.level.text = lc('soSkillScreen.soGUI.STRING_443_30') + str(LVL)
            self.component.exp.text = lc('soSkillScreen.soGUI.STRING_444_28') + str(EXP)
            self.component.skillPoints.text = lc('soSkillScreen.soGUI.STRING_445_36') + str(SPs)
            self.component.FeatPoints.text = lc('soSkillScreen.soGUI.STRING_446_35') + str(FPs)
            return

    def getCurrentTree(self):
        return self.currentTree

    def getCurrentSkill(self):
        return self.currentSkill

    def getCurrentFeat(self):
        return self.currentFeat

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()

    @PyGUIEvent('treeDDL', 'onSelect')
    def onTreeSel(self):
        treeName_en = ''
        for index, name in self.treeNames.items():
            if self.component.treeDDL.script.getSelection() == name:
                treeName_en = index

        self.selTree(treeName_en)
        self.update()

    @PyGUIEvent('skillDDL', 'onSelect')
    def onSkillSel(self):
        skillName_en = ''
        for index, name in self.skillNames.items():
            if self.component.skillDDL.script.getSelection() == name:
                skillName_en = index

        self.selSkill(skillName_en)

    @PyGUIEvent('featDDL', 'onSelect')
    def onFeatSel(self):
        self.selFeat(self.component.featDDL.script.getSelection())

    @PyGUIEvent('learnBtnSkill', 'onClick')
    def onSkillLearn(self):
        skillName_en = ''
        for index, name in self.skillNames.items():
            if self.component.skillDDL.script.getSelection() == name:
                skillName_en = index

        BWPersonality.GUICore.skillEvent(skillName_en, self.EVENT_LEARNSKILL)

    @PyGUIEvent('learnBtnFeat', 'onClick')
    def onFeatLearn(self):
        skillName_en = ''
        for index, name in self.skillNames.items():
            if self.component.skillDDL.script.getSelection() == name:
                skillName_en = index

        BWPersonality.GUICore.skillEvent((skillName_en, self.component.featDDL.script.getSelection()), self.EVENT_LEARNFEAT)


class soFeatSlotVisualState(VisualState):

    def __init__(self):
        VisualState.__init__(self)
        self.textStyle = ''
        self.iconTextureName = ''
        self.iconTextureMapping = None
        self.iconColour = (255, 255, 255, 255)
        return

    def onSave(self, dataSection):
        VisualState.onSave(self, dataSection)
        if self.textStyle:
            dataSection.writeString('textStyle', self.textStyle)
        iconSection = dataSection.createSection('icon')
        iconSection.writeString('textureName', self.iconTextureName)
        iconSection.writeString('materialFX', self.iconMaterialFX)
        if self.iconTextureMapping:
            mappingSection = iconSection.createSection('mapping')
            self._writeMappingSection(mappingSection, self.iconTextureMappingType, self.iconTextureMapping)
        iconSection.writeVector4('colour', self.iconColour)

    def onLoad(self, dataSection):
        VisualState.onLoad(self, dataSection)
        if dataSection.has_key('icon'):
            iconSection = dataSection._icon
            self.iconMaterialFX = iconSection.readString('materialFX', '')
            self.iconTextureName = iconSection.readString('textureName', '')
            if iconSection.has_key('mapping'):
                mappingSection = iconSection._mapping
                mappingType, mapping = self._readMappingSection(mappingSection)
                self.iconTextureMappingType = mappingType
                self.iconTextureMapping = mapping
            else:
                self.iconTextureMapping = None
            self.iconColour = iconSection.readVector4('colour', (255, 255, 255, 255))
        return

    def apply(self, componentScript):
        VisualState.apply(self, componentScript)
        if hasattr(componentScript, 'buttonIcon'):
            if self.iconTextureName != '':
                componentScript.buttonIcon.textureName = self.iconTextureName
            if self.iconTextureMapping:
                Utils.applyMapping(componentScript.buttonIcon, self.iconTextureMappingType, self.iconTextureMapping)
            componentScript.buttonIcon.colour = self.iconColour
            if self.iconMaterialFX != '':
                componentScript.buttonIcon.materialFX = self.iconMaterialFX
            else:
                componentScript.buttonIcon.materialFX = 'BLEND'


class soFeatSlot(PyGUI.PyGUIBase, soVisualStateComponent, soToolTipComponent):
    factoryString = 'soGUI.soFeatSlot'
    visualStateString = 'soGUI.soButtonVisualState'

    def __init__(self, component):
        PyGUI.PyGUIBase.__init__(self, component)
        soVisualStateComponent.__init__(self, component, soFeatSlot.visualStateString)
        soToolTipComponent.__init__(self, component, None)
        component.script = self
        self.buttonIcon = self.component
        self.interfaceID = BWPersonality.GUICore.GUI_ID_SKILLS
        return

    def handleMouseEnterEvent(self, component):
        soToolTipComponent.handleMouseEnterEvent(self, component)
        return True

    def handleMouseLeaveEvent(self, component):
        soToolTipComponent.handleMouseLeaveEvent(self, component)
        return True


class soLearnFeatBtn(soButton, soToolTipComponent):
    factoryString = 'soGUI.soLearnFeatBtn'

    def __init__(self, component):
        soButton.__init__(self, component)
        soToolTipComponent.__init__(self, component, None)
        component.script = self
        self.interfaceID = BWPersonality.GUICore.GUI_ID_SKILLS
        return

    def handleMouseEnterEvent(self, component):
        soButton.handleMouseEnterEvent(self, component)
        soToolTipComponent.handleMouseEnterEvent(self, component)
        return True

    def handleMouseLeaveEvent(self, component):
        soButton.handleMouseLeaveEvent(self, component)
        soToolTipComponent.handleMouseLeaveEvent(self, component)
        return True


class soSkillScreen2(PyGUI.Window):
    factoryString = 'soGUI.soSkillScreen2'
    EVENT_SELECT = 0
    EVENT_LEARNSKILL = 1
    EVENT_LEARNFEAT = 2
    FRAME_TEXTURE = 'soGUI/maps/Controls/skills/skillFrame.tga'
    TAB_HEIGHT = 30
    TAB_WIDTH = 148
    WINDOW_BORDERW = 4
    TAB_LEFT_OFFSET = 24
    SCREEN_WIDTH = 532
    SCREEN_HEIGHT = 350
    TYPICAL_OFFSET = 4
    TAB_COMBAT = 0
    TAB_SURVIVAL = 1
    TAB_SUPPORT = 2
    SKILL_BOX_HEIGHT = 80
    SKILL_BOX_INTERVAL = 5
    SCROLL_WIDTH = 16
    SMALL_BTN_SIZE = 16
    PERKS_PER_SKILL = 12
    FEATSLOT_HEIGHT = 40
    SKILL_BACK_TEXTURE = 'soGUI/maps/Controls/skills/skillBack.tga'
    DELIMETER_TEXTURE = 'soGUI/maps/Controls/skills/line.tga'
    TAB_LABELS = {TAB_COMBAT: lc('soSkillScreen.soGUI.STRING_638_16'),
     TAB_SURVIVAL: lc('soSkillScreen.soGUI.STRING_639_18'),
     TAB_SUPPORT: lc('soSkillScreen.soGUI.STRING_640_17')}

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        component.script = self
        self.tabs = {}
        self.currentTab = soSkillScreen2.TAB_COMBAT
        self.combatWnd = None
        self.survWnd = None
        self.supportWnd = None
        self.combatSkills = {}
        self.survivalSkills = {}
        self.craftSkills = {}
        self.setupRoot()
        self.setupFrame()
        self.setupCombatWnd()
        self.setupSurvWnd()
        self.setupSupportWnd()
        self.setupTabs()
        self.setupTreeInfo()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = self.SCREEN_WIDTH
        cmp.height = self.SCREEN_HEIGHT
        cmp.visible = False
        cmp.textureName = ''
        cmp.moveFocus = True
        cmp.dragFocus = True
        cmp.position = (-0.5, 0.5, 0.0)

    def setupFrame(self):
        frameCmp = GUI.Frame2(soSkillScreen2.FRAME_TEXTURE)
        frameCmp.verticalPositionMode = frameCmp.horizontalPositionMode = 'CLIP'
        frameCmp.widthMode = frameCmp.heightMode = 'PIXEL'
        frameCmp.horizontalAnchor = 'CENTER'
        frameCmp.verticalAnchor = 'BOTTOM'
        frameCmp.width = self.SCREEN_WIDTH
        frameCmp.height = self.SCREEN_HEIGHT - self.TAB_HEIGHT + 4
        frameCmp.position = (0.0, -1.0, 0.5)
        frameCmp.colour = (255, 255, 255, 255)
        frameCmp.materialFX = 'BLEND'
        frameCmp.visible = True
        self.component.addChild(frameCmp, 'frame')
        topLine = GUI.Simple(self.DELIMETER_TEXTURE)
        topLine.tiled = True
        topLine.tileHeight = 1
        topLine.tileWidth = 1
        topLine.verticalPositionMode = topLine.horizontalPositionMode = 'CLIP'
        topLine.widthMode = topLine.heightMode = 'PIXEL'
        topLine.horizontalAnchor = 'LEFT'
        topLine.verticalAnchor = 'TOP'
        topLine.width = self.SCREEN_WIDTH - self.WINDOW_BORDERW * 2
        topLine.height = 1
        topLine.position = (-1.0 + soGUI.getPixelWidth(self.component) * self.WINDOW_BORDERW, 1.0 - soGUI.getPixelHeight(self.component) * (29 + self.TAB_HEIGHT), 0.0)
        self.component.addChild(topLine, 'topLine')
        bottomLine = GUI.Simple(self.DELIMETER_TEXTURE)
        bottomLine.tiled = True
        bottomLine.tileHeight = 1
        bottomLine.tileWidth = 1
        bottomLine.verticalPositionMode = bottomLine.horizontalPositionMode = 'CLIP'
        bottomLine.widthMode = bottomLine.heightMode = 'PIXEL'
        bottomLine.horizontalAnchor = 'LEFT'
        bottomLine.verticalAnchor = 'BOTTOM'
        bottomLine.width = self.SCREEN_WIDTH - self.WINDOW_BORDERW * 2
        bottomLine.height = 1
        bottomLine.position = (-1.0 + soGUI.getPixelWidth(self.component) * self.WINDOW_BORDERW, -1.0 + soGUI.getPixelHeight(self.component) * 29, 0.0)
        self.component.addChild(bottomLine, 'bottomLine')
        scrollComp = GUI.Window()
        vScroll = soScrollBar(scrollComp)
        vScroll.component.widthMode = vScroll.component.heightMode = 'PIXEL'
        vScroll.component.width = self.SCROLL_WIDTH
        vScroll.component.height = self.SCREEN_HEIGHT - self.TAB_HEIGHT - 58 - 2
        vScroll.component.horizontalAnchor = 'RIGHT'
        vScroll.component.verticalAnchor = 'TOP'
        vScroll.component.horizontalPositionMode = vScroll.component.verticalPositionMode = 'PIXEL'
        vScroll.component.position = (530, 60, 0.0)
        vScroll.visible = True
        self.component.addChild(vScroll.component, 'vScroll')
        vScroll.initVSC('scripts/client/soGUI/schemas/soScrollBar_default.xml')
        vScroll.setVisualState('normal')
        vScroll.onBound()
        vScroll.makeLayout()
        vScroll.setupScrollingInfo(0)

    def setupTreeInfo(self):
        freeSP = GUI.Text('')
        freeSP.verticalPositionMode = freeSP.horizontalPositionMode = 'CLIP'
        freeSP.horizontalAnchor = 'RIGHT'
        freeSP.verticalAnchor = 'TOP'
        freeSP.font = 'ruRU_calibri_small.font'
        freeSP.text = lc('soSkillScreen.soGUI.STRING_772_16')
        freeSP.colour = (255, 255, 255, 255)
        freeSP.materialFX = 'BLEND'
        freeSP.position = (1.0 - soGUI.getPixelWidth(self.component) * 30, 1.0 - soGUI.getPixelHeight(self.component) * (self.TAB_HEIGHT + 4), 0.0)
        self.component.addChild(freeSP, 'freeSP')
        expa = GUI.Text('')
        expa.verticalPositionMode = expa.horizontalPositionMode = 'PIXEL'
        expa.horizontalAnchor = 'LEFT'
        expa.verticalAnchor = 'TOP'
        expa.font = 'ruRU_calibri_small.font'
        expa.text = lc('soSkillScreen.soGUI.STRING_790_14')
        expa.colour = (255, 255, 255, 255)
        expa.materialFX = 'BLEND'
        expa.position = (10, self.TAB_HEIGHT + 4, 0.0)
        self.component.addChild(expa, 'expa')
        pps = GUI.Text('')
        pps.verticalPositionMode = pps.horizontalPositionMode = 'PIXEL'
        pps.horizontalAnchor = 'LEFT'
        pps.verticalAnchor = 'TOP'
        pps.font = 'ruRU_calibri_small.font'
        pps.text = lc('soSkillScreen.soGUI.STRING_805_13')
        pps.colour = (255, 255, 255, 255)
        pps.materialFX = 'BLEND'
        pps.position = (135, self.TAB_HEIGHT + 4, 0.0)
        self.component.addChild(pps, 'pps')

    def setupTabs(self):
        i = 0
        for tab in [soSkillScreen2.TAB_COMBAT, soSkillScreen2.TAB_SURVIVAL, soSkillScreen2.TAB_SUPPORT]:
            btn = soButton(GUI.Window())
            cmp = btn.component
            cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = self.TAB_WIDTH
            cmp.height = self.TAB_HEIGHT
            cmp.position = (-1.0 + soGUI.getPixelWidth(self.component) * (self.TAB_LEFT_OFFSET + self.TAB_WIDTH * i), 1.0, 1.0)
            btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
            btn.onClick = partial(self.tabSelect, tab)
            btn.initVSC('soGUI/visual_styles/skillTab.xml')
            btn.onBound()
            btn.setVisualState('normal')
            self.component.addChild(btn.component, 'tab' + str(tab))
            cmp.label.position.x = -1.0 + soGUI.getPixelWidth(cmp) * 5
            cmp.label.horizontalAnchor = 'LEFT'
            cmp.label.text = self.TAB_LABELS[tab]
            self.tabs[tab] = btn
            i += 1

    def setupScroll(self):
        pass

    def tabSelect(self, tabID):
        if self.currentTab == tabID:
            self.tabs[self.currentTab].buttonActive = True
            self.tabs[self.currentTab].setVisualState('active')
            return
        self.currentTab = tabID
        for tab in self.tabs:
            if tab == tabID:
                self.tabs[tab].buttonActive = True
                self.tabs[tab].setVisualState('active')
                self.tabs[tab].component.position.z = 0.0
                continue
            self.tabs[tab].buttonActive = False
            if self.tabs[tab].buttonDisabled:
                self.tabs[tab].setVisualState('disabled')
            else:
                self.tabs[tab].setVisualState('normal')
            self.tabs[tab].component.position.z = 1.0

        if tabID == self.TAB_COMBAT:
            self.combatWnd.visible = True
            self.survWnd.visible = False
            self.supportWnd.visible = False
            self.updateScroll()
            self.component.vScroll.script.reset()
            self.combatWnd.scroll.y = 0.0
        elif tabID == self.TAB_SURVIVAL:
            self.combatWnd.visible = False
            self.survWnd.visible = True
            self.supportWnd.visible = False
            self.updateScroll()
            self.component.vScroll.script.reset()
            self.survWnd.scroll.y = 0.0
        elif tabID == self.TAB_SUPPORT:
            self.combatWnd.visible = False
            self.survWnd.visible = False
            self.supportWnd.visible = True
            self.updateScroll()
            self.component.vScroll.script.reset()
            self.survWnd.scroll.y = 0.0
        self.updateTreeInfo()
        GUI.reSort()

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'skillGUI')
        self.component.visible = True
        self.tabSelect(soSkillScreen2.TAB_COMBAT)
        self.combatWnd.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def setupCombatWnd(self):
        self.combatWnd = GUI.Window()
        cmp = self.combatWnd
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = self.SCREEN_WIDTH - self.TYPICAL_OFFSET * 2
        cmp.height = self.SCREEN_HEIGHT - self.TAB_HEIGHT - 58 - 2
        cmp.textureName = ''
        cmp.position = (-1.0 + soGUI.getPixelWidth(self.component) * self.TYPICAL_OFFSET, 1.0 - soGUI.getPixelHeight(self.component) * (self.TAB_HEIGHT + 29 + 1), 0.0)
        cmp.visible = False
        self.component.addChild(cmp, 'combatWnd')

    def setupSurvWnd(self):
        self.survWnd = GUI.Window()
        cmp = self.survWnd
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = self.SCREEN_WIDTH - self.TYPICAL_OFFSET * 2
        cmp.height = self.SCREEN_HEIGHT - self.TAB_HEIGHT - 58 - 2
        cmp.textureName = ''
        cmp.position = (-1.0 + soGUI.getPixelWidth(self.component) * self.TYPICAL_OFFSET, 1.0 - soGUI.getPixelHeight(self.component) * (self.TAB_HEIGHT + 29 + 1), 0.0)
        cmp.visible = False
        self.component.addChild(cmp, 'survWnd')

    def setupSupportWnd(self):
        self.supportWnd = GUI.Window()
        cmp = self.supportWnd
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = self.SCREEN_WIDTH - self.TYPICAL_OFFSET * 2
        cmp.height = self.SCREEN_HEIGHT - self.TAB_HEIGHT - 58 - 2
        cmp.textureName = ''
        cmp.position = (-1.0 + soGUI.getPixelWidth(self.component) * self.TYPICAL_OFFSET, 1.0 - soGUI.getPixelHeight(self.component) * (self.TAB_HEIGHT + 29 + 1), 0.0)
        cmp.visible = False
        self.component.addChild(cmp, 'supportWnd')

    def update(self):
        self.skillsUpdate(None)
        return

    def skillsUpdate(self, skillsData):
        firstTime = False
        if not len(self.combatSkills) and not len(self.survivalSkills) and not len(self.craftSkills):
            firstTime = True
        self.combatSkills = BWPersonality.GUICore.skillsDataSection['Combat']
        self.survivalSkills = BWPersonality.GUICore.skillsDataSection['Survival']
        self.supportSkills = BWPersonality.GUICore.skillsDataSection['Other']

        def setupCombat():
            i = 0
            for skill in self.combatSkills[0]:
                skillTab = GUI.Window()
                skillTab.horizontalPositionMode = skillTab.verticalPositionMode = 'CLIP'
                skillTab.widthMode = skillTab.heightMode = 'PIXEL'
                skillTab.horizontalAnchor = 'LEFT'
                skillTab.verticalAnchor = 'TOP'
                skillTab.width = self.combatWnd.width - self.SCROLL_WIDTH
                skillTab.height = self.SKILL_BOX_HEIGHT
                skillTab.position = (-1.0, 1.0 - soGUI.getPixelHeight(self.combatWnd) * (self.SKILL_BOX_HEIGHT + self.SKILL_BOX_INTERVAL) * i, 0.0)
                skillTab.mapping = ((0.0, 0.6666666),
                 (0.0, 1.0),
                 (1.0, 1.0),
                 (1.0, 0.6666666))
                skillTab.textureName = 'soGUI/maps/Controls/skills/skillBack.tga'
                skillFriendlyName = CharacterUtils.GetSkillFriendlyName(skill)
                skillName = GUI.Text(skillFriendlyName)
                skillName.verticalPositionMode = skillName.horizontalPositionMode = 'CLIP'
                skillName.horizontalAnchor = 'LEFT'
                skillName.verticalAnchor = 'TOP'
                skillName.colour = (255, 255, 255, 255)
                skillName.materialFX = 'BLEND'
                skillName.font = 'ruRU_calibri_small.font'
                skillName.position = (-1.0 + soGUI.getPixelWidth(skillTab) * 8, 1.0 - soGUI.getPixelHeight(skillTab) * 10, 0.0)
                skillTab.addChild(skillName, 'label')
                plusBtn = soButton(GUI.Window())
                plusBtn.soundControlName = 'PlusMinusBtn'
                plusCmp = plusBtn.component
                plusCmp.horizontalPositionMode = plusCmp.verticalPositionMode = 'CLIP'
                plusCmp.widthMode = plusCmp.heightMode = 'PIXEL'
                plusCmp.horizontalAnchor = 'RIGHT'
                plusCmp.verticalAnchor = 'TOP'
                plusCmp.width = self.SMALL_BTN_SIZE
                plusCmp.height = self.SMALL_BTN_SIZE
                plusCmp.position = (1.0 - soGUI.getPixelWidth(skillTab) * 12, 1.0 - soGUI.getPixelHeight(skillTab) * 12, 0.0)
                plusBtn.initVSC('soGUI/visual_styles/plusBtn.xml')
                plusBtn.onBound()
                plusBtn.setVisualState('normal')
                plusBtn.onClick = partial(self.learnSkill, skill, 1)
                skillTab.addChild(plusCmp, 'plus')
                minusBtn = soButton(GUI.Window())
                minusBtn.soundControlName = 'PlusMinusBtn'
                minusCmp = minusBtn.component
                minusCmp.horizontalPositionMode = minusCmp.verticalPositionMode = 'CLIP'
                minusCmp.widthMode = minusCmp.heightMode = 'PIXEL'
                minusCmp.horizontalAnchor = 'RIGHT'
                minusCmp.verticalAnchor = 'TOP'
                minusCmp.width = self.SMALL_BTN_SIZE
                minusCmp.height = self.SMALL_BTN_SIZE
                minusCmp.position = (1.0 - soGUI.getPixelWidth(skillTab) * 62, 1.0 - soGUI.getPixelHeight(skillTab) * 12, 0.0)
                minusBtn.initVSC('soGUI/visual_styles/minusBtn.xml')
                minusBtn.onBound()
                minusBtn.buttonDisabled = True
                minusBtn.setVisualState('disabled')
                skillTab.addChild(minusCmp, 'minus')
                skillPoints = GUI.Text('')
                skillPoints.verticalPositionMode = skillPoints.horizontalPositionMode = 'CLIP'
                skillPoints.horizontalAnchor = 'CENTER'
                skillPoints.verticalAnchor = 'TOP'
                skillPoints.colour = (255, 255, 255, 255)
                skillPoints.materialFX = 'BLEND'
                skillPoints.font = 'ruRU_calibri_default.font'
                skillPoints.position = (1.0 - soGUI.getPixelWidth(skillTab) * 44, 1.0 - soGUI.getPixelHeight(skillTab) * 10, 0.0)
                skillPoints.text = str(self.combatSkills[0][skill]['Value'])
                skillTab.addChild(skillPoints, 'skillPoints')
                for j in xrange(self.PERKS_PER_SKILL):
                    featSlot = soFeatSlot(GUI.Window())
                    featCmp = featSlot.component
                    featCmp.horizontalPositionMode = featCmp.verticalPositionMode = 'CLIP'
                    featCmp.widthMode = featCmp.heightMode = 'PIXEL'
                    featCmp.horizontalAnchor = 'LEFT'
                    featCmp.verticalAnchor = 'TOP'
                    slotWidth = (skillTab.width - 8) / self.PERKS_PER_SKILL
                    featCmp.width = slotWidth
                    featCmp.height = self.FEATSLOT_HEIGHT
                    featCmp.position = (-1.0 + soGUI.getPixelWidth(skillTab) * (slotWidth * j + 4), 1.0 - soGUI.getPixelHeight(skillTab) * 37, 0.2)
                    featCmp.colour = (255, 255, 255, 255)
                    featCmp.materialFX = 'BLEND'
                    featSlot.initVSC('soGUI/visual_styles/featSlot.xml')
                    featSlot.onBound()
                    featSlot.setVisualState('unknown')
                    skillTab.addChild(featCmp, 'featSlot' + str(j))
                    btn = soLearnFeatBtn(GUI.Window())
                    cmp = btn.component
                    cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
                    cmp.widthMode = cmp.heightMode = 'PIXEL'
                    cmp.horizontalAnchor = 'CENTER'
                    cmp.verticalAnchor = 'CENTER'
                    cmp.width = slotWidth - 4
                    cmp.height = self.FEATSLOT_HEIGHT - 4
                    cmp.position = (0.0, 0.0, 0.0)
                    btn.onClick = partial(self.learnFeat, 'Combat', skill, j, 1)
                    btn.initVSC('soGUI/visual_styles/learnFeatBtn.xml')
                    btn.onBound()
                    btn.buttonDisabled = True
                    btn.setVisualState('disabled')
                    featCmp.addChild(btn.component, 'feat' + str(j))

                progressBar = GUI.Window()
                progressBar.horizontalPositionMode = progressBar.verticalPositionMode = 'CLIP'
                progressBar.widthMode = progressBar.heightMode = 'PIXEL'
                progressBar.horizontalAnchor = 'LEFT'
                progressBar.verticalAnchor = 'TOP'
                progressBar.width = skillTab.width - 8
                progressBar.height = self.FEATSLOT_HEIGHT
                progressBar.position = (-1.0 + soGUI.getPixelWidth(skillTab) * 4, 1.0 - soGUI.getPixelHeight(skillTab) * 37, 0.1)
                progressBar.colour = (255, 255, 255, 125)
                progressBar.materialFX = 'BLEND'
                progressClipShader = GUI.ClipShader()
                progressClipShader.speed = 0
                progressClipShader.mode = 'RIGHT'
                progressClipShader.value = 1.0 / (120.0 / float(self.combatSkills[0][skill]['Value']))
                progressBar.addShader(progressClipShader, 'clipper')
                progressBar.textureName = 'soGUI/maps/Colours/darkGreen.bmp'
                progressBar.tiled = True
                progressBar.tileHeight = progressBar.tileWidth = 1
                skillTab.addChild(progressBar, 'skillProgress')
                self.combatWnd.addChild(skillTab, str(skill))
                i += 1

        def setupSurv():
            i = 0
            for skill in self.survivalSkills[0]:
                skillTab = GUI.Window()
                skillTab.horizontalPositionMode = skillTab.verticalPositionMode = 'CLIP'
                skillTab.widthMode = skillTab.heightMode = 'PIXEL'
                skillTab.horizontalAnchor = 'LEFT'
                skillTab.verticalAnchor = 'TOP'
                skillTab.width = self.combatWnd.width - self.SCROLL_WIDTH
                skillTab.height = self.SKILL_BOX_HEIGHT
                skillTab.position = (-1.0, 1.0 - soGUI.getPixelHeight(self.combatWnd) * (self.SKILL_BOX_HEIGHT + self.SKILL_BOX_INTERVAL) * i, 0.0)
                skillTab.mapping = ((0.0, 0.6666666),
                 (0.0, 1.0),
                 (1.0, 1.0),
                 (1.0, 0.6666666))
                skillTab.textureName = 'soGUI/maps/Controls/skills/skillBack.tga'
                skillFriendlyName = CharacterUtils.GetSkillFriendlyName(skill)
                skillName = GUI.Text(skillFriendlyName)
                skillName.verticalPositionMode = skillName.horizontalPositionMode = 'CLIP'
                skillName.horizontalAnchor = 'LEFT'
                skillName.verticalAnchor = 'TOP'
                skillName.colour = (255, 255, 255, 255)
                skillName.materialFX = 'BLEND'
                skillName.font = 'ruRU_calibri_small.font'
                skillName.position = (-1.0 + soGUI.getPixelWidth(skillTab) * 8, 1.0 - soGUI.getPixelHeight(skillTab) * 10, 0.0)
                skillTab.addChild(skillName, 'label')
                plusBtn = soButton(GUI.Window())
                plusBtn.soundControlName = 'PlusMinusBtn'
                plusCmp = plusBtn.component
                plusCmp.horizontalPositionMode = plusCmp.verticalPositionMode = 'CLIP'
                plusCmp.widthMode = plusCmp.heightMode = 'PIXEL'
                plusCmp.horizontalAnchor = 'RIGHT'
                plusCmp.verticalAnchor = 'TOP'
                plusCmp.width = self.SMALL_BTN_SIZE
                plusCmp.height = self.SMALL_BTN_SIZE
                plusCmp.position = (1.0 - soGUI.getPixelWidth(skillTab) * 12, 1.0 - soGUI.getPixelHeight(skillTab) * 12, 0.0)
                plusBtn.initVSC('soGUI/visual_styles/plusBtn.xml')
                plusBtn.onBound()
                plusBtn.setVisualState('normal')
                plusBtn.onClick = partial(self.learnSkill, skill, 1)
                skillTab.addChild(plusCmp, 'plus')
                minusBtn = soButton(GUI.Window())
                minusBtn.soundControlName = 'PlusMinusBtn'
                minusCmp = minusBtn.component
                minusCmp.horizontalPositionMode = minusCmp.verticalPositionMode = 'CLIP'
                minusCmp.widthMode = minusCmp.heightMode = 'PIXEL'
                minusCmp.horizontalAnchor = 'RIGHT'
                minusCmp.verticalAnchor = 'TOP'
                minusCmp.width = self.SMALL_BTN_SIZE
                minusCmp.height = self.SMALL_BTN_SIZE
                minusCmp.position = (1.0 - soGUI.getPixelWidth(skillTab) * 62, 1.0 - soGUI.getPixelHeight(skillTab) * 12, 0.0)
                minusBtn.initVSC('soGUI/visual_styles/minusBtn.xml')
                minusBtn.onBound()
                minusBtn.buttonDisabled = True
                minusBtn.setVisualState('disabled')
                skillTab.addChild(minusCmp, 'minus')
                skillPoints = GUI.Text('')
                skillPoints.verticalPositionMode = skillPoints.horizontalPositionMode = 'CLIP'
                skillPoints.horizontalAnchor = 'CENTER'
                skillPoints.verticalAnchor = 'TOP'
                skillPoints.colour = (255, 255, 255, 255)
                skillPoints.materialFX = 'BLEND'
                skillPoints.font = 'ruRU_calibri_default.font'
                skillPoints.position = (1.0 - soGUI.getPixelWidth(skillTab) * 44, 1.0 - soGUI.getPixelHeight(skillTab) * 10, 0.0)
                skillPoints.text = str(self.survivalSkills[0][skill]['Value'])
                skillTab.addChild(skillPoints, 'skillPoints')
                for j in xrange(self.PERKS_PER_SKILL):
                    featSlot = soFeatSlot(GUI.Window())
                    featCmp = featSlot.component
                    featCmp.horizontalPositionMode = featCmp.verticalPositionMode = 'CLIP'
                    featCmp.widthMode = featCmp.heightMode = 'PIXEL'
                    featCmp.horizontalAnchor = 'LEFT'
                    featCmp.verticalAnchor = 'TOP'
                    slotWidth = (skillTab.width - 8) / self.PERKS_PER_SKILL
                    featCmp.width = slotWidth
                    featCmp.height = self.FEATSLOT_HEIGHT
                    featCmp.position = (-1.0 + soGUI.getPixelWidth(skillTab) * (slotWidth * j + 4), 1.0 - soGUI.getPixelHeight(skillTab) * 37, 0.2)
                    featCmp.colour = (255, 255, 255, 255)
                    featCmp.materialFX = 'BLEND'
                    featSlot.initVSC('soGUI/visual_styles/featSlot.xml')
                    featSlot.onBound()
                    featSlot.setVisualState('unknown')
                    btn = soLearnFeatBtn(GUI.Window())
                    cmp = btn.component
                    cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
                    cmp.widthMode = cmp.heightMode = 'PIXEL'
                    cmp.horizontalAnchor = 'CENTER'
                    cmp.verticalAnchor = 'CENTER'
                    cmp.width = slotWidth - 4
                    cmp.height = self.FEATSLOT_HEIGHT - 4
                    cmp.position = (0.0, 0.0, 0.0)
                    btn.onClick = partial(self.learnFeat, 'Survival', skill, j, 1)
                    btn.initVSC('soGUI/visual_styles/learnFeatBtn.xml')
                    btn.onBound()
                    btn.buttonDisabled = True
                    btn.setVisualState('disabled')
                    featCmp.addChild(btn.component, 'feat' + str(j))
                    skillTab.addChild(featCmp, 'featSlot' + str(j))

                progressBar = GUI.Window()
                progressBar.horizontalPositionMode = progressBar.verticalPositionMode = 'CLIP'
                progressBar.widthMode = progressBar.heightMode = 'PIXEL'
                progressBar.horizontalAnchor = 'LEFT'
                progressBar.verticalAnchor = 'TOP'
                progressBar.width = skillTab.width - 8
                progressBar.height = self.FEATSLOT_HEIGHT
                progressBar.position = (-1.0 + soGUI.getPixelWidth(skillTab) * 4, 1.0 - soGUI.getPixelHeight(skillTab) * 37, 0.1)
                progressBar.colour = (255, 255, 255, 125)
                progressBar.materialFX = 'BLEND'
                progressClipShader = GUI.ClipShader()
                progressClipShader.speed = 0
                progressClipShader.mode = 'RIGHT'
                progressClipShader.value = 1.0 / (120.0 / float(self.survivalSkills[0][skill]['Value']))
                progressBar.addShader(progressClipShader, 'clipper')
                progressBar.textureName = 'soGUI/maps/Colours/darkGreen.bmp'
                progressBar.tiled = True
                progressBar.tileHeight = progressBar.tileWidth = 1
                skillTab.addChild(progressBar, 'skillProgress')
                self.survWnd.addChild(skillTab, str(skill))
                i += 1

        def setupSupport():
            i = 0
            for skill in self.supportSkills[0]:
                skillTab = GUI.Window()
                skillTab.horizontalPositionMode = skillTab.verticalPositionMode = 'CLIP'
                skillTab.widthMode = skillTab.heightMode = 'PIXEL'
                skillTab.horizontalAnchor = 'LEFT'
                skillTab.verticalAnchor = 'TOP'
                skillTab.width = self.combatWnd.width - self.SCROLL_WIDTH
                skillTab.height = self.SKILL_BOX_HEIGHT
                skillTab.position = (-1.0, 1.0 - soGUI.getPixelHeight(self.combatWnd) * (self.SKILL_BOX_HEIGHT + self.SKILL_BOX_INTERVAL) * i, 0.0)
                skillTab.mapping = ((0.0, 0.6666666),
                 (0.0, 1.0),
                 (1.0, 1.0),
                 (1.0, 0.6666666))
                skillTab.textureName = 'soGUI/maps/Controls/skills/skillBack.tga'
                skillFriendlyName = CharacterUtils.GetSkillFriendlyName(skill)
                skillName = GUI.Text(skillFriendlyName)
                skillName.verticalPositionMode = skillName.horizontalPositionMode = 'CLIP'
                skillName.horizontalAnchor = 'LEFT'
                skillName.verticalAnchor = 'TOP'
                skillName.colour = (255, 255, 255, 255)
                skillName.materialFX = 'BLEND'
                skillName.font = 'ruRU_calibri_small.font'
                skillName.position = (-1.0 + soGUI.getPixelWidth(skillTab) * 8, 1.0 - soGUI.getPixelHeight(skillTab) * 10, 0.0)
                skillTab.addChild(skillName, 'label')
                plusBtn = soButton(GUI.Window())
                plusBtn.soundControlName = 'PlusMinusBtn'
                plusCmp = plusBtn.component
                plusCmp.horizontalPositionMode = plusCmp.verticalPositionMode = 'CLIP'
                plusCmp.widthMode = plusCmp.heightMode = 'PIXEL'
                plusCmp.horizontalAnchor = 'RIGHT'
                plusCmp.verticalAnchor = 'TOP'
                plusCmp.width = self.SMALL_BTN_SIZE
                plusCmp.height = self.SMALL_BTN_SIZE
                plusCmp.position = (1.0 - soGUI.getPixelWidth(skillTab) * 12, 1.0 - soGUI.getPixelHeight(skillTab) * 12, 0.0)
                plusBtn.initVSC('soGUI/visual_styles/plusBtn.xml')
                plusBtn.onBound()
                plusBtn.setVisualState('normal')
                plusBtn.onClick = partial(self.learnSkill, skill, 1)
                skillTab.addChild(plusCmp, 'plus')
                minusBtn = soButton(GUI.Window())
                minusBtn.soundControlName = 'PlusMinusBtn'
                minusCmp = minusBtn.component
                minusCmp.horizontalPositionMode = minusCmp.verticalPositionMode = 'CLIP'
                minusCmp.widthMode = minusCmp.heightMode = 'PIXEL'
                minusCmp.horizontalAnchor = 'RIGHT'
                minusCmp.verticalAnchor = 'TOP'
                minusCmp.width = self.SMALL_BTN_SIZE
                minusCmp.height = self.SMALL_BTN_SIZE
                minusCmp.position = (1.0 - soGUI.getPixelWidth(skillTab) * 62, 1.0 - soGUI.getPixelHeight(skillTab) * 12, 0.0)
                minusBtn.initVSC('soGUI/visual_styles/minusBtn.xml')
                minusBtn.onBound()
                minusBtn.buttonDisabled = True
                minusBtn.setVisualState('disabled')
                skillTab.addChild(minusCmp, 'minus')
                skillPoints = GUI.Text('')
                skillPoints.verticalPositionMode = skillPoints.horizontalPositionMode = 'CLIP'
                skillPoints.horizontalAnchor = 'CENTER'
                skillPoints.verticalAnchor = 'TOP'
                skillPoints.colour = (255, 255, 255, 255)
                skillPoints.materialFX = 'BLEND'
                skillPoints.font = 'ruRU_calibri_default.font'
                skillPoints.position = (1.0 - soGUI.getPixelWidth(skillTab) * 44, 1.0 - soGUI.getPixelHeight(skillTab) * 10, 0.0)
                skillPoints.text = str(self.supportSkills[0][skill]['Value'])
                skillTab.addChild(skillPoints, 'skillPoints')
                for j in xrange(self.PERKS_PER_SKILL):
                    featSlot = soFeatSlot(GUI.Window())
                    featCmp = featSlot.component
                    featCmp.horizontalPositionMode = featCmp.verticalPositionMode = 'CLIP'
                    featCmp.widthMode = featCmp.heightMode = 'PIXEL'
                    featCmp.horizontalAnchor = 'LEFT'
                    featCmp.verticalAnchor = 'TOP'
                    slotWidth = (skillTab.width - 8) / self.PERKS_PER_SKILL
                    featCmp.width = slotWidth
                    featCmp.height = self.FEATSLOT_HEIGHT
                    featCmp.position = (-1.0 + soGUI.getPixelWidth(skillTab) * (slotWidth * j + 4), 1.0 - soGUI.getPixelHeight(skillTab) * 37, 0.2)
                    featCmp.colour = (255, 255, 255, 255)
                    featCmp.materialFX = 'BLEND'
                    featSlot.initVSC('soGUI/visual_styles/featSlot.xml')
                    featSlot.onBound()
                    featSlot.setVisualState('unknown')
                    btn = soLearnFeatBtn(GUI.Window())
                    cmp = btn.component
                    cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
                    cmp.widthMode = cmp.heightMode = 'PIXEL'
                    cmp.horizontalAnchor = 'CENTER'
                    cmp.verticalAnchor = 'CENTER'
                    cmp.width = slotWidth - 4
                    cmp.height = self.FEATSLOT_HEIGHT - 4
                    cmp.position = (0.0, 0.0, 0.0)
                    btn.onClick = partial(self.learnFeat, 'Other', skill, j, 1)
                    btn.initVSC('soGUI/visual_styles/learnFeatBtn.xml')
                    btn.onBound()
                    btn.buttonDisabled = True
                    btn.setVisualState('disabled')
                    featCmp.addChild(btn.component, 'feat' + str(j))
                    skillTab.addChild(featCmp, 'featSlot' + str(j))

                progressBar = GUI.Window()
                progressBar.horizontalPositionMode = progressBar.verticalPositionMode = 'CLIP'
                progressBar.widthMode = progressBar.heightMode = 'PIXEL'
                progressBar.horizontalAnchor = 'LEFT'
                progressBar.verticalAnchor = 'TOP'
                progressBar.width = skillTab.width - 8
                progressBar.height = self.FEATSLOT_HEIGHT
                progressBar.position = (-1.0 + soGUI.getPixelWidth(skillTab) * 4, 1.0 - soGUI.getPixelHeight(skillTab) * 37, 0.1)
                progressBar.colour = (255, 255, 255, 125)
                progressBar.materialFX = 'BLEND'
                progressClipShader = GUI.ClipShader()
                progressClipShader.speed = 0
                progressClipShader.mode = 'RIGHT'
                progressClipShader.value = 1.0 / (120.0 / float(self.supportSkills[0][skill]['Value']))
                progressBar.addShader(progressClipShader, 'clipper')
                progressBar.textureName = 'soGUI/maps/Colours/darkGreen.bmp'
                progressBar.tiled = True
                progressBar.tileHeight = progressBar.tileWidth = 1
                skillTab.addChild(progressBar, 'skillProgress')
                self.supportWnd.addChild(skillTab, str(skill))
                i += 1

        def updateCombat():
            self.component.tab0.label.text = self.TAB_LABELS[soSkillScreen2.TAB_COMBAT] + '                      ' + str(BWPersonality.GUICore.skillsDataSection['Combat'][2])
            for skill in self.combatSkills[0]:
                cmp = self.combatWnd.__getattribute__(skill)
                cmp.skillPoints.text = str(self.combatSkills[0][skill]['Value'])
                cmp.skillProgress.clipper.value = 1.0 / (120.0 / float(self.combatSkills[0][skill]['Value']))
                for i in xrange(self.PERKS_PER_SKILL):
                    featSlot = cmp.__getattribute__('featSlot' + str(i))
                    featBtn = cmp.__getattribute__('featSlot' + str(i)).__getattribute__('feat' + str(i))
                    status = BigWorld.player().GetPerkStatus('Combat', skill, i)
                    featBtn.script.toolTipID = ('Combat', skill, i)
                    featBtn.script.interfaceID = BWPersonality.GUICore.GUI_ID_SKILLS
                    if status == CharacterConst.PERK_STATUS_LOCKED:
                        featSlot.position.z = 0.2
                        featBtn.script.buttonDisabled = True
                        featBtn.script.setVisualState('disabled')
                        featSlot.script.setVisualState('unknown')
                    elif status == CharacterConst.PERK_STATUS_KNOWN:
                        featSlot.position.z = 0.0
                        featBtn.script.buttonDisabled = True
                        featBtn.script.setVisualState('disabled')
                        featSlot.script.setVisualState('learnt')
                    elif status == CharacterConst.PERK_STATUS_KNOWN_CAN_TAKE:
                        featSlot.position.z = 0.2
                        featBtn.script.buttonDisabled = False
                        featBtn.script.setVisualState('normal')
                        featSlot.script.setVisualState('learning')
                    elif status == CharacterConst.PERK_STATUS_CAN_TAKE:
                        featSlot.position.z = 0.2
                        featBtn.script.buttonDisabled = False
                        featBtn.script.setVisualState('normal')
                        featSlot.script.setVisualState('learning')
                    icon = BigWorld.player().GetPerkIcon('Combat', skill, i)
                    if icon != '':
                        iconCmp = GUI.Simple(icon)
                        iconCmp.verticalPositionMode = iconCmp.horizontalPositionMode = 'CLIP'
                        iconCmp.widthMode = iconCmp.heightMode = 'PIXEL'
                        iconCmp.horizontalAnchor = iconCmp.verticalAnchor = 'CENTER'
                        iconCmp.width = 38
                        iconCmp.height = 38
                        iconCmp.colour = (255, 255, 255, 255)
                        iconCmp.materialFX = 'BLEND'
                        featSlot.addChild(iconCmp, 'featIcon')

            GUI.reSort()

        def updateSurv():
            self.component.tab1.label.text = self.TAB_LABELS[soSkillScreen2.TAB_SURVIVAL] + '       ' + str(BWPersonality.GUICore.skillsDataSection['Survival'][2])
            for skill in self.survivalSkills[0]:
                cmp = self.survWnd.__getattribute__(skill)
                cmp.skillPoints.text = str(self.survivalSkills[0][skill]['Value'])
                cmp.skillProgress.clipper.value = 1.0 / (120.0 / float(self.survivalSkills[0][skill]['Value']))
                for i in xrange(self.PERKS_PER_SKILL):
                    featSlot = cmp.__getattribute__('featSlot' + str(i))
                    featBtn = cmp.__getattribute__('featSlot' + str(i)).__getattribute__('feat' + str(i))
                    status = BigWorld.player().GetPerkStatus('Survival', skill, i)
                    featBtn.script.toolTipID = ('Survival', skill, i)
                    featBtn.script.interfaceID = BWPersonality.GUICore.GUI_ID_SKILLS
                    if status == CharacterConst.PERK_STATUS_LOCKED:
                        featSlot.position.z = 0.2
                        featBtn.script.buttonDisabled = True
                        featBtn.script.setVisualState('disabled')
                        featSlot.script.setVisualState('unknown')
                    elif status == CharacterConst.PERK_STATUS_KNOWN:
                        featSlot.position.z = 0.0
                        featBtn.script.buttonDisabled = True
                        featBtn.script.setVisualState('disabled')
                        featSlot.script.setVisualState('learnt')
                    elif status == CharacterConst.PERK_STATUS_KNOWN_CAN_TAKE:
                        featSlot.position.z = 0.2
                        featBtn.script.buttonDisabled = False
                        featBtn.script.setVisualState('normal')
                        featSlot.script.setVisualState('learning')
                    elif status == CharacterConst.PERK_STATUS_CAN_TAKE:
                        featSlot.position.z = 0.2
                        featBtn.script.buttonDisabled = False
                        featBtn.script.setVisualState('normal')
                        featSlot.script.setVisualState('learning')
                    icon = BigWorld.player().GetPerkIcon('Survival', skill, i)
                    if icon != '':
                        iconCmp = GUI.Simple(icon)
                        iconCmp.verticalPositionMode = iconCmp.horizontalPositionMode = 'CLIP'
                        iconCmp.widthMode = iconCmp.heightMode = 'PIXEL'
                        iconCmp.horizontalAnchor = iconCmp.verticalAnchor = 'CENTER'
                        iconCmp.width = 38
                        iconCmp.height = 38
                        iconCmp.colour = (255, 255, 255, 255)
                        iconCmp.materialFX = 'BLEND'
                        featSlot.addChild(iconCmp, 'featIcon')

            GUI.reSort()

        def updateSupport():
            self.component.tab2.label.text = self.TAB_LABELS[soSkillScreen2.TAB_SUPPORT] + '       ' + str(BWPersonality.GUICore.skillsDataSection['Other'][2])
            for skill in self.supportSkills[0]:
                cmp = self.supportWnd.__getattribute__(skill)
                cmp.skillPoints.text = str(self.supportSkills[0][skill]['Value'])
                cmp.skillProgress.clipper.value = 1.0 / (120.0 / float(self.supportSkills[0][skill]['Value']))
                for i in xrange(self.PERKS_PER_SKILL):
                    featSlot = cmp.__getattribute__('featSlot' + str(i))
                    featBtn = cmp.__getattribute__('featSlot' + str(i)).__getattribute__('feat' + str(i))
                    status = BigWorld.player().GetPerkStatus('Other', skill, i)
                    featBtn.script.toolTipID = ('Other', skill, i)
                    featBtn.script.interfaceID = BWPersonality.GUICore.GUI_ID_SKILLS
                    if status == CharacterConst.PERK_STATUS_LOCKED:
                        featSlot.position.z = 0.2
                        featBtn.script.buttonDisabled = True
                        featBtn.script.setVisualState('disabled')
                        featSlot.script.setVisualState('unknown')
                    elif status == CharacterConst.PERK_STATUS_KNOWN:
                        featSlot.position.z = 0.0
                        featBtn.script.buttonDisabled = True
                        featBtn.script.setVisualState('disabled')
                        featSlot.script.setVisualState('learnt')
                    elif status == CharacterConst.PERK_STATUS_KNOWN_CAN_TAKE:
                        featSlot.position.z = 0.2
                        featBtn.script.buttonDisabled = False
                        featBtn.script.setVisualState('normal')
                        featSlot.script.setVisualState('learning')
                    elif status == CharacterConst.PERK_STATUS_CAN_TAKE:
                        featSlot.position.z = 0.2
                        featBtn.script.buttonDisabled = False
                        featBtn.script.setVisualState('normal')
                        featSlot.script.setVisualState('learning')
                    icon = BigWorld.player().GetPerkIcon('Other', skill, i)
                    if icon != '':
                        iconCmp = GUI.Simple(icon)
                        iconCmp.verticalPositionMode = iconCmp.horizontalPositionMode = 'CLIP'
                        iconCmp.widthMode = iconCmp.heightMode = 'PIXEL'
                        iconCmp.horizontalAnchor = iconCmp.verticalAnchor = 'CENTER'
                        iconCmp.width = 38
                        iconCmp.height = 38
                        iconCmp.colour = (255, 255, 255, 255)
                        iconCmp.materialFX = 'BLEND'
                        featSlot.addChild(iconCmp, 'featIcon')

            GUI.reSort()

        if firstTime:
            setupCombat()
            setupSurv()
            setupSupport()
        updateCombat()
        updateSurv()
        updateSupport()
        self.updateTreeInfo()
        self.updateScroll()

    def updateTreeInfo(self):
        tabName = 'Combat'
        if self.currentTab == self.TAB_COMBAT:
            tabName = 'Combat'
        elif self.currentTab == self.TAB_SURVIVAL:
            tabName = 'Survival'
        elif self.currentTab == self.TAB_SUPPORT:
            tabName = 'Other'
        self.component.expa.text = lc('soSkillScreen.soGUI.STRING_1767_29') + str(BWPersonality.GUICore.skillsDataSection[tabName][1])
        self.component.freeSP.text = lc('soSkillScreen.soGUI.STRING_1768_31') + str(BWPersonality.GUICore.skillsDataSection[tabName][3])
        self.component.pps.text = lc('soSkillScreen.soGUI.STRING_1769_28') + str(BWPersonality.GUICore.skillsDataSection[tabName][4])

    def updateScroll(self):
        screenH = BigWorld.screenHeight()
        itemH = self.SKILL_BOX_HEIGHT + self.SKILL_BOX_INTERVAL
        if self.currentTab == self.TAB_COMBAT:
            tabCount = len(self.combatSkills[0])
        elif self.currentTab == self.TAB_SURVIVAL:
            tabCount = len(self.survivalSkills[0])
        elif self.currentTab == self.TAB_SUPPORT:
            tabCount = len(self.supportSkills[0])
        if self.currentTab == self.TAB_COMBAT:
            holderHeight = self.combatWnd.height
        elif self.currentTab == self.TAB_SURVIVAL:
            holderHeight = self.survWnd.height
        elif self.currentTab == self.TAB_SUPPORT:
            holderHeight = self.supportWnd.height
        if self.currentTab == self.TAB_COMBAT:
            holderComponent = self.combatWnd
        elif self.currentTab == self.TAB_SURVIVAL:
            holderComponent = self.survWnd
        if self.currentTab == self.TAB_SUPPORT:
            holderComponent = self.supportWnd

        def setMaxScroll():
            elementsHeight = itemH * tabCount - self.SKILL_BOX_INTERVAL
            heightDiff = itemH / screenH * tabCount - holderHeight / screenH
            if heightDiff > 0.0:
                holderComponent.maxScroll = (0.0, heightDiff * 2)

        def setMinScroll():
            holderComponent.minScroll = (0.0, 0.0)

        setMaxScroll()
        setMinScroll()
        self.scrollStep = 2.0 / (screenH / itemH)
        scrollStepCount = (itemH * tabCount - holderHeight) / float(itemH)
        if scrollStepCount > 0:
            self.component.vScroll.script.setupScrollingInfo(math.ceil(scrollStepCount))
        else:
            self.component.vScroll.script.setupScrollingInfo(0)

    def learnSkill(self, skillName, value):
        BWPersonality.GUICore.skillEvent(skillName, self.EVENT_LEARNSKILL)

    def learnFeat(self, treeName, skillName, featNumber, value):
        BWPersonality.GUICore.skillEvent((treeName,
         skillName,
         featNumber,
         value), self.EVENT_LEARNFEAT)

    def scrollUP(self):
        if self.currentTab == self.TAB_COMBAT:
            if self.component.combatWnd.scroll.y < self.component.combatWnd.minScroll.y:
                self.component.combatWnd.scroll.y = self.component.combatWnd.minScroll.y
            if self.component.combatWnd.scroll.y > self.component.combatWnd.minScroll.y:
                self.component.combatWnd.scroll.y -= self.scrollStep
                self.component.vScroll.script.doStep(False)
        elif self.currentTab == self.TAB_SURVIVAL:
            if self.component.survWnd.scroll.y < self.component.survWnd.minScroll.y:
                self.component.survWnd.scroll.y = self.component.survWnd.minScroll.y
            if self.component.survWnd.scroll.y > self.component.survWnd.minScroll.y:
                self.component.survWnd.scroll.y -= self.scrollStep
                self.component.vScroll.script.doStep(False)
        elif self.currentTab == self.TAB_SUPPORT:
            if self.component.supportWnd.scroll.y < self.component.supportWnd.minScroll.y:
                self.component.supportWnd.scroll.y = self.component.supportWnd.minScroll.y
            if self.component.supportWnd.scroll.y > self.component.supportWnd.minScroll.y:
                self.component.supportWnd.scroll.y -= self.scrollStep
                self.component.vScroll.script.doStep(False)

    def scrollDN(self):
        if self.currentTab == self.TAB_COMBAT:
            if self.component.combatWnd.scroll.y > self.component.combatWnd.maxScroll.y:
                self.component.combatWnd.scroll.y = self.component.combatWnd.maxScroll.y
            if self.component.combatWnd.scroll.y < self.component.combatWnd.maxScroll.y:
                self.component.combatWnd.scroll.y += self.scrollStep
                self.component.vScroll.script.doStep(True)
        elif self.currentTab == self.TAB_SURVIVAL:
            if self.component.survWnd.scroll.y > self.component.survWnd.maxScroll.y:
                self.component.survWnd.scroll.y = self.component.survWnd.maxScroll.y
            if self.component.survWnd.scroll.y < self.component.survWnd.maxScroll.y:
                self.component.survWnd.scroll.y += self.scrollStep
                self.component.vScroll.script.doStep(True)
        elif self.currentTab == self.TAB_SUPPORT:
            if self.component.supportWnd.scroll.y > self.component.supportWnd.maxScroll.y:
                self.component.supportWnd.scroll.y = self.component.supportWnd.maxScroll.y
            if self.component.supportWnd.scroll.y < self.component.supportWnd.maxScroll.y:
                self.component.supportWnd.scroll.y += self.scrollStep
                self.component.vScroll.script.doStep(True)

    def handleMouseEvent(self, comp, event):
        dz = event.dz
        if dz > 0:
            self.scrollUP()
            return True
        if dz < 0:
            self.scrollDN()
            return True
        return False

    @PyGUIEvent('vScroll', 'scrollUP')
    def scrolledUP(self):
        self.scrollUP()

    @PyGUIEvent('vScroll', 'scrollDN')
    def scrolledDN(self):
        self.scrollDN()


class soSpecListElem(soList2ElementBase):
    factoryString = 'soGUI.soSpecListElem'
    EVENT_ACTIVATE = 0
    EVENT_DEACTIVATE = 1
    EVENT_INVEST = 2

    def __init__(self, component, id, data):
        soList2ElementBase.__init__(self, component, id, data)
        component.script = self
        self.pressed = False

    def setupRoot(self):
        soList2ElementBase.setupRoot(self)
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 323
        cmp.height = 26
        cmp.position.x = 0
        cmp.position.z = 0.1
        cmp.horizontalAnchor = 'LEFT'

    def setupContent(self):
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (28, 28, 28, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        cmp.script = self
        cmp.mouseButtonFocus = True
        self.component.addChild(cmp, 'backFrame')
        btn = soButtonWTT(GUI.Window(''), 'leveling_gui_invest_experience')
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (283, 4, 0.4)
        btn.initVSC('soGUI/visual_styles/arrow_up.xml')
        btn.onBound()
        btn._updateVisualState()
        btn.onClick = self._btnHandler
        self.component.addChild(cmp, 'btn')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (140, 13, 0.4)
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = self.elemData['spec_name']
        self.component.addChild(cmp, 'specName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 13, 0.4)
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = u'x{0}\\{1}'.format(self.elemData['modifier'][0], self.elemData['modifier'][1])
        self.component.addChild(cmp, 'modifier')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (276, 13, 0.4)
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = str(self.elemData['spec_points']).encode('utf-8')
        self.component.addChild(cmp, 'specPoints')

    def _btnHandler(self):
        self.activate(True)
        self.elementEvent(self.EVENT_INVEST, self)

    def enable(self):
        self.component.btn.script.buttonDisabled = False
        self.component.btn.script._updateVisualState()
        return False

    def disable(self):
        self.component.btn.script.buttonDisabled = True
        self.component.btn.script._updateVisualState()
        return False

    def activate(self, byUser = True):
        self.component.backFrame.colour = (45, 45, 30, 255)
        if byUser:
            self.elementEvent(self.EVENT_ACTIVATE, self)
        return False

    def deactivate(self, byUser = True):
        self.component.backFrame.colour = (28, 28, 28, 255)
        if byUser:
            self.elementEvent(self.EVENT_DEACTIVATE, self)
        return False

    def applyElemData(self):
        self.component.specName.text = self.elemData['spec_name']
        self.component.specPoints.text = self.elemData['spec_points']
        self.component.modifier.text = u'x{0}\\{1}'.format(self.elemData['modifier'][0], self.elemData['modifier'][1])

    def onClick(self):
        self.activate(True)

    def handleMouseButtonEvent(self, cmp, event):
        if event.key == KEY_LEFTMOUSE:
            if event.isKeyDown() and not self.pressed:
                self.pressed = True
            elif not event.isKeyDown() and self.pressed:
                self.pressed = False
                self.onClick()
        return True


class soBSkillSlot(soItemSlot):
    factoryString = 'soGUI.soBSkillSlot'
    SLOTWIDTH = 64
    SLOTHEIGHT = 64
    normalFrame = BigWorld.PyTextureProvider('soGUI/maps/Controls/inventory/cellFrame2.tga')
    selFrame = BigWorld.PyTextureProvider('soGUI/maps/Controls/skills/20/selFrame.tga')
    canLearn = BigWorld.PyTextureProvider('soGUI/maps/Controls/skills/20/canLearn.tga')
    cantLearn = BigWorld.PyTextureProvider('soGUI/maps/Controls/skills/20/cantLearn.tga')
    unaccessible = BigWorld.PyTextureProvider('soGUI/maps/Controls/skills/20/unaccessible.tga')

    def __init__(self, component, slotIndex, itemData = None):
        soItemSlot.__init__(self, component, slotIndex, itemData, centerDProxy=True)
        component.script = self

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.dragFocus = False
        cmp.dropFocus = False
        cmp.crossFocus = True
        cmp.moveFocus = False
        cmp.mouseButtonFocus = True

    def setupContent(self):
        cmp = GUI.Frame2('')
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.9)
        cmp.texture = soBSkillSlot.normalFrame
        self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Frame2('')
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.1)
        cmp.texture = soBSkillSlot.selFrame
        cmp.visible = False
        self.component.addChild(cmp, 'selFrame')
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
        self.component.addChild(cmp, 'skillIcon')
        cmp = GUI.Frame2('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.visible = False
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.3)
        self.component.addChild(cmp, 'skillState')

    def _applyItemData(self):
        skillGUI = self.component.parent.parent.script
        if self.haveItem():
            self.component.skillIcon.textureName = skillGUI.texturing_callback(self.itemData['id'])
            self.setState(skillGUI.skill_state_callback(self.itemData['id']))
        else:
            self.component.skillIcon.textureName = ''
            self.setState()

    def select(self, doSel = True):
        self.component.selFrame.visible = doSel

    def setState(self, state = LEVELING.STATE_LEARNED):
        self.component.skillState.visible = False
        if state == LEVELING.STATE_CANTLEARN:
            self.component.skillState.texture = soBSkillSlot.cantLearn
            self.component.skillState.visible = True
        elif state == LEVELING.STATE_CANLEARN:
            self.component.skillState.texture = soBSkillSlot.canLearn
            self.component.skillState.visible = True
        elif state == LEVELING.STATE_UNACCESSIBLE:
            self.component.skillState.texture = soBSkillSlot.unaccessible
            self.component.skillState.visible = True


class soAdSkillSlot(soItemSlot):
    factoryString = 'soGUI.soAdSkillSlot'
    SLOTWIDTH = 64
    SLOTHEIGHT = 64
    normalFrame = BigWorld.PyTextureProvider('soGUI/maps/Controls/inventory/cellFrame2.tga')
    selFrame = BigWorld.PyTextureProvider('soGUI/maps/Controls/skills/20/selFrame.tga')
    canLearn = BigWorld.PyTextureProvider('soGUI/maps/Controls/skills/20/canLearn.tga')
    cantLearn = BigWorld.PyTextureProvider('soGUI/maps/Controls/skills/20/cantLearn.tga')
    unaccessible = BigWorld.PyTextureProvider('soGUI/maps/Controls/skills/20/unaccessible.tga')

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
        cmp.dropFocus = False
        cmp.crossFocus = True
        cmp.moveFocus = True
        cmp.mouseButtonFocus = True

    def setupContent(self):
        cmp = GUI.Frame2('')
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.9)
        cmp.texture = soAdSkillSlot.normalFrame
        self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Frame2('')
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.1)
        cmp.texture = soAdSkillSlot.selFrame
        cmp.visible = False
        self.component.addChild(cmp, 'selFrame')
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
        self.component.addChild(cmp, 'skillIcon')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 0)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.7)
        self.component.addChild(cmp, 'skillState')

    def _applyItemData(self):
        skillGUI = self.component.parent.parent.script
        if self.haveItem():
            self.component.skillIcon.textureName = skillGUI.texturing_callback(self.itemData['id'])
            self.setState(skillGUI.skill_state_callback(self.itemData['id']))
        else:
            self.component.skillIcon.textureName = ''
            self.setState()
        self.dragProxy.texture = self.component.skillIcon.texture

    def onDragStart(self):
        skillGUI = self.component.parent.parent.script
        if self.haveItem():
            if skillGUI.skill_type_callback(self.itemData['id']) == LEVELING.TYPE_ABILITY:
                self.dragProxy.visible = True
                return True
        return False

    def onDragStop(self):
        self.dragProxy.visible = False
        return True

    def select(self, doSel = True):
        self.component.selFrame.visible = doSel

    def setState(self, state = LEVELING.STATE_LEARNED):
        self.component.skillState.visible = False
        if state == LEVELING.STATE_CANTLEARN:
            self.component.skillState.texture = soAdSkillSlot.cantLearn
            self.component.skillState.visible = True
        elif state == LEVELING.STATE_CANLEARN:
            self.component.skillState.texture = soAdSkillSlot.canLearn
            self.component.skillState.visible = True
        elif state == LEVELING.STATE_UNACCESSIBLE:
            self.component.skillState.texture = soAdSkillSlot.unaccessible
            self.component.skillState.visible = True


class soASkillSlot(soItemSlot):
    factoryString = 'soGUI.soASkillSlot'
    SLOTWIDTH = 64
    SLOTHEIGHT = 80
    normalFrame = BigWorld.PyTextureProvider('soGUI/maps/Controls/inventory/cellFrame2.tga')

    def __init__(self, component, slotIndex, itemData = None):
        soItemSlot.__init__(self, component, slotIndex, itemData, centerDProxy=True)
        component.script = self
        self.dragProxy = self.component.dragProxy
        self.proxyHolder = self.component
        self.proxyName = 'dragProxy'
        self.ticker = None
        self.ttl = 0
        self.totalTime = 0
        self._onDragStart = self.onDragStart
        self._onDragStop = self.onDragStop
        return

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
        cmp = GUI.Frame2('')
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = 64
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 16, 0.9)
        cmp.texture = soASkillSlot.normalFrame
        self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = 64
        cmp.colour = (255, 255, 255, 128)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 16, 0.5)
        cmp.visible = False
        self.component.addChild(cmp, 'dragProxy')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = 64
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 16, 0.4)
        self.component.addChild(cmp, 'skillIcon')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = 64
        cmp.colour = (70, 70, 70, 128)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 16, 0.4)
        self.component.addChild(cmp, 'skillProgress')
        shader = GUI.ClipShader()
        shader.value = 0.0
        shader.speed = 0
        cmp.addShader(shader, 'clipper')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (32, 8, 0.3)
        self.component.addChild(cmp, 'timeToLearn')

    def timeToString(self, secs):
        if secs < 0:
            return u''
        hours = floor(secs / 3600.0)
        minutes = floor((secs - hours * 3600.0) / 60.0)
        seconds = secs - (hours * 3600.0 + minutes * 60.0)
        outH = str(int(hours)) + lc('GUI.General.HOURS_SHORTENING')
        outM = str(int(minutes)) + lc('GUI.General.MINUTES_SHORTENING')
        outS = str(int(seconds)) + lc('GUI.General.SECONDS_SHORTENING')
        if hours:
            return outH
        if minutes:
            return outM
        if seconds:
            return outS
        return u''

    def _applyItemData(self):
        skillGUI = self.component.parent.parent.script
        if self.haveItem():
            self.component.skillIcon.textureName = skillGUI.texturing_callback(self.itemData['id'])
            self.ttl = self.itemData['time_to_learn']
            self.totalTime = self.itemData['total_time']
            self.updateTimer()
            self.runTimer()
            if self.ttl > 0:
                self.component.skillProgress.clipper.value = 1.0 / (self.totalTime / self.ttl)
            else:
                self.component.skillProgress.clipper.value = 0.0
            self.component.skillProgress.clipper.reset()
            self.component.skillProgress.clipper.speed = self.ttl
            self.component.skillProgress.clipper.value = 0.0
        else:
            self.component.skillIcon.textureName = ''
            self.ttl = 0
            self.totalTime = 0
            self.component.skillProgress.clipper.value = 0.0
            self.component.skillProgress.clipper.speed = 0
            self.component.skillProgress.clipper.reset()
            self.stopTimer()
            self.updateTimer()
        self.dragProxy.texture = self.component.skillIcon.texture
        self.dragProxy.texture = self.component.skillIcon.texture

    def runTimer(self):
        if self.ticker is not None:
            self.ticker.stop()
            self.ticker = None
        self.ticker = self.timeTicker()
        self.ticker.run()
        return

    def stopTimer(self):
        if self.ticker is not None:
            self.ticker.stop()
            self.ticker = None
        return

    def onDragStart(self):
        if self.haveItem():
            self.dragProxy.visible = True
            return True
        return False

    def onDragStop(self):
        self.dragProxy.visible = False
        return True

    def updateTimer(self):
        self.component.timeToLearn.text = self.timeToString(self.ttl)

    @BWMemberCoroutine
    def timeTicker(self):
        while self.ttl:
            yield BWWaitForPeriod(1.0)
            self.ttl -= 1
            self.updateTimer()

        self.ticker = None
        return


class soSkillGUI(PyGUIBase):
    factoryString = 'soGUI.soSkillGUI'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.currentTab = LEVELING.SPEC_EQUIPMENT
        self.currentSpec = None
        self.tabLabels = {LEVELING.SPEC_EQUIPMENT: lc('GUI.LevelingGUI.EQUIPMENT_SPEC_TAB_LABEL'),
         LEVELING.SPEC_MEDICINE: lc('GUI.LevelingGUI.MEDICINE_SPEC_TAB_LABEL'),
         LEVELING.SPEC_WEAPONRY: lc('GUI.LevelingGUI.WEAPONRY_SPEC_TAB_LABEL'),
         LEVELING.SPEC_REAPIRS: lc('GUI.LevelingGUI.REPAIRS_SPEC_TAB_LABEL')}
        self.expInvestWnd = None
        self.interfaceID = GUI_ID.GUI_ID_SKILLS
        self.playedTime = 0
        self.description_callback = lambda sID: u''
        self.naming_callback = lambda sID: u''
        self.texturing_callback = lambda sID: u''
        self.skill_state_callback = lambda sID: LEVELING.STATE_CANLEARN
        self.skill_type_callback = lambda sID: LEVELING.TYPE_ABILITY
        self.specsTree = {LEVELING.SPEC_EQUIPMENT: [],
         LEVELING.SPEC_MEDICINE: [],
         LEVELING.SPEC_WEAPONRY: [],
         LEVELING.SPEC_REAPIRS: []}
        self.advancedSkills = {}
        self.setupRoot()
        self.setupVisuals()
        self.setupLabels()
        self.setupControls()
        self.setupInvestWnd()
        self.playedTicker = self.timeTicker()
        self.playedTicker.run()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        cmp.width = 1024
        cmp.height = 639
        cmp.position = (0.0, 0.0, 0.09)

    def setupVisuals(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'dFrame')
        cmp = GUI.Frame2('soGUI/maps/Controls/skills/20/panelWhole.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 279
        cmp.height = 24
        cmp.position = (4, 31, 0.85)
        self.component.addChild(cmp, 'dFrame_level')
        cmp = GUI.Frame2('soGUI/maps/Controls/skills/20/AS_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 279
        cmp.height = 83
        cmp.position = (310, 411, 0.7)
        self.component.addChild(cmp, 'dFrame_ASkills')
        cmp = GUI.Frame2('soGUI/maps/Controls/skills/20/panelWhole.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 323
        cmp.height = 24
        cmp.position = (286, 31, 0.85)
        self.component.addChild(cmp, 'dFrame_proffession')
        cmp = GUI.Frame2('soGUI/maps/Controls/skills/20/panelWhole.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 408
        cmp.height = 24
        cmp.position = (612, 31, 0.85)
        self.component.addChild(cmp, 'dFrame_rank')
        cmp = GUI.Frame2('soGUI/maps/Controls/skills/20/panelWhole.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 279
        cmp.height = 443
        cmp.position = (4, 57, 0.85)
        self.component.addChild(cmp, 'dFrame_basicSkills')
        cmp = GUI.Frame2('soGUI/maps/Controls/skills/20/panelWhole.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 734
        cmp.height = 443
        cmp.position = (286, 57, 0.85)
        self.component.addChild(cmp, 'dFrame_advancedSkills')
        cmp = GUI.Frame2('soGUI/maps/Controls/skills/20/panelTopless.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 410
        cmp.height = 28
        cmp.position = (610, 499, 0.85)
        self.component.addChild(cmp, 'dFrame_specPoints')
        cmp = GUI.Frame2('soGUI/maps/Controls/skills/20/panelWhole.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 603
        cmp.height = 24
        cmp.position = (4, 503, 0.85)
        self.component.addChild(cmp, 'dFrame_freeExp')
        cmp = GUI.Frame2('soGUI/maps/Controls/skills/20/panelWhole.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 907
        cmp.height = 71
        cmp.position = (4, 530, 0.85)
        self.component.addChild(cmp, 'dFrame_desription')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 732
        cmp.height = 1
        cmp.position = (287, 86, 0.84)
        self.component.addChild(cmp, 'dLine1')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 409
        cmp.height = 1
        cmp.position = (610, 86, 0.84)
        self.component.addChild(cmp, 'dLine2')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 409
        cmp.height = 1
        cmp.position = (610, 499, 0.84)
        self.component.addChild(cmp, 'dLine3')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 323
        cmp.height = 1
        cmp.position = (287, 383, 0.84)
        self.component.addChild(cmp, 'dLine4')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 323
        cmp.height = 1
        cmp.position = (287, 406, 0.84)
        self.component.addChild(cmp, 'dLine5')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 323
        cmp.height = 1
        cmp.position = (287, 131, 0.84)
        self.component.addChild(cmp, 'dLine6')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 1
        cmp.height = 441
        cmp.position = (610, 58, 0.84)
        self.component.addChild(cmp, 'dLine7')

    def setupLabels(self):
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = u'Player Name'
        cmp.position = (18, 15, 0.8)
        self.component.addChild(cmp, 'pName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = lc('GUI.LevelingGUI.EXPERIENCE_LABEL') + u' 0'
        cmp.position = (10, 43, 0.8)
        self.component.addChild(cmp, 'experience')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = lc('GUI.LevelingGUI.LEVEL_LABEL') + u' 0'
        cmp.position = (277, 43, 0.8)
        self.component.addChild(cmp, 'level')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = u'Not Set'
        cmp.position = (292, 43, 0.8)
        self.component.addChild(cmp, 'faction')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = u'Not Set'
        cmp.position = (603, 43, 0.8)
        self.component.addChild(cmp, 'pClass')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = u'Not Set'
        cmp.position = (618, 43, 0.8)
        self.component.addChild(cmp, 'rank')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = lc('soSkillScreen.soGUI.STRING_2820_13')
        cmp.position = (1014, 43, 0.8)
        self.component.addChild(cmp, 'played')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_16i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = lc('GUI.LevelingGUI.ESSENTIAL_SKILLS_LABEL')
        cmp.position = (143, 82, 0.8)
        self.component.addChild(cmp, 'basicSkills')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = lc('GUI.LevelingGUI.SPECIALISATIONS_LABEL')
        cmp.position = (449, 73, 0.8)
        self.component.addChild(cmp, 'specialisations')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = lc('GUI.LevelingGUI.ADVANCED_SKILLS_LABEL')
        cmp.position = (815, 73, 0.8)
        self.component.addChild(cmp, 'class_skills')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = u''
        cmp.position = (815, 96, 0.8)
        self.component.addChild(cmp, 'spec_name')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = lc('GUI.LevelingGUI.SPECIALISATION_POINTS_LABEL') + u' 0'
        cmp.position = (815, 514, 0.8)
        self.component.addChild(cmp, 'specPoints')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = lc('GUI.LevelingGUI.AVAILABLE_EXPERIENCE_LABEL') + u' 0'
        cmp.position = (305, 514, 0.8)
        self.component.addChild(cmp, 'freeExp')

    def setupControls(self):
        for i in xrange(2):
            for j in xrange(3):
                btn = soButtonWFT(GUI.Window(''))
                cmp = btn.component
                cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.width = 106
                cmp.height = 21
                cmp.position = (288 + j * 106, 89 + i * 21, 0.4)
                btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
                btn.initVSC('soGUI/visual_styles/charScreenTab.xml')
                btn.onBound()
                tabN = i * 3 + j
                btn.onClick = partial(self.tabHandler, tabN)
                if self.tabLabels.has_key(tabN):
                    cmp.label.text = self.tabLabels[tabN]
                else:
                    cmp.label.text = u''
                    btn.buttonDisabled = True
                if tabN == 0:
                    btn.buttonActive = True
                btn._updateVisualState()
                self.component.addChild(cmp, 'spec_tab_{0}'.format(tabN))

        btn = soButtonWFT(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 321
        cmp.height = 21
        cmp.position = (288, 385, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.buttonActive = True
        btn.initVSC('soGUI/visual_styles/charScreenTab.xml')
        btn.onBound()
        btn.onClick = partial(self.tabHandler, -1)
        cmp.label.text = lc('GUI.LevelingGUI.ACTIVE_SKILLS_LABEL')
        btn._updateVisualState()
        self.component.addChild(cmp, 'activeSkillsTab')
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
        cmp.position = (1000, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        txt = soTextField3(GUI.Window(), width=907, height=71, textWidth=-1, hScroll=False, vScroll=True, hideScroll=False, borderWidth=0, vOffset=5, hOffset=5, textureless=True, autosize=False)
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (4, 530, 0.2)
        self.component.addChild(cmp, 'description')
        txt.onBound()
        itemView = soItemView(GUI.Window(), soBSkillSlot, slot_eventsHandler=self.BSlotHandler, eventsHandler=self.BIVHandler, rowWidth=4, cols=4, rows=6, hScroll=False, borderWidth=0, hInterval=1, vInterval=1)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (6, 109, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'BSkills')
        itemView.onBound()
        itemView.setRestrictingComponent(None)
        itemView.setItems(None)
        itemView = soItemView(GUI.Window(), soAdSkillSlot, slot_eventsHandler=self.AdSlotHandler, eventsHandler=self.AdIVHandler, rowWidth=6, cols=6, rows=6, hScroll=False, borderWidth=0, hInterval=1, vInterval=1)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (613, 109, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'AdSkills')
        itemView.onBound()
        itemView.setRestrictingComponent(None)
        itemView.setItems(None)
        itemView = soItemView(GUI.Window(), soASkillSlot, slot_eventsHandler=self.ASlotHandler, eventsHandler=self.AIVHandler, rowWidth=4, cols=4, rows=1, hScroll=False, borderWidth=0, hInterval=1)
        cmp = itemView.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (311, 412, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'ASkills')
        itemView.onBound()
        itemView.setRestrictingComponent(None)
        itemView.setItems(None)
        specList = soList2(GUI.Window(), width=323, height=251, elemHandler=self._specElemHandler)
        cmp = specList.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (287, 132, 0.2)
        self.component.addChild(cmp, 'specList')
        specList.onBound()
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (916, 532, 0.3)
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn._updateVisualState()
        btn.onBound()
        cmp.label.text = lc('GUI.LevelingGUI.CONFIRM_BUTTON_LABEL')
        self.component.addChild(cmp, 'confirmBtn')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (916, 568, 0.3)
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn._updateVisualState()
        btn.onBound()
        cmp.label.text = lc('GUI.LevelingGUI.CANCEL_BUTTON_LABEL')
        self.component.addChild(cmp, 'cancelBtn')
        return

    def setupInvestWnd(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.05)
        cmp.moveFocus = True
        cmp.crossFocus = True
        cmp.mouseButtonFocus = True
        cmp.dragFocus = True
        cmp.dropFocus = True
        cmp.visible = False
        self.component.addChild(cmp, 'expInvestWnd')
        self.expInvestWnd = cmp
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 306
        cmp.height = 166
        cmp.position = (0.0, 0.0, 0.9)
        self.expInvestWnd.addChild(cmp, 'innerFrame')
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.verticalAnchor = cmp.horizontalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.8)
        self.expInvestWnd.innerFrame.addChild(cmp, 'dFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = u'Skill Name'
        cmp.position = (18, 15, 0.8)
        self.expInvestWnd.innerFrame.addChild(cmp, 'sName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = lc('GUI.LevelingGUI.SPEND_EXPERIENCE_LABEL')
        cmp.position = (14, 47, 0.8)
        self.expInvestWnd.innerFrame.addChild(cmp, 'spendExpLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = lc('GUI.LevelingGUI.PROFESSION_MODIFIER_LABEL')
        cmp.position = (14, 67, 0.8)
        self.expInvestWnd.innerFrame.addChild(cmp, 'modifierLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = lc('GUI.LevelingGUI.SPECIALISATION_POINTS_LABEL')
        cmp.position = (14, 87, 0.8)
        self.expInvestWnd.innerFrame.addChild(cmp, 'specPointsLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = u'0'
        cmp.position = (92, 105, 0.8)
        self.expInvestWnd.innerFrame.addChild(cmp, 'specPoints')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = u'0'
        cmp.position = (282, 47, 0.8)
        self.expInvestWnd.innerFrame.addChild(cmp, 'spendExp')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = u'x1\\10'
        cmp.position = (282, 67, 0.8)
        self.expInvestWnd.innerFrame.addChild(cmp, 'modifier')
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
        cmp.position = (282, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.expInvestWnd.innerFrame.addChild(cmp, 'closeBox')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.soundControlName = 'PlusMinusBtn'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 18
        cmp.position = (184, 97, 0.3)
        btn.initVSC('soGUI/visual_styles/minusBtn.xml')
        btn._updateVisualState()
        btn.onClick = partial(self.expInvestPMHandler, -1)
        btn.onBound()
        self.expInvestWnd.innerFrame.addChild(cmp, 'minusBtn')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.soundControlName = 'PlusMinusBtn'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 18
        cmp.position = (275, 97, 0.3)
        btn.initVSC('soGUI/visual_styles/plusBtn.xml')
        btn._updateVisualState()
        btn.onClick = partial(self.expInvestPMHandler, 1)
        btn.onBound()
        self.expInvestWnd.innerFrame.addChild(cmp, 'plusBtn')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (47, 133, 0.3)
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn._updateVisualState()
        btn.onBound()
        cmp.label.text = lc('GUI.LevelingGUI.CONFIRM_BUTTON_LABEL')
        self.expInvestWnd.innerFrame.addChild(cmp, 'confirmBtn')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (157, 133, 0.3)
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn._updateVisualState()
        btn.onBound()
        cmp.label.text = lc('GUI.LevelingGUI.CANCEL_BUTTON_LABEL')
        self.expInvestWnd.innerFrame.addChild(cmp, 'cancelBtn')
        edit = soEditBox(GUI.Window(), width=70, height=21, font='ruRU_Cyrvetica_Extra_12i.font', hOffset=3, vOffset=3, inputValidator=self.expInvestInputHandler, autosize=False)
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (204, 96, 0.5)
        self.expInvestWnd.innerFrame.addChild(cmp, 'edit')
        edit.onBound()
        edit.setValue(u'0')

    def timeToString(self, secs):
        if secs < 0:
            return u''
        days = floor(secs / 86400.0)
        hours = floor((secs - days * 86400) / 3600.0)
        outD = int(days)
        outH = int(hours)
        return lc('soSkillScreen.soGUI.STRING_3303_9').format(outD, outH)

    def _specElemHandler(self, event, data):
        if self.currentSpec is not None and data.id != self.currentSpec:
            self.component.specList.script.deactivateElems([[self.currentSpec]])
        self.currentSpec = data.id
        self.component.description.script.setText(self.description_callback(self.currentSpec))
        if event == soSpecListElem.EVENT_INVEST:
            self.showExpInvest(True, data.elemData['spec_name'], data.elemData['modifier'], data.elemData['spec_points'])
        self.component.spec_name.text = data.elemData['spec_name']
        self.component.specPoints.text = u'{0} {1}'.format(lc('GUI.LevelingGUI.SPECIALISATION_POINTS_LABEL'), data.elemData['spec_points'])
        self.selectSkill(None, 'spec')
        self._updateAdSkills()
        return

    def expInvestInputHandler(self, newStr, wholeText, offset):
        valStr = wholeText
        if offset == len(wholeText):
            valStr += newStr
        elif offset < len(wholeText):
            valStr = wholeText[:offset] + newStr + wholeText[offset:]
        if valStr.isdigit():
            for spec in self.specsTree[self.currentTab]:
                if spec['id'] == self.currentSpec:
                    if int(valStr) * spec['modifier'][0] <= self._getFreeExp():
                        return True

        return False

    def expInvestPMHandler(self, dir, down = True):
        val = int(self.expInvestWnd.innerFrame.edit.script.getRaw())
        if dir > 0:
            val += 1
        else:
            val -= 1
        if val < 0:
            return
        for spec in self.specsTree[self.currentTab]:
            if spec['id'] == self.currentSpec:
                if val * spec['modifier'][0] <= self._getFreeExp():
                    self.expInvestWnd.innerFrame.edit.script.setValue(str(val))

    def showExpInvest(self, doShow = True, caption = u'', mod = [1, 1], specPoints = 0):
        self.expInvestWnd.innerFrame.sName.text = caption
        self.currentExpConverter = mod
        self.expInvestWnd.innerFrame.specPoints.text = str(specPoints)
        self.expInvestWnd.innerFrame.spendExp.text = u'0'
        self.expInvestWnd.innerFrame.modifier.text = u'x{0}\\{1}'.format(mod[0], mod[1])
        self.expInvestWnd.innerFrame.edit.script.setValue(u'0')
        self.expInvestWnd.visible = doShow

    def expInvestConfirm(self):
        val = int(self.expInvestWnd.innerFrame.edit.script.getRaw())
        BWPersonality.GUICore.skillEvent(LEVELING.EVENT_INVESTEXP, [self.currentSpec, val])
        self.showExpInvest(False)

    def expInvestCancel(self):
        self.showExpInvest(False)

    def _getFreeExp(self):
        return int(self.component.freeExp.text)

    def tabHandler(self, tab):
        for i in xrange(2):
            for j in xrange(3):
                tabN = i * 3 + j
                cmp = getattr(self.component, 'spec_tab_{0}'.format(tabN), None)
                if cmp:
                    btn = cmp.script
                    btn.buttonActive = False if tab != tabN else True
                    btn._updateVisualState()

        if tab == self.currentTab:
            return
        else:
            self.currentTab = tab
            self._updateSpecList()
            return

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'skillGUI')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def update(self, data):
        if data.has_key('free_exp'):
            self.component.freeExp.text = str(data['free_exp']).encode('utf-8')
        if data.has_key('pName'):
            self.component.pName.text = data['pName']
        if data.has_key('exp'):
            self.component.experience.text = str(data['exp']).encode('utf-8')
        if data.has_key('played'):
            self.playedTime = data['played']
            self._updatePlayed()
        if data.has_key('class'):
            self.component.pClass.text = data['class']
        if data.has_key('faction'):
            self.component.faction.text = data['faction']
        if data.has_key('rank'):
            self.component.rank.text = data['rank']
        if data.has_key('level'):
            self.component.level.text = str(data['level']).encode('utf-8')
        if data.has_key('description_callback'):
            self.description_callback = data['description_callback']
        if data.has_key('naming_callback'):
            self.naming_callback = data['naming_callback']
        if data.has_key('texturing_callback'):
            self.texturing_callback = data['texturing_callback']
        if data.has_key('skill_state_callback'):
            self.skill_state_callback = data['skill_state_callback']
        if data.has_key('skill_type_callback'):
            self.skill_type_callback = data['skill_type_callback']
        if data.has_key('basic_skills'):
            self.setBasicSkills(data['basic_skills'])
        if data.has_key('spec_trees'):
            for specTree in data['spec_trees']:
                self.setSpecTree(specTree, data['spec_trees'][specTree])

        if data.has_key('advanced_skills'):
            for spec in data['advanced_skills']:
                self.setAdvancedSkills(spec, data['advanced_skills'][spec])

        if data.has_key('active_skills'):
            self.setActiveSkills(data['active_skills'])

    def _updateSpecList(self):
        self.component.specList.script.clear()
        elems = []
        specs = self.specsTree[self.currentTab]
        for spec in specs:
            elem = [spec['id'], soSpecListElem, {'spec_name': spec['spec_name'],
              'modifier': spec['modifier'],
              'spec_points': spec['spec_points']}]
            elems.append(elem)

        self.component.specList.script.addElems(elems)
        for spec in self.specsTree[self.currentTab]:
            if spec['id'] == self.currentSpec:
                self.component.specList.script.activateElems([[self.currentSpec]])

    def _updateAdSkills(self):
        if self.currentSpec is not None:
            skills = None
            if self.advancedSkills.has_key(self.currentSpec):
                skills = self.advancedSkills[self.currentSpec]
            self.component.AdSkills.script.setItems(skills)
        else:
            self.component.AdSkills.script.setItems(None)
        return

    def _updatePlayed(self):
        self.component.played.text = self.timeToString(self.playedTime)

    def updateBasicSkills(self):
        self.component.BSkills.script._applyItems()

    def setBasicSkills(self, skills):
        self.component.BSkills.script.setItems(skills)

    def setSpecTree(self, spec_tree, specs):
        self.specsTree[spec_tree] = specs
        if spec_tree == self.currentTab:
            self._updateSpecList()

    def setSpec(self, spec_tree, spec):
        for spec_ in self.specsTree[spec_tree]:
            if spec_['id'] == spec['id']:
                spec_['modifier'] = spec['modifier']
                spec_['spec_name'] = spec['spec_name']
                spec_['spec_points'] = spec['spec_points']
                if self.currentTab == spec_tree:
                    self._updateSpecList()

        self.specsTree[spec_tree].append(spec)

    def updateAdvancedSkills(self):
        self.component.AdSkills.script._applyItems()

    def setAdvancedSkills(self, spec_id, skills):
        self.advancedSkills[spec_id] = skills
        if self.currentSpec == spec_id:
            self._updateAdSkills()

    def updateActiveSkills(self):
        self.component.ASkills.script._applyItems()

    def setActiveSkills(self, skills):
        self.component.ASkills.script.setItems(skills)

    def selectSkill(self, sID, selType = 'skill'):
        for name, child in self.component.BSkills.children:
            if 'slot' in name:
                if selType == 'skill':
                    child.script.select(False)
                if child.script.haveItem():
                    if child.script.itemData['id'] == sID:
                        child.script.select(True)

        for name, child in self.component.AdSkills.children:
            if 'slot' in name:
                child.script.select(False)
                if child.script.haveItem():
                    if child.script.itemData['id'] == sID:
                        child.script.select(True)

    def BSlotHandler(self, event, data):
        if event == module_soItemView.SLOTEVENT_LCLICK:
            if data.haveItem():
                self.selectSkill(data.itemData['id'])
                self.component.description.script.setText(self.description_callback(data.itemData['id']))
                return True
        if event == module_soItemView.SLOTEVENT_RCLICK:
            if data.haveItem():
                self.selectSkill(data.itemData['id'])
                self.component.description.script.setText(self.description_callback(data.itemData['id']))
                BWPersonality.GUICore.skillEvent(LEVELING.EVENT_CONTEXT, data.itemData['id'])
                return True
        if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
            BWPersonality.GUICore.toolTipEvent(None, None, soToolTipComponent.EVENT_HIDE)
            return True
        else:
            if event == module_soItemView.SLOTEVENT_MOUSEENTER:
                if data.haveItem():
                    BWPersonality.GUICore.toolTipEvent(data.itemData['id'], self.interfaceID, soToolTipComponent.EVENT_SHOW)
                    return True
            if event == module_soItemView.SLOTEVENT_DBLCLICK:
                if data.haveItem():
                    BWPersonality.GUICore.skillEvent(LEVELING.EVENT_ACTION, data.itemData['id'])
                    return True
            return False

    def BIVHandler(self, event, data):
        return False

    def AdSlotHandler(self, event, data):
        if event == module_soItemView.SLOTEVENT_LCLICK:
            if data.haveItem():
                self.selectSkill(data.itemData['id'])
                self.component.description.script.setText(self.description_callback(data.itemData['id']))
                return True
        if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
            BWPersonality.GUICore.toolTipEvent(None, None, soToolTipComponent.EVENT_HIDE)
            return True
        else:
            if event == module_soItemView.SLOTEVENT_MOUSEENTER:
                if data.haveItem():
                    BWPersonality.GUICore.toolTipEvent(data.itemData['id'], self.interfaceID, soToolTipComponent.EVENT_SHOW)
                    return True
            if event == module_soItemView.SLOTEVENT_DBLCLICK:
                if data.haveItem():
                    BWPersonality.GUICore.skillEvent(LEVELING.EVENT_ACTION, data.itemData['id'])
                    return True
            return False

    def AdIVHandler(self, event, data):
        return False

    def ASlotHandler(self, event, data):
        if event == module_soItemView.EVENT_DRAGENTER:
            if isinstance(data[1], soAdSkillSlot):
                return True
        if event == module_soItemView.EVENT_DROP:
            if isinstance(data[1], soAdSkillSlot):
                if data[0].haveItem():
                    BWPersonality.GUICore.skillEvent(LEVELING.EVENT_SETACTIVE, [data[1].itemData['id'], data[0].itemData['id']])
                else:
                    BWPersonality.GUICore.skillEvent(LEVELING.EVENT_SETACTIVE, [data[1].itemData['id'], None])
                return True
        if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
            BWPersonality.GUICore.toolTipEvent(None, None, soToolTipComponent.EVENT_HIDE)
            return True
        else:
            if event == module_soItemView.SLOTEVENT_MOUSEENTER:
                if data.haveItem():
                    BWPersonality.GUICore.toolTipEvent(data.itemData['id'], self.interfaceID, soToolTipComponent.EVENT_SHOW)
                    return True
            return False

    def AIVHandler(self, event, data):
        return False

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()

    @PyGUIEvent('confirmBtn', 'onClick')
    def onConfirm(self):
        BWPersonality.GUICore.skillEvent(LEVELING.EVENT_CONFIRM, None)
        return

    @PyGUIEvent('cancelBtn', 'onClick')
    def onCancel(self):
        BWPersonality.GUICore.skillEvent(LEVELING.EVENT_CANCEL, None)
        return

    @PyGUIEvent('expInvestWnd.innerFrame.closeBox', 'onClick')
    def onExpCloseBox(self):
        self.showExpInvest(False)

    @PyGUIEvent('expInvestWnd.innerFrame.confirmBtn', 'onClick')
    def onExpConfirm(self):
        self.expInvestConfirm()

    @PyGUIEvent('expInvestWnd.innerFrame.cancelBtn', 'onClick')
    def onExpCancel(self):
        self.expInvestCancel()

    @PyGUIEvent('expInvestWnd.innerFrame.edit', 'onValueChange')
    def onExpEditValue(self, byUser):
        valStr = self.expInvestWnd.innerFrame.edit.script.getRaw()
        if not valStr:
            self.expInvestWnd.innerFrame.spendExp.text = u'0'
        else:
            for spec in self.specsTree[self.currentTab]:
                if spec['id'] == self.currentSpec:
                    self.expInvestWnd.innerFrame.spendExp.text = str(spec['modifier'][0] * int(valStr))

    @BWMemberCoroutine
    def timeTicker(self):
        while True:
            yield BWWaitForPeriod(60.0)
            self.playedTime += 60.0
            self._updatePlayed()