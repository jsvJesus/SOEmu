# Embedded file name: scripts/client/soGUI/ScaleformDemo.py
import BigWorld
import GUI
import Scaleform
import Keys
import Helpers.PyGUI as PyGUI
import weakref
from bwdebug import *

class ScaleformDemo(PyGUI.PyGUIBase):
    calb = None
    ignoreHandleKeyEvent = False

    @staticmethod
    def create(movieName, backgroundAlpha):
        wde = BigWorld.worldDrawEnabled()
        BigWorld.worldDrawEnabled(False)
        view, movie = Scaleform.createMovieInstance(movieName)
        BigWorld.worldDrawEnabled(wde)
        if view is None:
            ERROR_MSG("Error loading Scaleform movie '%s'" % (movieName,))
            return
        else:
            view.backgroundAlpha = backgroundAlpha
            component = GUI.Flash(view)
            component.width = 1.0
            component.height = 1.0
            component.materialFX = 'BLEND'
            component.focus = True
            component.mouseButtonFocus = True
            component.crossFocus = True
            component.moveFocus = True
            component.dragFocus = True
            component.script = ScaleformDemo(component)
            component.script.viewX = view
            component.script.movieX = movie
            view.setExternalInterfaceCallback(component.script.exampleExternalInterfaceHandler)
            return component

    def setExternalInterfaceCallback(self, foo):
        self.viewX.setExternalInterfaceCallback(foo)

    def exampleExternalInterfaceHandler(self, cmd, args):
        if cmd == 'Luminance':
            self.viewX.backgroundAlpha = args[0][0]
        if self.calb:
            self.calb(cmd, args)

    def setCalback(self, calb):
        self.calb = calb

    def __init__(self, component):
        PyGUI.PyGUIBase.__init__(self, component)

    def handleKeyEvent(self, event):
        if self.ignoreHandleKeyEvent:
            return False
        return self.component.movie.handleKeyEvent(event)

    def handleMouseButtonEvent(self, comp, event):
        return self.component.movie.handleMouseButtonEvent(event)

    def handleMouseEvent(self, comp, event):
        return self.component.movie.handleMouseEvent(event)

    def allowAutoDefocus(self):
        return True