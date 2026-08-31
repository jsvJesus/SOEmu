# Embedded file name: scripts/client/soGUI/soDraggableComponent.py
import BigWorld
import GUI
import BWPersonality
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Math import Vector2, Vector3
import soGUI

class soDraggableComponent(object):

    def __init__(self, component, vDrag = True, hDrag = True, centerDProxy = False, autoCleanup = True):
        self.component = component
        component.script = self
        self.dragProxy = None
        self.proxyHolder = self.component
        self.proxyName = ''
        self.dragging = False
        self.dragProxyData = None
        self.currentOffset = (0.0, 0.0)
        self.constraints = [(0.0, 0.0), (0.0, 0.0)]
        self.vDrag = vDrag
        self.hDrag = hDrag
        self.restrictToComponent = None
        self.centerDProxy = centerDProxy
        self.autoCleanup = autoCleanup
        self._onDragStart = lambda : True
        self._onDragging = lambda : True
        self._onDragStop = lambda : True
        return

    def cleanupDragProxy(self):
        if self.dragProxy in GUI.roots():
            GUI.delRoot(self.dragProxy)
        self.dragProxy.horizontalPositionMode = self.dragProxyData[0]
        self.dragProxy.verticalPositionMode = self.dragProxyData[1]
        self.dragProxy.horizontalAnchor = self.dragProxyData[3]
        self.dragProxy.verticalAnchor = self.dragProxyData[4]
        self.proxyHolder.addChild(self.dragProxy, self.proxyName)
        self.dragProxy.position = self.dragProxyData[2]

    def handleMouseEvent(self, cmp, event):
        if not self._onDragging():
            return False
        if event.dx == 0 and event.dy == 0:
            return False
        if self.dragging:
            if self.hDrag:
                self.dragProxy.position.x = event.cursorPosition.x - self.currentOffset[0]
            if self.vDrag:
                self.dragProxy.position.y = event.cursorPosition.y - self.currentOffset[1]
            self.restrict()
        return True

    def updateConstraints(self):
        restrictCmp = self.restrictToComponent
        if restrictCmp is None:
            self.constraints = [(-1.0, 1.0), (1.0, -1.0)]
        else:
            oldWMode = restrictCmp.widthMode
            oldHMode = restrictCmp.heightMode
            restrictCmp.widthMode = restrictCmp.heightMode = 'PIXEL'
            leftTop = restrictCmp.localToScreen(Vector2(0, 0))
            rightBottom = restrictCmp.localToScreen(Vector2(restrictCmp.width, restrictCmp.height))
            restrictCmp.widthMode = oldWMode
            restrictCmp.heightMode = oldHMode
            self.constraints = [leftTop, rightBottom]
        return

    def handleDragStartEvent(self, cmp):
        if not self._onDragStart():
            return False
        mpos = GUI.mcursor().position
        legacyPos = self.component.localToScreen(Vector2(self.dragProxy.position.x, self.dragProxy.position.y))
        if self.component == self.dragProxy:
            legacyPos = self.proxyHolder.localToScreen((self.dragProxy.position.x, self.dragProxy.position.y))
        self.updateConstraints()
        self.dragging = True
        BWPersonality.GUICore.registerDnDHook(lambda event: self.handleMouseEvent(None, event))
        self.dragProxyData = [self.dragProxy.horizontalPositionMode,
         self.dragProxy.verticalPositionMode,
         Vector3(self.dragProxy.position),
         self.dragProxy.horizontalAnchor,
         self.dragProxy.verticalAnchor]
        self.dragProxy.horizontalPositionMode = self.dragProxy.verticalPositionMode = 'LEGACY'
        self.dragProxy.position.z = 0.0
        self.proxyHolder.delChild(self.dragProxy)
        self.dragProxy.position.x = legacyPos.x
        self.dragProxy.position.y = legacyPos.y
        if self.centerDProxy:
            self.dragProxy.horizontalAnchor = self.dragProxy.verticalAnchor = 'CENTER'
            self.dragProxy.position.x = mpos.x
            self.dragProxy.position.y = mpos.y
        else:
            hOffset = mpos.x - legacyPos.x
            vOffset = mpos.y - legacyPos.y
            self.currentOffset = (hOffset, vOffset)
        GUI.addRoot(self.dragProxy)
        return True

    def handleDragStopEvent(self, cmp):
        if not self.dragging:
            return False
        elif not self._onDragStop():
            return False
        else:
            self.dragging = False
            BWPersonality.GUICore.registerDnDHook(None)
            if self.autoCleanup:
                self.cleanupDragProxy()
            self.currentOffset = (0.0, 0.0)
            return True

    def restrict(self):
        lSize = [soGUI.getLegacyWidth(self.dragProxy), soGUI.getLegacyHeight(self.dragProxy)]
        zeroOffset = [lSize[0], lSize[1]]
        if self.dragProxy.horizontalAnchor == 'CENTER':
            lSize[0] /= 2.0
            zeroOffset[0] -= lSize[0]
        elif self.dragProxy.horizontalAnchor == 'RIGHT':
            lSize[0] = 0
            zeroOffset[0] -= lSize[0]
        elif self.dragProxy.horizontalAnchor == 'LEFT':
            zeroOffset[0] = 0
        if self.dragProxy.verticalAnchor == 'CENTER':
            lSize[1] /= 2.0
            zeroOffset[1] -= lSize[1]
        elif self.dragProxy.verticalAnchor == 'BOTTOM':
            lSize[1] = 0
            zeroOffset[1] -= lSize[1]
        elif self.dragProxy.verticalAnchor == 'TOP':
            zeroOffset[1] = 0
        if self.dragProxy.position.x < self.constraints[0][0] + zeroOffset[0]:
            self.dragProxy.position.x = self.constraints[0][0] + zeroOffset[0]
        if self.dragProxy.position.x > self.constraints[1][0] - lSize[0]:
            self.dragProxy.position.x = self.constraints[1][0] - lSize[0]
        if self.dragProxy.position.y > self.constraints[0][1] - zeroOffset[1]:
            self.dragProxy.position.y = self.constraints[0][1] - zeroOffset[1]
        if self.dragProxy.position.y < self.constraints[1][1] + lSize[1]:
            self.dragProxy.position.y = self.constraints[1][1] + lSize[1]

    def setRestrictingComponent(self, cmp):
        self.restrictToComponent = cmp
        self.updateConstraints()