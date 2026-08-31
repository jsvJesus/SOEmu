# Embedded file name: scripts/client/soGUI/soTabletScreen.py
from Localization import lc
import BWPersonality
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
from soGUI.soButton import soButton
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from copy import deepcopy
from Keys import *
from functools import partial
from Helpers.PyGUI import PyGUIEvent
from soGUI.soCheckBox import soCheckBox
from soGUI.soTextField import soTextField2, soTxtFieldPropsStructure
from soGUI.soEditField import soEditField2
from soGUI.data import GUIEvents

class soTabletScreen(PyGUI.Window):
    factoryString = 'soGUI.soTabletScreen'
    INTERFACE_MAIN = 0
    INTERFACE_QUESTLOG = 1
    INTERFACE_CLAN = 2
    INTERFACE_GPS = 3
    MSGBOX_CAPTIONMAP = {'ok': u'ok',
     'cancel': lc('soTabletScreen.soGUI.STRING_35_16'),
     'apply': lc('soTabletScreen.soGUI.STRING_36_15'),
     'yes': lc('soTabletScreen.soGUI.STRING_37_13'),
     'no': lc('soTabletScreen.soGUI.STRING_38_12')}
    EVENT_MSGBOXINPUT = 0
    EVENT_MSGBOXCLOSED = 1

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupTabletPC()
        self.setpWorkArea()
        self.GUI_ID_MAP = {self.INTERFACE_MAIN: BWPersonality.GUICore.GUI_ID_PDAMAIN,
         self.INTERFACE_QUESTLOG: BWPersonality.GUICore.GUI_ID_PDAQUEST,
         self.INTERFACE_CLAN: BWPersonality.GUICore.GUI_ID_PDAGUILD,
         self.INTERFACE_GPS: BWPersonality.GUICore.GUI_ID_PDAMAP}
        self.workArea = self.component.workArea
        self.interfaceMap = {}
        self.msgBoxCloser = lambda : None
        self.msgBox = None
        self.currentInterface = None
        return

    def setupRoot(self):
        self.component.textureName = ''
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.horizontalAnchor = 'CENTER'
        self.component.verticalAnchor = 'CENTER'
        self.component.horizontalPositionMode = self.component.verticalPositionMode = 'CLIP'
        self.component.width = 1004
        self.component.height = 749
        self.component.position = (0.0, 0.0, 0.11)
        self.component.colour = (255, 255, 255, 255)
        self.component.materialFX = 'BLEND'
        self.component.visible = False

    def setupTabletPC(self):
        tpcFrame = GUI.Simple('soGUI/maps/Controls/TabletPC/tpc.tga')
        tpcFrame.horizontalPositionMode = tpcFrame.verticalPositionMode = 'PIXEL'
        tpcFrame.widthMode = tpcFrame.heightMode = 'PIXEL'
        tpcFrame.horizontalAnchor = 'LEFT'
        tpcFrame.verticalAnchor = 'TOP'
        tpcFrame.width = 1004
        tpcFrame.height = 749
        tpcFrame.position = (0, 0, 1.0)
        tpcFrame.colour = (255, 255, 255, 255)
        tpcFrame.materialFX = 'BLEND'
        self.component.addChild(tpcFrame, 'tpcFrame')

    def setpWorkArea(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/work_area.tga'
        cmp.width = 792
        cmp.height = 518
        cmp.position = (106, 92, 0.1)
        self.component.addChild(cmp, 'workArea')

    def addInterface(self, interface, component):
        if not self.interfaceMap.has_key(interface):
            self.interfaceMap[interface] = component
            self.workArea.addChild(component, 'interface' + str(interface))

    def showInterface(self, interface):
        if self.currentInterface == interface:
            self.interfaceMap[interface].visible = True
            BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, self.GUI_ID_MAP[interface])
            return
        for interface_ in self.interfaceMap:
            if self.interfaceMap[interface_].visible:
                self.interfaceMap[interface_].visible = False
                BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, self.GUI_ID_MAP[interface_])

        if self.interfaceMap.has_key(interface):
            self.interfaceMap[interface].visible = True
            self.currentInterface = interface
            BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, self.GUI_ID_MAP[interface])

    def showMsgBox(self, id, width = 200, height = 450, text = u'PLACE_HOLDER', caption = u'', btnSet = ['ok', 'cancel', 'yes'], noCloseBox = False, additionalControls = [('check', u'labelText1', 'id_check'),
 ('check', u'labelText2', 'id_check2'),
 ('check', u'labelText3', 'id_check3'),
 ('edit', True, 'edit1')]):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.005)
        cmp.crossFocus = True
        cmp.moveFocus = True
        cmp.mouseButtonFocus = True
        self.workArea.addChild(cmp, 'dlgBox')
        self.msgBox = cmp
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.width = width
        cmp.height = height
        cmp.position = (0.0, 0.0, 0.0)
        self.msgBox.addChild(cmp, 'msgBoxWorkArea')
        cmp = GUI.Frame2('soGUI/maps/Controls/TabletPC/msgBox/msgBoxFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 1.0)
        self.msgBox.msgBoxWorkArea.addChild(cmp, 'frame')
        cmp = GUI.Frame2('soGUI/maps/Controls/TabletPC/msgBox/captionFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = width - 20
        cmp.height = 32
        cmp.position = (10, 10, 0.9)
        self.msgBox.msgBoxWorkArea.addChild(cmp, 'captionFrame')
        btnObj = soButton(GUI.Window())
        btnObj.initVSC('soGUI/visual_styles/closeBox.xml')
        cmp = btnObj.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (width - 19, 17, 0.2)
        self.msgBox.msgBoxWorkArea.addChild(cmp, 'closeBox')
        btnObj.onBound()
        btnObj.setVisualState('normal')
        btnObj.onClick = partial(self.msgBoxHandler, id, [], 'closebox')
        btnCount = len(btnSet)
        btnWidth = 0
        if btnCount:
            btnWidth = (width - 20 - 10 * (btnCount - 1)) / btnCount
        for i, btn in enumerate(btnSet):
            if btn in ('ok', 'cancel', 'apply', 'yes', 'no'):
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
                cmp.position = (10 + i * btnWidth + i * 10, height - 10, 0.2)
                cmp.label.font = 'ruRU_calibri_default.font'
                cmp.label.text = self.MSGBOX_CAPTIONMAP[btn]
                self.msgBox.msgBoxWorkArea.addChild(cmp, 'btn' + btn)
                btnObj.onBound()
                btnObj.setVisualState('normal')
                btnObj.onClick = partial(self.msgBoxHandler, id, additionalControls, btn)

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
                cmp.position = (10, height - btnHeight - addsHeight, 0.2)
                self.msgBox.msgBoxWorkArea.addChild(cmp, 'cb_' + str(addControl[2]))
                cb.onBound()
                addsHeight += cmp.height + 2
            elif addControl[0] == 'edit':
                edit = soEditField2(GUI.Window(), height=25, width=width - 20)
                edit.onBound()
                cmp = edit.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'BOTTOM'
                cmp.position = (10, height - btnHeight - addsHeight, 0.2)
                self.msgBox.msgBoxWorkArea.addChild(cmp, 'edit_' + str(addControl[2]))
                addsHeight += cmp.height + 2

        self.msgBoxCloser = partial(self.closeMsgBox, id)
        cmp = GUI.Frame2('soGUI/maps/Controls/TabletPC/msgBox/msgFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = width - 20
        cmp.height = height - 52 - addsHeight - btnHeight - 8
        cmp.position = (10, 52, 0.8)
        self.msgBox.msgBoxWorkArea.addChild(cmp, 'txtFrame')
        txt = soTextField2(GUI.Window(), soTxtFieldPropsStructure(autoSize=False, height=height - 52 - addsHeight - btnHeight - 8 - 14, width=width - 34, vScroll=True, textureless=True))
        cmp = txt.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalAnchor = 'LEFT'
        cmp.position = (17, 60, 0.2)
        txt.onBound()
        txt.setText(text)
        self.msgBox.msgBoxWorkArea.addChild(cmp, 'msgTxt')

    def msgBoxHandler(self, msgBoxID, addList, btn):
        data = []
        data.append(msgBoxID)
        data.append(btn)
        addData = []
        for add in addList:
            if add[0] == 'check':
                cmp = getattr(self.msgBox.msgBoxWorkArea, 'cb_' + str(add[2]))
                checked = cmp.script.isChecked()
                addData.append([add[2], checked])
            if add[0] == 'edit':
                cmp = getattr(self.msgBox.msgBoxWorkArea, 'edit_' + str(add[2]))
                inputStr = cmp.script.getValue()
                addData.append([add[2], inputStr])

        data.append(addData)
        BWPersonality.GUICore.TPCGeneralEvent(self.EVENT_MSGBOXINPUT, data)
        self.msgBoxCloser()

    def closeMsgBox(self, msgBoxID):
        BWPersonality.GUICore.TPCGeneralEvent(self.EVENT_MSGBOXCLOSED, msgBoxID)
        self.msgBoxCloser = lambda : None
        self.component.workArea.delChild(self.msgBox)
        self.msgBox = None
        BWPersonality.GUICore.clearCharacterReciever()
        return

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'tpc')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        for interface_ in self.interfaceMap:
            self.interfaceMap[interface_].visible = False

        BWPersonality.GUICore.setBestCursor()
        if self.msgBox:
            self.msgBoxCloser()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, self.GUI_ID_MAP[self.currentInterface])