# Embedded file name: scripts/client/soGUI/soPanComponent.py
import BigWorld
import GUI
import BWPersonality
import Helpers.PyGUI as PyGUI
import soGUI
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Keys import *

class soPanComponent(object):
    factoryString = 'soGUI.soPanComponent'

    def __init__(self, component, panProxy = None):
        self.component = component
        self.topLeft = (0.0, 0.0)
        self.downRight = (0.0, 0.0)
        self.panning = False
        if panProxy is None:
            self.panProxy = component
        else:
            self.panProxy = panProxy
        soPanComponent.setupRoot(self)
        return

    def setupRoot(self):
        self.component.dragFocus = False
        self.component.moveFocus = True
        self.component.crossFocus = True

    def setPanInfo(self, topLeft = (0.0, 0.0), downRight = (0.0, 0.0)):
        self.topLeft = topLeft
        self.downRight = downRight

    def handleMouseEvent(self, comp, event):
        dx = event.dx
        dy = event.dy
        dz = event.dz
        position = event.cursorPosition
        if self.panning:
            sW, sH = BigWorld.screenSize()
            GUI.mcursor().shape = 'pan'
            if dx != 0:
                self.panProxy.scroll.x += 2.0 / (sW / dx)
            if dy != 0:
                self.panProxy.scroll.y -= 2.0 / (sH / dy)
        else:
            GUI.mcursor().shape = 'canPan'
        return True

    def handleMouseButtonEvent(self, comp, event):
        key = event.key
        down = event.isKeyDown()
        if key == KEY_LEFTMOUSE:
            if down:
                self.panning = True
                GUI.mcursor().shape = 'pan'
            else:
                self.panning = False
                GUI.mcursor().shape = 'canPan'
        return True

    def handleMouseEnterEvent(self, comp):
        GUI.mcursor().shape = 'canPan'
        return True

    def handleMouseLeaveEvent(self, comp):
        GUI.mcursor().shape = 'arrow'
        self.panning = False
        return True

    def handleDragStartEvent(self, *args):
        self.panning = True
        GUI.mcursor().shape = 'pan'
        return True

    def handleDragStopEvent(self, *args):
        self.panning = False
        GUI.mcursor().shape = 'arrow'
        return True