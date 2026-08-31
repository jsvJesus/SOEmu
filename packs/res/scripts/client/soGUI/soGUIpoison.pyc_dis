# Embedded file name: scripts/client/soGUI/soGUIpoison.py
import BigWorld
import BWPersonality
import GUI
import random
import soGUI
import Stats
from Helpers.PyGUI import PyGUIBase
from Math import Matrix

class soGUIpoison(PyGUIBase):
    factoryString = 'soGUI.soGUIpoison'
    SCREEN_NAMES = ['frame_poison']
    BLINK_TIME = 0.1
    ALPHA_FRAME_SPEED = 5
    ALPHA_FRAME_SPEED_BACK = 7
    SUNC_TIME = 5.0
    FULLTICK = 30

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        self.back = False
        self._full_tick = 0
        component.script = self
        self.setupRoot()
        self.setupContent()
        self.isVisible = False
        self._frame_revert = False
        self.visible_components = []
        BigWorld.callback(self.BLINK_TIME, self.updateBlood)
        self.sound_poison = None
        self.isSlow = True
        self.timer_speed_heart = None
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = horizontalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 100)
        cmp.materialFX = 'BLEND'
        sW, sH = BigWorld.screenSize()
        cmp.height = sH
        cmp.width = sW
        cmp.position = (0.0, 0.0, 0.5)
        cmp.visible = False

    def setupContent(self):
        path = 'soGUI/maps/poison/%s.tga'
        for name in self.SCREEN_NAMES:
            self.createCmp(name, path % name)

    def createCmp(self, name, path):
        cmp = GUI.Simple(path)
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = horizontalAnchor = 'TOP'
        cmp.materialFX = 'BLEND'
        cmp.colour = (84, 156, 64, 255)
        sW, sH = BigWorld.screenSize()
        cmp.height = sH
        cmp.width = sW
        cmp.position = (0.0, 0.0, 0.5)
        cmp.visible = False
        cmp.script = self
        self.component.addChild(cmp, name)

    def show(self):
        if self.isVisible:
            return
        else:
            self.isVisible = True
            self.loadSound()
            if self.component.parent is None:
                BWPersonality.GUICore.worldLayer.addChild(self.component, 'soGUIpoison')
            self.component.visible = True
            self.component.frame_poison.visible = True
            self.visible_components = []
            self.updateSpeedHeart(True)
            self.sound_poison.play()
            return

    def loadSound(self):
        if not self.sound_poison:
            self.sound_poison = BigWorld.getSound('players/heartbeat/slow')

    def updateBlood(self):
        BigWorld.callback(self.BLINK_TIME, self.updateBlood)
        if not self.isVisible:
            return
        if self.back:
            self.component.frame_poison.colour.alpha -= self.ALPHA_FRAME_SPEED
            if self.component.frame_poison.colour.alpha <= 100:
                self.back = not self.back
        else:
            self.component.frame_poison.colour.alpha += self.ALPHA_FRAME_SPEED_BACK
            if self.component.frame_poison.colour.alpha >= 255:
                self._full_tick += 1
                if self._full_tick >= self.FULLTICK:
                    self.back = not self.back
                    self._full_tick = 0

    def updateSpeedHeart(self, force = False):
        if not self.isVisible:
            return
        self.timer_speed_heart = BigWorld.callback(self.SUNC_TIME, self.updateSpeedHeart)
        pl = BigWorld.player()
        if pl.__class__.__name__ != 'PlayerAvatar':
            self.hide()
            return
        try:
            BigWorld.camera().shake(1, (0.01, 0.0003, 3e-05))
        except Exception as e:
            print 'bleed shake error', e

    def hide(self):
        if self.timer_speed_heart:
            BigWorld.cancelCallback(self.timer_speed_heart)
        self.isVisible = False
        self.component.visible = False
        for name in self.SCREEN_NAMES:
            cmp = getattr(self.component, name)
            cmp.visible = False

        self.visible_components = []
        if self.sound_poison:
            self.sound_poison.stop()

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.height = sH
        self.component.width = sW
        for name in self.SCREEN_NAMES:
            cmp = getattr(self.component, name)
            cmp.height = sH
            cmp.width = sW

    def fini(self):
        pass