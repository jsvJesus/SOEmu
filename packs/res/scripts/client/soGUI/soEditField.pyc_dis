# Embedded file name: scripts/client/soGUI/soEditField.py
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import BWPersonality
from Helpers.BWKeyBindings import BWKeyBindingAction
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
from soGUI.soVisualStateComponent import soVisualStateComponent
from Helpers.PyGUI import Utils
import soGUI
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI import PyGUIBase
from Helpers.BWCoroutine import *
from math import ceil, floor
from Keys import *
import re

class soEditFieldVisualState(VisualState):

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
        self.textStyle = dataSection.readString('textStyle', '')
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
            componentScript.buttonIcon.textureName = self.iconTextureName


class soEditField(PyGUI.EditField, soVisualStateComponent):
    factoryString = 'soGUI.soEditField'
    visualStateString = 'soGUI.soEditFieldVisualState'
    CURSOR_CHAR = '|'
    MASK_CHAR = None
    CHARS_TO_IGNORE = [u'\r',
     u'\x08',
     u'\x1b',
     u'\t',
     u' ']
    editString = ''

    def __init__(self, component):
        PyGUI.EditField.__init__(self, component)
        soVisualStateComponent.__init__(self, component, self.visualStateString)
        component.script = self
        self.mouseCapture = None
        self.maxWidth = 380
        self.editComponent = GUI.Text('')
        self.setupFrame()
        self.buttonIcon = self.component.editFrame
        self.editComponent.font = 'ruRU_calibri_default.font'
        self.editComponent.verticalPositionMode = 'CLIP'
        self.editComponent.horizontalPositionMode = 'CLIP'
        self.editComponent.verticalAnchor = 'CENTER'
        self.editComponent.horizontalAnchor = 'LEFT'
        self.editComponent.position = (-1.0 + soGUI.getPixelWidth(self.component) * 4, 0.0, 0.0)
        self.component.addChild(self.editComponent, 'edit')
        self.initVSC('scripts/client/soGUI/schemas/soEditField_default.xml')
        self.setVisualState('passive')
        self.setupMouseCapture()
        return

    def setupFrame(self):
        editFrame = GUI.Frame2('')
        editFrame.horizontalPositionMode = editFrame.verticalPositionMode = 'CLIP'
        editFrame.widthMode = editFrame.heightMode = 'CLIP'
        editFrame.horizontalAnchor = 'CENTER'
        editFrame.verticalAnchor = 'CENTER'
        editFrame.colour = (255, 255, 255, 255)
        editFrame.materialFX = 'BLEND'
        editFrame.width = 2.0
        editFrame.height = 2.0
        editFrame.position = (0.0, 0.0, 0.5)
        self.component.addChild(editFrame, 'editFrame')

    def setupMouseCapture(self):
        self.mouseCapture = PyGUI.Window(GUI.Window())
        cmp = self.mouseCapture.component
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.focus = True
        cmp.mouseButtonFocus = True
        cmp.position = (0.0, 0.0, 0.0)
        self.mouseCapture.handleMouseClickEvent = self.handleMouseClickEvent
        self.mouseCapture.onBound()
        self.component.addChild(self.mouseCapture.component, 'mouseCapture')

    def onBound(self):
        PyGUI.EditField.onBound(self)

    def handleMouseClickEvent(self, component):
        self.component.focus = True
        return True

    def empty(self, doEmpty = False):
        if doEmpty:
            self.component.edit.text = ''
            self.editString = ''

    def handleCharEvent(self, character, key, mods):
        c = self.component.edit
        if character == u'\x08':
            c.text = c.text[0:len(c.text) - 2] + self.CURSOR_CHAR
            self.editString = self.editString[0:len(self.editString) - 2] + self.CURSOR_CHAR
            if c.text == '|':
                c.text = self.editString[-10:]
            return True
        if character not in self.CHARS_TO_IGNORE:
            if len(self.editString[0:len(self.editString) - 1]) < self.maxLength:
                self.editString = self.editString[0:len(self.editString) - 1] + character + self.CURSOR_CHAR
                if c.stringDimensions(self.editString)[0] > self.maxWidth:
                    c.text = self.editString[len(self.editString) - len(c.text):len(self.editString)]
                else:
                    c.text = c.text[0:len(c.text) - 1] + character + self.CURSOR_CHAR
            return True
        return False

    def handleKeyEvent(self, event):
        key = event.key
        mods = event.modifiers
        down = event.isKeyDown()
        char = event.character
        if key in (KEY_RETURN, KEY_NUMPADENTER) and down:
            self.component.focus = False
            self.onInputEnded()
            return True
        else:
            if down:
                if char is not None:
                    res = self.handleCharEvent(char, key, mods)
                    if res:
                        print 'sinking key', key, char
                        BigWorld.sinkKeyEvents(key)
                    return res
            else:
                return True
            return

    def onInputEnded(self):
        return None

    def value(self, newVal = None):
        if newVal is None:
            return self.editString[0:len(self.editString) - 1]
        else:
            self.component.edit.text = str(newVal)
            self.editString = str(newVal)
            return

    def focus(self, state):
        c = self.component.edit
        if state:
            self.setVisualState('active')
            c.colour = self.colour
            c.text = c.text + self.CURSOR_CHAR
        else:
            c.colour = (155, 155, 155, 255)
            c.text = c.text[0:len(c.text) - 1]
            self.setVisualState('passive')


class soEditFieldVisualState2(VisualState):

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


class soEditField2(PyGUI.PyGUIBase, soVisualStateComponent):
    factoryString = 'soGUI.soEditField2'
    visualStateString = 'soGUI.soEditFieldVisualState2'
    CHAR_BACKSPACE = '\x08'
    CHAR_RETURN = '\r'
    DEFAULT_CURSOR_WIDTH = 10
    CHARS_TO_IGNORE = [u'\r',
     u'\x08',
     u'\x1b',
     u'\t']

    def __init__(self, component, width = 150, height = 26, borderWidth = 2, font = 'ruRU_calibri_default.font', maxChars = 256, isNumerical = False, visualStyle = 'defaultEditField', maskChar = ''):
        PyGUI.PyGUIBase.__init__(self, component)
        soVisualStateComponent.__init__(self, component, self.visualStateString)
        component.script = self
        self.disabled = False
        self.hovering = False
        self.pressed = False
        self.active = False
        self.frameComponent = None
        self.cursorComponent = None
        self.maxCharacters = maxChars
        self.isNumerical = isNumerical
        self.cursorPosition = 0
        self.firstCharPosition = 0
        self.cmpWidth = width
        self.cmpHeight = height
        self.editFont = font
        self.borderWidth = borderWidth
        self.maskChar = maskChar
        self.onActivated = lambda : None
        self.trueText = ''
        self.visualText = ''
        self.setupRoot()
        self.setupFrame()
        self.setupText()
        self.setupCursor()
        self.initVSC('soGUI/visual_styles/' + visualStyle + '.xml')
        self.updateVisualState()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.cmpWidth
        cmp.height = self.cmpHeight
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.crossFocus = True
        cmp.moveFocus = True
        cmp.mouseButtonFocus = True

    def setupFrame(self):
        cmp = GUI.Frame2('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (0, 0, 0.5)
        cmp.width = self.cmpWidth
        cmp.height = self.cmpHeight
        self.component.addChild(cmp, 'frameCmp')
        self.frameComponent = self.component.frameCmp

    def setupText(self):
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.position = (self.borderWidth + 4, self.cmpHeight / 2.0, 0.4)
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.font = self.editFont
        self.component.addChild(cmp, 'textCmp')

    def setupCursor(self):
        cmp = GUI.Simple('soGUI/maps/Colours/darkGreen.bmp')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalAnchor = 'LEFT'
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.tiled = True
        cmp.width = self.DEFAULT_CURSOR_WIDTH
        cmp.height = 2
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        w, h = self.component.textCmp.stringDimensions('A')
        y = self.component.textCmp.position.y
        cmp.position = (self.borderWidth + 4, y + h / 2.0 - 4, 0.1)
        self.component.addChild(cmp, 'cursorCmp')
        self.cursorComponent = self.component.cursorCmp

    def updateVisualState(self):
        visualState = 'normal'
        if self.disabled:
            visualState = 'disabled' if not self.active else 'disabled_active'
        elif self.pressed and self.hovering:
            visualStatee = 'pressed' if not self.active else 'pressed_active'
        elif self.hovering:
            visualState = 'hover' if not self.active else 'hover_active'
        else:
            visualState = 'normal' if not self.active else 'active'
        self.setVisualState(visualState)

    def setActive(self, active = True):
        if active:
            BWPersonality.GUICore.registerCharacterReciever(self.component)
        else:
            BWPersonality.GUICore.unregisterCharacterReciever(self.component)

    def isEditActive(self):
        return self.active

    def onClick(self):
        self.eventClick()
        if not self.active:
            BWPersonality.GUICore.registerCharacterReciever(self.component)

    def onReturn(self):
        self.eventReturn()
        BWPersonality.GUICore.unregisterCharacterReciever(self.component)

    def handleKeyEvent(self, event):
        key = event.key
        char = event.character
        mods = event.modifiers
        down = event.isKeyDown()
        if event.isMouseButton():
            return False
        elif key == KEY_ESCAPE:
            self.setActive(False)
            self.eventEscape()
            return True
        elif key == KEY_LCONTROL:
            return False
        else:
            if key == KEY_RETURN or key == KEY_NUMPADENTER:
                if down:
                    if MODIFIER_ALT & mods == MODIFIER_ALT:
                        return False
                    else:
                        self.onReturn()
                        return True
            if char is not None:
                if down:
                    handled = self.handleChar(char)
                    if handled:
                        return True
                if not down:
                    return True
            elif self.active:
                return True
            return False

    def handleMouseEvent(self, comp, event):
        return True

    def handleMouseEnterEvent(self, comp):
        self.hovering = True
        self.updateVisualState()
        return True

    def handleMouseLeaveEvent(self, comp):
        self.hovering = False
        self.updateVisualState()
        return True

    def handleMouseButtonEvent(self, comp, event):
        if not event.isMouseButton():
            return False
        down = event.isKeyDown()
        key = event.key
        position = event.cursorPosition
        if key == KEY_LEFTMOUSE:
            if down:
                self.pressed = True
            elif self.pressed:
                self.pressed = False
                self.onClick()
            self.updateVisualState()
            return True
        return False

    def getCharacterFeed(self):
        self.onActivated()
        self.active = True
        self.updateVisualState()
        self.renderCursor()

    def lostCharacterFeed(self):
        self.active = False
        self.updateVisualState()
        self.renderCursor()
        self.eventLostFocus()

    def handleChar(self, char):
        if char == self.CHAR_BACKSPACE:
            self.trueText = self.trueText[:-1]
            self.visualText = self.visualText[:-1]
            self.cursorPosition -= 1
            if self.cursorPosition < 0:
                self.cursorPosition = 0
        elif char not in self.CHARS_TO_IGNORE:
            if self.isNumerical:
                if not char.isdigit():
                    return True
            self.trueText += char
            if self.maskChar != '':
                self.visualText += self.maskChar
            else:
                self.visualText += char
            self.cursorPosition += 1
        else:
            return False
        self.renderText()
        self.renderCursor()
        return True

    def renderText(self):
        visualString = ''
        maxPixels = self.cmpWidth - self.borderWidth * 2 - 4 - self.component.cursorCmp.width
        stringWidth = self.component.textCmp.stringWidth(self.visualText)
        if stringWidth > maxPixels:
            for i in xrange(len(self.trueText)):
                if self.component.textCmp.stringWidth(self.visualText[i:]) <= maxPixels:
                    visualString = self.visualText[i:]
                    self.firstCharPosition = i
                    break

        else:
            self.firstCharPosition = 0
            visualString = self.visualText
        self.component.textCmp.text = visualString

    def renderCursor(self):
        w, h = self.component.textCmp.stringDimensions(self.visualText[self.firstCharPosition:self.cursorPosition])
        curPos = self.borderWidth + 4 + w
        self.cursorComponent.position.x = curPos
        if not self.active:
            self.cursorComponent.visible = False
        else:
            self.cursorComponent.visible = True

    def setWidth(self, newWidth):
        self.cmpWidth = newWidth
        self.component.width = newWidth
        self.component.frameCmp.width = newWidth

    def setHeight(self, newHeight):
        self.cmpHeight = newHeight
        self.component.height = newHeight
        self.component.frameCmp.height = newHeight

    def getValue(self):
        return self.trueText

    def setValue(self, txt):
        self.trueText = txt
        if self.maskChar == '':
            self.visualText = txt
        else:
            self.visualText = ''
            for letter in self.trueText:
                self.visualText += self.maskChar

        self.renderText()
        self.cursorPosition = len(txt)
        self.renderCursor()

    def append(self, txt):
        self.trueText += txt
        self.visualText += txt
        self.renderText()
        self.cursorPosition = len(self.trueText) - 1
        self.renderCursor()

    def clear(self):
        self.trueText = ''
        self.visualText = ''
        self.renderText()
        self.cursorPosition = 0
        self.renderCursor()

    def eventReturn(self):
        return None

    def eventClick(self):
        return None

    def eventLostFocus(self):
        return None

    def eventEscape(self):
        return None

    def eventActive(self):
        return None


class soEditBox(PyGUIBase):
    factoryString = 'soGUI.soEditBox'
    FRAME_ACTIVE = BigWorld.PyTextureProvider('soGUI/maps/Controls/editBox/frame_active.tga')
    FRAME_PASSIVE = BigWorld.PyTextureProvider('soGUI/maps/Controls/editBox/frame_passive.tga')
    FRAME_ERROR = BigWorld.PyTextureProvider('soGUI/maps/Controls/editBox/frame_error.tga')
    CURSOR_TEXTURE = BigWorld.PyTextureProvider('soGUI/maps/Colours/white.tga')
    SELECTION_TEXTURE = BigWorld.PyTextureProvider('soGUI/maps/Colours/white.tga')
    BANNED_CHARACTERS = [u'\r',
     u'\x08',
     u'\x1b',
     u'\t']
    PUNCTUATION = [u'.',
     u',',
     u'[',
     u']',
     u'(',
     u')',
     u' ',
     u'<',
     u'>',
     u'-']

    def __init__(self, component, width, height, hOffset = 3, vOffset = 3, readOnly = False, font = 'ruRU_Cyrvetica_Extra_14i.font', multiline = False, color = (255, 255, 255, 255), maskChar = None, regEx = None, inputValidator = lambda newStr, wholeText, offset: True, autosize = True):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.width = width
        self.height = height
        self.hOffset = hOffset
        self.vOffset = vOffset
        self.readOnly = readOnly
        self.multiline = multiline
        self.font = font
        self.color = color
        self.maskChar = maskChar
        self.regEx = regEx
        self.inputValidator = inputValidator
        self.autosize = autosize
        self.hover = False
        self.pressed = False
        self.active = False
        self.disabled = False
        self.erroneous = False
        self.rawText = u''
        self.formattedText = ['']
        self.hScrollOff = 0
        self.vScrollOff = 0
        self.maxCharWidth, self.stringHeight = self._getTxtDims(u'W')
        self.blinker = None
        self.errorNotifier = None
        self.cursor = [0, 0]
        self.selectionAnchor = None
        self.selectionState = False
        self.setupRoot()
        self.setupContent()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = self.width
        cmp.height = self.height

    def setupContent(self):
        cmp = GUI.Frame2('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.width = cmp.height = 2.0
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.texture = self.FRAME_PASSIVE
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'dFrame')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = self.width - self.hOffset * 2.0
        cmp.height = self.height - self.vOffset * 2.0
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.hOffset, self.vOffset, 0.8)
        cmp.mouseButtonFocus = True
        cmp.moveFocus = True
        cmp.crossFocus = True
        cmp.script = self
        self.component.addChild(cmp, 'textPlane')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.texture = self.CURSOR_TEXTURE
        cmp.width = 1
        cmp.height = self._getTxtDims(u'W')[1] - 4
        cmp.visible = False
        cmp.position = (0, 0, 0.1)
        self.component.textPlane.addChild(cmp, 'cursor')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = self.color
        cmp.materialFX = 'BLEND'
        cmp.font = self.font
        cmp.multiline = self.multiline
        cmp.colourFormatting = False
        cmp.position = (0, 0, 0.2)
        self.component.textPlane.addChild(cmp, 'textRender')
        if self.autosize:
            self.height = self.stringHeight + self.vOffset * 2
            self.component.height = self.height
            self.component.textPlane.height = self.stringHeight

    def checkValidity(self, evaluationStr, offset):
        return self.inputValidator(evaluationStr, self.rawText, offset)

    def setValidator(self, callback):
        if callback is None:
            self.inputValidator = lambda newStr, wholeText, offset: True
        else:
            self.inputValidator = callback
        return

    def _getRawPosition(self, x, y):
        if x > len(self.formattedText):
            return None
        elif y > len(self.formattedText[x]):
            return None
        else:
            strLen = 0
            for i in xrange(x):
                strLen += len(self.formattedText[x])

            strLen += y
            return strLen

    def _getCharCoords(self, pos):
        strLen = 0
        for x in xrange(len(self.formattedText)):
            strLen += len(self.formattedText[x])
            if strLen >= pos:
                return [x, strLen - pos]

    def _inputError(self):
        self.runErrorNotify()

    def addChar(self, char):
        charPos = self._getRawPosition(*self.cursor)
        if self.selectionAnchor:
            self.deleteSelection()
        if not self.checkValidity(char, charPos):
            self._inputError()
            return False
        elif charPos is None:
            return False
        else:
            resultStr = u''
            for letter in char:
                if letter not in self.BANNED_CHARACTERS:
                    resultStr += letter

            if charPos < len(self.rawText):
                self.rawText = self.rawText[:charPos] + resultStr + self.rawText[charPos:]
            else:
                self.rawText += resultStr
            self.formattedText[self.cursor[0]] = self.formattedText[self.cursor[0]][:self.cursor[1]] + resultStr + self.formattedText[self.cursor[0]][self.cursor[1]:]
            self._renderText()
            self.onValueChange(True)
            return True

    def backSpace(self, shift = False):
        if self.selectionAnchor:
            self.deleteSelection()
            self._renderText()
            return True
        else:
            charPos = self._getRawPosition(*self.cursor)
            if charPos is None or charPos == 0:
                return False
            if charPos < len(self.rawText):
                if not shift:
                    self.rawText = self.rawText[:charPos - 1] + self.rawText[charPos:]
                else:
                    self.rawText = self.rawText[charPos:]
            elif not shift:
                self.rawText = self.rawText[:-1]
            else:
                self.clear()
            if not shift:
                self.formattedText[self.cursor[0]] = self.formattedText[self.cursor[0]][:self.cursor[1] - 1] + self.formattedText[self.cursor[0]][self.cursor[1]:]
            else:
                self.formattedText[self.cursor[0]] = self.formattedText[self.cursor[0]][self.cursor[1]:]
            self._renderText()
            self.onValueChange(True)
            return True

    def deleteChar(self, shift):
        charPos = self._getRawPosition(*self.cursor)
        if charPos is None:
            return False
        else:
            if charPos < len(self.rawText):
                if not shift:
                    self.rawText = self.rawText[:charPos] + self.rawText[charPos + 1:]
                    self.formattedText[self.cursor[0]] = self.formattedText[self.cursor[0]][:self.cursor[1]] + self.formattedText[self.cursor[0]][self.cursor[1] + 1:]
                else:
                    self.rawText = self.rawText[:charPos]
                    self.formattedText[self.cursor[0]] = self.formattedText[self.cursor[0]][:self.cursor[1]]
            self._renderText()
            self.onValueChange(True)
            return True

    def deleteSelection(self):
        startCoords = self.selectionAnchor
        stopCoords = self.cursor
        if not self.selectionAnchor:
            return
        else:
            direction = 1
            if self.selectionAnchor[0] < self.cursor[0]:
                startCoords = self.cursor
                stopCoords = self.selectionAnchor
                direction = -1
            elif self.selectionAnchor[0] == self.cursor[0]:
                if self.selectionAnchor[1] > self.cursor[1]:
                    startCoords = self.cursor
                    stopCoords = self.selectionAnchor
                    direction = -1
            for i in xrange(startCoords[0], stopCoords[0] + 1):
                startChar = 0
                endChar = len(self.formattedText[i])
                if i == startCoords[0]:
                    startChar = startCoords[1]
                if i == stopCoords[0]:
                    endChar = stopCoords[1]
                self.formattedText[i] = self.formattedText[i][:startChar] + self.formattedText[i][endChar:]

            rawCharStart = self._getRawPosition(*startCoords)
            rawCharStop = self._getRawPosition(*stopCoords)
            if rawCharStop is None:
                rawCharStop = len(self.rawText)
            self.rawText = self.rawText[:rawCharStart] + self.rawText[rawCharStop:]
            self.setCursor(startCoords[0], startCoords[1])
            self._renderText()
            self.onValueChange(True)
            return

    def deleteKey(self, shift = False):
        if self.selectionAnchor is None:
            self.deleteChar(shift)
        else:
            self.deleteSelection()
            self.deselect()
        return

    def homeKey(self, shift = False):
        if shift:
            if self.selectionAnchor is None:
                self._startSelection()
            else:
                self._startSelection(False)
        self.setCursor(self.cursor[0], 0)
        self._renderSelection()
        return

    def endKey(self, shift = False):
        if shift:
            if self.selectionAnchor is None:
                self._startSelection()
            else:
                self._startSelection(False)
        self.setCursor(self.cursor[0], len(self.formattedText[self.cursor[0]]))
        self._renderSelection()
        return

    def _renderText(self):
        self.component.textPlane.textRender.text = u''
        for txtLine in self.formattedText:
            if self.maskChar:
                txtLine = self.maskChar * len(txtLine)
            self.component.textPlane.textRender.text += txtLine

    def setCursor(self, x, y):
        if x < 0 or y < 0:
            return
        if x < len(self.formattedText):
            if y <= len(self.formattedText[x]):
                self.cursor = [x, y]
        if not self.selectionState:
            self.deselect()
        self._updateCursor()

    def _updateCursor(self):
        self.component.textPlane.cursor.position.y = self.cursor[0] * self.stringHeight + 2
        self.component.textPlane.cursor.position.x = self._getTxtDims(self.formattedText[self.cursor[0]][:self.cursor[1]])[0]
        self._scrollToCursor()

    def _findNearestPunctiation(self, start, direction = 1):
        searchStr = ''
        if direction > 0:
            searchStr = self.formattedText[start[0]][start[1]:len(self.formattedText[start[0]])]
        else:
            searchStr = self.formattedText[start[0]][0:start[1]]
        searchList = list(searchStr)
        if direction < 0:
            searchList.reverse()
        offset = 0
        for letter in searchList:
            offset += 1
            if letter in self.PUNCTUATION:
                if offset < 2:
                    return offset
                else:
                    return offset - 1

        return len(searchList)

    def handleKeyEvent(self, event):
        if event.isMouseButton():
            return event.isKeyDown() and False
        else:
            if event.key == KEY_LEFTMOUSE and self.pressed:
                BWPersonality.GUICore.mouseHook = lambda event: False
                self.pressed = False
                if self.selectionState:
                    if BigWorld.isKeyDown(KEY_LSHIFT) or not BigWorld.isKeyDown(KEY_RSHIFT):
                        self._stopSelection()
                    self._renderSelection()
                    return True
                else:
                    return False
            if event.key in [KEY_ESCAPE, KEY_TAB] and event.isKeyDown():
                self.activate(False)
                if event.key == KEY_ESCAPE:
                    self.onEscape()
                if event.key == KEY_TAB:
                    self.onTab()
            if event.isKeyUp():
                if event.key == KEY_LSHIFT or event.key == KEY_RSHIFT:
                    self._stopSelection()
            if event.isKeyDown():
                if event.key in (KEY_RETURN, KEY_NUMPADENTER):
                    if not self.multiline:
                        self.onDefaultAction()
                        self.activate(False)
                    return True
                if event.key == KEY_UPARROW:
                    self.setCursor(self.cursor[0] - 1, self.cursor[1])
                    return True
                if event.key == KEY_LEFTARROW:
                    if event.isShiftDown():
                        if self.selectionAnchor is None:
                            self._startSelection()
                        else:
                            self._startSelection(False)
                    if event.isCtrlDown():
                        offset = self._findNearestPunctiation(self.cursor, -1)
                        self.setCursor(self.cursor[0], self.cursor[1] - offset)
                    else:
                        self.setCursor(self.cursor[0], self.cursor[1] - 1)
                    self._renderSelection()
                    return True
                if event.key == KEY_RIGHTARROW:
                    if event.isShiftDown():
                        if self.selectionAnchor is None:
                            self._startSelection()
                        else:
                            self._startSelection(False)
                    if event.isCtrlDown():
                        offset = self._findNearestPunctiation(self.cursor, 1)
                        self.setCursor(self.cursor[0], self.cursor[1] + offset)
                    else:
                        self.setCursor(self.cursor[0], self.cursor[1] + 1)
                    self._renderSelection()
                    return True
                if event.key == KEY_DOWNARROW:
                    self.setCursor(self.cursor[0] + 1, self.cursor[1])
                    return True
                if event.key == KEY_BACKSPACE:
                    if self.backSpace(event.isShiftDown()):
                        if event.isShiftDown():
                            self.setCursor(self.cursor[0], 0)
                        else:
                            self.setCursor(self.cursor[0], self.cursor[1] - 1)
                    return True
                if event.key == KEY_DELETE:
                    self.deleteKey(event.isShiftDown())
                    return True
                if event.key == KEY_HOME:
                    self.homeKey(event.isShiftDown())
                    return True
                if event.key == KEY_END:
                    self.endKey(event.isShiftDown())
                    return True
                if event.key == KEY_C and event.isCtrlDown():
                    self.copy()
                    return True
                if event.key == KEY_V and event.isCtrlDown():
                    self.paste()
                    return True
                if event.key == KEY_X and event.isCtrlDown():
                    self.cut()
                    return True
            if event.character is not None:
                if event.isCtrlDown():
                    return True
                if event.character in self.BANNED_CHARACTERS:
                    return True
                if self.addChar(event.character):
                    self.setCursor(self.cursor[0], self.cursor[1] + 1)
            return True

    def _getTxtDims(self, txt):
        testTGC = GUI.Text('')
        testTGC.colourFormatting = False
        testTGC.multiline = False
        testTGC.font = self.font
        if self.maskChar:
            txt = self.maskChar * len(txt)
        return list(testTGC.stringDimensions(txt))

    def handleMouseButtonEvent(self, comp, event):
        if not event.isMouseButton():
            return False
        if event.key == KEY_LEFTMOUSE:
            if not self._isActive():
                if event.isKeyDown():
                    self.pressed = True
                elif self.pressed:
                    self.pressed = False
                    self.onClick()
            elif event.isKeyDown():
                self.pressed = True
                local = self.component.screenToLocal((event.cursorPosition[0], event.cursorPosition[1]))
                self._setCursorByMouse(local)
            else:
                self.pressed = False
                if self.selectionState:
                    (BigWorld.isKeyDown(KEY_LSHIFT) or not BigWorld.isKeyDown(KEY_RSHIFT)) and self._stopSelection()
                self._renderSelection()
        return False

    def _startSelection(self, ressetting = True):
        self.selectionState = True
        if ressetting:
            self.selectionAnchor = [self.cursor[0], self.cursor[1]]

    def _stopSelection(self):
        self.selectionState = False

    def _renderSelection(self):
        if self.selectionAnchor is None:
            return
        else:
            startCoords = self.selectionAnchor
            stopCoords = self.cursor
            direction = 1
            if self.selectionAnchor[0] < self.cursor[0]:
                startCoords = self.cursor
                stopCoords = self.selectionAnchor
                direction = -1
            elif self.selectionAnchor[0] == self.cursor[0]:
                if self.selectionAnchor[1] > self.cursor[1]:
                    startCoords = self.cursor
                    stopCoords = self.selectionAnchor
                    direction = -1
            for i in xrange(startCoords[0], stopCoords[0] + 1):
                startChar = 0
                endChar = len(self.formattedText[i])
                if i == startCoords[0]:
                    startChar = startCoords[1]
                if i == stopCoords[0]:
                    endChar = stopCoords[1]
                cmp = GUI.Simple('')
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.colour = (0, 0, 0, 255)
                cmp.materialFX = 'BLEND'
                cmp.position.y = i * self.stringHeight + self.vScrollOff
                cmp.position.x = self._getTxtDims(self.formattedText[i][:startChar])[0]
                cmp.width = self._getTxtDims(self.formattedText[i][startChar:endChar])[0]
                cmp.height = self.stringHeight
                cmp.position.z = 0.5
                cmp.texture = self.SELECTION_TEXTURE
                self.component.textPlane.addChild(cmp, 'selection_{0}'.format(i))

            return

    def select(self, start, stop):
        self.deselect()
        self.selectionState = True
        self.selectionAnchor = start
        self.setCursor(stop[0], stop[1])
        self._renderSelection()
        self.selectionState = False

    def deselect(self):
        self.selectionAnchor = None
        self.selectionState = False
        for name, child in self.component.textPlane.children:
            if 'selection_' in name:
                self.component.textPlane.delChild(child)
                child.script = None

        return

    def handleMouseEvent(self, comp, event):
        if not self._isActive():
            return False
        if not self.selectionState and self.pressed:
            self._startSelection()
        if self.selectionState and not BigWorld.isKeyDown(KEY_LSHIFT) and not BigWorld.isKeyDown(KEY_RSHIFT):
            local = self.component.screenToLocal((event.cursorPosition[0], event.cursorPosition[1]))
            self._setCursorByMouse(local)
            self._renderSelection()
            return True
        return False

    def activate(self, doActivate = True, silent = False):
        if doActivate:
            if not self._isActive():
                self.active = doActivate
                BWPersonality.GUICore.registerCharacterReciever(self.component)
                self.runBlinker()
        else:
            self.active = doActivate
            BWPersonality.GUICore.unregisterCharacterReciever(self.component)
            self.stopBlinker()
            self.deselect()
        self.updateVisuals()
        if not silent:
            self.onActive(self._isActive())

    def _isActive(self):
        return self.active

    def onClick(self):
        self.activate()

    def onRClick(self):
        self.activate()

    def lostCharacterFeed(self):
        if self._isActive():
            self.activate(False)

    def getCharacterFeed(self):
        if not self._isActive():
            self.activate()

    def _updateScrolledState(self):
        self.component.textPlane.textRender.position.x = -self.hScrollOff
        self.component.textPlane.textRender.position.y = self.vScrollOff
        self.component.textPlane.cursor.position.x -= self.hScrollOff
        self.component.textPlane.cursor.position.y += self.vScrollOff

    def _setCursorByMouse(self, coords):
        stringNumber = int(ceil((coords.y + self.vScrollOff) / self.stringHeight))
        strWidth = 0
        charNumber = 0
        if stringNumber >= len(self.formattedText):
            stringNumber = len(self.formattedText) - 1
        if stringNumber < 0:
            stringNumber = 0
        if self._getTxtDims(self.formattedText[stringNumber])[0] < coords.x + self.hScrollOff:
            charNumber = len(self.formattedText[stringNumber])
        else:
            while strWidth < coords.x - self.component.textPlane.textRender.position.x:
                strWidth += self._getTxtDims(self.formattedText[stringNumber][charNumber])[0]
                charNumber += 1

            if charNumber > 0:
                charNumber -= 1
        if BigWorld.isKeyDown(KEY_LSHIFT) or BigWorld.isKeyDown(KEY_RSHIFT):
            if self.selectionAnchor is None:
                self._startSelection(True)
            else:
                self._startSelection(False)
        self.setCursor(stringNumber, charNumber)
        return

    def _scrollToCursor(self):
        hOff = self.component.textPlane.cursor.position.x + self.component.textPlane.cursor.width - self.component.textPlane.width
        if hOff > 0:
            self.hScrollOff = hOff
        else:
            self.hScrollOff = 0
        vOff = self.component.textPlane.cursor.position.y + self.component.textPlane.cursor.height - self.component.textPlane.height
        if vOff > 0:
            self.vScrollOff = vOff
        else:
            self.vScrollOff = 0
        self._updateScrolledState()

    def mouseHook(self, event):
        self.handleMouseEvent(self.component.textPlane, event)

    def handleMouseEnterEvent(self, component):
        BWPersonality.GUICore.mouseHook = lambda event: False
        return True

    def handleMouseLeaveEvent(self, component):
        if self.selectionAnchor is not None and self.pressed:
            BWPersonality.GUICore.mouseHook = self.mouseHook
            self._renderSelection()
        return True

    def copy(self):
        if not self.selectionAnchor:
            return
        else:
            startCoords = self.selectionAnchor
            stopCoords = self.cursor
            direction = 1
            if self.selectionAnchor[0] < self.cursor[0]:
                startCoords = self.cursor
                stopCoords = self.selectionAnchor
                direction = -1
            elif self.selectionAnchor[0] == self.cursor[0]:
                if self.selectionAnchor[1] > self.cursor[1]:
                    startCoords = self.cursor
                    stopCoords = self.selectionAnchor
                    direction = -1
            rawCharStart = self._getRawPosition(*startCoords)
            rawCharStop = self._getRawPosition(*stopCoords)
            if rawCharStop is None:
                rawCharStop = len(self.rawText)
            cpyTxt = self.rawText[rawCharStart:rawCharStop]
            if self.maskChar:
                cpyTxt = self.maskChar * len(cpyTxt)
            BigWorld.clipboardSetPlainText(cpyTxt)
            return

    def paste(self):
        clipText = BigWorld.clipboardGetPlainText()
        self.deleteSelection()
        self.addChar(clipText)
        self.setCursor(self.cursor[0], self.cursor[1] + len(clipText))
        self._renderText()

    def cut(self):
        self.copy()
        self.deleteSelection()

    def updateVisuals(self):
        if self._isActive():
            self.component.dFrame.texture = self.FRAME_ACTIVE
        else:
            self.component.dFrame.texture = self.FRAME_PASSIVE
        if self.erroneous:
            self.component.dFrame.texture = self.FRAME_ERROR

    def runBlinker(self):
        if self.blinker is None:
            self.blinker = self.cursorBlink()
            self.blinker.run()
        return

    def stopBlinker(self):
        if self.blinker:
            self.blinker.stop()
            self.blinker = None
        self.component.textPlane.cursor.visible = False
        return

    def runErrorNotify(self):
        if self.errorNotifier:
            self.errorNotifier.stop()
        self.errorNotifier = self.erroneousState(0.05)
        self.errorNotifier.run()

    def stopErrorNotify(self):
        if self.errorNotifier:
            self.errorNotifier.stop()
            self.errorNotifier = None
        self.erroneous = False
        self.updateVisuals()
        return

    def clear(self, byUser = True):
        self.rawText = u''
        self.formattedText = ['']
        self.deselect()
        self._renderText()
        self.setCursor(0, 0)
        self.onValueChange(byUser)

    def setValue(self, newText):
        self.clear()
        self.addChar(newText)
        self.setCursor(self.cursor[0], self.cursor[1] + len(newText))
        self._renderText()

    def fini(self):
        if self._isActive():
            BWPersonality.GUICore.unregisterCharacterReciever(self.component)
        BWPersonality.GUICore.mouseHook = lambda event: False
        self.stopBlinker()
        self.stopErrorNotify()

    def getValue(self):
        return self.formattedText

    def getRaw(self):
        return self.rawText

    def onActive(self, active):
        return None

    def onDefaultAction(self):
        return None

    def onValueChange(self, byUser):
        return None

    def onEscape(self):
        return None

    def onTab(self):
        return None

    @BWMemberCoroutine
    def cursorBlink(self, frequency = 0.25):
        self.component.textPlane.cursor.visible = True
        while self.active:
            yield BWWaitForPeriod(frequency)
            self.component.textPlane.cursor.visible = not self.component.textPlane.cursor.visible

        self.component.textPlane.cursor.visible = False
        self.blinker = None
        return

    @BWMemberCoroutine
    def erroneousState(self, lasting = 1.0):
        self.erroneous = True
        self.updateVisuals()
        yield BWWaitForPeriod(lasting)
        self.erroneous = False
        self.updateVisuals()
        self.errorNotifier = None
        return


class soEditBox2(PyGUIBase):
    factoryString = 'soGUI.soEditBox2'
    FRAME_ACTIVE = BigWorld.PyTextureProvider('soGUI/maps/Controls/editBox/frame_active.tga')
    FRAME_PASSIVE = BigWorld.PyTextureProvider('soGUI/maps/Controls/editBox/frame_passive.tga')
    FRAME_ERROR = BigWorld.PyTextureProvider('soGUI/maps/Controls/editBox/frame_error.tga')
    CURSOR_TEXTURE = BigWorld.PyTextureProvider('soGUI/maps/Colours/white.tga')
    SELECTION_TEXTURE = BigWorld.PyTextureProvider('soGUI/maps/Colours/white.tga')
    BANNED_CHARACTERS = [u'\r',
     u'\x08',
     u'\x1b',
     u'\t']
    PUNCTUATION = [u'.',
     u',',
     u'[',
     u']',
     u'(',
     u')',
     u' ',
     u'<',
     u'>',
     u'-']

    def __init__(self, component, width, height, hOffset = 3, vOffset = 3, readOnly = False, font = 'ruRU_Cyrvetica_Extra_14i.font', multiline = False, color = (255, 255, 255, 255), maskChar = None, regEx = None, inputValidator = lambda newStr, wholeText, offset: True, autosize = True):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.width = width
        self.height = height
        self.hOffset = hOffset
        self.vOffset = vOffset
        self.readOnly = readOnly
        self.multiline = multiline
        self.font = font
        self.color = color
        self.maskChar = maskChar
        self.regEx = regEx
        self.inputValidator = inputValidator
        self.autosize = autosize
        self.hover = False
        self.pressed = False
        self.active = False
        self.disabled = False
        self.erroneous = False
        self.rawText = u''
        self.formattedText = ['']
        self.hScrollOff = 0
        self.vScrollOff = 0
        self.maxCharWidth, self.stringHeight = self._getTxtDims(u'W')
        self.blinker = None
        self.errorNotifier = None
        self.cursor = [0, 0]
        self.selectionAnchor = None
        self.selectionState = False
        self.setupRoot()
        self.setupContent()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = self.width
        cmp.height = self.height

    def setupContent(self):
        cmp = GUI.Frame2('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.width = cmp.height = 2.0
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.texture = self.FRAME_PASSIVE
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'dFrame')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = self.width - self.hOffset * 2.0
        cmp.height = self.height - self.vOffset * 2.0
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.hOffset, self.vOffset, 0.8)
        cmp.mouseButtonFocus = True
        cmp.moveFocus = True
        cmp.crossFocus = True
        cmp.script = self
        self.component.addChild(cmp, 'textPlane')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.texture = self.CURSOR_TEXTURE
        cmp.width = 1
        cmp.height = self._getTxtDims(u'W')[1] - 4
        cmp.visible = False
        cmp.position = (0, 0, 0.1)
        self.component.textPlane.addChild(cmp, 'cursor')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = self.color
        cmp.materialFX = 'BLEND'
        cmp.font = self.font
        cmp.multiline = self.multiline
        cmp.colourFormatting = False
        cmp.position = (0, 0, 0.2)
        self.component.textPlane.addChild(cmp, 'textRender')
        if self.autosize:
            self.height = self.stringHeight + self.vOffset * 2
            self.component.height = self.height
            self.component.textPlane.height = self.stringHeight

    def checkValidity(self, evaluationStr, offset):
        return self.inputValidator(evaluationStr, self.rawText, offset)

    def setValidator(self, callback):
        if callback is None:
            self.inputValidator = lambda newStr, wholeText, offset: True
        else:
            self.inputValidator = callback
        return

    def _getRawPosition(self, x, y):
        if x > len(self.formattedText):
            return None
        elif y > len(self.formattedText[x]):
            return None
        else:
            strLen = 0
            for i in xrange(x):
                strLen += len(self.formattedText[x])

            strLen += y
            return strLen

    def _getCharCoords(self, pos):
        strLen = 0
        for x in xrange(len(self.formattedText)):
            strLen += len(self.formattedText[x])
            if strLen >= pos:
                return [x, strLen - pos]

    def _inputError(self):
        self.runErrorNotify()

    def addChar(self, char):
        charPos = self._getRawPosition(*self.cursor)
        if self.selectionAnchor:
            self.deleteSelection()
        if not self.checkValidity(char, charPos):
            self._inputError()
            return False
        elif charPos is None:
            return False
        else:
            resultStr = u''
            for letter in char:
                if letter not in self.BANNED_CHARACTERS:
                    resultStr += letter

            if charPos < len(self.rawText):
                self.rawText = self.rawText[:charPos] + resultStr + self.rawText[charPos:]
            else:
                self.rawText += resultStr
            self.formattedText[self.cursor[0]] = self.formattedText[self.cursor[0]][:self.cursor[1]] + resultStr + self.formattedText[self.cursor[0]][self.cursor[1]:]
            self._renderText()
            self.onValueChange(True)
            return True

    def backSpace(self, shift = False):
        if self.selectionAnchor:
            self.deleteSelection()
            self._renderText()
            return True
        else:
            charPos = self._getRawPosition(*self.cursor)
            if charPos is None or charPos == 0:
                return False
            if charPos < len(self.rawText):
                if not shift:
                    self.rawText = self.rawText[:charPos - 1] + self.rawText[charPos:]
                else:
                    self.rawText = self.rawText[charPos:]
            elif not shift:
                self.rawText = self.rawText[:-1]
            else:
                self.clear()
            if not shift:
                self.formattedText[self.cursor[0]] = self.formattedText[self.cursor[0]][:self.cursor[1] - 1] + self.formattedText[self.cursor[0]][self.cursor[1]:]
            else:
                self.formattedText[self.cursor[0]] = self.formattedText[self.cursor[0]][self.cursor[1]:]
            self._renderText()
            self.onValueChange(True)
            return True

    def deleteChar(self, shift):
        charPos = self._getRawPosition(*self.cursor)
        if charPos is None:
            return False
        else:
            if charPos < len(self.rawText):
                if not shift:
                    self.rawText = self.rawText[:charPos] + self.rawText[charPos + 1:]
                    self.formattedText[self.cursor[0]] = self.formattedText[self.cursor[0]][:self.cursor[1]] + self.formattedText[self.cursor[0]][self.cursor[1] + 1:]
                else:
                    self.rawText = self.rawText[:charPos]
                    self.formattedText[self.cursor[0]] = self.formattedText[self.cursor[0]][:self.cursor[1]]
            self._renderText()
            self.onValueChange(True)
            return True

    def deleteSelection(self):
        startCoords = self.selectionAnchor
        stopCoords = self.cursor
        if not self.selectionAnchor:
            return
        else:
            direction = 1
            if self.selectionAnchor[0] < self.cursor[0]:
                startCoords = self.cursor
                stopCoords = self.selectionAnchor
                direction = -1
            elif self.selectionAnchor[0] == self.cursor[0]:
                if self.selectionAnchor[1] > self.cursor[1]:
                    startCoords = self.cursor
                    stopCoords = self.selectionAnchor
                    direction = -1
            for i in xrange(startCoords[0], stopCoords[0] + 1):
                startChar = 0
                endChar = len(self.formattedText[i])
                if i == startCoords[0]:
                    startChar = startCoords[1]
                if i == stopCoords[0]:
                    endChar = stopCoords[1]
                self.formattedText[i] = self.formattedText[i][:startChar] + self.formattedText[i][endChar:]

            rawCharStart = self._getRawPosition(*startCoords)
            rawCharStop = self._getRawPosition(*stopCoords)
            if rawCharStop is None:
                rawCharStop = len(self.rawText)
            self.rawText = self.rawText[:rawCharStart] + self.rawText[rawCharStop:]
            self.setCursor(startCoords[0], startCoords[1])
            self._renderText()
            self.onValueChange(True)
            return

    def deleteKey(self, shift = False):
        if self.selectionAnchor is None:
            self.deleteChar(shift)
        else:
            self.deleteSelection()
            self.deselect()
        return

    def homeKey(self, shift = False):
        if shift:
            if self.selectionAnchor is None:
                self._startSelection()
            else:
                self._startSelection(False)
        self.setCursor(self.cursor[0], 0)
        self._renderSelection()
        return

    def endKey(self, shift = False):
        if shift:
            if self.selectionAnchor is None:
                self._startSelection()
            else:
                self._startSelection(False)
        self.setCursor(self.cursor[0], len(self.formattedText[self.cursor[0]]))
        self._renderSelection()
        return

    def _renderText(self):
        self.component.textPlane.textRender.text = u''
        for txtLine in self.formattedText:
            if self.maskChar:
                txtLine = self.maskChar * len(txtLine)
            self.component.textPlane.textRender.text += txtLine

    def setCursor(self, x, y):
        if x < 0 or y < 0:
            return
        if x < len(self.formattedText):
            if y <= len(self.formattedText[x]):
                self.cursor = [x, y]
        if not self.selectionState:
            self.deselect()
        self._updateCursor()

    def _updateCursor(self):
        self.component.textPlane.cursor.position.y = self.cursor[0] * self.stringHeight + 2
        self.component.textPlane.cursor.position.x = self._getTxtDims(self.formattedText[self.cursor[0]][:self.cursor[1]])[0]
        self._scrollToCursor()

    def _findNearestPunctiation(self, start, direction = 1):
        searchStr = ''
        if direction > 0:
            searchStr = self.formattedText[start[0]][start[1]:len(self.formattedText[start[0]])]
        else:
            searchStr = self.formattedText[start[0]][0:start[1]]
        searchList = list(searchStr)
        if direction < 0:
            searchList.reverse()
        offset = 0
        for letter in searchList:
            offset += 1
            if letter in self.PUNCTUATION:
                if offset < 2:
                    return offset
                else:
                    return offset - 1

        return len(searchList)

    def handleKeyEvent(self, event):
        if event.isMouseButton():
            return event.isKeyDown() and False
        else:
            if event.key == KEY_LEFTMOUSE and self.pressed:
                BWPersonality.GUICore.mouseHook = lambda event: False
                self.pressed = False
                if self.selectionState:
                    if BigWorld.isKeyDown(KEY_LSHIFT) or not BigWorld.isKeyDown(KEY_RSHIFT):
                        self._stopSelection()
                    self._renderSelection()
                    return True
                else:
                    return False
            if event.key in [KEY_ESCAPE, KEY_TAB] and event.isKeyDown():
                self.activate(False)
                if event.key == KEY_ESCAPE:
                    self.onEscape()
                if event.key == KEY_TAB:
                    self.onTab()
            if event.isKeyUp():
                if event.key == KEY_LSHIFT or event.key == KEY_RSHIFT:
                    self._stopSelection()
            if event.isKeyDown():
                if event.key == KEY_PGUP:
                    self.onPgUp()
                    return True
                if event.key == KEY_PGDN:
                    self.onPgDn()
                    return True
                if event.key in (KEY_RETURN, KEY_NUMPADENTER):
                    if not self.multiline:
                        self.onDefaultAction()
                    return True
                if event.key == KEY_UPARROW:
                    self.setCursor(self.cursor[0] - 1, self.cursor[1])
                    return True
                if event.key == KEY_LEFTARROW:
                    if event.isShiftDown():
                        if self.selectionAnchor is None:
                            self._startSelection()
                        else:
                            self._startSelection(False)
                    if event.isCtrlDown():
                        offset = self._findNearestPunctiation(self.cursor, -1)
                        self.setCursor(self.cursor[0], self.cursor[1] - offset)
                    else:
                        self.setCursor(self.cursor[0], self.cursor[1] - 1)
                    self._renderSelection()
                    return True
                if event.key == KEY_RIGHTARROW:
                    if event.isShiftDown():
                        if self.selectionAnchor is None:
                            self._startSelection()
                        else:
                            self._startSelection(False)
                    if event.isCtrlDown():
                        offset = self._findNearestPunctiation(self.cursor, 1)
                        self.setCursor(self.cursor[0], self.cursor[1] + offset)
                    else:
                        self.setCursor(self.cursor[0], self.cursor[1] + 1)
                    self._renderSelection()
                    return True
                if event.key == KEY_DOWNARROW:
                    self.setCursor(self.cursor[0] + 1, self.cursor[1])
                    return True
                if event.key == KEY_BACKSPACE:
                    if self.backSpace(event.isShiftDown()):
                        if event.isShiftDown():
                            self.setCursor(self.cursor[0], 0)
                        else:
                            self.setCursor(self.cursor[0], self.cursor[1] - 1)
                    return True
                if event.key == KEY_DELETE:
                    self.deleteKey(event.isShiftDown())
                    return True
                if event.key == KEY_HOME:
                    self.homeKey(event.isShiftDown())
                    return True
                if event.key == KEY_END:
                    self.endKey(event.isShiftDown())
                    return True
                if event.key == KEY_C and event.isCtrlDown():
                    self.copy()
                    return True
                if event.key == KEY_V and event.isCtrlDown():
                    self.paste()
                    return True
                if event.key == KEY_X and event.isCtrlDown():
                    self.cut()
                    return True
            if event.character is not None:
                if event.isCtrlDown():
                    return True
                if event.character in self.BANNED_CHARACTERS:
                    return True
                if self.addChar(event.character):
                    self.setCursor(self.cursor[0], self.cursor[1] + 1)
            return True

    def _getTxtDims(self, txt):
        testTGC = GUI.Text('')
        testTGC.colourFormatting = False
        testTGC.multiline = False
        testTGC.font = self.font
        if self.maskChar:
            txt = self.maskChar * len(txt)
        return list(testTGC.stringDimensions(txt))

    def handleMouseButtonEvent(self, comp, event):
        if not event.isMouseButton():
            return False
        if event.key == KEY_LEFTMOUSE:
            if not self._isActive():
                if event.isKeyDown():
                    self.pressed = True
                elif self.pressed:
                    self.pressed = False
                    self.onClick()
            elif event.isKeyDown():
                self.pressed = True
                local = self.component.screenToLocal((event.cursorPosition[0], event.cursorPosition[1]))
                self._setCursorByMouse(local)
            else:
                self.pressed = False
                if self.selectionState:
                    (BigWorld.isKeyDown(KEY_LSHIFT) or not BigWorld.isKeyDown(KEY_RSHIFT)) and self._stopSelection()
                self._renderSelection()
        return False

    def _startSelection(self, ressetting = True):
        self.selectionState = True
        if ressetting:
            self.selectionAnchor = [self.cursor[0], self.cursor[1]]

    def _stopSelection(self):
        self.selectionState = False

    def _renderSelection(self):
        if self.selectionAnchor is None:
            return
        else:
            startCoords = self.selectionAnchor
            stopCoords = self.cursor
            direction = 1
            if self.selectionAnchor[0] < self.cursor[0]:
                startCoords = self.cursor
                stopCoords = self.selectionAnchor
                direction = -1
            elif self.selectionAnchor[0] == self.cursor[0]:
                if self.selectionAnchor[1] > self.cursor[1]:
                    startCoords = self.cursor
                    stopCoords = self.selectionAnchor
                    direction = -1
            for i in xrange(startCoords[0], stopCoords[0] + 1):
                startChar = 0
                endChar = len(self.formattedText[i])
                if i == startCoords[0]:
                    startChar = startCoords[1]
                if i == stopCoords[0]:
                    endChar = stopCoords[1]
                cmp = GUI.Simple('')
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.colour = (0, 0, 0, 255)
                cmp.materialFX = 'BLEND'
                cmp.position.y = i * self.stringHeight + self.vScrollOff
                cmp.position.x = self._getTxtDims(self.formattedText[i][:startChar])[0]
                cmp.width = self._getTxtDims(self.formattedText[i][startChar:endChar])[0]
                cmp.height = self.stringHeight
                cmp.position.z = 0.5
                cmp.texture = self.SELECTION_TEXTURE
                self.component.textPlane.addChild(cmp, 'selection_{0}'.format(i))

            return

    def select(self, start, stop):
        self.deselect()
        self.selectionState = True
        self.selectionAnchor = start
        self.setCursor(stop[0], stop[1])
        self._renderSelection()
        self.selectionState = False

    def deselect(self):
        self.selectionAnchor = None
        self.selectionState = False
        for name, child in self.component.textPlane.children:
            if 'selection_' in name:
                self.component.textPlane.delChild(child)
                child.script = None

        return

    def handleMouseEvent(self, comp, event):
        if not self._isActive():
            return False
        if not self.selectionState and self.pressed:
            self._startSelection()
        if self.selectionState and not BigWorld.isKeyDown(KEY_LSHIFT) and not BigWorld.isKeyDown(KEY_RSHIFT):
            local = self.component.screenToLocal((event.cursorPosition[0], event.cursorPosition[1]))
            self._setCursorByMouse(local)
            self._renderSelection()
            return True
        return False

    def activate(self, doActivate = True, silent = False):
        if doActivate:
            if not self._isActive():
                self.active = doActivate
                BWPersonality.GUICore.registerCharacterReciever(self.component)
                self.runBlinker()
        else:
            self.active = doActivate
            BWPersonality.GUICore.unregisterCharacterReciever(self.component)
            self.stopBlinker()
            self.deselect()
        self.updateVisuals()
        if not silent:
            self.onActive(self._isActive())

    def _isActive(self):
        return self.active

    def onClick(self):
        self.activate()

    def onRClick(self):
        self.activate()

    def lostCharacterFeed(self):
        if self._isActive():
            self.activate(False)

    def getCharacterFeed(self):
        if not self._isActive():
            self.activate()

    def _updateScrolledState(self):
        self.component.textPlane.textRender.position.x = -self.hScrollOff
        self.component.textPlane.textRender.position.y = self.vScrollOff
        self.component.textPlane.cursor.position.x -= self.hScrollOff
        self.component.textPlane.cursor.position.y += self.vScrollOff

    def _setCursorByMouse(self, coords):
        stringNumber = int(ceil((coords.y + self.vScrollOff) / self.stringHeight))
        strWidth = 0
        charNumber = 0
        if stringNumber >= len(self.formattedText):
            stringNumber = len(self.formattedText) - 1
        if stringNumber < 0:
            stringNumber = 0
        if self._getTxtDims(self.formattedText[stringNumber])[0] < coords.x + self.hScrollOff:
            charNumber = len(self.formattedText[stringNumber])
        else:
            while strWidth < coords.x - self.component.textPlane.textRender.position.x:
                strWidth += self._getTxtDims(self.formattedText[stringNumber][charNumber])[0]
                charNumber += 1

            if charNumber > 0:
                charNumber -= 1
        if BigWorld.isKeyDown(KEY_LSHIFT) or BigWorld.isKeyDown(KEY_RSHIFT):
            if self.selectionAnchor is None:
                self._startSelection(True)
            else:
                self._startSelection(False)
        self.setCursor(stringNumber, charNumber)
        return

    def _scrollToCursor(self):
        hOff = self.component.textPlane.cursor.position.x + self.component.textPlane.cursor.width - self.component.textPlane.width
        if hOff > 0:
            self.hScrollOff = hOff
        else:
            self.hScrollOff = 0
        vOff = self.component.textPlane.cursor.position.y + self.component.textPlane.cursor.height - self.component.textPlane.height
        if vOff > 0:
            self.vScrollOff = vOff
        else:
            self.vScrollOff = 0
        self._updateScrolledState()

    def mouseHook(self, event):
        self.handleMouseEvent(self.component.textPlane, event)

    def handleMouseEnterEvent(self, component):
        BWPersonality.GUICore.mouseHook = lambda event: False
        return True

    def handleMouseLeaveEvent(self, component):
        if self.selectionAnchor is not None and self.pressed:
            BWPersonality.GUICore.mouseHook = self.mouseHook
            self._renderSelection()
        return True

    def copy(self):
        if not self.selectionAnchor:
            return
        else:
            startCoords = self.selectionAnchor
            stopCoords = self.cursor
            direction = 1
            if self.selectionAnchor[0] < self.cursor[0]:
                startCoords = self.cursor
                stopCoords = self.selectionAnchor
                direction = -1
            elif self.selectionAnchor[0] == self.cursor[0]:
                if self.selectionAnchor[1] > self.cursor[1]:
                    startCoords = self.cursor
                    stopCoords = self.selectionAnchor
                    direction = -1
            rawCharStart = self._getRawPosition(*startCoords)
            rawCharStop = self._getRawPosition(*stopCoords)
            if rawCharStop is None:
                rawCharStop = len(self.rawText)
            cpyTxt = self.rawText[rawCharStart:rawCharStop]
            if self.maskChar:
                cpyTxt = self.maskChar * len(cpyTxt)
            BigWorld.clipboardSetPlainText(cpyTxt)
            return

    def paste(self):
        clipText = BigWorld.clipboardGetPlainText()
        self.deleteSelection()
        self.addChar(clipText)
        self.setCursor(self.cursor[0], self.cursor[1] + len(clipText))
        self._renderText()

    def cut(self):
        self.copy()
        self.deleteSelection()

    def updateVisuals(self):
        if self._isActive():
            self.component.dFrame.texture = self.FRAME_ACTIVE
        else:
            self.component.dFrame.texture = self.FRAME_PASSIVE
        if self.erroneous:
            self.component.dFrame.texture = self.FRAME_ERROR

    def runBlinker(self):
        if self.blinker is None:
            self.blinker = self.cursorBlink()
            self.blinker.run()
        return

    def stopBlinker(self):
        if self.blinker:
            self.blinker.stop()
            self.blinker = None
        self.component.textPlane.cursor.visible = False
        return

    def runErrorNotify(self):
        if self.errorNotifier:
            self.errorNotifier.stop()
        self.errorNotifier = self.erroneousState(0.05)
        self.errorNotifier.run()

    def stopErrorNotify(self):
        if self.errorNotifier:
            self.errorNotifier.stop()
            self.errorNotifier = None
        self.erroneous = False
        self.updateVisuals()
        return

    def clear(self, byUser = True):
        self.rawText = u''
        self.formattedText = ['']
        self.deselect()
        self._renderText()
        self.setCursor(0, 0)
        self.onValueChange(byUser)

    def setValue(self, newText):
        self.clear()
        self.addChar(newText)
        self.setCursor(self.cursor[0], self.cursor[1] + len(newText))
        self._renderText()

    def fini(self):
        if self._isActive():
            BWPersonality.GUICore.unregisterCharacterReciever(self.component)
        BWPersonality.GUICore.mouseHook = lambda event: False
        self.stopBlinker()
        self.stopErrorNotify()

    def getValue(self):
        return self.formattedText

    def getRaw(self):
        return self.rawText

    def onActive(self, active):
        return None

    def onDefaultAction(self):
        return None

    def onValueChange(self, byUser):
        return None

    def onEscape(self):
        return None

    def onTab(self):
        return None

    def onPgUp(self):
        return None

    def onPgDn(self):
        return None

    @BWMemberCoroutine
    def cursorBlink(self, frequency = 0.25):
        self.component.textPlane.cursor.visible = True
        while self.active:
            yield BWWaitForPeriod(frequency)
            self.component.textPlane.cursor.visible = not self.component.textPlane.cursor.visible

        self.component.textPlane.cursor.visible = False
        self.blinker = None
        return

    @BWMemberCoroutine
    def erroneousState(self, lasting = 1.0):
        self.erroneous = True
        self.updateVisuals()
        yield BWWaitForPeriod(lasting)
        self.erroneous = False
        self.updateVisuals()
        self.errorNotifier = None
        return