# Embedded file name: scripts/client/soGUI/soSlider.py
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import BWPersonality
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
from soGUI.soVisualStateComponent import soVisualStateComponent
from Helpers.PyGUI.DraggableComponent import DraggableComponent
from Keys import *
from math import ceil, floor
from Math import Vector2

class guiKeyEvent(object):

    def __init__(self, key, down, mods = None):
        self.key = key
        self.down = down
        self.modifiers = mods

    def isKeyDown(self):
        return self.down


class soSliderVisualState(VisualState):

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
        if dataSection.has_key('line'):
            lineSection = dataSection._line
            self.lineMaterialFX = lineSection.readString('materialFX', '')
            self.lineTextureName = lineSection.readString('textureName', '')
            self.lineLeftTextureName = lineSection.readString('leftSide', '')
            self.lineRightTextureName = lineSection.readString('rightSide', '')
            self.lineColour = lineSection.readVector4('colour', (255, 255, 255, 255))
        if dataSection.has_key('mark'):
            markSection = dataSection._mark
            self.markTextureName = markSection.readString('textureName', '')
        if dataSection.has_key('btn'):
            btnSection = dataSection._btn
            self.btnMaterialFX = btnSection.readString('materialFX', '')
            self.btnTextureName = btnSection.readString('textureName', '')
            self.btnColour = btnSection.readVector4('colour', (255, 255, 255, 255))

    def apply(self, componentScript):
        VisualState.apply(self, componentScript)
        componentScript.component.backLine.textureName = self.lineTextureName
        componentScript.component.backLine.colour = self.lineColour
        componentScript.component.leftBackLine.textureName = self.lineLeftTextureName
        componentScript.component.rightBackLine.textureName = self.lineRightTextureName
        if hasattr(componentScript, 'markTexture'):
            componentScript.markTexture = BigWorld.PyTextureProvider(self.markTextureName)
            componentScript.updateMarks()
        if hasattr(componentScript, 'btnComponent'):
            componentScript.btnComponent.texture = None
            componentScript.btnComponent.textureName = self.btnTextureName
            componentScript.btnComponent.colour = self.btnColour
            if self.btnMaterialFX != '':
                componentScript.btnComponent.materialFX = self.btnMaterialFX
            else:
                componentScript.btnComponent.materialFX = 'BLEND'
        return


class soSliderButton(PyGUIBase, DraggableComponent):
    factoryString = 'soGUI.soSliderButton'

    def __init__(self, component, slider = None):
        PyGUIBase.__init__(self, component)
        DraggableComponent.__init__(self, True, False, True)
        component.script = self
        self.step = 0
        self.dragProxy = self.component
        self.pushed = False
        self.isDragging = False
        self.onDragging = self.dragging
        self.onEndDrag = self.endDrag
        self.slider = slider
        self.setupRoot()
        self.setupBtn()

    def endDrag(self):
        self.slider.onSliderStop()

    def dragging(self):
        self.slider.onSliderMove()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.width = 7
        cmp.height = 14
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
        cmp.width = 7
        cmp.height = 14
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


class soSlider(PyGUIBase, soVisualStateComponent):
    factoryString = 'soGUI.soSlider'
    visualStateString = 'soGUI.soSliderVisualState'

    def __init__(self, component, steps = 101, visualSteps = 20, minMax = [0.0, 1.0], width = 150, default_settings_width = 5, height = 16, style = 'soGUI/visual_styles/defaultSlider.xml', showMinMax = True, font = 'ruRU_calibri_default.font', limOffset = 5):
        PyGUIBase.__init__(self, component)
        soVisualStateComponent.__init__(self, component, self.visualStateString)
        component.script = self
        self.width = width
        self.height = height
        self.default_settings_width = default_settings_width
        self.steps = steps
        self.visualSteps = visualSteps
        self.minMax = minMax
        self.showMinMax = showMinMax
        self.font = font
        self.step = 0
        self.markTexture = None
        self.markMap = {}
        self.stepMap = {}
        self.setupRoot()
        self.setupLine()
        self.setupBtn()
        self.buildStepMap()
        self.initVSC(style)
        self.setVisualState('normal')
        self.setStep(0)
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.width
        cmp.height = self.height
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.mouseButtonFocus = True

    def setupLine(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileWidth = self.default_settings_width
        cmp.tileHeight = self.height
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.width = self.width - 8
        cmp.height = self.height
        cmp.position = (4, 0, 0.5)
        self.component.addChild(cmp, 'backLine')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.width = 4
        cmp.height = self.height
        cmp.position = (0, 0, 0.5)
        self.component.addChild(cmp, 'leftBackLine')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.width = 4
        cmp.height = self.height
        cmp.position = (self.width, 0, 0.5)
        self.component.addChild(cmp, 'rightBackLine')

    def setupMarks(self):
        offset = (self.btnComponent.width - 1) / 2.0
        r_offset = 2.0 / (self.component.backLine.width / offset)
        stepSize = (2.0 - r_offset * 2.0) / float(self.visualSteps - 1)
        mH = self.height / 2.0
        for i in xrange(self.visualSteps):
            cmp = GUI.Simple('')
            cmp.horizontalPositionMode = 'CLIP'
            cmp.verticalPositionMode = 'CLIP'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'TOP'
            cmp.tiled = True
            cmp.tileWidth = 1
            cmp.tileHeight = self.height / 2
            cmp.width = 1
            cmp.height = mH
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.texture = self.markTexture
            cmp.position = (-1.0 + r_offset + stepSize * i, 0.0, 0.2)
            self.component.addChild(cmp, 'mark' + str(i))
            self.markMap[i] = cmp.position.x

    def setupBtn(self):
        btn = soSliderButton(GUI.Window(), self)
        cmp = btn.component
        btn.onBound()
        self.btnComponent = cmp
        self.component.addChild(cmp, 'btn')

    def buildStepMap(self):
        offset = (self.btnComponent.width - 1) / 2.0
        r_offset = 2.0 / (self.component.backLine.width / offset)
        stepSize = 0.0
        if self.steps > 1:
            stepSize = (2.0 - r_offset * 2.0) / float(self.steps - 1)
        for i in xrange(self.steps):
            self.stepMap[i] = -1.0 + r_offset + stepSize * i

    def updateMarks(self):
        return
        for i in xrange(self.visualSteps):
            cmp = self.component.__getattribute__('mark' + str(i))
            cmp.texture = self.markTexture

    def setValue(self, val = 0, byUser = True):
        step = self.valueToStep(val)
        self.setStep(step, byUser)
        if byUser:
            self.onValueChanged(step, self.getValue())
            self.onValueChanged__()
        else:
            self.onValueSet(step, self.getValue())

    def setStep(self, step = 0, byUser = True):
        self.btnComponent.position.x = self.stepMap[step]
        self.step = step
        if byUser:
            self.onValueChanged(step, self.getValue())
            self.onValueChanged__()
        else:
            self.onValueSet(step, self.getValue())

    def getStep(self):
        return self.step

    def getValue(self):
        return self.stepToValue(self.step)

    def valueToStep(self, val):
        if not val or not val - self.minMax[0]:
            return 0
        if val > self.minMax[1]:
            val = self.minMax[1]
        relVal = 1 / ((self.minMax[1] - self.minMax[0]) / (val - self.minMax[0]))
        step = ceil(self.steps * relVal)
        return step - 1

    def stepToValue(self, step):
        if not step:
            return self.minMax[0]
        if step > self.steps:
            step = self.steps
        relStep = 1 / ((self.steps - 1) / float(step))
        val = self.minMax[0] + (self.minMax[1] - self.minMax[0]) * relStep
        return val

    def setLimits(self, min, max):
        self.minMax = [min, max]
        self.onValueSet(self.step, self.getValue())

    def _drawLimits(self):
        return
        if not self.showMinMax:
            return
        if not hasattr(self.component, 'minLabel'):
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.font = self.font
            cmp.materialFX = 'BLEND'
            cmp.colour = (255, 255, 255, 255)
            cmp.position = (-1.0, -1.0, 0.5)
            self.component.addChild(cmp, 'minLabel')
        if not hasattr(self.component, 'maxLabel'):
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.horizontalAnchor = 'RIGHT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.font = self.font
            cmp.materialFX = 'BLEND'
            cmp.colour = (255, 255, 255, 255)
            cmp.position = (1.0, -1.0, 0.5)
            self.component.addChild(cmp, 'maxLabel')
        self.component.minLabel.text = str(self.minMax[0])
        self.component.maxLabel.text = str(self.minMax[1])

    def _alignSlider(self):
        pos = self.btnComponent.position.x
        minDist = 2.0
        bestStep = self.stepMap[0]
        for step in self.stepMap:
            dist = abs(self.stepMap[step] - pos)
            if dist < minDist:
                minDist = dist
                bestStep = step

        self.setStep(bestStep, True)

    def onSliderStop(self):
        self._alignSlider()

    def onSliderMove(self):
        pos = self.btnComponent.position.x
        minDist = 2.0
        bestStep = self.stepMap[0]
        for step in self.stepMap:
            dist = abs(self.stepMap[step] - pos)
            if dist < minDist:
                minDist = dist
                bestStep = step

        self.onTargetChanged(bestStep)

    def handleMouseButtonEvent(self, cmp, event):
        if event.isKeyUp():
            return False
        self.component.widthMode = self.component.heightMode = 'CLIP'
        localCoords = self.component.screenToLocal(Vector2(event.cursorPosition.x, event.cursorPosition.y))
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.btnComponent.position.x = localCoords.x
        self._alignSlider()
        return True

    def onValueChanged(self, step, val):
        return None

    def onValueSet(self, step, val):
        return None

    def onValueChanged__(self):
        return None

    def onTargetChanged(self, step):
        return None