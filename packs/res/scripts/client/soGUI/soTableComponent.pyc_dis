# Embedded file name: scripts/client/soGUI/soTableComponent.py
import BigWorld
import GUI
import soGUI
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI.PyGUIBase import PyGUIBase
import BWPersonality
from soGUI.soScrollBar import soScrollBar, soScrollBar2
from functools import partial
from soGUI.soButton import soButton, soButtonWTT
from soGUI.soCheckBox import soCheckBox
from Keys import *
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
from soGUI.soVisualStateComponent import soVisualStateComponent
from soGUI.soEditField import soEditField2
from soGUI.soToolTipComponent import soToolTipComponent
from math import floor, ceil
from operator import contains
from Helpers.PyGUI import PyGUIEvent
ITEMTYPE_TEXT = 0
ITEMTYPE_BOOL = 1
ITEMTYPE_BOOLEXCLUSIVE = 2
ITEMTYPE_LIST = 3
ITEMTYPE_PICTURE = 4
ITEMTYPE_BUTTON = 5
ITEMTYPE_TOGGLE = 6
ITEMTYPE_HYPERLINK = 7
ITEMTYPE_GUIOBJECT = 8

class soTableComponentVisualState(VisualState):

    def __init__(self):
        VisualState.__init__(self)
        self.delimeterTextureName = ''
        self.itemTextureName = ''
        self.itemSelTextureName = ''
        self.frameTextureName = ''
        self.borderWidth = 0
        self.delimeterWidth = 0
        self.captionButtonVStyle = ''

    def onSave(self, dataSection):
        pass

    def onLoad(self, dataSection):
        VisualState.onLoad(self, dataSection)
        self.delimeterTextureName = dataSection.readString('delimeterTextureName', '')
        self.itemTextureName = dataSection.readString('itemTextureName', '')
        self.itemSelTextureName = dataSection.readString('itemSelTextureName', '')
        self.frameTextureName = dataSection.readString('frameTextureName', '')
        self.borderWidth = dataSection.readInt('borderWidth', 0)
        self.delimeterWidth = dataSection.readInt('delimeterWidth', 0)
        self.captionButtonVStyle = dataSection.readString('captionButtonVStyle', 'soGUI/visual_styles/defaultBtnEmpty.xml')

    def apply(self, componentScript):
        VisualState.apply(self, componentScript)
        if self.frameTextureName != '':
            componentScript.frameTexture = BigWorld.PyTextureProvider(self.frameTextureName)
        if self.itemTextureName != '':
            componentScript.itemTexture = BigWorld.PyTextureProvider(self.itemTextureName)
        if self.itemSelTextureName != '':
            componentScript.itemSelTexture = BigWorld.PyTextureProvider(self.itemSelTextureName)
        if self.delimeterTextureName != '':
            componentScript.dlmTexture = BigWorld.PyTextureProvider(self.delimeterTextureName)
        if self.captionButtonVStyle != '':
            componentScript.captionButtonVStyle = self.captionButtonVStyle
        componentScript.borderWidth = self.borderWidth
        componentScript.delimeterWidth = self.delimeterWidth
        componentScript.newStyle()


class tablePropsStructure(object):

    def __init__(self, width = 600, visibleRows = 10, hScroll = False, vScroll = True, readOnly = True, rowHeight = 25, colCaptionHeight = 30, selType = 'ROW'):
        self.width = width
        self.visibleRows = visibleRows
        self.hScroll = hScroll
        self.vScroll = vScroll
        self.readOnly = readOnly
        self.rowHeight = rowHeight
        self.colCaptionHeight = colCaptionHeight
        self.selType = selType


class soTableItem(PyGUIBase):
    factoryString = 'soGUI.soTableItem'

    def __init__(self, component, w, h, font = 'ruRU_calibri_default.font', type = ITEMTYPE_TEXT):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.width = w
        self.height = h
        self.font = font
        self.colName = ''
        self.rowIndex = 0
        self.itemType = type
        self.onLmb = lambda : None
        self.onRmb = lambda : None
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.width
        cmp.height = self.height
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.mouseButtonFocus = True

    def setupContent(self):
        if self.itemType == ITEMTYPE_TEXT:
            cmp = GUI.Text('')
            cmp.font = self.font
            cmp.multiline = False
            cmp.colourFormatting = True
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            self.component.addChild(cmp, 'label')
        if self.itemType == ITEMTYPE_BOOL:
            cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=u''))
            cmp = cb.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (0.0, 0.0, 0.4)
            self.component.addChild(cmp, 'bool')
            cb.onStateChange = self.boolHandler
            cb.onBound()

    def handleMouseButtonEvent(self, comp, event):
        if not event.isMouseButton():
            return False
        down = event.isKeyDown()
        key = event.key
        if key == KEY_LEFTMOUSE:
            if down:
                self.onLmb()
                return True
        if key == KEY_RIGHTMOUSE:
            if down:
                self.onRmb()
                return True
        return False

    def setLabel(self, txt = u''):
        if self.itemType == ITEMTYPE_TEXT:
            self.component.label.text = txt

    def setBool(self, active):
        if self.itemType != ITEMTYPE_BOOL:
            return
        if active:
            self.component.bool.script.setActive()
        else:
            self.component.bool.script.setInactive()

    def clear(self):
        if self.itemType == ITEMTYPE_TEXT:
            self.component.label.text = u''

    def setWidth(self, w):
        self.component.width = w

    def setColRow(self, col, row):
        self.colName = col
        self.rowIndex = row

    def getType(self):
        return self.itemType

    def boolEvent(self, col, row, val):
        return None

    def boolHandler(self):
        checked = self.component.bool.script.isChecked()
        self.boolEvent(self.colName, self.rowIndex, checked)


class soTableComponent(PyGUIBase, soVisualStateComponent):
    factoryString = 'soGUI.soTableComponent'
    visualStateString = 'soGUI.soTableComponentVisualState'

    def __init__(self, component, props = tablePropsStructure()):
        PyGUIBase.__init__(self, component)
        soVisualStateComponent.__init__(self, component, self.visualStateString)
        component.script = self
        self.props = props
        self.columns = []
        self.rows = []
        self.colData = {}
        self.vScroll = None
        self.hScroll = None
        self.onSelectLeft = lambda : None
        self.onSelectRight = lambda : None
        self.dlmTexture = None
        self.itemTexture = None
        self.itemSelTexture = None
        self.frameTexture = None
        self.borderWidth = 0
        self.delimeterWidth = 1
        self.captionButtonVStyle = 'soGUI/visual_styles/defaultBtnEmpty.xml'
        self.minScroll = [0, 0]
        self.maxScroll = [0, 0]
        self.dirty = False
        self.cursor = [0, 0]
        self.selection = None
        self.items = []
        self.colCaptionBtns = []
        self.setupRoot()
        self.setupContent()
        self.setupScrolls()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.props.width
        cmp.height = self.props.colCaptionHeight + self.props.rowHeight * self.props.visibleRows + self.delimeterWidth * (self.props.visibleRows - 1)
        cmp.texture = self.frameTexture
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.moveFocus = True

    def setupScrolls(self):
        if self.props.vScroll:
            scrollComp = GUI.Window()
            self.vScroll = soScrollBar(scrollComp)
        cmp = self.vScroll.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 16
        cmp.height = self.component.height
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (self.props.width, 0, 0.2)
        cmp.visible = self.props.vScroll
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(self.vScroll.component, 'vScroll')
        self.vScroll.initVSC('scripts/client/soGUI/schemas/soScrollBar_default.xml')
        self.vScroll.setVisualState('normal')
        self.vScroll.onBound()
        self.vScroll.makeLayout()
        self.vScroll.setupScrollingInfo(0)
        self.vScroll.scrollUP = partial(self.doVScroll, False)
        self.vScroll.scrollDN = partial(self.doVScroll, True)

    def setupContent(self):
        for i in xrange(1, self.props.visibleRows):
            if i < self.props.visibleRows:
                cmp = GUI.Simple('')
                cmp.tiled = True
                cmp.pixelSnap = False
                cmp.tileHeight = cmp.tileWidth = self.delimeterWidth
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.verticalAnchor = 'TOP'
                cmp.horizontalAnchor = 'LEFT'
                cmp.width = self.component.width - self.delimeterWidth * 2
                cmp.height = self.delimeterWidth
                cmp.texture = self.dlmTexture
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.position = (self.borderWidth, self.props.colCaptionHeight + (self.props.rowHeight + self.delimeterWidth) * i, 0.4)
                self.component.addChild(cmp, 'hLine' + str(i))

    def renderTable(self):
        if self.isDirty():
            self.constructTable()
        rowCount = len(self.rows) - self.cursor[1]
        if rowCount > self.props.visibleRows:
            rowCount = self.props.visibleRows
        for i in xrange(rowCount):
            row = self.rows[i + self.cursor[1]]
            for col in self.columns:
                cmp = self.component.__getattribute__('tableItem' + col + 'x' + str(i))
                cmp.script.clear()
                if self.selection:
                    if i + self.cursor[1] == self.selection[1]:
                        cmp.texture = self.itemSelTexture
                    elif self.itemTexture:
                        cmp.texture = self.itemTexture
                    else:
                        cmp.textureName = ''

            for data in row:
                if self.columns.count(data) > 0:
                    cmp = self.component.__getattribute__('tableItem' + data + 'x' + str(i))
                    if cmp.script.getType() == ITEMTYPE_TEXT:
                        cmp.script.setLabel(row[data])
                    if cmp.script.getType() == ITEMTYPE_BOOL:
                        cmp.script.setBool(row[data])

        self.updateScroll()

    def constructTable(self):
        colCaption = 0
        colWidth = 1
        self.colCaptionBtns = []
        for i, col in enumerate(self.columns):
            colBtn = soButton(GUI.Window())
            cmp = colBtn.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            w = self._getColumnPixelWidth(col)
            cmp.width = w
            cmp.height = self.props.colCaptionHeight - self.delimeterWidth
            xPos = self.borderWidth
            for _col in self.columns[:i]:
                _w = self._getColumnPixelWidth(_col)
                xPos += _w

            cmp.position = (xPos, self.borderWidth, 0.5)
            cmp.label.font = 'ruRU_calibri_default.font'
            cmp.label.colour = (255, 255, 255, 255)
            cmp.label.text = self.colData[col][colCaption]
            self.component.addChild(cmp, col)
            colBtn.onClick = partial(self.colBtnClick, col)
            colBtn.initVSC('soGUI/visual_styles/defaultBtnEmpty.xml')
            colBtn.onBound()
            self.colCaptionBtns.append(colBtn)
            if i + 1 < len(self.columns):
                cmp = GUI.Simple('')
                cmp.tiled = True
                cmp.tileHeight = cmp.tileWidth = self.delimeterWidth
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.verticalAnchor = 'TOP'
                cmp.horizontalAnchor = 'LEFT'
                cmp.width = self.delimeterWidth
                cmp.height = self.component.height - self.borderWidth * 2
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.texture = self.dlmTexture
                cmp.position = (xPos + self._getColumnPixelWidth(col), self.borderWidth, 0.4)
                self.component.addChild(cmp, 'vLine' + str(i))
            cmp = GUI.Simple('')
            cmp.tiled = True
            cmp.tileHeight = cmp.tileWidth = self.delimeterWidth
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.verticalAnchor = 'TOP'
            cmp.horizontalAnchor = 'LEFT'
            cmp.width = self.component.width - self.borderWidth * 2
            if self.props.vScroll:
                cmp.width -= 16
            cmp.height = self.delimeterWidth
            cmp.texture = self.dlmTexture
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (self.borderWidth, self.props.colCaptionHeight, 0.4)
            self.component.addChild(cmp, 'lineColCaption')

        for item in self.items:
            self.component.delChild(item)
            item = None

        self.items = []
        for i in xrange(len(self.columns)):
            for j in xrange(self.props.visibleRows):
                item = soTableItem(GUI.Window(), self._getColumnPixelWidth(self.columns[i]), self.props.rowHeight, type=self.colData[self.columns[i]][3])
                item.onLmb = partial(self.onRowElement, self.columns[i], j, 'LEFT')
                item.onRmb = partial(self.onRowElement, self.columns[i], j, 'RIGHT')
                item.setColRow(self.columns[i], j)
                if self.colData[self.columns[i]][3] == ITEMTYPE_BOOL:
                    item.boolEvent = self.onBoolElement
                cmp = item.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.texture = self.itemTexture
                posX = self.borderWidth
                for _col in self.columns[:i]:
                    posX += self._getColumnPixelWidth(_col)
                    posX += 1

                posY = self.borderWidth + self.props.colCaptionHeight + self.delimeterWidth + (self.props.rowHeight + self.delimeterWidth) * j
                cmp.position = (posX, posY, 0.41)
                self.component.addChild(cmp, 'tableItem' + self.columns[i] + 'x' + str(j))
                self.items.append(cmp)
                item.onBound()

        GUI.reSort()
        self.dirty = False
        return

    def _getKeyColumn(self):
        for col in self.columns:
            if self.colData[col][2]:
                return col

        return None

    def _getColumnPixelWidth(self, col):
        tableW = self.component.width
        if self.props.vScroll:
            tableW -= 16
        w = tableW / 100.0 * self.colData[col][1] - self.delimeterWidth
        return ceil(w)

    def _getRow(self, colName, y):
        if self.cursor[1] + y >= len(self.rows):
            return None
        elif self.columns.count(colName) < 1:
            print "ERROR: Table doesn't have a column with", colName, 'name.'
            return None
        elif not self._getKeyColumn() and not self.rows[self.cursor[1] + y].has_key('__key__'):
            print 'ERROR: Table does not have a key Column or __key__ value.'
            return None
        else:
            retVal = self.rows[self.cursor[1] + y][self._getKeyColumn()]
            if self.rows[self.cursor[1] + y].has_key('__key__'):
                retVal = self.rows[self.cursor[1] + y]['__key__']
            return retVal

    def addRows(self, rows):
        keyCol = self._getKeyColumn()
        for entry in rows:
            if not entry.has_key(keyCol):
                print 'ERROR: Trying to add the entry without a key column:', entry
                return False
            for row in self.rows:
                if row[keyCol] == entry[keyCol]:
                    print 'ERROR: Table', self, 'already have an entry with the same key value.'
                    return False

        self.rows += rows
        self.renderTable()
        return True

    def alterRows(self, rows):
        keyCol = self._getKeyColumn()
        for row in rows:
            if not row.has_key(keyCol):
                print 'ERROR: row', row, 'dows not have a key'
                return False
            for _row in self.rows:
                if row[keyCol] == _row[keyCol]:
                    _row[keyCol].update(row[keyCol])

    def delRows(self, rows):
        keyCol = self._getKeyColumn()
        delIndexes = []
        for row in self.rows:
            for _row in rows:
                if row[keyCol] == _row:
                    delIndexes.append(self.rows.index(row))

        self.rows = filter(lambda i: self.rows.index(i) not in delIndexes, self.rows)
        self.dirty = True
        self.renderTable()

    def clear(self):
        rows = []
        keyCol = self._getKeyColumn()
        for row in self.rows:
            rows.append(row[keyCol])

        self.delRows(rows)

    def colBtnClick(self, colName):
        pass

    def onRowElement(self, col, row, btn):
        self.selection = [col, row + self.cursor[1]]
        if btn == 'LEFT':
            self.onSelectLeft()
        if btn == 'RIGHT':
            self.onSelectRight()
        self.renderTable()

    def onBoolElement(self, col, row, val):
        self.dataEditEvent(self._getRow(col, row), newVal)

    def isDirty(self):
        return self.dirty

    def updateScroll(self):
        self.minScroll = [0, 0]
        self.maxScroll = [0, 0]
        needV = len(self.rows) - self.props.visibleRows
        if needV > 0:
            self.maxScroll[1] = needV
            self.vScroll.setupScrollingInfo(needV)

    def doVScroll(self, down = True):
        if down:
            if self.cursor[1] < self.maxScroll[1]:
                self.cursor[1] += 1
                self.vScroll.doStep(True)
        elif self.cursor[1] > self.minScroll[1]:
            self.cursor[1] -= 1
            self.vScroll.doStep(False)
        self.renderTable()

    def doHScroll(self, right = True):
        pass

    def addColumn(self, colName, colCaption = u'', colWidth = 100, isKey = False, elemType = ITEMTYPE_TEXT):
        if isKey and self._getKeyColumn():
            print 'ERROR: Table', self, 'already have a Key column'
            print 'column', colName, 'can not be constructed'
            return False
        self.columns.append(colName)
        self.colData[colName] = (colCaption,
         colWidth,
         isKey,
         elemType)
        self.dirty = True
        return True

    def newStyle(self):
        self.dirty = True
        for i in xrange(1, self.props.visibleRows):
            if i < self.props.visibleRows:
                if hasattr(self.component, 'hLine' + str(i)):
                    cmp = self.component.__getattribute__('hLine' + str(i))
                    cmp.texture = self.dlmTexture

        self.component.texture = self.frameTexture
        self.renderTable()

    def getSelectedRow(self):
        retVal = self.rows[self.selection[1]][self._getKeyColumn()]
        if self.rows[self.selection[1]].has_key('__key__'):
            retVal = self.rows[self.selection[1]]['__key__']
        return retVal

    def handleMouseEvent(self, cmp, event):
        dx = event.dx
        dy = event.dy
        dz = event.dz
        position = event.cursorPosition
        if dz > 0:
            self.doVScroll(False)
            return True
        if dz < 0:
            self.doVScroll(True)
            return True
        return False

    def dataEditEvent(self, row, newVal):
        return None


class IsoCustomTableElement(object):

    def __init__(self, component):
        component.script = self

    def sendEvent(self, event, data):
        return None

    def onHover(self):
        return None

    def onSelect(self):
        return None


class soTablePropsStructure(object):

    def __init__(self, tableWidth = 400, tableHeight = 400, outerBorderWidth = 1, innerBorderWidth = 1, outerBorderColor = (255, 255, 255, 255), innerBorderColor = (255, 255, 255, 255)):
        self.tableWidth = tableWidth
        self.tableHeight = tableHeight
        self.outerBorderWidth = outerBorderWidth
        self.innerBorderWidth = innerBorderWidth
        self.innerBorderColor = innerBorderColor
        self.outerBorderColor = outerBorderColor


class soTableElemPropsStructure(object):

    def __init__(self, spanLeft = 0, spanDown = 0, dataType = ITEMTYPE_TEXT, dataStyles = {'font': 'ruRU_calibri_default.font',
 'color': (255, 255, 255, 255)}, rights = ['READ']):
        self.dataType = dataType
        self.dataStyles = dataStyles
        self.rights = rights
        self.spanLeft = spanLeft
        self.spanDown = spanDown


class soTableElem(PyGUIBase, soToolTipComponent):
    factoryString = 'soGUI.soTableElem'

    def __init__(self, component, parentRow, parentCol, parentTable, props = soTableElemPropsStructure()):
        PyGUIBase.__init__(self, component)
        self.props = props
        self.ttID = None if not props.dataStyles.has_key('toolTipID') else props.dataStyles['toolTipID']
        soToolTipComponent.__init__(self, component, self.ttID)
        component.script = self
        self.parentRow = parentRow
        self.parentCol = parentCol
        self.parentTable = parentTable
        self.selected = False
        self.mouseHover = False
        self.disabled = False
        self.setupRoot()
        self.setupContent()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        color = (0, 0, 0, 0)
        if self.props.dataStyles.has_key('color'):
            color = self.props.dataStyles['color']
        cmp.colour = color
        cmp.materialFX = 'BLEND'
        cmp.width = self.parentCol.getElemWidth(self.props.spanLeft)
        cmp.height = self.parentRow.getElemHeight(self.props.spanDown)
        cmp.texture = self.parentTable.elemBackGroundTextureProvider
        cmp.pixelSnap = False
        cmp.filterType = 'POINT'
        cmp.mouseButtonFocus = True

    def setupContent(self):
        if self.props.dataType == ITEMTYPE_TEXT:
            cmp = GUI.Text('')
            cmp.font = self.props.dataStyles['font']
            color = (255, 255, 255, 255)
            if self.props.dataStyles.has_key('contentColor'):
                color = self.props.dataStyles['contentColor']
            cmp.colour = color
            cmp.materialFX = 'BLEND'
            cmp.multiline = True
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.verticalAnchor = cmp.horizontalAnchor = 'CENTER'
            cmp.position = (0.0, 0.0, 0.2)
            self.component.addChild(cmp, 'textOut')
        elif self.props.dataType == ITEMTYPE_PICTURE:
            cmp = GUI.Simple('')
            color = (255, 255, 255, 255)
            if self.props.dataStyles.has_key('contentColor'):
                color = self.props.dataStyles['contentColor']
            cmp.colour = color
            cmp.materialFX = 'BLEND'
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.verticalAnchor = cmp.horizontalAnchor = 'CENTER'
            cmp.widthMode = cmp.heightMode = 'CLIP'
            cmp.width = cmp.height = 2.0
            cmp.position = (0.0, 0.0, 0.2)
            self.component.addChild(cmp, 'pictOut')
        elif self.props.dataType == ITEMTYPE_BOOL:
            cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=u''))
            cmp = cb.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (0.0, 0.0, 0.4)
            self.component.addChild(cmp, 'boolOut')
            cb.onBound()
            cb.onStateChange = partial(self.contentsEvent, 'CHECKBOX', None)
        elif self.props.dataType == ITEMTYPE_BUTTON:
            btn = soButtonWTT(GUI.Window(), self.ttID)
            btn.initVSC('soGUI/visual_styles/defaultBtnEmpty.xml')
            cmp = btn.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.widthMode = cmp.heightMode = 'CLIP'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.width = 2.0
            cmp.height = 2.0
            cmp.position = (0.0, 0.0, 0.2)
            btn.onClick = partial(self.contentsEvent, 'BUTTON', None)
            cmp.label.font = self.props.dataStyles['font']
            cmp.label.colour = (140, 141, 126, 255)
            cmp.label.text = u''
            self.component.addChild(cmp, 'btnOut')
            btn.onBound()
        return

    def setData(self, data):
        if 'READ' not in self.props.rights:
            if not hasattr(self.component, 'secrecyMarker'):
                cmp = GUI.Simple('')
                color = (255, 255, 255, 255)
                if self.props.dataStyles.has_key('contentColor'):
                    color = self.props.dataStyles['contentColor']
                cmp.colour = color
                cmp.materialFX = 'BLEND'
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
                cmp.verticalAnchor = cmp.horizontalAnchor = 'CENTER'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.width = cmp.height = 18
                cmp.position = (0.0, 0.0, 0.2)
                cmp.texture = self.parentTable.secretElemTextureProvider
                self.component.addChild(cmp, 'secrecyMarker')
            else:
                self.component.secrecyMarker.visible = True
        elif hasattr(self.component, 'secrecyMarker'):
            self.component.secrecyMarker.visible = False
        if self.props.dataType == ITEMTYPE_TEXT:
            if 'READ' in self.props.rights:
                self.component.textOut.text = data['text']
            else:
                self.component.textOut.text = u''
        elif self.props.dataType == ITEMTYPE_PICTURE:
            if 'READ' in self.props.rights:
                if isinstance(data['picture'], BigWorld.PyTextureProvider):
                    self.component.pictOut.texture = data['picture']
                else:
                    self.component.pictOut.textureName = data['picture']
            else:
                self.component.pictOut.textureName = ''
        elif self.props.dataType == ITEMTYPE_BOOL:
            if 'READ' in self.props.rights:
                self.component.boolOut.script.setLabel(data['text'])
                if data['boolState']:
                    self.component.boolOut.script.setActive()
                else:
                    self.component.boolOut.script.setInactive()
            else:
                self.component.boolOut.visible = False
        elif self.props.dataType == ITEMTYPE_BUTTON:
            if 'READ' in self.props.rights:
                self.component.btnOut.label.text = data['text']
                self.component.btnOut.script.initVSC(data['btnVS'])
                self.component.btnOut.script.setVisualState('normal')
            else:
                self.component.btnOut.visible = False

    def getData(self):
        return self.parentRow.elements[self.parentCol.colName]['data']

    def handleMouseEnterEvent(self, component):
        self.hover(True)
        soToolTipComponent.handleMouseEnterEvent(self, component)
        return True

    def handleMouseLeaveEvent(self, component):
        self.hover(False)
        soToolTipComponent.handleMouseLeaveEvent(self, component)
        return True

    def handleMouseButtonEvent(self, comp, event):
        down = event.isKeyDown()
        key = event.key
        modifiers = event.modifiers
        if down:
            if key == KEY_LEFTMOUSE:
                self.parentTable.elementEvent(self.parentCol.colName, self.parentRow.rowIndex, 'LEFTMOUSE', None)
            elif key == KEY_RIGHTMOUSE:
                self.parentTable.elementEvent(self.parentCol.colName, self.parentRow.rowIndex, 'RIGHTMOUSE', None)
        return True

    def contentsEvent(self, event, data):
        if event == 'CHECKBOX':
            self.parentTable.editEvent(self.parentCol.colName, self.parentRow.rowIndex, event, self.component.boolOut.script.isChecked())
        if event == 'BUTTON':
            self.parentTable.editEvent(self.parentCol.colName, self.parentRow.rowIndex, event, None)
        return

    def updateVisual(self):
        if self.selected or self.mouseHover:
            cmp = self.component
            color = (0, 0, 0, 0)
            if self.props.dataStyles.has_key('selectColor'):
                color = self.props.dataStyles['selectColor']
            cmp.colour = color
            cmp = None
            if self.props.dataType == ITEMTYPE_TEXT:
                cmp = self.component.textOut
            elif self.props.dataType == ITEMTYPE_PICTURE:
                cmp = self.component.pictOut
            elif self.props.dataType == ITEMTYPE_BOOL:
                cmp = self.component.boolOut
            if cmp is not None:
                color = (0, 0, 0, 0)
                if self.selected and self.props.dataStyles.has_key('contentColorSelect'):
                    color = self.props.dataStyles['contentColorSelect']
                elif self.mouseHover and self.props.dataStyles.has_key('contentColorHover'):
                    color = self.props.dataStyles['contentColorHover']
                cmp.colour = color
            return
        else:
            cmp = self.component
            color = (0, 0, 0, 0)
            if self.props.dataStyles.has_key('color'):
                color = self.props.dataStyles['color']
            cmp.colour = color
            cmp = None
            if self.props.dataType == ITEMTYPE_TEXT:
                cmp = self.component.textOut
            elif self.props.dataType == ITEMTYPE_PICTURE:
                cmp = self.component.pictOut
            elif self.props.dataType == ITEMTYPE_BOOL:
                cmp = self.component.boolOut
            if cmp is not None:
                color = (0, 0, 0, 0)
                if self.props.dataStyles.has_key('contentColor'):
                    color = self.props.dataStyles['contentColor']
                cmp.colour = color
            return

    def select(self):
        self.selected = True
        self.updateVisual()

    def deselect(self):
        self.selected = False
        self.updateVisual()

    def hover(self, mouseIn = True):
        self.mouseHover = mouseIn
        self.updateVisual()

    def delElem(self):
        self.parentCol = None
        self.parentRow = None
        self.parentTable = None
        if self.props.dataType == ITEMTYPE_BOOL:
            self.component.boolOut.script.fini()
            self.component.boolOut.script.onStateChange = None
        return


class soTableRow(object):

    def __init__(self, rowIndex, parentTable, rowHeight = 30, tablePart = 'MIDDLE', attachment = None):
        self.rowIndex = rowIndex
        self.rowHeight = rowHeight
        self.tablePart = tablePart
        self.parentTable = parentTable
        self.attachment = attachment
        self.elements = {}

    def addElements(self, elems):
        self.elements.update(elems)

    def removeElements(self, colNames):
        for colName in colNames:
            if self.elements.has_key(colName):
                del self.elements[colName]

    def getElemHeight(self, spanDown = 0):
        retVal = 0
        if self.parentTable.isSideRow(self.rowIndex):
            retVal = self.rowHeight
        else:
            retVal = self.rowHeight - self.parentTable.props.innerBorderWidth
        for i in xrange(spanDown):
            tryIndex = 1
            rowIndex = i + tryIndex + self.rowIndex
            row = self.parentTable._getRowByIndex(rowIndex)
            while row.tablePart != self.tablePart and row is not None:
                tryIndex += 1
                rowIndex = i + tryIndex + self.rowIndex
                row = self.parentTable._getRowByIndex(rowIndex)

            if row is not None:
                retVal += row.getElemHeight() + self.parentTable.props.innerBorderWidth

        return retVal

    def getRowHeight(self):
        return self.rowHeight

    def delRow(self):
        self.parentTable = None
        self.elements = None
        self.attachment = None
        return


class soTableCol(object):

    def __init__(self, colName, colIndex, parentTable, colWidth = 150, attachment = None):
        self.colName = colName
        self.colWidth = colWidth
        self.colIndex = colIndex
        self.parentTable = parentTable
        self.attachment = None
        return

    def getElemWidth(self, spanLeft = 0):
        retVal = 0
        if self.parentTable.isSideCol(self.colName):
            retVal = self.colWidth - self.parentTable.props.outerBorderWidth - self.parentTable.props.innerBorderWidth
        else:
            retVal = self.colWidth - self.parentTable.props.innerBorderWidth
        for i in xrange(spanLeft):
            colIndex = i + 1 + self.colIndex
            col = self.parentTable._getColByIndex(colIndex)
            if col is not None:
                retVal += col.getElemWidth() + self.parentTable.props.innerBorderWidth

        return retVal

    def getColWidth(self):
        return self.colWidth


class soTableComponent2(PyGUIBase):
    factoryString = 'soGUI.soTableComponent2'
    STUBROW_HEIGHT = 25

    def __init__(self, component, tableProps = soTablePropsStructure(), isDefaultScrollBar = 'TRUE', isFriendList = 'FALSE'):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.props = tableProps
        self.dirtyTop = True
        self.dirtyBottom = True
        self.dirtyMid = True
        self.dirtyTable = True
        self.isFriendList = isFriendList
        self.editedRow = None
        self.editedCol = None
        self.highestVSpan = 0
        self.widestHSpan = 0
        self.selectedElems = []
        self.isDefaultScrollBar = isDefaultScrollBar
        self.editing = False
        self.rows = []
        self.cols = []
        self.cursor = [0, 0]
        self.minMaxV = [0, 0]
        self.minMaxH = [0, 0]
        self.delayedRender = 0
        self.elemBackGroundTextureProvider = BigWorld.PyTextureProvider('soGUI/maps/Colours/white.tga')
        self.markUpTextureProvider = BigWorld.PyTextureProvider('soGUI/maps/Colours/white.tga')
        self.secretElemTextureProvider = BigWorld.PyTextureProvider('soGUI/maps/Controls/Table/classified_cell.tga')
        self.selectorColour = (255, 125, 56, 255)
        self.markUpColour = self.props.innerBorderColor
        self.setupRoot()
        if self.isFriendList == 'FALSE':
            if isDefaultScrollBar == 'TRUE':
                self.setupScroll()
            else:
                self.setupScrollForSettings()
        else:
            self.setupScrollForFriendList()
        self.setupTyper()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = self.props.tableWidth
        cmp.height = self.props.tableHeight
        cmp.textureName = ''
        cmp.pixelSnap = False
        cmp.filterType = 'POINT'
        cmp.mouseButtonFocus = True
        cmp.moveFocus = True
        cmp.crossFocus = True
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.width = self.props.tableWidth - 16
        cmp.height = self.props.tableHeight - 16
        cmp.position = (0, 0, 0.7)
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        self.component.addChild(cmp, 'midRowsHolder')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.width = self.props.tableWidth - 16
        cmp.height = self.props.tableHeight - 16
        cmp.position = (0, 0, 0.5)
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        self.component.addChild(cmp, 'topRowsHolder')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.width = self.props.tableWidth - 16
        cmp.height = self.props.tableHeight - 16
        cmp.position = (0, 0, 0.6)
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        self.component.addChild(cmp, 'bottomRowsHolder')

    def setupScroll(self):
        scroll = soScrollBar2(GUI.Window(), width=16, height=self.props.tableHeight - self.props.outerBorderWidth * 2 - 16, steps=0)
        cmp = scroll.component
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.horizontalPositionMode = 'PIXEL'
        cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (self.props.tableWidth - self.props.outerBorderWidth + 1, self.props.outerBorderWidth, 0.1)
        scroll.setVisualState('normal')
        scroll.onBound()
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        self.component.addChild(cmp, 'vScroll')
        scroll.setSteps(0)
        scroll = soScrollBar2(GUI.Window(), width=16, height=self.props.tableWidth - self.props.outerBorderWidth * 2 - 16, steps=0, horizontal=True)
        cmp = scroll.component
        cmp.verticalAnchor = 'BOTTOM'
        cmp.horizontalAnchor = 'LEFT'
        cmp.horizontalPositionMode = 'PIXEL'
        cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (self.props.outerBorderWidth, self.props.tableHeight - self.props.outerBorderWidth, 0.1)
        scroll.setVisualState('normal')
        scroll.onBound()
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        self.component.addChild(cmp, 'hScroll')
        scroll.setSteps(0)

    def setupScrollForSettings(self):
        scroll = soScrollBar2(GUI.Window(), width=16, height=self.props.tableHeight - self.props.outerBorderWidth * 2 - 50, steps=0, style='soGUI/visual_styles/ScrollBarSettings.xml')
        cmp = scroll.component
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.horizontalPositionMode = 'PIXEL'
        cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (self.props.tableWidth - self.props.outerBorderWidth, self.props.outerBorderWidth + 30, 0.1)
        scroll.setVisualState('normal')
        scroll.onBound()
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        self.component.addChild(cmp, 'vScroll')
        scroll.setSteps(0)
        scroll = soScrollBar2(GUI.Window(), width=16, height=self.props.tableWidth - self.props.outerBorderWidth * 2 - 16, steps=0, horizontal=True)
        cmp = scroll.component
        cmp.verticalAnchor = 'BOTTOM'
        cmp.horizontalAnchor = 'LEFT'
        cmp.horizontalPositionMode = 'PIXEL'
        cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (self.props.outerBorderWidth, self.props.tableHeight - self.props.outerBorderWidth, 0.1)
        scroll.setVisualState('normal')
        scroll.onBound()
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        self.component.addChild(cmp, 'hScroll')
        scroll.setSteps(0)

    def setupScrollForFriendList(self):
        scroll = soScrollBar2(GUI.Window(), width=16, height=self.props.tableHeight - 2, steps=0, style='soGUI/visual_styles/ScrollBarSettings.xml')
        cmp = scroll.component
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.horizontalPositionMode = 'PIXEL'
        cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (self.props.tableWidth - 5, 2, 0.1)
        scroll.setVisualState('normal')
        scroll.onBound()
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        self.component.addChild(cmp, 'vScroll')
        scroll.setSteps(0)
        scroll = soScrollBar2(GUI.Window(), width=16, height=self.props.tableWidth - self.props.outerBorderWidth * 2 - 16, steps=0, horizontal=True)
        cmp = scroll.component
        cmp.verticalAnchor = 'BOTTOM'
        cmp.horizontalAnchor = 'LEFT'
        cmp.horizontalPositionMode = 'PIXEL'
        cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (self.props.outerBorderWidth, self.props.tableHeight - self.props.outerBorderWidth, 0.1)
        scroll.setVisualState('normal')
        scroll.onBound()
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        self.component.addChild(cmp, 'hScroll')
        scroll.setSteps(0)

    def setupTyper(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.width = 0
        cmp.height = 0
        cmp.position = (0, 0, 0.05)
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        self.component.addChild(cmp, 'inputHolder')
        edit = soEditField2(GUI.Window(), width=10, height=25, font='ruRU_calibri_small.font')
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (0, 0, 0.1)
        self.component.inputHolder.addChild(cmp, 'edit')
        edit.onBound()

    def addCols(self, cols):
        if not cols:
            return False
        for col in cols:
            tableCol = soTableCol(col[0], len(self.cols), self, col[1])
            self.cols.append(tableCol)

    def _checkForMaxSpan(self, elems):
        for elem in elems:
            props = elems[elem]['props']
            if props.spanLeft > self.widestHSpan:
                self.widestHSpan = props.spanLeft
            if props.spanDown > self.highestVSpan:
                self.highestVSpan = props.spanDown

    def addRows(self, rows):
        if not rows:
            return False
        else:
            for row in rows:
                if row[0][1] == 'TOP':
                    self.dirtyTop = True
                elif row[0][1] == 'MIDDLE':
                    self.dirtyMid = True
                elif row[0][1] == 'BOTTOM':
                    self.dirtyBottom = True
                else:
                    print 'ERROR in table', self, ': trying to add a row with invalid target area, skipping.'
                    continue
                attachment = None if len(row[0]) < 3 else row[0][2]
                tableRow = soTableRow(len(self.rows), self, row[0][0], row[0][1], attachment)
                self._checkForMaxSpan(row[1])
                tableRow.addElements(row[1])
                self.rows.append(tableRow)

            self.renderTable()
            return

    def alterElem(self, colName, rowIndex, props, data):
        row = self._getRowByIndex(rowIndex)
        if row is None:
            return
        else:
            if row.tablePart == 'TOP':
                self.dirtyTop = True
            elif row.tablePart == 'MIDDLE':
                self.dirtyMid = True
            elif row.tablePart == 'BOTTOM':
                self.dirtyBottom = True
            row.elements[colName]['props'] = props
            row.elements[colName]['data'] = data
            self._checkForMaxSpan(row.elements)
            self.renderTable()
            return

    def showTyper(self, row, col, doShow = True):
        if not doShow:
            self.editing = False
            cmp = self.component.inputHolder
            cmp.visible = False
            cmp = self.component.inputHolder.edit
            cmp.visible = False
            cmp.script.setValue('')
            if cmp.script.isEditActive():
                cmp.script.setActive(False)
        else:
            self.editedRow = row
            self.editedCol = col
            self.editing = True
            holder = None
            rowObj = self._getRowByIndex(row)
            if rowObj.tablePart == 'TOP':
                holder = self.component.topRowsHolder
            elif rowObj.tablePart == 'MIDDLE':
                holder = self.component.midRowsHolder
            elif rowObj.tablePart == 'BOTTOM':
                holder = self.component.bottomRowsHolder
            elemCmp = getattr(holder, 'elem_' + str(row) + '_' + str(col))
            cmp = self.component.inputHolder
            cmp.visible = True
            if elemCmp.width < self.props.tableWidth - self.props.outerBorderWidth * 2 - 16:
                cmp.width = elemCmp.width
            else:
                cmp.width = self.props.tableWidth - self.props.outerBorderWidth * 2 - 16
            cmp.height = elemCmp.height
            cmp.position.x = holder.position.x + elemCmp.position.x
            cmp.position.y = holder.position.y + elemCmp.position.y if rowObj.tablePart != 'TOP' else holder.position.y + elemCmp.position.y - elemCmp.height
            cmp = self.component.inputHolder.edit
            cmp.visible = True
            cmp.script.setWidth(self.component.inputHolder.width)
            cmp.script.setHeight(self.component.inputHolder.height)
            data = elemCmp.script.getData()
            cmp.script.setActive(True)
            cmp.script.setValue(data['text'])
        return

    def delayRender(self, steps = 1):
        self.delayedRender += steps

    def removeRows(self, rowIndexes):
        self.dirtyTop = True
        self.dirtyMid = True
        self.dirtyBottom = True
        for rowIdx in rowIndexes:
            row = self._getRowByIndex(rowIdx)
            if row is not None:
                listIdx = self.rows.index(row)
                row.delRow()
                self.rows[listIdx] = None

        self.renderTable()
        return

    def rewriteRow(self, rowIndex, newRow):
        listIdx = -1
        for row in self.rows:
            if row is None:
                continue
            if row.rowIndex == rowIndex:
                listIdx = self.rows.index(row)
                row.delRow()

        if listIdx >= 0:
            del self.rows[listIdx]
            attachment = None if len(newRow[0]) < 3 else newRow[0][2]
            tableRow = soTableRow(rowIndex, self, newRow[0][0], newRow[0][1], attachment)
            self.rows.insert(listIdx, tableRow)
            tableRow.addElements(newRow[1])
            if newRow[0][1] == 'TOP':
                self.dirtyTop = True
            elif newRow[0][1] == 'MIDDLE':
                self.dirtyMid = True
            elif newRow[0][1] == 'BOTTOM':
                self.dirtyBottom = True
        self.renderTable()
        return

    def _getVisibleColsWidth(self):
        tw, th = self._getTableSize()
        vw = 0
        for i in xrange(self.cursor[0], len(self.cols)):
            col = self._getColByIndex(i)
            vw += col.getColWidth()
            if vw >= tw:
                return vw

        return vw

    def _getTableSize(self):
        return [self.props.tableWidth, self.props.tableHeight]

    def _getColX(self, colName):
        retVal = self.props.outerBorderWidth
        invisWidth = 0
        for col in self.cols[:self.cursor[0]]:
            invisWidth += col.getColWidth()

        for col in self.cols:
            if col.colName == colName:
                return retVal - invisWidth
            retVal += col.getColWidth()

        return -1

    def isSideCol(self, colName):
        col = self._getColByName(colName)
        if col is not None:
            colIndex = self.cols.index(col)
            if colIndex == len(self.cols) - 1:
                return True
            else:
                return False
        return

    def isSideRow(self, rowIndex):
        row = self._getRowByIndex(rowIndex)
        if row is not None:
            rowIdx = self.rows.index(row)
            if rowIdx == len(self.rows) - 1 or rowIdx == 0:
                return True
            else:
                return False
        return

    def _getVisibleColsWidth(self):
        retVal = 0
        for col in self.cols:
            retVal += col.getColWidth()

        return retVal

    def _getColByName(self, colName):
        retVal = None
        for col in self.cols:
            if col.colName == colName:
                retVal = col

        return retVal

    def _getColByIndex(self, colIndex):
        retVal = None
        for col in self.cols:
            if col.colIndex == colIndex:
                retVal = col

        return retVal

    def _getRowByIndex(self, rowIndex):
        retVal = None
        for row in self.rows:
            if row is None:
                continue
            if row.rowIndex == rowIndex:
                retVal = row

        return retVal

    def _getTopRowsHeight(self):
        retVal = 0
        for row in self.rows:
            if row is None:
                continue
            if row.tablePart == 'TOP':
                retVal += row.getRowHeight()

        retVal += self.props.outerBorderWidth
        return retVal

    def _getBottomRowsHeight(self):
        retVal = 0
        for row in self.rows:
            if row is None:
                continue
            if row.tablePart == 'BOTTOM':
                retVal += row.getRowHeight()

        retVal += self.props.outerBorderWidth
        if self.component.hScroll.visible:
            retVal += 16
        return retVal

    def _calculateMinMaxV(self, midAreaHeight):
        midRows = filter(lambda row: row is not None and row.tablePart == 'MIDDLE', self.rows)
        vh = 0
        rowIndex = len(midRows) - 1
        rowCount = 0
        while rowIndex >= 0 and vh < midAreaHeight:
            row = midRows[rowIndex]
            vh += row.getRowHeight()
            rowIndex -= 1
            rowCount += 1

        if vh > midAreaHeight:
            rowCount -= 1
        self.minMaxV[0] = 0
        max = 0 if len(midRows) - rowCount <= 0 else len(midRows) - rowCount
        self.minMaxV[1] = max
        self.component.vScroll.script.setSteps(max)
        return self.minMaxV

    def _calculateMinMaxH(self):
        colsWidth = 0
        min = 0
        max = 0
        for col in self.cols:
            colsWidth += col.getColWidth()
            if colsWidth > self.props.tableWidth:
                max += 1

        self.minMaxH[0] = min
        self.minMaxH[1] = max
        self.component.hScroll.script.setSteps(max)
        self._updateScrollVisuals()
        return self.minMaxH

    def _updateScrollVisuals(self):
        hideHorizontal = False
        if self.minMaxH[1] <= 0:
            hideHorizontal = True
        self.component.hScroll.visible = not hideHorizontal

    def renderTable(self):
        renderNearbySpannedElems = False
        if self.delayedRender > 0:
            self.delayedRender -= 1
            return
        else:
            self._calculateMinMaxH()
            topRows = []
            midRows = []
            bottomRows = []
            tW, tH = self._getTableSize()
            for row in self.rows:
                if row is None:
                    continue
                if row.tablePart == 'TOP':
                    topRows.append(row)
                elif row.tablePart == 'MIDDLE':
                    midRows.append(row)
                elif row.tablePart == 'BOTTOM':
                    bottomRows.append(row)

            visibleHeightTop = self.props.outerBorderWidth
            visibleHeightMid = 0
            visibleHeightBottom = 0
            if self.component.hScroll.visible:
                visibleHeightBottom = 16
            if self.dirtyTop:
                self.dirtyMid = True
                self.clearAllChildren(self.component.topRowsHolder)
                self.component.topRowsHolder.width = tW
                self.component.topRowsHolder.height = visibleHeightTop
                self.component.topRowsHolder.position.x = 0
                self.component.topRowsHolder.position.y = 0
                self.component.topRowsHolder.position.z = 0.5
                for row in topRows:
                    for col in self.cols[self.cursor[0]:]:
                        elem = col.colName
                        if not row.elements.has_key(elem):
                            continue
                        tableElem = soTableElem(GUI.Window(), row, self._getColByName(elem), self, row.elements[elem]['props'])
                        tableElem.onBound()
                        cmp = tableElem.component
                        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                        cmp.horizontalAnchor = 'LEFT'
                        cmp.verticalAnchor = 'TOP'
                        cmp.position.x = self._getColX(elem)
                        cmp.position.y = visibleHeightTop
                        cmp.position.z = 0.5
                        self.component.topRowsHolder.addChild(cmp, 'elem_' + str(row.rowIndex) + '_' + str(elem))
                        tableElem.setData(row.elements[elem]['data'])
                        cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=tableElem.component.width + self.props.innerBorderWidth, height=self.props.innerBorderWidth, colour=self.markUpColour)
                        cmp.texture = self.markUpTextureProvider
                        cmp.position = (self._getColX(elem), visibleHeightTop + tableElem.component.height, 0.15)
                        self.component.topRowsHolder.addChild(cmp, 'hLine' + str(row.rowIndex) + '_' + str(elem))
                        cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self.props.innerBorderWidth, height=tableElem.component.height, colour=self.markUpColour)
                        cmp.texture = self.markUpTextureProvider
                        cmp.position = (self._getColX(elem) + tableElem.component.width, visibleHeightTop, 0.15)
                        self.component.topRowsHolder.addChild(cmp, 'vLine' + str(row.rowIndex) + '_' + str(elem))

                    visibleHeightTop += row.getRowHeight()
                    self.component.topRowsHolder.height = visibleHeightTop

                visibleHeightTop += self.props.innerBorderWidth
                self.component.topRowsHolder.height = visibleHeightTop
                cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self.props.tableWidth, height=self.props.outerBorderWidth, colour=self.markUpColour)
                cmp.texture = self.markUpTextureProvider
                cmp.position = (0, 0, 0.2)
                self.component.topRowsHolder.addChild(cmp, 'topHLine')
                cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self.props.outerBorderWidth, height=visibleHeightTop, colour=self.markUpColour)
                cmp.texture = self.markUpTextureProvider
                cmp.position = (0, 0, 0.2)
                self.component.topRowsHolder.addChild(cmp, 'leftVLine')
                cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self.props.outerBorderWidth, height=visibleHeightTop, colour=self.markUpColour, hAnchor='RIGHT')
                cmp.texture = self.markUpTextureProvider
                cmp.position = (self.props.tableWidth, 0, 0.2)
                self.component.topRowsHolder.addChild(cmp, 'rightVLine')
            else:
                visibleHeightTop = self._getTopRowsHeight()
            if self.dirtyBottom:
                self.dirtyMid = True
                self.clearAllChildren(self.component.bottomRowsHolder)
                self.component.bottomRowsHolder.width = tW
                self.component.bottomRowsHolder.height = visibleHeightBottom
                self.component.bottomRowsHolder.position.x = 0
                self.component.bottomRowsHolder.position.y = tH
                self.component.bottomRowsHolder.position.z = 0.6
                for row in bottomRows:
                    for col in self.cols[self.cursor[0]:]:
                        elem = col.colName
                        if not row.elements.has_key(elem):
                            continue
                        tableElem = soTableElem(GUI.Window(), row, self._getColByName(elem), self, row.elements[elem]['props'])
                        tableElem.onBound()
                        cmp = tableElem.component
                        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                        cmp.horizontalAnchor = 'LEFT'
                        cmp.verticalAnchor = 'TOP'
                        cmp.position.x = self._getColX(elem)
                        cmp.position.y = visibleHeightBottom + self.props.innerBorderWidth - 16
                        cmp.position.z = 0.5
                        self.component.bottomRowsHolder.addChild(cmp, 'elem_' + str(row.rowIndex) + '_' + str(elem))
                        tableElem.setData(row.elements[elem]['data'])
                        cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=tableElem.component.width + self.props.innerBorderWidth, height=self.props.innerBorderWidth, colour=self.markUpColour, vAnchor='TOP')
                        cmp.texture = self.markUpTextureProvider
                        cmp.position = (self._getColX(elem), visibleHeightBottom - 16, 0.15)
                        self.component.bottomRowsHolder.addChild(cmp, 'hLine' + str(row.rowIndex) + '_' + str(elem))
                        cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self.props.innerBorderWidth, height=tableElem.component.height, colour=self.markUpColour, hAnchor='LEFT')
                        cmp.texture = self.markUpTextureProvider
                        cmp.position = (self._getColX(elem) + tableElem.component.width, visibleHeightBottom + self.props.innerBorderWidth - 16, 0.15)
                        self.component.bottomRowsHolder.addChild(cmp, 'vLine' + str(row.rowIndex) + '_' + str(elem))

                    visibleHeightBottom += row.getRowHeight()
                    self.component.bottomRowsHolder.height = visibleHeightBottom

                visibleHeightBottom += self.props.outerBorderWidth
                self.component.bottomRowsHolder.height = visibleHeightBottom
                cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self.props.outerBorderWidth, height=visibleHeightBottom, colour=self.markUpColour)
                cmp.texture = self.markUpTextureProvider
                cmp.position = (0, 0, 0.2)
                self.component.bottomRowsHolder.addChild(cmp, 'leftVLine')
                cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self.props.outerBorderWidth, height=visibleHeightBottom, colour=self.markUpColour, hAnchor='RIGHT')
                cmp.texture = self.markUpTextureProvider
                cmp.position = (self.props.tableWidth, 0, 0.2)
                self.component.bottomRowsHolder.addChild(cmp, 'rightVLine')
                cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self.props.tableWidth, height=self.props.outerBorderWidth, colour=self.markUpColour, vAnchor='BOTTOM')
                cmp.texture = self.markUpTextureProvider
                cmp.position = (0, visibleHeightBottom, 0.2)
                self.component.bottomRowsHolder.addChild(cmp, 'botHLine')
            else:
                visibleHeightBottom = self._getBottomRowsHeight()
            midRowIndex = self.cursor[1] - self.highestVSpan
            if midRowIndex < 0:
                midRowIndex = 0
            midAreaHeight = tH - (visibleHeightTop + visibleHeightBottom)
            freeMidHeight = midAreaHeight
            if self.dirtyMid:
                self.clearAllChildren(self.component.midRowsHolder)
                self.component.midRowsHolder.width = tW
                self.component.midRowsHolder.height = 0
                self.component.midRowsHolder.position.x = 0
                self.component.midRowsHolder.position.y = visibleHeightTop
                self.component.midRowsHolder.position.z = 0.7
                while visibleHeightMid < midAreaHeight and midRowIndex < len(midRows):
                    row = midRows[midRowIndex]
                    midRowIndex += 1
                    startIdx = self.cursor[0] - self.widestHSpan
                    if startIdx < 0:
                        startIdx = 0
                    colSlice = self.cols[startIdx:]
                    for col in colSlice:
                        elem = col.colName
                        listIndex = midRows.index(row)
                        vCoord = visibleHeightMid
                        if not row.elements.has_key(elem):
                            continue
                        if self.cols.index(col) < self.cursor[0] and row.elements[elem]['props'].spanLeft == 0:
                            continue
                        if listIndex < self.cursor[1] and row.elements[elem]['props'].spanDown == 0:
                            continue
                        tableElem = soTableElem(GUI.Window(), row, self._getColByName(elem), self, row.elements[elem]['props'])
                        tableElem.onBound()
                        cmp = tableElem.component
                        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                        cmp.horizontalAnchor = 'LEFT'
                        cmp.verticalAnchor = 'TOP'
                        cmp.position.x = self._getColX(elem)
                        if listIndex < self.cursor[1] and row.elements[elem]['props'].spanDown > 0:
                            vOffset = 0
                            scrolledCount = self.cursor[1] - listIndex
                            for midRow in midRows[listIndex:listIndex + scrolledCount]:
                                vOffset += midRow.getRowHeight()

                            vCoord -= vOffset
                        cmp.position.y = vCoord
                        cmp.position.z = 0.5
                        self.component.midRowsHolder.addChild(cmp, 'elem_' + str(row.rowIndex) + '_' + str(elem))
                        tableElem.setData(row.elements[elem]['data'])
                        cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=tableElem.component.width + self.props.innerBorderWidth, height=self.props.innerBorderWidth, colour=self.markUpColour)
                        cmp.texture = self.markUpTextureProvider
                        cmp.position = (self._getColX(elem), vCoord + tableElem.component.height, 0.15)
                        self.component.midRowsHolder.addChild(cmp, 'hLine' + str(row.rowIndex) + '_' + str(elem))
                        cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self.props.innerBorderWidth, height=tableElem.component.height, colour=self.markUpColour, hAnchor='LEFT')
                        cmp.texture = self.markUpTextureProvider
                        cmp.position = (self._getColX(elem) + tableElem.component.width, visibleHeightMid, 0.15)
                        self.component.midRowsHolder.addChild(cmp, 'vLine' + str(row.rowIndex) + '_' + str(elem))

                    if midRows.index(row) >= self.cursor[1]:
                        visibleHeightMid += row.getRowHeight()
                        freeMidHeight = midAreaHeight - visibleHeightMid
                    self._calculateMinMaxV(midAreaHeight)

                self.component.midRowsHolder.height = midAreaHeight
                if freeMidHeight > 0:
                    for i in xrange(self.cursor[0], len(self.cols)):
                        col = self._getColByIndex(i)
                        cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self.props.innerBorderWidth, height=freeMidHeight, colour=self.markUpColour, hAnchor='LEFT')
                        cmp.texture = self.markUpTextureProvider
                        cmp.position = (self._getColX(col.colName) + col.getElemWidth(), visibleHeightMid, 0.15)
                        self.component.midRowsHolder.addChild(cmp, 'vLine_stub' + str(i))

                    for i in xrange(1, int(ceil(freeMidHeight / self.STUBROW_HEIGHT)) + 1):
                        cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self._getVisibleColsWidth(), height=self.props.innerBorderWidth, colour=self.markUpColour)
                        cmp.texture = self.markUpTextureProvider
                        cmp.position = (0, visibleHeightMid + i * self.STUBROW_HEIGHT, 0.15)
                        self.component.midRowsHolder.addChild(cmp, 'hLine_stub' + str(i))

                cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self.props.outerBorderWidth, height=midAreaHeight, colour=self.markUpColour)
                cmp.texture = self.markUpTextureProvider
                cmp.position = (0, 0, 0.2)
                self.component.midRowsHolder.addChild(cmp, 'leftVLine')
                cmp = BWPersonality.GUICore.createGenericGUICmp(tiled=True, width=self.props.outerBorderWidth, height=midAreaHeight, colour=self.markUpColour, hAnchor='RIGHT')
                cmp.texture = self.markUpTextureProvider
                cmp.position = (self.props.tableWidth, 0, 0.2)
                self.component.midRowsHolder.addChild(cmp, 'rightVLine')
            self.dirtyTop = False
            self.dirtyMid = False
            self.dirtyBottom = False
            return

    def scrollTableV(self, down = True, steps = 1):
        if down:
            self.cursor[1] += 1
        else:
            self.cursor[1] -= 1
        if self.cursor[1] < self.minMaxV[0]:
            self.cursor[1] = self.minMaxV[0]
        if self.cursor[1] > self.minMaxV[1]:
            self.cursor[1] = self.minMaxV[1]
        self.dirtyMid = True
        self.component.vScroll.script.setValue(self.cursor[1])
        self.renderTable()

    def scrollTableH(self, right = True, steps = 1):
        if right:
            self.cursor[0] += 1
        else:
            self.cursor[0] -= 1
        if self.cursor[0] < self.minMaxH[0]:
            self.cursor[0] = self.minMaxH[0]
        if self.cursor[0] > self.minMaxH[1]:
            self.cursor[0] = self.minMaxH[1]
        self.dirtyTop = True
        self.dirtyMid = True
        self.dirtyBottom = True
        self.component.hScroll.script.setValue(self.cursor[0])
        self.renderTable()

    def handleMouseEvent(self, cmp, event):
        dx = event.dx
        dy = event.dy
        dz = event.dz
        position = event.cursorPosition
        if dz > 0:
            self.scrollTableV(False, 1)
            return True
        if dz < 0:
            self.scrollTableV(True, 1)
            return True
        return False

    def getRowByIndex(self, index):
        row = self._getRowByIndex(index)
        return row.elements

    def getRowAttachmentByIndex(self, index):
        row = self._getRowByIndex(index)
        return row.attachment

    def getRowIndexByValue(self, val, colName, start = 0, end = -1):
        if end < 0:
            end = len(self.rows)
        rowRange = []
        for row in self.rows:
            if row is None:
                continue
            if row.rowIndex >= start and row.rowIndex < end:
                rowRange.append(row)

        for row in rowRange:
            if row.elements.has_key(colName):
                if row.elements[colName]['data'] == val:
                    return row.rowIndex

        return -1

    def getRowIndexByAttachment(self, attachment, start = 0, end = -1):
        if end < 0:
            end = len(self.rows)
        rowRange = []
        for row in self.rows:
            if row is None:
                continue
            if row.rowIndex >= start and row.rowIndex < end:
                rowRange.append(row)

        for row in rowRange:
            if row.attachment == attachment:
                return row.rowIndex

        return -1

    def getSelection(self):
        data = []
        for elem in self.selectedElems:
            data.append(elem)

        return data

    def selectElem(self, col, row, doSelect = True):
        rowObj = self._getRowByIndex(row)
        if rowObj is None:
            print 'ERROR in table', self, 'there is no such row.'
            return False
        else:
            holder = None
            if rowObj.tablePart == 'TOP':
                holder = self.component.topRowsHolder
            elif rowObj.tablePart == 'MIDDLE':
                holder = self.component.midRowsHolder
            elif rowObj.tablePart == 'BOTTOM':
                holder = self.component.bottomRowsHolder
            elemCmp = getattr(holder, 'elem_' + str(row) + '_' + str(col))
            if doSelect:
                elemCmp.script.select()
                data = (col, row)
                self.selectedElems.append(data)
            else:
                elemCmp.script.deselect()
                data = (col, row)
                if contains(self.selectedElems, data):
                    self.selectedElems.remove(data)
            return True

    def clearTable(self):
        self.dirtyTop = True
        self.dirtyMid = True
        self.dirtyBottom = True
        self.rows = []
        self.renderTable()

    def clearRowRange(self, start = 0, end = -1):
        self.dirtyTop = True
        self.dirtyMid = True
        self.dirtyBottom = True
        if end < 0:
            end = len(self.rows)
        for row in self.rows:
            if row is None:
                continue
            if row.rowIndex >= start and row.rowIndex < end:
                listIdx = self.rows.index(row)
                row.delRow()
                self.rows[listIdx] = None

        self.renderTable()
        return

    def clearSelection(self):
        for selElem in self.selectedElems:
            rowObj = self._getRowByIndex(selElem[1])
            if rowObj is None:
                print 'ERROR in table', self, 'there is not such row.'
                return False
            holder = None
            if rowObj.tablePart == 'TOP':
                holder = self.component.topRowsHolder
            elif rowObj.tablePart == 'MIDDLE':
                holder = self.component.midRowsHolder
            elif rowObj.tablePart == 'BOTTOM':
                holder = self.component.bottomRowsHolder
            elemCmp = getattr(holder, 'elem_' + str(selElem[1]) + '_' + str(selElem[0]), None)
            if elemCmp:
                elemCmp.script.deselect()

        self.selectedElems = []
        return

    def selectRow(self, rowIndex, doSelect = True):
        rowObj = self._getRowByIndex(rowIndex)
        holder = None
        if rowObj.tablePart == 'TOP':
            holder = self.component.topRowsHolder
        elif rowObj.tablePart == 'MIDDLE':
            holder = self.component.midRowsHolder
        elif rowObj.tablePart == 'BOTTOM':
            holder = self.component.bottomRowsHolder
        for elem in rowObj.elements:
            elemCmp = getattr(holder, 'elem_' + str(rowIndex) + '_' + str(elem))
            if doSelect:
                elemCmp.script.select()
                data = (elem, rowIndex)
                self.selectedElems.append(data)
            else:
                elemCmp.script.deselect()
                data = (elem, rowIndex)
                if contains(self.selectedElems, data):
                    self.selectedElems.remove(data)

        return

    def onElementEvent(self, col, row, event, data):
        return None

    def elementEvent(self, col, row, event, data):
        self.onElementEvent(col, row, event, data)
        if event == 'LEFTMOUSE':
            rowObj = self._getRowByIndex(row)
            elemProps = rowObj.elements[col]['props']
            if 'EDIT' not in elemProps.rights:
                return
            if elemProps.dataType == ITEMTYPE_TEXT:
                if not self.editing:
                    self.showTyper(row, col, True)
                else:
                    self.showTyper(None, None, False)
                    self.showTyper(row, col, True)
        return

    def onEditEvent(self, col, row, event, data):
        return None

    def editEvent(self, col, row, event, data):
        self.onEditEvent(col, row, event, data)

    def clearAllChildren(self, component):
        for name, child in component.children:
            if isinstance(child.script, soTableElem):
                child.script.delElem()
            if len(child.children) > 0:
                self.clearAllChildren(child)
                component.delChild(child)
                child.script = None
            else:
                component.delChild(child)
                child.script = None

        return

    @PyGUIEvent('vScroll', 'scrollUp')
    def scrolledUP(self):
        self.scrollTableV(False, 1)
        print 'scrolledUP'

    @PyGUIEvent('vScroll', 'scrollDown')
    def scrolledDOWN(self):
        self.scrollTableV(True, 1)
        print 'scrolledDOWN'

    @PyGUIEvent('hScroll', 'scrollLeft')
    def scrolledLEFT(self):
        self.scrollTableH(False, 1)

    @PyGUIEvent('hScroll', 'scrollRight')
    def scrolledRIGHT(self):
        self.scrollTableH(True, 1)

    @PyGUIEvent('vScroll', 'scrollMoved')
    def vScrollMoved(self, newVal):
        self.cursor[1] = newVal
        self.dirtyMid = True
        self.renderTable()
        self.component.vScroll.script.setValue(newVal)

    @PyGUIEvent('hScroll', 'scrollMoved')
    def hScrollMoved(self, newVal):
        self.cursor[0] = newVal
        self.dirtyMid = True
        self.dirtyTop = True
        self.dirtyBottom = True
        self.renderTable()
        self.component.hScroll.script.setValue(newVal)

    @PyGUIEvent('inputHolder.edit', 'eventLostFocus')
    def typeEnd(self):
        self.showTyper(None, None, False)
        return

    @PyGUIEvent('inputHolder.edit', 'eventReturn')
    def typeComplete(self):
        data = self.component.inputHolder.edit.script.getValue()
        self.editEvent(self.editedCol, self.editedRow, 'TEXTINPUT', data)