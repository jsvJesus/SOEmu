# Embedded file name: scripts/client/soGUI/soDialogueBox.py
from Localization import lc
import BWPersonality
import BigWorld
import GUI
import soGUI
import Helpers.PyGUI as PyGUI
from soGUI.soButton import soButton
from soGUI.soTextField import soTextField2
from soGUI.soEditField import soEditField2
from soGUI.soEditField import soEditBox
from soGUI.soTextField import soTxtFieldPropsStructure
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soVisualStateComponent import soVisualStateComponent
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI.DraggableComponent import DraggableComponent
from functools import partial
from Helpers.BWCoroutine import *
from soGUI.soCheckBox import soCheckBox
from sounds import playSound
from soGUI.data import SoundFeed
from soGUI.soRadioButton import soRadioButton2
from Keys import *

class soDlgBoxVisualState(VisualState):

    def __init__(self):
        VisualState.__init__(self)
        self.textStyle = ''
        self.frameTextureName = ''
        self.frameColour = (255, 255, 255, 255)

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
        if dataSection.has_key('frame'):
            frameSection = dataSection._frame
            self.frameMaterialFX = frameSection.readString('materialFX', '')
            self.frameTextureName = frameSection.readString('textureName', '')
            self.frameColour = frameSection.readVector4('colour', (255, 255, 255, 255))

    def apply(self, componentScript):
        VisualState.apply(self, componentScript)
        if hasattr(componentScript, 'frameComponent'):
            componentScript.frameComponent.texture = None
            componentScript.frameComponent.textureName = self.frameTextureName
            componentScript.frameComponent.colour = self.frameColour
            if self.frameMaterialFX != '':
                componentScript.frameComponent.materialFX = self.frameMaterialFX
            else:
                componentScript.frameComponent.materialFX = 'BLEND'
        return


class soDlgBoxPropsStructure(object):

    def __init__(self, caption = '', msg = '', picture = ('', 100, 100), width = 250, height = 150, modal = False, posX = 0, posY = 0, btnSet = [], additions = [], closeBox = True):
        self.caption = caption
        self.msg = msg
        self.picture = picture
        self.modal = modal
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.btnSet = btnSet
        self.additions = additions
        self.closeBox = closeBox


class soDlgCaption(PyGUIBase):
    factoryString = 'soGUI.soDlgCaption'

    def __init__(self, component, closeBox):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.captionActive = True
        self.onClick = lambda : None
        self.dragging = False
        self.following = True
        self.closeBox = closeBox
        self.setupRoot()
        self.setupFrame()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 0
        cmp.height = 0
        cmp.position = (0, 0, 1.0)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.mouseButtonFocus = True
        cmp.moveFocus = True
        cmp.crossFocus = True

    def setupFrame(self):
        cmp = GUI.Frame2('soGUI/maps/con_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 0
        cmp.height = 28
        cmp.position = (0, 0, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'cptFrame')

    def setupContent(self):
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
        cmp.position = (0, 4, 0.2)
        self.component.addChild(cmp, 'closeBox')
        btn.onBound()
        btn.buttonDisabled = not self.closeBox
        if btn.buttonDisabled:
            btn.setVisualState('disabled')
        else:
            btn.setVisualState('normal')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.multiline = False
        cmp.colourFormatting = True
        cmp.position = (0, 4, 0.5)
        self.component.addChild(cmp, 'caption')

    def setWidth(self, w):
        self.component.width = w
        self.component.cptFrame.width = w
        self.component.closeBox.position.x = w - 4
        self.component.caption.position.x = 4

    def setHeight(self, h):
        self.component.height = h

    def setCaption(self, cpt):
        self.component.caption.text = cpt

    def handleMouseButtonEvent(self, comp, event):
        key = event.key
        down = event.isKeyDown()
        if key == KEY_LEFTMOUSE:
            if down:
                self.following = True
                self.followCursor().run()
            else:
                self.following = False
        self.onClick()
        return True

    def onCloseBox(self):
        return None

    @PyGUIEvent('closeBox', 'onClick')
    def closeBoxClicked(self):
        self.onCloseBox()

    @BWMemberCoroutine
    def followCursor(self):
        while self.following:
            yield BWWaitForPeriod(0.01)
            mouseX, mouseY = GUI.mcursor().position
            self.component.parent.position.x = mouseX
            self.component.parent.position.y = mouseY


class soDialogueBox(PyGUI.Window, soVisualStateComponent):
    factoryString = 'soGUI.soDialogueBox'
    visualStateString = 'soGUI.soTextFieldVisualState'
    BTN_OK = 0
    BTN_CANCEL = 1
    BTN_YES = 2
    BTN_NO = 3
    BTN_UNDO = 4
    BTN_APPLY = 5
    BTN_RESET = 6
    EVENT_BTNPRESS = 0
    EVENT_CLOSE = 1
    EVENT_CLOSE_NONUSER = 2
    ADDITIONAL_CONTROL_EDIT = 0
    ADDITIONAL_CONTROL_SLIDER = 1
    ADDITIONAL_CONTROL_CHECKBOX = 2

    def __init__(self, component, id, dlgProps = soDlgBoxPropsStructure()):
        PyGUI.Window.__init__(self, component)
        soVisualStateComponent.__init__(self, component, self.visualStateString)
        component.script = self
        self.props = dlgProps
        self.id = id
        self.isDlgActive = True
        self.soundControlName = 'MSGBox'
        self.btnCaptionMap = {soDialogueBox.BTN_OK: u'ok',
         soDialogueBox.BTN_CANCEL: lc('soDialogueBox.soGUI.STRING_268_33'),
         soDialogueBox.BTN_YES: lc('soDialogueBox.soGUI.STRING_269_30'),
         soDialogueBox.BTN_NO: lc('soDialogueBox.soGUI.STRING_270_29'),
         soDialogueBox.BTN_UNDO: lc('soDialogueBox.soGUI.STRING_271_31'),
         soDialogueBox.BTN_APPLY: lc('soDialogueBox.soGUI.STRING_272_32'),
         soDialogueBox.BTN_RESET: lc('soDialogueBox.soGUI.STRING_273_32')}
        self.setupRoot()
        self.setupFrame()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.position = (0.0, 0.0, 0.005)
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.props.width
        cmp.height = self.props.height
        cmp.textureName = ''
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        cmp.mouseButtonFocus = True
        cmp.focus = True

    def setupFrame(self):
        cmp = GUI.Frame2('soGUI/maps/con_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.props.width
        cmp.height = self.props.height - 28
        cmp.position = (0, 28, 0.9)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'bodyFrame')
        cpt = soDlgCaption(GUI.Window(), self.props.closeBox)
        cmp = cpt.component
        cpt.setWidth(self.props.width)
        cpt.setHeight(self.props.height)
        cpt.setCaption(self.props.caption)
        cpt.onBound()
        self.component.addChild(cmp, 'caption')
        cpt.dragProxy = self.component

    def setupContent(self):
        contentHeight = 32 * len(self.props.additions)
        if self.props.height < contentHeight + 200:
            self.props.height = contentHeight + 200
        self.component.height = self.props.height
        self.component.bodyFrame.height = self.props.height - 28
        btnSet = self.props.btnSet
        additionalControls = self.props.additions
        btnCount = len(btnSet)
        btnWidth = 0
        if btnCount:
            btnWidth = (self.props.width - 20 - 10 * (btnCount - 1)) / btnCount
        for i, btn in enumerate(btnSet):
            if btn in [self.BTN_APPLY,
             self.BTN_CANCEL,
             self.BTN_NO,
             self.BTN_OK,
             self.BTN_RESET,
             self.BTN_UNDO,
             self.BTN_YES]:
                btnObj = soButton(GUI.Window())
                btnObj.initVSC('soGUI/visual_styles/defaultBtn.xml')
                cmp = btnObj.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'BOTTOM'
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.width = btnWidth
                cmp.height = 25
                cmp.position = (10 + i * btnWidth + i * 10, self.props.height - 10, 0.2)
                cmp.label.font = 'ruRU_calibri_default.font'
                cmp.label.text = self.btnCaptionMap[btn]
                self.component.addChild(cmp, 'btn' + str(btn))
                btnObj.onBound()
                btnObj.setVisualState('normal')
                btnObj.onClick = partial(self.dlgBtnClick, btn)

        additionalControls.reverse()
        btnHeight = 10 if len(btnSet) == 0 else 45
        addsHeight = 0
        for i, addControl in enumerate(additionalControls):
            if addControl[0] == 'check':
                cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=addControl[1]))
                cmp = cb.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'BOTTOM'
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.position = (10, self.props.height - btnHeight - addsHeight, 0.2)
                self.component.addChild(cmp, 'cb_' + str(addControl[2]))
                cb.onBound()
                addsHeight += cmp.height + 2
                if len(addControl) > 3:
                    if addControl[3]:
                        cb.setActive()
                    else:
                        cb.setInactive()
            elif addControl[0] == 'edit':
                validator = lambda newStr, wholeText, offset: True
                if len(addControl) > 4:
                    validator = addControl[4]
                edit = soEditBox(GUI.Window(), height=25, width=self.props.width - 20, inputValidator=validator)
                edit.onBound()
                cmp = edit.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'BOTTOM'
                cmp.position = (10, self.props.height - btnHeight - addsHeight, 0.2)
                self.component.addChild(cmp, 'edit_' + str(addControl[2]))
                addsHeight += cmp.height + 2
                if len(addControl) > 3:
                    edit.setValue(addControl[3])
            elif addControl[0] == 'radio':
                rb = soRadioButton2(GUI.Window(), btnW=18, btnH=18, radioGroup='msg_box{0}'.format(self.id), labelText=addControl[1])
                rb.onBound()
                cmp = rb.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'BOTTOM'
                cmp.position = (10, self.props.height - btnHeight - addsHeight, 0.2)
                self.component.addChild(cmp, 'radio_' + str(addControl[2]))
                addsHeight += cmp.height + 2
                if len(addControl) > 3:
                    if addControl[3]:
                        rb.setActive()
                    else:
                        rb.setInactive()

        txtWidth = self.props.width - 8 if self.props.picture[0] == '' else self.props.width - self.props.picture[1] - 8
        txtHeight = self.props.height - 68 - 32 * len(self.props.additions)
        txt = soTextField2(GUI.Window(), soTxtFieldPropsStructure(autoSize=False, height=txtHeight, width=txtWidth, vScroll=True, textureless=True))
        cmp = txt.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalAnchor = 'LEFT'
        cmp.position = (4, 32, 0.0)
        txt.onBound()
        txt.setText(self.props.msg)
        self.component.addChild(cmp, 'msgTxt')
        if self.props.picture is not None:
            if self.props.picture[0] != '':
                maxPicH = self.props.height - 68 - 32 * len(self.props.additions)
                cmp = GUI.Simple('')
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'RIGHT'
                cmp.verticalAnchor = 'TOP'
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.width = self.props.picture[1]
                cmp.height = self.props.picture[2] if self.props.picture[2] < maxPicH else maxPicH
                cmp.textureName = self.props.picture[0]
                cmp.position = (self.props.width - 4, 32, 0.5)
                self.component.addChild(cmp, 'pict')
        return

    def userClose(self):
        data = [(None, None), None, None]
        data[0] = self.id
        BWPersonality.GUICore.dlgBoxEvent(self.EVENT_CLOSE, data)
        if hasattr(self.component, 'editFld'):
            self.component.editFld.script.activate(False)
        BWPersonality.GUICore.closeMessageBox(self.id)
        return

    def nonUserClose(self):
        data = [(None, None), None, None]
        data[0] = self.id
        BWPersonality.GUICore.dlgBoxEvent(self.EVENT_CLOSE_NONUSER, data)
        if hasattr(self.component, 'editFld'):
            self.component.editFld.script.activate(False)
        return

    def dlgBtnClick(self, btn):
        self.toTop()
        data = [(None, None), None, None]
        data[0] = self.id
        data[1] = btn
        addData = []
        for add in self.props.additions:
            if add[0] == 'check':
                cmp = getattr(self.component, 'cb_' + str(add[2]))
                checked = cmp.script.isChecked()
                addData.append([add[2], checked])
            if add[0] == 'edit':
                cmp = getattr(self.component, 'edit_' + str(add[2]))
                inputStr = cmp.script.getRaw()
                addData.append([add[2], inputStr])
                cmp.script.activate(False)
            if add[0] == 'radio':
                cmp = getattr(self.component, 'radio_' + str(add[2]))
                checked = cmp.script.isChecked()
                addData.append([add[2], checked])

        data[2] = addData
        BWPersonality.GUICore.dlgBoxEvent(self.EVENT_BTNPRESS, data)
        if btn in [self.BTN_OK,
         self.BTN_CANCEL,
         self.BTN_NO,
         self.BTN_YES]:
            BWPersonality.GUICore.closeMessageBox(self.id)
        return

    def show(self):
        if self.component.parent is None:
            if self.props.modal:
                BWPersonality.GUICore.modalLayer.addChild(self.component)
                BWPersonality.GUICore.goModal()
            else:
                BWPersonality.GUICore.generalLayer.addChild(self.component)
        self.component.visible = True
        soundName = SoundFeed.soundFeed.getSound(self.soundControlName, 'Pop')
        playSound(soundName)
        for dlgBx in BWPersonality.GUICore.dlgBoxes:
            if BWPersonality.GUICore.dlgBoxes[dlgBx] is not self:
                if BWPersonality.GUICore.dlgBoxes[dlgBx].isDlgActive:
                    self.component.position.x = BWPersonality.GUICore.dlgBoxes[dlgBx].component.position.x + 0.1
                    self.component.position.y = BWPersonality.GUICore.dlgBoxes[dlgBx].component.position.y - 0.1

        for addControl in self.props.additions:
            if addControl[0] == 'edit':
                cmp = getattr(self.component, 'edit_' + str(addControl[2]))
                cmp.script.activate(True)

        return

    def hide(self):
        self.component.visible = False
        if self.props.modal:
            BWPersonality.GUICore.modalLayer.delChild(self.component)
            for name, child in BWPersonality.GUICore.modalLayer.children:
                if isinstance(child.script, soDialogueBox):
                    return

            BWPersonality.GUICore.goModal(False)
        else:
            BWPersonality.GUICore.generalLayer.delChild(self.component)

    def activate(self, doActivate = True):
        if doActivate:
            if self.component.visible:
                for dlgBx in BWPersonality.GUICore.dlgBoxes:
                    if BWPersonality.GUICore.dlgBoxes[dlgBx] != self:
                        BWPersonality.GUICore.dlgBoxes[dlgBx].activate(False)

                self.isDlgActive = True
                self.toTop()
        else:
            self.isDlgActive = False
            if hasattr(self.component, 'editFld'):
                self.component.editFld.script.setActive(False)

    def controlActivated(self):
        self.activate()

    def setMsg(self, msg):
        self.component.msgTxt.script.setText(msg)

    def setPicture(self, pict):
        self.component.pict.textureName = pict

    def setCaption(self, caption):
        self.component.caption.caption.text = caption

    def toTop(self):
        minZ = 0.005
        for dlgBx in BWPersonality.GUICore.dlgBoxes:
            if BWPersonality.GUICore.dlgBoxes[dlgBx].component.position.z < minZ:
                minZ = BWPersonality.GUICore.dlgBoxes[dlgBx].component.position.z

        self.component.position.z = minZ - 1e-05
        GUI.reSort()

    def handleMouseButtonEvent(self, comp, event):
        key = event.key
        down = event.isKeyDown()
        self.toTop()
        return True

    @PyGUIEvent('caption', 'onCloseBox')
    def closeBoxClick(self):
        self.userClose()

    @PyGUIEvent('caption', 'onClick')
    def captionClick(self):
        self.activate()