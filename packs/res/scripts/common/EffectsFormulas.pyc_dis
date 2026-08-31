# Embedded file name: scripts/common/EffectsFormulas.py
from functools import partial
from FiringDefs import FiringDefs, DamageTypes, BODY_ZONES
import Stats

def onlyValueFormula(subEf, baseEf, stacks, entity):
    return subEf['value']


def useStacksFormula(subEf, baseEf, stacks, entity):
    return subEf['value'] * stacks


def useStacksMinusFormula(subEf, baseEf, stacks, entity):
    return subEf['value'] * max(stacks - subEf['stacksMinus'], 0)


def modificatorMultiplyFormula(subEf, baseEf, stacks, entity):
    return subEf['value'] * baseEf['modifier']


def modificatorMultiplyAndStacksFormula(subEf, baseEf, stacks, entity):
    return subEf['value'] * stacks * baseEf['modifier']


def fullDurationFormula(subEf, baseEf, stacks, entity):
    duration = baseEf['duration'] + (baseEf['stacks'] - 1) * baseEf['stackDuration']
    return duration


def radiationStacksFormula(subEf, baseEf, stacks, entity):
    radiationDef = entity.get_defence(BODY_ZONES.TORSO, DamageTypes.RADIATION)
    return subEf['value'] * round(stacks * (1 - min(0.95, radiationDef * 0.001)))


def bioDefOnHeadStacksFormula(subEf, baseEf, stacks, entity):
    bioDef = entity.get_defence(BODY_ZONES.HEAD, DamageTypes.BIO)
    return subEf['value'] * stacks * (1.0 - min(1.0, bioDef * 0.001))


def damageTypeStacksFormula(subEf, baseEf, stacks, entity):
    _damageType = baseEf['damageType']
    _dmgDef = entity.get_defence(BODY_ZONES.TORSO, _damageType)
    return subEf['value'] * round(stacks * (1 - min(0.95, _dmgDef * 0.001)))


def impactIfHasEffectFormula(subEf, baseEf, stacks, entity):
    otherEffectStacks = entity.getEffectStacks(subEf['otherEffectID'])
    return subEf['value'] * min(otherEffectStacks, 1)


def impactIfHasNotEffectFormula(subEf, baseEf, stacks, entity):
    otherEffectStacks = entity.getEffectStacks(subEf['otherEffectID'])
    if otherEffectStacks == 0:
        return subEf['value']
    else:
        return 0


def waterDamageByMetersFormula(subEf, baseEf, stacks, entity):
    enableEffectLevel = entity.position[1] + 0.2
    if enableEffectLevel < entity.waterHeight:
        return subEf['value'] * round(entity.waterHeight - enableEffectLevel)
    else:
        return 0


def waterSlowingByMetersFromula(subEf, baseEf, stacks, entity):
    enableEffectLevel = entity.position[1] + 0.15
    maxValue = 2
    if enableEffectLevel < entity.waterHeight:
        return subEf['value'] * min(entity.waterHeight - enableEffectLevel, maxValue)
    else:
        return 0


def regenerationAvatarHPFormula(subEf, baseEf, stacks, entity):
    regeneration_value = entity.GetStatValue(Stats.ch_HitPointsRegeneration)
    return regeneration_value


def regenerationAvatarMPFormula(subEf, baseEf, stacks, entity):
    regeneration_value = entity.GetStatValue(Stats.ch_StaminaRegeneration)
    return regeneration_value


def regenerationAvatarCPFormula(subEf, baseEf, stacks, entity):
    regeneration_value = entity.GetStatValue(Stats.ch_CombatPointsRegeneration)
    return regeneration_value


class Formula:
    Value = partial(onlyValueFormula)
    UseStacks = partial(useStacksFormula)
    UseStacksMinus = partial(useStacksMinusFormula)
    MultMod = partial(modificatorMultiplyFormula)
    MultModAndStacks = partial(modificatorMultiplyAndStacksFormula)
    FullDuration = partial(fullDurationFormula)
    Radiation = partial(radiationStacksFormula)
    BioDefOnHead = partial(bioDefOnHeadStacksFormula)
    impactIfHasEffect = partial(impactIfHasEffectFormula)
    impactIfHasNotEffect = partial(impactIfHasNotEffectFormula)
    waterFormula = partial(waterDamageByMetersFormula)
    waterSlowing = partial(waterSlowingByMetersFromula)
    regenerationHPAvatar = partial(regenerationAvatarHPFormula)
    regenerationMPAvatar = partial(regenerationAvatarMPFormula)
    regenerationCPAvatar = partial(regenerationAvatarCPFormula)