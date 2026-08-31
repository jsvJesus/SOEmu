# Embedded file name: scripts/client/soGUI/soChatConsole.py
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

class soChatConsole(PyGUI.Window, BWKeyBindings.BWActionHandler):
    factoryString = 'soGUI.soChatConsole'
    numLines = 9
    editing = False
    autoHideTimeout = 18
    hidden = True
    hideTimer = autoHideTimeout

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        component.script = self
        self.backImage = None
        self.outPutLines = []
        self.multiPurposeLine = None
        self.maxWidth = 0.74
        self.strings = []
        for i in range(self.numLines):
            self.strings.append('')

        self.editField = None
        self.setupEdit()
        self.setupOutputFrame()
        self.messageCallBack = None
        BWPersonality.gpd.keyBindings.addHandler(self)
        BWKeyBindings.BWActionHandler.setupActionList(self)
        self.setAlphaShader()
        self.beginHide().run()
        return

    def setAlphaShader(self):
        if self.autoHideTimeout > 0:
            aShade = GUI.AlphaShader()
            aShade.mode = 'ALL'
            aShade.speed = 10
            aShade.value = 0
            self.component.addShader(aShade, 'fader')

    @BWMemberCoroutine
    def beginHide(self):
        self.hidden = True
        while self.hideTimer and self.hidden:
            yield BWWaitForPeriod(1.0)
            self.hideTimer -= 1
        else:
            if self.hidden:
                self.component.fader.value = 0

    def unHide(self):
        self.hideTimer = self.autoHideTimeout
        self.component.fader.reset()
        self.component.fader.value = 255
        self.hidden = False

    def refreshHide(self):
        self.hideTimer = self.autoHideTimeout

    def setupEdit(self):
        self.editField = soEditField(GUI.Window(''))
        self.editField.component.position = (-1.0, -1.0, 0.0)
        self.editField.component.verticalAnchor = 'BOTTOM'
        self.editField.component.horizontalAnchor = 'LEFT'
        self.editField.component.horizontalPositionMode = 'CLIP'
        self.editField.component.verticalPositionMode = 'CLIP'
        self.editField.component.widthMode = 'PIXEL'
        self.editField.component.heightMode = 'PIXEL'
        self.editField.component.width = 400
        self.editField.component.height = 30
        self.editField.component.edit.font = 'ruRU_calibri_default.font'
        self.editField.CHARS_TO_IGNORE = [u'\r',
         u'\x08',
         u'\x1b',
         u'\t']
        self.component.addChild(self.editField.component, 'edit')
        self.editField.component.focus = False
        self.editField.maxLength = 200

    def setupOutputFrame(self):
        outFrame = GUI.Frame2('soGUI/maps/con_frame.tga')
        outFrame.horizontalPositionMode = outFrame.verticalPositionMode = 'CLIP'
        outFrame.widthMode = outFrame.heightMode = 'CLIP'
        outFrame.horizontalAnchor = 'CENTER'
        outFrame.verticalAnchor = 'CENTER'
        outFrame.colour = (255, 255, 255, 255)
        outFrame.materialFX = 'BLEND'
        outFrame.width = 2.0
        outFrame.height = 2.0
        outFrame.position = (0.0, 0.0, 0.5)
        self.component.addChild(outFrame, 'outFrame')

    def onBound(self):
        PyGUI.Window.onBound(self)
        self.multiPurposeLine = GUI.Text(u'')
        self.multiPurposeLine.visible = False
        self.multiPurposeLine.font = 'ruRU_calibri_default.font'
        for i in range(self.numLines):
            line = GUI.Text('')
            line.position = (-0.95, 0.95, 0.0)
            line.verticalAnchor = 'TOP'
            line.horizontalAnchor = 'LEFT'
            line.horizontalPositionMode = 'CLIP'
            line.verticalPositionMode = 'CLIP'
            line.widthMode = 'PIXEL'
            line.heightMode = 'PIXEL'
            line.font = 'ruRU_calibri_default.font'
            line.colour = (155, 157, 71, 255)
            line.position[1] -= i / 5.5
            self.outPutLines.append(line)
            self.component.addChild(self.outPutLines[i], 'line' + str(i + 1))

        self.updateOutput()

    def updateOutput(self):
        for i in range(self.numLines):
            self.outPutLines[i].text = self.strings[i]

    def addMessage(self, msg, color = 4294967295L):
        tokens = msg.split()
        numTokens = len(tokens)
        self.multiPurposeLine.text = u''
        formatedMsg = []
        line = ''
        for i in range(numTokens):
            self.multiPurposeLine.text += tokens[i] + u' '
            if self.multiPurposeLine.width >= self.maxWidth:
                formatedMsg.append(line)
                self.multiPurposeLine.text = tokens[i] + u' '
                line = tokens[i] + u' '
            else:
                line = self.multiPurposeLine.text

        if line != '':
            formatedMsg.append(line)

        def shiftUp():
            del self.strings[0]
            self.strings.append('')

        def allocateMsg():
            targetString = self.numLines - 1
            for i in range(len(self.strings)):
                if self.strings[i] == '':
                    targetString = i
                    break

            needToFree = 0
            if len(formatedMsg) > len(self.strings) - (targetString + 1):
                needToFree = len(formatedMsg)
            if needToFree > 0:
                for i in range(needToFree):
                    shiftUp()
                    targetString -= 1

            for i in range(len(formatedMsg)):
                self.strings[i + targetString] = formatedMsg[i]

        self.unHide()
        self.beginHide().run()
        allocateMsg()
        self.updateOutput()

    def cancelInput(self):
        self.editField.component.focus = False
        self.editField.empty(True)
        self.editing = False
        self.beginHide().run()

    def setInputCallBack(self, callback):
        if hasattr(callback, '__call__'):
            self.messageCallBack = callback

    def toggleConsoleInput(self, isDown = True):
        if isDown:
            if self.editing:
                self.editing = False
                self.editField.component.focus = False
                if self.messageCallBack is not None and self.editField.value():
                    self.messageCallBack(self.editField.value())
                self.editField.empty(True)
                self.beginHide().run()
            else:
                self.editing = True
                self.editField.component.focus = True
                self.unHide()
        return

    @PyGUIEvent('edit', 'onInputEnded')
    def onInputEnd(self):
        self.toggleConsoleInput(True)


class soChatConsoleVisualState(VisualState):

    def __init__(self):
        VisualState.__init__(self)
        self.textStyle = ''
        self.frameTextureName = ''
        self.frameColour = (255, 255, 255, 255)

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
        self.textStyle = dataSection.readString('textStyle', '')
        if dataSection.has_key('frame'):
            frameSection = dataSection._frame
            self.frameMaterialFX = frameSection.readString('materialFX', '')
            self.frameTextureName = frameSection.readString('textureName', '')
            self.frameColour = frameSection.readVector4('colour', (255, 255, 255, 255))

    def apply(self, componentScript):
        VisualState.apply(self, componentScript)
        if hasattr(componentScript, 'frameComponent'):
            componentScript.frameComponent.texture = None
            componentScript.frameComponent.textureName = self.frameTextureName
            componentScript.frameComponent.colour = self.frameColour
            if self.frameMaterialFX != '':
                componentScript.frameComponent.materialFX = self.frameMaterialFX
            else:
                componentScript.frameComponent.materialFX = 'BLEND'
        return


class soChatConsole2(PyGUIBase, soVisualStateComponent):
    factoryString = 'soGUI.soChatConsole2'
    visualStateString = 'soGUI.soChatConsoleVisualState'
    autoHideTimeout = 18
    hideTimer = autoHideTimeout
    hidden = True
    EVENT_SEND = 0
    COLOUR_SYSTEM = (0, 235, 235, 255)
    COLOUR_RECIEVED_DAMAGE = (255, 45, 45, 255)
    COLOUR_INFLICTED_DAMAGE = (100, 245, 100, 255)
    COLOUR_MESSAGE = (255, 255, 255, 255)
    COLOUR_PRIVATE_MESSAGE = (215, 0, 193, 255)
    COLOUR_CLAN_MESSAGE = (6, 192, 1, 255)
    COLOUR_GROUP_MESSAGE = (66, 66, 255, 255)

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        soVisualStateComponent.__init__(self, component, self.visualStateString)
        component.script = self
        self.frameComponent = None
        self.active = False
        self.pressed = False
        self.hovering = False
        self.disabled = False
        self.setupRoot()
        self.setupFrame()
        self.setupTxt()
        self.setupInput()
        self.setupTabs()
        self.setupAlphaShader()
        self.initVSC('soGUI/visual_styles/defaultChatConsole.xml')
        self.setVisualState('normal')
        self.beginHide().run()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.width = 350
        cmp.height = 300
        cmp.position = (-1.0, -1.0, 1.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (-1.0, 1.0, 0.0)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.crossFocus = True
        cmp.script = self
        self.component.addChild(cmp, 'mouseCapture')

    def setupFrame(self):
        cmp = GUI.Frame2('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.width = 350
        cmp.height = 270
        cmp.position = (-1.0, -1.0, 1.0)
        self.component.addChild(cmp)
        self.frameComponent = cmp

    def setupAlphaShader(self):
        if self.autoHideTimeout > 0:
            aShade = GUI.AlphaShader()
            aShade.mode = 'ALL'
            aShade.speed = 10
            aShade.value = 0
            self.component.addShader(aShade, 'fader')

    def setupTabs(self):
        pass

    def setupTxt(self):
        txt = soTextField2(GUI.Window(), soTxtFieldPropsStructure(width=350, height=250, textureless=True, autoScroll=True, hideScroll=True))
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (0, 30, 0.5)
        self.component.addChild(cmp, 'textFld')
        txt.onBound()

    def setupInput(self):
        edit = soEditField2(GUI.Window(), width=350, height=25, font='ruRU_calibri_small.font')
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.position = (-1.0, -1.0, 0.1)
        self.component.addChild(cmp, 'edit')

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'chatConsole')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False

    def toggleConsoleInput(self):
        self.active = not self.active
        if self.active:
            self.component.edit.script.setActive()
            self.unHide()
        else:
            self.component.edit.script.setActive(False)
            self.beginHide().run()

    def update(self):
        self.unHide()
        self.component.textFld.script.addText(BWPersonality.GUICore.chatConsoleDataSection)
        BWPersonality.GUICore.chatConsoleDataSection = None
        self.beginHide().run()
        return

    def handleMouseEnterEvent(self, component):
        self.unHide()
        return True

    def handleMouseLeaveEvent(self, component):
        self.beginHide().run()
        return True

    @BWMemberCoroutine
    def beginHide(self):
        self.hidden = True
        while self.hideTimer and self.hidden:
            yield BWWaitForPeriod(1.0)
            self.hideTimer -= 1
        else:
            if self.hidden:
                self.component.fader.value = 0

    def unHide(self):
        self.hideTimer = self.autoHideTimeout
        self.component.fader.reset()
        self.component.fader.value = 255
        self.hidden = False

    def refreshHide(self):
        self.hideTimer = self.autoHideTimeout

    @PyGUIEvent('edit', 'eventReturn')
    def onMessageEntered(self):
        msg = self.component.edit.script.getValue()
        if len(msg) > 0:
            BWPersonality.GUICore.chatEvent(self.EVENT_SEND, msg)
        self.active = False
        self.component.edit.script.clear()

    @PyGUIEvent('edit', 'eventLostFocus')
    def onFocusLost(self):
        self.beginHide().run()
        self.active = False

    @PyGUIEvent('edit', 'eventEscape')
    def onEscape(self):
        self.beginHide().run()
        self.active = False
        self.component.edit.script.clear()