# Embedded file name: scripts/client/soGUI/soCheckBox.py
from Localization import lc
import BigWorld
import BWPersonality
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
from soGUI.soButton import soButton
from Helpers.PyGUI import PyGUIEvent

class CheckBoxPropsStructure(object):

    def __init__(self, labelText = lc('soCheckBox.soGUI.STRING_12_32'), checkBoxW = 18, checkBoxH = 18, font = 'ruRU_calibri_default.font', labelLeftOffset = 5, labelColour = (255, 255, 255, 255)):
        self.checkBoxWidth = checkBoxW
        self.checkBoxHeight = checkBoxH
        self.checkBoxFont = font
        self.labelLeftOffset = labelLeftOffset
        self.labelText = labelText
        self.labelColour = labelColour


class soCheckBox(PyGUI.Window):
    factoryString = 'soGUI.soCheckBox'

    def __init__(self, component, props = CheckBoxPropsStructure(), default_style = 'soGUI/visual_styles/checkBox.xml'):
        PyGUI.Window.__init__(self, component)
        component.script = self
        self.label = None
        self.box = None
        self.style = default_style
        self.boxWidth = props.checkBoxWidth
        self.boxHeight = props.checkBoxHeight
        self.labelFont = props.checkBoxFont
        self.labelColour = props.labelColour
        self.labelLeftOffset = props.labelLeftOffset
        self.labelText = props.labelText
        self.setupRoot()
        self.setupCheckBox()
        self.setupLabel()
        return

    def setupRoot(self):
        testString = GUI.Text('')
        testString.font = self.labelFont
        labelDims = testString.stringDimensions(self.labelText)
        testString = None
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.horizontalAnchor = 'LEFT'
        self.component.verticalAnchor = 'TOP'
        self.component.width = labelDims[0] + self.labelLeftOffset + self.boxWidth
        if labelDims[1] > self.boxHeight:
            self.component.height = labelDims[1]
        else:
            self.component.height = self.boxHeight
        self.component.visible = True
        return

    def setupCheckBox(self):
        if self.box is None:
            self.box = soButton(GUI.Window())
        self.box.component.widthMode = self.box.component.heightMode = 'PIXEL'
        self.box.component.horizontalPositionMode = self.box.component.verticalPositionMode = 'CLIP'
        self.box.component.verticalAnchor = 'CENTER'
        self.box.component.horizontalAnchor = 'LEFT'
        self.box.component.width = self.boxWidth
        self.box.component.height = self.boxHeight
        self.box.component.position = (-1.0, 0.0, 0.0)
        self.box.buttonStyle = soButton.CHECKBOX_STYLE
        self.box.initVSC(self.style)
        self.box.onBound()
        self.box.setVisualState('normal')
        if not hasattr(self.component, 'checkBox'):
            self.component.addChild(self.box.component, 'checkBox')
        return

    def setupLabel(self):
        if self.label is None:
            self.label = GUI.Text(self.labelText)
        self.label.horizontalPositionMode = self.label.verticalPositionMode = 'CLIP'
        self.label.verticalAnchor = 'CENTER'
        self.label.horizontalAnchor = 'RIGHT'
        self.label.font = self.labelFont
        self.label.colour = self.labelColour
        self.label.position = (1.0, 0.0, 0.0)
        if not hasattr(self.component, 'label'):
            self.component.addChild(self.label, 'label')
        return

    def setLabel(self, text):
        self.labelText = text
        testString = GUI.Text('')
        testString.font = self.labelFont
        labelDims = testString.stringDimensions(self.labelText)
        testString = None
        self.component.width = labelDims[0] + self.labelLeftOffset + self.boxWidth
        if labelDims[1] > self.boxHeight:
            self.component.height = labelDims[1]
        else:
            self.component.height = self.boxHeight
        self.label.text = self.labelText
        return

    def setVisualState(self, state):
        self.box.setVisualState(state)

    def isChecked(self):
        return self.box.buttonActive

    def disable(self):
        self.box.buttonDisabled = True
        self.box._updateVisualState()

    def enable(self):
        self.box.buttonDisabled = False
        self.box._updateVisualState()

    def setActive(self):
        self.box.buttonActive = True
        self.box._updateVisualState()

    def setInactive(self):
        self.box.buttonActive = False
        self.box._updateVisualState()

    def onStateChange(self):
        return None

    def fini(self):
        self.box = None
        self.label = None
        return

    @PyGUIEvent('checkBox', 'onClick')
    def onCheck(self):
        self.onStateChange()