# Embedded file name: scripts/client/soGUI/soQuitMenu.py
import BigWorld
import BWPersonality
import soGUI
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI.PyGUIBase import PyGUIBase
import GUI
from soGUI.soButton import soButton
from Helpers.PyGUI import PyGUIEvent
from Localization import lc

class soQuitMenu(PyGUIBase):
    factoryString = 'soGUI.soQuitMenu'

    def __init__(self, component, callbackOnYesBtnClick = None, callbackOnNoBtnClick = None):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.callbackOnNoBtnClick = callbackOnNoBtnClick
        self.callbackOnYesBtnClick = callbackOnYesBtnClick
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 200)
        cmp.materialFX = 'BLEND'
        cmp.textureName = 'soGUI/maps/Colours/black.bmp'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 1.0)
        cmp.visible = False
        cmp.moveFocus = True
        cmp.crossFocus = True
        cmp.mouseButtonFocus = True

    def setupContent(self):
        sh, sw = BigWorld.screenSize()
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 35
        cmp.height = 30
        cmp.label.text = lc('GUI.QuitMenu.YES_BTN_LABEL')
        cmp.position = (sh / 2.0 - 50, sw / 2.0, 0.2)
        cmp.textureName = 'soGUI/maps/Controls/ingameMenu/resume_game.tga'
        btn.onClick = self.onClickToYesBtn
        self.component.addChild(cmp, 'YesBtn')
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
        cmp.width = 45
        cmp.height = 30
        cmp.label.text = lc('GUI.QuitMenu.NO_BTN_LABEL')
        cmp.position = (sh / 2.0 + 50, sw / 2.0, 0.2)
        cmp.textureName = 'soGUI/maps/Controls/ingameMenu/resume_game.tga'
        self.component.addChild(cmp, 'NoBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn.onClick = self.onBtnNOClick
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_large.font'
        cmp.colour = (140, 141, 126, 255)
        cmp.text = lc('GUI.QuitMenu.QUESTION_LABEL')
        cmp.materialFX = 'BLEND'
        cmp.position = (sh / 2.0, sw / 2.0 - 25, 0.2)
        self.component.addChild(cmp, 'loginCaption')

    def doReposition(self):
        sh, sw = BigWorld.screenSize()
        self.component.YesBtn.position = (sh / 2.0 - 50, sw / 2.0, 0.2)
        self.component.NoBtn.position = (sh / 2.0 + 50, sw / 2.0, 0.2)
        self.component.loginCaption.position = (sh / 2.0, sw / 2.0 - 25, 0.2)

    def onClickToYesBtn(self):
        self.Hide()
        self.callbackOnYesBtnClick()

    def onBtnNOClick(self):
        if self.callbackOnNoBtnClick is not None:
            self.callbackOnNoBtnClick()
        self.Hide()
        return

    def Show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.generalLayer.addChild(self.component, 'QuitMenu')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def Hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()