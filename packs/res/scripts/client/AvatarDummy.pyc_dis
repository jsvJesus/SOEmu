# Embedded file name: scripts/client/AvatarDummy.py
"""
Created on 28.01.2011

@author: muzhig
"""
import BigWorld
from Math import Vector3
import ResMgr
import time
import Account
import Avatar
from CallbackHelpers import callback
from Helpers.Listener import Listenable
from Items import ItemsCatalog
import GUI
from random import random
import heads
import soGUI
import ItemsUtils
import StalkerModel
from utils_bw import wait
from DummyRotating import DummyRotating
dummies = []

class AvatarDummy(BigWorld.Entity, Listenable):
    """
    \xd0\x9a\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81 \xd0\xb4\xd0\xbb\xd1\x8f \xd0\xbe\xd1\x82\xd0\xbe\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd0\xb2\xd0\xb5\xd1\x89\xd0\xb5\xd0\xb9 \xd0\xb0\xd0\xb2\xd0\xb0\xd1\x82\xd0\xb0\xd1\x80\xd0\xb0 \xd0\xbd\xd0\xb0 \xd0\xba\xd0\xbb\xd0\xb8\xd0\xb5\xd0\xbd\xd1\x82\xd0\xb5, \xd0\xba\xd0\xbe\xd0\xb3\xd0\xb4\xd0\xb0 \xd0\xbe\xd0\xbd \xd0\xb2\xd1\x8b\xd0\xb1\xd0\xb8\xd1\x80\xd0\xb0\xd0\xb5\xd1\x82 \xd0\xbf\xd0\xb5\xd1\x80\xd1\x81\xd0\xbe\xd0\xbd\xd0\xb0\xd0\xb6, \xd0\xba\xd0\xbe\xd1\x82\xd0\xbe\xd1\x80\xd1\x8b\xd0\xbc \xd1\x85\xd0\xbe\xd1\x87\xd0\xb5\xd1\x82 \xd0\xb7\xd0\xb0\xd0\xb9\xd1\x82\xd0\xb8 \xd0\xb2 \xd0\xb8\xd0\xb3\xd1\x80\xd1\x83
    """
    SELECTED_BREATH_RATE_ADDITION = 1.0
    DEFAULT_BREATH_TEMPO = 1.0

    def __init__(self):
        BigWorld.Entity.__init__(self)
        Listenable.__init__(self)
        self.name = ''
        self.character = None
        self.default_models = {}
        self.register()
        return

    def register(self):
        dummies.append(self)

    def setBreath(self, tempo = DEFAULT_BREATH_TEMPO):
        if not self.model:
            return
        else:
            try:
                rate = self.model.IdleUnarmed.frameRate * tempo
                self.model.IdleUnarmed.stop()
                self.model.IdleUnarmed(0, None, 0, -1, -1, rate)
            except:
                print 'AvatarDummy - action error'

            return

    def getCurrentBreathFrame(self):
        time_passed = time.time() - self.breath_start
        frames_passed = self.breath_rate * time_passed
        frames_count = self.model.IdleUnarmed.frameCount
        frames_mod = frames_passed % frames_count
        return int((self.breath_start_frame + frames_mod) % frames_count)

    def reset(self):
        self.character = None
        self.name = ''
        self.setModel(clear=True)
        return

    def set_character(self, character):
        BigWorld.delShadowEntity(self)
        if character:
            self.character = character
            self.name = self.character.name
            self.filter = BigWorld.AvatarFilter()
            self.setModel()
            BigWorld.addShadowEntity(self)
        else:
            self.character = None
            self.name = ''
            self.setModel(False)
        return

    def onEnterWorld(self, pre = None):
        self.listeners.onEnterWorld()

    def onLeaveWorld(self):
        BigWorld.delShadowEntity(self)
        self.nameBoxAtch = None
        self.nameBox = None
        return

    def update_from_GUI(self, choice_group, data, set_model_finally = True):
        model_part = {'01_head': ItemsCatalog.HEAD,
         '02_body': ItemsCatalog.SHIRT,
         '03_palms': ItemsCatalog.HANDS,
         '04_legs': ItemsCatalog.PANTS,
         '05_feet': ItemsCatalog.BOOTS}[choice_group]
        if choice_group == heads.gui_key:
            self.default_models[model_part] = heads.preset_by_headid[data['head_id']]
        else:
            self.default_models[model_part] = data['item_type_ID']
        if set_model_finally:
            self.setModel()

    def set_default_models_from_gui(self, data):
        for cg, value in data.iteritems():
            self.update_from_GUI(cg, value, False)

        self.setModel()

    def setModel(self, clear = False):
        if clear:
            self.model = None
            self.default_models.clear()
        else:
            if self.model:
                savedActionQueue = ResMgr.DataSection('savedActionQueue')
                self.model.saveActionQueue(savedActionQueue)
            else:
                savedActionQueue = None
            self.model = self.compileModel()
            if savedActionQueue:
                self.model.restoreActionQueue(savedActionQueue)
            else:
                self.setBreath()
            DummyRotating().init_motor(self.model)
        return

    def compileModel(self):

        def GetDefaultValues():
            var_dict = {}
            for key in ItemsCatalog.cloth_dict:
                var_dict[ItemsCatalog.cloth_dict[key][0]] = 0
                var_dict[ItemsCatalog.cloth_dict[key][1]] = 0

            return var_dict

        self.ActiveArmorSet = self.character.playerKit if self.character else GetDefaultValues()
        self.ActiveWeaponSet = {'PrimarySlotID': 0,
         'SecondarySlotID': 0}
        return StalkerModel.ComposePlayerModel(self)

    def getDefaultModels(self):
        if self.character:
            return Avatar.parse_character_default_models(self.character['defaultModels'])
        else:
            return self.default_models

    def GetEquippedItemModels(self, type):
        return None

    def hasArmor(self):
        if self.ActiveArmorSet['ArmorID'] > 0:
            return True
        else:
            return False

    def GetPlayerEntryValues(self, entries, default_values = None):
        BASE = 'characters/avatars/basem.model'
        default_values = default_values or {}
        list_added_to_model_items = [0]
        supermodel = [BASE]
        headmodel = []
        i = 0
        for model_part in ItemsCatalog.cloth_dict.keys():
            model = None
            i += 1
            if entries.has_key(model_part):
                item_type = entries[model_part][0]
                if item_type not in list_added_to_model_items:
                    model = ItemsUtils.getModelNameByItemType(item_type)
                    if model:
                        list_added_to_model_items.append(item_type)
            elif default_values.has_key(model_part):
                model = default_values[model_part][0]
            if model:
                if model_part in ItemsCatalog.base_model_attr_dict.keys():
                    supermodel.append(model)
                elif model_part in ItemsCatalog.head_mode_attr_dict.keys():
                    headmodel.append(model)

        return (supermodel, headmodel)