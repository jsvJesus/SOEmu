# Embedded file name: scripts/client/soGUI/soScrollBar.py
import GUI
import BigWorld
import soGUI
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI import PyGUIBase
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
from soGUI.soVisualStateComponent import soVisualStateComponent
from Helpers.PyGUI.DraggableComponent import DraggableComponent
from Helpers.PyGUI.Utils import clipPosition, clipSize, applyMapping
from Helpers.PyGUI import PyGUIEvent
from soGUI.soButton import soButton
import Keys
import math
from Keys import *

class guiKeyEvent(object):

    def __init__(self, key, down, mods = None):
        self.key = key
        self.down = down
        self.modifiers = mods

    def isKeyDown(self):
        return self.down


class soScrollBarVisualState(VisualState):

    def __init__(self):
        VisualState.__init__(self)
        self.dataSect = None
        self.backgroundTextureName = ''
        self.backgroundTextureMapping = None
        self.backgroundColour = (255, 255, 255, 255)
        self.thumbTextureName = ''
        self.thumbTextureMapping = None
        self.thumbColour = (255, 255, 255, 255)
        return

    def onSave(self, dataSection):
        VisualState.onSave(self, dataSection)
        backgroundSection = dataSection.createSection('background')
        backgroundSection.writeString('textureName', self.backgroundTextureName)
        if self.backgroundTextureMapping:
            mappingSection = backgroundSection.createSection('mapping')
            self._writeMappingSection(mappingSection, self.backgroundTextureMappingType, self.backgroundTextureMapping)
        backgroundSection.writeVector4('colour', self.backgroundColour)
        thumbSection = dataSection.createSection('thumb')
        thumbSection.writeString('textureName', self.thumbTextureName)
        if self.thumbTextureMapping:
            mappingSection = thumbSection.createSection('mapping')
            self._writeMappingSection(mappingSection, self.thumbTextureMappingType, self.thumbTextureMapping)
        thumbSection.writeVector4('colour', self.thumbColour)

    def onLoad(self, dataSection):
        VisualState.onLoad(self, dataSection)
        if dataSection.has_key('background'):
            backgroundSection = dataSection._background
            self.backgroundTextureName = backgroundSection.readString('textureName', '')
            if backgroundSection.has_key('mapping'):
                mappingSection = backgroundSection._mapping
                mappingType, mapping = self._readMappingSection(mappingSection)
                self.backgroundTextureMappingType = mappingType
                self.backgroundTextureMapping = mapping
            else:
                self.backgroundTextureMapping = None
            self.backgroundColour = backgroundSection.readVector4('colour', (255, 255, 255, 255))
        if dataSection.has_key('thumb'):
            thumbSection = dataSection._thumb
            self.thumbTextureName = thumbSection.readString('textureName', '')
            if thumbSection.has_key('mapping'):
                mappingSection = thumbSection._mapping
                mappingType, mapping = self._readMappingSection(mappingSection)
                self.thumbTextureMappingType = mappingType
                self.thumbTextureMapping = mapping
            else:
                self.thumbTextureMapping = None
            self.thumbColour = thumbSection.readVector4('colour', (255, 255, 255, 255))
        return

    def apply(self, componentScript):
        VisualState.apply(self, componentScript)
        componentScript.component.textureName = self.backgroundTextureName
        componentScript.component.colour = self.backgroundColour
        if hasattr(componentScript, 'sliderThumb'):
            componentScript.sliderThumb.component.textureName = self.thumbTextureName
            if self.thumbTextureMapping:
                applyMapping(componentScript.sliderThumb.component, self.thumbTextureMappingType, self.thumbTextureMapping)
            componentScript.sliderThumb.component.colour = self.thumbColour


class soScrollSlider(PyGUIBase, DraggableComponent):
    factoryString = 'soGUI.soScrollSlider'

    def __init__(self, component, isHorizontal = True):
        PyGUIBase.__init__(self, component)
        DraggableComponent.__init__(self, isHorizontal, not isHorizontal, True)
        component.script = self
        self.component.focus = True
        self.component.moveFocus = True
        self.component.crossFocus = True
        self.onDragging = self._onDrag
        self.dragProxy = self.component

    def _setValue(self, value):
        sliderWidth, sliderHeight = clipSize(self.component)
        slider = self.component.parent.script
        thumbPos = (value - slider.minValue) / (slider.maxValue - slider.minValue)
        if slider.isHorizontal:
            thumbPos = (2.0 - sliderWidth) * thumbPos - 1.0 + sliderWidth / 2
        else:
            thumbPos = (2.0 - sliderHeight) * thumbPos - 1.0 + sliderHeight / 2
        self.component.position = (thumbPos, 0, 1) if slider.isHorizontal else (0, thumbPos, 1)

    def _setValueFromMouse(self, pos):
        slider = self.component.parent.script
        parent = self.component.parent
        position = parent.screenToLocal(pos)
        self.component.position = (2 * position[0] / parent.width - 1.0, 0, 1) if slider.isHorizontal else (0, 2 * position[1] / parent.height - 1.0, 1)
        self._onDrag()

    def _onDrag(self):
        position = clipPosition(self.component)
        sliderWidth, sliderHeight = clipSize(self.component)
        if sliderWidth == 2.0:
            sliderWidth = 1.9999
        slider = self.component.parent.script
        if slider.isHorizontal:
            thumbPos = (position[0] + 1.0 - sliderWidth / 2) / (2.0 - sliderWidth)
        else:
            thumbPos = (position[1] + 1.0 - sliderHeight / 2) / (2.0 - sliderHeight)
        thumbPos = min(max(0.0, thumbPos), 1.0)
        newValue = thumbPos * (slider.maxValue - slider.minValue) + slider.minValue
        newValue += slider.stepSize / 2.0
        newValue -= math.fmod(newValue, slider.stepSize)
        self._setValue(newValue)
        slider.value = newValue
        slider.onValueChanged()

    def handleMouseButtonEvent(self, comp, event):
        PyGUIBase.handleMouseButtonEvent(self, comp, event)
        key = event.key
        down = event.isKeyDown()
        slider = self.component.parent.script
        if key == Keys.KEY_LEFTMOUSE:
            if down and not slider.thumbPressed:
                slider.thumbPressed = True
            elif not down and slider.thumbPressed:
                slider.thumbPressed = False
        slider._updateVisualState(hover=True)
        return DraggableComponent.handleMouseButtonEvent(self, comp, event)

    def handleMouseEnterEvent(self, comp):
        PyGUIBase.handleMouseEnterEvent(self, comp)
        slider = self.component.parent.script
        slider.handleMouseEnterEvent(comp)
        slider.thumbPressed = slider.thumbPressed and BigWorld.isKeyDown(Keys.KEY_LEFTMOUSE)
        slider._updateVisualState(hover=True)
        return True

    def handleMouseLeaveEvent(self, comp):
        slider = self.component.parent.script
        slider._updateVisualState(hover=False)
        return True


class soScrollBar(PyGUIBase, soVisualStateComponent):
    NORMAL_STATE = 'normal'
    HOVER_STATE = 'hover'
    PRESSED_STATE = 'pressed'
    DISABLED_STATE = 'disabled'
    factoryString = 'soGUI.soScrollBar'
    visualStateString = 'soGUI.soScrollBarVisualState'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        soVisualStateComponent.__init__(self, component, soScrollBar.visualStateString)
        component.script = self
        self.isHorizontal = False
        self.minValue = 0.0
        self.maxValue = 1.0
        self.stepSize = 0.1
        self.stepValue = 0
        self._value = 0.0
        self.thumbPressed = False
        self.sliderDisabled = False
        self.scrollConstrains = (1.0, -1.0)
        component.focus = True
        component.crossFocus = True
        component.moveFocus = True
        component.tiled = True
        component.tileHeight = 1
        component.tileWidth = 16
        self.onValueChanged = lambda : None
        self.scrollBtnUP = None
        self.scrollBtnDN = None
        self.setupBtns()
        self.setupThumb()
        self._bindEvents(self.__class__)
        return

    def _updateVisualState(self, hover):
        if self.sliderDisabled:
            visualStateName = soScrollBar.DISABLED_STATE
        elif self.thumbPressed:
            visualStateName = soScrollBar.PRESSED_STATE
        elif hover:
            visualStateName = soScrollBar.HOVER_STATE
        else:
            visualStateName = soScrollBar.NORMAL_STATE
        self.setVisualState(visualStateName)

    def _onValueChanged(self):
        self.onValueChanged()

    def _getValue(self):
        return self._value

    def _setValue(self, value):
        self._value = value
        self.component.thumb.script._setValue(value)

    value = property(_getValue, _setValue)

    def handleMouseButtonEvent(self, comp, key, down, modifiers):
        if down and not self.sliderDisabled:
            if GUI.mcursor().position.y > self.sliderThumb.component.localToScreen((self.sliderThumb.component.position.x, self.sliderThumb.component.position.y)).y:
                self.scrollUP()
                self.scrollUP()
                self.scrollUP()
                self.scrollUP()
            else:
                self.scrollDN()
                self.scrollDN()
                self.scrollDN()
                self.scrollDN()
        return True

    def onSave(self, dataSection):
        PyGUIBase.onSave(self, dataSection)
        dataSection.writeBool('isHorizontal', self.isHorizontal)
        dataSection.writeFloat('minValue', self.minValue)
        dataSection.writeFloat('maxValue', self.maxValue)
        dataSection.writeFloat('stepSize', self.stepSize)
        VisualStateComponent.onSave(self, dataSection)

    def onLoad(self, dataSection):
        PyGUIBase.onLoad(self, dataSection)
        self.isHorizontal = dataSection.readBool('isHorizontal', self.isHorizontal)
        self.minValue = dataSection.readFloat('minValue', self.minValue)
        self.maxValue = dataSection.readFloat('maxValue', self.maxValue)
        self.stepSize = dataSection.readFloat('stepSize', self.stepSize)
        VisualStateComponent.onLoad(self, dataSection)

    def onBound(self):
        self.value = self.minValue
        self.sliderBackground = self.component
        self._updateVisualState(hover=False)

    def setupThumb(self):
        self.sliderThumb = soScrollSlider(GUI.Window())
        self.sliderThumb.component.widthMode = 'PIXEL'
        self.sliderThumb.component.heightMode = 'PIXEL'
        self.sliderThumb.component.verticalPositionMode = 'CLIP'
        self.sliderThumb.component.horizontalPositionMode = 'CLIP'
        self.sliderThumb.component.width = 14
        self.sliderThumb.component.height = 14
        self.sliderThumb.component.materialFX = 'BLEND'
        self.sliderThumb.component.position = (0.0, 0.0, 0.0)
        self.sliderThumb.component.focus = True
        self.sliderThumb.component.crossFocus = True
        self.sliderThumb.component.moveFocus = True
        self.sliderThumb.component.dragFocus = True
        self.component.addChild(self.sliderThumb.component, 'thumb')

    def setupScrollingInfo(self, scrollSteps):
        self.scrollConstrains = (1.0 - (soGUI.getPixelHeight(self.component) * 16 + soGUI.getPixelHeight(self.component) * 7), -1.0 + (soGUI.getPixelHeight(self.component) * 16 + soGUI.getPixelHeight(self.component) * 7))
        if scrollSteps > 0:
            self.stepSize = self.maxValue / scrollSteps
        else:
            self.stepSize = 0.0
        if not self.stepSize:
            self.disableScroll()
        else:
            self.enableScroll()
            stepDisplacement = (self.scrollConstrains[0] - self.scrollConstrains[1]) / (self.maxValue / self.stepSize)
            self.sliderThumb.component.position.y = self.scrollConstrains[0] - stepDisplacement * self.stepValue

    def doStep(self, scrollDown = True):
        if scrollDown:
            if self.stepValue * self.stepSize <= self.maxValue:
                self.stepValue += 1
                stepDisplacement = (self.scrollConstrains[0] - self.scrollConstrains[1]) / (self.maxValue / self.stepSize)
                self.sliderThumb.component.position.y -= stepDisplacement
        elif self.stepValue * self.stepSize >= self.minValue:
            self.stepValue -= 1
            stepDisplacement = (self.scrollConstrains[0] - self.scrollConstrains[1]) / (self.maxValue / self.stepSize)
            self.sliderThumb.component.position.y += stepDisplacement

    def reset(self):
        self.stepValue = 0
        stepDisplacement = (self.scrollConstrains[0] - self.scrollConstrains[1]) / (self.maxValue / self.stepSize)
        self.sliderThumb.component.position.y = self.scrollConstrains[0] - stepDisplacement * self.stepValue

    def disableScroll(self):
        self.sliderDisabled = True
        self.scrollBtnDN.buttonDisabled = True
        self.scrollBtnUP.buttonDisabled = True
        self.scrollBtnDN.setVisualState('disabled')
        self.scrollBtnUP.setVisualState('disabled')
        self.sliderThumb.component.focus = False
        self.sliderThumb.component.crossFocus = False
        self.sliderThumb.component.moveFocus = False
        self.sliderThumb.component.dragFocus = False
        self.sliderThumb.component.visible = False

    def enableScroll(self):
        self.sliderDisabled = False
        self.scrollBtnDN.buttonDisabled = False
        self.scrollBtnUP.buttonDisabled = False
        self.scrollBtnDN.setVisualState('normal')
        self.scrollBtnUP.setVisualState('normal')
        self.sliderThumb.component.focus = True
        self.sliderThumb.component.crossFocus = True
        self.sliderThumb.component.moveFocus = True
        self.sliderThumb.component.dragFocus = True
        self.sliderThumb.component.visible = True

    def setupBtns(self):
        self.scrollBtnUP = soButton(GUI.Window())
        self.scrollBtnDN = soButton(GUI.Window())
        self.scrollBtnUP.component.verticalAnchor = 'TOP'
        self.scrollBtnUP.component.horizontalAnchor = 'LEFT'
        self.scrollBtnUP.component.verticalPositionMode = 'CLIP'
        self.scrollBtnUP.component.horizontalPositionMode = 'CLIP'
        self.scrollBtnUP.component.widthMode = 'CLIP'
        self.scrollBtnUP.component.heightMode = 'CLIP'
        self.scrollBtnUP.component.position = (-1.0, 1.0, 0.0)
        self.scrollBtnUP.component.width = 0
        self.scrollBtnUP.component.height = 0
        self.scrollBtnUP.component.visible = True
        self.scrollBtnUP.component.materialFX = 'BLEND'
        self.scrollBtnUP.component.focus = True
        self.scrollBtnDN.component.verticalAnchor = 'BOTTOM'
        self.scrollBtnDN.component.horizontalAnchor = 'LEFT'
        self.scrollBtnDN.component.verticalPositionMode = 'CLIP'
        self.scrollBtnDN.component.horizontalPositionMode = 'CLIP'
        self.scrollBtnDN.component.widthMode = 'CLIP'
        self.scrollBtnDN.component.heightMode = 'CLIP'
        self.scrollBtnDN.component.position = (-1.0, -1.0, 0.0)
        self.scrollBtnDN.component.width = 0
        self.scrollBtnDN.component.height = 0
        self.scrollBtnDN.component.visible = True
        self.scrollBtnDN.component.materialFX = 'BLEND'
        self.scrollBtnDN.component.focus = True
        self.scrollBtnUP.initVSC('soGUI/visual_styles/scrollBtnUP.xml')
        self.scrollBtnDN.initVSC('soGUI/visual_styles/scrollBtnDN.xml')
        self.scrollBtnDN.onBound()
        self.scrollBtnUP.onBound()
        self.scrollBtnDN.setVisualState('normal')
        self.scrollBtnUP.setVisualState('normal')
        self.component.addChild(self.scrollBtnUP.component, 'btnUP')
        self.component.addChild(self.scrollBtnDN.component, 'btnDN')

    def makeLayout(self):
        self.scrollBtnDN.component.width = soGUI.getPixelWidth(self.component) * 16
        self.scrollBtnUP.component.width = soGUI.getPixelWidth(self.component) * 16
        self.scrollBtnDN.component.height = soGUI.getPixelHeight(self.component) * 16
        self.scrollBtnUP.component.height = soGUI.getPixelHeight(self.component) * 16

    def scrollUP(self):
        return None

    def scrollDN(self):
        return None

    @PyGUIEvent('btnDN', 'onClick')
    def btnDNClicked(self):
        self.scrollDN()

    @PyGUIEvent('btnUP', 'onClick')
    def btnUPClicked(self):
        self.scrollUP()


class soScrollBarVisualState2(VisualState):

    def __init__(self):
        VisualState.__init__(self)
        self.dataSect = None
        self.backgroundTextureName = ''
        self.backgroundTextureMapping = None
        self.backgroundColour = (255, 255, 255, 255)
        self.scrollerTextureName = ''
        self.scrollerTextureMapping = None
        self.scrollerColour = (255, 255, 255, 255)
        return

    def onSave(self, dataSection):
        pass

    def onLoad(self, dataSection):
        VisualState.onLoad(self, dataSection)
        if dataSection.has_key('background'):
            backgroundSection = dataSection._background
            self.backgroundTextureName = backgroundSection.readString('textureName', '')
            if backgroundSection.has_key('mapping'):
                mappingSection = backgroundSection._mapping
                mappingType, mapping = self._readMappingSection(mappingSection)
                self.backgroundTextureMappingType = mappingType
                self.backgroundTextureMapping = mapping
            else:
                self.backgroundTextureMapping = None
            self.backgroundColour = backgroundSection.readVector4('colour', (255, 255, 255, 255))
        if dataSection.has_key('scroller'):
            scrollerSection = dataSection._scroller
            self.scrollerTextureName = scrollerSection.readString('textureName', '')
            if scrollerSection.has_key('mapping'):
                mappingSection = scrollerSection._mapping
                mappingType, mapping = self._readMappingSection(mappingSection)
                self.scrollerTextureMappingType = mappingType
                self.scrollerTextureMapping = mapping
            else:
                self.scrollerTextureMapping = None
            self.scrollerColour = scrollerSection.readVector4('colour', (255, 255, 255, 255))
        return

    def apply(self, componentScript):
        VisualState.apply(self, componentScript)
        componentScript.component.backFrame.textureName = self.backgroundTextureName
        componentScript.component.backFrame.colour = self.backgroundColour
        if hasattr(componentScript, 'btnComponent'):
            componentScript.btnComponent.textureName = self.scrollerTextureName
            if self.scrollerTextureMapping:
                applyMapping(componentScript.btnComponent, self.scrollerTextureMappingType, self.scrollerTextureMapping)
            componentScript.btnComponent.colour = self.scrollerColour


class soScrollerButton(PyGUIBase, DraggableComponent):
    factoryString = 'soGUI.soScrollerButton'

    def __init__(self, component, scrollBar = None):
        PyGUIBase.__init__(self, component)
        hDrag = scrollBar.isHorizontal
        DraggableComponent.__init__(self, hDrag, not hDrag, True)
        component.script = self
        self.step = 0
        self.dragProxy = self.component
        self.pushed = False
        self.isDragging = False
        self.onEndDrag = self.endDrag
        self.onDragging = self.onDrag
        self.scrollBar = scrollBar
        self.setupRoot()
        self.setupBtn()

    def onDrag(self):
        self.scrollBar.onBtnMove()

    def endDrag(self):
        self.scrollBar.onBtnStop()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.width = 16
        cmp.height = 16
        cmp.position = (0.0, 0.0, 0.1)
        cmp.focus = True
        cmp.dragFocus = True
        cmp.crossFocus = True
        cmp.mouseButtonFocus = True

    def setupBtn(self):
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 16
        cmp.height = 16
        cmp.position = (0, 0, 1.0)
        self.component.addChild(cmp, 'btn')

    def handleMouseButtonEvent(self, comp, event):
        down = event.isKeyDown()
        key = event.key
        modifiers = event.modifiers
        if down:
            self.pushed = True
        else:
            self.pushed = False
        if self.isDragging:
            dragHandle = DraggableComponent.handleMouseButtonEvent(self, comp, event)
            return dragHandle
        return True

    def handleDragStartEvent(self, *args):
        event = guiKeyEvent(KEY_LEFTMOUSE, True, None)
        DraggableComponent.handleMouseButtonEvent(self, self.component, event)
        self.isDragging = True
        return True

    def handleDragStopEvent(self, *args):
        event = guiKeyEvent(KEY_LEFTMOUSE, False, None)
        DraggableComponent.handleMouseButtonEvent(self, self.component, event)
        self.isDragging = False
        return True

    def handleDragEnterEvent(self, comp, dragged):
        return True

    def handleMouseEnterEvent(self, component):
        return True

    def handleMouseLeaveEvent(self, component):
        return True


class soScrollBar2(PyGUIBase, soVisualStateComponent):
    factoryString = 'soGUI.soScrollBar2'
    visualStateString = 'soGUI.soScrollBarVisualState2'

    def __init__(self, component, steps = 10, width = 16, height = 100, style = 'soGUI/visual_styles/defaultScrollBar.xml', horizontal = False, sendOnMove = True):
        PyGUIBase.__init__(self, component)
        soVisualStateComponent.__init__(self, component, self.visualStateString)
        component.script = self
        self.width = width
        self.height = height
        self.steps = steps
        self.isHorizontal = horizontal
        self.sendOnMove = sendOnMove
        self.btnComponent = None
        self.scrollUp = lambda : None
        self.scrollDown = lambda : None
        self.scrollLeft = lambda : None
        self.scrollRight = lambda : None
        self.value = 0
        self.style = style
        self.posMap = []
        self.setupRoot()
        self.setupFrame()
        self.setupBtns()
        self.buildPosMap()
        self.initVSC(style)
        self.setVisualState('normal')
        self.setValue(0)
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.width if not self.isHorizontal else self.height
        cmp.height = self.height if not self.isHorizontal else self.width
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''

    def setupFrame(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileWidth = 16 if not self.isHorizontal else 1
        cmp.tileHeight = 1 if not self.isHorizontal else 16
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        if self.style == 'soGUI/visual_styles/defaultScrollBar.xml':
            cmp.textureName = 'soGUI/maps/Controls/scroll/scrollbar.tga'
        else:
            cmp.textureName = 'soGUI/maps/Controls/scroll/scrollbar1.tga'
        cmp.width = 16 if not self.isHorizontal else self.height - 32
        cmp.height = self.height - 32 if not self.isHorizontal else 16
        cmp.position = (0, 16, 0.5) if not self.isHorizontal else (16, 0, 0.5)
        self.component.addChild(cmp, 'backFrame')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 16 if not self.isHorizontal else self.height - 32
        cmp.height = self.height - 32 if not self.isHorizontal else 16
        cmp.position = (0, 16, 0.1) if not self.isHorizontal else (16, 0, 0.1)
        cmp.textureName = ''
        self.component.addChild(cmp, 'scrollerHold')

    def buildPosMap(self):
        if self.steps <= 0:
            return
        self.posMap = []
        offset = self.btnComponent.height / 2.0
        r_offset = 0.0
        if self.isHorizontal:
            r_offset = 2.0 / (self.component.scrollerHold.width / offset)
        else:
            r_offset = 2.0 / (self.component.scrollerHold.height / offset)
        stepSize = (2.0 - r_offset * 2.0) / float(self.steps)
        for i in xrange(self.steps + 1):
            pos = 0
            if self.isHorizontal:
                pos = -1.0 + r_offset + stepSize * i
            else:
                pos = 1.0 - r_offset - stepSize * i
            self.posMap.append(pos)

    def setupBtns(self):
        btn = soScrollerButton(GUI.Window(), self)
        cmp = btn.component
        btn.onBound()
        self.btnComponent = cmp
        self.component.scrollerHold.addChild(cmp, 'btn')
        btn = soButton(GUI.Window())
        if self.style == 'soGUI/visual_styles/defaultScrollBar.xml':
            btn.initVSC('soGUI/visual_styles/scrollBtnUP.xml')
        else:
            btn.initVSC('soGUI/visual_styles/scrollBtnUPForSettings.xml')
        btn.setVisualState('normal')
        btn.soundControlName = 'ArrowBtn'
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 16
        cmp.height = 16
        cmp.position = (0, 0, 0.1) if not self.isHorizontal else (0, 0, 0.1)
        self.component.addChild(cmp, 'btnUP')
        btn.onBound()
        btn = soButton(GUI.Window())
        if self.style == 'soGUI/visual_styles/defaultScrollBar.xml':
            btn.initVSC('soGUI/visual_styles/scrollBtnDN.xml')
        else:
            btn.initVSC('soGUI/visual_styles/scrollBtnDNForSettings.xml')
        btn.setVisualState('normal')
        btn.soundControlName = 'ArrowBtn'
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 16
        cmp.height = 16
        cmp.position = (0, self.height, 0.1) if not self.isHorizontal else (self.height - 16, 16, 0.1)
        self.component.addChild(cmp, 'btnDN')
        btn.onBound()

    def updateMarks(self):
        pass

    def setValue(self, val = 0):
        if self.steps <= 0:
            return
        if self.isHorizontal:
            self.btnComponent.position.x = self.posMap[int(val)]
        else:
            self.btnComponent.position.y = self.posMap[int(val)]
        self.value = int(val)

    def setSteps(self, steps):
        if steps <= 0:
            self.component.btnUP.script.buttonDisabled = True
            self.component.btnUP.script.setVisualState('disabled')
            self.component.btnDN.script.buttonDisabled = True
            self.component.btnDN.script.setVisualState('disabled')
            self.btnComponent.visible = False
        else:
            self.component.btnUP.script.buttonDisabled = False
            self.component.btnUP.script.setVisualState('normal')
            self.component.btnDN.script.buttonDisabled = False
            self.component.btnDN.script.setVisualState('normal')
            self.btnComponent.visible = True
        self.steps = int(steps)
        self.buildPosMap()
        if self.value > steps:
            self.value = steps
            if self.value < 0:
                self.value = 0
        self.setValue(self.value)

    def setWidth(self, w = 16):
        pass

    def setHeight(self, h):
        self.height = h
        if self.isHorizontal:
            self.component.width = h
            self.component.btnUP.position.x = h - 16
        else:
            self.component.height = h
            self.component.btnDN.position.y = h
        cmp = self.component.scrollerHold
        cmp.width = 16 if not self.isHorizontal else h - 32
        cmp.height = h - 32 if not self.isHorizontal else 16
        cmp = self.component.backFrame
        cmp.width = 16 if not self.isHorizontal else h - 32
        cmp.height = h - 32 if not self.isHorizontal else 16
        self.buildPosMap()
        self.setValue(self.value)

    def getValue(self):
        return self.value

    def onBtnStop(self):
        btnPos = None
        if self.isHorizontal:
            btnPos = self.btnComponent.position.x
        else:
            btnPos = self.btnComponent.position.y
        minDist = 2.0
        bestMark = 0
        for i, pos in enumerate(self.posMap):
            dist = abs(pos - btnPos)
            if dist < minDist:
                minDist = dist
                bestMark = i

        if self.isHorizontal:
            self.btnComponent.position.x = self.posMap[self.value]
        else:
            self.btnComponent.position.y = self.posMap[self.value]
        self.scrollMoved(bestMark)
        return

    def onBtnMove(self):
        btnPos = None
        if self.isHorizontal:
            btnPos = self.btnComponent.position.x
        else:
            btnPos = self.btnComponent.position.y
        minDist = 2.0
        bestMark = 0
        for i, pos in enumerate(self.posMap):
            dist = abs(pos - btnPos)
            if dist < minDist:
                minDist = dist
                bestMark = i

        if self.sendOnMove:
            self.scrollMoved(bestMark)
        return

    def scrollMoved(self, val):
        return None

    @PyGUIEvent('btnUP', 'onClick')
    def scrolledUP(self):
        if self.isHorizontal:
            self.scrollLeft()
        else:
            self.scrollUp()

    @PyGUIEvent('btnDN', 'onClick')
    def scrolledDN(self):
        if self.isHorizontal:
            self.scrollRight()
        else:
            self.scrollDown()