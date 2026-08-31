# Embedded file name: scripts/client/soGUI/soContextMenuComponent.py
import Helpers.PyGUI as PyGUI
import BigWorld
import GUI
import soGUI
import BWPersonality
from soGUI.soList import soList
from soGUI.soButton import soButton
from functools import partial
from Items import ItemsCatalog
import ItemsUtils
from Keys import *

class soContextMenuElement(soButton):
    factoryString = 'soGUI.soContextMenuElement'

    def __init__(self, component, id, menuObject):
        soButton.__init__(self, component)
        component.script = self
        self.menuObject = menuObject
        self.actionId = id

    def handleMouseEnterEvent(self, comp):
        soButton.handleMouseEnterEvent(self, comp)
        self.menuObject.captureCursor(True)
        return True

    def handleMouseLeaveEvent(self, comp):
        soButton.handleMouseLeaveEvent(self, comp)
        self.menuObject.captureCursor(False)
        return True


class soContextMenuComponent(PyGUI.Window):
    LEFT_OFFSET = 4
    TOP_OFFSET = 4
    LABEL_LEFT_OFFSET = 5
    ELEMENT_HEIGHT = 20
    ELEMENT_INTERVAL = 0
    FONT_NAME = 'ruRU_calibri_default.font'
    FRAME_TEXTURE = 'soGUI/maps/con_frame.tga'
    EVENT_SELECT = 0
    EVENT_SHOW = 1
    EVENT_CANCEL = 2
    isVisible = True

    def __init__(self, component, actions, iid):
        PyGUI.Window.__init__(self, component)
        self.actions = actions
        self.iid = iid
        component.script = self
        self.cursorCapture = False
        self.elemBtns = []
        self.setupRoot()
        self.setupFrame()
        self.setupActions()
        self.contextIgnoreKeys = [KEY_LEFTMOUSE, KEY_RIGHTMOUSE]
        BWPersonality.GUICore.contextMenuEvent(iid, None, None, self.EVENT_SHOW)
        return

    def getMaxWidth(self):
        maxWidth = 50
        for action in self.actions:
            testString = GUI.Text('')
            testString.font = soContextMenuComponent.FONT_NAME
            actionWidth = testString.stringWidth(self.actions[action])
            if actionWidth > maxWidth:
                maxWidth = actionWidth

        return maxWidth

    def setupRoot(self):
        maxWidth = self.getMaxWidth()
        mouseX, mouseY = GUI.mcursor().position
        self.component.verticalPositionMode = self.component.horizontalPositionMode = 'LEGACY'
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.width = soContextMenuComponent.LABEL_LEFT_OFFSET * 2 + soContextMenuComponent.LEFT_OFFSET * 2 + maxWidth
        self.component.height = soContextMenuComponent.TOP_OFFSET * 2 + soContextMenuComponent.ELEMENT_INTERVAL * (len(self.actions) - 1) + soContextMenuComponent.ELEMENT_HEIGHT * len(self.actions)
        if soGUI.getLegacyWidth(self.component) + mouseX > 1.0:
            self.component.horizontalAnchor = 'RIGHT'
        else:
            self.component.horizontalAnchor = 'LEFT'
        if soGUI.getLegacyHeight(self.component) - mouseY < -1.0:
            self.component.verticalAnchor = 'BOTTOM'
        else:
            self.component.verticalAnchor = 'TOP'
        self.component.position = (mouseX, mouseY, 0)
        self.component.textureName = ''
        self.component.colour = (255, 255, 255, 255)
        self.component.materialFX = 'BLEND'
        self.component.visible = True
        self.component.crossFocus = True
        self.component.dragFocus = True
        GUI.addRoot(self.component)

    def setupFrame(self):
        mainFrame = GUI.Frame2(soContextMenuComponent.FRAME_TEXTURE)
        mainFrame.horizontalPositionMode = mainFrame.verticalPositionMode = 'CLIP'
        mainFrame.widthMode = mainFrame.heightMode = 'CLIP'
        mainFrame.horizontalAnchor = 'LEFT'
        mainFrame.verticalAnchor = 'BOTTOM'
        mainFrame.width = 2.0
        mainFrame.height = 2.0
        mainFrame.position = (-1.0, -1.0, 0.1)
        mainFrame.colour = (255, 255, 255, 255)
        mainFrame.materialFX = 'BLEND'
        self.component.addChild(mainFrame, 'theFrame')

    def setupActions(self):
        for elem in self.elemBtns:
            self.component.delChild(elem.component)

        elemWidth = self.getMaxWidth() + soContextMenuComponent.LEFT_OFFSET * 2
        i = 0
        akeys = self.actions.keys()
        akeys.sort()
        for action in akeys:
            btn = soContextMenuElement(GUI.Window(), action, self)
            cmp = btn.component
            cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'TOP'
            cmp.width = elemWidth
            cmp.height = self.ELEMENT_HEIGHT
            btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
            cmp.position = (0.0, 1.0 - soGUI.getPixelHeight(self.component) * (self.TOP_OFFSET + self.ELEMENT_HEIGHT * i), 0.0)
            btn.onBound()
            btn.component.label.position = (-1.0 + soGUI.getPixelWidth(cmp) * self.LABEL_LEFT_OFFSET, 0.0, 0.0)
            btn.component.label.horizontalAnchor = 'LEFT'
            btn.component.label.font = self.FONT_NAME
            btn.component.label.text = self.actions[action]
            self.component.addChild(cmp)
            btn.setVisualState('normal')
            btn.onClick = partial(self.onElement, self.iid, btn.actionId, self.actions[action], self.EVENT_SELECT)
            self.elemBtns.append(btn)
            i += 1

    def onElement(self, iid, id, caption, event):
        BWPersonality.GUICore.contextMenuEvent(iid, id, caption, event)
        self.hide(False)

    def showMenu(self, actions, iid):
        self.isVisible = True
        self.actions = actions
        self.iid = iid
        self.setupRoot()
        self.setupFrame()
        self.setupActions()
        BWPersonality.GUICore.contextMenuEvent(iid, None, None, self.EVENT_SHOW)
        return

    def hide(self, nonuser = True):
        self.isVisible = False
        self.actions = {}
        self.component.visible = False
        if nonuser:
            BWPersonality.GUICore.contextMenuEvent(self.iid, None, None, self.EVENT_CANCEL)
        return

    def handleMouseEnterEvent(self, comp):
        self.cursorCapture = True
        return True

    def handleAxisEvent(self, *e):
        print 'handleAxisEvent', e

    def handleMouseEvent(self, *e):
        print 'handleMouseEvent', e

    def handleMouseLeaveEvent(self, comp):
        self.cursorCapture = False
        return True

    def captureCursor(self, captured):
        if captured:
            self.cursorCapture = True
        else:
            self.cursorCapture = False