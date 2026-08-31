# Embedded file name: scripts/client/soGUI/soResizeComponent.py
import BigWorld
import GUI
import BWPersonality
from Keys import *

class soResizeComponent(object):
    factoryString = 'soGUI.soResizeComponent'

    def __init__(self, component, horizontal = True, vertical = True, width = 20, height = 20):
        component.script = self
        self.component = component
        self.horizontalResize = horizontal
        self.verticalResize = vertical
        self.width = width
        self.height = height
        self.resizing = False
        self.sizingBox = None
        self.setupResizer()
        return

    def setupResizer(self):
        cmp = GUI.Window('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.width
        cmp.height = self.height
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0.0, 0.0, 0.1)
        cmp.dragFocus = True
        cmp.crossFocus = True
        cmp.script = self
        self.component.addChild(cmp, 'resizer')
        cmp = GUI.Frame2('soGUI/maps/Misc/resizeBox.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 0.0
        cmp.height = 0.0
        cmp.position = (0.0, 0.0, 0.05)
        self.sizingBox = cmp

    def mouseHook(self, event):
        self.onResizing(event.cursorPosition)
        return True

    def onResizing(self, pos):
        return None

    def handleMouseEnterEvent(self, cmp):
        if cmp != self.component.resizer:
            return False
        cursorT = 'resizeHV'
        if self.verticalResize and not self.horizontalResize:
            cursorT = 'resizeV'
        if self.horizontalResize and not self.verticalResize:
            cursorT = 'resizeH'
        GUI.mcursor().shape = cursorT
        return True

    def handleMouseLeaveEvent(self, cmp):
        if cmp != self.component.resizer:
            return False
        if not self.resizing:
            GUI.mcursor().shape = 'arrow'
        return True

    def handleDragStartEvent(self, cmp):
        if cmp == self.component.resizer:
            self.resizeStart()
            return True
        return False

    def handleDragStopEvent(self, cmp):
        if cmp == self.component.resizer:
            self.resizeFinish()
            return True
        return False

    def resizeStart(self):
        self.resizing = True
        BWPersonality.GUICore.registerDnDHook(self.mouseHook)
        self.onResizeStart()

    def resizeFinish(self):
        self.resizing = False
        GUI.mcursor().shape = 'arrow'
        if self.sizingBox.parent is BWPersonality.GUICore.generalLayer:
            BWPersonality.GUICore.generalLayer.delChild(self.sizingBox)
        BWPersonality.GUICore.registerDnDHook(None)
        self.onResizeFinish()
        return

    def onResizeStart(self):
        return None

    def onResizeFinish(self):
        return None

    def drawResizeBox(self, start, size):
        self.sizingBox.position.x = start[0]
        self.sizingBox.position.y = start[1]
        self.sizingBox.width = size[0]
        self.sizingBox.height = size[1]
        if self.sizingBox.parent is None:
            BWPersonality.GUICore.generalLayer.addChild(self.sizingBox, 'resizingFrame')
        return