# Embedded file name: scripts/client/soGUI/soList.py
import BWPersonality
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI import Utils
import soGUI
from soGUI.soScrollBar import soScrollBar
from soGUI.soButton import soButton
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
from soGUI.soVisualStateComponent import soVisualStateComponent
from functools import partial
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI import PyGUIBase
import Math
import math
from math import floor, ceil
import Keys
from soGUI.soScrollBar import soScrollBar2
from Helpers.PyGUI.PyGUIBase import PyGUIBase

class ListPropsStructure(object):

    def __init__(self, width = 200, height = 400, topOffset = 5, leftOffset = 5, lineOffset = 0, elemHeight = 20, scrollWidth = 16, listFont = 'ruRU_calibri_default.font', isMultiSel = True, needScroll = True, selectCallBack = None, nuSelectionCB = None, sorted = True, colorFont = (175, 166, 112, 255)):
        self.width = width
        self.height = height
        self.colorFont = colorFont
        self.topOffset = topOffset
        self.leftOffset = leftOffset
        self.lineOffset = lineOffset
        self.elementHeight = elemHeight
        self.texture = 'soGUI/maps/Controls/listFrame.tga'
        self.textureMappings = (0.0, 0.0, 400.0, 200.0)
        self.isMultiSelect = isMultiSel
        self.scrollWidth = scrollWidth
        self.needScroll = needScroll
        self.selectCallBack = selectCallBack
        self.nuSelectionCB = nuSelectionCB
        self.sorted = sorted
        self.font = listFont


class soListElement(soButton):
    factoryString = 'soGUI.soListElement'

    def __init__(self, component, rootComp = None, fontLabel = 'ruRU_calibri_large.font'):
        self.font = fontLabel
        soButton.__init__(self, component, fontLabel=self.font, isOptions=True)
        component.script = self
        self.rootComp = rootComp

    def handleMouseEnterEvent(self, cmp):
        soButton.handleMouseEnterEvent(self, cmp)
        handled = self.rootComp.script.handleMouseEnterEvent(self.rootComp)
        return handled

    def handleMouseEvent(self, comp, event):
        dx = event.dx
        dy = event.dy
        dz = event.dz
        position = event.cursorPosition
        soButton.handleMouseEvent(self, comp.script, event)
        handled = self.rootComp.script.handleMouseEvent(comp, event)
        return handled

    def handleMouseButtonEvent(self, comp, event):
        handled = soButton.handleMouseButtonEvent(self, comp, event)
        key = event.key
        down = event.isKeyDown()
        if key == Keys.KEY_RIGHTMOUSE and down:
            self.rootComp.script.onRmb(self.component.label.text)
            return True
        return handled


class soList(PyGUI.Window):
    factoryString = 'soGUI.soList'

    def __init__(self, component, props = ListPropsStructure(), default_frame_skin = 'soGUI/maps/con_frame.tga'):
        PyGUI.Window.__init__(self, component)
        component.script = self
        self.frameComp = None
        self.elementHolder = None
        self.vScroll = None
        self.default_frame_skin = default_frame_skin
        self.scrollStep = 0.0
        self.textFont = props.font
        self.colorFont = props.colorFont
        self.frameWidth = props.width
        self.frameHeight = props.height
        self.topOffset = props.topOffset
        self.leftOffset = props.leftOffset
        self.lineOffset = props.lineOffset
        self.frameTexture = props.texture
        self.frameMapping = props.textureMappings
        self.elementHeight = props.elementHeight
        self.scrollWidth = props.scrollWidth
        self.isMultiSel = props.isMultiSelect
        self.needScroll = props.needScroll
        self.selectionCallBack = props.selectCallBack
        self.nonuserSelectionCB = props.nuSelectionCB
        self.sorted = props.sorted
        self.wheelFocus = False
        self.elements = {}
        self.attachments = {}
        self.indexes = []
        self.setupRoot()
        self.setupFrame()
        self.setupScroll()
        self.setupElemHolder()
        return

    def setupRoot(self):
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.verticalPositionMode = self.horizontalPositionMode = 'CLIP'
        self.component.width = self.frameWidth
        self.component.height = self.frameHeight
        self.component.materialFX = 'BLEND'
        self.component.colour = (255, 255, 255, 255)
        self.component.position = (400, 300, 0.0)
        self.component.crossFocus = True
        self.component.visible = True
        self.component.mouseButtonFocus = True

    def setupFrame(self):
        if self.frameComp is None:
            self.frameComp = GUI.Frame2(self.default_frame_skin)
        self.frameComp.widthMode = self.frameComp.heightMode = 'PIXEL'
        self.frameComp.width = self.frameWidth
        self.frameComp.height = self.frameHeight
        self.frameComp.horizontalAnchor = 'LEFT'
        self.frameComp.verticalAnchor = 'TOP'
        self.frameComp.horizontalPositionMode = self.frameComp.verticalPositionMode = 'CLIP'
        self.frameComp.materialFX = 'BLEND'
        self.frameComp.colour = (255, 255, 255, 255)
        self.frameComp.visible = True
        self.frameComp.position = (-1.0, 1.0, 0.0)
        self.component.addChild(self.frameComp, 'listFrame')
        return

    def setupScroll(self):
        if not self.needScroll:
            return
        else:
            if self.vScroll is None:
                self.vScroll = soScrollBar2(GUI.Window(), width=16, height=self.frameComp.height - self.scrollWidth)
            cmp = self.vScroll.component
            cmp.horizontalAnchor = 'RIGHT'
            cmp.verticalAnchor = 'TOP'
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.position = (self.frameWidth - self.leftOffset, self.topOffset, 0.6)
            self.component.listFrame.addChild(cmp, 'vScroll')
            self.vScroll.setVisualState('normal')
            self.vScroll.onBound()
            self.vScroll.setSteps(0)
            return

    def setupElemHolder(self):
        if self.elementHolder is None:
            self.elementHolder = GUI.Window()
        self.elementHolder.widthMode = self.elementHolder.heightMode = 'PIXEL'
        self.elementHolder.width = self.frameComp.width - self.leftOffset * 2 - self.scrollWidth
        self.elementHolder.height = self.frameComp.height - self.topOffset * 2
        self.elementHolder.widthMode = self.elementHolder.heightMode = 'PIXEL'
        self.elementHolder.horizontalPositionMode = self.elementHolder.verticalPositionMode = 'CLIP'
        self.elementHolder.horizontalAnchor = 'LEFT'
        self.elementHolder.verticalAnchor = 'TOP'
        self.elementHolder.position = (-1.0 + soGUI.getPixelWidth(self.frameComp) * self.leftOffset, 1.0 - soGUI.getPixelHeight(self.frameComp) * self.topOffset, 0.0)
        self.elementHolder.textureName = ''
        self.elementHolder.visible = True
        self.elementHolder.scroll.set(0.0, 0.0)
        self.frameComp.addChild(self.elementHolder, 'elementHolder')
        return

    def applyElements(self):
        self.clearAllChildren(self.elementHolder)
        elemComps = []
        i = 0
        elemList = self.indexes
        if self.sorted:
            elemList.sort()
        for elem in elemList:
            elemComp = soListElement(GUI.Window(), self.component, fontLabel=self.textFont)
            elemComp.component.verticalPositionMode = elemComp.component.horizontalPositionMode = 'CLIP'
            elemComp.component.widthMode = elemComp.component.heightMode = 'PIXEL'
            elemComp.component.horizontalAnchor = 'LEFT'
            elemComp.component.verticalAnchor = 'TOP'
            elemComp.component.width = self.elementHolder.width
            elemComp.component.height = self.elementHeight
            elemComp.component.tiled = True
            elemComp.component.tileWidth = 1
            elemComp.component.tileHeight = 20
            elemComp.component.position = (-1.0, 1.0 - soGUI.getPixelHeight(self.elementHolder) * self.elementHeight * i, 0.0)
            elemComp.component.visible = True
            elemComp.component.materialFX = 'BLEND'
            elemComp.buttonStyle = soButton.TOGGLEBUTTON_STYLE
            elemComp.initVSC('soGUI/visual_styles/listElement.xml')
            elemComp.onBound()
            if self.elements[elem] == 0:
                elemComp.buttonActive = False
                elemComp.setVisualState('normal')
            else:
                elemComp.buttonActive = True
                elemComp.setVisualState('active')
            elemComp.onClick = partial(self.toggleElement, elem)
            elemComp.component.label.text = elem
            elemComp.component.label.horizontalPositionMode = elemComp.component.label.verticalPositionMode = 'CLIP'
            elemComp.component.label.horizontalAnchor = 'LEFT'
            elemComp.component.label.position = (-1.0 + soGUI.getPixelWidth(elemComp.component), 0.0, 0.0)
            elemComp.fontColor = self.colorFont
            elemComp.fontLabel = self.textFont
            elemComp.component.label.colour = self.colorFont
            elemComp.component.label.font = self.textFont
            elemComp._updateVisualState()
            elemComps.append(elemComp)
            i += 1

        i = 0
        for elem in elemComps:
            self.elementHolder.addChild(elem.component, 'element' + str(i))
            i += 1

        screenH = BigWorld.screenHeight()
        itemH = self.elementHeight + self.lineOffset

        def setMaxScroll():
            elementsHeight = len(self.elements) * itemH
            holderHeight = self.elementHolder.height
            heightDiff = itemH / screenH * len(self.elements) - holderHeight / screenH
            if heightDiff > 0.0:
                self.elementHolder.maxScroll = (0.0, heightDiff * 2)

        def setMinScroll():
            self.elementHolder.minScroll = (0.0, 0.0)

        setMaxScroll()
        setMinScroll()
        self.scrollStep = 2.0 / (screenH / itemH)
        scrollStepCount = (itemH * len(self.elements) - self.elementHolder.height) / float(itemH)
        if scrollStepCount > 0:
            self.vScroll.setSteps(math.ceil(scrollStepCount))
        else:
            self.vScroll.setSteps(0)
        self.onElementsRedraw()

    def toggleElement(self, elemCaption, silent = False):
        if not self.elements.has_key(elemCaption):
            self.applyElements()
            return False
        if not BigWorld.isKeyDown(Keys.KEY_LCONTROL) or not self.isMultiSel:
            for elem in self.elements:
                self.elements[elem] = 0

        if BigWorld.isKeyDown(Keys.KEY_LCONTROL) and self.isMultiSel:
            if self.elements[elemCaption] == 0:
                self.elements[elemCaption] = 1
            else:
                self.elements[elemCaption] = 0
        elif self.elements[elemCaption] == 0:
            self.elements[elemCaption] = 1
        self.applyElements()
        if not silent:
            self.onSelected()
        elif self.nonuserSelectionCB:
            self.nonuserSelectionCB()
        return True

    def getElementByAttachment(self, elemAttachment):
        for entry in self.attachments.items():
            if entry[1] == elemAttachment:
                return entry[0]

        return None

    def onSelected(self):
        if self.selectionCallBack is not None:
            self.selectionCallBack()
        return

    def addElement(self, elementCaption, attachment = None, delayedRender = False):
        if self.elements.has_key(elementCaption):
            return False
        else:
            self.elements[elementCaption] = 0
            self.attachments[elementCaption] = attachment
            self.indexes.append(elementCaption)
            if not delayedRender:
                self.applyElements()
            return True

    def removeElement(self, elementCaption):
        if self.elements.has_key(elementCaption):
            del self.elements[elementCaption]
            del self.attachments[elementCaption]
            self.indexes.remove(elementCaption)
            self.applyElements()
            return True
        else:
            return False

    def clear(self):
        self.elements = {}
        self.attachments = {}
        self.indexes = []
        self.elementHolder.scroll.y = 0.0
        self.elementHolder.maxScroll.y = 0.0
        self.elementHolder.minScroll.y = 0.0
        self.applyElements()

    def getSelection(self):
        retVal = []
        for elem in self.elements:
            if self.elements[elem] == 1:
                retVal.append(elem)

        return retVal

    def getAttachment(self, elemCaption):
        if self.attachments.has_key(elemCaption):
            return self.attachments[elemCaption]
        else:
            return elemCaption

    def onElementsRedraw(self):
        return None

    def scrollUp(self):
        if self.elementHolder.scroll.y < self.elementHolder.minScroll.y:
            self.elementHolder.scroll.y = self.elementHolder.minScroll.y
        if self.elementHolder.scroll.y > self.elementHolder.minScroll.y:
            self.elementHolder.scroll.y -= self.scrollStep
            self.vScroll.setValue(self.vScroll.getValue() - 1)

    def scrollDown(self):
        if self.elementHolder.scroll.y > self.elementHolder.maxScroll.y:
            self.elementHolder.scroll.y = self.elementHolder.maxScroll.y
        if self.elementHolder.scroll.y < self.elementHolder.maxScroll.y:
            self.elementHolder.scroll.y += self.scrollStep
            self.vScroll.setValue(self.vScroll.getValue() + 1)

    def handleMouseEnterEvent(self, comp):
        self.wheelFocus = True
        self.component.focus = True
        return True

    def handleMouseLeaveEvent(self, comp):
        self.wheelFocus = False
        self.component.focus = False
        self.multiSelON = False
        return True

    def handleMouseEvent(self, comp, event):
        dz = event.dz
        if dz > 0:
            self.scrollUp()
            return True
        if dz < 0:
            self.scrollDown()
            return True
        return False

    def onRmb(self, caption):
        return None

    @PyGUIEvent('listFrame.vScroll', 'scrollUp')
    def scrolledUP(self):
        self.scrollUp()

    @PyGUIEvent('listFrame.vScroll', 'scrollDown')
    def scrolledDOWN(self):
        self.scrollDown()

    @PyGUIEvent('listFrame.vScroll', 'scrollMoved')
    def vScrollMoved(self, newVal):
        self.elementHolder.scroll.y = newVal * self.scrollStep
        self.vScroll.setValue(newVal)


class soList2ElementBase(PyGUIBase):
    factoryString = 'soGUI.soList2ElementBase'

    def __init__(self, component, id, data):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.id = id
        self.elemData = data
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.verticalAnchor = 'TOP'

    def setupContent(self):
        return None

    def elementEvent(self, event, data):
        return None

    def isActive(self):
        return False

    def isEnabled(self):
        return False

    def activate(self, byUser = True):
        return False

    def deactivate(self, byUser = True):
        return False

    def enable(self):
        return False

    def disable(self):
        return False

    def getDims(self):
        return None

    def getID(self):
        return self.id

    def applyElemData(self):
        return None

    def setElemData(self, data):
        self.elemData = data
        self.applyElemData()


class soList2(PyGUIBase):
    factoryString = 'soGUI.soList2'

    def __init__(self, component, width, height, vScroll = True, hScroll = False, borderWidth = 0, elemHandler = lambda event, data: None, listHandler = lambda event, data: None, borderTexture = '', vScrollStep = 20, hScrollStep = 20):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.width = width
        self.height = height
        self.vScroll = vScroll
        self.hScroll = hScroll
        self.borderWidth = borderWidth
        self.vScrollStep = vScrollStep
        self.hScrollStep = hScrollStep
        self.elemHandler = elemHandler
        self.listHandler = listHandler
        self.borderTexture = borderTexture
        self.cursor = [0, 0]
        self.maxScroll = [0, 0]
        self.elements = []
        self.setupRoot()
        self.setupContent()

    def __getitem__(self, key):
        return self.elements[key]

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.width
        cmp.height = self.height
        cmp.moveFocus = True

    def setupContent(self):
        cmp = GUI.Window('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = self.width - self.borderWidth * 2
        cmp.height = self.height - self.borderWidth * 2
        if self.vScroll:
            cmp.width -= 16
        if self.hScroll:
            cmp.height -= 16
        cmp.position = (self.borderWidth, self.borderWidth, 0.2)
        self.component.addChild(cmp, 'elemHolder')
        cmp = GUI.Frame2(self.borderTexture)
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'dFrame')
        vSHeight = self.height - self.borderWidth * 2 if not self.hScroll else self.height - self.borderWidth * 2 - 16
        scroll = soScrollBar2(GUI.Window(), width=16, height=vSHeight)
        cmp = scroll.component
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.visible = self.vScroll
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (self.width - self.borderWidth, self.borderWidth, 0.6)
        self.component.addChild(cmp, 'vScroll')
        scroll.setVisualState('normal')
        scroll.onBound()
        scroll.setSteps(0)
        hSHeight = self.height - self.borderWidth * 2 if not self.vScroll else self.width - self.borderWidth * 2 - 16
        scroll = soScrollBar2(GUI.Window(), width=16, height=hSHeight, horizontal=True)
        cmp = scroll.component
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.visible = self.hScroll
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (self.borderWidth, self.height - self.borderWidth, 0.6)
        self.component.addChild(cmp, 'hScroll')
        scroll.setVisualState('normal')
        scroll.onBound()
        scroll.setSteps(0)

    def addElems(self, elems):
        firstNew = 0
        for elem in elems:
            self.elements.append(self._createElem(elem))

        self.reArrangeElems(firstNew)
        self._updateScrolls()

    def updateElems(self, elems):
        for elem in elems:
            cmp = getattr(self.component.elemHolder, 'elem_' + str(elem[0]), None)
            if cmp:
                elemObj = cmp.script
                elemObj.setElemData(elem[1])

        self.reArrangeElems(0)
        return

    def removeElems(self, elems):
        minModIdx = len(self.elements)
        for elem in elems:
            erasedIdx = self._eraseElem(elem)
            if erasedIdx:
                if erasedIdx < minModIdx:
                    minModIdx = erasedIdx

        self.reArrangeElems(minModIdx)
        self._updateScrolls()

    def insertElems(self, firstIndex, elems):
        if firstIndex >= len(self.elements):
            self.addElems(elems)
            return
        newSlice = []
        for elem in elems:
            newSlice.append(self._createElem(elem))

        self.elements = self.elements[0:firstIndex] + newSlice + self.elements[firstIndex:]
        self.reArrangeElems(firstIndex)
        self._updateScrolls()

    def enableElems(self, elems):
        shouldRearrange = False
        for elem in elems:
            cmp = getattr(self.component.elemHolder, 'elem_' + str(elem[0]), None)
            if cmp:
                if cmp.script.enable():
                    shouldRearrange = True

        if shouldRearrange:
            self.reArrangeElems()
        return

    def disableElems(self, elems):
        shouldRearrange = False
        for elem in elems:
            cmp = getattr(self.component.elemHolder, 'elem_' + str(elem[0]), None)
            if cmp:
                if cmp.script.disable():
                    shouldRearrange = True

        if shouldRearrange:
            self.reArrangeElems()
        return

    def activateElems(self, elems, byUser = False):
        shouldRearrange = False
        for elem in elems:
            cmp = getattr(self.component.elemHolder, 'elem_' + str(elem[0]), None)
            if cmp:
                if cmp.script.activate(byUser):
                    shouldRearrange = True

        if shouldRearrange:
            self.reArrangeElems()
        return

    def deactivateElems(self, elems, byUser = False):
        shouldRearrange = False
        for elem in elems:
            cmp = getattr(self.component.elemHolder, 'elem_' + str(elem[0]), None)
            if cmp:
                if cmp.script.deactivate(byUser):
                    shouldRearrange = True

        if shouldRearrange:
            self.reArrangeElems()
        return

    def clear(self):
        self.elements = []
        self.clearAllChildren(self.component.elemHolder)
        self._updateScrolls()

    def reArrangeElems(self, start = 0):
        if start > len(self.elements):
            return
        else:
            lastHeight = 0
            if start > 0:
                lastHeight = self.elements[start - 1].component.position.y + self.elements[start - 1].component.height
            for i in xrange(start, len(self.elements)):
                id = self.elements[i].getID()
                cmp = getattr(self.component.elemHolder, 'elem_' + str(id), None)
                if cmp:
                    cmp.position.y = lastHeight
                    lastHeight += cmp.height
                else:
                    print 'warning: soList2::reArrangeElems was called before all elements was initialized.'

            return

    def getIndex(self, id):
        cmp = getattr(self.component.elemHolder, 'elem_' + str(id), None)
        if cmp:
            if cmp.script.getID() == id:
                return self.elements.index(cmp.script)
            print 'some weird shit just happened in soList2::getIndex'
        else:
            return
        return

    def _updateScrolls(self):
        if not self.elements:
            self.component.vScroll.script.setSteps(0)
            self.component.elemHolder.maxScroll.y = 0.0
            self.maxScroll[1] = 0
            return
        cmp = self.elements[-1].component
        wholeHeight = cmp.position.y + cmp.height
        scrollHeight = wholeHeight - self.component.elemHolder.height
        if scrollHeight <= 0:
            self.component.vScroll.script.setSteps(0)
            self.component.elemHolder.maxScroll.y = 0.0
            self.maxScroll[1] = 0
        else:
            self.maxScroll[1] = ceil(scrollHeight / float(self.vScrollStep))
            self.component.vScroll.script.setSteps(self.maxScroll[1])
            scrollStep = self._getScrollStep()
            self.component.elemHolder.maxScroll.y = scrollStep[1] * scrollHeight

    def _getScrollStep(self):
        sW, sH = BigWorld.screenSize()
        return [2.0 / sW, 2.0 / sH]

    def _idInUse(self, id):
        cmp = getattr(self.component.elemHolder, 'elem_' + str(id), None)
        if cmp:
            return True
        else:
            return False
            return

    def _createElem(self, elem, overwrite = True):
        if self._idInUse(elem[0]):
            if overwrite:
                self._eraseElem(elem)
            else:
                self._updateElem(elem[0], elem)
        elemObj = elem[1](GUI.Window(), elem[0], elem[2])
        elemObj.elementEvent = self.elemHandler
        self.component.elemHolder.addChild(elemObj.component, 'elem_' + str(elem[0]))
        return elemObj

    def _eraseElem(self, elem):
        cmp = getattr(self.component.elemHolder, 'elem_' + str(elem[0]), None)
        if cmp:
            elemObj = cmp.script
            elemIdx = self.elements.index(elemObj)
            self.component.elemHolder.delChild(cmp)
            elemObj.clearAllChildren(cmp)
            cmp.script = None
            elemObj.component = None
            self.elements.remove(elemObj)
            return elemIdx
        else:
            return
            return

    def _updateElem(self, id, elem):
        cmp = getattr(self.component.elemHolder, 'elem_' + str(elem[0]), None)
        if cmp:
            elmObj = cmp.script
            elemObj.setElemData(elem[2])
        return

    def handleMouseEvent(self, cmp, event):
        if event.dz:
            if event.dz < 0:
                self.scrollHandler('DOWN', None)
            else:
                self.scrollHandler('UP', None)
        return True

    def scrollHandler(self, event, data):
        if event == 'RIGHT':
            self.cursor[0] += 1
        elif event == 'LEFT':
            self.cursor[0] -= 1
        elif event == 'hMOVE':
            self.cursor[0] = data
        if event == 'DOWN':
            self.cursor[1] += 1
        elif event == 'UP':
            self.cursor[1] -= 1
        elif event == 'vMOVE':
            self.cursor[1] = data
        if self.cursor[0] > self.maxScroll[0]:
            self.cursor[0] = self.maxScroll[0]
        if self.cursor[0] < 0:
            self.cursor[0] = 0
        if self.cursor[1] > self.maxScroll[1]:
            self.cursor[1] = self.maxScroll[1]
        if self.cursor[1] < 0:
            self.cursor[1] = 0
        self.component.vScroll.script.setValue(self.cursor[1])
        self.component.hScroll.script.setValue(self.cursor[0])
        self.component.elemHolder.scroll.y = self.cursor[1] * self._getScrollStep()[1] * self.vScrollStep

    @PyGUIEvent('vScroll', 'scrollUp')
    def scrolledUP(self):
        self.scrollHandler('UP', None)
        return

    @PyGUIEvent('vScroll', 'scrollDown')
    def scrolledDOWN(self):
        self.scrollHandler('DOWN', None)
        return

    @PyGUIEvent('hScroll', 'scrollLeft')
    def scrolledLEFT(self):
        self.scrollHandler('LEFT', None)
        return

    @PyGUIEvent('hScroll', 'scrollRight')
    def scrolledRIGHT(self):
        self.scrollHandler('RIGHT', None)
        return

    @PyGUIEvent('vScroll', 'scrollMoved')
    def vScrollMoved(self, newVal):
        self.scrollHandler('vMOVE', newVal)

    @PyGUIEvent('hScroll', 'scrollMoved')
    def hScrollMoved(self, newVal):
        self.scrollHandler('hMOVE', newVal)