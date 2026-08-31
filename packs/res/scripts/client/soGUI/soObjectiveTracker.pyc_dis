# Embedded file name: scripts/client/soGUI/soObjectiveTracker.py
import BigWorld
import GUI
import BWPersonality
from Helpers.PyGUI import PyGUIBase
from gui_const import GUI_ID, OBJECTIVE_TRACKER
from soGUI import soButton
from time import time
from soDraggableComponent import soDraggableComponent

class soObjective(PyGUIBase):
    factoryString = 'soGUI.soObjective'

    def __init__(self, component, objectiveData):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.objectiveData = objectiveData
        self.setupRoot()
        self.applyObjectiveData()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 0
        cmp.height = 0
        cmp.position.z = 0.5

    def cleanUp(self):
        self.component.height = 0
        self.component.width = 0
        self.clearAllChildren(self.component)

    def fini(self):
        self.cleanUp()
        self.component = None
        return

    def applyObjectiveData(self):
        self.cleanUp()
        if self.objectiveData is None:
            return
        else:
            curHeight = 0
            maxWidth = 0
            cmps = []
            if self.objectiveData.has_key('caption'):
                cmp = GUI.Text('')
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'RIGHT'
                cmp.verticalAnchor = 'TOP'
                cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
                cmp.colour = (175, 166, 112, 255)
                cmp.materialFX = 'BLEND'
                cmp.text = self.objectiveData['caption']
                w, h = cmp.stringDimensions(cmp.text)
                cmp.position = (0, curHeight, 0.5)
                self.component.addChild(cmp, 'caption')
                curHeight += h
                if w > maxWidth:
                    maxWidth = w
                cmps.append(cmp)
            if self.objectiveData.has_key('track_data'):
                for idx, objective in enumerate(self.objectiveData['track_data']):
                    if objective['data_type'] == OBJECTIVE_TRACKER.DATATYPE_PLAINTEXT:
                        cmp = GUI.Text('')
                        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                        cmp.horizontalAnchor = 'RIGHT'
                        cmp.verticalAnchor = 'TOP'
                        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
                        cmp.colour = (175, 166, 112, 255)
                        cmp.materialFX = 'BLEND'
                        cmp.text = objective['data']
                        w, h = cmp.stringDimensions(cmp.text)
                        cmp.position = (0, curHeight, 0.5)
                        self.component.addChild(cmp, 'tracker_objective_{0}'.format(idx))
                        curHeight += h
                        if w > maxWidth:
                            maxWidth = w
                        cmps.append(cmp)

            self.component.width = maxWidth
            self.component.height = curHeight
            for cmp in cmps:
                cmp.position.x = maxWidth

            return

    def dims(self):
        return [self.component.width, self.component.height]

    def setObjectiveData(self, data):
        self.objectiveData = data
        self.applyObjectiveData()


class soObjectiveTrackerGUI(PyGUIBase, soDraggableComponent):
    factoryString = 'soGUI.soObjectiveTrackerGUI'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        soDraggableComponent.__init__(self, component, centerDProxy=False, autoCleanup=True)
        component.script = self
        self.interfaceID = GUI_ID.GUI_ID_OBJECTIVETRACKER
        self.objectives = {}
        self.HP_objectives = []
        self.NP_objectives = []
        self.LP_objectives = []
        self.height = 22
        self.width = 33
        self.objectives_visible = True
        self.setupRoot()
        self.setupContent()
        self._alignToMiniMap()
        self.dragProxy = self.component.dragProxy
        self.proxyHolder = self.component
        self.proxyName = 'dragProxy'
        self._onDragStart = self.onDragStart
        self._onDragStop = self.onDragStop

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 33
        cmp.height = 22
        cmp.crossFocus = True
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/trackerGUI/trackerFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 0
        cmp.height = 0
        cmp.colour = (255, 255, 255, 255)
        cmp.visible = False
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 22, 0.9)
        self.component.addChild(cmp, 'dFrame')
        cmp = GUI.Frame2('soGUI/maps/Misc/resizeBox.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 0
        cmp.height = 0
        cmp.visible = False
        cmp.position = (0, 0, 0.05)
        self.component.addChild(cmp, 'dragProxy')
        cmp = GUI.Window('soGUI/maps/Controls/trackerGUI/trackerFrame_controls.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 30
        cmp.height = 22
        cmp.position = (self.component.width - 3, 0, 0.5)
        self.component.addChild(cmp, 'controlsFrame')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/minusBtn_tracker.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 16
        cmp.height = 16
        cmp.position = (11, 3, 0.2)
        self.component.controlsFrame.addChild(cmp, 'minMaxBtn')
        btn.onClick = self.onMinMaxBtn
        btn.onBound()
        btn._updateVisualState()
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 8
        cmp.height = 18
        cmp.position = (2, 2, 0.1)
        cmp.script = self
        cmp.dragFocus = True
        cmp.moveFocus = True
        self.component.controlsFrame.addChild(cmp, 'dragAnchor')

    def addObjective(self, id, priority, objective_data):
        if self.objectives.has_key(id):
            return False
        self.objectives[id] = objective_data
        if priority == OBJECTIVE_TRACKER.PRIORITY_LOW:
            self.LP_objectives.append(id)
        if priority == OBJECTIVE_TRACKER.PRIORITY_NORMAL:
            self.NP_objectives.append(id)
        if priority == OBJECTIVE_TRACKER.PRIORITY_HIGHEST:
            self.HP_objectives.append(id)
        self.updateObjectives()
        self._repositionObjectives()
        return True

    def setObjective(self, id, objective_data):
        if self.objectives.has_key(id):
            self.objectives[id] = objective_data
            self.updateObjectives()
            self._repositionObjectives()
            return True
        else:
            return False

    def delObjective(self, id):
        if id is None:
            self.clearObjectives()
            return True
        elif self.objectives.has_key(id):
            if id in self.LP_objectives:
                self.LP_objectives.remove(id)
            if id in self.NP_objectives:
                self.NP_objectives.remove(id)
            if id in self.HP_objectives:
                self.HP_objectives.remove(id)
            cmp = getattr(self.component, 'objective_{0}'.format(id), None)
            if cmp:
                cmp.script.fini()
                self.component.delChild(cmp)
            del self.objectives[id]
            self._repositionObjectives()
            return True
        else:
            return False
            return

    def clearObjectives(self):
        ids = self.objectives.keys()
        for id in ids:
            self.delObjective(id)

    def _repositionObjectives(self):
        curHeight = 37
        maxWidth = 0
        cmps = []
        for oid in self.HP_objectives:
            cmp = getattr(self.component, 'objective_{0}'.format(oid), None)
            if cmp:
                w, h = cmp.script.dims()
                cmp.position.y = curHeight
                if w > maxWidth:
                    maxWidth = w
                curHeight += h + 10
                cmps.append(cmp)
            else:
                print 'WARNING: soObjectiveTracker::_repositionObjectives didnt properly build objective elements'

        for oid in self.NP_objectives:
            cmp = getattr(self.component, 'objective_{0}'.format(oid), None)
            if cmp:
                w, h = cmp.script.dims()
                cmp.position.y = curHeight
                if w > maxWidth:
                    maxWidth = w
                curHeight += h + 10
                cmps.append(cmp)
            else:
                print 'WARNING: soObjectiveTracker::_repositionObjectives didnt properly build objective elements'

        for oid in self.LP_objectives:
            cmp = getattr(self.component, 'objective_{0}'.format(oid), None)
            if cmp:
                w, h = cmp.script.dims()
                cmp.position.y = curHeight
                if w > maxWidth:
                    maxWidth = w
                curHeight += h + 10
                cmps.append(cmp)
            else:
                print 'WARNING: soObjectiveTracker::_repositionObjectives didnt properly build objective elements'

        self.width = maxWidth + 30
        self.height = curHeight
        self._updateObjectivesVisibility()
        return

    def updateObjectives(self):
        for oid in self.objectives:
            cmp = getattr(self.component, 'objective_{0}'.format(oid), None)
            if cmp:
                cmp.script.setObjectiveData(self.objectives[oid])
            else:
                objective = soObjective(GUI.Window(), self.objectives[oid])
                cmp = objective.component
                self.component.addChild(cmp, 'objective_{0}'.format(oid))

        return

    def showObjectives(self, doShow = True):
        self.objectives_visible = doShow
        if doShow:
            self.component.controlsFrame.minMaxBtn.script.initVSC('soGUI/visual_styles/minusBtn_tracker.xml')
        else:
            self.component.controlsFrame.minMaxBtn.script.initVSC('soGUI/visual_styles/plusBtn_tracker.xml')
        self._updateObjectivesVisibility()

    def _updateObjectivesVisibility(self):
        if self.objectives_visible:
            self.component.height = self.height
            self.component.width = self.width
        else:
            self.component.height = 22
            self.component.width = 33
        self.component.controlsFrame.position.x = self.component.width - 3
        self.component.dFrame.width = self.width
        self.component.dFrame.height = self.height - 22
        self.component.dFrame.position.x = self.width
        for name, cmp in self.component.children:
            if 'objective_' in name:
                cmp.position.x = self.width - 15

    def mouseFocus(self, doFocus = True):
        if BWPersonality.gpd.cursorMode == BWPersonality.CURSOR_TYPE_DIRECTION:
            doFocus = False
        self.component.dFrame.visible = doFocus

    def _alignToMiniMap(self):
        cmp = getattr(BWPersonality.GUICore.worldLayer, 'minimap', None)
        if cmp:
            self.component.position.x = cmp.position.x
            self.component.position.y = cmp.position.y + cmp.height + 40
            self.component.position.z = 1.5
        return

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'trackerGUI')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False

    def onDragStart(self):
        self.dragProxy.width = self.component.width
        self.dragProxy.height = self.component.height
        self.dragProxy.visible = True
        return True

    def onDragStop(self):
        offset = self.component.screenToLocal((self.dragProxy.position.x, self.dragProxy.position.y))
        self.dragProxy.visible = False
        self.component.position.x += offset.x
        self.component.position.y += offset.y
        return True

    def doReposition(self):
        sw, sh = BigWorld.screenSize()
        if self.component.position.x > sw:
            self.component.position.x = sw
        if self.component.position.y + 22 > sh:
            self.component.position.y = sh - 22

    def handleDragStartEvent(self, cmp):
        soDraggableComponent.handleDragStartEvent(self, cmp)
        return True

    def handleDragStopEvent(self, cmp):
        soDraggableComponent.handleDragStopEvent(self, cmp)
        return True

    def handleMouseEvent(self, cmp, event):
        if not self.dragging:
            return False
        soDraggableComponent.handleMouseEvent(self, cmp, event)
        return True

    def handleMouseEnterEvent(self, component):
        self.mouseFocus(True)
        return True

    def handleMouseLeaveEvent(self, component):
        leaved = True
        pos = GUI.mcursor().position
        relPos = self.component.screenToLocal(pos)
        if relPos[0] > 0 and relPos[0] < self.component.width and relPos[1] > 0 and relPos[1] < self.component.height:
            leaved = False
        self.mouseFocus(not leaved)
        return True

    def onMinMaxBtn(self):
        self.showObjectives(not self.objectives_visible)

    def getObjectiveList(self):
        return self.HP_objectives + self.NP_objectives + self.LP_objectives