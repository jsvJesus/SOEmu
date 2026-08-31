# Embedded file name: scripts/client/soGUI/soActionBar.py
import BigWorld
import GUI
import BWPersonality
import Keys
import Helpers.PyGUI as PyGUI
import Helpers.BWKeyBindings as BWKeyBindings
import Helpers.Listener as Listener
from Helpers.BWKeyBindings import BWKeyBindingAction
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
import soGUI
from soGUI.soButton import soButton
from functools import partial

class soActionBar(PyGUI.Window, BWKeyBindings.BWActionHandler, Listener.Listenable):
    factoryString = 'soGUI.soActionBar'
    ACTION_USE = 0
    ACTION_DROP = 1
    SLOTW = 128
    SLOTH = 64
    SLOT_INTERVAL = 0

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        BWPersonality.gpd.keyBindings.addHandler(self)
        BWKeyBindings.BWActionHandler.setupActionList(self)
        component.script = self
        self.actionButtons = {}
        self.barPlacement = 'CENTER'
        self.numSlots = 4
        self.setupRoot()
        self.setupBtns()
        self.setupFrames()

    def setupRoot(self):
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.verticalAnchor = 'BOTTOM'
        self.component.horizontalAnchor = self.barPlacement
        self.component.textureName = ''
        self.component.height = soActionBar.SLOTH
        self.component.width = soActionBar.SLOTW * self.numSlots + soActionBar.SLOT_INTERVAL * (self.numSlots - 1)
        self.component.position = (0.05, -1.0, 0.0)

    def setupBtns(self):
        pixelW = soGUI.getPixelWidth(self.component)
        pixelH = soGUI.getPixelHeight(self.component)
        for i in xrange(7):
            btn = soButton(GUI.Window())
            btnCmp = btn.component
            btnCmp.verticalPositionMode = btnCmp.horizontalPositionMode = 'CLIP'
            btnCmp.widthMode = btnCmp.heightMode = 'PIXEL'
            btnCmp.horizontalAnchor = 'LEFT'
            btnCmp.verticalAnchor = 'CENTER'
            btnCmp.width = soActionBar.SLOTW
            btnCmp.height = soActionBar.SLOTH
            btnCmp.position = (-1.0 + pixelW * i * (self.SLOTW + self.SLOT_INTERVAL), 0.0, 0.0)
            btnCmp.label.colour = (255, 255, 65, 255)
            btnCmp.label.verticalAnchor = 'BOTTOM'
            btnCmp.label.position = (0.0, -1.0, 0.0)
            btnCmp.textureName = ''
            self.actionButtons[i] = btn

        for btn in self.actionButtons:
            self.actionButtons[btn].initVSC('soGUI/visual_styles/actionButton.xml')
            self.actionButtons[btn].setVisualState('normal')
            self.actionButtons[btn].onBound()
            self.component.addChild(self.actionButtons[btn].component, 'slot' + str(btn))

    def setupFrames(self):
        pixelW = soGUI.getPixelWidth(self.component)
        pixelH = soGUI.getPixelHeight(self.component)
        for i in xrange(1, 4):
            frameCmp = GUI.Frame2('soGUI/maps/Controls/window_frame/genericFrame.tga')
            frameCmp.verticalPositionMode = frameCmp.horizontalPositionMode = 'CLIP'
            frameCmp.widthMode = frameCmp.heightMode = 'PIXEL'
            frameCmp.horizontalAnchor = 'LEFT'
            frameCmp.verticalAnchor = 'CENTER'
            frameCmp.width = soActionBar.SLOTW
            frameCmp.height = soActionBar.SLOTH
            frameCmp.position = (-1.0 + pixelW * i * (self.SLOTW + self.SLOT_INTERVAL), 0.0, 0.0)
            frameCmp.colour = (255, 255, 255, 255)
            frameCmp.materialFX = 'BLEND'
            self.component.addChild(frameCmp)

    def onBound(self):
        PyGUI.Window.onBound(self)

    def setItems(self, newVal):
        for i in xrange(4):
            if i + 1 in newVal:
                if newVal[i + 1][0] != 'empty':
                    tex = newVal[i + 1][0]
                    cnt = newVal[i + 1][1]
                    self.component.__getattribute__('slot' + str(i + 1)).glyph.widthMode = 'CLIP'
                    self.component.__getattribute__('slot' + str(i + 1)).glyph.heightMode = 'CLIP'
                    self.component.__getattribute__('slot' + str(i + 1)).glyph.width = 2.0
                    self.component.__getattribute__('slot' + str(i + 1)).glyph.height = 2.0
                    self.component.__getattribute__('slot' + str(i + 1)).glyph.textureName = tex
                    if cnt > 0:
                        self.component.__getattribute__('slot' + str(i + 1)).label.text = str(cnt)
                    else:
                        self.component.__getattribute__('slot' + str(i + 1)).label.text = ''
                else:
                    self.component.__getattribute__('slot' + str(i + 1)).glyph.textureName = ''
                    self.component.__getattribute__('slot' + str(i + 1)).label.text = ''

    @BWKeyBindingAction('AB_DropSlot1', 1, ACTION_DROP)
    @BWKeyBindingAction('AB_DropSlot2', 2, ACTION_DROP)
    @BWKeyBindingAction('AB_DropSlot3', 3, ACTION_DROP)
    @BWKeyBindingAction('AB_DropSlot4', 4, ACTION_DROP)
    @BWKeyBindingAction('AB_DropSlot5', 5, ACTION_DROP)
    @BWKeyBindingAction('AB_DropSlot6', 6, ACTION_DROP)
    @BWKeyBindingAction('AB_DropSlot7', 7, ACTION_DROP)
    @BWKeyBindingAction('AB_Slot1', 1, ACTION_USE)
    @BWKeyBindingAction('AB_Slot2', 2, ACTION_USE)
    @BWKeyBindingAction('AB_Slot3', 3, ACTION_USE)
    @BWKeyBindingAction('AB_Slot4', 4, ACTION_USE)
    @BWKeyBindingAction('AB_Slot5', 5, ACTION_USE)
    @BWKeyBindingAction('AB_Slot6', 6, ACTION_USE)
    @BWKeyBindingAction('AB_Slot7', 7, ACTION_USE)
    def actionBarCommence(self, slot, action, isDown = True):
        if isDown:
            self.listeners.actionBarEvent(slot, action)


class soActionButton(PyGUI.Window):
    factoryString = 'soGUI.soActionButton'

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        self.component.script = self
        self.myLabel = None
        self.myIcon = None
        self.myCounter = None
        return

    def setEmpty(self):
        self.component.textureName = 'soGUI/maps/ActionButton.tga'
        self.myIcon.textureName = ''
        self.myCounter.text = ''