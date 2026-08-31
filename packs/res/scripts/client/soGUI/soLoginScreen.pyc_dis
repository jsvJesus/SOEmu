# Embedded file name: scripts/client/soGUI/soLoginScreen.py
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import BWPersonality
import VersionSO
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soEditField import soEditField2, soEditBox
from soGUI.soButton import soButton
from soGUI.soCheckBox import soCheckBox
from Helpers.PyGUI import PyGUIEvent
from gui_const import MESSAGEBOX
from soGUI.soQuitMenu import soQuitMenu
from Keys import *
from Localization import lc
from gui_const import LOGIN
from soGUI.soRadioButton import soRadioButton2, soRadioButton, RadioButtonPropsStructure

class soLoginScreen(PyGUIBase):
    factoryString = 'soGUI.soLoginScreen'
    EVENT_LOGIN = 0
    EVENT_QUITGAME = 1

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.miscFrame = None
        self.optionsBtn = None
        self.creditsBtn = None
        self.setupRoot()
        self.setupLoginFrame()
        self.setupMiscFrame()
        self.component.loginFrame.loginEdit.script.setActive()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.0)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.focus = True
        cmp.textureName = ''

    def setupLoginFrame(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.width = 264
        cmp.height = 146
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0.0, 0.0, 1.0)
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        self.component.addChild(cmp, 'loginFrame')
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.width = 264
        cmp.height = 146
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0.0, 0.0, 1.0)
        self.component.loginFrame.addChild(cmp, 'dFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (132, 18, 0.3)
        cmp.text = lc('GUI.TitleMenu.LOGIN_WINDOW_CAPTION')
        self.component.loginFrame.addChild(cmp, 'iLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.text = lc('GUI.TitleMenu.LOGIN_WINDOW_LOGIN_LABEL')
        cmp.position = (51, 51, 0.9)
        self.component.loginFrame.addChild(cmp, 'loginLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.text = lc('GUI.TitleMenu.LOGIN_WINDOW_PASSWORD_LABEL')
        cmp.position = (51, 75, 0.9)
        self.component.loginFrame.addChild(cmp, 'pwdLabel')
        loginEdit = soEditField2(GUI.Window(), height=22, width=138)
        loginEdit.onBound()
        cmp = loginEdit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (93, 39, 0.5)
        self.component.loginFrame.addChild(cmp, 'loginEdit')
        pwdEdit = soEditField2(GUI.Window(), height=22, width=138, maskChar='*')
        pwdEdit.onBound()
        cmp = pwdEdit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (93, 64, 0.5)
        self.component.loginFrame.addChild(cmp, 'pwdEdit')
        loginBtn = soButton(GUI.Window())
        loginBtn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        loginBtn.onBound()
        loginBtn.component.label.font = 'ruRU_calibri_default.font'
        loginBtn.component.label.text = lc('GUI.TitleMenu.LOGIN_WINDOW_LOGIN_BUTTON_LABEL')
        cmp = loginBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 120
        cmp.height = 22
        cmp.position = (82, 113, 0.5)
        self.component.loginFrame.addChild(cmp, 'loginBtn')
        cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=lc('GUI.TitleMenu.LOGIN_WINDOW_SAVE_PASSWORD_LABEL'), font='ruRU_calibri_small.font'))
        cmp = cb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (103, 88, 0.4)
        self.component.loginFrame.addChild(cmp, 'savePwd')

    def setupMiscFrame(self):
        sW, sH = BigWorld.screenSize()
        if self.miscFrame is None:
            self.miscFrame = GUI.Window()
        self.miscFrame.horizontalPositionMode = self.miscFrame.verticalPositionMode = 'PIXEL'
        self.miscFrame.widthMode = self.miscFrame.heightMode = 'PIXEL'
        self.miscFrame.horizontalAnchor = 'LEFT'
        self.miscFrame.verticalAnchor = 'BOTTOM'
        self.miscFrame.materialFX = 'BLEND'
        self.miscFrame.colour = (255, 255, 255, 255)
        self.miscFrame.textureName = ''
        self.miscFrame.visible = True
        self.miscFrame.width = 146
        self.miscFrame.height = 272
        self.miscFrame.position = (89, sH, 0.0)
        if not hasattr(self.component, 'miscFrame'):
            self.component.addChild(self.miscFrame, 'miscFrame')
        if self.optionsBtn is None:
            self.optionsBtn = soButton(GUI.Window())
        self.optionsBtn.component.horizontalPositionMode = self.optionsBtn.component.verticalPositionMode = 'PIXEL'
        self.optionsBtn.component.widthMode = self.optionsBtn.component.heightMode = 'PIXEL'
        self.optionsBtn.component.horizontalAnchor = 'LEFT'
        self.optionsBtn.component.verticalAnchor = 'TOP'
        self.optionsBtn.component.materialFX = 'BLEND'
        self.optionsBtn.component.colour = (255, 255, 255, 255)
        self.optionsBtn.component.visible = True
        self.optionsBtn.component.width = 145
        self.optionsBtn.component.height = 37
        self.optionsBtn.component.position = (0, 64, 0.0)
        self.miscFrame.addChild(self.optionsBtn.component, 'optBtn')
        self.optionsBtn.initVSC('soGUI/visual_styles/btn_options.xml')
        self.optionsBtn.onBound()
        self.optionsBtn.setVisualState('normal')
        if self.creditsBtn is None:
            self.creditsBtn = soButton(GUI.Window())
        self.creditsBtn.component.horizontalPositionMode = self.creditsBtn.component.verticalPositionMode = 'PIXEL'
        self.creditsBtn.component.widthMode = self.creditsBtn.component.heightMode = 'PIXEL'
        self.creditsBtn.component.horizontalAnchor = 'LEFT'
        self.creditsBtn.component.verticalAnchor = 'TOP'
        self.creditsBtn.component.colour = (255, 255, 255, 255)
        self.creditsBtn.component.visible = True
        self.creditsBtn.component.materialFX = 'BLEND'
        self.creditsBtn.component.width = 103
        self.creditsBtn.component.height = 35
        self.creditsBtn.component.position = (0, 103, 0.0)
        self.miscFrame.addChild(self.creditsBtn.component, 'creditsBtn')
        self.creditsBtn.initVSC('soGUI/visual_styles/btn_credits.xml')
        self.creditsBtn.onBound()
        self.creditsBtn.buttonDisabled = True
        self.creditsBtn.setVisualState('disabled')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 94
        cmp.height = 37
        cmp.textureName = ''
        cmp.position = (0, 141, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.miscFrame.addChild(cmp, 'quitBtn')
        btn.initVSC('soGUI/visual_styles/btn_quit.xml')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 114
        cmp.height = 37
        cmp.textureName = ''
        cmp.position = (0, 26, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.miscFrame.addChild(cmp, 'addonsBtn')
        btn.initVSC('soGUI/visual_styles/btn_addons.xml')
        btn.onBound()
        btn.buttonDisabled = True
        btn.setVisualState('disabled')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 67
        cmp.height = 32
        cmp.textureName = ''
        cmp.position = (0, 0, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.miscFrame.addChild(cmp, 'siteBtn')
        btn.initVSC('soGUI/visual_styles/btn_site.xml')
        btn.onBound()
        btn.buttonDisabled = True
        btn.setVisualState('disabled')
        return

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.menuLayer.addChild(self.component, 'loginScreen')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False

    def handleKeyEvent(self, event):
        key = event.key
        char = event.character
        mods = event.modifiers
        down = event.isKeyDown()
        if key == KEY_TAB:
            if down:
                if not self.component.loginFrame.loginEdit.script.isEditActive() and not self.component.loginFrame.pwdEdit.script.isEditActive():
                    self.component.loginFrame.loginEdit.script.setActive()
                elif self.component.loginFrame.loginEdit.script.isEditActive():
                    self.component.loginFrame.pwdEdit.script.setActive()
                elif self.component.loginFrame.pwdEdit.script.isEditActive():
                    self.component.loginFrame.loginEdit.script.setActive()
        return False

    def update(self):
        if BWPersonality.GUICore.loginDataSection is not None:
            self.component.loginFrame.loginEdit.script.setValue(BWPersonality.GUICore.loginDataSection['login'])
            self.component.loginFrame.pwdEdit.script.setValue(BWPersonality.GUICore.loginDataSection['pwd'])
            if BWPersonality.GUICore.loginDataSection['autoSave']:
                self.component.loginFrame.savePwd.script.setActive()
            else:
                self.component.loginFrame.savePwd.script.setInactive()
        return

    def deactivateEdits(self):
        self.component.loginFrame.loginEdit.script.setActive(False)
        self.component.loginFrame.pwdEdit.script.setActive(False)

    def tryLogin(self, login, pwd):
        BWPersonality.GUICore.loginEvent(self.EVENT_LOGIN, (login, pwd, self.component.loginFrame.savePwd.script.isChecked()))

    def tryQuit(self, login, pwd):
        BWPersonality.GUICore.loginEvent(self.EVENT_QUITGAME, (login, pwd))

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.miscFrame.position = (89, sH, 0.0)

    @PyGUIEvent('loginFrame.loginEdit', 'eventReturn')
    def onLoginEntered(self):
        self.component.loginFrame.pwdEdit.script.setActive()

    @PyGUIEvent('loginFrame.pwdEdit', 'eventReturn')
    def onPwdEntered(self):
        self.tryLogin(self.component.loginFrame.loginEdit.script.getValue(), self.component.loginFrame.pwdEdit.script.getValue())

    @PyGUIEvent('loginFrame.loginBtn', 'onClick')
    def onLoginBtnClick(self):
        self.tryLogin(self.component.loginFrame.loginEdit.script.getValue(), self.component.loginFrame.pwdEdit.script.getValue())

    @PyGUIEvent('miscFrame.quitBtn', 'onClick')
    def onQuitBtnClick(self):
        self.tryQuit(self.component.loginFrame.loginEdit.script.getValue(), self.component.loginFrame.pwdEdit.script.getValue())

    @PyGUIEvent('miscFrame.optBtn', 'onClick')
    def optsBtnClicked(self):
        BWPersonality.GUICore.showOptions(True)


class soLoginScreen2(PyGUIBase):
    factoryString = 'soGUI.soLoginScreen2'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.isServVisible = False
        self.setupRoot()
        self.setupLoginFrame()
        self.setupContent()
        import Localization
        if Localization.localization_object.globalLanguage == 'russian':
            self.component.lanENG_Btn.script.setDisabledState(0)
            self.component.lanRU_Btn.script.setDisabledState(1)
        else:
            self.component.lanENG_Btn.script.setDisabledState(1)
            self.component.lanRU_Btn.script.setDisabledState(0)

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = 'soGUI/maps/Login/bg.jpg'
        cmp.filterType = 'LINEAR'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.3)

    def setupLoginFrame(self):
        cmp = GUI.Window('soGUI/maps/Login/win.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 256
        cmp.height = 128
        cmp.position = (0.0, 0.0, 0.5)
        self.component.addChild(cmp, 'loginWnd')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (140, 141, 126, 255)
        cmp.text = lc('GUI.TitleMenu.LOGIN_WINDOW_CAPTION').format(version=VersionSO.stalkerVersion)
        cmp.materialFX = 'BLEND'
        cmp.position = (128, 15, 0.5)
        self.component.loginWnd.addChild(cmp, 'caption')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (140, 141, 126, 255)
        cmp.text = lc('GUI.TitleMenu.LOGIN_WINDOW_LOGIN_LABEL')
        cmp.materialFX = 'BLEND'
        cmp.position = (50, 48, 0.5)
        self.component.loginWnd.addChild(cmp, 'loginCaption')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (140, 141, 126, 255)
        cmp.text = lc('GUI.TitleMenu.LOGIN_WINDOW_PASSWORD_LABEL')
        cmp.materialFX = 'BLEND'
        cmp.position = (50, 73, 0.5)
        self.component.loginWnd.addChild(cmp, 'pwdCaption')
        edit = soEditBox(GUI.Window(), width=128, height=20, font='ruRU_Cyrvetica_Extra_14i.font', hOffset=3, vOffset=2)
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (87, 38, 0.5)
        self.component.loginWnd.addChild(cmp, 'loginEdit')
        edit.onBound()
        edit = soEditBox(GUI.Window(), width=128, height=20, font='ruRU_Cyrvetica_Extra_14i.font', hOffset=3, vOffset=2, maskChar=u'*')
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (87, 63, 0.5)
        self.component.loginWnd.addChild(cmp, 'pwdEdit')
        edit.onBound()
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (78, 90, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.label.text = lc('GUI.TitleMenu.LOGIN_WINDOW_LOGIN_BUTTON_LABEL')
        self.component.loginWnd.addChild(cmp, 'logBtn')
        btn.initVSC('soGUI/visual_styles/mainMenuBtn.xml')
        btn.onBound()
        btn._updateVisualState()
        btn = soButton(GUI.Window())
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 19
        cmp.height = 18
        cmp.position = (220, 39, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.loginWnd.addChild(cmp, 'saveLogin')
        btn.initVSC('soGUI/visual_styles/saveLogin.xml')
        btn.onBound()
        btn._updateVisualState()

    def setupContent(self):
        sw, sh = BigWorld.screenSize()
        cmp = GUI.Window('soGUI/maps/Login/frame_menu.dds')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = sh
        cmp.position = (-1.0, 1.0, 0.9)
        cmp.filterType = 'LINEAR'
        self.component.addChild(cmp, 'mm_frame')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (74, 74, 74, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2
        cmp.height = sh
        cmp.position = (299, 0, 0.8)
        self.component.addChild(cmp, 'vLine1')
        cmp = GUI.Frame2('soGUI/maps/Login/blackout_1.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = sw - 300
        cmp.height = sh
        cmp.position = (300, 0, 0.9)
        self.component.addChild(cmp, 'blackBG')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.width = 30
        cmp.height = 21
        cmp.textureName = ''
        cmp.position = (125, sh - 139, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.label.text = lc('GUI.TitleMenu.LOGIN_WINDOW_lanRU')
        self.component.addChild(cmp, 'lanRU_Btn')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        btn.onClick = self.BtnRU
        btn.onBound()
        btn._updateVisualState()
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.width = 42
        cmp.height = 21
        cmp.textureName = ''
        cmp.position = (170, sh - 139, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.label.text = lc('GUI.TitleMenu.LOGIN_WINDOW_lanENG')
        self.component.addChild(cmp, 'lanENG_Btn')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        btn.onClick = self.BtnENG
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
        cmp.position = (150, sh - 99, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.label.text = lc('GUI.TitleMenu.LOGIN_WINDOW_OPTIONS_BUTTON_LABEL')
        self.component.addChild(cmp, 'optionsBtn')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
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
        cmp.label.text = lc('GUI.TitleMenu.LOGIN_WINDOW_QUIT_BUTTON_LABEL')
        self.component.addChild(cmp, 'quitBtn')
        btn.initVSC('soGUI/visual_styles/mainMenuBtnEmpty.xml')
        btn.onBound()
        btn._updateVisualState()

    def BtnENG(self):
        BWPersonality.settings.applyLanguage('english')

    def BtnRU(self):
        BWPersonality.settings.applyLanguage('russian')

    def showServ(self):
        if self.isServVisible:
            return
        self.isServVisible = True
        x, y = sW, sH = BigWorld.screenSize()
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (74, 74, 74, 200)
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = 200
        cmp.position = (sW / 2.0, sH - 30, 0.8)
        self.component.addChild(cmp, 'frameServ')

        def xonStateChange(server):
            print 'xonStateChange', server
            host = server.split('#', 1)[1]
            BWPersonality.game.dHost = host

        servers = ('test #update-a3.stalker.so:22231', 'dev #144.76.95.48:22231', 'msk #62.76.91.67:22231', 'hz-app1 #hz-app1.stalker.so:22231', 'hz-app2 #hz-app2.stalker.so:22231')
        for index, serv in enumerate(servers):
            rb = soRadioButton2(GUI.Window(), btnW=18, btnH=18, radioGroup='radiogr_servers', labelText=serv, bvisual_styles='soGUI/visual_styles/radioButton.xml')
            rb.onStateChange = lambda serv = serv: xonStateChange(serv)
            rb.onBound()
            cmp = rb.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.position = (sW / 2.0 - 130, sH - 100 - index * 25, 0.2)
            self.component.addChild(cmp, 'radio_%s' % index)
            rb.setInactive()

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.menuLayer.addChild(self.component, 'loginScreen')
        self.component.visible = True
        if BWPersonality.GUICore.currentMode == BWPersonality.GUICore.GAMEMODE_LOGIN:
            self.component.loginWnd.loginEdit.script.activate()
        else:
            self.deactivateEdits()
        return

    def hide(self):
        self.component.visible = False

    def update(self):
        if BWPersonality.GUICore.loginDataSection is not None:
            self.component.loginWnd.loginEdit.script.setValue(BWPersonality.GUICore.loginDataSection['login'])
            if BWPersonality.GUICore.loginDataSection['autoSave']:
                self.component.loginWnd.saveLogin.script.buttonActive = True
                self.component.loginWnd.pwdEdit.script.activate()
            else:
                self.component.loginWnd.saveLogin.script.buttonActive = False
        self.component.loginWnd.saveLogin.script._updateVisualState()
        return

    def _getLoginAndPwd(self):
        login = self.component.loginWnd.loginEdit.script.getRaw()
        pwd = self.component.loginWnd.pwdEdit.script.getRaw()
        return (login, pwd)

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.mm_frame.height = sH
        self.component.vLine1.height = sH
        self.component.blackBG.height = sH
        self.component.blackBG.width = sW - 300
        self.component.optionsBtn.position.y = sH - 99
        self.component.quitBtn.position.y = sH - 59

    def tryLogin(self):
        login, pwd = self._getLoginAndPwd()
        saveLogin = self.component.loginWnd.saveLogin.script.buttonActive
        BWPersonality.GUICore.loginEvent(LOGIN.EVENT_LOGIN, (login, pwd, saveLogin))

    def tryQuit(self):
        login, pwd = self._getLoginAndPwd()
        BWPersonality.GUICore.loginEvent(LOGIN.EVENT_QUITGAME, (login, pwd))

    def deactivateEdits(self):
        self.component.loginWnd.loginEdit.script.activate(False)
        self.component.loginWnd.pwdEdit.script.activate(False)

    @PyGUIEvent('loginWnd.loginEdit', 'onTab', 'login')
    @PyGUIEvent('loginWnd.pwdEdit', 'onTab', 'pwd')
    def onEditTab(self, edit):
        if edit == 'login':
            self.component.loginWnd.pwdEdit.script.activate()
        else:
            self.component.loginWnd.loginEdit.script.activate()

    @PyGUIEvent('loginWnd.loginEdit', 'onDefaultAction', 'login')
    @PyGUIEvent('loginWnd.pwdEdit', 'onDefaultAction', 'pwd')
    def onEditReturn(self, edit):
        if edit == 'login':
            self.component.loginWnd.pwdEdit.script.activate()
        elif not self.component.loginWnd.loginEdit.script.getRaw():
            self.component.loginWnd.loginEdit.script.activate()
        elif self.component.loginWnd.pwdEdit.script.getRaw():
            self.tryLogin()

    @PyGUIEvent('loginWnd.loginEdit', 'onEscape')
    @PyGUIEvent('loginWnd.pwdEdit', 'onEscape')
    def onEditEsc(self):
        self.component.loginWnd.pwdEdit.script.activate(False, silent=True)
        self.component.loginWnd.loginEdit.script.activate(False, silent=True)

    @PyGUIEvent('optionsBtn', 'onClick')
    def onOptionsBtn(self):
        if BWPersonality.GUICore.optionsGUI.component.visible == False:
            BWPersonality.GUICore.showOptions()

    @PyGUIEvent('quitBtn', 'onClick')
    def onQuitBtn(self):
        if BWPersonality.GUICore.optionsGUI.component.visible == False:
            BWPersonality.GUICore.showQuitMenu(callbackYes=self.onQuit, callbackNo=None)
        return

    def onQuit(self):
        self.deactivateEdits()
        self.tryQuit()

    @PyGUIEvent('loginWnd.logBtn', 'onClick')
    def onLoginBtn(self):
        self.deactivateEdits()
        self.tryLogin()