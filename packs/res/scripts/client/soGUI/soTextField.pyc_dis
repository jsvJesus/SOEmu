# Embedded file name: scripts/client/soGUI/soTextField.py
import BWPersonality
import BigWorld
import GUI
import soGUI
import Helpers.PyGUI as PyGUI
from soGUI.soScrollBar import soScrollBar, soScrollBar2
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
from soGUI.soVisualStateComponent import soVisualStateComponent
from math import ceil
from math import floor
import time
from Helpers.BWCoroutine import *
from weakref import ref
import CallbackHelpers

class soTextField(PyGUIBase):
    factoryString = 'soGUI.soTextField'

    def __init__(self, component, fontName = 'ruRU_calibri_default.font', vertScrollNeed = True):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.textFrame = None
        self.vertScroll = None
        self.horzScroll = None
        self.verticalScrollNeed = vertScrollNeed
        self.horizontalScrollNeed = False
        self.scrollWidth = 20
        self.topOffset = 5
        self.leftOffset = 5
        self.frameTopOffset = 3
        self.frameLeftOffset = 3
        self.scrollOffset = 2
        self.textHeight = 0
        self.textWidth = 0
        self.lineOffset = 2
        self.wholeText = ''
        self.formatedText = []
        self.cursor = (0, 0)
        self.setupScrolls()
        self.setupFrame()
        self.fontName = fontName
        self.lineWidth = self.getLineWidth()
        self.lineHeight = self.getLineHeight()
        self.textLines = []
        self.numLines = 0
        self.setupLines()
        self.redrawText()
        self.maxScroll = 0
        return

    def getLineHeight(self):
        testString = GUI.Text('')
        testString.font = self.fontName
        retVal = testString.stringDimensions('A')[1]
        testString = None
        return retVal

    def getLineWidth(self):
        return self.textWidth - self.frameLeftOffset * 2

    def scrollUp(self):
        if self.cursor[1] > 0:
            self.cursor = (self.cursor[0], self.cursor[1] - 1)
            self.redrawText()
            self.vertScroll.doStep(False)

    def scrollDown(self):
        if self.cursor[1] < self.maxScroll:
            self.cursor = (self.cursor[0], self.cursor[1] + 1)
            self.redrawText()
            self.vertScroll.doStep()

    def addText(self, txt, newLine = True):
        if newLine:
            self.wholeText += '\n' + txt
        else:
            self.wholeText += txt
        self.redrawText()

    def delText(self):
        self.wholeText = ' '
        self.redrawText()

    def redrawText(self):
        txtLines = self.wholeText.splitlines()
        self.formatedText = []

        def formOneLine(txt):
            testString = GUI.Text('')
            testString.font = self.fontName
            symbols = ''
            for i in xrange(len(txt)):
                symbols += txt[i]
                if testString.stringDimensions(symbols)[0] > self.lineWidth:
                    testString = None
                    symbols = symbols[:-1] + '-'
                    return symbols

            testString = None
            return symbols

        def allocLine(txt):
            self.formatedText.append(txt)

        def applyLines():
            visibleText = []
            if len(self.formatedText) < self.numLines:
                maxLine = len(self.formatedText)
            else:
                maxLine = self.numLines
            for i in xrange(self.cursor[1], self.cursor[1] + maxLine):
                visibleText.append(self.formatedText[i])

            for i in xrange(len(visibleText)):
                self.textLines[i].text = visibleText[i]

        for i in xrange(len(txtLines)):
            formatedLine = formOneLine(txtLines[i])
            pos = len(formatedLine)
            if pos < len(txtLines[i]):
                pos -= 1
            while formatedLine:
                allocLine(formatedLine)
                formatedLine = formOneLine(txtLines[i][pos:])
                if len(formatedLine) + pos < len(txtLines[i]):
                    pos += len(formatedLine) - 1
                else:
                    pos += len(formatedLine)

        self.maxScroll = len(self.formatedText) - self.numLines
        applyLines()
        if self.vertScroll is not None:
            self.vertScroll.setupScrollingInfo(self.maxScroll)
        return

    def setupLines(self):
        self.numLines = int((self.textHeight - self.frameTopOffset * 2) / self.lineHeight)
        pixelWidth = soGUI.getPixelWidth(self.textFrame)
        pixelHeight = soGUI.getPixelHeight(self.textFrame)
        for i in xrange(self.numLines):
            line = GUI.Text('')
            line.verticalAnchor = 'TOP'
            line.horizontalAnchor = 'LEFT'
            line.horizontalPositionMode = 'CLIP'
            line.verticalPositionMode = 'CLIP'
            line.widthMode = 'PIXEL'
            line.heightMode = 'PIXEL'
            line.font = self.fontName
            line.colour = (155, 157, 71, 255)
            self.textLines.append(line)
            line.position = (-1.0 + pixelWidth * self.frameLeftOffset, 1.0 - pixelHeight * self.frameTopOffset - i * pixelHeight * self.lineHeight - pixelHeight * self.lineOffset, 0.0)
            self.textFrame.addChild(self.textLines[i], 'line' + str(i + 1))

    def setupFrame(self):
        self.textFrame = GUI.Window()
        self.textFrame.textureName = soGUI.TEXTFIELD_TEXTURE_TEXTFRAME
        self.textFrame.horizontalPositionMode = self.textFrame.verticalPositionMode = 'CLIP'
        self.textFrame.widthMode = self.textFrame.heightMode = 'PIXEL'
        self.textFrame.horizontalAnchor = 'LEFT'
        self.textFrame.verticalAnchor = 'TOP'
        self.textFrame.position = (-1.0 + soGUI.getPixelWidth(self.component) * self.leftOffset, 1.0 - soGUI.getPixelHeight(self.component) * self.topOffset, 0.0)
        if self.horzScroll is None:
            self.textHeight = self.textFrame.height = self.component.height - self.topOffset * 2
        if self.vertScroll is None:
            self.textWidth = self.textFrame.width = self.component.width - self.leftOffset * 2
        else:
            self.textWidth = self.textFrame.width = self.component.width - self.leftOffset * 2 - (self.vertScroll.component.width + self.scrollOffset)
        self.textFrame.visible = True
        self.component.addChild(self.textFrame, 'textFrame')
        self.doLayout()
        return

    def setupScrolls(self):
        self.vertScroll = soScrollBar(GUI.Window())
        self.vertScroll.component.verticalAnchor = 'TOP'
        self.vertScroll.component.horizontalAnchor = 'RIGHT'
        self.vertScroll.component.widthMode = 'PIXEL'
        self.vertScroll.component.heightMode = 'PIXEL'
        self.vertScroll.component.horizontalPositionMode = 'CLIP'
        self.vertScroll.component.verticalPositionMode = 'CLIP'
        self.vertScroll.component.width = 16
        self.vertScroll.component.height = 0
        self.vertScroll.component.position = (1.0 - soGUI.getPixelWidth(self.component) * self.leftOffset, 1.0 - soGUI.getPixelHeight(self.component) * self.topOffset, 0.0)
        self.vertScroll.initVSC('scripts/client/soGUI/schemas/soScrollBar_default.xml')
        self.vertScroll.setVisualState('normal')
        self.component.addChild(self.vertScroll.component, 'vScroll')
        self.vertScroll.component.visible = self.verticalScrollNeed

    def doLayout(self):
        if self.vertScroll is not None:
            self.vertScroll.component.height = self.textHeight
            self.vertScroll.makeLayout()
        if self.vertScroll is not None:
            self.vertScroll.component.position = (1.0 - soGUI.getPixelWidth(self.component) * self.leftOffset, 1.0 - soGUI.getPixelHeight(self.component) * self.topOffset, 0.0)
        if hasattr(self, 'textFrame'):
            self.textFrame.position = (-1.0 + soGUI.getPixelWidth(self.component) * self.leftOffset, 1.0 - soGUI.getPixelHeight(self.component) * self.topOffset, 0.0)
        if self.horzScroll is None:
            self.textHeight = self.textFrame.height = self.component.height - self.topOffset * 2
        if self.vertScroll is None:
            self.textWidth = self.textFrame.width = self.component.width - self.leftOffset * 2
        else:
            self.textWidth = self.textFrame.width = self.component.width - self.leftOffset * 2 - (self.vertScroll.component.width + self.scrollOffset)
        return

    @PyGUIEvent('vScroll', 'scrollUP')
    def scrolledUP(self):
        self.scrollUp()

    @PyGUIEvent('vScroll', 'scrollDN')
    def scrolledDN(self):
        self.scrollDown()


class soTextFieldVisualState(VisualState):

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


class soTxtFieldPropsStructure(object):

    def __init__(self, width = 300, height = 300, textureless = True, vScroll = True, hScroll = False, visualStyle = 'soGUI/visual_styles/defaultTextField.xml', scrollWidth = 16, font = 'ruRU_calibri_default.font', borderWidth = 3, autoSize = False, autoScroll = False, wordWarp = True, hideScroll = False):
        self.width = width
        self.height = height
        self.textureless = textureless
        self.vScroll = vScroll
        self.hScroll = hScroll
        self.visualStyle = visualStyle
        self.scrollWidth = scrollWidth
        self.font = font
        self.borderWidth = borderWidth
        self.autoSize = autoSize
        self.autoScroll = autoScroll
        self.wordWarp = wordWarp
        self.hideScroll = hideScroll


class soTextField2(PyGUIBase, soVisualStateComponent):
    factoryString = 'soGUI.soTextField2'
    visualStateString = 'soGUI.soTextFieldVisualState'

    def __init__(self, component, props = soTxtFieldPropsStructure()):
        PyGUIBase.__init__(self, component)
        soVisualStateComponent.__init__(self, component, self.visualStateString)
        component.script = self
        self.props = props
        self.frameComponent = None
        self.active = False
        self.disabled = False
        self.hovering = False
        self.pressed = False
        self.vScroll = None
        self.hScroll = None
        self.freshState = False
        self.cursor = (0, 0)
        self.maxScroll = 0
        self.trueText = ''
        self.formattedText = ''
        self.visualText = ''
        self.rawText = ''
        self.setupRoot()
        self.setupTextField()
        self.setupScrolls()
        self.initVSC(self.props.visualStyle)
        self.updateVisualState()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.props.width
        cmp.height = self.props.height if not self.props.autoSize else 0
        cmp.textureName = ''
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        if self.props.vScroll or self.props.hScroll:
            self.component.moveFocus = True
        self.component.crossFocus = True
        self.component.moveFocus = True

    def setupTextField(self):
        frameCmp = GUI.Frame2('')
        frameCmp.horizontalPositionMode = frameCmp.verticalPositionMode = 'PIXEL'
        frameCmp.widthMode = frameCmp.heightMode = 'PIXEL'
        frameCmp.horizontalAnchor = 'LEFT'
        frameCmp.verticalAnchor = 'TOP'
        frameCmp.width = self.props.width
        frameCmp.height = self.component.height
        frameCmp.position = (0, 0, 1.0)
        frameCmp.visible = not self.props.textureless
        self.frameComponent = frameCmp
        self.component.addChild(self.frameComponent, 'frameCmp')
        textRender = GUI.Text('')
        cmp = textRender
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = self.props.font
        cmp.colour = (255, 255, 255, 255)
        cmp.multiline = True
        cmp.colourFormatting = True
        cmp.position = (self.props.borderWidth, self.props.borderWidth, 0.5)
        self.component.addChild(cmp, 'textRender')

    def setupScrolls(self):
        if self.vScroll is None:
            scrollComp = GUI.Window()
            self.vScroll = soScrollBar2(scrollComp, width=self.props.scrollWidth, height=self.props.height - self.props.borderWidth * 2)
        cmp = self.vScroll.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (self.props.width - self.props.borderWidth, self.props.borderWidth, 0.2)
        cmp.visible = self.props.vScroll
        if self.props.vScroll:
            if not self.props.hideScroll:
                cmp.visible = True
            else:
                cmp.visible = False
        self.component.addChild(self.vScroll.component, 'vScroll')
        self.vScroll.setVisualState('normal')
        self.vScroll.onBound()
        return

    def updateScroll(self):
        strCount = self.formattedText.count('\n') + 1
        stringSize = self.component.textRender.stringDimensions(u'A')
        stringHeight = stringSize[1]
        renderHeight = self.component.frameCmp.height - self.props.borderWidth * 2
        numLines = floor(renderHeight / float(stringHeight))
        self.maxScroll = 0
        if strCount > numLines:
            self.maxScroll = strCount - numLines
        self.vScroll.setSteps(self.maxScroll)
        if self.props.hideScroll:
            if self.maxScroll <= 0:
                if self.vScroll.component.visible:
                    self.vScroll.component.visible = False
            elif not self.vScroll.component.visible:
                self.vScroll.component.visible = True
        if self.props.autoScroll and self.freshState:
            self.scrollToEnd()
            self.freshState = False

    def renderText(self):
        maxWidth = self.component.frameCmp.width - self.props.borderWidth * 2
        if self.props.vScroll:
            maxWidth -= self.props.scrollWidth
        self.visualText = ''
        formattedString = ''
        calculationsString = ''
        colourCodeIndex = -1
        buffer = ''
        w = 0
        for i in xrange(len(self.rawText)):
            if w > maxWidth:
                doWarp = self.props.wordWarp
                if formattedString.find(' ') < 0:
                    doWarp = False
                if not doWarp:
                    buffer = formattedString[-2:]
                    formattedString = formattedString[:-2]
                    formattedString += '-\n'
                    self.formattedText += formattedString
                    formattedString = ''
                    calculationsString = ''
                    colourCodeIndex = -1
                else:
                    spaceIndex = formattedString.rfind(' ')
                    if spaceIndex >= 0:
                        buffer = formattedString[spaceIndex + 1:]
                        formattedString = formattedString[:spaceIndex] + '\n'
                        self.formattedText += formattedString
                        formattedString = u''
                        calculationsString = u''
                        colourCodeIndex = -1
            if self.rawText[i] == '\\':
                if self.rawText[i + 1] == 'c':
                    colourCodeIndex = i
            formattedString += buffer
            formattedString += self.rawText[i]
            if colourCodeIndex < 0:
                calculationsString += buffer
                calculationsString += self.rawText[i]
            elif i not in xrange(colourCodeIndex, colourCodeIndex + 11):
                calculationsString += buffer
                calculationsString += self.rawText[i]
            buffer = ''
            w = self.component.textRender.stringWidth(calculationsString)

        if formattedString != '':
            self.formattedText += formattedString
        n = 0
        start = 0
        end = len(self.formattedText) - 1
        while n < self.cursor[1]:
            start = self.formattedText.find('\n', start, end)
            if start < 0:
                break
            else:
                n += 1
                start += 1

        firstIndex = start
        stringSize = self.component.textRender.stringDimensions(u'A')
        stringHeight = stringSize[1]
        h = self.component.frameCmp.height if not self.props.autoSize else self.props.height
        maxLines = floor((h - self.props.borderWidth * 2) / float(stringHeight))
        n = 0
        while n < maxLines:
            start = self.formattedText.find('\n', start, end)
            if start < 0:
                break
            else:
                start += 1
                n += 1

        lastIndex = start if start > 0 else len(self.formattedText)
        self.visualText = self.formattedText[firstIndex:lastIndex]
        self.component.textRender.text = self.visualText
        if self.props.autoSize:
            textSize = self.component.textRender.stringDimensions(self.component.textRender.text)
            tH = textSize[1] + self.props.borderWidth * 2
            if len(self.visualText) < len(self.formattedText):
                self.component.height = self.props.height
            else:
                self.component.height = tH
            self.component.frameCmp.height = self.component.height
            self.vScroll.setHeight(self.component.height - self.props.borderWidth * 2)
        self.rawText = ''

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

    def setText(self, txt):
        self.freshState = True
        self.trueText = txt
        self.rawText = txt
        self.formattedText = ''
        self.renderText()
        self.updateScroll()

    def addText(self, txt, newLine = True):
        self.freshState = True
        self.rawText = txt
        self.trueText += txt if not newLine else '\n' + txt
        if newLine:
            self.formattedText += '\n'
        self.renderText()
        self.updateScroll()

    def getHeight(self):
        return self.component.frameCmp.height

    def getWidth(self):
        return self.component.frameCmp.width

    def getTxtWidth(self):
        w, h = self.component.textRender.stringDimensions(self.component.textRender.text)
        return w + self.props.borderWidth * 2

    def setWidth(self, newWidth):
        oldText = self.trueText
        self.setText(u'')
        self.props.width = newWidth
        self.component.width = newWidth
        self.vScroll.component.position.x = newWidth - self.props.borderWidth
        self.component.frameCmp.width = newWidth
        self.setText(oldText)

    def clear(self):
        self.setText(u'')

    def handleMouseEnterEvent(self, comp):
        self.hovering = True
        self.updateVisualState()
        return True

    def handleMouseLeaveEvent(self, comp):
        self.hovering = False
        self.updateVisualState()
        return True

    def handleMouseEvent(self, cmp, event):
        dx = event.dx
        dy = event.dy
        dz = event.dz
        position = event.cursorPosition
        if dz > 0:
            self.scrollUp()
            return True
        if dz < 0:
            self.scrollDown()
            return True
        return False

    def scrollUp(self):
        if not self.props.vScroll:
            return
        if self.cursor[1] > 0:
            self.cursor = (self.cursor[0], self.cursor[1] - 1)
            self.renderText()
            self.vScroll.setValue(self.cursor[1])

    def scrollDown(self):
        if not self.props.vScroll:
            return
        elif self.cursor[1] < self.maxScroll:
            self.cursor = (self.cursor[0], self.cursor[1] + 1)
            self.renderText()
            self.vScroll.setValue(self.cursor[1])
            return True
        else:
            return False

    def scrollToEnd(self):
        if not self.props.vScroll:
            return
        self.cursor = (self.cursor[0], self.maxScroll)
        self.vScroll.setValue(self.maxScroll)
        self.renderText()

    def scrollToTop(self):
        if not self.props.vScroll:
            return
        self.cursor = (self.cursor[0], 0)
        self.vScroll.setValue(0)
        self.renderText()

    @PyGUIEvent('vScroll', 'scrollMoved')
    def scrollMoved(self, newVal):
        self.cursor = (self.cursor[0], newVal)
        self.renderText()
        self.vScroll.setValue(newVal)

    @PyGUIEvent('vScroll', 'scrollUp')
    def scrolledUP(self):
        self.scrollUp()

    @PyGUIEvent('vScroll', 'scrollDown')
    def scrolledDN(self):
        self.scrollDown()


class TxtToken(object):
    TOKENTYPE_TEXT = 0
    TOKENTYPE_PICTURE = 1
    TOKENTYPE_HLINK = 2
    TOKENTYPE_FONT = 3
    TOKENTYPE_COLOR = 4
    TOKENTYPE_NEWLINE = 5
    TOKENTYPE_PARAGRAPH = 6
    TOKENTYPE_DYNAMIC = 7
    TOKENTYPE_ALIGNMENT = 8

    def __init__(self, tokenType = TOKENTYPE_TEXT, occurrence = 0, data = None, raw = u''):
        self.tokenType = tokenType
        self.tokenData = data
        self.occurrence = occurrence
        self.rawData = raw


class soTextField3(PyGUIBase):
    factoryString = 'soGUI.soTextField3'
    TAG_HYPERLINK = 'hlink'
    TAG_COLOR = 'color'
    TAG_FONT = 'font'
    TAG_PICTURE = 'img'
    TAG_PARAGRAPH = 'p'
    TAG_NEWLINE = 'n'
    TAG_DYNAMICDATA = 'dyn'
    TAG_ALIGNMENT = u'alignment'
    CHAR_TAGOPEN = '<'
    CHAR_TAGCLOSE = '>'
    SHORTEST_TAG_LEN = 1
    LONGEST_TAG_LEN = 9
    PROPS_TAGS = [TAG_COLOR,
     TAG_FONT,
     TAG_ALIGNMENT,
     TAG_NEWLINE,
     TAG_PARAGRAPH]
    CONTENT_TAGS = [TAG_HYPERLINK, TAG_PICTURE, TAG_DYNAMICDATA]
    TAGS = [TAG_HYPERLINK,
     TAG_COLOR,
     TAG_FONT,
     TAG_PICTURE,
     TAG_PARAGRAPH,
     TAG_NEWLINE,
     TAG_DYNAMICDATA,
     TAG_ALIGNMENT]
    MINIMUM_WIDTH = 16
    MINIMUM_HEIGHT = 16
    MIN_RENDER_THRESHHOLD = 0.15
    DEFAULT_PIC_WIDTH = 50
    DEFAULT_PIC_HEIGHT = 20
    DEFAULT_FONT = 'ruRU_Cyrvetica_Extra_14i.font'
    DEFAULT_ALIGNMENT = 'left'
    DEFAULT_COLOR = [255,
     255,
     255,
     255]
    RENDERMODE_VSCROLL = 1
    RENDERMODE_HSCROLL = 2

    def __init__(self, component, width = 100, height = 50, textWidth = 200, hScroll = True, vScroll = True, hideScroll = True, borderWidth = 1, vOffset = 1, hOffset = 1, textureless = False, autosize = False, readOnly = True, canSelect = False, maxAppends = -1):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.rawText = u''
        self.formattedText = []
        self.textData = ''
        self.scrollCursor = [0, 0]
        self.cursor = [0, 0]
        self.nMap = [0]
        self.hMap = []
        self.appendMap = []
        self.cutOffset = 0
        self.fontMap = {}
        self.alignMap = {}
        self.colorMap = {}
        self.txtConverterTaskQueue = []
        self.unscrollableAreas = [0, 0]
        self.autosize = autosize
        self.readOnly = readOnly
        self.canSelect = canSelect
        self.maxAppends = maxAppends
        self.width = width
        self.height = height
        self.maxWidth = 0
        self.widthLimit = width
        self.testTGC = GUI.Text('')
        self.testTGC.colourFormatting = False
        self.testTGC.multiline = False
        self.hScroll = hScroll
        self.vScroll = vScroll
        if self.autosize:
            self.hScroll = False
            self.vScroll = False
        self.hideScroll = hideScroll
        self.borderWidth = borderWidth
        self.vOffset = vOffset
        self.hOffset = hOffset
        self.texturless = textureless
        if textWidth > 0:
            self.textWidth = textWidth
            self.fitToRenderPlane = False
        else:
            self.textWidth = self.width - self.borderWidth * 2 - self.hOffset * 2
            self.fitToRenderPlane = True
        self.maxScroll = [0, 0]
        self.tokenPosCache = {}
        self.setupRoot()
        self.setupTextPlane()
        self.setupScrolls()
        self._refitCmps()

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.width
        cmp.height = self.height

    def setupTextPlane(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = self.width - self.borderWidth * 2 - self.hOffset * 2
        cmp.height = self.height - self.borderWidth * 2 - self.vOffset * 2
        cmp.position = (self.borderWidth + self.hOffset, self.borderWidth + self.vOffset, 0.5)
        cmp.textureName = ''
        self.component.addChild(cmp, 'textRendererPlane')

    def setupScrolls(self):
        vSHeight = self.height - self.borderWidth * 2 if not self.hScroll else self.height - self.borderWidth * 2 - 16
        scroll = soScrollBar2(GUI.Window(), width=16, height=vSHeight, sendOnMove=True)
        cmp = scroll.component
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.visible = False
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (self.width - self.borderWidth, self.borderWidth, 0.6)
        self.component.addChild(cmp, 'vScroll')
        scroll.setVisualState('normal')
        scroll.onBound()
        hSHeight = self.height - self.borderWidth * 2 if not self.vScroll else self.width - self.borderWidth * 2 - 16
        scroll = soScrollBar2(GUI.Window(), width=16, height=hSHeight, horizontal=True, sendOnMove=True)
        cmp = scroll.component
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.visible = False
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (self.borderWidth, self.height - self.borderWidth, 0.6)
        self.component.addChild(cmp, 'hScroll')
        scroll.setVisualState('normal')
        scroll.onBound()

    def _refitCmps(self):
        if self.autosize:
            self.width = self.maxWidth
            if len(self.hMap) > 0:
                self.height = self.hMap[-1]
        cmp = self.component.textRendererPlane
        self.component.width = self.width
        self.component.height = self.height
        dW = self.width - self.borderWidth * 2 - self.hOffset * 2
        dH = self.height - self.borderWidth * 2 - self.vOffset * 2
        if self.vScroll and not self.hideScroll:
            dW -= 18
        if self.hScroll and not self.hideScroll:
            dH -= 18
        cmp.width = dW
        cmp.height = dH
        if self.maxScroll[1] > 0 and self.vScroll:
            self.component.vScroll.visible = True
            cmp.width = dW - self.component.vScroll.width
        else:
            self.component.vScroll.visible = False
        if self.maxScroll[0] > 0 and self.hScroll:
            self.component.hScroll.visible = True
            cmp.height = dW - self.component.hScroll.width
        if self.vScroll and not self.hideScroll:
            self.component.vScroll.visible = True
        if self.hScroll and not self.hideScroll:
            self.component.hScroll.visible = True
        if self.fitToRenderPlane and not self.autosize:
            if self.textWidth != cmp.width:
                self._setTextWidth(cmp.width)
        if self.component.vScroll.visible:
            if self.component.hScroll.visible:
                self.component.vScroll.script.setHeight(self.component.height - self.component.hScroll.width)
            else:
                self.component.vScroll.script.setHeight(self.component.height)
        if self.component.hScroll.visible:
            if self.component.vScroll.visible:
                self.component.hScroll.script.setHeight(self.component.width - self.component.vScroll.width)
            else:
                self.component.hScroll.script.setHeight(self.component.width)

    def setHeight(self, h):
        self.height = h
        if self.vScroll:
            self.component.vScroll.script.setHeight(self.component.height)
        self._recalcScrolls()
        self._checkCursor()
        CallbackHelpers.callback(self.renderText, self.MIN_RENDER_THRESHHOLD, cancel_existing=True)

    def _recalcScrolls(self):
        maxHeight = self.height - self.borderWidth * 2 - self.vOffset * 2
        if len(self.hMap) < 1:
            self.maxScroll[1] = 0
            self.component.vScroll.script.setSteps(self.maxScroll[1])
            self._checkCursor()
            return
        if self.hMap[-1] <= maxHeight:
            self.maxScroll[1] = 0
            self.component.vScroll.script.setSteps(self.maxScroll[1])
            self._checkCursor()
            return
        lineIdx = 0
        while self.hMap[lineIdx] < maxHeight:
            lineIdx += 1

        self.maxScroll[1] = len(self.hMap) - lineIdx
        self.component.vScroll.script.setSteps(self.maxScroll[1])
        self._checkCursor()

    def _checkCursor(self):
        if self.scrollCursor[0] > self.maxScroll[0]:
            self.scrollCursor[0] = self.maxScroll[0]
        if self.scrollCursor[1] > self.maxScroll[1]:
            self.scrollCursor[1] = self.maxScroll[1]

    def _getFont(self, pos):
        pos += self.cutOffset
        if len(self.fontMap) < 1:
            return self.DEFAULT_FONT
        posMap = self.fontMap.keys()
        bestPos = posMap[0]
        for p in posMap:
            if p <= pos:
                if pos - bestPos < 0:
                    bestPos = p
                if abs(p - pos) < abs(bestPos - pos):
                    bestPos = p

        return self.fontMap[bestPos].tokenData[0]

    def _getColor(self, pos):
        pos += self.cutOffset
        if len(self.colorMap) < 1:
            return self.DEFAULT_COLOR
        if self.colorMap.has_key(pos):
            return self.colorMap[pos].tokenData
        posMap = self.colorMap.keys()
        bestPos = posMap[0]
        for p in posMap:
            if p <= pos:
                if pos - bestPos < 0:
                    bestPos = p
                if abs(p - pos) < abs(bestPos - pos):
                    bestPos = p

        return self.colorMap[bestPos].tokenData

    def _getAlignment(self, pos):
        pos += self.cutOffset
        if len(self.alignMap) < 1:
            return self.DEFAULT_ALIGNMENT
        posMap = self.alignMap.keys()
        bestPos = posMap[0]
        for p in posMap:
            if p <= pos:
                if pos - bestPos < 0:
                    bestPos = p
                if abs(p - pos) < abs(bestPos - pos):
                    bestPos = p

        return self.alignMap[bestPos].tokenData[0]

    def _buildToken(self, input, occurrence = 0):
        if len(input[1:-1]) < self.SHORTEST_TAG_LEN or input[0] != self.CHAR_TAGOPEN or input[-1] != self.CHAR_TAGCLOSE:
            print 'incorrect token'
            print 'input was', input
            print 'occurance is', occurrence
            return
        else:
            retVal = None
            closingChar = input.find('=', 1)
            if closingChar < 0:
                closingChar = input.find('>')
            tagStr = input[1:closingChar]
            for tag in self.TAGS:
                if tagStr == tag:
                    if tag is self.TAG_HYPERLINK:
                        dlm1 = input.find(';', 7, -1)
                        dlm2 = input.find(';', dlm1 + 1, -1)
                        visText = input[7:dlm1]
                        linkID = input[dlm1 + 1:dlm2]
                        visStyle = input[dlm2 + 1:-1]
                        if visStyle not in ('normal', 'color', 'textlike'):
                            visStyle = 'normal'
                        data = [visText, linkID, visStyle]
                        retVal = TxtToken(tag, occurrence, data, input)
                    elif tag is self.TAG_PICTURE:
                        dlm1 = input.find(';', 5, -1)
                        dlm2 = input.find(';', dlm1 + 1, -1)
                        tName = input[5:dlm1]
                        w = input[dlm1 + 1:dlm2]
                        if not w.isdigit():
                            print 'warning: picture tag contains invalid width, setting to default'
                            print 'input was:', input
                            w = self.DEFAULT_PIC_WIDTH
                        h = input[dlm2 + 1:-1]
                        if not h.isdigit():
                            print 'warning: picture tag contains invalid height, setting to default'
                            print 'input was:', input
                            h = self.DEFAULT_PIC_HEIGHT
                        data = [tName, w, h]
                        retVal = TxtToken(tag, occurrence, data, input)
                    elif tag is self.TAG_ALIGNMENT:
                        alType = input[11:-1]
                        if alType not in ('left', 'center', 'right'):
                            print 'warning: invalid alignment was specified, setting to left'
                            print 'input was:', input
                            alType = 'left'
                        data = [alType]
                        retVal = TxtToken(tag, occurrence, data, input)
                    elif tag is self.TAG_COLOR:
                        r = input[7:10]
                        if not r.isdigit():
                            print 'warning: incorrect data in color tag, setting red value to zero'
                            print 'input was:', input
                            r = '000'
                        g = input[10:13]
                        if not g.isdigit():
                            print 'warning: incorrect data in color tag, setting green value to zero'
                            print 'input was:', input
                            g = '000'
                        b = input[13:16]
                        if not b.isdigit():
                            print 'warning: incorrect data in color tag, setting blue value to zero'
                            print 'input was:', input
                            b = '000'
                        a = input[16:19]
                        if not a.isdigit():
                            print 'warning: incorrect data in color tag, setting alpha value to zero'
                            print 'input was:', input
                            a = '000'
                        data = [int(r),
                         int(g),
                         int(b),
                         int(a)]
                        retVal = TxtToken(tag, occurrence, data, input)
                    elif tag is self.TAG_FONT:
                        fName = input[6:-1]
                        data = [fName]
                        retVal = TxtToken(tag, occurrence, data, input)
                    elif tag is self.TAG_DYNAMICDATA:
                        tpID = input[5:-1]
                        data = [tpID]
                        retVal = TxtToken(tag, occurrence, data, input)
                    elif tag is self.TAG_NEWLINE:
                        data = None
                        retVal = TxtToken(tag, occurrence, data, input)
                    elif tag is self.TAG_PARAGRAPH:
                        data = None
                        retVal = TxtToken(tag, occurrence, data, input)
                if retVal is not None:
                    return retVal

            return retVal

    def _parseStr(self, input, offset = 0):
        firstOccurrence = offset
        output = []
        cur = 0
        plainText = ''
        while cur < len(input):
            if input[cur] == self.CHAR_TAGOPEN:
                idx = cur
                while idx < len(input) and input[idx] != self.CHAR_TAGCLOSE:
                    idx += 1

                if idx <= len(input):
                    tagStr = input[cur:idx + 1]
                    token = self._buildToken(tagStr, firstOccurrence + cur)
                    if isinstance(token, TxtToken):
                        output.append(token)
                        plainText += ' ' * len(tagStr)
                    else:
                        plainText += tagStr
                    cur = idx + 1
            else:
                plainText += input[cur]
                cur += 1

        output.append(plainText)
        return output

    def _recalcPropsMap(self):
        propsMap = self._calculatePropsMap(self.rawText, 0)
        self.fontMap = propsMap[0]
        self.alignMap = propsMap[1]
        self.colorMap = propsMap[2]

    def _recalcNMap(self):
        self.nMap = [self.cutOffset]
        self.nMap += self._calculateNMap(self.rawText, 0, False)

    def _calculatePropsMap(self, input, offset = -1):
        if offset < 0:
            offset = len(self.rawText)
        fontMap = {}
        alignMap = {}
        colorMap = {}
        parserData = self._parseStr(input, offset)
        for token in parserData[:-1]:
            if token.tokenType is self.TAG_FONT:
                fontMap[token.occurrence] = token
            elif token.tokenType is self.TAG_ALIGNMENT:
                alignMap[token.occurrence] = token
            elif token.tokenType is self.TAG_COLOR:
                colorMap[token.occurrence] = token

        output = [fontMap, alignMap, colorMap]
        return output

    def _recalcHMap(self, start):
        if len(self.nMap) < 1 or not self.rawText:
            return
        self.hMap = self.hMap[:start]
        parserData = self._parseStr(self.rawText[self.nMap[start]:], self.nMap[start])
        lineIdx = start
        hMap = []
        if len(self.hMap) > 0:
            cH = self.hMap[start - 1]
        else:
            cH = 0
        currentFont = self._getFont(self.nMap[start])
        while lineIdx < len(self.nMap):
            rawLine = u''
            if lineIdx + 1 >= len(self.nMap):
                rawLine = self.rawText[self.nMap[lineIdx]:len(self.rawText)]
            else:
                rawLine = self.rawText[self.nMap[lineIdx]:self.nMap[lineIdx + 1]]
            parserData = self._parseStr(rawLine, self.nMap[lineIdx])
            tokens = parserData[0:-1]
            lineDims = self._getTxtDims('W', currentFont)
            for token in tokens:
                if token.tokenType is self.TAG_FONT:
                    currentFont = token.tokenData[0]
                    lH = self._getTxtDims('W', currentFont)[1]
                    if lH > lineDims[1]:
                        lineDims[1] = lH
                else:
                    tH = self._getTokenDims(token)[1]
                    if tH > lineDims[1]:
                        lineDims[1] = tH

            cH += lineDims[1]
            hMap.append(cH)
            lineIdx += 1

        self.hMap += hMap

    def _calculateNMap(self, input, offset = -1, newLine = True):
        output = []
        if offset < 0:
            offset = len(self.rawText) + self.cutOffset
        if offset > 0 and not newLine:
            offset += self.cutOffset
            trailingStr = self.rawText[self.nMap[-1]:len(self.rawText)]
            if trailingStr[-3:] != u'<n>':
                input = trailingStr + input
                offset -= len(trailingStr)
        if offset == 0:
            offset += self.cutOffset
        parserData = self._parseStr(input, offset)
        tokens = {}
        fonts = {}
        plainText = parserData[-1]
        for token in parserData[0:-1]:
            tokens[token.occurrence] = token

        for token in parserData[0:-1]:
            if token.tokenType is self.TAG_NEWLINE:
                if self.nMap.count(token.occurrence) == 0:
                    output.append(token.occurrence)
            elif token.tokenType is self.TAG_PARAGRAPH:
                if token.occurrence > 0:
                    output.append(token.occurrence)
            elif token.tokenType is self.TAG_DYNAMICDATA:
                if token.occurrence > 0:
                    output.append(token.occurrence)
            elif token.tokenType is self.TAG_FONT:
                fonts[token.occurrence] = token.tokenData[0]

        cur = 0
        currentFont = self._getFont(offset)
        strWidth = 0
        lastWS = -1
        lastWSW = -1
        while cur < len(input):
            if cur + offset in fonts:
                currentFont = fonts[cur + offset]
            if tokens.has_key(cur + offset):
                if self.autosize:
                    if tokens[cur + offset].tokenType in [self.TAG_NEWLINE, self.TAG_PARAGRAPH, self.TAG_DYNAMICDATA]:
                        if strWidth > self.maxWidth:
                            self.maxWidth = strWidth
                        strWidth = 0
                    else:
                        strWidth += self._getTokenDims(tokens[cur + offset])[0]
                    cur += len(tokens[cur + offset].rawData)
                    continue
                else:
                    if tokens[cur + offset].tokenType in [self.TAG_NEWLINE, self.TAG_PARAGRAPH, self.TAG_DYNAMICDATA]:
                        strWidth = 0
                        lastWS = -1
                        cur += len(tokens[cur + offset].rawData)
                        continue
                    if strWidth + self._getTokenDims(tokens[cur + offset])[0] >= self.textWidth:
                        if strWidth == 0:
                            cur += len(tokens[cur + offset].rawData)
                            lastWS = -1
                            output.append(offset + cur)
                            continue
                        else:
                            output.append(offset + cur)
                            lastWS = -1
                            strWidth = 0
                            continue
                    else:
                        strWidth += self._getTokenDims(tokens[cur + offset])[0]
                        cur += len(tokens[cur + offset].rawData)
                        continue
            charWidth = 0
            if cur < len(input):
                charWidth = self._getTxtDims(input[cur], currentFont)[0]
                if input[cur] == u' ':
                    lastWS = cur
                    lastWSW = strWidth + charWidth
            if self.autosize:
                if cur == len(input) - 1:
                    if strWidth + charWidth > self.maxWidth:
                        self.maxWidth = strWidth + charWidth
                if strWidth + charWidth < self.widthLimit:
                    strWidth += charWidth
                elif lastWS > 0:
                    cur = lastWS + 1
                    if strWidth > self.maxWidth:
                        self.maxWidth = strWidth
                    strWidth = 0
                    lastWS = -1
                    output.append(offset + cur)
                    continue
                else:
                    output.append(offset + cur)
                    if strWidth > self.maxWidth:
                        self.maxWidth = strWidth
                    strWidth = charWidth
                    lastWS = -1
                cur += 1
                continue
            if strWidth + charWidth < self.textWidth:
                strWidth += charWidth
            elif lastWS > 0:
                cur = lastWS + 1
                strWidth = 0
                lastWS = -1
                output.append(offset + cur)
                continue
            else:
                output.append(offset + cur)
                strWidth = charWidth
                lastWS = -1
            cur += 1

        output.sort()
        return output

    def _getTxtDims(self, txt, font = DEFAULT_FONT):
        self.testTGC.font = font
        return list(self.testTGC.stringDimensions(txt))

    def _getTokenDims(self, token):
        dims = None
        if not isinstance(token, TxtToken):
            return dims
        elif token.tokenType is self.TAG_NEWLINE or token.tokenType is self.TAG_PARAGRAPH:
            self.testTGC.font = self._getFont(token.occurrence)
            dims = [0, self.testTGC.stringDimensions('W')[1]]
            return dims
        elif token.tokenType in self.PROPS_TAGS:
            dims = [0, 0]
            return dims
        else:
            if token.tokenType is self.TAG_PICTURE:
                dims = [int(token.tokenData[1]), int(token.tokenData[2])]
            elif token.tokenType is self.TAG_HYPERLINK:
                self.testTGC.font = self._getFont(token.occurrence)
                dims = list(self.testTGC.stringDimensions(token.tokenData[0]))
            elif token.tokenType is self.TAG_DYNAMICDATA:
                self.testTGC.font = self._getFont(token.occurrence)
                dims = [self.textWidth, self.testTGC.stringDimensions('W')[1]]
            return dims

    def _buildTokenManifestation(self, rawData, offset = 0):
        token = self._buildToken(rawData, offset)
        cmp = None
        if token.tokenType is self.TAG_PICTURE:
            cmp = GUI.Simple(token.tokenData[0])
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.width = int(token.tokenData[1])
            cmp.height = int(token.tokenData[2])
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
        if token.tokenType is self.TAG_HYPERLINK:
            from soHyperLinkComponent import soHyperLinkComponent
            cmp = GUI.Text('')
            cmp.font = self._getFont(token.occurrence)
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.colourFormatting = False
            cmp.multiline = False
            cmp.text = token.tokenData[0]
            hlink = soHyperLinkComponent(cmp)
            hlink.initVSC('soGUI/visual_styles/hlink_default.xml')
            hlink.setVisualState('normal')
            hlink.setToolTip(token.tokenData[1], None)
            hlink.setID(token.tokenData[1])
        return cmp

    def _buildTextManifestation(self, txt, font = DEFAULT_FONT, color = DEFAULT_COLOR, alignment = DEFAULT_ALIGNMENT):
        cmp = GUI.Text('')
        cmp.font = font
        cmp.colour = tuple(color)
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.colourFormatting = False
        cmp.multiline = False
        cmp.text = txt
        return cmp

    def _getLineIdx(self, lineN):
        try:
            return self.nMap[lineN] - self.cutOffset
        except IndexError:
            print 'soTextField ERROR::_getLineIdx IndexError ', lineN
            return 0

    def renderText(self):
        self.clearAllChildren(self.component.textRendererPlane)
        visHeight = 0
        maxHeight = self.height - self.vOffset * 2 - self.borderWidth * 2
        lineIdx = self.scrollCursor[1]
        currentFont = self._getFont(self._getLineIdx(lineIdx))
        currentColor = self._getColor(self._getLineIdx(lineIdx))
        completed = False
        while visHeight < maxHeight and not completed:
            rawLine = u''
            if lineIdx + 1 >= len(self.nMap):
                rawLine = self.rawText[self._getLineIdx(lineIdx):]
                completed = True
            else:
                rawLine = self.rawText[self._getLineIdx(lineIdx):self._getLineIdx(lineIdx + 1)]
            parserData = self._parseStr(rawLine, self._getLineIdx(lineIdx))
            visualTokens = {}
            fonts = {}
            colors = {}
            aligns = {}
            skips = {}
            plainText = parserData[-1]
            cur = 0
            firstCharIdx = self._getLineIdx(lineIdx)
            lineWidth = 0
            lineDims = [0, 0]
            buffer = u''
            alignment = self._getAlignment(firstCharIdx)
            toAttach = []
            for token in parserData[0:-1]:
                if token.tokenType == self.TAG_NEWLINE:
                    lineDims[1] = self._getTokenDims(token)[1]
                if token.tokenType in self.CONTENT_TAGS:
                    visualTokens[token.occurrence] = token
                elif token.tokenType == self.TAG_FONT:
                    fonts[token.occurrence] = token
                elif token.tokenType == self.TAG_COLOR:
                    colors[token.occurrence] = token
                elif token.tokenType is self.TAG_ALIGNMENT:
                    aligns[token.occurrence] = token
                else:
                    skips[token.occurrence] = token

            while cur < len(rawLine):
                if skips.has_key(firstCharIdx + cur):
                    w, h = self._getTokenDims(skips[firstCharIdx + cur])
                    cur += len(skips[firstCharIdx + cur].rawData)
                    if h > lineDims[1]:
                        lineDims[1] = h
                    continue
                if visualTokens.has_key(firstCharIdx + cur):
                    if len(buffer) > 0:
                        cmp = self._buildTextManifestation(buffer.strip(), currentFont, currentColor, alignment)
                        cmp.position = (lineDims[0], 0, 0.5)
                        w, h = cmp.stringDimensions(cmp.text)
                        lineDims[0] += w
                        if h > lineDims[1]:
                            lineDims[1] = h
                        toAttach.append(cmp)
                        buffer = ''
                    cmp = self._buildTokenManifestation(visualTokens[firstCharIdx + cur].rawData, firstCharIdx + cur)
                    if cmp:
                        cmp.position = (lineDims[0], 0, 0.5)
                        toAttach.append(cmp)
                    w, h = self._getTokenDims(visualTokens[firstCharIdx + cur])
                    cur += len(visualTokens[firstCharIdx + cur].rawData)
                    lineDims[0] += w
                    if h > lineDims[1]:
                        lineDims[1] = h
                    continue
                if fonts.has_key(firstCharIdx + cur):
                    if len(buffer) > 0:
                        cmp = self._buildTextManifestation(buffer.strip(), currentFont, currentColor, alignment)
                        cmp.position = (lineDims[0], 0, 0.5)
                        w, h = cmp.stringDimensions(cmp.text)
                        lineDims[0] += w
                        if h > lineDims[1]:
                            lineDims[1] = h
                        toAttach.append(cmp)
                        currentFont = fonts[firstCharIdx + cur].tokenData
                        cur += len(fonts[firstCharIdx + cur].rawData)
                        buffer = ''
                    else:
                        currentFont = fonts[firstCharIdx + cur].tokenData
                        cur += len(fonts[firstCharIdx + cur].rawData)
                    continue
                if colors.has_key(firstCharIdx + cur):
                    if len(buffer) > 0:
                        cmp = self._buildTextManifestation(buffer.strip(), currentFont, currentColor, alignment)
                        cmp.position = (lineDims[0], 0, 0.5)
                        w, h = cmp.stringDimensions(cmp.text)
                        lineDims[0] += w
                        if h > lineDims[1]:
                            lineDims[1] = h
                        toAttach.append(cmp)
                        currentColor = colors[firstCharIdx + cur].tokenData
                        cur += len(colors[firstCharIdx + cur].rawData)
                        buffer = ''
                    else:
                        currentColor = colors[firstCharIdx + cur].tokenData
                        cur += len(colors[firstCharIdx + cur].rawData)
                    continue
                if aligns.has_key(firstCharIdx + cur):
                    if len(buffer) > 0:
                        cmp = self._buildTextManifestation(buffer.strip(), currentFont, currentColor, alignment)
                        cmp.position = (lineDims[0], 0, 0.5)
                        w, h = cmp.stringDimensions(cmp.text)
                        lineDims[0] += w
                        if h > lineDims[1]:
                            lineDims[1] = h
                        toAttach.append(cmp)
                        alignment = aligns[firstCharIdx + cur].tokenData[0]
                        cur += len(aligns[firstCharIdx + cur].rawData)
                        buffer = ''
                    else:
                        alignment = aligns[firstCharIdx + cur].tokenData[0]
                        cur += len(aligns[firstCharIdx + cur].rawData)
                    continue
                if cur < len(rawLine):
                    buffer += rawLine[cur]
                cur += 1

            if visHeight + lineDims[1] > maxHeight:
                return
            if len(buffer) > 0:
                cmp = self._buildTextManifestation(buffer.strip(), currentFont, currentColor, alignment)
                cmp.position = (lineDims[0], 0, 0.5)
                w, h = cmp.stringDimensions(cmp.text)
                lineDims[0] += w
                if h > lineDims[1]:
                    lineDims[1] = h
                toAttach.append(cmp)
            lineOffset = 0
            if alignment == 'left':
                lineOffset = 0
            elif alignment == 'right':
                lineOffset = self.textWidth - lineDims[0]
            elif alignment == 'center':
                lineOffset = (self.textWidth - lineDims[0]) / 2
            for cmp in toAttach:
                cmp.position.x += lineOffset
                cmp.position.y = visHeight + lineDims[1]
                self.component.textRendererPlane.addChild(cmp)

            visHeight += lineDims[1]
            lineIdx += 1

    def setText(self, text):
        self.maxWidth = 0
        task = []
        task.append('SET')
        task.append(self.replaceNewLines(text))
        try:
            self._addTask(task)
        except:
            print 'soTextField crash here'
            import traceback
            traceback.print_exc()

    def addText(self, text, newLine = True):
        task = []
        task.append('ADD')
        task.append(self.replaceNewLines(text))
        task.append(newLine)
        try:
            self._addTask(task)
        except:
            print 'soTextField crash here'
            import traceback
            traceback.print_exc()

    def setSize(self, w, h):
        recalcVS = False
        self.width = w
        if h != self.height:
            self.height = h
            recalcVS = True
        self._refitCmps()
        if recalcVS:
            self._recalcScrolls()

    def setCursor(self, h = 0, v = 0):
        self.scrollCursor[0] = h
        self.scrollCursor[1] = v
        self._checkCursor()
        self.component.vScroll.script.setValue(self.scrollCursor[1])
        self.component.hScroll.script.setValue(self.scrollCursor[0])
        CallbackHelpers.callback(self.renderText, self.MIN_RENDER_THRESHHOLD, cancel_existing=True)

    def setTextWidth(self, w):
        self.textWidth = w
        self.fitToRenderPlane = False
        self._recalcNMap()
        self._recalcHMap(0)
        self._recalcScrolls()
        CallbackHelpers.callback(self.renderText, self.MIN_RENDER_THRESHHOLD, cancel_existing=True)

    def _setTextWidth(self, w):
        self.textWidth = w
        self._recalcNMap()
        self._recalcHMap(0)
        self._recalcScrolls()
        CallbackHelpers.callback(self.renderText, self.MIN_RENDER_THRESHHOLD, cancel_existing=True)

    def scrollTo(self, scroll = [0, 0]):
        self.setCursor(scroll[0], scroll[1])

    def getMaxScroll(self):
        return self.maxScroll

    def replaceNewLines(self, text):
        return text.replace('\n', u'<n>')

    def _newAppend(self, appendPos):
        self.appendMap.append(appendPos + self.cutOffset)
        cutLen = 0
        if len(self.appendMap) > self.maxAppends:
            del self.appendMap[0]
            cutLen = self.appendMap[0] - self.cutOffset
            self.cutOffset = self.appendMap[0]
        fontIndices = self.fontMap.keys()
        colorIndices = self.colorMap.keys()
        alignIndices = self.alignMap.keys()
        for index in fontIndices:
            if index < self.cutOffset:
                del self.fontMap[index]

        for index in colorIndices:
            if index < self.cutOffset:
                del self.colorMap[index]

        for index in alignIndices:
            if index < self.cutOffset:
                del self.alignMap[index]

        i = 0
        index = self.nMap[i]
        while index < self.cutOffset:
            del self.nMap[i]
            i += 1
            index = self.nMap[i]

        self.rawText = self.rawText[cutLen:]

    def _addTask(self, task):
        if task[0] == 'SET':
            self.rawText = task[1]
            self.appendMap = []
            self._recalcPropsMap()
            self._recalcNMap()
            self._recalcHMap(0)
            self._recalcScrolls()
            self._refitCmps()
        elif task[0] == 'ADD':
            if task[2]:
                task[1] = u'<n>' + task[1]
            propsMap = self._calculatePropsMap(task[1], -1)
            nMap = self._calculateNMap(task[1], -1, task[2])
            appendPos = len(self.rawText)
            self.rawText += task[1]
            self.fontMap.update(propsMap[0])
            self.alignMap.update(propsMap[1])
            self.colorMap.update(propsMap[2])
            self.nMap += nMap
            self._recalcHMap(len(self.nMap) - len(nMap) - 1)
            if self.maxAppends > 0:
                self._newAppend(appendPos)
            self._recalcScrolls()
            self._refitCmps()
        CallbackHelpers.callback(self.renderText, self.MIN_RENDER_THRESHHOLD, cancel_existing=True)

    def scrollHandler(self, event, data):
        if event == 'RIGHT':
            self.scrollCursor[0] += 1
        elif event == 'LEFT':
            self.scrollCursor[0] -= 1
        elif event == 'hMOVE':
            self.scrollCursor[0] = data
        if event == 'DOWN':
            self.scrollCursor[1] += 1
        elif event == 'UP':
            self.scrollCursor[1] -= 1
        elif event == 'vMOVE':
            self.scrollCursor[1] = data
        if self.scrollCursor[0] > self.maxScroll[0]:
            self.scrollCursor[0] = self.maxScroll[0]
        if self.scrollCursor[0] < 0:
            self.scrollCursor[0] = 0
        if self.scrollCursor[1] > self.maxScroll[1]:
            self.scrollCursor[1] = self.maxScroll[1]
        if self.scrollCursor[1] < 0:
            self.scrollCursor[1] = 0
        self.component.vScroll.script.setValue(self.scrollCursor[1])
        self.component.hScroll.script.setValue(self.scrollCursor[0])
        CallbackHelpers.callback(self.renderText, self.MIN_RENDER_THRESHHOLD, cancel_existing=True)

    @PyGUIEvent('vScroll', 'scrollUp')
    def scrolledUP(self):
        self.scrollHandler('UP', None)
        return

    @PyGUIEvent('vScroll', 'scrollDown')
    def scrolledDOWN(self):
        self.scrollHandler('DOWN', None)
        return

    @PyGUIEvent('hScroll', 'scrollLeft')
    def scrolledLEFT(self):
        self.scrollHandler('LEFT', None)
        return

    @PyGUIEvent('hScroll', 'scrollRight')
    def scrolledRIGHT(self):
        self.scrollHandler('RIGHT', None)
        return

    @PyGUIEvent('vScroll', 'scrollMoved')
    def vScrollMoved(self, newVal):
        self.scrollHandler('vMOVE', newVal)

    @PyGUIEvent('hScroll', 'scrollMoved')
    def hScrollMoved(self, newVal):
        self.scrollHandler('hMOVE', newVal)