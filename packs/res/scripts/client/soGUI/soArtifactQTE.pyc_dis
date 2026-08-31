# Embedded file name: scripts/client/soGUI/soArtifactQTE.py
import BigWorld
import GUI
import BWPersonality
import Helpers.PyGUI as PyGUI
import soGUI
from Keys import *
from copy import deepcopy
import Math
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.BWCoroutine import *
from functools import partial

class soArtifactPoint(PyGUIBase):
    factoryString = 'soGUI.soArtifactPoint'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.artifactID = -1
        self.onClick = lambda : None
        self.range = 1.0
        self.setupRoot()
        self.setupVisual()
        self.setupAlphaShader()
        self.setupSelector()
        self.blinkLoop().run()

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.width = 25
        cmp.height = 25
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.mouseButtonFocus = True

    def setupVisual(self):
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 23
        cmp.height = 23
        cmp.colour = (255, 255, 255, 255)
        cmp.position = (0.0, 0.0, 0.1)
        cmp.materialFX = 'BLEND'
        cmp.textureName = 'soGUI/maps/ArtifactQTE/artifactPoint.tga'
        self.component.addChild(cmp, 'visual')

    def setupSelector(self):
        cmp = GUI.Simple('soGUI/maps/ArtifactQTE/selector.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 25
        cmp.height = 25
        cmp.colour = (255, 255, 255, 255)
        cmp.position = (0.0, 0.0, 0.0)
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        self.component.addChild(cmp, 'selector')

    def setupAlphaShader(self):
        shader = GUI.AlphaShader()
        shader.mode = 'ALL'
        shader.speed = 3
        shader.alpha = 1.0
        self.component.visual.addShader(shader, 'fader')

    def setID(self, id):
        self.artifactID = id

    def getID(self):
        return self.artifactID

    def handleMouseButtonEvent(self, comp, event):
        if not event.isMouseButton():
            return False
        down = event.isKeyDown()
        key = event.key
        position = event.cursorPosition
        if key == KEY_LEFTMOUSE:
            if down:
                self.onClick()
                return True
        return False

    def select(self):
        self.component.selector.visible = True

    def deselect(self):
        self.component.selector.visible = False

    @BWMemberCoroutine
    def blinkLoop(self):
        yield BWWaitForPeriod(1.8)
        while self.component.visible:
            self.component.visual.fader.alpha = 0
            yield BWWaitForPeriod(2.5)
            self.component.visual.fader.alpha = 1.0
            self.component.visual.fader.reset()


class soArtifactQTE(PyGUIBase):
    factoryString = 'soGUI.soArtifactQTE'
    EVENT_SELECT = 0
    EVENT_TAKE = 1
    EVENT_SCANNED = 2
    EVENT_CLOSED = 3
    STATUS_IDLE = 0
    STATUS_PLAY = 1
    STATUS_FAIL = 2
    KEYMAP = {KEY_UPARROW: 'soGUI/maps/ArtifactQTE/key_up.tga',
     KEY_DOWNARROW: 'soGUI/maps/ArtifactQTE/key_down.tga',
     KEY_LEFTARROW: 'soGUI/maps/ArtifactQTE/key_left.tga',
     KEY_RIGHTARROW: 'soGUI/maps/ArtifactQTE/key_right.tga',
     KEY_1: 'soGUI/maps/ArtifactQTE/key_1.tga',
     KEY_2: 'soGUI/maps/ArtifactQTE/key_2.tga',
     KEY_3: 'soGUI/maps/ArtifactQTE/key_3.tga',
     KEY_4: 'soGUI/maps/ArtifactQTE/key_4.tga',
     KEY_5: 'soGUI/maps/ArtifactQTE/key_5.tga',
     KEY_6: 'soGUI/maps/ArtifactQTE/key_6.tga',
     KEY_7: 'soGUI/maps/ArtifactQTE/key_7.tga',
     KEY_8: 'soGUI/maps/ArtifactQTE/key_8.tga',
     KEY_9: 'soGUI/maps/ArtifactQTE/key_9.tga',
     KEY_0: 'soGUI/maps/ArtifactQTE/key_0.tga'}
    STATUSMAP = {STATUS_IDLE: '',
     STATUS_PLAY: '',
     STATUS_FAIL: 'soGUI/maps/ArtifactQTE/fail.tga'}

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.sliderMP = None
        self.spotlineMP = None
        self.sliderData = None
        self.QTEdata = None
        self.keyData = None
        self.selectorData = None
        self.status = soArtifactQTE.STATUS_IDLE
        self.points = []
        self.setupRoot()
        self.setupContent()
        self.spotlineLoop().run()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.position = (-1.0, 0.0, 0.0)
        cmp.width = 388
        cmp.height = 700
        cmp.textureName = ''
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'

    def setupContent(self):
        cmp = GUI.Simple('soGUI/maps/ArtifactQTE/back.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 388
        cmp.height = 700
        cmp.position = (0, 0, 1.0)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'background')
        cmp = GUI.Window('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 217
        cmp.height = 217
        cmp.position = (87, 120, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'radarHolder')
        cmp = GUI.Simple('soGUI/maps/ArtifactQTE/radarNet.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 272
        cmp.height = 304
        cmp.position = (58, 62, 0.9)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'radarNet')
        cmp = GUI.Simple('soGUI/maps/ArtifactQTE/infos.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 249
        cmp.height = 187
        cmp.position = (68, 366, 0.9)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'infoBar')
        cmp = GUI.Simple('soGUI/maps/ArtifactQTE/spotLine.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.width = 217
        cmp.height = 124
        cmp.position = (-1.0, 1.0, 0.4)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.radarHolder.addChild(cmp, 'spotLine')
        self.spotlineMP = Math.Matrix()
        self.spotlineMP.translation = (0.0, 0.0, 0.0)
        shader = GUI.MatrixShader()
        shader.eta = 0
        shader.blend = True
        shader.target = self.spotlineMP
        self.component.radarHolder.spotLine.addShader(shader, 'mover')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 227
        cmp.height = 23
        cmp.position = (80, 377, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'sliderHolder')
        cmp = GUI.Simple('soGUI/maps/ArtifactQTE/slider.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 14
        cmp.height = 23
        cmp.position = (-1.0, 1.0, 0.8)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.sliderHolder.addChild(cmp, 'timeSlider')
        for i in xrange(5):
            cmp = GUI.Simple('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 38
            cmp.height = 38
            cmp.position = (80 + i * 48, 392, 0.4)
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            self.component.addChild(cmp, 'key' + str(i))

        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 71
        cmp.height = 28
        cmp.position = (107, 444, 0.8)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'statusMarker')

    def renderContents(self, slider = True, points = True, keyBinds = True, select = True, status = True):
        if slider:
            cmp = self.component.sliderHolder.timeSlider
            hPos = self.sliderData * 2.0 - 1.0
            cmp.position = (hPos, 1.0, 0.8)
        if points:
            for point in self.points:
                self.component.radarHolder.delChild(point)

            self.points = []
            for point in self.QTEdata:
                pointObj = soArtifactPoint(GUI.Window())
                cmp = pointObj.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
                cmp.position = (self.QTEdata[point][0], self.QTEdata[point][1], 0.0)
                self.component.radarHolder.addChild(cmp, 'point' + str(point))
                pointObj.onBound()
                pointObj.setID(point)
                pointObj.onClick = partial(self.processPoint, point)
                self.points.append(cmp)

        if keyBinds:
            if len(self.keyData) < 5:
                for i in xrange(5):
                    cmp = self.component.__getattribute__('key' + str(i))
                    cmp.visible = False

            i = 0
            for key in self.keyData:
                cmp = self.component.__getattribute__('key' + str(i))
                cmp.textureName = self.KEYMAP[key[0]]
                cmp.visible = key[1]
                i += 1

        if select:
            if hasattr(self.component.radarHolder, 'point' + str(self.selectorData)):
                cmp = self.component.radarHolder.__getattribute__('point' + str(self.selectorData))
                cmp.script.select()
        if status:
            self.component.statusMarker.textureName = self.STATUSMAP[self.status]

    def update(self):
        slider, points, keyBinds, select, status = (False,
         False,
         False,
         False,
         False)
        if self.sliderData != BWPersonality.GUICore.artifactQTEDataSection['slider']:
            self.sliderData = BWPersonality.GUICore.artifactQTEDataSection['slider']
            slider = True
        if self.QTEdata != BWPersonality.GUICore.artifactQTEDataSection['QTEdata']:
            self.QTEdata = deepcopy(BWPersonality.GUICore.artifactQTEDataSection['QTEdata'])
            points = True
        if self.keyData != BWPersonality.GUICore.artifactQTEDataSection['keyData']:
            self.keyData = deepcopy(BWPersonality.GUICore.artifactQTEDataSection['keyData'])
            keyBinds = True
        if self.selectorData != BWPersonality.GUICore.artifactQTEDataSection['selector']:
            self.selectorData = BWPersonality.GUICore.artifactQTEDataSection['selector']
            select = True
        if self.status != BWPersonality.GUICore.artifactQTEDataSection['QTEStatus']:
            self.status = BWPersonality.GUICore.artifactQTEDataSection['QTEStatus']
            status = True
        self.renderContents(slider, points, keyBinds, select, status)

    def processPoint(self, point):
        if self.status is not self.STATUS_PLAY:
            BWPersonality.GUICore.artifactQTEEvent(self.EVENT_SELECT, point)

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'artifactQTE')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.artifactQTEEvent(self.EVENT_CLOSED, None)
        return

    def scanComplete(self):
        BWPersonality.GUICore.artifactQTEEvent(self.EVENT_SCANNED, None)
        return

    @BWMemberCoroutine
    def spotlineLoop(self):
        pixStartPoint = self.component.radarHolder.localToScreen((0, 0))
        startPoint = pixStartPoint[1]
        pixEndPoint = self.component.radarHolder.localToScreen((0, self.component.radarHolder.height + self.component.radarHolder.spotLine.height))
        offset = startPoint - pixEndPoint[1]
        while True:
            self.component.radarHolder.spotLine.mover.eta = 1.2
            self.spotlineMP.translation = (0, -offset, 0)
            yield BWWaitForPeriod(2.5)
            self.spotlineMP.translation = (0, 0, 0)
            self.component.radarHolder.spotLine.mover.reset()
            self.scanComplete()