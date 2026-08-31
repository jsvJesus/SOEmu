# Embedded file name: scripts/client/NPC.py
"""
Created on 17.08.2010

@author: muzhig
"""
import BigWorld
from functools import partial
import traceback
from Avatar import Avatar
import ItemsUtils
from NPCs import NPCs
import particles
from Items import ItemsCatalog
from NPCs import NPCs
from Trader import Trader
from BaseTrader import BaseTrader
import Helpers.Caps
from random import random, randrange
from InteractiveObject import InteractiveObject
from CallbackHelpers import callback

class NPC(Avatar, Trader, InteractiveObject, BaseTrader):

    def __init__(self):
        Avatar.__init__(self)
        if self.npcType not in [NPCs.GUARDIAN, NPCs.STANDING_GUARDIAN]:
            Trader.__init__(self)
        if self.npcName == 'clan_base_trader':
            BaseTrader.__init__(self)
        InteractiveObject.__init__(self)
        self.facingTracker1 = None
        return

    def prerequisites(self):
        model_set, head_attachments, back_pack_attachments, weapon_back_attachments, weapon_pistol_attachments = ([],
         [],
         [],
         [],
         [])
        res = []
        for ex in (model_set,
         head_attachments,
         back_pack_attachments,
         weapon_back_attachments,
         weapon_pistol_attachments):
            for e in ex:
                if e is not None:
                    res.append(e)

        mdl = None
        if mdl is not None:
            if mdl is list:
                try:
                    for e in mdl:
                        if e is not None:
                            res.append(e)

                except Exception as e:
                    print 'error', e

            else:
                res.append(mdl)
        return res

    def onEnterWorld(self, prereq):
        Avatar.onEnterWorld(self, prereq)
        self.filter = BigWorld.AvatarDropFilter()
        InteractiveObject.onEnterWorld(self)
        if self.headTrackerEnable:
            self.idPotHeadTrackIn = BigWorld.addPot(self.matrix, 5.0, self.potCallbackIn)
            self.idPotHeadTrackOut = BigWorld.addPot(self.matrix, 23.0, self.potCallbackOut)
        if NPCs.names_by_npcName.get(self.npcName) != None and NPCs.names_by_npcName.get(self.npcName) != '<NO DATA>':
            self.name = NPCs.names_by_npcName.get(self.npcName)
        return

    def onLeaveWorld(self):
        Avatar.onLeaveWorld(self)
        if hasattr(self, 'idPotHeadTrackIn'):
            BigWorld.delPot(self.idPotHeadTrackIn)
        if hasattr(self, 'idPotHeadTrackOut'):
            BigWorld.delPot(self.idPotHeadTrackOut)
        self.potCallbackOut(0, 0)

    def set_dead(self, *e):
        if self.dead:
            self.potCallbackOut(0, 0)

    def potCallbackOut(self, enteredTrap, handle):
        if not enteredTrap:
            if hasattr(self.model, 'facingTracker1') and self.model.facingTracker1:
                self.model.facingTracker1 = None
        return

    def potCallbackIn(self, enteredTrap, handle):
        if not enteredTrap:
            return
        if self.dead:
            return
        if hasattr(self.model, 'facingTracker1') and self.model.facingTracker1:
            return
        p = BigWorld.player()
        try:
            matrix = self.model.head.matrix
        except:
            self.model.head = BigWorld.Model('')
            matrix = self.model.head.matrix

        pl_head_matrix = p.targetModelTrakerNPC.matrix
        tracker = BigWorld.Tracker()
        diffDirProvider = BigWorld.DiffDirProvider(matrix, pl_head_matrix)
        tracker.directionProvider = diffDirProvider
        secondaryNodes = [('HP_spine1', 0.15), ('spine', 0.15), ('neck', 0.3)]
        nodeInfo = BigWorld.TrackerNodeInfo(self.model, 'HP_head', secondaryNodes, 'None', -500, 500, 1000, -1000, randrange(150, 300))
        nodeInfo.maxYaw = 1.3 + randrange(-0.1, 0.4, int=float)
        nodeInfo.minYaw = -0.7 + randrange(-0.1, 0.1, int=float)
        nodeInfo.maxPitch = 0.6 + randrange(-0.1, 0.3, int=float)
        nodeInfo.minPitch = -0.5 + randrange(-0.1, 0.1, int=float)
        nodeInfo.angularHalflife = 0.001
        tracker.nodeInfo = nodeInfo
        self.model.facingTracker1 = tracker
        tracker.relativeProvider = 0

    def fire(self):
        self.delayedActionOnLaunch(30.0)
        Avatar.fire(self, draw_impacts=False)

    def GetFiryingItemDamage(self):
        damage = NPCs.damage_by_npcName.get(self.npcName)
        if damage is None:
            damage = NPCs.damage_by_npcType.get(self.npcType, {})
        return damage

    def SimpleGetFiryingItemDamage(self):
        damage = NPCs.damage_by_npcName.get(self.npcName)
        if damage is None:
            damage = NPCs.damage_by_npcType.get(self.npcType, {})
        return damage

    def onDeath(self, *args):
        Avatar.onDeath(self, *args)
        self.cancelDelayedActionOnLaunch()

    def onRevive(self):
        Avatar.onRevive(self)
        self.delayedActionOnLaunch(10.0)

    def getModel(self):
        models = [NPCs.BaseModel]
        onTheHead = []
        backpack = []
        tints = {}
        head_tints = {}
        tints_backpack = {}
        models.append(NPCs.Heads.models[self.npcHead])
        tint_head = NPCs.Heads.tint_head.get(self.npcHead)
        if tint_head:
            tints['tint_head'] = tint_head
        cap = NPCs.Caps.models[self.npcCap]
        tint_cap = NPCs.Caps.tint_cap.get(self.npcCap)
        if tint_cap:
            head_tints['tint_cap'] = tint_cap
        mask = NPCs.Masks.models[self.npcMask]
        tint_mask = NPCs.Masks.tint_mask.get(self.npcMask)
        if tint_mask:
            head_tints['tint_mask'] = tint_mask
        if cap:
            onTheHead.append(cap)
        if mask:
            onTheHead.append(mask)
        models.append(NPCs.Bodies.models[self.npcBody])
        tint_body = NPCs.Bodies.tint_body.get(self.npcBody)
        if tint_body:
            tints['tint_body'] = tint_body
        backpack.append(NPCs.Backpacks.models[self.npcBackpack])
        tints_back = NPCs.Backpacks.tint_back.get(self.npcBackpack)
        if tints_back:
            tints_backpack['tint_back'] = tints_back
        models.append(NPCs.Hands.models[self.npcHands])
        tint_hand = NPCs.Hands.tint_hand.get(self.npcHands)
        if tint_hand:
            tints['tint_hand'] = tint_hand
        armor = NPCs.Armors.models[self.npcArmor]
        tint_armor = NPCs.Armors.tint_armor.get(self.npcArmor)
        if tint_armor:
            tints['tint_armor'] = tint_armor
        if armor:
            models.append(armor)
        models.append(NPCs.Legs.models[self.npcLegs])
        tint_legs = NPCs.Legs.tint_legs.get(self.npcLegs)
        if tint_legs:
            tints['tint_legs'] = tint_legs
        models.append(NPCs.Boots.models[self.npcBoots])
        tint_boots = NPCs.Boots.tint_boots.get(self.npcBoots)
        if tint_boots:
            tints['tint_boots'] = tint_boots
        return ((models, tints),
         (onTheHead, head_tints),
         (backpack, tints_backpack),
         bool(armor))

    def set_npcFlags(self, v):
        tmpCaps = self.targetCaps
        if Helpers.Caps.CAP_CAN_EXCHANGE in tmpCaps:
            tmpCaps.remove(Helpers.Caps.CAP_CAN_EXCHANGE)
            self.targetCaps = tmpCaps

    def getEquippedItemType(self):
        return ItemsUtils.GetEquippedItemType(self)

    def getAvatarAnimationCaps(self):
        equippedItemType = self.getEquippedItemType()
        if equippedItemType in [ItemsCatalog.PISTOL, ItemsCatalog.REVOLVER]:
            caps_list = []
        elif equippedItemType in [ItemsCatalog.ASSAULT_RIFLE,
         ItemsCatalog.SNIPER_RIFLE,
         ItemsCatalog.SHOTGUN,
         ItemsCatalog.MACHINE_GUN,
         ItemsCatalog.SUB_MACHINE_GUN,
         ItemsCatalog.RIFLE,
         ItemsCatalog.GRENADE_LAUNCHER,
         ItemsCatalog.ROCKET_LAUNCHER]:
            caps_list = ['AutogunArmed']
        else:
            caps_list = ['Unarmed']
        if self.dead:
            caps_list.append('Dead')
        if self.isDisableDialogs:
            caps_list = ['NPC_DISABLE']
        return caps_list

    def SetAvatarModel(self):
        (body, body_tints), (onTheHead, on_head_tints), (backpack, backpackTints), armored = self.getModel()
        try:
            if self.isDisableDialogs:
                body = list(body)
                body.append('characters/items/misc/guitar_lod1.model')
                body.append('models/bolvan/taburet_4_npc.model')
            self.model = BigWorld.Model(*body)
            for attrname, attrvalue in body_tints.items():
                setattr(self.model, attrname, attrvalue)

        except ValueError as e:
            print e
            print body
            raise

        if onTheHead:
            try:
                self.model.head = BigWorld.Model(*onTheHead)
                for attrname, attrvalue in on_head_tints.items():
                    setattr(self.model.head, attrname, attrvalue)

            except ValueError as e:
                print e
                print onTheHead

        if backpack:
            try:
                model_backpack = BigWorld.Model(*backpack)
                for tintattrname, tintattrvalue in backpackTints.items():
                    setattr(model_backpack, tintattrname, tintattrvalue)

                if armored:
                    self.model.backpack = model_backpack
                else:
                    self.model.backpack_noarmor = model_backpack
            except ValueError as e:
                print e
                print backpack

        modelNames_dict = {}
        if self.npcWeapon:
            weapon = NPCs.Weapons.weapon_items.get(self.npcWeapon)
            gun_type = ItemsCatalog.NONE_TYPE
            if weapon:
                self.ActiveItemID = 1000
                self.ActiveItemType = weapon['TypeID']
                modelNames_dict = {ItemsCatalog.BODY: [weapon['ModelNames'][ItemsCatalog.BODY], '', {}]}
                gun_type = weapon['GunType']
            self.autogunModel = self.getModelByNamesDict(modelNames_dict)
            self.hp_barrel_node = self.autogunModel.node('HP_barrel')
            self.model.effectorright = self.autogunModel
        self.UpdateAvatarAnimationCaps()
        if not self.dead:
            if self.npcWeapon:
                rate = self.model.IdleForever.frameRate * (0.9 + 0.2 * random())
                self.model.IdleForever(0, None, 0, -1, -1, rate)
            else:
                rate = self.model.IdleUnarmed.frameRate * (0.9 + 0.2 * random())
                self.model.IdleUnarmed(0, None, 0, -1, -1, rate)
            self.startModelAction(self.actionOnLaunch)
        try:
            lfoot = self.model.node('lefttoebase')
            rfoot = self.model.node('righttoebase')
            footSoundPath = 'players/footsteps'
            self.footTriggers = [BigWorld.FootTrigger(0, footSoundPath), BigWorld.FootTrigger(1, footSoundPath)]
            lfoot.attach(self.footTriggers[0])
            rfoot.attach(self.footTriggers[1])
            self.dustSource = particles.attachDustSource(self.model)
        except:
            print "ERROR: Unable to set up foot triggers for model ['%s']" % "', '".join(self.model.sources)

        self.add_collider()
        self.set_npcFlags(None)
        if self.npcFlags & NPCs.FLAG_NIGHT_HIGHLIGHT:
            self.createLight()
        self.onAvatarModelChanged()
        scale = tuple([NPCs.scale_by_npcName.get(self.npcName, 1.0)] * 3)
        if self.model:
            self.model.scale = scale
            if getattr(self.model, 'head', None):
                self.model.head.scale = scale
            if getattr(self.model, 'backpack', None):
                self.model.backpack.scale = scale
        if getattr(self, 'autogunModel', None):
            self.autogunModel.scale = scale
        if self.isDisableDialogs:
            self.model.UseGuitar()
        return

    def startModelAction(self, action_name):
        if action_name:
            try:
                self.model.action(action_name)()
                return True
            except ValueError:
                pass

        return False

    def stopModelAction(self, action_name):
        if action_name:
            try:
                self.model.action(action_name).stop()
                return True
            except ValueError:
                pass

        return False

    def cancelDelayedActionOnLaunch(self):
        callback.cancel('NPC.delayedActionOnLaunch%s' % self.id)

    def delayedActionOnLaunch(self, time_to_delay = 0.0):
        if self.actionOnLaunch:
            self.stopModelAction(self.actionOnLaunch)
            callback(partial(self.startModelAction, self.actionOnLaunch), time_to_delay, cancel_existing=True, id='NPC.delayedActionOnLaunch%s' % self.id)

    def reload(self, reload_type, time_mod, ammo_num):
        self.EnableModelPitch(False)
        self.model.ReloadAutogun(0, self.onReloadAnimationEnd)

    def onReloadAnimationEnd(self):
        self.EnableModelPitch(True)

    def dropItem(self, id):
        pass

    def deleteItem(self, id):
        pass

    def prepareForTeleport(self):
        pass

    def afterTeleport(self):
        pass

    def set_talkFlag(self, old_value):
        InteractiveObject.set_talkFlag(self, old_value)

    def set_isDisableDialogs(self, old_value):
        self.SetAvatarModel()
        if self.isDisableDialogs:
            self.model.UseGuitar()
        else:
            self.model.UseGuitar().stop()