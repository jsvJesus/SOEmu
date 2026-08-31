# Embedded file name: scripts/common/CharacterUtils.py
from Localization import lc
from Perks import PerkList
from Items import ItemsCatalog
import ItemsUtils
import math
import random
from FiringDefs import FiringDefs

def GetMaxStamina(entity):
    return GetStatistic(entity, 'Endurance') * CharacterConst.STAMINA_ENDURANCE_MULTIPLYER + CharacterConst.STAMINA_BASE


def GetMedicineMod(entity, heal_other):
    koeff = GetOtherSkillValue(entity, 'Medicine') / CharacterConst.MEDECINE_SKILL_KOEFF
    if heal_other:
        perk_number = GetPerkNumber(entity, PerkList.BATTLE_DOCTOR)
        if perk_number:
            koeff += PerkList.BATTLE_DOCTOR['Value']
    else:
        perk_number = GetPerkNumber(entity, PerkList.MEDICINE_ADDON)
        if perk_number:
            koeff += PerkList.MEDICINE_ADDON['Value']
    return CharacterConst.KOEFF_BASE_UNIT + koeff


def GetSpotKoeff(entity):
    koeff = float(CharacterConst.KOEFF_BASE_UNIT + GetStatistic(entity, 'Perception') / CharacterConst.CAMOUFLAGE_SKILL_KOEFF)
    return CharacterConst.MAX_LINE_OF_SIGHT * float(GetSurvivalSkillValue(entity, 'Spotting') / float(CharacterConst.MAX_SKILL_VALUE_SUPER)) * koeff
    return GetSurvivalSkillValue(entity, 'Spotting') * (CharacterConst.KOEFF_BASE_UNIT + GetStatistic(entity, 'Perception') / CharacterConst.CAMOUFLAGE_SKILL_KOEFF)


def GetCamouflageKoeff(entity):
    gun_type = ItemsUtils.GetEquippedItemType(entity)
    koeff = ItemsCatalog.VISIBILITY_WEAPON_KOEFF[gun_type]
    if gun_type in [ItemsCatalog.ROCKET_LAUNCHER, ItemsCatalog.GRENADE_LAUNCHER, ItemsCatalog.MACHINE_GUN]:
        perk_number = GetPerkNumber(entity, PerkList.VISIBILITY_REDUCE_HEAVY_WEAPON)
        if perk_number:
            koeff += PerkList.VISIBILITY_REDUCE_HEAVY_WEAPON['Value']
    if entity.IsEncumbered():
        koeff -= CharacterConst.ENCUMBRANCE_CAMOUFLAGE_LOSS
        perk_number = GetPerkNumber(entity, PerkList.VISIBILITY_REDUCE_HEAVY_LOAD)
        if perk_number:
            koeff += PerkList.VISIBILITY_REDUCE_HEAVY_LOAD['Value']
    koeff += CharacterConst.KOEFF_BASE_UNIT + GetStatistic(entity, 'Agility') / CharacterConst.CAMOUFLAGE_SKILL_KOEFF
    return CharacterConst.MAX_CAMOUFLAGE_DISTANCE * float(GetSurvivalSkillValue(entity, 'Camouflage') / float(CharacterConst.MAX_SKILL_VALUE_SUPER)) * float(koeff)
    return GetSurvivalSkillValue(entity, 'Camouflage') * (CharacterConst.KOEFF_BASE_UNIT + GetStatistic(entity, 'Agility') / CharacterConst.CAMOUFLAGE_SKILL_KOEFF)


def GetAnomalySpotting(entity):
    return CharacterConst.MAX_ANOMALY_LINE_OF_SIGHT * float(GetSurvivalSkillValue(entity, 'AnomalySpotting') / float(CharacterConst.MAX_SKILL_VALUE_SUPER))
    return GetSurvivalSkillValue(entity, 'AnomalySpotting') * (CharacterConst.KOEFF_BASE_UNIT + GetStatistic(entity, 'Perception') / CharacterConst.CAMOUFLAGE_SKILL_KOEFF)


def GetDodgeChance(entity):
    return 0.0


def GetSkillStatus():
    pass


def GetLevelUpExp(level):
    if level <= 8:
        return CharacterConst.LEVEL_UP_BASE_EXP * math.exp(level - 1)
    elif level <= 19:
        return 1200000 + 1000000 * (level - 8)
    else:
        return 12200000 + 5000000 * (level - 19)


def GetSummaryLevel(self):
    return self.CharacterCombatLevel + self.CharacterSurvivalLevel + self.CharacterOtherLevel


def GetCurrentWeaponProfiency(skill):
    if skill < CharacterConst.SKILL_WEAPON_PROFESSIONAL:
        return ItemsCatalog.SKILL_LEVEL_BASIC
    elif skill < CharacterConst.SKILL_WEAPON_EXPERT:
        return ItemsCatalog.SKILL_LEVEL_ADVANCED
    else:
        return ItemsCatalog.SKILL_LEVEL_PROFESSIONAL


def getReloadTimeModifyer(entity, gun_type, item_type):
    time_mod = CharacterConst.KOEFF_BASE_UNIT
    if gun_type in [ItemsCatalog.PISTOL, ItemsCatalog.REVOLVER]:
        if GetPerkNumber(entity, PerkList.LIGHT_WEAPON_RELOAD_TIME_REDUCE):
            time_mod *= PerkList.LIGHT_WEAPON_RELOAD_TIME_REDUCE['Value']
    if gun_type in [ItemsCatalog.ASSAULT_RIFLE, ItemsCatalog.SUB_MACHINE_GUN]:
        if GetPerkNumber(entity, PerkList.ASSAULT_RIFLES_RELOAD_TIME_REDUCE):
            time_mod *= PerkList.ASSAULT_RIFLES_RELOAD_TIME_REDUCE['Value']
    if gun_type in [ItemsCatalog.ROCKET_LAUNCHER, ItemsCatalog.GRENADE_LAUNCHER, ItemsCatalog.MACHINE_GUN]:
        if GetPerkNumber(entity, PerkList.HEAVY_WEAPON_RELOAD_TIME_REDUCE):
            time_mod *= PerkList.HEAVY_WEAPON_RELOAD_TIME_REDUCE['Value']
    if gun_type in [ItemsCatalog.SNIPER_RIFLE, ItemsCatalog.RIFLE, ItemsCatalog.SHOTGUN]:
        if GetPerkNumber(entity, PerkList.RIFLES_RELOAD_TIME_REDUCE):
            time_mod *= PerkList.RIFLES_RELOAD_TIME_REDUCE['Value']
    adaptation = GetWeaponAdaptivity(entity, item_type)
    if adaptation > CharacterConst.WEAPON_ADAPTIVITY_LEVEL_2:
        time_mod *= CharacterConst.KOEFF_BASE_UNIT + CharacterConst.ADAPTIVITY_LEVEL2_BONUS
    elif adaptation > CharacterConst.WEAPON_ADAPTIVITY_LEVEL_1:
        time_mod *= CharacterConst.KOEFF_BASE_UNIT + CharacterConst.ADAPTIVITY_LEVEL1_BONUS
    return time_mod


def getEquipTimeModifyer(entity, gun_type):
    if gun_type in [ItemsCatalog.PISTOL, ItemsCatalog.REVOLVER]:
        if GetPerkNumber(entity, PerkList.LIGHT_WEAPON_EQIUP_TIME_REDUCE):
            return PerkList.LIGHT_WEAPON_EQIUP_TIME_REDUCE['Value']
        else:
            return CharacterConst.KOEFF_BASE_SMALL_ARMS_EQUIP
    if gun_type in [ItemsCatalog.ASSAULT_RIFLE, ItemsCatalog.SUB_MACHINE_GUN]:
        if GetPerkNumber(entity, PerkList.ASSAULT_RIFLES_EQIUP_TIME_REDUCE):
            return PerkList.ASSAULT_RIFLES_EQIUP_TIME_REDUCE['Value']
    if gun_type in [ItemsCatalog.ROCKET_LAUNCHER, ItemsCatalog.GRENADE_LAUNCHER, ItemsCatalog.MACHINE_GUN]:
        if GetPerkNumber(entity, PerkList.HEAVY_WEAPON_EQIUP_TIME_REDUCE):
            return PerkList.HEAVY_WEAPON_EQIUP_TIME_REDUCE['Value']
    if gun_type in [ItemsCatalog.SNIPER_RIFLE, ItemsCatalog.RIFLE, ItemsCatalog.SHOTGUN]:
        if GetPerkNumber(entity, PerkList.RIFLES_EQIUP_TIME_REDUCE):
            return PerkList.RIFLES_EQIUP_TIME_REDUCE['Value']
    return CharacterConst.KOEFF_BASE_UNIT


def GetDebuffTimeModifyer(entity):
    DebuffTimeModifyer = CharacterConst.KOEFF_BASE_UNIT
    perk_number = GetPerkNumber(entity, PerkList.DEBUFF_NIHILIZER)
    if perk_number > 0:
        DebuffTimeModifyer = PerkList.DEBUFF_NIHILIZER['Value']
    return DebuffTimeModifyer


def GetMaxSpeedModifyer(entity):
    speedModifyer = CharacterConst.KOEFF_BASE_UNIT + GetSurvivalSkillValue(entity, 'Sportsmanship') * 0.002
    perk_number = GetPerkNumber(entity, PerkList.MOVE_SPEED_UP)
    if perk_number > 0:
        speedModifyer *= PerkList.MOVE_SPEED_UP['Value']
    return speedModifyer


def GetMethabolismModifyer(entity):
    met_modifyer = CharacterConst.KOEFF_BASE_UNIT
    perk_number = GetPerkNumber(entity, PerkList.PHYSICAL_RESISTANCE)
    if perk_number > 0:
        met_modifyer *= PerkList.PHYSICAL_RESISTANCE['Value']
    skill = GetSurvivalSkillValue(entity, 'Metabolism') * (GetStatistic(entity, 'Endurance') / 10.0 + 0.5)
    return met_modifyer - skill * 0.0016


def GetMedicineModifyer(entity):
    skill = GetOtherSkillValue(entity, 'Medicine') * (GetStatistic(entity, 'Intelligence') / 10.0 + 0.5)
    MedicineModifyer = CharacterConst.KOEFF_BASE_UNIT + skill / 120.0
    perk_number = GetPerkNumber(entity, PerkList.MEDICINE_ADDON)
    if perk_number > 0:
        MedicineModifyer += PerkList.MEDICINE_ADDON['Value'] * perk_number
    return MedicineModifyer


def GetRepairSkillLevel(entity):
    if GetPerkNumber(entity, PerkList.REPAIR_ALL_LEVEL) > 0:
        return 10
    if GetPerkNumber(entity, PerkList.REPAIR_HIGH_LEVEL) > 0:
        return 3
    if GetPerkNumber(entity, PerkList.REPAIR_MEDIUM_LEVEL) > 0:
        return 2
    if GetPerkNumber(entity, PerkList.REPAIR_LOW_LEVEL) > 0:
        return 1
    return 0


def GetCraftSkillLevel(entity):
    if GetPerkNumber(entity, PerkList.CRAFT_LOW_LEVEL) > 0:
        return 1
    if GetPerkNumber(entity, PerkList.CRAFT_MEDIUM_LEVEL) > 0:
        return 2
    if GetPerkNumber(entity, PerkList.CRAFT_HIGH_LEVEL) > 0:
        return 3
    if GetPerkNumber(entity, PerkList.CRAFT_ALL_LEVEL) > 0:
        return 10
    return 0


def GetWeaponSkillValue(entity, gun_type):
    skill = 0
    if gun_type in [ItemsCatalog.PISTOL, ItemsCatalog.REVOLVER]:
        skill = GetCombatSkillValue(entity, 'LightWeapon')
    if gun_type in [ItemsCatalog.ASSAULT_RIFLE, ItemsCatalog.SUB_MACHINE_GUN]:
        skill = GetCombatSkillValue(entity, 'AssaultRifles')
    if gun_type in [ItemsCatalog.ROCKET_LAUNCHER, ItemsCatalog.GRENADE_LAUNCHER, ItemsCatalog.MACHINE_GUN]:
        skill = GetCombatSkillValue(entity, 'HeavyWeapon')
    if gun_type in [ItemsCatalog.SNIPER_RIFLE, ItemsCatalog.RIFLE, ItemsCatalog.SHOTGUN]:
        skill = GetCombatSkillValue(entity, 'Rifles')
    return skill


def GetKickbackModifyer(entity, gun_type, needed_mastery, item_type):
    skill = GetWeaponSkillValue(entity, gun_type)
    mastery = GetCurrentWeaponProfiency(skill)
    if needed_mastery > mastery:
        return CharacterConst.KOEFF_BASE_UNIT / ((needed_mastery - mastery) * CharacterConst.MASTERY_PENALTY)
    adaptation = GetWeaponAdaptivity(entity, item_type)
    adaptation_koeff = 0.0
    if adaptation > CharacterConst.WEAPON_ADAPTIVITY_LEVEL_2:
        adaptation_koeff = CharacterConst.ADAPTIVITY_LEVEL2_BONUS
    elif adaptation > CharacterConst.WEAPON_ADAPTIVITY_LEVEL_1:
        adaptation_koeff = CharacterConst.ADAPTIVITY_LEVEL1_BONUS
    skill_koeff = skill * CharacterConst.SHOOT_SKILL_VALUE / CharacterConst.MAX_SKILL_VALUE_SUPER
    stat_koeff = GetStatistic(entity, 'Strength') * CharacterConst.SHOOT_STAT_VALUE / CharacterConst.MAX_STAT_VALUE
    kickBack_mod = stat_koeff + skill_koeff + adaptation_koeff
    return CharacterConst.KOEFF_BASE_UNIT + CharacterConst.KOEFF_BASE_DOUBLE * kickBack_mod


def GetAccuracyModifyer(entity):
    return CharacterConst.ACCURACY_MOD_BASE - CharacterConst.ACCURACY_MOD_ADDED * GetStatistic(entity, 'Perception')


def GetMoveShootModifyer(entity):
    skill = GetCombatSkillValue(entity, 'ShootingOnMove')
    return CharacterConst.SHOT_MOVE_MOD * skill + CharacterConst.KOEFF_BASE_DOUBLE


def GetThrowModifyer(entity):
    throw_mod = 0
    perk_number = GetPerkNumber(entity, PerkList.THROW_RANGE)
    if perk_number > 0:
        throw_mod += PerkList.THROW_RANGE['Value'] * perk_number
    skill = GetCombatSkillValue(entity, 'Throwing')
    throw_mod += 0.004 * skill + 0.5
    return throw_mod


def GetMaxLaunchedGrenadesNumber(entity):
    return CharacterConst.KOEFF_BASE_UNIT + GetPerkNumber(entity, PerkList.MORE_GRENADES) * PerkList.MORE_GRENADES['Value']


def GetWeightModifyer(entity, item_class, item_sub_class):
    perk_modifyer = CharacterConst.KOEFF_BASE_UNIT
    for perk in PerkList.WEIGHT_REDUCERS_PERKS.values():
        for affected_item in perk['AffectedItems']:
            if affected_item[0] == item_class and affected_item[1] == item_sub_class:
                if GetPerkNumber(entity, perk) > 0:
                    perk_modifyer = perk['Value']

    if item_class in [ItemsCatalog.AMMO, ItemsCatalog.EXPLOSION, ItemsCatalog.LOOT]:
        return 1 - GetOtherSkillValue(entity, 'Packing') * CharacterConst.PACKING_MODIFYER
    else:
        return perk_modifyer


def GetReloadSpeedModifyer(entity, weapon_type):
    perk_modifyer = CharacterConst.KOEFF_BASE_UNIT
    for perk in PerkList.RELOAD_TIME_REDUCERS_PERKS.values():
        for affected_item in perk['AffectedItems']:
            if affected_item == weapon_type:
                if GetPerkNumber(entity, perk) > 0:
                    perk_modifyer = perk['Value']

    return perk_modifyer


def GetEquipSpeedModifyer(entity, weapon_type):
    perk_modifyer = CharacterConst.KOEFF_BASE_UNIT
    for perk in PerkList.EQUIP_TIME_REDUCERS_PERKS.values():
        for affected_item in perk['AffectedItems']:
            if affected_item == weapon_type:
                if GetPerkNumber(entity, perk) > 0:
                    perk_modifyer = perk['Value']

    return perk_modifyer


def GetCraftChanceModifyer(entity):
    return (GetOtherSkillValue(entity, 'Modification') / 2.0 + GetStatistic(entity, 'Intelligence') / 2.0) / 100.0


def GetRepairChanceModifyer(entity):
    return (GetOtherSkillValue(entity, 'Repair') / 2.0 + GetStatistic(entity, 'Intelligence') / 2.0) / 100.0


def GetNeatnessModifyer(entity, gun_type):
    have_needed_perk = False
    if gun_type in [ItemsCatalog.PISTOL, ItemsCatalog.REVOLVER]:
        if GetPerkNumber(entity, PerkList.LIGHT_WEAPON_NEATNESS) > 0:
            have_needed_perk = True
    if gun_type in [ItemsCatalog.ASSAULT_RIFLE, ItemsCatalog.SUB_MACHINE_GUN]:
        if GetPerkNumber(entity, PerkList.ASSAULT_RIFLE_NEATNESS) > 0:
            have_needed_perk = True
    if gun_type in [ItemsCatalog.ROCKET_LAUNCHER, ItemsCatalog.GRENADE_LAUNCHER, ItemsCatalog.MACHINE_GUN]:
        if GetPerkNumber(entity, PerkList.HEAVY_WEAPON_NEATNESS) > 0:
            have_needed_perk = True
    if gun_type in [ItemsCatalog.SNIPER_RIFLE, ItemsCatalog.RIFLE, ItemsCatalog.SHOTGUN]:
        if GetPerkNumber(entity, PerkList.RIFLES_NEATNESS) > 0:
            have_needed_perk = True
    if have_needed_perk:
        return GetOtherSkillValue(entity, 'Neatness') * 0.02
    else:
        return 0.2


def CanSniping(entity, gun_type):
    if gun_type in [ItemsCatalog.SNIPER_RIFLE, ItemsCatalog.RIFLE, ItemsCatalog.SHOTGUN]:
        if GetPerkNumber(entity, PerkList.RIFLES_SNIPING) > 0:
            return True
    else:
        return False


def CalculateMaxWeight(entity):
    Kpaking = (GetStatistic(entity, 'Agility') + GetOtherSkillValue(entity, 'Packing')) / CharacterConst.PACKING_KOEFF
    maxWeigth = float(GetStatistic(entity, 'Strength') * CharacterConst.STRENGTH_WEIGHT_MULTIPLYER + Kpaking + CharacterConst.STRENGTH_WEIGHT_ADD)
    maxWeigth += GetSurvivalSkillValue(entity, 'Sportsmanship') / 5.0
    perk = PerkList.MAX_WEIGHT_ADDON
    perk_number = GetPerkNumber(entity, perk)
    maxWeigth += perk['Value'] * perk_number
    return maxWeigth


def GetStunModifyer(entity):
    perk = PerkList.STUN_RESISTANCE
    perk_number = GetPerkNumber(entity, perk)
    if perk_number > 0:
        return perk['Value']
    else:
        return CharacterConst.KOEFF_BASE_UNIT


def GetCombatSkillValue(entity, skill_name):
    return entity.CombatSkills[skill_name].SkillValue


def GetSurvivalSkillValue(entity, skill_name):
    return entity.SurvivalSkills[skill_name].SkillValue


def GetOtherSkillValue(entity, skill_name):
    return entity.OtherSkills[skill_name].SkillValue


def GetCombatPerkValue(entity, skill_name):
    return entity.CombatSkills[skill_name].PerkList


def GetSurvivalPerkValue(entity, skill_name):
    return entity.SurvivalSkills[skill_name].PerkList


def GetOtherPerkValue(entity, skill_name):
    return entity.OtherSkills[skill_name].PerkList


def GetPerkNumber(entity, perk):
    number = 0
    for linked_skill in perk['MasterSkill']:
        if linked_skill[0] == PerkList.COMBAT:
            if perk['PerkType'] in entity.CombatSkills[linked_skill[1]].PerkList:
                number += entity.CombatSkills[linked_skill[1]].PerkList.count(perk['PerkType'])
        elif linked_skill[0] == PerkList.SURVIVAL:
            if perk['PerkType'] in entity.SurvivalSkills[linked_skill[1]].PerkList:
                number += entity.SurvivalSkills[linked_skill[1]].PerkList.count(perk['PerkType'])
        elif linked_skill[0] == PerkList.OTHER:
            if perk['PerkType'] in entity.OtherSkills[linked_skill[1]].PerkList:
                number += entity.OtherSkills[linked_skill[1]].PerkList.count(perk['PerkType'])

    return number


def GetStatistic(entity, stat_name):
    perk_group = PerkList.STAT_BOOT_PERKS[stat_name]
    StatModifyer = GetPerkNumber(entity, perk_group) * perk_group['Value']
    return entity.Stats[stat_name] + StatModifyer


def GetDamageModifyer(entity, gun_type):
    damage_koeff = CharacterConst.KOEFF_BASE_UNIT
    damage_type = FiringDefs.DAMAGE_CRITICAL
    crit_chance = 0.0
    critacal_roll = random.random()
    for perk in PerkList.DAMAGE_BOOSTERS.values():
        if GetPerkNumber(entity, perk) > 0:
            if perk['Type'] == PerkList.CRIT_CHANCE:
                crit_chance += perk['Value']
            if perk['Type'] == PerkList.CRIT_DAMAGE:
                damage_koeff += perk['Value']

    if critacal_roll > crit_chance:
        damage_koeff = CharacterConst.KOEFF_BASE_UNIT
        damage_type = FiringDefs.DAMAGE_NORMAL
    return (damage_type, damage_koeff)


def GetLuckDropModifyer(entity, item_class):
    dropModifyer = 0
    if item_class == ItemsCatalog.WEAPON:
        if GetPerkNumber(entity, PerkList.WEAPON_DROP_LOWER) > 0:
            dropModifyer += PerkList.WEAPON_DROP_LOWER['Value']
    if item_class in [ItemsCatalog.AMMO, ItemsCatalog.BUFF]:
        if GetPerkNumber(entity, PerkList.AMMO_DROP_LOWER) > 0:
            dropModifyer += PerkList.AMMO_DROP_LOWER['Value']
    if item_class == ItemsCatalog.LOOT:
        if GetPerkNumber(entity, PerkList.LOOT_DROP_LOWER) > 0:
            dropModifyer += PerkList.LOOT_DROP_LOWER['Value']
    dropModifyer += (GetStatistic(entity, 'Perception') + GetOtherSkillValue(entity, 'Luck') / 2.0) / 100.0
    return dropModifyer


def GetCombatSkillsValue(entity):
    return entity.CombatSkills


def GetSurvivalSkillsValue(entity):
    return entity.SurvivalSkills


def GetOtherSkillsValue(entity):
    return entity.OtherSkills


def GetWeaponAdaptivity(entitiy, itemType):
    for adaptive_entry in entitiy.WeaponAdaptations:
        if adaptive_entry['ItemType'] == itemType:
            return adaptive_entry['AdaptationPercent']

    return 0.0


def GetSkillFriendlyName(name):
    if name in CharacterConst.combat_skills_ready_names:
        return CharacterConst.combat_skills_friendly_names[CharacterConst.combat_skills_ready_names.index(name)]
    elif name in CharacterConst.survival_skills_ready_names:
        return CharacterConst.survival_skills_friendly_names[CharacterConst.survival_skills_ready_names.index(name)]
    elif name in CharacterConst.other_skills_ready_names:
        return CharacterConst.other_skills_friendly_names[CharacterConst.other_skills_ready_names.index(name)]
    else:
        return u''


def GetSkillValue(entity, name):
    if name in CharacterConst.combat_skills_ready_names:
        return GetCombatSkillValue(entity, name)
    if name in CharacterConst.survival_skills_ready_names:
        return GetSurvivalSkillValue(entity, name)
    if name in CharacterConst.other_skills_ready_names:
        return GetOtherSkillValue(entity, name)


def GetMaxEquippedArtifactNumber(self):
    num_artifacts = 0
    if self.CharacterCombatLevel >= CharacterConst.COMBAT_ARTIFACT_UNLOCK:
        num_artifacts += 1
    if self.CharacterSurvivalLevel >= CharacterConst.SURVIVAL_ARTIFACT_UNLOCK:
        num_artifacts += 1
    if self.CharacterOtherLevel >= CharacterConst.OTHER_ARTIFACT_UNLOCK:
        num_artifacts += 1
    return num_artifacts


class CharacterConst:
    MAX_PLAYER_EXPERIENCE = 62200000
    SPRINT_SPEED_ADJ = 1.5
    SHOOT_SKILL_VALUE = 0.5
    SHOOT_STAT_VALUE = 0.3
    KOEFF_BASE_UNIT = 1.0
    KOEFF_BASE_SMALL_ARMS_EQUIP = 0.5
    KOEFF_BASE_DOUBLE = 2.0
    BASE_DEFAULT_COST = 1000
    HP_REGENERATION_PER_SEC = 0.2
    PERK_STATUS_LOCKED, PERK_STATUS_KNOWN, PERK_STATUS_KNOWN_CAN_TAKE, PERK_STATUS_CAN_TAKE = xrange(4)
    COMBAT_EXPIRIENCE, SURVIVAL_EXPIRIENCE, OTHER_EXPIRIENCE = xrange(1, 4)
    MAX_LINE_OF_SIGHT = 150.0
    MAX_ANOMALY_LINE_OF_SIGHT = 50.0
    MAX_CAMOUFLAGE_DISTANCE = MAX_LINE_OF_SIGHT - 30.0
    STRENGTH_WEIGHT_MULTIPLYER = 5.0
    STRENGTH_WEIGHT_ADD = 5.0
    PACKING_KOEFF = 10.0
    HIT_POINTS_BASE = 100
    HIT_POINTS_ENDURANCE_MULTIPLYER = 15
    STAMINA_BASE = 100.0
    STAMINA_ENDURANCE_MULTIPLYER = 15.0
    STAMINA_SPRINT_USAGE = 5.0
    STAMINA_HEARTMODE_USAGE = 5.0
    STAMINA_JUMP_USAGE = 20.0
    STAMINA_RECOVERY = 5.0
    REGENERATION_UPDATE_PERIOD = 1.0
    INTELLIGENCE_MODIFYER_MULT = 0.1
    INTELLIGENCE_MODIFYER_ADD = 0.5
    BASE_SKILL_POINTS = 10
    PACKING_MODIFYER = 0.005
    MAX_STAT_VALUE = 15
    MAX_SKILL_VALUE = 80
    MAX_SKILL_VALUE_SUPER = 120
    PERK_PER_SKILL_AMOUNT = 20
    MAX_PERK_NUMBER = 12
    DUMMYS_PERK_PREQ_LIST = [0,
     10,
     20,
     30,
     40,
     50,
     60,
     70,
     80,
     90,
     100,
     110]
    NUM_KILLS_BEFORE_RENEGADE = 8
    PK_KARMA_GUARDIAN_KILL_LEVEL = 500
    SKILL_WEAPON_PROFESSIONAL = 50
    SKILL_WEAPON_EXPERT = 80
    WEAPON_ADAPTIVITY_LEVEL_1 = 0.4
    WEAPON_ADAPTIVITY_LEVEL_2 = 0.8
    ADAPTIVITY_LEVEL1_BONUS = 0.1
    ADAPTIVITY_LEVEL2_BONUS = 0.2
    ENCUMBRANCE_CAMOUFLAGE_LOSS = 0.3
    MASTERY_PENALTY = 2.0
    MAX_KICKBACK_VALUE = 1.5
    PLAYER_KILLER_DROP_MOD = 5.0
    CRAFT_EXP_LEVEL_MOD = 5
    CRAFT_EXP_TYPES_MOD = 1
    CRAFT_EXP_NUMBER_MOD = 0.1
    DROPPED_ITEM_VISION_LENGTH = 14.0
    DROPPED_ITEM_VISION_PERIOD = 20
    LOOT_EXP_ART_MOD = 50
    MEDECINE_SKILL_KOEFF = 100.0
    CAMOUFLAGE_SKILL_KOEFF = 50.0
    LEVEL_UP_BASE_EXP = 1000
    ACCURACY_MOD_BASE = 1.3
    ACCURACY_MOD_ADDED = 0.0
    SHOT_MOVE_MOD = -0.0125
    COMBAT_ARTIFACT_UNLOCK = 9
    SURVIVAL_ARTIFACT_UNLOCK = 8
    OTHER_ARTIFACT_UNLOCK = 7
    combat_skills_ready_names = ['LightWeapon',
     'AssaultRifles',
     'HeavyWeapon',
     'Rifles',
     'Throwing',
     'ShootingOnMove']
    survival_skills_ready_names = ['Sportsmanship',
     'Metabolism',
     'Camouflage',
     'Spotting',
     'AnomalySpotting']
    other_skills_ready_names = ['Medicine',
     'Repair',
     'Modification',
     'Luck',
     'Neatness',
     'Packing']
    combat_skills_friendly_names = [lc('CharacterUtils.common.LIGHT_WEAPON'),
     lc('CharacterUtils.common.ASSAULT_RIFLES'),
     lc('CharacterUtils.common.HEAVY_WEAPON'),
     lc('CharacterUtils.common.RIFLES'),
     lc('CharacterUtils.common.THROWING'),
     lc('CharacterUtils.common.SHOOT_ON_MOVE')]
    survival_skills_friendly_names = [lc('CharacterUtils.common.SPORTMANSHIP'),
     lc('CharacterUtils.common.METHABOLISM'),
     lc('CharacterUtils.common.CAMOUFLAGE'),
     lc('CharacterUtils.common.SPOTTING'),
     lc('CharacterUtils.common.ANOMALY_SPOTTING')]
    other_skills_friendly_names = [lc('CharacterUtils.common.MEDECINE'),
     lc('CharacterUtils.common.REPAIR'),
     lc('CharacterUtils.common.MODIFICATION'),
     lc('CharacterUtils.common.LUCK'),
     lc('CharacterUtils.common.NEATNESS'),
     lc('CharacterUtils.common.PACKING')]