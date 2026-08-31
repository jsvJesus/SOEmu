# Embedded file name: scripts/client/soGUI/soTPCMainMenu.py
import BigWorld
import GUI
import soGUI
import Helpers.PyGUI as PyGUI
import BWPersonality
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soButton import soButton

class soTPCMainMenu(PyGUIBase):
    factoryString = 'soGUI.soTPCMainMenu'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.interfaceID = BWPersonality.GUICore.GUI_ID_PDAMAIN
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 792
        cmp.height = 521
        cmp.position = (0, 0, 0.1)
        cmp.textureName = ''
        cmp.visible = False

    def setupContent(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 786
        cmp.height = 24
        cmp.position = (3, 3, 0.8)
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/head/frame.tga'
        self.component.addChild(cmp, 'headFrame')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 32
        cmp.height = 16
        cmp.position = (748, 7, 0.7)
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/head/power_full.tga'
        self.component.addChild(cmp, 'power')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 20
        cmp.height = 13
        cmp.position = (8, 10, 0.7)
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/head/signal_full.tga'
        self.component.addChild(cmp, 'signal')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (697, 8, 0.7)
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colourFormatting = True
        cmp.text = u'\\c000000FF;10:40'
        self.component.addChild(cmp, 'time')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 786
        cmp.height = 492
        cmp.position = (3, 24, 0.9)
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/wallpaper.tga'
        self.component.addChild(cmp, 'wallpaper')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/btn_TPCMainLinks.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/quests.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 173
        cmp.height = 127
        cmp.position = (105, 68, 0.1)
        self.component.addChild(cmp, 'questLog')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/btn_TPCMainLinks.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/map.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 173
        cmp.height = 127
        cmp.position = (524, 214, 0.1)
        self.component.addChild(cmp, 'map')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/btn_TPCMainLinks.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/skills.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 173
        cmp.height = 127
        cmp.position = (105, 214, 0.1)
        btn.buttonDisabled = True
        self.component.addChild(cmp, 'skills')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/btn_TPCMainLinks.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/recipes.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 173
        cmp.height = 127
        cmp.position = (524, 68, 0.1)
        btn.buttonDisabled = True
        self.component.addChild(cmp, 'recipes')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/btn_TPCMainLinks.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/group.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 173
        cmp.height = 127
        cmp.position = (524, 359, 0.1)
        self.component.addChild(cmp, 'clan')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/btn_TPCMainLinks.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/beastiary.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 173
        cmp.height = 127
        cmp.position = (105, 359, 0.1)
        btn.buttonDisabled = True
        self.component.addChild(cmp, 'pedia')
        btn.onBound()
        btn.setVisualState('normal')

    @PyGUIEvent('questLog', 'onClick')
    def questBtnClicked(self):
        BWPersonality.GUICore.showQuestLog(True)

    @PyGUIEvent('skills', 'onClick')
    def skillsBtnClicked(self):
        BWPersonality.GUICore.showSkillsGUI(True)

    @PyGUIEvent('clan', 'onClick')
    def clanBtnClicked(self):
        BWPersonality.GUICore.showClanGUI(True)

    @PyGUIEvent('map', 'onClick')
    def mapBtnClicked(self):
        BWPersonality.GUICore.showGPS(True)