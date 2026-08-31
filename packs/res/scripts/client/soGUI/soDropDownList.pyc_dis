# Embedded file name: scripts/client/soGUI/soDropDownList.py
import BigWorld
import BWPersonality
import GUI
import soGUI
import Helpers.PyGUI as PyGUI
from soGUI.soList import soList
from soGUI.soList import ListPropsStructure
from soGUI.soButton import soButton
from soGUI.soVisualStateComponent import soVisualStateComponent
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
from Helpers.PyGUI import PyGUIBase
import Helpers.PyGUI.TextStyles as TextStyles
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI import Utils
from Keys import *
from functools import partial

class DropDownListPropsStructure(object):

    def __init__(self, btnPlacement = 'RIGHT', btnW = 30, btnH = 30, DDLWidth = 250, DDLHeight = 300, DDLElemHeight = 25, DDLSelViewTexture = ('soGUI/maps/Controls/dropdown.tga', (0.0, 0.0, 200.0, 30.0)), sorted = True):
        """
        btnPlacement - \xd1\x80\xd0\xb0\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xba\xd0\xbd\xd0\xbe\xd0\xbf\xd0\xba\xd0\xb8 \xd0\xbf\xd0\xbe \xd0\xbe\xd1\x82\xd0\xbd\xd0\xbe\xd1\x88\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8e \xd0\xba \xd0\xbf\xd0\xbe\xd0\xbb\xd1\x8e \xd1\x81 \xd0\xb2\xd1\x8b\xd0\xb1\xd1\x80\xd0\xb0\xd0\xbd\xd0\xbd\xd1\x8b\xd0\xbc \xd1\x8d\xd0\xbb\xd0\xb5\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x82\xd0\xbe\xd0\xbc; RIGHT \xd0\xb8\xd0\xbb\xd0\xb8 LEFT
        btnW, btnH - \xd1\x88\xd0\xb8\xd1\x80\xd0\xb8\xd0\xbd\xd0\xb0 \xd0\xb8 \xd0\xb2\xd1\x8b\xd1\x81\xd0\xbe\xd1\x82\xd0\xb0 \xd0\xba\xd0\xbd\xd0\xbe\xd0\xbf\xd0\xba\xd0\xb8 \xd1\x81\xd0\xbe\xd0\xbe\xd1\x82\xd0\xb2\xd0\xb5\xd1\x82\xd1\x81\xd1\x82\xd0\xb2\xd0\xb5\xd0\xbd\xd0\xbd\xd0\xbe
        DDLWidth, DDLHeight - \xd1\x88\xd0\xb8\xd1\x80\xd0\xb8\xd0\xbd\xd0\xb0 \xd0\xb8 \xd0\xb2\xd1\x8b\xd1\x81\xd0\xbe\xd1\x82\xd0\xb0 dropdown list'\xd0\xb0 \xd0\xb2 \xd1\x80\xd0\xb0\xd1\x81\xd0\xba\xd1\x80\xd1\x8b\xd1\x82\xd0\xbe\xd0\xbc \xd1\x81\xd0\xbe\xd1\x81\xd1\x82\xd0\xbe\xd1\x8f\xd0\xbd\xd0\xb8\xd0\xb8
        DDLElemHeight - \xd0\xb2\xd1\x8b\xd1\x81\xd0\xbe\xd1\x82\xd0\xb0 \xd1\x8d\xd0\xbb\xd0\xb5\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x82\xd0\xbe\xd0\xb2 \xd0\xb2 \xd1\x81\xd0\xbf\xd0\xb8\xd1\x81\xd0\xba\xd0\xb5 
        """
        self.buttonAlignment = btnPlacement
        self.btnWidth = btnW
        self.btnHeight = btnH
        self.ddListWidth = DDLWidth
        self.ddListHeight = DDLHeight
        self.ddListElemHeight = DDLElemHeight
        self.selViewTexture = DDLSelViewTexture
        self.sorted = sorted


class soDropDownList(PyGUI.Window):
    factoryString = 'soGUI.soDropDownList'

    def __init__(self, component, props = DropDownListPropsStructure()):
        PyGUI.Window.__init__(self, component)
        component.script = self
        self.listBtn = None
        self.chosenElem = None
        self.elemList = None
        self.ddListWidth = props.ddListWidth
        self.ddListHeight = props.ddListHeight
        self.elemHeight = props.ddListElemHeight
        self.btnAlign = props.buttonAlignment
        self.sorted = props.sorted
        if self.btnAlign not in ('LEFT', 'RIGHT'):
            self.btnAlign = 'RIGHT'
        self.btnWidth = props.btnWidth
        self.btnHeight = props.btnHeight
        self.selViewTexture = props.selViewTexture
        self.listActive = False
        self.setupRoot()
        self.setupSelectionView()
        self.setupButton()
        self.setupList()
        return

    def setupRoot(self):
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.width = self.ddListWidth
        self.component.height = self.btnHeight
        self.component.verticalAnchor = 'TOP'
        self.component.textureName = ''

    def setupList(self):
        if self.elemList is None:
            self.elemList = soList(GUI.Window(), soGUI.ListPropsStructure(width=self.component.width - self.btnWidth, height=self.ddListHeight - self.btnHeight, isMultiSel=False, selectCallBack=self.onSelected, sorted=self.sorted))
        self.elemList.component.horizontalPositionMode = self.elemList.component.verticalPositionMode = 'CLIP'
        self.elemList.component.widthMode = self.elemList.component.heightMode = 'PIXEL'
        self.elemList.component.visible = True
        self.elemList.component.verticalAnchor = 'BOTTOM'
        if self.btnAlign == 'LEFT':
            self.elemList.component.horizontalAnchor = 'RIGHT'
            self.elemList.component.position = (1.0, -1.0, 0.0)
        elif self.btnAlign == 'RIGHT':
            self.elemList.component.horizontalAnchor = 'LEFT'
            self.elemList.component.position = (-1.0, -1.0, 0.0)
        self.elemList.onBound()
        return

    def setupButton(self):
        if self.listBtn is None:
            self.listBtn = soButton(GUI.Window())
        self.listBtn.component.horizontalPositionMode = self.listBtn.component.verticalPositionMode = 'CLIP'
        self.listBtn.component.widthMode = self.listBtn.component.heightMode = 'PIXEL'
        self.listBtn.component.width = 18
        self.listBtn.component.height = 18
        self.listBtn.component.verticalAnchor = 'CENTER'
        if self.btnAlign == 'LEFT':
            self.listBtn.component.horizontalAnchor = 'LEFT'
            self.listBtn.component.position = (-1.0 + soGUI.getPixelWidth(self.component) * 6, 1.0 - soGUI.getPixelHeight(self.component) * 15, 0.0)
        elif self.btnAlign == 'RIGHT':
            self.listBtn.component.horizontalAnchor = 'RIGHT'
            self.listBtn.component.position = (1.0 - soGUI.getPixelWidth(self.component) * 6, 1.0 - soGUI.getPixelHeight(self.component) * 15, 0.0)
        self.listBtn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        self.listBtn.initVSC('soGUI/visual_styles/arrow_down.xml')
        self.listBtn.setVisualState('normal')
        self.listBtn.onBound()
        self.component.addChild(self.listBtn.component, 'ddBtn')
        return

    def setupSelectionView(self):
        texture = self.selViewTexture[0]
        mapping = [[self.selViewTexture[1][0], self.selViewTexture[1][1]],
         [self.selViewTexture[1][0], self.selViewTexture[1][3]],
         [self.selViewTexture[1][2], self.selViewTexture[1][3]],
         [self.selViewTexture[1][2], self.selViewTexture[1][1]]]
        if self.chosenElem is None:
            self.chosenElem = soButton(GUI.Frame2(''))
        self.chosenElem.component.widthMode = self.chosenElem.component.heightMode = 'PIXEL'
        self.chosenElem.component.horizontalPositionMode = self.chosenElem.component.verticalPositionMode = 'CLIP'
        self.chosenElem.component.verticalAnchor = 'TOP'
        self.chosenElem.component.height = self.btnHeight
        self.chosenElem.component.width = self.component.width
        if self.btnAlign == 'RIGHT':
            self.chosenElem.component.horizontalAnchor = 'LEFT'
            self.chosenElem.component.position = (-1.0, 1.0, 0.1)
        elif self.btnAlign == 'LEFT':
            self.chosenElem.component.horizontalAnchor = 'RIGHT'
            self.chosenElem.component.position = (1.0, 1.0, 0.1)
        self.component.addChild(self.chosenElem.component, 'selectionView')
        self.chosenElem.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        self.chosenElem.initVSC('soGUI/visual_styles/dropdownSelectionView.xml')
        self.chosenElem.setVisualState('normal')
        if hasattr(self.chosenElem.component, 'label'):
            self.chosenElem.component.label.text = ''
            self.chosenElem.component.label.horizontalAnchor = self.chosenElem.component.horizontalAnchor
            self.chosenElem.component.label.position = (-1.0 + soGUI.getPixelWidth(self.chosenElem.component) * 5, 0.0, 0.0)
        self.chosenElem.onBound()
        return

    def addElement(self, elementCaption):
        self.elemList.addElement(elementCaption)

    def removeElement(self, elementCaption):
        self.elemList.removeElement(elementCaption)

    def clear(self):
        self.elemList.clear()

    def getSelection(self):
        return self.chosenElem.component.label.text

    def setSelection(self, text):
        self.chosenElem.component.label.text = text

    def topmostHiden(self):
        self.listActive = False

    @PyGUIEvent('selectionView', 'onClick')
    @PyGUIEvent('ddBtn', 'onClick')
    def showList(self):
        self.elemList.component.horizontalAnchor = 'LEFT'
        self.elemList.component.verticalAnchor = 'TOP'
        self.elemList.component.horizontalPositionMode = self.elemList.component.verticalPositionMode = 'LEGACY'
        pos = self.component.localToScreen((0.0, self.btnHeight))
        self.elemList.component.position = (pos[0], pos[1], 0.0)
        if not self.listActive:
            BWPersonality.GUICore.showTopmost(self.elemList.component, self.component)
            self.listActive = True
        else:
            BWPersonality.GUICore.hideTopmost(self.elemList.component, BWPersonality.GUICore.TOPMOST_DDL)
            self.listActive = False
        self.listBtn.buttonActive = self.elemList.component.visible
        self.listBtn._updateVisualState()

    def onSelect(self):
        return None

    def onSelected(self):
        self.chosenElem.component.label.text = self.elemList.getSelection()[0]
        self.elemList.component.visible = not self.elemList.component.visible
        self.listBtn.buttonActive = self.elemList.component.visible
        self.listBtn._updateVisualState()
        self.listActive = False
        self.onSelect()

    def closeList(self):
        pass


class soDDLVisualState(VisualState):

    def __init__(self):
        VisualState.__init__(self)
        self.textStyle = ''
        self.btnTextureMapping = None
        self.btnTexture = None
        self.frameTexture = None
        self.listVS = None
        return

    def onSave(self, dataSection):
        pass

    def onLoad(self, dataSection):
        VisualState.onLoad(self, dataSection)
        self.textStyle = dataSection.readString('textStyle', '')
        if dataSection.has_key('btn'):
            btnSection = dataSection._btn
            btnTextureName = btnSection.readString('textureName', '')
            self.btnTexture = BigWorld.PyTextureProvider(btnTextureName)
            if btnSection.has_key('mapping'):
                mappingSection = btnSection._mapping
                mappingType, mapping = self._readMappingSection(mappingSection)
                self.btnTextureMappingType = mappingType
                self.btnTextureMapping = mapping
            else:
                self.btnTextureMapping = None
        if dataSection.has_key('frame'):
            frameTextureName = dataSection._frame.readString('textureName', '')
            self.frameTexture = BigWorld.PyTextureProvider(frameTextureName)
        if dataSection.has_key('list'):
            self.listVS = dataSection._list.readString('visual_style', '')
        return

    def apply(self, componentScript):
        VisualState.apply(self, componentScript)
        if getattr(componentScript.component, 'label', None) is not None and self.textStyle:
            TextStyles.setStyle(componentScript.component.label, self.textStyle)
        if hasattr(componentScript.component, 'btn'):
            if self.btnTexture is not None:
                componentScript.component.btn.texture = self.btnTexture
            if self.btnTextureMapping:
                Utils.applyMapping(componentScript.component.btn, self.btnTextureMappingType, self.btnTextureMapping)
        if hasattr(componentScript.component, 'frameCmp'):
            if self.frameTexture is not None:
                componentScript.component.frameCmp.texture = self.frameTexture
        return


class soDropDownList2(PyGUIBase, soVisualStateComponent):
    factoryString = 'soGUI.soDropDownList2'
    visualStateString = 'soGUI.soDDLVisualState'
    SORT_METHOD_NONE = 0

    def __init__(self, component, width = 200, height = 25, btnAlignment = 'RIGHT', acceptInput = False, listHeight = 170, listWidth = 200, sortMethod = SORT_METHOD_NONE, elemHeight = 20, VS = 'soGUI/visual_styles/defaultDDL.xml', font = 'ruRU_calibri_large.font', colorFont = (175, 166, 112, 255), isOptions = False):
        PyGUIBase.__init__(self, component)
        soVisualStateComponent.__init__(self, component, self.visualStateString)
        component.script = self
        self.isOptions = isOptions
        self.font = font
        self.fontColor = colorFont
        self.width = width
        self.height = height
        self.btnAlignment = btnAlignment
        self.acceptIput = acceptInput
        self.listHeight = listHeight
        self.listWidth = listWidth
        self.sortMethod = sortMethod
        self.elemHeight = elemHeight
        self.VS = VS
        self.active = False
        self.disabled = False
        self.hovering = False
        self.pressed = False
        self.actualList = None
        self.listActive = False
        self.setupRoot()
        self.setupFrame()
        self.setupList()
        self.initVSC(self.VS)
        self.updateVisualState()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.width
        cmp.height = self.height
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.crossFocus = True
        cmp.mouseButtonFocus = True

    def setupFrame(self):
        cmp = GUI.Frame2('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = 'PIXEL'
        cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = self.btnAlignment
        cmp.verticalAnchor = 'CENTER'
        cmp.width = cmp.height = 18
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        btnX = 4 if self.btnAlignment == 'LEFT' else self.component.width - 4
        cmp.position = (btnX, 0.0, 0.2)
        self.component.addChild(cmp, 'btn')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = 'PIXEL'
        cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'LEFT' if self.btnAlignment == 'RIGHT' else 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_calibri_large.font'
        cmp.colour = (140, 141, 126, 255)
        labelX = 4 if self.btnAlignment == 'RIGHT' else self.component.width - 4
        cmp.position = (labelX, 0.0, 0.3)
        self.component.addChild(cmp, 'label')

    def setupList(self):
        font = 'ruRU_calibri_default.font'
        skin = 'soGUI/maps/con_frame.tga'
        color = (255, 255, 255, 255)
        if self.VS != 'soGUI/visual_styles/defaultDDL.xml':
            font = self.font
            skin = 'soGUI/maps/con_frame_for_options.tga'
            color = (140, 141, 126, 255)
        self.actualList = soList(GUI.Window(), soGUI.ListPropsStructure(width=self.width, colorFont=color, height=self.listHeight, isMultiSel=False, listFont=font, selectCallBack=partial(self._onListElem, False), nuSelectionCB=partial(self._onListElem, True), sorted=False), default_frame_skin=skin)
        cmp = self.actualList.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        self.actualList.onBound()

    def showList(self, doShow = True):
        if not doShow:
            if self.listActive:
                BWPersonality.GUICore.hideTopmost(self.actualList.component, BWPersonality.GUICore.TOPMOST_DDL)
            self.listActive = False
            return
        pos = self.component.localToScreen((0, self.height))
        self.actualList.component.position = (pos[0], pos[1], 0.0)
        if not self.listActive:
            BWPersonality.GUICore.showTopmost(self.actualList.component, self.component)
            self.listActive = True

    def setSelectionByText(self, txt, forceText = False, silent = False):
        if not self.actualList.toggleElement(txt, silent):
            if forceText:
                self._setSelectionLabel(txt)

    def setSelectionByValue(self, val, silent = False):
        caption = self.actualList.getElementByAttachment(val)
        if caption is not None:
            self.actualList.toggleElement(caption, silent)
        return

    def getSelection(self):
        caption = self.component.label.text
        atch = self.actualList.getAttachment(caption)
        value = atch if atch != caption else None
        return [caption, value]

    def clear(self):
        self.actualList.clear()
        self._setSelectionLabel(u'', silent=True)

    def _setSelectionLabel(self, txt, silent = False):
        self.component.label.text = txt
        if not silent:
            self.onSelectedText(txt)
            self.onUserAction()

    def _onListElem(self, nonUser = False):
        elem = self.actualList.getSelection()[0]
        attachment = self.actualList.getAttachment(elem)
        self._setSelectionLabel(elem, nonUser)
        if not nonUser:
            self.onSelectedElement(attachment)
            self.onUserAction()
        self.showList(False)

    def updateVisualState(self):
        visualState = 'normal'
        if self.disabled:
            visualState = 'disabled' if not self.active else 'disabled_active'
        elif self.pressed and self.hovering:
            visualStatee = 'pressed' if not self.active else 'pressed_active'
        elif self.hovering:
            visualState = 'hover' if not self.active else 'hover_active'
        else:
            visualState = 'normal' if not self.active else 'active'
        self.setVisualState(visualState)
        if self.isOptions:
            self.component.label.colour = self.fontColor
            self.component.label.font = self.font

    def topmostHiden(self):
        self.listActive = False

    def _onClick(self):
        self.showList(not self.listActive)

    def addElements(self, elems):
        for elem in elems:
            last = True if elem is elems[-1] else False
            self.actualList.addElement(elem[1], elem[0], not last)

    def handleMouseButtonEvent(self, comp, event):
        PyGUIBase.handleMouseButtonEvent(self, comp, event)
        key = event.key
        down = event.isKeyDown()
        if key == KEY_LEFTMOUSE:
            if down and not self.pressed:
                self.pressed = True
            elif not down and self.pressed:
                self.pressed = False
                self._onClick()
        self.updateVisualState()
        return True

    def handleMouseEnterEvent(self, comp):
        PyGUIBase.handleMouseEnterEvent(self, comp)
        self.pressed = self.pressed and BigWorld.isKeyDown(KEY_LEFTMOUSE)
        self.hovering = True
        self.updateVisualState()
        return True

    def handleMouseLeaveEvent(self, comp):
        self.hovering = False
        self.updateVisualState()
        return True

    def onSelectedText(self, txt):
        return None

    def onSelectedElement(self, elemID):
        return None

    def onUserAction(self):
        return None