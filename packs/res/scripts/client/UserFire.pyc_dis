# Embedded file name: scripts/client/UserFire.py
import BigWorld
import Math
import Pixie
import random
import ItemsUtils
import time
import GUI
from Localization import lc
from ItemHolder import ItemHolder
from Helpers.Caps import CAP_CAN_OPEN_AND_EXPLORE_USER_FIRE

class UserFire(BigWorld.Entity, ItemHolder):
    """" client/UserFire """
    LIGHT_BLINK_SPEED = 0.15
    LIGHT_BLINK_DELTA = 9.1e-05
    UPDATE_TIME_LIFE = 0.2
    multiply = 3.0
    MODEL_NAME = 'models\\misc\\fireplace\\fireplace03_lod01.model'
    MODEL_NAME_OFF = 'models\\misc\\fireplace\\fireplace03_lod01_off.model'
    PARTICLES_NAMES = ('particles\\_bonfire3.xml', 'particles\\_bonfire2.xml', 'particles\\_bonfire.xml')
    PARTICLES_NAME_OFF = 'particles\\fire_place03.xml'

    def __init__(self):
        BigWorld.Entity.__init__(self)
        self.light_timer_id = None
        self.sound = None
        self._fireType = 0
        self.targetCaps = [CAP_CAN_OPEN_AND_EXPLORE_USER_FIRE]
        self.effects = None
        self._sound = None
        self.name = lc('soGUICore.soGUI.STRING_FirePlace') + u' %s' % self.pOwnerName
        self._messageTimerHandle = None
        self._messageAttachment = None
        self._loopFire_timer_id = None
        self.life_time = None
        self.max_life_time = None
        self.dict_items = {}
        return

    def onEnterWorld(self, prereqs):
        self._model = BigWorld.Model(self.MODEL_NAME)
        self.effects = [ Pixie.create(name) for name in self.PARTICLES_NAMES ]
        self._model_OFF = BigWorld.Model(self.MODEL_NAME_OFF)
        self.effect_OFF = Pixie.create(self.PARTICLES_NAME_OFF)
        self._model_OFF.root.attach(self.effect_OFF)
        self.changeFireEf(self._fireType)
        self.light = light = BigWorld.PyChunkLight()
        self.light_start_position = self.position + Math.Vector3(0.0, 0.7, 0)
        light.innerRadius = 2.0
        light.outerRadius = 10.0
        light.position = self.light_start_position
        light.specular = 1
        light.diffuse = 1
        light.visible = 1
        light.colour = Math.Vector4(self.multiply * 255.0, self.multiply * 128.0, 0.0, self.multiply * 255.0)
        self._fire_light_blend()
        self._loopFire()
        self.cell.updateClients()

    def onLeaveWorld(self):
        self.light.visible = False
        if self.light_timer_id:
            BigWorld.cancelCallback(self.light_timer_id)
        if self._loopFire_timer_id:
            BigWorld.cancelCallback(self._loopFire_timer_id)
        self._clearMessage()
        if self._sound:
            self._sound.stop()

    def changeFireEf(self, fireType):
        last_model = self.model
        if fireType:
            moddelCnahe = 0
            if self.model != self._model:
                moddelCnahe = 1
                self.model = self._model
            for fire in self.model.root.attachments:
                self.model.root.detach(fire)

            self.model.root.attach(self.effects[fireType - 1])
            if not self._sound:
                self._sound = BigWorld.playSound('environment/fire_campfire', self.model)
            if moddelCnahe and last_model:
                self._sound.play()
        elif self.model != self._model_OFF:
            self.model = self._model_OFF

    def updateLifeTime(self, fireType, life_time, max_life_time, dict_items):
        if self._fireType != fireType:
            self.changeFireEf(fireType)
        self._fireType = fireType
        self.life_time = life_time
        self.max_life_time = max_life_time
        self.dict_items = {}
        for x in dict_items:
            complexItemID = x['id']
            cook_time = x['time']
            alltime = x['alltime']
            self.dict_items[complexItemID] = [cook_time, alltime]

    def _loopFire(self):
        self._loopFire_timer_id = BigWorld.callback(self.UPDATE_TIME_LIFE, self._loopFire)
        if self.life_time is None or self.max_life_time is None:
            return
        else:
            self.life_time -= self.UPDATE_TIME_LIFE
            if self.life_time < 0:
                self.life_time = 0
            multiply = self.multiply * self.life_time / self.max_life_time
            self.light.colour = Math.Vector4(multiply * 255.0, multiply * 128.0, 0.0, multiply * 255.0)
            if self.life_time:
                for complexItemID in self.dict_items.keys():
                    cook_time, alltime = self.dict_items[complexItemID]
                    cook_time -= self.UPDATE_TIME_LIFE
                    if cook_time < 0:
                        cook_time = 0
                    self.dict_items[complexItemID] = [cook_time, alltime]

            return

    def _fire_light_blend(self):
        self.light_timer_id = BigWorld.callback(random.random() * self.LIGHT_BLINK_SPEED, self._fire_light_blend)

        def r():
            return random.randrange(-1000, 1000) * self.LIGHT_BLINK_DELTA

        self.light.position = self.light_start_position + Math.Vector3(r(), r(), r())

    def _displayMessage(self, msg):
        self._clearMessage()
        text = GUI.Text(msg)
        text.explicitSize = True
        text.size = (0, 0.4)
        text.colour = (255, 205, 149, 245)
        text.filterType = 'LINEAR'
        text.verticalAnchor = 'BOTTOM'
        text.position = (0, 1, 0)
        atch = GUI.Attachment()
        atch.component = text
        atch.faceCamera = True
        self.text_atch = atch
        self.model.root.attach(atch)
        self._messageAttachment = atch
        self._setMessageHideTimer()

    def _clearMessage(self):
        self._cancelMessageTimer()
        if self._messageAttachment is not None:
            self.model.root.detach(self._messageAttachment)
            self._messageAttachment = None
        return

    def _setMessageHideTimer(self, timeout = 500.0):
        self._cancelMessageTimer()
        self._messageTimerHandle = BigWorld.callback(timeout, self._handleMessageHideTimer)

    def _cancelMessageTimer(self):
        if self._messageTimerHandle is not None:
            BigWorld.cancelCallback(self._messageTimerHandle)
            self._messageTimerHandle = None
        return

    def _handleMessageHideTimer(self):
        self._messageTimerHandle = None
        self._clearMessage()
        return

    def set_CarryingItems(self, old_value):

        def redraw_player_cache(enteredTrap, handle):
            if enteredTrap:
                pl = BigWorld.player()
                if pl.__class__.__name__ == 'PlayerAvatar':
                    pl.NeedToUpdateItemCache()

        BigWorld.addPot(self.matrix, ItemsUtils.EXTRACTION_RANGE, redraw_player_cache)