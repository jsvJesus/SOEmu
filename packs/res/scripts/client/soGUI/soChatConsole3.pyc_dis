# Embedded file name: scripts/client/soGUI/soChatConsole3.py
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
from Keys import *
import BWPersonality
from Helpers.BWKeyBindings import BWKeyBindingAction
import Helpers.BWKeyBindings as BWKeyBindings
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.BWCoroutine import *
from soGUI.soEditField import soEditField
from colorCodes import *
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
from soGUI.soVisualStateComponent import soVisualStateComponent
from soGUI.soTextField import soTextField2
from soGUI.soTextField import soTxtFieldPropsStructure
from soGUI.soEditField import soEditField2
from soGUI.soEditField import soEditBox
from soGUI.soEditField import soEditBox2
from soGUI.soTextField import soTextField3
from soGUI.soButton import soButton, soButtonWTT, soButtonWFT
from functools import partial
from soGUI.soCheckBox import soCheckBox
from gui_const import CHAT_CONSOLE
from soGUI.soResizeComponent import soResizeComponent
from Localization import lc
import chat_utils

class soChatConsole3(PyGUIBase, soResizeComponent):
    factoryString = 'soGUI.soChatConsole3'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        soResizeComponent.__init__(self, component, width=9, height=5, horizontal=False)
        component.script = self
        self.currentTab = CHAT_CONSOLE.TAB_ALL
        self.tab_settings = {CHAT_CONSOLE.TAB_ALL: [CHAT_CONSOLE.MESSAGE_DAMAGE | CHAT_CONSOLE.MESSAGE_ITEMS | CHAT_CONSOLE.MESSAGE_SYSTEM | CHAT_CONSOLE.MESSAGE_QUEST | CHAT_CONSOLE.MESSAGE_NPC | CHAT_CONSOLE.MESSAGE_GENERAL | CHAT_CONSOLE.MESSAGE_CLAN | CHAT_CONSOLE.MESSAGE_PARTY | CHAT_CONSOLE.MESSAGE_PRIVATE | CHAT_CONSOLE.MESSAGE_FRIENDS | CHAT_CONSOLE.MESSAGE_TRADE, False],
         CHAT_CONSOLE.TAB_CLAN: [CHAT_CONSOLE.MESSAGE_CLAN, False],
         CHAT_CONSOLE.TAB_PARTY: [CHAT_CONSOLE.MESSAGE_PARTY, True],
         CHAT_CONSOLE.TAB_PRIVATE: [CHAT_CONSOLE.MESSAGE_PRIVATE, False],
         CHAT_CONSOLE.TAB_FRIENDS: [CHAT_CONSOLE.MESSAGE_FRIENDS, False]}
        self.settingsWnd = None
        self.typing = False
        self.newSize = None
        self.fadeDelay = 2
        self.fadeSpeed = 1
        self.minHeight = 189
        self.fader = None
        self.setupRoot()
        self.setupContent()
        self.setupTabs()
        self.setupSettingsWnd()
        self.mouseFocus(False)
        return

    def setupRoot(self):
        sW, sH = BigWorld.screenSize()
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        cmp.crossFocus = True
        cmp.moveFocus = True
        cmp.width = 326
        cmp.height = 410
        cmp.position = (1, sH - 1, 0.01)
        shader = GUI.AlphaShader()
        shader.alpha = 1.0
        shader.speed = self.fadeSpeed
        self.component.addShader(shader, 'fader')
        cmp = self.component.resizer
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 9
        cmp.height = 5
        cmp.textureName = 'soGUI/maps/Misc/vertSizingCorner.tga'
        self.component.resizer.position = (313, 3, 0.1)

    def setupWidgets(self):
        pass

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/chat/frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'dFrame')
        edit = soEditBox2(GUI.Window(), width=287, height=29, font='ruRU_Cyrvetica_Extra_14i.font', hOffset=5, vOffset=5)
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (4, self.component.height - 57, 0.5)
        self.component.addChild(cmp, 'edit')
        edit.onBound()
        btn = soButtonWTT(GUI.Window(), 'chat_console_enter_btn')
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 29
        cmp.height = 29
        cmp.position = (293, self.component.height - 57, 0.4)
        btn.initVSC('soGUI/visual_styles/chatEnterBtn.xml')
        btn.onBound()
        btn._updateVisualState()
        self.component.addChild(cmp, 'enterBtn')
        btn = soButtonWTT(GUI.Window(), 'chat_console_settings_btn')
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (270, 6, 0.4)
        btn.initVSC('soGUI/visual_styles/chatSettingsBtn.xml')
        btn.onBound()
        btn._updateVisualState()
        self.component.addChild(cmp, 'settingsBtn')
        closeBox = soButton(GUI.Window())
        cmp = closeBox.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.visible = False
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (10, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeChat')
        cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText='stop scroll', font='ruRU_Cyrvetica_Extra_14i.font', labelColour=(175, 166, 112, 255)))
        cmp = cb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (50, 6, 0.3)
        cmp.visible = False
        self.component.addChild(cmp, 'stop_scroll')
        cb.onBound()
        for tab in xrange(5):
            txt = soTextField3(GUI.Window(), width=318, height=321, textWidth=-1, hScroll=False, vScroll=True, hideScroll=False, borderWidth=0, vOffset=1, hOffset=1, textureless=True, autosize=False, maxAppends=chat_utils.MAX_MESSAGE_COUNT)
            cmp = txt.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.visible = False
            cmp.position = (4, 28, 0.2)
            self.component.addChild(cmp, 'txtOut{0}'.format(tab))
            txt.onBound()
            if tab == CHAT_CONSOLE.TAB_ALL:
                cmp.visible = True

        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 320
        cmp.height = 1
        cmp.position = (3, 27, 0.8)
        self.component.addChild(cmp, 'line1')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 320
        cmp.height = 1
        cmp.position = (3, self.component.height - 60, 0.8)
        self.component.addChild(cmp, 'line2')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 320
        cmp.height = 1
        cmp.position = (3, self.component.height - 25, 0.8)
        self.component.addChild(cmp, 'line3')

    def setupTabs(self):
        for tab in xrange(5):
            btn = soButtonWFT(GUI.Window(''))
            cmp = btn.component
            cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 64
            cmp.height = 21
            cmp.position = (3 + tab * 64, self.component.height - 24, 0.4)
            btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
            btn.initVSC('soGUI/visual_styles/chatTab.xml')
            btn.onBound()
            btn.onClick = partial(self._tabHandler, tab)
            btn.setVisualState('normal')
            self.component.addChild(cmp, 'tab{0}'.format(tab))
            if tab == CHAT_CONSOLE.TAB_ALL:
                cmp.label.text = lc('GUI.ChatConsole.ALL_CHANNELS_TAB_LABEL')
                btn.buttonActive = True
            elif tab == CHAT_CONSOLE.TAB_CLAN:
                cmp.label.text = lc('GUI.ChatConsole.CLAN_CHANNEL_TAB_LABEL')
            elif tab == CHAT_CONSOLE.TAB_FRIENDS:
                cmp.label.text = lc('GUI.ChatConsole.FRIENDS_CHANNEL_TAB_LABEL')
            elif tab == CHAT_CONSOLE.TAB_PARTY:
                cmp.label.text = lc('GUI.ChatConsole.PARTY_CHANNEL_TAB_LABEL')
            elif tab == CHAT_CONSOLE.TAB_PRIVATE:
                cmp.label.text = lc('GUI.ChatConsole.PRIVATE_MESSAGES_TAB_LABEL')
            btn._updateVisualState()

    def setupSettingsWnd(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 274
        cmp.height = 238
        cmp.visible = False
        self.settingsWnd = cmp
        cmp = GUI.Frame2('soGUI/maps/Controls/chat/frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.settingsWnd.addChild(cmp, 'dFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (18, 15, 0.3)
        cmp.text = lc('GUI.ChatConsole.CHANNEL_SETTINGS_WINDOW_CAPTION')
        self.settingsWnd.addChild(cmp, 'label')
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
        cmp.position = (249, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        closeBox.onClick = partial(self._settingsHandler, 'cancel', None)
        self.settingsWnd.addChild(cmp, 'closeBox')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.ChatConsole.CHANNEL_SETTINGS_WINDOW_CONFIRM_BUTTON_LABEL')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (32, 205, 0.3)
        self.settingsWnd.addChild(cmp, 'applyBtn')
        btn.onBound()
        btn.onClick = partial(self._settingsHandler, 'apply', None)
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.ChatConsole.CHANNEL_SETTINGS_WINDOW_CANCEL_BUTTON_LABEL')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (141, 205, 0.3)
        self.settingsWnd.addChild(cmp, 'cancelBtn')
        btn.onBound()
        btn.onClick = partial(self._settingsHandler, 'cancel', None)
        btn.setVisualState('normal')
        for i in xrange(6):
            labelTxt = u''
            checkBoxName = 'CB'
            if i == 0:
                labelTxt = lc('GUI.ChatConsole.MESSAGE_TYPE_DAMAGE')
                checkBoxName = 'cb_dmg'
            elif i == 1:
                labelTxt = lc('GUI.ChatConsole.MESSAGE_TYPE_ITEMS')
                checkBoxName = 'cb_items'
            elif i == 2:
                labelTxt = lc('GUI.ChatConsole.TIMESTAMP_OPTION_LABEL')
                checkBoxName = 'cb_time'
            elif i == 3:
                labelTxt = lc('GUI.ChatConsole.MESSAGE_TYPE_SYSTEM')
                checkBoxName = 'cb_system'
            elif i == 4:
                labelTxt = lc('GUI.ChatConsole.MESSAGE_TYPE_QUESTS')
                checkBoxName = 'cb_quest'
            elif i == 5:
                labelTxt = lc('GUI.ChatConsole.MESSAGE_TYPE_NPCS')
                checkBoxName = 'cb_npc'
            cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=labelTxt, font='ruRU_Cyrvetica_Extra_14i.font', labelColour=(175, 166, 112, 255)))
            cmp = cb.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (22, 54 + i * 20, 0.4)
            self.settingsWnd.addChild(cmp, checkBoxName)
            cb.onBound()

        for i in xrange(6):
            labelTxt = u''
            checkBoxName = 'CB'
            if i == 0:
                labelTxt = lc('GUI.ChatConsole.MESSAGE_TYPE_GENERAL')
                checkBoxName = 'cb_general'
            elif i == 1:
                labelTxt = lc('GUI.ChatConsole.MESSAGE_TYPE_CLAN')
                checkBoxName = 'cb_clan'
            elif i == 2:
                labelTxt = lc('GUI.ChatConsole.MESSAGE_TYPE_PARTY')
                checkBoxName = 'cb_party'
            elif i == 3:
                labelTxt = lc('GUI.ChatConsole.MESSAGE_TYPE_PRIVATE')
                checkBoxName = 'cb_private'
            elif i == 4:
                labelTxt = lc('GUI.ChatConsole.MESSAGE_TYPE_FRIENDS')
                checkBoxName = 'cb_friends'
            elif i == 5:
                labelTxt = lc('GUI.ChatConsole.MESSAGE_TYPE_TRADE')
                checkBoxName = 'cb_trade'
            cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=labelTxt, font='ruRU_Cyrvetica_Extra_14i.font', labelColour=(175, 166, 112, 255)))
            cmp = cb.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (149, 54 + i * 20, 0.4)
            self.settingsWnd.addChild(cmp, checkBoxName)
            cb.onBound()

        return

    def mouseFocus(self, doFocus = True):
        self.component.dFrame.visible = doFocus
        self.component.settingsBtn.visible = doFocus
        self.component.line1.visible = doFocus
        self.component.line2.visible = doFocus
        for tab in xrange(5):
            cmp = getattr(self.component, 'txtOut{0}'.format(tab), None)
            if cmp:
                for name, child in cmp.vScroll.children:
                    child.visible = doFocus

        self.component.resizer.visible = doFocus
        return

    def _tabHandler(self, newTab):
        if self.currentTab == newTab:
            return
        else:
            self.currentTab = newTab
            for tab in xrange(5):
                cmp = getattr(self.component, 'tab{0}'.format(tab), None)
                if cmp:
                    cmp.script.buttonActive = False
                    cmp.script._updateVisualState()
                cmp = getattr(self.component, 'txtOut{0}'.format(tab), None)
                if cmp:
                    cmp.visible = False

            cmp = getattr(self.component, 'tab{0}'.format(newTab), None)
            if cmp:
                cmp.script.buttonActive = True
                cmp.script._updateVisualState()
            cmp = getattr(self.component, 'txtOut{0}'.format(newTab), None)
            cmp.visible = True
            self._applyCurrentTag()
            self.showSettings(False)
            return

    def _applyCurrentTag(self):
        if self.currentTab == CHAT_CONSOLE.TAB_ALL:
            self.component.edit.script.setValue(u'')
        elif self.currentTab == CHAT_CONSOLE.TAB_CLAN:
            self.component.edit.script.setValue(u'%')
        elif self.currentTab == CHAT_CONSOLE.TAB_FRIENDS:
            self.component.edit.script.setValue(u'#')
        elif self.currentTab == CHAT_CONSOLE.TAB_PARTY:
            self.component.edit.script.setValue(u'+')
        elif self.currentTab == CHAT_CONSOLE.TAB_PRIVATE:
            self.component.edit.script.setValue(u'@')

    def showSettings(self, doShow = True):
        self.settingsWnd.position.x = self.component.position.x + self.component.width
        self.settingsWnd.position.y = self.component.position.y - self.component.height - 5
        self.settingsWnd.position.z = 0.5
        cmp = getattr(self.component, 'tab{0}'.format(self.currentTab), None)
        if cmp:
            self.settingsWnd.label.text = lc('GUI.ChatConsole.CHANNEL_SETTINGS_WINDOW_CAPTION') + cmp.label.text
        self.settingsWnd.visible = doShow
        if self.settingsWnd.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.settingsWnd, 'chatSettings')
        self._setCurrentSettings()
        BWPersonality.GUICore.setBestCursor()
        if doShow:
            self.unfade()
        else:
            self.runFader()
        return

    def _setCurrentSettings(self):
        if self.tab_settings[self.currentTab][1]:
            self.settingsWnd.cb_time.script.setActive()
        else:
            self.settingsWnd.cb_time.script.setInactive()
        if CHAT_CONSOLE.MESSAGE_CLAN & self.tab_settings[self.currentTab][0] == CHAT_CONSOLE.MESSAGE_CLAN:
            self.settingsWnd.cb_clan.script.setActive()
        else:
            self.settingsWnd.cb_clan.script.setInactive()
        if CHAT_CONSOLE.MESSAGE_DAMAGE & self.tab_settings[self.currentTab][0] == CHAT_CONSOLE.MESSAGE_DAMAGE:
            self.settingsWnd.cb_dmg.script.setActive()
        else:
            self.settingsWnd.cb_dmg.script.setInactive()
        if CHAT_CONSOLE.MESSAGE_FRIENDS & self.tab_settings[self.currentTab][0] == CHAT_CONSOLE.MESSAGE_FRIENDS:
            self.settingsWnd.cb_friends.script.setActive()
        else:
            self.settingsWnd.cb_friends.script.setInactive()
        if CHAT_CONSOLE.MESSAGE_GENERAL & self.tab_settings[self.currentTab][0] == CHAT_CONSOLE.MESSAGE_GENERAL:
            self.settingsWnd.cb_general.script.setActive()
        else:
            self.settingsWnd.cb_general.script.setInactive()
        if CHAT_CONSOLE.MESSAGE_ITEMS & self.tab_settings[self.currentTab][0] == CHAT_CONSOLE.MESSAGE_ITEMS:
            self.settingsWnd.cb_items.script.setActive()
        else:
            self.settingsWnd.cb_items.script.setInactive()
        if CHAT_CONSOLE.MESSAGE_NPC & self.tab_settings[self.currentTab][0] == CHAT_CONSOLE.MESSAGE_NPC:
            self.settingsWnd.cb_npc.script.setActive()
        else:
            self.settingsWnd.cb_npc.script.setInactive()
        if CHAT_CONSOLE.MESSAGE_PARTY & self.tab_settings[self.currentTab][0] == CHAT_CONSOLE.MESSAGE_PARTY:
            self.settingsWnd.cb_party.script.setActive()
        else:
            self.settingsWnd.cb_party.script.setInactive()
        if CHAT_CONSOLE.MESSAGE_PRIVATE & self.tab_settings[self.currentTab][0] == CHAT_CONSOLE.MESSAGE_PRIVATE:
            self.settingsWnd.cb_private.script.setActive()
        else:
            self.settingsWnd.cb_private.script.setInactive()
        if CHAT_CONSOLE.MESSAGE_QUEST & self.tab_settings[self.currentTab][0] == CHAT_CONSOLE.MESSAGE_QUEST:
            self.settingsWnd.cb_quest.script.setActive()
        else:
            self.settingsWnd.cb_quest.script.setInactive()
        if CHAT_CONSOLE.MESSAGE_SYSTEM & self.tab_settings[self.currentTab][0] == CHAT_CONSOLE.MESSAGE_SYSTEM:
            self.settingsWnd.cb_system.script.setActive()
        else:
            self.settingsWnd.cb_system.script.setInactive()
        if CHAT_CONSOLE.MESSAGE_TRADE & self.tab_settings[self.currentTab][0] == CHAT_CONSOLE.MESSAGE_TRADE:
            self.settingsWnd.cb_trade.script.setActive()
        else:
            self.settingsWnd.cb_trade.script.setInactive()
        self.settingsWnd.cb_clan.script.enable()
        self.settingsWnd.cb_friends.script.enable()
        self.settingsWnd.cb_party.script.enable()
        self.settingsWnd.cb_private.script.enable()
        if self.currentTab == CHAT_CONSOLE.TAB_CLAN:
            self.settingsWnd.cb_clan.script.disable()
        elif self.currentTab == CHAT_CONSOLE.TAB_FRIENDS:
            self.settingsWnd.cb_friends.script.disable()
        elif self.currentTab == CHAT_CONSOLE.TAB_PARTY:
            self.settingsWnd.cb_party.script.disable()
        elif self.currentTab == CHAT_CONSOLE.TAB_PRIVATE:
            self.settingsWnd.cb_private.script.disable()

    def _getCurrentSettings(self):
        retVal = []
        retVal.append(self.currentTab)
        msk = 0
        if self.settingsWnd.cb_clan.script.isChecked():
            msk |= CHAT_CONSOLE.MESSAGE_CLAN
        if self.settingsWnd.cb_dmg.script.isChecked():
            msk |= CHAT_CONSOLE.MESSAGE_DAMAGE
        if self.settingsWnd.cb_friends.script.isChecked():
            msk |= CHAT_CONSOLE.MESSAGE_FRIENDS
        if self.settingsWnd.cb_general.script.isChecked():
            msk |= CHAT_CONSOLE.MESSAGE_GENERAL
        if self.settingsWnd.cb_items.script.isChecked():
            msk |= CHAT_CONSOLE.MESSAGE_ITEMS
        if self.settingsWnd.cb_npc.script.isChecked():
            msk |= CHAT_CONSOLE.MESSAGE_NPC
        if self.settingsWnd.cb_party.script.isChecked():
            msk |= CHAT_CONSOLE.MESSAGE_PARTY
        if self.settingsWnd.cb_private.script.isChecked():
            msk |= CHAT_CONSOLE.MESSAGE_PRIVATE
        if self.settingsWnd.cb_quest.script.isChecked():
            msk |= CHAT_CONSOLE.MESSAGE_QUEST
        if self.settingsWnd.cb_system.script.isChecked():
            msk |= CHAT_CONSOLE.MESSAGE_SYSTEM
        if self.settingsWnd.cb_trade.script.isChecked():
            msk |= CHAT_CONSOLE.MESSAGE_TRADE
        retVal.append(msk)
        retVal.append(self.settingsWnd.cb_time.script.isChecked())
        return retVal

    def toggleConsoleInput(self):
        cmp = getattr(self.component, 'edit', None)
        if cmp:
            if not cmp.script._isActive():
                cmp.script.activate(True)
        return

    def applyConfig(self, data):
        if data.has_key(CHAT_CONSOLE.TAB_ALL):
            self.tab_settings[CHAT_CONSOLE.TAB_ALL] = data[CHAT_CONSOLE.TAB_ALL]
        if data.has_key(CHAT_CONSOLE.TAB_CLAN):
            self.tab_settings[CHAT_CONSOLE.TAB_CLAN] = data[CHAT_CONSOLE.TAB_CLAN]
        if data.has_key(CHAT_CONSOLE.TAB_FRIENDS):
            self.tab_settings[CHAT_CONSOLE.TAB_FRIENDS] = data[CHAT_CONSOLE.TAB_FRIENDS]
        if data.has_key(CHAT_CONSOLE.TAB_PARTY):
            self.tab_settings[CHAT_CONSOLE.TAB_PARTY] = data[CHAT_CONSOLE.TAB_PARTY]
        if data.has_key(CHAT_CONSOLE.TAB_PRIVATE):
            self.tab_settings[CHAT_CONSOLE.TAB_PRIVATE] = data[CHAT_CONSOLE.TAB_PRIVATE]
        if data.has_key('validator'):
            self.component.edit.script.setValidator(data['validator'])

    def addMessage(self, mask, msg, timeStamp):
        beginName = msg.find('=') + 1
        endName = msg.find(';')
        Name = msg[beginName:endName]
        if beginName > 0:
            if BWPersonality.GUICore.friendList.isBlackList(Name.encode('utf-8')) == 0:
                self.WriteToChat(mask, msg, timeStamp)
            else:
                print 'message from ', Name.encode('utf-8'), ' is locked'
        else:
            self.WriteToChat(mask, msg, timeStamp)

    def WriteToChat(self, mask, msg, timeStamp):
        for tab in xrange(5):
            cmp = getattr(self.component, 'txtOut{0}'.format(tab), None)
            if cmp:
                if mask & self.tab_settings[tab][0] == mask:
                    before_scrollCursor = cmp.script.scrollCursor[1]
                    try:
                        before_val_nMap = cmp.script.nMap[before_scrollCursor]
                    except IndexError as e:
                        before_val_nMap = None

                    if not self.tab_settings[tab][1]:
                        cmp.script.addText(msg, True)
                    elif timeStamp:
                        cmp.script.addText(timeStamp + u':' + msg, True)
                    else:
                        cmp.script.addText(msg, True)
                    scrollCursor = cmp.script.scrollCursor[1]
                    maxScroll = cmp.script.getMaxScroll()[1]
                    if not self.component.stop_scroll.script.isChecked():
                        cmp.script.scrollTo([0, maxScroll])
                    else:
                        newScroll = 0
                        try:
                            newScroll = cmp.script.nMap.index(before_val_nMap)
                        except ValueError:
                            pass

                        cmp.script.scrollTo([0, newScroll])
                    self.unfade()
                    self.runFader()

        return

    def clearConsole(self):
        for tab in xrange(5):
            cmp = getattr(self.component, 'txtOut{0}'.format(tab), None)
            if cmp:
                cmp.script.setText(u'')

        return

    def _settingsHandler(self, event, data):
        if event == 'cancel':
            self.showSettings(False)
        if event == 'apply':
            BWPersonality.GUICore.chatEvent(CHAT_CONSOLE.EVENT_SETTINGS, self._getCurrentSettings())

    def setPromt(self, promt, replaceTag = False, eraseOld = False, activating = False):
        self.unfade()
        self.runFader()
        if activating:
            self.component.edit.script.activate()
        if eraseOld:
            self.component.edit.script.clear()
        else:
            oldTxt = self.component.edit.script.getRaw()
            self.component.edit.script.setValue(oldTxt + promt)
            return
        if replaceTag:
            self.component.edit.script.setValue(promt)
        else:
            tag = u''
            if self.currentTab == CHAT_CONSOLE.TAB_CLAN:
                tag = u'%'
            elif self.currentTab == CHAT_CONSOLE.TAB_FRIENDS:
                tag = u'#'
            elif self.currentTab == CHAT_CONSOLE.TAB_PARTY:
                tag = u'+'
            elif self.currentTab == CHAT_CONSOLE.TAB_PRIVATE:
                tag = u'@'
            self.component.edit.script.setValue(tag + promt)

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'chatConsole')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        self.component.edit.script.activate(False)

    def runFader(self):
        if self.fader is not None:
            self.fader.stop()
            self.fader = None
        self.fader = self.consoleFader()
        self.fader.run()
        return

    def unfade(self):
        if self.fader is not None:
            self.fader.stop()
            self.fader = None
        self.component.fader.alpha = 1.0
        self.component.fader.reset()
        return

    def handleMouseEnterEvent(self, component):
        soResizeComponent.handleMouseEnterEvent(self, component)
        return True

    def handleMouseLeaveEvent(self, component):
        soResizeComponent.handleMouseLeaveEvent(self, component)
        return True

    def handleMouseEvent(self, cmp, event):
        cmp = getattr(self.component, 'txtOut{0}'.format(self.currentTab), None)
        if event.dz:
            if event.dz < 0:
                cmp.script.scrollHandler('DOWN', None)
            else:
                cmp.script.scrollHandler('UP', None)
        return True

    def scrollPage(self, up = True):
        cmp = getattr(self.component, 'txtOut{0}'.format(self.currentTab), None)
        if not cmp:
            raise ValueError, self.currentTab
        countmsg = len(cmp.script.nMap)
        maxScroll = cmp.script.getMaxScroll()[1]
        size_lines = countmsg - maxScroll
        if up:
            size_lines *= -1
        scrollCursor = cmp.script.scrollCursor[1]
        new_Scroll = scrollCursor + size_lines
        new_Scroll = max(0, new_Scroll)
        new_Scroll = min(maxScroll, new_Scroll)
        cmp.script.scrollTo([0, new_Scroll])
        return

    def handleDragStartEvent(self, cmp):
        handled = soResizeComponent.handleDragStartEvent(self, cmp)
        return handled

    def handleDragStopEvent(self, cmp):
        handled = soResizeComponent.handleDragStopEvent(self, cmp)
        return handled

    def onResizeStart(self):
        self.newSize = [self.component.width, self.component.height]

    def onResizeFinish(self):
        self.newHeight(self.newSize[1])
        self.newSize = None
        return

    def onResizing(self, pos):
        sW, sH = BigWorld.screenSize()
        maxHeight = sH - BWPersonality.GUICore.healthBarGUI.component.height - BWPersonality.GUICore.healthBarGUI.component.position.y
        startX = -1.0 + 2.0 / (sW / self.component.position.x)
        startY = pos.y
        width = 2.0 / (sW / self.component.width)
        height = abs(pos.y - (1.0 - 2.0 / (sH / self.component.position.y)))
        pHeight = sH / (2.0 / abs(pos.y - (pos.y - height)))
        if pHeight < self.minHeight:
            pHeight = self.minHeight
            height = pHeight * (2.0 / sH)
            startY = -1.0 + 2.0 / (sH / self.minHeight)
        elif pHeight > maxHeight:
            pHeight = maxHeight
            height = pHeight * (2.0 / sH)
            startY = -1.0 + 2.0 / (sH / maxHeight)
        self.newSize[1] = pHeight
        self.drawResizeBox([startX, startY], [width, height])

    def newHeight(self, h):
        self.component.height = h
        for tab in xrange(5):
            cmp = getattr(self.component, 'txtOut{0}'.format(tab), None)
            if cmp:
                cmp.script.setSize(318, h - 89)
            cmp = getattr(self.component, 'tab{0}'.format(tab), None)
            cmp.position.y = h - 24

        self.component.edit.position.y = h - 57
        self.component.line2.position.y = h - 60
        self.component.line3.position.y = h - 25
        self.component.enterBtn.position.y = h - 57
        return

    def sendInput(self):
        msg = self.component.edit.script.getRaw()
        if len(msg) > 128:
            return
        BWPersonality.GUICore.chatEvent(CHAT_CONSOLE.EVENT_SEND, msg)
        self.component.edit.script.clear()
        self._applyCurrentTag()

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        cmp = self.component
        cmp.position = (1, sH - 1, 0.0)

    def repeatInput(self, dir):
        BWPersonality.GUICore.chatEvent(CHAT_CONSOLE.EVENT_REPEAT, dir)

    @PyGUIEvent('edit', 'onActive')
    def onEditActive(self, active):
        if not active:
            self.component.edit.script.clear()
            self._applyCurrentTag()
            self.typing = False
            self.runFader()
            self.mouseFocus(False)
            self.component.closeChat.visible = 0
            self.component.stop_scroll.visible = 0
        else:
            self.typing = True
            self.unfade()
            self.mouseFocus(True)
            self.component.stop_scroll.visible = 1
            self.component.closeChat.visible = 1
        BWPersonality.GUICore.setBestCursor()

    @PyGUIEvent('settingsBtn', 'onClick')
    def onSettingsBtn(self):
        self.showSettings(True)

    @PyGUIEvent('enterBtn', 'onClick')
    def onSendBtn(self):
        self.sendInput()
        self.component.edit.script.activate(False)

    @PyGUIEvent('edit', 'onDefaultAction')
    def onEditDA(self):
        self.sendInput()

    @PyGUIEvent('edit', 'onEscape')
    def onEscape(self):
        self.component.edit.script.activate(False)

    @PyGUIEvent('edit', 'onPgUp')
    def onPgUp(self):
        self.scrollPage(True)

    @PyGUIEvent('edit', 'onPgDn')
    def onPgDn(self):
        self.scrollPage(False)

    @PyGUIEvent('closeChat', 'onClick')
    def _handleClose(self, *w):
        self.component.edit.script.activate(False)

    @BWMemberCoroutine
    def consoleFader(self):
        if self.typing:
            return
        else:
            yield BWWaitForPeriod(self.fadeDelay)
            self.component.fader.speed = self.fadeSpeed
            self.component.fader.alpha = 0.0
            self.fader = None
            return