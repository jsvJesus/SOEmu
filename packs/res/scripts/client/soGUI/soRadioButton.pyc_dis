# Embedded file name: scripts/client/soGUI/soRadioButton.py
import BigWorld
import BWPersonality
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
from soGUI.soButton import soButton
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI import PyGUIBase

class RadioButtonPropsStructure(object):

    def __init__(self, labelText = u'push me', radioBtnW = 20, radioBtnH = 20, font = 'ruRU_calibri_default.font', labelLeftOffset = 5, labelColour = (255, 255, 255, 255)):
        self.radioButtonWidth = radioBtnW
        self.radioButtonHeight = radioBtnH
        self.radioButtonFont = font
        self.labelLeftOffset = labelLeftOffset
        self.labelText = labelText
        self.labelColour = labelColour


class soRadioButton(PyGUI.Window):
    factoryString = 'soGUI.soRadioButton'

    def __init__(self, component, parentScreen, group = 0, props = RadioButtonPropsStructure()):
        PyGUI.Window.__init__(self, component)
        component.script = self
        self.label = None
        self.radio = None
        self.radioWidth = props.radioButtonWidth
        self.radioHeight = props.radioButtonHeight
        self.labelFont = props.radioButtonFont
        self.labelColour = props.labelColour
        self.labelLeftOffset = props.labelLeftOffset
        self.labelText = props.labelText
        self.group = 0
        if isinstance(parentScreen, soGUI.soScreen):
            self.parentScreen = parentScreen
            self.setRadioGroup(group)
        else:
            self.parentScreen = None
            print 'Warning: RadioButton ', component, ' has no valid parent soScreen.'
        self.setupRoot()
        self.setupRadio()
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
        self.component.width = labelDims[0] + self.labelLeftOffset + self.radioWidth
        if labelDims[1] > self.radioHeight:
            self.component.height = labelDims[1]
        else:
            self.component.height = self.radioHeight
        self.component.visible = True
        return

    def setupRadio(self):
        if self.radio is None:
            self.radio = soButton(GUI.Window())
        self.radio.component.widthMode = self.radio.component.heightMode = 'PIXEL'
        self.radio.component.horizontalPositionMode = self.radio.component.verticalPositionMode = 'CLIP'
        self.radio.component.verticalAnchor = 'CENTER'
        self.radio.component.horizontalAnchor = 'LEFT'
        self.radio.component.width = self.radioWidth
        self.radio.component.height = self.radioHeight
        self.radio.component.position = (-1.0, 0.0, 0.0)
        self.radio.buttonStyle = soButton.RADIOBUTTON_STYLE
        self.radio.initVSC('soGUI/visual_styles/radioButton.xml')
        self.radio.onBound()
        self.radio.setVisualState('normal')
        if not hasattr(self.component, 'radioBtn'):
            self.component.addChild(self.radio.component, 'radioBtn')
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

    @PyGUIEvent('radioBtn', 'onClick')
    def processRadioClick(self):
        if self.parentScreen is not None:
            self.parentScreen.radioSelect(self.component)
        return

    def setRadioGroup(self, group):
        self.group = group
        if self.parentScreen is not None:
            self.parentScreen.registerRadioBtn(self.component, self.group)
        return

    def selection(self, doSelect = True):
        self.radio.buttonActive = doSelect
        if doSelect:
            self.radio.setVisualState('active')
        else:
            self.radio.setVisualState('normal')


class soRadioButton2(PyGUIBase):
    factoryString = 'soGUI.soRadioButton2'

    def __init__(self, component, labelText = u'RadioBtn', btnW = 18, btnH = 18, font = 'ruRU_calibri_default.font', labelLeftOffset = 5, labelColour = (255, 255, 255, 255), radioGroup = 'global_radio', bvisual_styles = 'soGUI/visual_styles/checkBox.xml'):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.bvisual_styles = bvisual_styles
        self.label = None
        self.btn = None
        self.btnWidth = btnW
        self.btnHeight = btnH
        self.labelFont = font
        self.labelColour = labelColour
        self.labelLeftOffset = labelLeftOffset
        self.radioGroup = radioGroup
        self.labelText = labelText
        self.setupRoot()
        self.setupCheckBox()
        self.setupLabel()
        self.registerRadioGroup()
        return

    def setupRoot(self):
        testString = GUI.Text('')
        testString.font = self.labelFont
        labelDims = testString.stringDimensions(self.labelText)
        testString = None
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.horizontalAnchor = 'LEFT'
        self.component.verticalAnchor = 'TOP'
        self.component.width = labelDims[0] + self.labelLeftOffset + self.btnWidth
        if labelDims[1] > self.btnHeight:
            self.component.height = labelDims[1]
        else:
            self.component.height = self.btnHeight
        self.component.visible = True
        return

    def setupCheckBox(self):
        if self.btn is None:
            self.btn = soButton(GUI.Window())
        self.btn.component.widthMode = self.btn.component.heightMode = 'PIXEL'
        self.btn.component.horizontalPositionMode = self.btn.component.verticalPositionMode = 'CLIP'
        self.btn.component.verticalAnchor = 'CENTER'
        self.btn.component.horizontalAnchor = 'LEFT'
        self.btn.component.width = self.btnWidth
        self.btn.component.height = self.btnHeight
        self.btn.component.position = (-1.0, 0.0, 0.0)
        self.btn.buttonStyle = soButton.CHECKBOX_STYLE
        self.btn.initVSC(self.bvisual_styles)
        self.btn.onBound()
        self.btn.setVisualState('normal')
        if not hasattr(self.component, 'checkBox'):
            self.component.addChild(self.btn.component, 'checkBox')
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
        self.component.width = labelDims[0] + self.labelLeftOffset + self.btnWidth
        if labelDims[1] > self.btnHeight:
            self.component.height = labelDims[1]
        else:
            self.component.height = self.btnHeight
        self.label.text = self.labelText
        return

    def registerRadioGroup(self):
        BWPersonality.GUICore.addToRadioGroup(self.radioGroup, self)

    def setVisualState(self, state):
        self.btn.setVisualState(state)

    def isChecked(self):
        return self.btn.buttonActive

    def disable(self):
        self.btn.buttonDisabled = True
        self.btn._updateVisualState()

    def enable(self):
        self.btn.buttonDisabled = False
        self.btn._updateVisualState()

    def setActive(self):
        self.btn.buttonActive = True
        self.btn._updateVisualState()
        BWPersonality.GUICore.onRadioBtn(self.radioGroup, self)

    def setInactive(self):
        self.btn.buttonActive = False
        self.btn._updateVisualState()

    def onStateChange(self):
        return None

    def fini(self):
        self.btn = None
        self.label = None
        return

    @PyGUIEvent('checkBox', 'onClick')
    def onCheck(self):
        self.onStateChange()
        BWPersonality.GUICore.onRadioBtn(self.radioGroup, self)