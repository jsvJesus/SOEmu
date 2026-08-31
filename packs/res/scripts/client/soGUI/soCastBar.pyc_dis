# Embedded file name: scripts/client/soGUI/soCastBar.py
from Localization import lc
import BigWorld
import GUI
import BWPersonality
import soGUI
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI import PyGUIBase
from Helpers.BWCoroutine import *

class soCastBar(PyGUIBase):
    factoryString = 'soGUI.soCastBar'
    EVENT_FINISH = 0
    EVENT_OVERRIDE = 1
    EVENT_INTERRUPT = 2
    EVENT_CANCEL = 3

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.currentID = None
        self.currentTimeTotal = 0
        self.castStartedAt = 0
        self.currentTicker = None
        self.hideInProcess = None
        self.setupRoot()
        self.setupContent()
        return

    def setupRoot(self):
        sw, sh = BigWorld.screenSize()
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 256
        cmp.height = 16
        cmp.visible = False
        cmp.position = (sw / 2.0, sh - 114, 0.5)

    def setupContent(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.5)
        cmp.textureName = 'soGUI/maps/Controls/castbar/castbar_empty.tga'
        self.component.addChild(cmp, 'PGBack')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.4)
        cmp.textureName = 'soGUI/maps/Controls/castbar/castbar_full.tga'
        self.component.addChild(cmp, 'PGFront')
        shader = GUI.ClipShader()
        shader.mode = 'RIGHT'
        shader.value = 1.0
        shader.speed = 0
        cmp.addShader(shader, 'clipper')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.3)
        cmp.textureName = 'soGUI/maps/Controls/castbar/castbar_int.tga'
        self.component.addChild(cmp, 'PGFail')
        shader = GUI.AlphaShader()
        shader.mode = 'ALL'
        shader.alpha = 0.0
        shader.speed = 1.0
        cmp.addShader(shader, 'fader')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (249, 233, 137, 255)
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.materialFX = 'BLEND'
        cmp.multiline = False
        cmp.colourFormatting = True
        cmp.position = (0.0, 0.0, 0.2)
        self.component.addChild(cmp, 'caption')

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'castBar')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False

    def runCast(self, duration, caption = u'', id = 0):
        if self.currentID is not None:
            self.overrideCast()
        self.show()
        self.currentTicker = self.progressTicker(duration)
        self.currentTicker.run()
        self.component.caption.text = caption
        self.currentID = id
        self.component.PGFront.clipper.value = 0.0
        self.component.PGFront.clipper.reset()
        self.component.PGFront.clipper.speed = duration
        self.component.PGFront.clipper.value = 1.0
        self.show()
        return

    def interruptCast(self, msg = lc('soCastBar.soGUI.STRING_135_31')):
        if self.currentID is None:
            if not self.component.visible:
                return
        self.component.caption.text = msg
        self._castInterrupted()
        self.component.PGFront.clipper.value = 0.0
        self.component.PGFront.clipper.reset()
        self.currentID = None
        self.castStartedAt = 0
        self.currentTimeTotal = 0
        self.hideInProcess = self.delayedHider()
        self.hideInProcess.run()
        return

    def overrideCast(self):
        self._castOverriden()
        self._reset()

    def cancelCast(self):
        self._reset()
        self.hide()
        self._castCanceled()

    def setCastTime(self, pos, caption = u''):
        if self.currentID is not None:
            self.overrideCast()
        self.component.PGFront.clipper.value = pos
        self.component.PGFront.clipper.reset()
        self.component.caption.text = caption
        self.show()
        return

    def getState(self):
        if self.currentID is not None:
            timeLeft = BigWorld.time() - self.castStartedAt
            return (self.currentID, timeLeft, self.currentTimeTotal)
        else:
            return

    def _castFinished(self):
        BWPersonality.GUICore.castBarEvent(self.EVENT_FINISH, self.currentID)

    def _castOverriden(self):
        BWPersonality.GUICore.castBarEvent(self.EVENT_OVERRIDE, self.currentID)

    def _castInterrupted(self):
        BWPersonality.GUICore.castBarEvent(self.EVENT_INTERRUPT, self.currentID)

    def _castCanceled(self):
        BWPersonality.GUICore.castBarEvent(self.EVENT_CANCEL, self.currentID)

    def _reset(self):
        if self.currentTicker is not None:
            self.currentTicker.stop()
        if self.hideInProcess is not None:
            self.hideInProcess.stop()
        self.currentID = None
        self.currentTimeTotal = 0
        self.castStartedAt = 0
        self.component.caption.text = u''
        self.component.PGFront.clipper.value = 0.0
        self.component.PGFront.clipper.reset()
        self.component.PGFail.fader.value = 0.0
        self.component.PGFail.fader.reset()
        return

    @BWMemberCoroutine
    def progressTicker(self, duration):
        self.currentTimeTotal = duration
        self.castStartedAt = BigWorld.time()
        yield BWWaitForPeriod(duration)
        self.hide()
        self._castFinished()
        self.currentID = None
        self.currentTimeTotal = 0
        self.castStartedAt = 0
        return

    @BWMemberCoroutine
    def delayedHider(self):
        self.component.PGFail.fader.alpha = 1.0
        self.component.PGFail.fader.reset()
        yield BWWaitForPeriod(0.5)
        self.component.PGFail.fader.alpha = 0.0
        yield BWWaitForPeriod(1.0)
        self.hide()