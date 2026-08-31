# Embedded file name: scripts/client/soGUI/soGUIBleed.py
import BigWorld
import BWPersonality
import GUI
import random
import soGUI
import Stats
from Helpers.PyGUI import PyGUIBase
from Math import Matrix
from Settings import Settings

class ClassName(object):
    """docstring for ClassName"""

    def __init__(self):
        pass

    def play(self):
        pass

    def stop(self):
        pass


class soBleedGUI(PyGUIBase):
    factoryString = 'soGUI.soBleedGUI'
    BLOOD_NAMES = ['frame']
    BLINK_TIME = 0.1
    ALPHA_SPEED = 10
    ALPHA_FRAME_SPEED = 35
    SPAWN_RAND = 0.09
    SLOW_TIME = 0.775
    FAST_TIME = 0.372
    SUNC_TIME = 1.0

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupContent()
        self.isVisible = False
        self._frame_revert = False
        self.visible_components = []
        BigWorld.callback(self.BLINK_TIME, self.updateBlood)
        self.sound_slow = None
        self.sound_fast = None
        self.isSlow = True
        self.timer_speed_heart = None
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = horizontalAnchor = 'TOP'
        cmp.colour = (100, 1, 1, 100)
        cmp.materialFX = 'BLEND'
        sW, sH = BigWorld.screenSize()
        cmp.height = sH
        cmp.width = sW
        cmp.position = (0.0, 0.0, 0.5)
        cmp.visible = False

    def setupContent(self):
        path = 'soGUI/maps/blood/%s.tga'
        for name in self.BLOOD_NAMES:
            self.createCmp(name, path % name)

    def createCmp(self, name, path):
        cmp = GUI.Simple(path)
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = horizontalAnchor = 'TOP'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        sW, sH = BigWorld.screenSize()
        cmp.height = sH
        cmp.width = sW
        cmp.position = (0.0, 0.0, 0.5)
        cmp.visible = False
        cmp.script = self
        self.component.addChild(cmp, name)

    def show(self):
        self.isVisible = True
        self.loadSound()
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'bleedGUI')
        self.component.visible = True
        self.component.frame.visible = True
        self.visible_components = []
        self.updateSpeedHeart(True)
        return

    def loadSound(self):
        if not self.sound_fast:
            self.sound_fast = BigWorld.getSound('players/heartbeat/fast')
        if not self.sound_slow:
            self.sound_slow = BigWorld.getSound('players/heartbeat/slow')

    def updateBlood(self):
        BigWorld.callback(self.BLINK_TIME, self.updateBlood)
        if not self.isVisible:
            return
        self.component.frame.colour.alpha -= self.ALPHA_FRAME_SPEED

    def updateSpeedHeart(self, force = False):
        self.timer_speed_heart = BigWorld.callback(self.SUNC_TIME, self.updateSpeedHeart)
        self.component.frame.colour.alpha = 255.0
        pl = BigWorld.player()
        if pl.__class__.__name__ != 'PlayerAvatar':
            self.hide()
            return
        try:
            BigWorld.camera().shake(0.1, (0.03, 0.03, 0.03))
        except Exception as e:
            print 'bleed shake error', e

        health = pl.GetStatValue(Stats.ch_HitPoints)
        maxHealth = pl.GetStatValue(Stats.ch_MaxHitPoints)
        if health == 0:
            self.hide()
            return
        if health / maxHealth > 0.25:
            slow = True
        else:
            slow = False
        if self.isSlow != slow or force:
            self.setSlow(slow)

    def setSlow(self, value):
        self.isSlow = value
        s = Settings()
        v = s.getSfxVolume()
        if self.isSlow:
            self.sound_fast.stop()
            self.sound_slow.play()
            self.sound_slow.volume = v
            self.SUNC_TIME = self.SLOW_TIME
            self.component.frame.colour = (100, 0, 0, 255)
        else:
            self.sound_fast.play()
            self.sound_slow.stop()
            self.sound_fast.volume = v
            self.SUNC_TIME = self.FAST_TIME
            self.component.frame.colour = (170, 41, 17, 255)
        if self.timer_speed_heart:
            BigWorld.cancelCallback(self.timer_speed_heart)
        self.timer_speed_heart = BigWorld.callback(self.SUNC_TIME, self.updateSpeedHeart)

    def hide(self):
        if self.timer_speed_heart:
            BigWorld.cancelCallback(self.timer_speed_heart)
        self.isVisible = False
        self.component.visible = False
        for name in self.BLOOD_NAMES:
            cmp = getattr(self.component, name)
            cmp.visible = False

        self.visible_components = []
        if self.sound_fast:
            self.sound_fast.stop()
        if self.sound_slow:
            self.sound_slow.stop()

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.height = sH
        self.component.width = sW
        for name in self.BLOOD_NAMES:
            cmp = getattr(self.component, name)
            cmp.height = sH
            cmp.width = sW

    def fini(self):
        pass