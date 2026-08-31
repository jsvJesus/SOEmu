# Embedded file name: scripts/client/soGUI/soMessageBoxGUI.py
import BigWorld
import GUI
import BWPersonality
import soGUI
from Helpers.PyGUI import PyGUIBase
from gui_const import MESSAGEBOX
from soGUI.soEditField import soEditBox
from soGUI.soCheckBox import soCheckBox
from soGUI.soRadioButton import soRadioButton2
from soGUI.soTextField import soTextField3
from random import randint
from time import time
import ResMgr
from Helpers.PyGUI import PyGUIEvent
from soGUI import soButton, soButtonWTT
from functools import partial
from soDraggableComponent import soDraggableComponent
from gui_const import GUI_ID
from Helpers.BWCoroutine import *
from Localization import lc

def getBtnLabel(btn):
    if btn == MESSAGEBOX.BTN_OK:
        return lc('GUI.MessageBoxes.OK_BUTTON_LABEL')
    if btn == MESSAGEBOX.BTN_CANCEL:
        return lc('GUI.MessageBoxes.CANCEL_BUTTON_LABEL')
    if btn == MESSAGEBOX.BTN_YES:
        return lc('GUI.MessageBoxes.YES_BUTTON_LABEL')
    if btn == MESSAGEBOX.BTN_NO:
        return lc('GUI.MessageBoxes.NO_BUTTON_LABEL')
    if btn == MESSAGEBOX.BTN_UNDO:
        return lc('GUI.MessageBoxes.UNDO_BUTTON_LABEL')
    if btn == MESSAGEBOX.BTN_APPLY:
        return lc('GUI.MessageBoxes.APPLY_BUTTON_LABEL')
    if btn == MESSAGEBOX.BTN_RESET:
        return lc('GUI.MessageBoxes.RESET_BUTTON_LABEL')
    if btn == MESSAGEBOX.BTN_CONFIRM:
        return lc('GUI.MessageBoxes.CONFIRM_BUTTON_LABEL')
    if btn == MESSAGEBOX.BTN_SAVE:
        return lc('GUI.MessageBoxes.SAVE_BUTTON_LABEL')
    return lc('GUI.MessageBoxes.SAVE_BUTTON_LABEL')


def isClosingBtn(btn):
    if btn in [MESSAGEBOX.BTN_OK,
     MESSAGEBOX.BTN_CANCEL,
     MESSAGEBOX.BTN_YES,
     MESSAGEBOX.BTN_NO,
     MESSAGEBOX.BTN_CONFIRM]:
        return True
    return False


class soMsgBoxMgr(PyGUIBase):
    MIN_DEPTH = 0.0
    MAX_DEPTH = 1.0

    def __init__(self):
        self.modalState = False
        self.msgBoxes = {}
        self.msgBoxesOrder = []
        self.generalRenderPlane = None
        self.systemRenderPlane = None
        self.msgHistory = {}
        self.setupRenderPlanes()
        self.loadHistory()
        PyGUIBase.__init__(self, self.generalRenderPlane)
        return

    def setupRenderPlanes(self):
        cmp = GUI.Window('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.06)
        cmp.script = self
        BWPersonality.GUICore.generalLayer.addChild(cmp, 'msgBoxRenderPlane')
        self.generalRenderPlane = cmp
        cmp = GUI.Window('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.06)
        cmp.script = self
        BWPersonality.GUICore.systemLayer.addChild(cmp, 'msgBoxRenderPlane')
        self.systemRenderPlane = cmp

    def loadHistory(self):
        historyFile = None
        if not ResMgr.isFile('../../game/dlgBoxHistory.xml'):
            ds = ResMgr.openSection('../../game')
            historyFile = ds.createSection('dlgBoxHistory.xml')
            historyFile.save()
        else:
            historyFile = ResMgr.openSection('../../game/dlgBoxHistory.xml')
        for msgBox in historyFile.values():
            self.msgHistory[msgBox.readString('id')] = [msgBox.readFloat('x'), msgBox.readFloat('y')]

        return

    def saveHistory(self):
        return
        historyFile = None
        if not ResMgr.isFile('../../game/dlgBoxHistory.xml'):
            ds = ResMgr.openSection('../../game')
            historyFile = ds.createSection('dlgBoxHistory.xml')
            historyFile.save()
        else:
            historyFile = ResMgr.openSection('../../game/dlgBoxHistory.xml')
        for msgBox in historyFile.values():
            historyFile.deleteSection(msgBox)

        for msgID in self.msgBoxes:
            self.msgHistory[msgID] = [self.msgBoxes[msgID].component.position.x, self.msgBoxes[msgID].component.position.y]

        for msgID in self.msgHistory:
            ds = historyFile.createSection('msg_box')
            ds.writeString('id', msgID)
            ds.writeFloat('x', self.msgHistory[msgID][0])
            ds.writeFloat('y', self.msgHistory[msgID][1])

        historyFile.save()
        return

    def updateModalState(self):
        modalID = None
        for msgID in self.msgBoxesOrder:
            if self.msgBoxes[msgID].isModal:
                modalID = msgID

        if modalID is not None:
            self.setActiveMsgBox(msgID)
            self.goModal(True)
        else:
            self.goModal(False)
        return

    def goModal(self, goModal = True):
        self.modalState = goModal
        self.generalRenderPlane.crossFocus = goModal
        self.generalRenderPlane.mouseButtonFocus = goModal
        self.generalRenderPlane.moveFocus = goModal
        self.generalRenderPlane.dragFocus = goModal
        self.generalRenderPlane.dropFocus = goModal

    def setActiveMsgBox(self, id):
        if self.modalState:
            return False
        elif self.msgBoxes.has_key(id):
            self.msgBoxesOrder.remove(id)
            self.msgBoxesOrder.append(id)
            self.updateDepth()
            return True
        else:
            return False

    def addMsgBox(self, msgBox):
        if self.msgBoxes.has_key(msgBox.msgBoxID):
            return False
        else:
            self.msgBoxes[msgBox.msgBoxID] = msgBox
            msgBox.msgBoxEvent = self.msgBoxEventRepeater
            self.msgBoxesOrder.append(msgBox.msgBoxID)
            renderPlane = self.generalRenderPlane
            if msgBox.isSystem:
                renderPlane = self.systemRenderPlane
            renderPlane.addChild(msgBox.component, 'msgBox_{0}'.format(msgBox.msgBoxID))
            if not msgBox.forcePos:
                if self.msgHistory.has_key(msgBox.msgBoxID):
                    msgBox.setPos(self.msgHistory[msgBox.msgBoxID][0], self.msgHistory[msgBox.msgBoxID][1])
                else:
                    self.msgHistory[msgBox.msgBoxID] = [msgBox.x, msgBox.y]
            self.updateDepth()
            self.updateModalState()
            BWPersonality.GUICore.setBestCursor()
            return True

    def delMsgBox(self, id):
        if self.msgBoxes.has_key(id):
            self.msgHistory[id] = [self.msgBoxes[id].component.position.x, self.msgBoxes[id].component.position.y]
            msgBox = self.msgBoxes[id]
            renderPlane = self.generalRenderPlane
            if msgBox.isSystem:
                renderPlane = self.systemRenderPlane
            renderPlane.delChild('msgBox_{0}'.format(id))
            self.msgBoxes[id].fini()
            del self.msgBoxes[id]
            self.msgBoxesOrder.remove(id)
            self.updateDepth()
            self.updateModalState()
            BWPersonality.GUICore.setBestCursor()
            return True
        else:
            return False

    def getDnDHolderPlane(self, msgBox):
        if msgBox.isSystem:
            return self.systemRenderPlane
        return self.generalRenderPlane

    def setAddControlData(self, msgBoxID, controlID, data):
        if self.msgBoxes.has_key(msgBoxID):
            self.msgBoxes[msgBoxID].setAddControlData(controlID, data)

    def setBtnData(self, msgBoxID, btn_type, data):
        if self.msgBoxes.has_key(msgBoxID):
            self.msgBoxes[msgBoxID].setBtnData(btn_type, data)

    def updateDepth(self):
        for index, msgID in enumerate(self.msgBoxesOrder):
            cmp = getattr(self.generalRenderPlane, 'msgBox_{0}'.format(msgID), None)
            if cmp:
                cmp.position.z = self.MAX_DEPTH - (self.MAX_DEPTH - self.MIN_DEPTH) / (len(self.msgBoxes) * 1.0) * index
                GUI.reSort()

        return

    def onGameModeChange(self, mode):
        ids = self.msgBoxes.keys()
        for msgID in ids:
            self.msgBoxes[msgID].internalClose()

    def msgBoxEventRepeater(self, event, data):
        BWPersonality.GUICore.msgBoxEvent(event, data)
        if event == MESSAGEBOX.EVENT_BTNPRESS:
            boxId = data['id']
            btn = data['btn']
            if isClosingBtn(btn):
                self.delMsgBox(boxId)
        if event == MESSAGEBOX.EVENT_CLOSE or event == MESSAGEBOX.EVENT_CLOSE_NONUSER:
            boxId = data['id']
            self.delMsgBox(boxId)

    def updateParentVisibility(self):
        ids = self.msgBoxes.keys()
        for msgID in ids:
            if self.msgBoxes[msgID].parentGUI is not None:
                if self.msgBoxes[msgID].parentGUI not in BWPersonality.GUICore.getGUIMap(return_id=True):
                    self.msgBoxes[msgID].internalClose()

        return

    def onEscapeKey(self):
        ids = self.msgBoxes.keys()
        handled = False
        if ids:
            for msgID in ids:
                handled = self.msgBoxes[msgID].onEscapeKey()

        return handled

    def onReturnKey(self):
        if self.msgBoxesOrder:
            return self.msgBoxes[self.msgBoxesOrder[-1]].onReturnKey()

    def handleMouseEvent(self, comp, event):
        return True

    def handleMouseButtonEvent(self, comp, event):
        return True

    def handleMouseClickEvent(self, component):
        return True

    def handleMouseEnterEvent(self, comp):
        return True

    def handleMouseLeaveEvent(self, comp):
        return True

    def handleDragStartEvent(self, comp):
        return True

    def handleDragStopEvent(self, comp):
        return True

    def handleDragEnterEvent(self, comp, dragged):
        return True

    def handleDragLeaveEvent(self, comp, dragged):
        return True

    def handleDropEvent(self, comp, dropped):
        return True

    def fini(self):
        self.saveHistory()


class soMessageBox(PyGUIBase, soDraggableComponent):
    factoryString = 'soGUI.soMessageBox'
    LEFT_ORIGIN = 20
    TOP_ORIGIN = 41
    ADDS_INTERVAL = 5

    def __init__(self, component, id, isModal, x, y, width, caption, forcePos, parent_gui_id, bind_to_parent, btn_set, timeout, closeBox, defaultAction, addControls, callback = lambda event, data: None, system = False):
        PyGUIBase.__init__(self, component)
        soDraggableComponent.__init__(self, component, centerDProxy=False, autoCleanup=False)
        component.script = self
        self.x = x
        self.y = y
        self.width = width
        self.height = 0
        self.caption = caption
        self.forcePos = forcePos
        self.addControls = addControls
        self.btns = btn_set
        self.parentGUI = parent_gui_id
        self.msgBoxID = id
        self.timeout = timeout
        self.defaultAction = defaultAction
        self.closeBox = closeBox
        self.isModal = isModal
        self.callback = callback
        self.parentBind = bind_to_parent
        self.isSystem = system
        self.controlWidth = self.width - self.LEFT_ORIGIN * 2
        self.autoHeight = True if self.height <= 0 else False
        self.ticker = None
        self.dragProxy = self.component
        self.proxyHolder = BWPersonality.GUICore.msgBoxMgr.getDnDHolderPlane(self)
        self.proxyName = 'msgBox_{0}'.format(self.msgBoxID)
        self._onDragStop = self.onDragStop
        self.setupRoot()
        self.setupContent()
        self.setupAddControls()
        self.setupBtns()
        self.updateBinding()
        if self.timeout > 0:
            self.ticker = self.timeoutTicker()
            self.ticker.run()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        if isinstance(self.x, int):
            cmp.horizontalPositionMode = 'PIXEL'
        if isinstance(self.y, int):
            cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = self.width
        cmp.height = self.height
        cmp.position.x = self.x
        cmp.position.y = self.y
        cmp.position.z = 0.5
        cmp.mouseButtonFocus = True
        cmp.dragFocus = True
        cmp.moveFocus = True

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/msgBox/windowFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'dFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.multiline = False
        cmp.colourFormatting = False
        cmp.text = self.caption
        cmp.position = (18, 15, 0.8)
        self.component.addChild(cmp, 'caption')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = 'PIXEL'
        cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = self.width
        cmp.height = 28
        cmp.position = (0.0, 1.0, 0.3)
        cmp.dragFocus = True
        cmp.moveFocus = True
        cmp.script = self
        self.component.addChild(cmp, 'dragPlane')

    def setupAddControls(self):
        lastHeight = self.TOP_ORIGIN
        for addControl in self.addControls:
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_EDIT:
                lastHeight += self._makeEdit(addControl, lastHeight) + self.ADDS_INTERVAL
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_CHECKBOX:
                lastHeight += self._makeCheckBox(addControl, lastHeight) + self.ADDS_INTERVAL
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_RADIO:
                lastHeight += self._makeRadio(addControl, lastHeight) + self.ADDS_INTERVAL
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_TEXTFIELD:
                lastHeight += self._makeText(addControl, lastHeight) + self.ADDS_INTERVAL
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_LABEL:
                lastHeight += self._makeLabel(addControl, lastHeight) + self.ADDS_INTERVAL
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_SPACING_T1:
                lastHeight += self._makeSpacing1(addControl, lastHeight) + self.ADDS_INTERVAL
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_SPACING_T2:
                lastHeight += self._makeSpacing2(addControl, lastHeight) + self.ADDS_INTERVAL
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_LIST:
                print 'soMessageBox::_makeList is NYI'
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_DDL:
                print 'soMessageBox::_makeDDL is NYI'
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_SLIDER:
                print 'soMessageBox::_makeSlider is NYI'

        self.component.height = lastHeight + 15

    def setupBtns(self):
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/closeBox.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (self.width - 6, 6, 0.2)
        self.component.addChild(cmp, 'closeBox')
        btn.onClick = self.onCloseBoxClick
        btn.onBound()
        btn.buttonDisabled = not self.closeBox
        btn._updateVisualState()
        cmp.dragFocus = True
        if len(self.btns) > 0:
            self.component.height += 29
        for index, btn_ in enumerate(self.btns):
            btn = soButton(GUI.Window())
            btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
            cmp = btn.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            btnWidth = (self.controlWidth - (len(self.btns) + 1) * 10) / (len(self.btns) * 1.0)
            if btn_.has_key('width'):
                if btn_['width'] > 0:
                    btnWidth = btn_['width']
            cmp.width = btnWidth
            cmp.height = 29
            if btn_.has_key('caption'):
                cmp.label.text = btn_['caption']
            else:
                cmp.label.text = getBtnLabel(btn_['type'])
            if btn_.has_key('enabled'):
                btn.buttonDisabled = not btn_['enabled']
            hPos = self.LEFT_ORIGIN + self.controlWidth / (len(self.btns) * 1.0) * index + self.controlWidth / (len(self.btns) * 1.0) / 2.0
            cmp.position = (hPos, self.component.height - 8, 0.2)
            self.component.addChild(cmp, 'btn_{0}'.format(btn_['type']))
            btn.onClick = partial(self.btnHandler, btn_['type'], True)
            btn.onBound()
            btn._updateVisualState()

    def updateBinding(self):
        if self.parentGUI is not None:
            if self.parentBind:
                if self.parentGUI == GUI_ID.GUI_ID_INVENTORY:
                    self.setRestrictingComponent(BWPersonality.GUICore.worldLayer.inventory)
        return

    def handleDragStartEvent(self, cmp):
        if not self.component:
            print 'BUG HERE SP3,  stack:'
            import traceback
            traceback.print_stack()
            return True
        if cmp == self.component.closeBox:
            print 'handleDragStartEvent'
        if cmp != self.component.dragPlane:
            return False
        self._wantFocus()
        soDraggableComponent.handleDragStartEvent(self, cmp)
        return True

    def handleDragStopEvent(self, cmp):
        if cmp == self.component:
            return False
        soDraggableComponent.handleDragStopEvent(self, cmp)
        return True

    def handleMouseEvent(self, cmp, event):
        if not self.dragging:
            if event.dz:
                if event.dz > 0:
                    self.mouseWheel(True)
                else:
                    self.mouseWheel(False)
                return True
            return False
        soDraggableComponent.handleMouseEvent(self, cmp, event)
        return True

    def handleMouseButtonEvent(self, cmp, event):
        self._wantFocus()
        return True

    def onDragStop(self):
        GUI.delRoot(self.dragProxy)
        self.proxyHolder.addChild(self.component, self.proxyName)
        return True

    def mouseWheel(self, up = True):
        for addControl in self.addControls:
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_TEXTFIELD:
                cmp = getattr(self.component, 'txt_{0}'.format(addControl['ID']), None)
                if cmp:
                    if up:
                        cmp.script.scrollHandler('UP', None)
                    else:
                        cmp.script.scrollHandler('DOWN', None)

        return

    def _makeEdit(self, addControl, height):
        validator = lambda newStr, wholeText, offset: True
        if addControl.has_key('input_validator'):
            validator = addControl['input_validator']
        font = 'ruRU_Cyrvetica_Extra_14i.font'
        if addControl.has_key('font'):
            font = addControl[6]
        width = self.controlWidth
        if addControl.has_key('width'):
            width = addControl['width']
        edit = soEditBox(GUI.Window(), width=width, height=10, autosize=True, font=font, hOffset=3, vOffset=3, inputValidator=validator)
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        hA = MESSAGEBOX.ANCHOR_LEFT
        if addControl.has_key('hAnchor'):
            hA = addControl['hAnchor']
        cmp.horizontalAnchor = hA
        cmp.verticalAnchor = 'TOP'
        hPos = self.LEFT_ORIGIN
        if hA == MESSAGEBOX.ANCHOR_CENTER:
            hPos = self.component.width / 2.0
        elif hA == MESSAGEBOX.ANCHOR_RIGHT:
            hPos = self.component.width - 20
        cmp.position.x = hPos
        cmp.position.y = height
        cmp.position.z = 0.5
        self.component.addChild(cmp, 'edit_{0}'.format(addControl['ID']))
        edit.onBound()
        if addControl.has_key('default'):
            edit.setValue(addControl['default'])
        if addControl.has_key('active'):
            if addControl['active']:
                edit.activate(True)
        edit.onValueChange = partial(self._editFieldsHandler, addControl['ID'])
        return cmp.height

    def _makeCheckBox(self, addControl, height):
        label = u''
        if addControl.has_key('caption'):
            label = addControl['caption']
        color = (175, 166, 112, 255)
        if addControl.has_key('color'):
            color = addControl['color']
        font = 'ruRU_Cyrvetica_Extra_14i.font'
        if addControl.has_key('font'):
            font = addControl['font']
        cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=label, labelColour=color, font=font))
        cmp = cb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        hA = MESSAGEBOX.ANCHOR_LEFT
        if addControl.has_key('hAnchor'):
            hA = addControl['hAnchor']
        cmp.horizontalAnchor = hA
        cmp.verticalAnchor = 'TOP'
        hPos = self.LEFT_ORIGIN
        if hA == MESSAGEBOX.ANCHOR_CENTER:
            hPos = self.component.width / 2.0
        elif hA == MESSAGEBOX.ANCHOR_RIGHT:
            hPos = self.component.width - 20
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (hPos, height, 0.5)
        self.component.addChild(cmp, 'check_{0}'.format(addControl['ID']))
        cb.onBound()
        if addControl.has_key('default'):
            if addControl['default']:
                cb.setActive()
            else:
                cb.setInactive()
        cb.onStateChange = partial(self.addControlsHandler, addControl['ID'])
        return cmp.height

    def _makeRadio(self, addControl, height):
        label = u''
        if addControl.has_key('caption'):
            label = addControl['caption']
        color = (175, 166, 112, 255)
        if addControl.has_key('color'):
            color = addControl['color']
        font = 'ruRU_Cyrvetica_Extra_14i.font'
        if addControl.has_key('font'):
            font = addControl['font']
        rb = soRadioButton2(GUI.Window(), radioGroup='msg_box_{0}'.format(self.msgBoxID), labelText=label, labelColour=color, font=font)
        cmp = rb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        hA = MESSAGEBOX.ANCHOR_LEFT
        if addControl.has_key('hAnchor'):
            hA = addControl['hAnchor']
        cmp.horizontalAnchor = hA
        cmp.verticalAnchor = 'TOP'
        hPos = self.LEFT_ORIGIN
        if hA == MESSAGEBOX.ANCHOR_CENTER:
            hPos = self.component.width / 2.0
        elif hA == MESSAGEBOX.ANCHOR_RIGHT:
            hPos = self.component.width - 20
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (hPos, height, 0.5)
        self.component.addChild(cmp, 'radio_{0}'.format(addControl['ID']))
        rb.onBound()
        if addControl.has_key('default'):
            if addControl['default']:
                rb.setActive()
            else:
                rb.setInactive()
        rb.onStateChange = partial(self.addControlsHandler, addControl['ID'])
        return cmp.height

    def _makeText(self, addControl, height):
        text = u''
        if addControl.has_key('text'):
            text = addControl['text']
        width = self.controlWidth
        if addControl.has_key('width'):
            width = addControl['width']
        hA = MESSAGEBOX.ANCHOR_LEFT
        if addControl.has_key('hAnchor'):
            hA = addControl['hAnchor']
        autosize = True
        if addControl.has_key('autosize'):
            autosize = addControl['autosize']
        _height = 100
        if addControl.has_key('height'):
            _height = addControl['height']
        txt = soTextField3(GUI.Window(), height=_height, textWidth=-1, hScroll=False, vScroll=True, hideScroll=False, borderWidth=0, vOffset=0, hOffset=0, textureless=True, autosize=autosize, width=width)
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = hA
        cmp.verticalAnchor = 'TOP'
        hPos = self.LEFT_ORIGIN
        if hA == MESSAGEBOX.ANCHOR_CENTER:
            hPos = self.component.width / 2.0
        elif hA == MESSAGEBOX.ANCHOR_RIGHT:
            hPos = self.component.width - 20
        cmp.position.x = hPos
        cmp.position.y = height
        cmp.position.z = 0.5
        self.component.addChild(cmp, 'txt_{0}'.format(addControl['ID']))
        txt.onBound()
        txt.setText(text)
        return cmp.height

    def _makeLabel(self, addControl, height):
        text = u''
        if addControl.has_key('text'):
            text = addControl['text']
        color = (175, 166, 112, 255)
        if addControl.has_key('color'):
            color = addControl['color']
        font = 'ruRU_Cyrvetica_Extra_14i.font'
        if addControl.has_key('font'):
            font = addControl['font']
        hA = MESSAGEBOX.ANCHOR_LEFT
        if addControl.has_key('hAnchor'):
            hA = addControl['hAnchor']
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = hA
        cmp.verticalAnchor = 'TOP'
        cmp.font = font
        cmp.colour = color
        cmp.multiline = False
        cmp.colourFormatting = True
        cmp.text = text
        hPos = self.LEFT_ORIGIN
        if hA == MESSAGEBOX.ANCHOR_CENTER:
            hPos = self.component.width / 2.0
        elif hA == MESSAGEBOX.ANCHOR_RIGHT:
            hPos = self.component.width - 20
        cmp.position.x = hPos
        cmp.position.y = height
        cmp.position.z = 0.5
        self.component.addChild(cmp, 'label_{0}'.format(addControl['ID']))
        return cmp.stringDimensions('W')[1]

    def _makeSpacing1(self, addControl, height):
        h = 15
        if addControl.has_key('height'):
            h = addControl['height']
        return h

    def _makeSpacing2(self, addControl, height):
        color = (38, 38, 38, 255)
        if addControl.has_key('color'):
            color = addControl['color']
        h = 15
        if addControl.has_key('height'):
            h = addControl['height']
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = color
        cmp.materialFX = 'BLEND'
        cmp.height = 1
        cmp.width = self.controlWidth
        cmp.position.x = self.width / 2.0
        cmp.position.y = height + h / 2.0
        cmp.position.z = 0.5
        rndI = randint(0, 10000000)
        while getattr(self.component, 'spacing2_{0}'.format(rndI), None):
            rndI = randint(0, 10000000)

        self.component.addChild(cmp, 'spacing2_{0}'.format(rndI))
        return h

    def setPos(self, x, y):
        self.component.position.x = self.x = x
        self.component.position.y = self.y = y

    def sendEvent(self, event, data):
        self.callback(event, data)
        BWPersonality.GUICore.msgBoxEvent(event, data)

    def show(self):
        self.component.visible = True

    def hide(self):
        self.component.visible = False

    def internalClose(self):
        self.callback(MESSAGEBOX.EVENT_CLOSE_NONUSER, {'id': self.msgBoxID})
        self.msgBoxEvent(MESSAGEBOX.EVENT_CLOSE_NONUSER, {'id': self.msgBoxID})

    def userClose(self):
        self.callback(MESSAGEBOX.EVENT_CLOSE, {'id': self.msgBoxID})
        self.msgBoxEvent(MESSAGEBOX.EVENT_CLOSE, {'id': self.msgBoxID})

    def fini(self):
        self.handleDragStopEvent(self.component)
        for addControl in self.addControls:
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_EDIT:
                cmp = getattr(self.component, 'edit_{0}'.format(addControl['ID']), None)
                if cmp:
                    cmp.script.fini()

        self.msgBoxEvent = None
        self.clearAllChildren(self.component)
        self.component = None
        if self.ticker is not None:
            self.ticker.stop()
            self.ticker = None
        return

    def msgBoxEvent(self, event, data):
        return None

    def _wantFocus(self):
        BWPersonality.GUICore.msgBoxMgr.setActiveMsgBox(self.msgBoxID)

    def _editFieldsHandler(self, id, byUser):
        if byUser:
            self.addControlsHandler(id)

    def addControlsHandler(self, id):
        self._wantFocus()
        controlData = self._getControlData(id)
        if controlData is not None:
            self.callback(MESSAGEBOX.EVENT_ADDCONTROL, {'id': self.msgBoxID,
             'add_control_id': id,
             'add_control_data': controlData})
            self.msgBoxEvent(MESSAGEBOX.EVENT_ADDCONTROL, {'id': self.msgBoxID,
             'add_control_id': id,
             'add_control_data': controlData})
        return

    def setAddControlData(self, controlID, data):
        for addControl in self.addControls:
            if addControl.has_key('ID'):
                if addControl['ID'] == controlID:
                    if addControl['type'] == MESSAGEBOX.ADDCONTROL_EDIT:
                        cmp = getattr(self.component, 'edit_{0}'.format(addControl['ID']), None)
                        if cmp:
                            cmp.script.setValue(data)
                    if addControl['type'] == MESSAGEBOX.ADDCONTROL_CHECKBOX:
                        cmp = getattr(self.component, 'check_{0}'.format(addControl['ID']), None)
                        if cmp:
                            if data:
                                cmp.script.setActive()
                            else:
                                cmp.script.setInactive()
                    if addControl['type'] == MESSAGEBOX.ADDCONTROL_RADIO:
                        cmp = getattr(self.component, 'radio_{0}'.format(addControl['ID']), None)
                        if cmp:
                            if data:
                                cmp.script.setActive()
                            else:
                                cmp.script.setInactive()
                    if addControl['type'] == MESSAGEBOX.ADDCONTROL_TEXTFIELD:
                        cmp = getattr(self.component, 'txt_{0}'.format(addControl['ID']), None)
                        if cmp:
                            cmp.script.setText(data)
                    if addControl['type'] == MESSAGEBOX.ADDCONTROL_LABEL:
                        cmp = getattr(self.component, 'label_{0}'.format(addControl['ID']), None)
                        if cmp:
                            cmp.text = data

        return

    def setBtnData(self, btn_type, data):
        for btn in self.btns:
            if btn['type'] == btn_type:
                btnCmp = getattr(self.component, 'btn_{0}'.format(btn_type), None)
                if btnCmp:
                    if data.has_key('width'):
                        btnCmp.width = data['width']
                    if data.has_key('caption'):
                        btnCmp.label.text = data['caption']
                    if data.has_key('enabled'):
                        btnCmp.script.buttonDisabled = not data['enabled']
                        btnCmp.script._updateVisualState()

        return

    def _getControlData(self, id):
        controlsData = self._getControlsData()
        if controlsData.has_key(id):
            return controlsData[id]
        else:
            return None

    def _getControlsData(self):
        controlsData = {}
        for addControl in self.addControls:
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_EDIT:
                cmp = getattr(self.component, 'edit_{0}'.format(addControl['ID']), None)
                if cmp:
                    controlsData[addControl['ID']] = cmp.script.getRaw()
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_CHECKBOX:
                cmp = getattr(self.component, 'check_{0}'.format(addControl['ID']), None)
                if cmp:
                    controlsData[addControl['ID']] = cmp.script.isChecked()
            if addControl['type'] == MESSAGEBOX.ADDCONTROL_RADIO:
                cmp = getattr(self.component, 'radio_{0}'.format(addControl['ID']), None)
                if cmp:
                    controlsData[addControl['ID']] = cmp.script.isChecked()

        return controlsData

    def btnHandler(self, btn, byUser):
        self.callback(MESSAGEBOX.EVENT_BTNPRESS, {'id': self.msgBoxID,
         'btn': btn,
         'add_controls': self._getControlsData()})
        self.msgBoxEvent(MESSAGEBOX.EVENT_BTNPRESS, {'id': self.msgBoxID,
         'btn': btn,
         'add_controls': self._getControlsData()})

    def onCloseBoxClick(self):
        self.userClose()

    def onEscapeKey(self):
        if self.closeBox:
            self.userClose()
            return True
        return False

    def onReturnKey(self):
        if self.defaultAction is not None:
            self.btnHandler(self.defaultAction, False)
            return True
        else:
            return False

    @BWMemberCoroutine
    def timeoutTicker(self):
        if self.defaultAction is not None:
            cmp = getattr(self.component, 'btn_{0}'.format(self.defaultAction), None)
            if cmp:
                btnName = cmp.label.text.split()[0]
                cmp.label.text = u'{0} ({1})'.format(btnName, self.timeout)
        while self.timeout > 0:
            yield BWWaitForPeriod(1.0)
            self.timeout -= 1
            if self.defaultAction is not None:
                cmp = getattr(self.component, 'btn_{0}'.format(self.defaultAction), None)
                if cmp:
                    btnName = cmp.label.text.split()[0]
                    cmp.label.text = u'{0} ({1})'.format(btnName, self.timeout)

        self.ticker = None
        if self.defaultAction is not None:
            self.btnHandler(self.defaultAction, False)
        else:
            self.internalClose()
        return