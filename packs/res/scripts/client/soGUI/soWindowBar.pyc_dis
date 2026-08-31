# Embedded file name: scripts/client/soGUI/soWindowBar.py
import traceback
import BigWorld
import BWPersonality
import GUI
import random
from soGUI.soButton import soButton, soButtonWTT
from Helpers.PyGUI.PyGUIBase import PyGUIBase

class soWindowBar(PyGUIBase):

    def __init__(self, component, width, height, mainClass):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.mainClass = mainClass
        self.width = width
        self.height = height
        self.windows = {}
        self._Blabels = {}
        self._buttons = []
        self._wbuttonsIDs = []
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = self.width
        cmp.height = self.height

    def setupContent(self):
        cmp = GUI.Simple('textures/default/bright_gray.jpg')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 255, 255, 128)
        cmp.materialFX = 'BLEND'
        cmp.width = self.component.width - 1
        cmp.height = 2
        cmp.position = (0, self.height, 0.9)
        cmp.visible = 1
        self.component.addChild(cmp, 'frame1')

    def addWindow(self, wID, saleWindow, saleName):
        if wID in self._wbuttonsIDs:
            return
        else:
            self.windows[wID] = (saleWindow, saleName)
            self._wbuttonsIDs.append(wID)
            self.rePlaceButton()
            saleWindow.w_onHide = self.onHide
            saleWindow.w_onClose = self.onClose
            saleWindow.w_onShow = self.onShow
            cmp = saleWindow.component
            if cmp.parent is None:
                self.mainClass.component.addChild(cmp, 'window_%s' % wID)
            return

    def delWindow(self, wID):
        self._wbuttonsIDs.remove(wID)
        del self.windows[wID]
        self.rePlaceButton()
        self.mainClass.component.delChild('window_%s' % wID)

    def rePlaceButton(self):
        for c in self._buttons:
            self.component.delChild(c)
            self.component.delChild('status_' + c)

        self._buttons = []
        bwidth = self.width / (len(self._wbuttonsIDs) + 0.1)
        bwidth = min(250, bwidth)
        for i, wID in enumerate(self._wbuttonsIDs):
            saleWindow, saleName = self.windows[wID]
            btn = soButton(GUI.Window())
            cmp = btn.component
            btn.initVSC('soGUI/visual_styles/skillTab.xml')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.label.text = saleName
            cmp.width = bwidth
            cmp.height = 22
            cmp.position = (i * bwidth, 25, 0.4)
            bname = 'button_w_%s' % i
            self.component.addChild(cmp, bname)
            self._buttons.append(bname)
            cmp.script.onClick = lambda wID = wID: self.onBClick(wID)
            btn.onBound()
            board = 16
            if bwidth <= board * 2:
                board = 0
            cmp = GUI.Simple('textures/default/bright_gray.jpg')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.colour = (255, 255, 255, 150)
            cmp.materialFX = 'BLEND'
            cmp.width = bwidth - board * 2
            cmp.height = 2
            cmp.position = (i * bwidth + board, 27, 0.4)
            cmp.visible = saleWindow.component.visible
            self._Blabels[wID] = cmp
            self.component.addChild(cmp, 'status_' + bname)

    def onBClick(self, wID):
        saleWindow, saleName = self.windows[wID]
        saleWindow.component.visible = not saleWindow.component.visible
        width, height = (400, 256)
        if saleWindow.component.visible:
            saleWindow.component.position = (width, height, 0.08)
            saleWindow.show()
            self.topWindow(wID)
        cmp = self._Blabels[wID]
        cmp.visible = saleWindow.component.visible

    def topWindow(self, wID):
        for _wID in self._wbuttonsIDs:
            saleWindow, saleName = self.windows[_wID]
            x, y, z = saleWindow.component.position
            z = 0.0 if _wID == wID else 0.09
            saleWindow.component.position = (x, y, z)

    def getWindowByID(self, wID):
        if wID in self._wbuttonsIDs:
            saleWindow, saleName = self.windows[wID]
            return saleWindow
        else:
            return None

    def onHide(self, wID):
        cmp = self._Blabels[wID]
        cmp.visible = False

    def onShow(self, wID):
        cmp = self._Blabels[wID]
        cmp.visible = True

    def onClose(self, wID):
        self.delWindow(wID)