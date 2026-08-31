# Embedded file name: scripts/client/soGUI/soButton.py
import BigWorld
import GUI
import Keys
import Helpers.PyGUI as PyGUI
import soGUI
import Helpers.PyGUI.TextStyles as TextStyles
import Helpers.PyGUI.Utils as Utils
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
from soGUI.soVisualStateComponent import soVisualStateComponent
from soGUI.data import SoundFeed
import sounds
import Helpers.PyGUI.Utils

def _getRadioButtons(comp, groupName):
    if comp is None:
        return []
    else:
        return [ child for name, child in comp.children if child.script and getattr(child.script, 'buttonStyle', None) == soButton.RADIOBUTTON_STYLE and child.script.groupName == groupName ]
        return


class soButtonVisualState(VisualState):

    def __init__(self):
        VisualState.__init__(self)
        self.textStyle = ''
        self.iconTextureName = ''
        self.iconTextureMapping = None
        self.textureType = 'SIMPLE'
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
            if iconSection.has_key('textureType'):
                self.textureType = iconSection._textureType.asString
            self.iconColour = iconSection.readVector4('colour', (255, 255, 255, 255))
        return

    def apply(self, componentScript):
        VisualState.apply(self, componentScript)
        if getattr(componentScript, 'buttonLabel', None) is not None and self.textStyle:
            TextStyles.setStyle(componentScript.buttonLabel, self.textStyle)
        if hasattr(componentScript, 'buttonIcon'):
            if self.iconTextureName != '':
                if self.textureType == 'SIMPLE':
                    componentScript.buttonIcon.textureName = self.iconTextureName
                    componentScript.buttonFIcon.textureName = ''
                elif self.textureType == 'FRAME':
                    componentScript.buttonFIcon.textureName = self.iconTextureName
                    componentScript.buttonIcon.textureName = ''
            if self.iconTextureMapping:
                Utils.applyMapping(componentScript.buttonIcon, self.iconTextureMappingType, self.iconTextureMapping)
            componentScript.buttonIcon.colour = self.iconColour
            if self.iconMaterialFX != '':
                componentScript.buttonIcon.materialFX = self.iconMaterialFX
            else:
                componentScript.buttonIcon.materialFX = 'BLEND'
        return


class soButton(PyGUIBase, soVisualStateComponent):
    PRESSBUTTON_STYLE = 'pressbutton'
    TOGGLEBUTTON_STYLE = 'togglebutton'
    CHECKBOX_STYLE = 'checkbox'
    RADIOBUTTON_STYLE = 'radiobutton'
    TOGGLABLE_BUTTON_STYLES = (TOGGLEBUTTON_STYLE, CHECKBOX_STYLE, RADIOBUTTON_STYLE)
    NORMAL_STATE = 'normal'
    HOVER_STATE = 'hover'
    PRESSED_STATE = 'pressed'
    ACTIVE_STATE = 'active'
    DISABLED_STATE = 'disabled'
    HOVER_ACTIVE_STATE = 'hover_active'
    PRESSED_ACTIVE_STATE = 'pressed_active'
    DISABLED_ACTIVE_STATE = 'disabled_active'
    BTN_LABEL_DEPTH = 0.0
    BTN_ICON_DEPTH = 1.0
    factoryString = 'soGUI.soButton'
    visualStateString = 'soGUI.soButtonVisualState'

    def __init__(self, component, default_label_horizontal_anchor = 'CENTER', default_PositionMode = 'CLIP', isOptions = False, fontLabel = 'ruRU_calibri_large.font', fontColor = (175, 166, 112, 255)):
        PyGUIBase.__init__(self, component)
        soVisualStateComponent.__init__(self, component, soButton.visualStateString)
        self.default_label_horizontal_anchor = default_label_horizontal_anchor
        self.default_PositionMode = default_PositionMode
        self._makeFrameTexture()
        component.script = self
        self.fontColor = fontColor
        self.fontLabel = fontLabel
        self.isOptions = isOptions
        self.component = component
        self.component.focus = True
        self.component.mouseButtonFocus = True
        self.component.moveFocus = True
        self.component.crossFocus = True
        self.buttonStyle = soButton.PRESSBUTTON_STYLE
        self.buttonPressed = False
        self.buttonActive = False
        self.buttonDisabled = False
        self.groupName = None
        self.hovering = False
        self.muted = False
        self.soundControlName = 'Button'
        self.onClick = lambda : None
        self.onActivate = lambda : None
        self.onDeactivate = lambda : None
        self.myLabel = None
        self.myGlyph = None
        if not hasattr(self, 'glyphTexture'):
            self.glyphTexture = ''
        if not hasattr(self, 'labelText'):
            self.labelText = ''
        self.initBtnChildren()
        self.updateChildren()
        return

    def _updateVisualState(self):
        if self.buttonDisabled:
            visualStateName = soButton.DISABLED_STATE if not self.buttonActive else soButton.DISABLED_ACTIVE_STATE
        elif self.buttonPressed and self.hovering:
            visualStateName = soButton.PRESSED_STATE if not self.buttonActive else soButton.PRESSED_ACTIVE_STATE
        elif self.hovering:
            visualStateName = soButton.HOVER_STATE if not self.buttonActive else soButton.HOVER_ACTIVE_STATE
        else:
            visualStateName = soButton.NORMAL_STATE if not self.buttonActive else soButton.ACTIVE_STATE
        self.setVisualState(visualStateName)
        if self.isOptions:
            self.myLabel.font = self.fontLabel
            self.myLabel.colour = self.fontColor

    def _onClick(self):
        if self.buttonDisabled:
            return
        if not self.muted:
            soundName = SoundFeed.soundFeed.getSound(self.soundControlName, 'Press')
            if soundName:
                sounds.playSound(soundName)
        if self.buttonStyle in soButton.TOGGLABLE_BUTTON_STYLES:
            self._makeActive(not self.buttonActive)
            if self.buttonActive:
                self.onActivate()
            else:
                self.onDeactivate()
        self.onClick()

    def setDisabledState(self, state):
        if self.buttonDisabled == state:
            return
        self.buttonDisabled = state
        self._updateVisualState()

    def setToggleState(self, state):
        self._makeActive(state)
        self._updateVisualState()

    def _makeActive(self, active = True):
        if self.buttonStyle == soButton.RADIOBUTTON_STYLE:
            if self.buttonActive == active:
                return
            if active:
                siblings = _getRadioButtons(self.component.parent, self.groupName)
                siblings = [ sibling for sibling in siblings if sibling.script != self ]
                for sibling in siblings:
                    if sibling.script.buttonActive:
                        sibling.script.buttonActive = False
                        sibling.script.onDeactivate()
                        sibling.script._updateVisualState()

        if self.buttonStyle in soButton.TOGGLABLE_BUTTON_STYLES:
            self.buttonActive = active

    def handleMouseButtonEvent(self, comp, event):
        PyGUIBase.handleMouseButtonEvent(self, comp, event)
        key = event.key
        down = event.isKeyDown()
        if key == Keys.KEY_LEFTMOUSE:
            if down and not self.buttonPressed:
                self.buttonPressed = True
            elif not down and self.buttonPressed:
                self.buttonPressed = False
                self._onClick()
        self._updateVisualState()
        return True

    def handleMouseEnterEvent(self, comp):
        if not self.muted:
            soundName = SoundFeed.soundFeed.getSound(self.soundControlName, 'Hover')
        if soundName:
            sounds.playSound(soundName)
        PyGUIBase.handleMouseEnterEvent(self, comp)
        self.buttonPressed = self.buttonPressed and BigWorld.isKeyDown(Keys.KEY_LEFTMOUSE)
        self.hovering = True
        self._updateVisualState()
        return True

    def handleMouseLeaveEvent(self, comp):
        self.hovering = False
        self._updateVisualState()
        return True

    def onSave(self, dataSection):
        PyGUIBase.onSave(self, dataSection)
        dataSection.writeBool('buttonDisabled', self.buttonDisabled)
        dataSection.writeString('buttonStyle', self.buttonStyle)
        if self.groupName:
            dataSection.writeString('groupName', self.groupName)
        VisualStateComponent.onSave(self, dataSection)

    def onLoad(self, dataSection):
        PyGUIBase.onLoad(self, dataSection)
        self.buttonStyle = dataSection.readString('buttonStyle')
        self.buttonDisabled = dataSection.readBool('buttonDisabled', False)
        self.groupName = dataSection.readString('groupName')
        soVisualStateComponent.onLoad(self, dataSection)
        self.labelText = dataSection.readString('labelText')
        self.glyphTexture = dataSection.readString('glyphTexture')
        self.updateChildren()

    def onBound(self):
        self.buttonIcon = self.component
        self.buttonFIcon = self.component.frameTexture
        self.buttonLabel = getattr(self.component, 'label', None)
        self._updateVisualState()
        return

    def _makeFrameTexture(self):
        cmp = GUI.Frame2('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'frameTexture')

    def initBtnChildren(self):
        buttonLabel = GUI.Text('')
        buttonGlyph = GUI.Simple('')
        self.myLabel = buttonLabel
        self.myLabel.horizontalPositionMode = self.default_PositionMode
        self.myLabel.verticalPositionMode = 'CLIP'
        self.myLabel.horizontalAnchor = self.default_label_horizontal_anchor
        self.myLabel.verticalAnchor = 'CENTER'
        self.myLabel.colour = (255.0, 20.0, 255.0, 255.0)
        self.myLabel.position = (0.0, 0.0, self.BTN_LABEL_DEPTH)
        self.myLabel.visible = 1
        self.myLabel.font = self.fontLabel
        self.myLabel.colourFormatting = True
        self.myGlyph = buttonGlyph
        self.myGlyph.horizontalPositionMode = 'CLIP'
        self.myGlyph.verticalPositionMode = 'CLIP'
        self.myGlyph.horizontalAnchor = 'CENTER'
        self.myGlyph.verticalAnchor = 'CENTER'
        self.myGlyph.widthMode = 'CLIP'
        self.myGlyph.heightMode = 'CLIP'
        self.myGlyph.width = 2.0
        self.myGlyph.height = 2.0
        self.myGlyph.colour = (255.0, 255.0, 255.0, 255.0)
        self.myGlyph.visible = True
        self.myLabel.position = (0.0, 0.0, 0.1)
        self.myGlyph.materialFX = 'BLEND'
        self.component.addChild(self.myGlyph, 'glyph')
        self.component.addChild(self.myLabel, 'label')
        self.updateChildren()

    def updateChildren(self):
        self.component.glyph.textureName = self.component.script.glyphTexture
        self.component.label.text = self.component.script.labelText

    def setLabel(self, txt):
        self.component.script.labelText = txt
        self.updateChildren()

    def setIcon(self, texture):
        self.component.script.glyphTexture = texture
        self.updateChildren()

    def setLabelColor(self, color = 4294967295L):
        a = color >> 24 & 255
        r = color >> 16 & 255
        g = color >> 8 & 255
        b = color & 255
        self.component.label.color = (r,
         g,
         b,
         a)

    def setGlyphColor(self, color = 4294967295L):
        a = color >> 24 & 255
        r = color >> 16 & 255
        g = color >> 8 & 255
        b = color & 255
        self.component.glyph.color = (r,
         g,
         b,
         a)


from soGUI.soToolTipComponent import soToolTipComponent

class soButtonWTT(soButton, soToolTipComponent):
    factoryString = 'soGUI.soButtonWTT'

    def __init__(self, component, TTid = None):
        soButton.__init__(self, component)
        soToolTipComponent.__init__(self, component, None)
        component.script = self
        self.toolTipID = TTid
        return

    def handleMouseEnterEvent(self, component):
        if self.buttonDisabled:
            return False
        soButton.handleMouseEnterEvent(self, component)
        soToolTipComponent.handleMouseEnterEvent(self, component)
        return True

    def handleMouseLeaveEvent(self, component):
        if self.buttonDisabled:
            return False
        soButton.handleMouseLeaveEvent(self, component)
        soToolTipComponent.handleMouseLeaveEvent(self, component)
        return True


class soButtonWFT(soButton):
    factoryString = 'soGUI.soButtonWFT'

    def __init__(self, component):
        soButton.__init__(self, component)
        component.script = self
        self._makeFrameTexture()

    def _makeFrameTexture(self):
        cmp = GUI.Frame2('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'frameTexture')

    def onBound(self):
        soButton.onBound(self)
        self.buttonIcon = self.component.frameTexture