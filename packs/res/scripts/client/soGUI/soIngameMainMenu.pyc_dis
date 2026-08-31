# Embedded file name: scripts/client/soGUI/soIngameMainMenu.py
import BigWorld
import BWPersonality
import soGUI
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI.PyGUIBase import PyGUIBase
import GUI
from soGUI.soButton import soButton
from Helpers.PyGUI import PyGUIEvent
from Localization import lc
from gui_const import MESSAGEBOX

class soIngameMainMenu(PyGUIBase):
    factoryString = 'soGUI.soIngameMainMenu'
    EVENT_RESUME = 0
    EVENT_OPTIONS = 1
    EVENT_LOGOFF = 2
    EVENT_QUIT = 3

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 125)
        cmp.materialFX = 'BLEND'
        cmp.textureName = 'soGUI/maps/Colours/black.bmp'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.05)
        cmp.visible = False
        cmp.moveFocus = True
        cmp.crossFocus = True
        cmp.mouseButtonFocus = True

    def setupContent(self):
        sW, sH = BigWorld.screenSize()
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = 37
        cmp.label.text = lc('GUI.IngameMenu.changeTeam')
        cmp.position = (sW / 2.0, sH / 2.0 - 194, 0.2)
        cmp.textureName = 'soGUI/maps/Controls/ingameMenu/resume_game.tga'
        cmp.visible = False
        self.component.addChild(cmp, 'changeTeam')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = 37
        cmp.label.text = lc('GUI.IngameMenu.leaveFromRoom')
        cmp.position = (sW / 2.0, sH / 2.0 - 154, 0.2)
        cmp.textureName = 'soGUI/maps/Controls/ingameMenu/resume_game.tga'
        cmp.visible = False
        self.component.addChild(cmp, 'pvpLeave')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = 37
        cmp.label.text = 'PVP(debug)'
        cmp.position = (sW / 2.0, sH / 2.0 - 114, 0.2)
        cmp.textureName = 'soGUI/maps/Controls/ingameMenu/resume_game.tga'
        cmp.visible = 0
        self.component.addChild(cmp, 'pvpBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = 37
        cmp.label.text = lc('GUI.IngameMenu.RESUME_GAME_BTN_LABEL')
        cmp.position = (sW / 2.0, sH / 2.0 - 74, 0.2)
        cmp.textureName = 'soGUI/maps/Controls/ingameMenu/resume_game.tga'
        self.component.addChild(cmp, 'resumeBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = 37
        cmp.label.text = lc('GUI.IngameMenu.OPTIONS_BTN_LABEL')
        cmp.position = (sW / 2.0, sH / 2.0 - 37, 0.2)
        cmp.textureName = 'soGUI/maps/Controls/ingameMenu/options.tga'
        self.component.addChild(cmp, 'optionsBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = 37
        cmp.label.text = lc('GUI.IngameMenu.LOGOUT_BTN_LABEL')
        cmp.position = (sW / 2.0, sH / 2.0, 0.2)
        cmp.textureName = 'soGUI/maps/Controls/ingameMenu/logoff.tga'
        self.component.addChild(cmp, 'logoffBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = 37
        cmp.label.text = lc('GUI.IngameMenu.QUIT_GAME_BTN_LABEL')
        cmp.position = (sW / 2.0, sH / 2.0 + 37, 0.05)
        cmp.textureName = 'soGUI/maps/Controls/ingameMenu/quit_game.tga'
        self.component.addChild(cmp, 'quitBtn')
        btn.onBound()
        btn.setVisualState('normal')

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.generalLayer.addChild(self.component, 'escMenu')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        p = BigWorld.player()
        inPVPinstance = getattr(p, 'inPVPinstance', 0)
        self.change_inPVPinstance(inPVPinstance)
        return

    def change_inPVPinstance(self, value):
        self.component.pvpLeave.visible = value
        self.component.changeTeam.visible = value

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def resumeGame(self):
        BWPersonality.GUICore.ingameMenuEvent(self.EVENT_RESUME, None)
        self.hide()
        return

    def wantOptions(self):
        BWPersonality.GUICore.showOptions(callback=self.show)

    def logoff(self):
        BigWorld.player().playerLogOff()
        BWPersonality.GUICore.ingameMenuEvent(self.EVENT_LOGOFF, None)
        self.hide()
        return

    def quitGame(self):
        BigWorld.player().playerLogOff()
        BWPersonality.GUICore.ingameMenuEvent(self.EVENT_QUIT, None)
        return

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.resumeBtn.position = (sW / 2.0, sH / 2.0 - 74, 0.2)
        self.component.optionsBtn.position = (sW / 2.0, sH / 2.0 - 37, 0.2)
        self.component.logoffBtn.position = (sW / 2.0, sH / 2.0, 0.2)
        self.component.quitBtn.position = (sW / 2.0, sH / 2.0 + 37, 0.2)
        self.component.pvpBtn.position = (sW / 2.0, sH / 2.0 - 114, 0.2)
        self.component.pvpLeave.position = (sW / 2.0, sH / 2.0 - 154, 0.2)
        self.component.changeTeam.position = (sW / 2.0, sH / 2.0 - 194, 0.2)

    @PyGUIEvent('changeTeam', 'onClick')
    def onchangeTeamClick(self):
        self.hide()
        BWPersonality.GUICore.showChoiceTeam(True)

    @PyGUIEvent('pvpLeave', 'onClick')
    def onPVPLeaveClick(self):
        BigWorld.player().base.leaveFromRoom()
        self.hide()

    @PyGUIEvent('pvpBtn', 'onClick')
    def onPVPClick(self):
        BWPersonality.GUICore.showSelectMap(True)
        self.hide()

    @PyGUIEvent('resumeBtn', 'onClick')
    def onResumeClick(self):
        self.resumeGame()

    @PyGUIEvent('optionsBtn', 'onClick')
    def onOptionsClick(self):
        self.wantOptions()
        self.hide()

    @PyGUIEvent('logoffBtn', 'onClick')
    def onLogoffClick(self):
        self.logoff()

    @PyGUIEvent('quitBtn', 'onClick')
    def onQuitClick(self):
        self.hide()
        BWPersonality.GUICore.showQuitMenu(callbackYes=self.quitGame, callbackNo=self.show)