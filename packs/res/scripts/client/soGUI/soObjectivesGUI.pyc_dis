# Embedded file name: scripts/client/soGUI/soObjectivesGUI.py
from Localization import lc
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import BWPersonality
from Avatar import PlayerAvatar
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.BWCoroutine import *
from math import ceil, floor

class soObjectivesGUI(PyGUIBase):
    factoryString = 'soGUI.soObjectivesGUI'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupCaptureTracker()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.5)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'

    def setupCaptureTracker(self):
        sW, sH = BigWorld.screenSize()
        cmp = GUI.Window('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 258
        cmp.height = 25
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = 'soGUI/maps/Misc/baseCaptureEmpty.tga'
        cmp.position = (sW / 2.0, 150, 1.0)
        self.component.addChild(cmp, 'captureTrackerBack')
        cmp = GUI.Window('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 258
        cmp.height = 25
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = 'soGUI/maps/Misc/baseCaptureFull.tga'
        cmp.position = (sW / 2.0, 150, 0.9)
        self.component.addChild(cmp, 'captureTrackerFront')
        shader = GUI.ClipShader()
        shader.speed = 0.2
        shader.mode = 'RIGHT'
        shader.value = 0.0
        self.component.captureTrackerFront.addShader(shader, 'clipper')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.position = (0.0, 0.0, 0.0)
        self.component.captureTrackerFront.addChild(cmp, 'percentLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.position = (sW / 2.0, 150, 0.5)
        cmp.text = lc('soObjectivesGUI.soGUI.STRING_97_13')
        self.component.addChild(cmp, 'baseCaptureLabel')

    def show(self):
        if self.component.parent is None:
            if isinstance(BigWorld.player(), PlayerAvatar):
                BigWorld.player().playerGUI.addChild(self.component, 'objectiveGUI')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False

    def setCaptureProgress(self, n):
        self.component.captureTrackerFront.clipper.value = n

    def update(self):
        if BWPersonality.GUICore.objectiveDataSection[0]:
            self.setCaptureProgress(BWPersonality.GUICore.objectiveDataSection[1])
        else:
            self.hide()


class soObjectiveFlag(PyGUIBase):
    factoryString = 'soGUI.soObjectiveFlag'

    def __init__(self, component, id = 0):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.flagID = id
        self.ownerSide = 0
        self.attackingSide = 0
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.width = 18
        cmp.height = 30

    def setupContent(self):
        cmp = GUI.Simple('soGUI/maps/Controls/pvp_objectives/flag.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 20
        cmp.position = (0.0, 1.0, 0.5)
        self.component.addChild(cmp, 'flag')
        cmp = GUI.Simple('soGUI/maps/Controls/pvp_objectives/flagGlow.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 20
        cmp.visible = False
        cmp.position = (0.0, 1.0, 0.5)
        self.component.addChild(cmp, 'glow')
        cmp = GUI.Simple('soGUI/maps/Controls/pvp_objectives/smallPGBack.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 7
        cmp.position = (0.0, -1.0, 0.5)
        self.component.addChild(cmp, 'pgBack')
        cmp = GUI.Simple('soGUI/maps/Controls/pvp_objectives/smallPGFront.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 7
        cmp.position = (0.0, -1.0, 0.4)
        self.component.addChild(cmp, 'pgFront')
        shader = GUI.ClipShader()
        shader.speed = 0.5
        shader.mode = 'RIGHT'
        shader.value = 1.0
        self.component.pgFront.addShader(shader, 'clipper')

    def setOwner(self, owner):
        self.ownerSide = owner
        self.component.flag.colour = soObjectivesGUI2.COLORMAP[owner]

    def setAttacker(self, attacker):
        self.attackingSide = attacker
        if attacker is None:
            self.glow(False)
        if self.ownerSide == attacker:
            self.glow(False)
        else:
            self.component.glow.colour = soObjectivesGUI2.COLORMAP[attacker]
            self.glow(True)
        return

    def setProgress(self, n):
        self.component.pgFront.clipper.value = n

    def glow(self, doGlow = True):
        self.component.glow.visible = doGlow

    def getID(self):
        return self.flagID


class soObjectivesGUI2(PyGUIBase):
    factoryString = 'soGUI.soObjectivesGUI2'
    MODE_BASECONQUER = 0
    TIMERMODE_READY = 0
    TIMERMODE_BATTLE = 1
    COLORMAP = {0: (255, 55, 55, 255),
     1: (55, 55, 255, 255),
     2: (55, 255, 55, 255)}

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.flags = []
        self.timeleft = 0
        self.timerRed = False
        self.flashTimer = False
        self.timerMode = self.TIMERMODE_READY
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 1.5)

    def setupContent(self):
        sW, sH = BigWorld.screenSize()
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.width = 217
        cmp.height = 120
        cmp.position = (sW - 10, sH / 2.0, 0.9)
        self.component.addChild(cmp, 'flagFrame')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp = GUI.Frame2('soGUI/maps/Controls/pvp_objectives/frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.flagFrame.addChild(cmp, 'background')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('soObjectivesGUI.soGUI.STRING_320_13')
        cmp.colourFormatting = True
        cmp.multiline = False
        cmp.position = (20, 20, 0.5)
        self.component.flagFrame.addChild(cmp, 'capturedPoints')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('soObjectivesGUI.soGUI.STRING_336_13')
        cmp.colourFormatting = True
        cmp.multiline = False
        cmp.position = (20, 84, 0.5)
        self.component.flagFrame.addChild(cmp, 'timer')
        cmp = GUI.Window('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 200
        cmp.height = 35
        cmp.visible = False
        cmp.position = (sW / 2.0, 100, 0.9)
        self.component.addChild(cmp, 'currentCptFrame')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('soObjectivesGUI.soGUI.STRING_368_13')
        cmp.colourFormatting = True
        cmp.multiline = False
        cmp.position = (100, 0, 0.5)
        self.component.currentCptFrame.addChild(cmp, 'captureLabel')
        cmp = GUI.Simple('soGUI/maps/Controls/pvp_objectives/currentCapturePGBack.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 200
        cmp.height = 10
        cmp.position = (100, 35, 0.8)
        self.component.currentCptFrame.addChild(cmp, 'pgBack')
        cmp = GUI.Simple('soGUI/maps/Controls/pvp_objectives/currentCapturePGFront.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 200
        cmp.height = 10
        cmp.position = (100, 35, 0.7)
        self.component.currentCptFrame.addChild(cmp, 'pgFront')
        shader = GUI.ClipShader()
        shader.speed = 0.05
        shader.mode = 'RIGHT'
        shader.value = 0.0
        self.component.currentCptFrame.pgFront.addShader(shader, 'clipper')

    def updateFlags(self):
        if not BWPersonality.GUICore.objectiveDataSection.has_key('flags'):
            return
        flags = BWPersonality.GUICore.objectiveDataSection['flags']
        flagIDs = []
        flagObjIDs = []
        for flag in flags:
            flagIDs.append(flag[0])

        deletedFlags = filter(lambda flag: flag.getID() not in flagIDs, self.flags)
        self.flags = filter(lambda flag: flag.getID() in flagIDs, self.flags)
        for flag in self.flags:
            flagObjIDs.append(flag.getID())

        for flag in deletedFlags:
            self.component.flagFrame.delChild(flag.component)

        for i, flag in enumerate(flags):
            if flag[0] in flagObjIDs:
                if hasattr(self.component.flagFrame, 'flag' + str(flag[0])):
                    cmp = self.component.flagFrame.__getattribute__('flag' + str(flag[0]))
                    cmp.script.setOwner(flag[1])
                    cmp.script.setProgress(flag[2])
                    cmp.script.setAttacker(flag[3])
                    cmp.position = (19 + i * 20, 45, 0.3)
                continue
            _flag = soObjectiveFlag(GUI.Window(), flag[0])
            cmp = _flag.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.position = (19 + i * 20, 45, 0.3)
            self.component.flagFrame.addChild(cmp, 'flag' + str(flag[0]))
            _flag.setOwner(flag[1])
            _flag.setProgress(flag[2])
            _flag.setAttacker(flag[3])
            _flag.onBound()
            self.flags.append(_flag)

    def updateCurrentProgress(self):
        if not BWPersonality.GUICore.objectiveDataSection.has_key('currentProgress'):
            return
        progress = BWPersonality.GUICore.objectiveDataSection['currentProgress']
        if progress[0] < 0:
            self.component.currentCptFrame.visible = False
            return
        self.component.currentCptFrame.visible = True
        s = u''
        if progress[1] == 'point':
            s = lc('soObjectivesGUI.soGUI.STRING_461_7')
        elif progress[1] == 'flag':
            s = lc('soObjectivesGUI.soGUI.STRING_463_7')
        self.component.currentCptFrame.captureLabel.text = lc('soObjectivesGUI.soGUI.STRING_465_53') + s + u':'
        self.component.currentCptFrame.pgFront.clipper.value = progress[0]

    def timeToString(self, secs):
        hours = floor(secs / 3600.0)
        minutes = floor((secs - hours * 3600.0) / 60.0)
        seconds = secs - (hours * 3600.0 + minutes * 60.0)
        outH = str(int(hours)) if hours > 9 else u'0' + str(int(hours))
        outM = str(int(minutes)) if minutes > 9 else u'0' + str(int(minutes))
        outS = str(int(seconds)) if seconds > 9 else u'0' + str(int(seconds))
        return u'' + outH + u':' + outM + u':' + outS

    def updateFlagInfo(self):
        if BWPersonality.GUICore.objectiveDataSection.has_key('total_points'):
            self.component.flagFrame.capturedPoints.text = lc('soObjectivesGUI.soGUI.STRING_480_50') + BWPersonality.GUICore.objectiveDataSection['total_points']
        if BWPersonality.GUICore.objectiveDataSection.has_key('time'):
            self.timeleft = BWPersonality.GUICore.objectiveDataSection['time'][0]
            if BWPersonality.GUICore.objectiveDataSection['time'][1] == 'ready':
                self.timerMode = self.TIMERMODE_READY
            elif BWPersonality.GUICore.objectiveDataSection['time'][1] == 'battle':
                self.timerMode = self.TIMERMODE_BATTLE

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'objectiveGUI')
        if self.component.visible:
            return
        else:
            self.component.visible = True
            self.timeChecker().run()
            self.component.flagFrame.timer.colour = (255, 255, 255, 255)
            self.timerRed = False
            return

    def hide(self):
        self.component.visible = False

    def update(self):
        data = BWPersonality.GUICore.objectiveDataSection
        if not data:
            return
        self.updateFlags()
        self.updateFlagInfo()
        self.updateCurrentProgress()

    @BWMemberCoroutine
    def timeCritical(self):
        self.flashTimer = True
        while self.timeleft < 121:
            yield BWWaitForPeriod(0.2)
            if not self.timerRed:
                self.component.flagFrame.timer.colour = (255, 75, 75, 255)
                self.timerRed = True
            else:
                self.component.flagFrame.timer.colour = (255, 255, 255, 255)
                self.timerRed = False

        self.flashTimer = False

    @BWMemberCoroutine
    def timeChecker(self):
        while self.component.visible:
            self.timeleft -= 1
            if self.timeleft < 0:
                self.timeleft = 0
            if self.timeleft < 121 and not self.flashTimer:
                self.timeCritical().run()
            timerText = u''
            if self.timerMode == self.TIMERMODE_BATTLE:
                timerText = lc('soObjectivesGUI.soGUI.STRING_539_16')
                self.component.flagFrame.timer.visible = True
            elif self.timerMode == self.TIMERMODE_READY:
                self.component.flagFrame.timer.visible = False
            self.component.flagFrame.timer.text = timerText + self.timeToString(self.timeleft)
            yield BWWaitForPeriod(1.0)