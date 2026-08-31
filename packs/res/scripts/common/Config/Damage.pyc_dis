# Embedded file name: scripts/common/Config/Damage.py
__author__ = 'monitorius'
__all__ = ['get_damage_type', 'get_damage_name']

class DamageTypes:
    MELEE = 0
    BULLET = 1
    EXPLOSION = 2
    FALL = 3
    ARMOR_PIERCING = 4
    BLEED = 5
    MAGNETIC = 6
    GRAVITATION = 7
    ELECTROSTATIC = 8
    INFRARED = 9
    RADIATION = 10
    PSY = 11
    BIO = 12
    AUDIO = 13
    AUDIOSELF = 14
    NIFF = 15
    SUFFOCATION = 16
    WATER = 17
    COLD = 18


class BODY_ZONES:
    NUM_BODY_ZONES = 9
    HEAD, FACE, TORSO, HEART, GROIN, ARM, FOREARM, LEG_UPPER, LEG_LOWER = xrange(NUM_BODY_ZONES)


def get_damage_type(damage_name):
    try:
        return DamageTypes.__dict__[damage_name]
    except KeyError:
        raise ValueError('No such damage name', damage_name)


def get_body_zone(body_zone_name):
    try:
        return BODY_ZONES.__dict__[body_zone_name]
    except KeyError:
        raise ValueError('No such body zone', body_zone_name)


def get_damage_name(damage_type):
    """Only for debug purposes."""
    for name, val in DamageTypes.__dict__.iteritems():
        if not name.startswith('__') and val == damage_type:
            return name


def get_body_zone_name(body_zone):
    """Only for debug purposes"""
    for name, val in BODY_ZONES.__dict__.iteritems():
        if not name.startswith('__') and val == body_zone:
            return name


class Flags:
    CRITICAL = 1


class SourceTypes:
    AVATAR = 1
    CREATURE = 2
    NPC_PVE = 3
    NPC_PVP = 4
    SUICIDE = 5
    EFFECT = 6
    WORLD = 7
    ANOMALY = 8
    UNKNOWN = 9
    data = {AVATAR: {},
     CREATURE: {},
     NPC_PVE: {},
     NPC_PVP: {},
     SUICIDE: {},
     EFFECT: {},
     WORLD: {},
     ANOMALY: {},
     UNKNOWN: {}}


class Restrictions:
    FROM_AVATAR = 1
    COLD_DAMAGE = 20
    TO_HEAD = 21

    class Types:
        BY_SOURCE_TYPE = 1
        BY_DAMAGE_TYPE = 2
        BY_BODY_ZONE = 3

    data = {FROM_AVATAR: {'type': Types.BY_SOURCE_TYPE,
                   'source_types': [SourceTypes.AVATAR]},
     COLD_DAMAGE: {'type': Types.BY_DAMAGE_TYPE,
                   'damage_types': [DamageTypes.COLD]},
     TO_HEAD: {'type': Types.BY_BODY_ZONE,
               'damage_types': [BODY_ZONES.HEAD]}}


body_zone_damage_multiplier = {BODY_ZONES.HEAD: 2.0,
 BODY_ZONES.GROIN: 1.5,
 BODY_ZONES.LEG_LOWER: 0.5,
 BODY_ZONES.FOREARM: 0.5}