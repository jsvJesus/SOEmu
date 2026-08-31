# Embedded file name: scripts/common/EffectUtils.py
import copy
import Stats

class EFFECT_TYPE:
    UNDEFINED, BUFF, DEBUFF = xrange(3)


class ON_REAPPLY:
    NONE, STACKS, DURATION, ALL = xrange(4)


class SOURCE:
    ITEMS, EXTERNAL, AVATAR_SPECIAL, CREATURE_SPECIAL = xrange(4)


class DefaultSubEf(dict):

    def __init__(self, **params):
        from EffectData import defaultSubEffect
        dict.__init__(self, defaultSubEffect)


class SubEfClass:
    _damageActive, _damagePassive, _healActive, _healPassive, _healPercentActive, _healPercentPassive, _directStatChangeActive, _directStatChangePassive, _statChange, _applyEffectActive, _applyEffectPassive, _safe, _stun, _removeEffectsActive, _removeEffectsPassive, _food, _staminaDeltaUsage, _burn, _TestStatEff, _poisonScreen, _adrenaline = xrange(21)

    class StatChange(DefaultSubEf):
        saveStats = [Stats.ch_MoveSpeed, Stats.ch_Accuracy]

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            from EffectData import defaultStatChange
            dict.__init__(self, defaultStatChange)
            self.update(params)
            self['class'] = SubEfClass._statChange

    class DirectStatChange(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            from EffectData import defaultDirectStatChange
            dict.__init__(self, defaultDirectStatChange)
            self.update(params)
            self['class'] = SubEfClass._directStatChangePassive

    class Damage(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            from EffectData import defaultDamage
            dict.__init__(self, defaultDamage)
            self.update(params)
            self['class'] = SubEfClass._damagePassive

    class Heal(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            from EffectData import defaultHeal
            dict.__init__(self, defaultHeal)
            self.update(params)
            self['class'] = SubEfClass._healPassive

    class HealPercent(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            from EffectData import defaultHealPercent
            dict.__init__(self, defaultHealPercent)
            self.update(params)
            self['class'] = SubEfClass._healPercentPassive

    class ApplyEffect(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            from EffectData import defaultApplyEffect
            dict.__init__(self, defaultApplyEffect)
            self.update(params)
            self['class'] = SubEfClass._applyEffectPassive

    class Safe(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            from EffectData import defaultSafe
            dict.__init__(self, defaultSafe)
            self.update(params)
            self['class'] = SubEfClass._safe

    class Stun(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            from EffectData import defaultStun
            dict.__init__(self, defaultStun)
            self.update(params)
            self['class'] = SubEfClass._stun

    class RemoveEffects(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            from EffectData import defaultRemoveEffects
            dict.__init__(self, defaultRemoveEffects)
            self.update(params)
            self['class'] = SubEfClass._removeEffectsPassive

    class FoodEffects(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            from EffectData import defaultFoodEffects
            dict.__init__(self, defaultFoodEffects)
            self.update(params)
            self['class'] = SubEfClass._food

    class TestStatEffects(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            dict.__init__(self, {})
            self.update(params)
            self['class'] = SubEfClass._TestStatEff

    class BurnEffects(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            from EffectData import defaultBurnEffects
            dict.__init__(self, defaultBurnEffects)
            self.update(params)
            self['class'] = SubEfClass._burn

    class AdrenalineEffect(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            dict.__init__(self, {})
            self.update(params)
            self['class'] = SubEfClass._adrenaline

    class PoisonScreenEffects(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            dict.__init__(self, {})
            self.update(params)
            self['class'] = SubEfClass._poisonScreen

    class StaminaDeltaUsageEffect(DefaultSubEf):

        def __init__(self, **params):
            DefaultSubEf.__init__(self)
            from EffectData import defaultStaminaDeltaUsageEffect
            dict.__init__(self, defaultStaminaDeltaUsageEffect)
            self.update(params)
            self['class'] = SubEfClass._staminaDeltaUsage


class Effect(dict):

    def __init__(self, **params):
        from EffectData import defaultEffect
        dict.__init__(self, defaultEffect)
        self.update(params)


def getTickDuration():
    return 0.5


def getEffect(effectId):
    from EffectData import EffectsConfig
    if EffectsConfig.has_key(effectId):
        return EffectsConfig[effectId]
    else:
        print '\tEffectUtils.getEffect: no such effect', effectId
        return None
        return None


def getBaseEffectParam(baseEffect, paramName = None):
    """ Used to retrieve baseEffect data from globalData. If paramName == None, then return all baseEffect data """
    if paramName == None:
        return getEffect(baseEffect['id'])
    else:
        return getEffect(baseEffect['id']).get(paramName, None)
        return


def prepareEffectsConfig(EffectsConfig):
    """ Prepares EffectData.EffectsConfig:
            * Set ids for effects
            * Convert durations in seconds to ticks
            * Active/passive class select (it makes no sence to do this work by game designers)
    """
    for id, ef in EffectsConfig.items():
        ef['id'] = id

    for ef in [ ef for ef in EffectsConfig.values() if ef['stackDuration'] != -1 ]:
        ef['stackDuration'] /= getTickDuration()

    passive = [ subEf for ef in EffectsConfig.values() for subEf in ef['passive'] ]
    active = [ subEf for ef in EffectsConfig.values() for subEf in ef['active'] ]
    efPairs = [(SubEfClass._damagePassive, SubEfClass._damageActive),
     (SubEfClass._healPassive, SubEfClass._healActive),
     (SubEfClass._applyEffectPassive, SubEfClass._applyEffectActive),
     (SubEfClass._removeEffectsPassive, SubEfClass._removeEffectsActive),
     (SubEfClass._directStatChangePassive, SubEfClass._directStatChangeActive),
     (SubEfClass._healPercentPassive, SubEfClass._healPercentActive)]
    for subEf in active:
        subEf['interval'] /= getTickDuration()
        for pair in efPairs:
            if subEf['class'] == pair[0]:
                subEf['class'] = pair[1]
                break

    for baseEf in EffectsConfig.values():
        if baseEf['sources'] and baseEf['stackDuration'] != -1:
            print 'DESIGNER_WARNING: prepareEffectsConfig: baseEf %d with sources is not permanent (stackDuration != -1)' % baseEf['id']
            baseEf['stackDuration'] = -1

    stat_changers = [ ef for ef in passive if ef['class'] == SubEfClass._statChange ]
    for subEf in stat_changers:
        index = subEf['stat_index']
        if not isinstance(index, list):
            index = [index]
        for i, val in enumerate(index):
            if not isinstance(val, list):
                index[i] = [val]

        for val in index:
            dicts = [ {} for i in xrange(len(index)) ]
            dicts.append(True)
            for i in xrange(len(index) - 1, -1, -1):
                for val in index[i]:
                    dicts[i][val] = dicts[i + 1]

        subEf['stat_index'] = dicts[0]