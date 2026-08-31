# Embedded file name: scripts/client/ItemHolder.py
"""
Created on 21.07.2010

@author: leviathan
"""
import BigWorld
import BWPersonality
import ItemsUtils
from Items import ItemsCatalog
from Math import Vector3
from Inventory import Inventory
import copy
from FiringDefs import FiringDefs
import traceback
from copy import deepcopy
import Durations
from ItemHolderCommon import ItemHolderCommon
import gui_jokes
import colorCodes
from Localization import lc
from Codes import ShopResponses
from NPCs import NPCs
_NPCs = NPCs()

class ItemHolder(ItemHolderCommon):

    def Initialize(self):
        pass

    def InitWeaponAmmo(self):
        pass

    def GetEquippedWeaponMastery(self):
        if not ItemsUtils.CheckEquippedItemValidityClient(self):
            return ItemsCatalog.NONE_TYPE
        complexItemType = self.ActiveItemType
        complexItemParams = ItemsCatalog.GetItemParam(complexItemType)
        if not complexItemParams:
            return ItemsCatalog.NONE_TYPE
        item_class = ItemsCatalog.GetItemClass(complexItemType)
        if item_class != ItemsCatalog.WEAPON:
            return ItemsCatalog.NONE_TYPE
        return complexItemParams['SkillLevel']

    def GetEquippedBinocularAbility(self):
        if self.ActiveGadjetSet.GadjetID:
            gadget_param = ItemsCatalog.GetItemParam(self.ActiveGadjetSet.GadjetType)
            return gadget_param.get('Zoom', None)
        else:
            return None

    def GetEquippedBinocularAbilityNVpossible(self):
        if self.ActiveGadjetSet.GadjetID:
            gadget_param = ItemsCatalog.GetItemParam(self.ActiveGadjetSet.GadjetType)
            return gadget_param.get('isNightVision', False)

    def GetGrenadeThrowPossibility(self):
        if not ItemsUtils.CheckEquippedGrenadeValidityClient(self):
            return False
        return True

    def GetThrowingGrenadeParam(self):
        complexItem = ItemsUtils.GetComplexItemByID(self, self.ActiveGrenadeID)
        complexItemType = complexItem['complexItemType']
        item_class = ItemsCatalog.GetItemClass(complexItemType)
        if item_class != ItemsCatalog.WEAPON:
            return
        properties_keys = complexItem['complexItemParametresKeys']
        complexItem['complexItemParametresValues'][properties_keys.index(ItemsCatalog.INC_MUNITION_NUMBER)] -= 1
        self.NeedToUpdateWeaponIcon()

    def GetFiringGrenadeThrowType(self):
        if not ItemsUtils.CheckEquippedGrenadeValidityClient(self):
            return None
        complexItemType = self.ActiveGrenadeType
        item_class = ItemsCatalog.GetItemClass(complexItemType)
        if item_class != ItemsCatalog.EXPLOSION:
            return None
        item_param = ItemsCatalog.GetItemParam(complexItemType)
        if item_param:
            return item_param['ThrowType']
        else:
            return None

    def GetShootPossibility(self):
        if not ItemsUtils.CheckEquippedItemValidityClient(self):
            return FiringDefs.NO_ITEM_EQUIPPED
        if not self.GetModelShootPossibility():
            return FiringDefs.MODEL_NOT_READY
        complexItem = ItemsUtils.GetComplexItemByID(self, self.ActiveItemID)
        if complexItem:
            complexItemType = complexItem['complexItemType']
            item_class = ItemsCatalog.GetItemClass(complexItemType)
            if item_class != ItemsCatalog.WEAPON:
                return FiringDefs.NOT_A_WEAPON
            item_params = ItemsUtils.GetComplexItemInconstanParams(complexItem)
            if self.CurrentWeaponAmmo <= 0:
                return FiringDefs.NO_AMMO
            if self.ActiveItemJammed != 0:
                return FiringDefs.WEAPON_JAMMED
            return FiringDefs.WEAPON_READY
        return FiringDefs.NO_ITEM_EQUIPPED

    def IsCurrentWeaponAutomatic(self):
        if not ItemsUtils.CheckEquippedItemValidityClient(self):
            return False
        elif self.CurrentWeaponParam['FireType'] == ItemsCatalog.AUTOMATIC:
            return True
        else:
            return False

    def GetFiryingItemParams(self):
        if not ItemsUtils.CheckEquippedItemValidityClient(self):
            return (0.0,
             100.0,
             0,
             0,
             -1,
             0,
             {ItemsCatalog.WEAPON_ACCMOD_LYING: 2.0,
              ItemsCatalog.WEAPON_ACCMOD_AIM_LYING: 1.5,
              ItemsCatalog.WEAPON_ACCMOD_SNIPING_LYING: 1.1,
              ItemsCatalog.WEAPON_ACCMOD_KNEES: 3.0,
              ItemsCatalog.WEAPON_ACCMOD_AIM_KNEES: 2.5,
              ItemsCatalog.WEAPON_ACCMOD_SNIPING_KNEES: 2.0,
              ItemsCatalog.WEAPON_ACCMOD_STAND: 6.0,
              ItemsCatalog.WEAPON_ACCMOD_AIM_STAND: 5.0,
              ItemsCatalog.WEAPON_ACCMOD_SNIPING_STAND: 0.5,
              ItemsCatalog.WEAPON_SCOPEMOD_SNIPING_STAND: 5.0})
        complexItemType = self.ActiveItemType
        complexItemParams = ItemsCatalog.GetItemParam(complexItemType)
        ammo_params = ItemsCatalog.GetItemParam(self.ActiveItemAmmoType)
        if ammo_params:
            ammo_accuracy = ammo_params.get('Accuracy', 0)
            num_shot = ammo_params['NumShots']
        else:
            ammo_accuracy = 0
            num_shot = ItemsCatalog.DEFAULT_NUM_SHOTS
        fire_params = []
        fire_params.append(complexItemParams['Accuracy'] + ammo_accuracy)
        fire_params.append(complexItemParams['Range'])
        fire_params.append(num_shot)
        fire_params.append(complexItemParams['RateOfFire'])
        fire_params.append(ItemsUtils.GetFiryingItemSFXParams(self))
        fire_params.append(complexItemParams['FireType'])
        fire_params.append(complexItemParams['AccStandMods'])
        return fire_params

    def SpendFiryingWeaponAmmo(self):
        self.CurrentWeaponAmmo -= 1
        gun_type = ItemsCatalog.GetItemParam(self.ActiveItemType)['GunType']
        if gun_type == ItemsCatalog.ROCKET_LAUNCHER:
            if self.CurrentWeaponAmmo <= 0:
                complexItem = ItemsUtils.GetComplexItemByID(self, self.ActiveItemID)
                if not complexItem:
                    print 'error spend weapon ammo'
                    return
                complexItem_InconstantParam = ItemsUtils.GetComplexItemInconstanParams(complexItem)
                complexItem_InconstantParam[ItemsCatalog.INC_LOADED_MUNITION_TYPE] = 0
                ItemsUtils.SetComplexItemInconstanParams(complexItem, complexItem_InconstantParam)
                ItemsUtils.SetActiveWeaponUpgradesTypes(self, complexItem)
        self.NeedToUpdateWeaponIcon()

    def GetEquippedItemAmmoModels(self, secondary_primary_active):
        if secondary_primary_active == ItemsCatalog.SECONDARY:
            complexItemType = self.ActiveWeaponSet.SecondarySlotType
        elif secondary_primary_active == ItemsCatalog.PRIMARY:
            complexItemType = self.ActiveWeaponSet.PrimarySlotType
        elif secondary_primary_active == ItemsCatalog.ACTIVE:
            if not ItemsUtils.CheckEquippedItemValidityClient(self):
                return ''
            complexItemType = self.ActiveItemType
        complexItemParams = ItemsCatalog.GetItemParam(complexItemType)
        gun_type = complexItemParams['GunType']
        gun_priority = ItemsUtils.GetWeaponPriority(gun_type)
        if gun_priority == ItemsCatalog.SECONDARY:
            upgrade_item_type = self.SecondaryWeaponUpgrades[ItemsCatalog.weapon_upgrades_dict[ItemsCatalog.INC_LOADED_MUNITION_TYPE]]
        else:
            upgrade_item_type = self.PrimaryWeaponUpgrades[ItemsCatalog.weapon_upgrades_dict[ItemsCatalog.INC_LOADED_MUNITION_TYPE]]
        if upgrade_item_type > 0:
            upgrade_item_param = ItemsCatalog.GetItemParam(upgrade_item_type)
            model_dict = {}
            for key in upgrade_item_param['ModelNames']:
                tint_dict = {}
                if complexItemParams.has_key('Tint'):
                    tint_dict = complexItemParams['Tint']
                model_dict[key] = [upgrade_item_param['ModelNames'][key], ItemsCatalog.HardPointsNames[key], tint_dict]

            return model_dict

    def GetEquippedItemModels(self, secondary_primary_active):
        if secondary_primary_active == ItemsCatalog.SECONDARY:
            complexItemType = self.ActiveWeaponSet.SecondarySlotType
            complexItemID = self.ActiveWeaponSet.SecondarySlotID
            tintID = self.ActiveWeaponSet.SecondarySlotTintID
        elif secondary_primary_active == ItemsCatalog.PRIMARY:
            complexItemType = self.ActiveWeaponSet.PrimarySlotType
            complexItemID = self.ActiveWeaponSet.PrimarySlotID
            tintID = self.ActiveWeaponSet.PrimarySlotTintID
        elif secondary_primary_active == ItemsCatalog.ACTIVE:
            if not ItemsUtils.CheckEquippedItemValidityClient(self):
                return
            complexItemType = self.ActiveItemType
            complexItemID = self.ActiveItemID
            tintID = self.ActiveTintID
        complexItemParams = ItemsCatalog.GetItemParam(complexItemType)
        if not complexItemParams:
            return
        else:
            gun_type = complexItemParams['GunType']
            model_dict = {}
            item_core_model_dict = complexItemParams['ModelNames']
            for key in item_core_model_dict:
                tint_dict = {}
                if complexItemParams.has_key('TintsNames'):
                    tintName = ItemsUtils.getTintNameByID(tintID)
                    if tintName is not None:
                        tint_dict = {'tint_weapon': tintName}
                elif complexItemParams.has_key('Tint'):
                    tint_dict = complexItemParams['Tint']
                model_dict[key] = [item_core_model_dict[key], ItemsCatalog.HardPointsNames[key], tint_dict]

            for upgrade in ItemsCatalog.weapon_upgrades_dict.keys():
                gun_priority = ItemsUtils.GetWeaponPriority(gun_type)
                if gun_priority == ItemsCatalog.SECONDARY:
                    upgrade_item_type = self.SecondaryWeaponUpgrades[ItemsCatalog.weapon_upgrades_dict[upgrade]]
                else:
                    upgrade_item_type = self.PrimaryWeaponUpgrades[ItemsCatalog.weapon_upgrades_dict[upgrade]]
                if upgrade_item_type > 0:
                    upgrade_item_param = ItemsCatalog.GetItemParam(upgrade_item_type)
                    if upgrade_item_param != None:
                        tint_dict = {}
                        if upgrade_item_param.has_key('TintsNames'):
                            tintName = ItemsUtils.getTintNameByID(tintID)
                            if tintName is not None:
                                tint_dict = {'tint_weapon': tintName}
                        elif complexItemParams.has_key('Tint'):
                            tint_dict = complexItemParams['Tint']
                        part_type = upgrade_item_param.get('PartType', 0)
                        if len(upgrade_item_param['ModelNames'].values()):
                            model_dict[part_type] = [upgrade_item_param['ModelNames'].values()[0], ItemsCatalog.HardPointsNames[part_type], tint_dict]

            return model_dict

    def GetItemModel(self, item):
        models_lsit = ItemsCatalog.GetItemParam(item['complexItemType'])['ModelNames'].values()
        for sub_item in item['itemList']:
            sub_item_params = ItemsCatalog.GetItemParam(sub_item['itemType'])
            if sub_item_params:
                models_lsit += sub_item_params['ModelNames'].values()

        return models_lsit

    def DropActiveItem(self):
        self.dropItem(self.ActiveItemID)

    def SearchInEquipsAndSetToZero(self, itemID):
        ItemsUtils.SearchIDinEquipsAndSetToZero(self, itemID)
        return
        if itemID == self.ActiveItemID:
            self.ActiveItemID = 0
            self.autogunModel = BigWorld.Model('')
            self.model.effectorright = self.autogunModel
        if itemID == self.ActiveGrenadeID:
            self.ActiveGrenadeID = 0
        if itemID == self.ActiveWeaponSet.SecondarySlotID:
            for key in self.SecondaryWeaponUpgrades.keys():
                self.SecondaryWeaponUpgrades[key] = 0

        elif itemID == self.ActiveWeaponSet.PrimarySlotID:
            for key in self.PrimaryWeaponUpgrades.keys():
                self.PrimaryWeaponUpgrades[key] = 0

        for key in self.ActiveArmorSet.keys():
            if self.ActiveArmorSet[key] == itemID:
                self.ActiveArmorSet[key] = 0
                if self.AvatarCanRedrawModel():
                    self.SetAvatarModel()

        for key in self.ActiveWeaponSet.keys():
            if self.ActiveWeaponSet[key] == itemID:
                self.ActiveWeaponSet[key] = 0
                if self.AvatarCanRedrawModel():
                    self.SetAvatarModel()

        for key in self.ActiveGadjetSet.keys():
            if self.ActiveGadjetSet[key] == itemID:
                self.ActiveGadjetSet[key] = 0

    def onDropItem(self, item):
        if self.canDrop():
            itemID = item['complexItemID']
            if item:
                if not ItemsUtils.IsItemMoveable(item):
                    self.cell.dropItem(itemID)
                    self.SearchInEquipsAndSetToZero(itemID)
                    self.LockItemToDrop(item)
        self.NeedToUpdateInventory()

    def onDeleteItem(self, item):
        if item:
            itemID = item['complexItemID']
            if not ItemsUtils.IsItemMoveable(item):
                self.cell.deleteItem(itemID)
                self.SearchInEquipsAndSetToZero(itemID)
        self.NeedToUpdateInventory()

    def set_CarryingItems(self, oldType = None):
        pass

    def set_CreditNumber(self, oldType = None):
        pass

    def set_ActiveItemID(self, oldType = None):
        pass

    def set_ActiveGrenadeID(self, oldType = None):
        pass

    def NeedToUpdateInventory(self):
        pass

    def NeedToUpdateTradeInterface(self, trader_id):
        pass

    def NeedToUpdateWeaponIcon(self):
        pass

    def getModelByNamesDict(self, names_dict):
        core_model = None
        if names_dict:
            body_entry = names_dict[ItemsCatalog.BODY]
            core_model = BigWorld.Model(body_entry[ItemsUtils.MODEL_LIST_POSITION])
            tint_dict = body_entry[ItemsUtils.MODEL_TINT_DICT_POSITION]
            if tint_dict:
                for tint_key in tint_dict:
                    if hasattr(core_model, tint_key):
                        setattr(core_model, tint_key, tint_dict[tint_key])

            del names_dict[ItemsCatalog.BODY]
            if names_dict:
                for model_entry in names_dict.values():
                    if model_entry[ItemsUtils.MODEL_LIST_POSITION]:
                        model = BigWorld.Model(model_entry[ItemsUtils.MODEL_LIST_POSITION])
                    else:
                        continue
                    tint_dict = model_entry[ItemsUtils.MODEL_TINT_DICT_POSITION]
                    if tint_dict:
                        for tint_key in tint_dict:
                            if hasattr(model, tint_key):
                                setattr(model, tint_key, tint_dict[tint_key])

                    try:
                        setattr(core_model, model_entry[ItemsUtils.MODEL_HP_POSITION], model)
                    except ValueError:
                        print 'Cant attach model at hp', model_entry[ItemsUtils.MODEL_HP_POSITION], ' model name ', model_entry[ItemsUtils.MODEL_LIST_POSITION]
                        return core_model
                    except AttributeError:
                        print 'Cant attach model at hp', model_entry[ItemsUtils.MODEL_HP_POSITION], ' model name ', model_entry[ItemsUtils.MODEL_LIST_POSITION]
                        return core_model

        return core_model

    def getModelNameByNamesDict(self, names_dict):
        if names_dict:
            if len(names_dict) == 1:
                return names_dict[0]
            else:
                return names_dict
        else:
            return None
        return None

    def onPutOnItem(self, item, slot_number = 0):
        self.systemChatline('onPutOnItem')
        if not self.canEquip():
            return
        elif item:
            item_type = item['complexItemType']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            itemID = item['complexItemID']
            if ItemsUtils.GetComplexItemByID(self, itemID) is None:
                return
            unequiping_item_type = 0
            if item_class == ItemsCatalog.CLOTH:
                pass
            elif item_class == ItemsCatalog.ARTIFACT:
                if not self.CheckEquippedArtifactNumber():
                    return
                if not ItemsUtils.IsItemEquipable(None, item_params):
                    return
                depleet_time = ItemsUtils.GetArtefactDepleetionTime(item, item_params, self.timeServerDiff)
                if depleet_time != None and depleet_time < 0:
                    return
            if item_class == ItemsCatalog.GADGET:
                if ItemsUtils.IsItemEquipable(None, item_params):
                    self.ActiveGadjetSet.GadjetID = itemID
                    self.ActiveGadjetSet.GadjetType = item_type
            if item_class == ItemsCatalog.WEAPON:
                gun_type = item_params['GunType']
                gun_priority = ItemsUtils.GetWeaponPriority(gun_type)
                unequiping_item_type = self.ActiveItemType
                self.ActiveItemID = itemID
                self.ActiveItemType = item_type
                if gun_priority == ItemsCatalog.SECONDARY:
                    self.ActiveWeaponSet.SecondarySlotID = itemID
                    self.ActiveWeaponSet.SecondarySlotType = item_type
                    self.ActiveWeaponSet.SecondarySlotTintID = ItemsUtils.getTintID(item)
                else:
                    self.ActiveWeaponSet.PrimarySlotID = itemID
                    self.ActiveWeaponSet.PrimarySlotType = item_type
                    print 'cl self.ActiveWeaponSet.PrimarySlotTintID ', self.ActiveWeaponSet.PrimarySlotTintID
                    self.ActiveWeaponSet.PrimarySlotTintID = ItemsUtils.getTintID(item)
                    print 'cl set self.ActiveWeaponSet.PrimarySlotTintID ', self.ActiveWeaponSet.PrimarySlotTintID
                self.SetEquippedWeaponParams(itemID, item_type, item)
            put_on_duration = Durations.GetPutOnDuration(self, item_type, unequiping_item_type)
            self.DrawItemPutOn(put_on_duration, item_type, unequiping_item_type)
            self.cell.putOnItem(itemID, slot_number)
            self.systemChatline(str(self.ActiveItemType) + ' ' + str(self.ActiveWeaponSet.PrimarySlotType))
            return put_on_duration
        else:
            self.systemChatline(str(self.ActiveItemType) + ' ' + str(self.ActiveWeaponSet.PrimarySlotType))
            return

    def putOnItemStep2(self, item):
        if not self.canEquip():
            return
        elif item:
            item_type = item['complexItemType']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            itemID = item['complexItemID']
            if ItemsUtils.GetComplexItemByID(self, itemID) is None:
                return
            unequiping_item_type = 0
            if item_class == ItemsCatalog.CLOTH:
                for types in item_params['ArmorType']:
                    print 'found ID', types, ItemsCatalog.cloth_dict[types][0], self.ActiveArmorSet[ItemsCatalog.cloth_dict[types][0]]
                    what_putted_off = ItemsUtils.GetComplexItemByID(self, self.ActiveArmorSet[ItemsCatalog.cloth_dict[types][0]])
                    self.onPutOffItem(what_putted_off)
                    self.ActiveArmorSet[ItemsCatalog.cloth_dict[types][0]] = itemID
                    self.ActiveArmorSet[ItemsCatalog.cloth_dict[types][1]] = item_type

                put_on_duration = 0.0
            elif item_class == ItemsCatalog.ARTIFACT:
                put_on_duration = 0.0
            else:
                return 0.0
            self.DrawItemPutOn(put_on_duration, item_type, unequiping_item_type)
            self.cell.putOnItemStep2(itemID)
            return put_on_duration
        else:
            return

    def onPutOffItem(self, item):
        self.systemChatline('onPutOffItem')
        if not self.canEquip():
            return
        if item:
            item_type = item['complexItemType']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            itemID = item['complexItemID']
            if item_class == ItemsCatalog.CLOTH:
                for types in item_params['ArmorType']:
                    self.ActiveArmorSet[ItemsCatalog.cloth_dict[types][0]] = 0
                    self.ActiveArmorSet[ItemsCatalog.cloth_dict[types][1]] = 0

            if item_class == ItemsCatalog.GADGET:
                self.ActiveGadjetSet.GadjetID = 0
                self.ActiveGadjetSet.GadjetType = 0
            if item_class == ItemsCatalog.WEAPON:
                gun_type = item_params['GunType']
                gun_priority = ItemsUtils.GetWeaponPriority(gun_type)
                if gun_priority == ItemsCatalog.SECONDARY:
                    if self.ActiveWeaponSet.SecondarySlotID == self.ActiveItemID:
                        self.ActiveItemID = 0
                        self.ActiveItemType = 0
                    self.ActiveWeaponSet.SecondarySlotID = 0
                    self.ActiveWeaponSet.SecondarySlotType = 0
                else:
                    if self.ActiveWeaponSet.PrimarySlotID == self.ActiveItemID:
                        self.ActiveItemID = 0
                        self.ActiveItemType = 0
                    self.ActiveWeaponSet.PrimarySlotID = 0
                    self.ActiveWeaponSet.PrimarySlotType = 0
                ItemsUtils.ClearActiveWeaponUpgradesTypes(self, item)
            if item_class == ItemsCatalog.EXPLOSION:
                if self.ActiveGrenadeID == itemID:
                    self.ActiveGrenadeID = 0
                    self.ActiveGrenadeType = 0
            self.SetAvatarModel()
            self.NeedToUpdateInventory()
            self.cell.putOffItem(itemID)

    def hasArmor(self):
        if self.ActiveArmorSet.ArmorID > 0:
            return True
        else:
            return False

    def hasBackpack(self):
        if self.ActiveArmorSet.BackPackID > 0:
            return True
        else:
            return False

    def onUseItem(self, item):
        error_level = ItemsUtils.FAIL_NO
        if not self.canUse():
            error_level = ItemsUtils.FAIL_OTHER_ACTION
            return (error_level, None)
        else:
            if item:
                item_type = item['complexItemType']
                itemID = item['complexItemID']
                item_class = ItemsCatalog.GetItemClass(item_type)
                item_params = ItemsCatalog.GetItemParam(item_type)
                duration = 0.0
                if 'isBlackBox' in item_params:
                    self.cell.useItem(itemID)
                    return (ItemsUtils.FAIL_NO, None)
                if item_class == ItemsCatalog.BUFF:
                    if ItemsCatalog.EFFECTS_START_USERFIRE in item_params['Effect'].keys():
                        firePos = self.checkPosibleUserFire()
                        if firePos:
                            self.physics.velocity = (0, 0, 0)
                            self.cell.startCreateUserFire(firePos, itemID, item_type)
                        return (ItemsUtils.FAIL_NO, None)
                    if ItemsCatalog.EFFECTS_START_FIREWORKS in item_params['Effect'].keys():
                        self.cell.startCreateFireWork(itemID, item_type)
                        return (ItemsUtils.FAIL_NO, None)
                    if ItemsCatalog.EFFECTS_HEAL in item_params['Effect'].keys():
                        self.cell.useItem(itemID)
                        duration = Durations.GetItemUseDuration(self, item_type)
                    if ItemsCatalog.EFFECTS_REPAIR in item_params['Effect'].keys():
                        self.ChooseRepairItem(itemID)
                        duration = Durations.GetItemUseDuration(self, item_type)
                    if ItemsCatalog.EFFECTS_RECIPE in item_params['Effect'].keys():
                        if item_params['Effect'][ItemsCatalog.EFFECTS_RECIPE] not in self.KnowingRecipes:
                            self.cell.useItem(itemID)
                            duration = Durations.GetItemUseDuration(self, item_type)
                        else:
                            error_level = ItemsUtils.FAIL_KNOWN_RECIPE
                    if ItemsCatalog.EFFECTS_EAT in item_params['Effect'].keys():
                        self.cell.useItem(itemID)
                        duration = Durations.GetItemUseDuration(self, item_type)
                    self.DrawUseItem(item_type, duration)
                if item_class == ItemsCatalog.LOOT:
                    if ItemsCatalog.EFFECTS_EAT in item_params['Effect'].keys():
                        self.cell.useItem(itemID)
                        duration = Durations.GetItemUseDuration(self, item_type)
                        self.DrawUseItem(item_type, duration)
                if item_class == ItemsCatalog.GADGET:
                    item_param = ItemsCatalog.GetItemParam(item_type)
                    gadjet_action = item_param['Action']
                    if gadjet_action == ItemsCatalog.GADJET_ACTION_ART_GRAB:
                        self.startArtifactExtraction(item_param, item)
            else:
                error_level = ItemsUtils.FAIL_ITEM_STRUCTURE
            return (error_level, duration)

    def StartItemRepair(self, kit_id, item_id):
        self.cell.onItemRepair(item_id, kit_id)

    def GetFiryingItemDamage(self):
        if not ItemsUtils.CheckEquippedItemValidityClient(self):
            return
        return ItemsUtils.GetItemDamage(self)

    def SimpleGetFiryingItemDamage(self):
        complexItemParams = ItemsCatalog.GetItemParam(self.ActiveItemType)
        ammo_params = ItemsCatalog.GetItemParam(self.ActiveItemAmmoType)
        weaponMainDamage = deepcopy(complexItemParams['DamageMain'])
        weaponAdditionalDamage = deepcopy(complexItemParams['DamageAdditional'])
        ammoMainDamage = deepcopy(ammo_params['DamageMain'])
        ammoAdditionalDamage = deepcopy(ammo_params['DamageAdditional'])
        penetration_summary = ammo_params['Penetration'] + complexItemParams['Penetration']
        for keys in ammoMainDamage.keys():
            if weaponMainDamage.has_key(keys):
                weaponMainDamage[keys][0] += ammoMainDamage[keys][0]
                weaponMainDamage[keys][1] += ammoMainDamage[keys][1]
            else:
                weaponMainDamage[keys] = ammoMainDamage[keys]

        for keys in ammoAdditionalDamage.keys():
            if weaponAdditionalDamage.has_key(keys):
                weaponAdditionalDamage[keys][0] += ammoAdditionalDamage[keys][0]
                weaponAdditionalDamage[keys][1] += ammoAdditionalDamage[keys][1]
            else:
                weaponAdditionalDamage[keys] = ammoAdditionalDamage[keys]

        return dict(penetration=penetration_summary, mainDamage=weaponMainDamage, additionalDamage=weaponAdditionalDamage)

    def GetArmor(self, zone_id):
        return ItemsUtils.GetArmor(self, zone_id, False)

    def onUseItemOnTarget(self, target_id, itemID):
        if not self.canUse():
            return
        item = ItemsUtils.GetComplexItemByID(self, itemID)
        if item:
            equippingitemType = item['complexItemType']
            item_class = ItemsCatalog.GetItemClass(equippingitemType)
            duration = Durations.GetItemUseDuration(self, equippingitemType)
            if item_class == ItemsCatalog.BUFF:
                self.cell.useItemOnTarget(target_id, itemID)
                self.DrawUseItemOnTarget(equippingitemType, duration)
            return duration

    def InitWeaponProperty(self, item, complexItemParams = None):
        if item == None:
            current_item_params['ItemID'] = 0
            current_item_params['ItemType'] = 0
            current_item_params['Accuracy'] = 0
            self.ActiveItemAmmo = 0
            self.ActiveItemAmmoType = 0
            return
        else:
            item_type = item['complexItemType']
            item_id = item['complexItemID']
            if complexItemParams == None:
                complexItemParams = ItemsCatalog.GetItemParam(item_type)
            if item and complexItemParams.get('AmmoCapacity') and complexItemParams.get('AmmoType'):
                self.ActiveItemAmmo = complexItemParams['AmmoCapacity']
                self.ActiveItemAmmoType = ItemsUtils.GetAmmoByType(self, complexItemParams['AmmoType']).complexItemType
            if self.ActiveItemAmmoType:
                ammo_params = ItemsCatalog.GetItemParam(self.ActiveItemAmmoType)
            else:
                ammo_params = None
            current_item_params = {}
            current_item_params['ItemID'] = item_id
            current_item_params['ItemType'] = item_type
            current_item_params['Accuracy'] = complexItemParams['Accuracy']
            current_item_params['Range'] = complexItemParams['Range']
            current_item_params['RateOfFire'] = complexItemParams['RateOfFire']
            current_item_params['SFXParam'] = ItemsUtils.GetFiryingItemSFXParams(self)
            current_item_params['FireType'] = complexItemParams['FireType']
            current_item_params['AccuracyBorder'] = complexItemParams['AccuracyBorder']
            current_item_params['Kickback'] = complexItemParams['Kickback']
            current_item_params['AccuracyRecoil'] = complexItemParams['AccuracyRecoil']
            current_item_params['MoveAccuracyLost'] = complexItemParams['MoveAccuracyLost']
            current_item_params['GunType'] = complexItemParams['GunType']
            current_item_params['SkillLevel'] = complexItemParams['SkillLevel']
            current_item_params['DamageRangeMods'] = complexItemParams.get('DamageDistanceMod', (1.0, 1.0, 1.0, 1.0))
            current_item_params['AccStandModsKeys'] = complexItemParams['AccStandMods'].keys()
            current_item_params['AccStandModsValues'] = complexItemParams['AccStandMods'].values()
            current_item_params['DamageMainKeys'] = complexItemParams['DamageMain'].keys()
            current_item_params['DamageMainValues'] = complexItemParams['DamageMain'].values()
            current_item_params['DamageAdditionalKeys'] = complexItemParams['DamageAdditional'].keys()
            current_item_params['DamageAdditionalValues'] = complexItemParams['DamageAdditional'].values()
            if ammo_params != None:
                current_item_params['Accuracy'] += ammo_params.get('Accuracy', 0)
                current_item_params['Penetration'] = ammo_params['Penetration'] + complexItemParams['Penetration']
                current_item_params['NumShots'] = ammo_params['NumShots']
                current_item_params['AmmoDamageMainKeys'] = ammo_params['DamageMain'].keys()
                current_item_params['AmmoDamageMainValues'] = ammo_params['DamageMain'].values()
                current_item_params['AmmoDamageAdditionalKeys'] = ammo_params['DamageAdditional'].keys()
                current_item_params['AmmoDamageAdditionalValues'] = ammo_params['DamageAdditional'].values()
            else:
                current_item_params['Penetration'] = 0
                current_item_params['NumShots'] = 0
                current_item_params['AmmoDamageMainKeys'] = []
                current_item_params['AmmoDamageMainValues'] = []
                current_item_params['AmmoDamageAdditionalKeys'] = []
                current_item_params['AmmoDamageAdditionalValues'] = []
            self.CurrentWeaponParam = current_item_params
            return

    def SetEquippedWeaponParams(self, itemID, equippedType, item):
        self.systemChatline('SetEquippedWeaponParams: ' + str(itemID) + ' ' + str(equippedType))
        self.ActiveItemID = itemID
        self.ActiveItemType = equippedType
        self.InitWeaponProperty(item)
        ItemsUtils.SetActiveWeaponUpgradesTypes(self, item)
        self.InitWeaponAmmo()

    def onEquipItem(self, item):
        self.systemChatline('onEquipItem')
        if not self.canEquip():
            return None
        else:
            unequippedType, equippedType, item_class, equippingGunType, unequippingGunType = (0, 0, None, None, None)
            if item:
                itemID = item['complexItemID']
                if self.ActiveItemID == itemID:
                    return None
                equippedType = item['complexItemType']
                item_class = ItemsCatalog.GetItemClass(equippedType)
                equipping_item_param = ItemsCatalog.GetItemParam(equippedType)
                if item_class == ItemsCatalog.WEAPON:
                    equippingGunType = equipping_item_param['GunType']
                    if self.ActiveItemID:
                        unequippedType = self.ActiveItemType
                        unequippedItemParams = ItemsCatalog.GetItemParam(unequippedType)
                        unequippingGunType = unequippedItemParams['GunType']
                    unequipping_time = Durations.GetEquipDuration(self, unequippingGunType)
                    equipping_time = Durations.GetEquipDuration(self, equippingGunType)
                    self.SetEquippedWeaponParams(itemID, equippedType, item)
                    self.DrawUnequipItem(unequippedType, equippedType, unequipping_time, equipping_time)
                elif item_class == ItemsCatalog.EXPLOSION:
                    equippingGunType = ItemsCatalog.GRENADE
                    self.ActiveGrenadeID = itemID
                    self.ActiveGrenadeType = equippedType
                    self.drawEquipGrenade(self.ActiveItemType)
                    equipping_time = Durations.GetEquipDuration(self, equippingGunType)
                    unequipping_time = 0
                else:
                    return False
                self.cell.equipItem(itemID)
            else:
                unequippedType = self.ActiveItemType
                unequippedItemParams = ItemsCatalog.GetItemParam(unequippedType)
                unequippingGunType = unequippedItemParams['GunType']
                unequipping_time = Durations.GetEquipDuration(self, unequippingGunType)
                equipping_time = 0
                self.ActiveItemID = 0
                self.ActiveItemType = 0
                self.DrawUnequipItem(unequippedType, equippedType, unequipping_time, equipping_time)
                self.cell.equipItem(0)
            return equipping_time + unequipping_time

    def onInFormWeponJammed(self):
        if not self.canInformJamm():
            return
        complexItemParams = ItemsCatalog.GetItemParam(self.ActiveItemType)
        weapon_load_type = complexItemParams['LoadType']
        reload_type = ItemsUtils.GetItemReloadType(weapon_load_type, False)
        return reload_type

    def onComplexRepair(self, traderID):
        items_to_repair = self.GetEquippedItemsToRepair()
        for item in items_to_repair:
            self.NPCRepair(traderID, item['complexItemID'])

    def GetEquippedItemsToRepair(self):

        def FilterRepairItems(item):
            return ItemsUtils.CanItemBeRepaired(self, item) == None

        items_to_repair = self.GetEquippedItemsList()
        items_to_repair = filter(FilterRepairItems, items_to_repair)
        return items_to_repair

    def GetEquipedItemsRepairCost(self, repairman_entity):
        items_to_repair = self.GetEquippedItemsToRepair()
        repair_cost = 0
        for item in items_to_repair:
            end_cost, margin = ItemsUtils.GetRepairCost(item, self, repairman_entity)
            repair_cost += end_cost

        return repair_cost

    def onUnJammWeapon(self):
        if not self.canUnjam():
            return
        complexItemParams = ItemsCatalog.GetItemParam(self.ActiveItemType)
        weapon_load_type = complexItemParams['LoadType']
        reload_type = ItemsUtils.GetItemReloadType(weapon_load_type, False)
        return reload_type

    def SetActiveWeaponAmmo(self, ammo_num):
        pass

    def GetReloadParams(self, item_type, loaded_ammo_type):
        complexItemParams = ItemsCatalog.GetItemParam(item_type)
        weapon_load_type = complexItemParams['LoadType']
        weapon_type = complexItemParams['GunType']
        short_reload, add_catridge = ItemsUtils.CanShortReload(self.CurrentWeaponAmmo, complexItemParams)
        reload_type = ItemsUtils.GetItemReloadType(weapon_load_type, short_reload)
        if not loaded_ammo_type:
            ammo_item = ItemsUtils.GetAmmoByType(self, complexItemParams['AmmoType'])
            if ammo_item:
                loaded_ammo_type = ammo_item['complexItemType']
            else:
                return
        num_ammo_we_have = ItemsUtils.GetItemQuanity(self.CarryingItems, loaded_ammo_type)
        if num_ammo_we_have == 0:
            ammo_cart = ItemsUtils.GetAmmoByType(self, complexItemParams['AmmoType'])
            if ammo_cart == None:
                return
            num_ammo_we_have = ItemsUtils.GetItemQuanity(self.CarryingItems, ammo_cart['complexItemType'])
            if num_ammo_we_have == 0:
                return
        weapon_capacity = ItemsUtils.GetWeaponAmmoCapacity(self, complexItemParams)
        if num_ammo_we_have >= weapon_capacity:
            num_loaded_ammo = weapon_capacity - self.CurrentWeaponAmmo
        else:
            num_loaded_ammo = num_ammo_we_have - self.CurrentWeaponAmmo
        self.CurrentWeaponAmmo = 0
        item = ItemsUtils.GetComplexItemByType(self, item_type)
        self.SetEquippedWeaponParams(item['complexItemID'], item_type, item)
        return (reload_type, num_loaded_ammo, item_type)

    def canReload(self):
        if self.ActiveItemID:
            if self.ActiveItemType:
                itemParams = ItemsCatalog.GetItemParam(self.ActiveItemType)
                weapon_ammo_capacity = ItemsUtils.GetWeaponAmmoCapacity(self, itemParams)
                ammo_cart_number = ItemsUtils.GetAmmoByType(self, itemParams['AmmoType'])
                if ammo_cart_number <= 0:
                    CanReload = 1
                elif self.CurrentWeaponAmmo < weapon_ammo_capacity:
                    CanReload = 0
                else:
                    CanReload = 2
            else:
                CanReload = 3
        else:
            CanReload = 3
        return CanReload

    def onReload(self):
        return self.GetReloadParams(self.ActiveItemType, self.ActiveItemAmmoType)

    def ChangeActiveItemAmmoType(self):
        if ItemsUtils.CheckEquippedItemValidityClient(self):
            weapon_params = ItemsCatalog.GetItemParam(self.ActiveItemType)
            unique_ammo_list = ItemsUtils.GetUniqueAmmosListByType(self, weapon_params['AmmoType'])
            new_ammo_id = 0
            if len(unique_ammo_list) > 1:
                for position, item in enumerate(unique_ammo_list):
                    if item['complexItemType'] == self.ActiveItemAmmoType:
                        if item == unique_ammo_list[-1]:
                            new_ammo_id = unique_ammo_list[0]['complexItemID']
                        else:
                            new_ammo_id = unique_ammo_list[position + 1]['complexItemID']
                        break
                else:
                    new_ammo_id = unique_ammo_list[0]['complexItemID']

            elif len(unique_ammo_list) == 1 and unique_ammo_list[0]['complexItemType'] != self.ActiveItemAmmoType:
                new_ammo_id = unique_ammo_list[0]['complexItemID']
            if new_ammo_id:
                self.LoadAmmoInCurrentWeapon(new_ammo_id)

    def canLoadAmmo(self, id):
        result = ItemsUtils.CanLoadAmmo(self, id)
        if result != ItemsUtils.FAIL_NO:
            self.ReportCodedMessage(result)
            return False
        return True

    def onLoadAmmoInCurrentWeapon(self, id):
        ammoItem = ItemsUtils.GetComplexItemByID(self, id)
        ammo_type = ammoItem['complexItemType']
        item_type = self.ActiveItemType
        self.CurrentWeaponAmmo = 0
        self.cell.LoadAmmoInCurrentWeapon(id)
        return self.GetReloadParams(item_type, ammo_type)

    def ChangeItemSlot(self, old, new):
        self.cell.ChangeItemSlot(old, new)

    def SellItem(self, trader_id, item):
        itemID = item['complexItemID']
        self.SearchInEquipsAndSetToZero(itemID)
        self.cell.SellItemToTrader(trader_id, itemID)

    def BuyItem(self, trader_id, item, forGold):
        self.cell.BuyItemFromTrader(trader_id, item['complexItemType'], forGold)

    def GetActiveWeaponAccuracyDiff(self):
        if not ItemsUtils.CheckEquippedItemValidityClient(self):
            return ([-3000,
              1200,
              600,
              3500,
              3500],
             0,
             0,
             0)
        item_type = self.ActiveItemType
        itemParam = ItemsCatalog.GetItemParam(item_type)
        return ([itemParam['AccuracyBorder'],
          itemParam['Kickback'],
          itemParam['AccuracyRecoil'],
          itemParam['MoveAccuracyLost'],
          itemParam['MoveAccuracyLost']],
         itemParam['GunType'],
         itemParam['SkillLevel'],
         self.ActiveItemType)

    def onAttachItem(self, mother_item_id, attaching_item_id):
        mother_item = ItemsUtils.GetComplexItemByID(self, mother_item_id)
        attaching_item = ItemsUtils.GetComplexItemByID(self, attaching_item_id)
        ItemsUtils.AttachItem(self, mother_item, attaching_item)
        self.SetEquippedWeaponParams(mother_item['complexItemID'], mother_item['complexItemType'], mother_item)
        self.UpdateInventory()
        return Durations.GetModificationDuration(self)

    def onDatachItem(self, mother_item_id, detaching_id):
        mother_item = ItemsUtils.GetComplexItemByID(self, mother_item_id)
        detaching_item = ItemsUtils.GetSubItemByID(mother_item, detaching_id)
        ItemsUtils.DetachItem(self, mother_item, detaching_item)
        self.SetEquippedWeaponParams(mother_item['complexItemID'], mother_item['complexItemType'], mother_item)
        self.UpdateInventory()
        return Durations.GetModificationDuration(self)

    def ReportFail(self, fail_code):
        self.ReportCodedMessage(fail_code)

    def ReportCodedMessage(self, code):
        pass

    def onGetMaxWeight(self):
        return ItemsUtils.onGetMaxWeight(self)

    def GetEquippedItemsList(self):
        equip_list = ItemsUtils.GetEquipListIDs(self)
        equipped_item_list = []
        for id in equip_list:
            item = ItemsUtils.GetComplexItemByID(self, id)
            if item:
                equipped_item_list.append(item)

        return equipped_item_list

    def GetTradingItemList(self):
        if self.ExchangeProperties.fOffer:
            trading_list = self.ExchangeProperties.ItemsToExchange
        else:
            trading_list = []
            for trade_item in self.PCTradeItems:
                item = ItemsUtils.GetComplexItemByID(self, trade_item['complexItemID'])
                if item:
                    trading_list.append(item)

        return trading_list

    def BeginSpare(self, item, quantity):
        self.cell.DivideItem(item['complexItemID'], quantity)

    def ExchangeAppruved(self):
        Inventory.ShowExchange(self)

    def debug_print_item_list(self):
        for item in self.CarryingItems:
            print 'Item ID:', item['complexItemID'], ' Item Type:', item['complexItemType']
            for subitem in item['itemList']:
                print 'SubItem ID:', subitem['itemID'], ' SubItem Type:', subitem['itemType']

    def ExchangeEnded(self):
        Inventory.ExchangeEnded(self)

    def set_ExchangeProperties(self, old_value):

        def redraw_player_table(enteredTrap, handle):
            if enteredTrap:
                BigWorld.player().NeedToUpdateExchangeInterface()

        BigWorld.addPot(self.matrix, 12.0, redraw_player_table)

    def GetExchangeOpponentEntity(self):
        try:
            opponent_entity = BigWorld.entities[self.ExchangeProperties.TradingEntity]
            return opponent_entity
        except:
            return None

        return None

    def NeedToUpdateExchangeInterface(self):
        opponent_entity = self.GetExchangeOpponentEntity()
        if opponent_entity:
            self.UpdateExchange(opponent_entity)
            self.NeedToUpdateInventory()

    def set_StoredItems(self, old_value):
        pass

    def set_StoredItemsInShop(self, old_value):
        pass

    def checkMsgFromShop(self):
        if not self.isInWorld:
            return
        if self.msgFromShop:
            for type_msg, msg in self.msgFromShop:
                if type_msg:
                    gui_jokes.askUserOk(u'', colorCodes.tf3_regular_text_color + msg)
                else:
                    self.systemChatline(msg)

        self.msgFromShop = []

    def showShopMessageExpand(self, type_msg, index_msg, data):
        print 'showShopMessageExpand', type_msg, index_msg, data
        formatdata = dict(itemname='', bank='', price='', buyerName='')
        formatdata.update(data)
        msg = ShopResponses.msg[index_msg]
        typeID = data['complexItemType']
        itemname = '[???]'
        if typeID:
            itemname = ItemsUtils.GetItemName(typeID, fGetShortName=True, tintItem=data)
        bank = _NPCs.names_by_npcName.get(data['BankName'], '???')
        formatdata['itemname'] = itemname
        formatdata['bank'] = bank
        formatdata['buyerName'] = formatdata['buyerName'].decode('utf8')
        msg = msg.format(**formatdata)
        if not self.isInWorld:
            if not self.msgFromShop:
                self.msgFromShop = []
            self.msgFromShop.append((type_msg, msg))
            print 'showShopMessageExpand add msgFromShop'
            return
        if type_msg:
            gui_jokes.askUserOk(u'', colorCodes.tf3_regular_text_color + msg)
        else:
            self.systemChatline(msg)

    def showShopMessage(self, type_msg, index_msg):
        """
        type_msg : 0 -chat, 1 - popup
        """
        print 'showShopMessage', type_msg, index_msg
        msg = ShopResponses.msg[index_msg]
        if not self.isInWorld:
            if not self.msgFromShop:
                self.msgFromShop = []
            self.msgFromShop.append((type_msg, msg))
            print 'showShopMessage add msgFromShop'
            return
        if type_msg:
            gui_jokes.askUserOk(u'', colorCodes.tf3_regular_text_color + msg)
        else:
            self.systemChatline(msg)

    def shopContextMenuEvent(self, interface_id, event_id, caption, event):
        if interface_id != BWPersonality.GUICore.GUI_ID_ITEMCACHE:
            return
        if event == BWPersonality.soGUI.soContextMenuComponent.EVENT_SELECT:
            if not event_id:
                return
            command, complexItemID = event_id
            if not self.cacheObjectID:
                return
            npc = BigWorld.entity(self.cacheObjectID)
            if not npc:
                return
            if not hasattr(npc, 'npcName'):
                return
            BankName = npc.npcName
            item = ItemsUtils.GetComplexItemByIDFromStoredItems(self, BankName, complexItemID)
            if not item:
                return
            item_type = item['complexItemType']
            if command == 'sale':
                BWPersonality.GUICore.showStartSale(True, item, BankName)
            if command == 'cancel_sale':

                def cancel_sale(event):
                    if event == gui_jokes.askUserYesNo.YES:
                        self.cell.cancelSaleShop(complexItemID, BankName)

                itemName = ItemsUtils.GetItemName(item_type, fGetShortName=True, tintItem=item)
                ask = lc('ItemHolder.ask_cancel_sale').format(itemName=itemName)
                gui_jokes.askUserYesNo(u'', colorCodes.tf3_regular_text_color + ask, cancel_sale)

    def set_ItemsWeight(self, old_value):
        pass

    def onWeaponChanged(self):
        pass

    def fromShopError(self, error_code):
        print 'fromShopError', error_code

    def itemToShop(self, complexItem, price, BankName):
        self.cell.itemToShop(complexItem, price, BankName)

    def buyItemFromShop(self, sellerAvatarName, complexItemID, price, BankName):
        self.cell.buyItemFromShop(sellerAvatarName, complexItemID, price, BankName)

    def getShopCatalogFiltered(self, sortFlag, forward, page_start, page_len, tags):
        self.cell.getShopCatalogFiltered(sortFlag, forward, page_start, page_len, tags)

    def shopCatalogResponseFiltered(self, data, page_start, last_index_item, all_index_item):
        BWPersonality.GUICore.setBulletinBoardShopData({'data': data,
         'page_start': page_start,
         'last_index_item': last_index_item,
         'all_index_item': all_index_item})

    def getShopCatalogAll(self, tags):
        self.cell.getShopAllCatalog(tags)

    def shopCatalogAllResponse(self, data):
        print 'shopCatalogAllResponse', len(data)

    def StoreItem(self, entity, item):
        self.cell.StoreItem(entity, item['complexItemID'])

    def RestoreItem(self, entity, item):
        item_id = item['complexItemID']
        self.cell.RestoreItem(entity, item_id)

    def GetReceiptList(self):
        return_list = []
        for recipe in self.KnowingRecipes:
            if recipe not in return_list:
                return_list.append(recipe)

        return return_list

    def startCraft(self, receipt_id, craftItemList):
        if self.canUse():
            self.restrictShoot(self.ShootRestictions.CRAFTING)
            self.cell.StartCraft(receipt_id, craftItemList)

    def startNPCBarter(self, trader_id, numSelectedEntry, items_ids_list):
        self.cell.StartNPCBarter(trader_id, numSelectedEntry, items_ids_list)

    def NPCRepair(self, TraderID, item_id):
        item = ItemsUtils.GetComplexItemByID(self, item_id)
        if item:
            err_code = ItemsUtils.CanItemBeRepaired(self, item)
            if err_code == None:
                self.cell.StartNPCRepair(item_id, TraderID)
            else:
                self.ReportFail(err_code)
        return

    def set_KnowingRecipes(self, old):
        pass

    def set_ActiveWeaponSet(self, oldType = None):
        pass

    def set_ActiveGadjetSet(self, oldType = None):
        pass

    def onCraftEnded(self):
        self.restrictShoot(self.ShootRestictions.CRAFTING, False)
        self.UpgradeCraft()

    def GetReceiptPartsList(self, number):
        recipe_param = ItemsCatalog.GetItemParam(number)
        return recipe_param['NeededResourcess']

    def onItemAdded(self, type, number, id):
        pass

    def onItemLost(self, type, number, id):
        pass

    def GetItemFromContainer(self, cacheObjectID, item):
        item_id = item['complexItemID']
        self.cell.GetItemFromHolderClient(cacheObjectID, item_id)

    def PutItemToContainer(self, cacheObjectID, data):
        try:
            container = BigWorld.entities[cacheObjectID]
        except:
            return

        item = data
        if not item:
            return
        if ItemsUtils.IsItemMoveable(item):
            return
        container.cell.GetItemFromHolderClient(self.id, data['complexItemID'])

    def PutItemToWarehouse(self, trader_id, item):
        BigWorld.entities[trader_id].cell.addItem(self.clanID, item)

    def GetItemFromWarehouse(self, trader_id, item):
        BigWorld.entities[trader_id].cell.removeItem(self.clanID, item)