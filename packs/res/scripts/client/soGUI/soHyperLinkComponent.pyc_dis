# Embedded file name: scripts/client/soGUI/soHyperLinkComponent.py
import BWPersonality
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import Keys
import Helpers.PyGUI.TextStyles as TextStyles
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
from soGUI.soVisualStateComponent import soVisualStateComponent
from soGUI.soToolTipComponent import soToolTipComponent
from Helpers.PyGUI.PyGUIBase import PyGUIBase
import Helpers.PyGUI.Utils

class soHLinkVisualState(VisualState):

    def __init__(self):
        VisualState.__init__(self)
        self.textStyle = ''

    def onSave(self, dataSection):
        pass

    def onLoad(self, dataSection):
        VisualState.onLoad(self, dataSection)
        self.r = dataSection.readInt('r', 0)
        self.g = dataSection.readInt('g', 0)
        self.b = dataSection.readInt('b', 0)
        self.a = dataSection.readInt('a', 0)

    def apply(self, componentScript):
        VisualState.apply(self, componentScript)
        if getattr(componentScript, 'component', None) is not None and componentScript.isText:
            componentScript.component.colour = (self.r,
             self.g,
             self.b,
             self.a)
        return


class soHyperLinkComponent(PyGUI.PyGUIBase, soVisualStateComponent, soToolTipComponent):
    factoryString = 'soGUI.soHyperLinkComponent'
    visualStateString = 'soGUI.soHLinkVisualState'
    NORMAL_STATE = 'normal'
    HOVER_STATE = 'hover'
    PRESSED_STATE = 'pressed'
    DISABLED_STATE = 'disabled'
    EVENT_LMB = 0
    EVENT_RMB = 1
    EVENT_CLICK = 2
    EVENT_RCLICK = 3

    def __init__(self, component):
        PyGUI.PyGUIBase.__init__(self, component)
        soVisualStateComponent.__init__(self, component, soHyperLinkComponent.visualStateString)
        soToolTipComponent.__init__(self, component, None)
        component.script = self
        self.isText = True
        self.isHovering = False
        self.isPressed = False
        self.isDisabled = False
        self.component.focus = True
        self.component.moveFocus = True
        self.component.crossFocus = True
        self.component.mouseButtonFocus = True
        self.hlinkID = None
        self.setupRoot()
        return

    def setupRoot(self):
        if hasattr(self.component, 'text'):
            self.isText = True
            self.component.text = self.component.text
        else:
            self.isText = False

    def onLmb(self):
        if self.hlinkID is not None:
            BWPersonality.GUICore.hlinkEvent(self.EVENT_LMB, [self.toolTipID, self.interfaceID])
        return

    def onRmb(self):
        if self.hlinkID is not None:
            BWPersonality.GUICore.hlinkEvent(self.EVENT_RMB, [self.toolTipID, self.interfaceID])
        return

    def onClick(self):
        if self.hlinkID is not None:
            BWPersonality.GUICore.hlinkEvent(self.EVENT_CLICK, [self.toolTipID, self.interfaceID])
        return

    def onRClick(self):
        if self.hlinkID is not None:
            BWPersonality.GUICore.hlinkEvent(self.EVENT_RCLICK, [self.toolTipID, self.interfaceID])
        return

    def setToolTip(self, id, iid = None):
        self.toolTipID = id
        self.interfaceID = iid

    def setLabel(self, txt):
        self.component.text = txt

    def setID(self, hlinkID):
        self.hlinkID = hlinkID

    def _updateVisualState(self):
        visualStateName = soHyperLinkComponent.NORMAL_STATE
        if self.isDisabled:
            visualStateName = soHyperLinkComponent.DISABLED_STATE
        elif self.isPressed and self.isHovering:
            visualStateName = soHyperLinkComponent.PRESSED_STATE
        elif self.isHovering:
            visualStateName = soHyperLinkComponent.HOVER_STATE
        self.setVisualState(visualStateName)

    def handleMouseButtonEvent(self, comp, event):
        hanled = PyGUIBase.handleMouseButtonEvent(self, comp, event)
        key = event.key
        down = event.isKeyDown()
        if self.isDisabled:
            return handled
        if key == Keys.KEY_LEFTMOUSE:
            if down and not self.isPressed:
                self.isPressed = True
                self.onLmb()
            elif not down and self.isPressed:
                self.isPressed = False
                self.onClick()
        if key == Keys.KEY_RIGHTMOUSE:
            if down and not self.isPressed:
                self.isPressed = True
                self.onRmb()
            elif not down and self.isPressed:
                self.isPressed = False
                self.onRClick()
        self._updateVisualState()
        return True

    def handleMouseEnterEvent(self, comp):
        PyGUIBase.handleMouseEnterEvent(self, comp)
        soToolTipComponent.handleMouseEnterEvent(self, comp)
        self.isPressed = self.isPressed and BigWorld.isKeyDown(Keys.KEY_LEFTMOUSE)
        self.isHovering = True
        self._updateVisualState()
        return True

    def handleMouseLeaveEvent(self, comp):
        soToolTipComponent.handleMouseLeaveEvent(self, comp)
        self.isHovering = False
        self._updateVisualState()
        return True