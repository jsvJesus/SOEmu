# Embedded file name: scripts/common/ThrowingData.py


class ThrowTypes:
    GRENADE_F1, HOMEMADE_GRENADE, ATOMIC_GRENADE, STONE, TEST_CREATURE_GRENADE, BIO, OUTCAST, RGD5_GRENADE, F1_FAKE_GRENADE, RGN_GRENADE, RGO_GRENADE, SNOW_GRENADE, FLASH_GRENADE, WEB_GRENADE, POISON_GRENADE, GLUE_GRENADE, HOMEMADE_ACID_GRENADE, SMOKE_GRENADE, GRENADE_MOLOTOV = xrange(19)


def get_throw_type(name):
    try:
        return ThrowTypes.__dict__[name]
    except KeyError:
        raise ValueError('No such throw type', name)


ALL_ALLOWED = ['Avatar', 'NPC', 'Creature']
NO_CREATURES = ['Avatar', 'NPC']
ONLY_AVATAR = ['Avatar']
NO_TARGETS = None

class default(dict):

    def __init__(self, **params):
        dict.__init__(self)
        self['elasticity'] = 0.2
        self['radius'] = 0.1
        self['maxBounces'] = 3
        self['timeSlice'] = 1.0 / 30.0
        self['tripTime'] = 20
        self['modelSFX'] = None
        self['particles'] = None
        self[' isFXPersistent'] = None
        self['timeDestroy'] = 10.0
        self.update(params)
        return


class grenade(default):

    def __init__(self, **params):
        default.__init__(self, **params)
        self['entityClassName'] = 'Grenade'
        self['explodeSFX'] = 'sfx/grenade_explode.xml'
        self['explodeOnFlyingEnded'] = False
        self['allowed_targets'] = ALL_ALLOWED
        self.update(params)


Throwing = {ThrowTypes.GRENADE_F1: grenade(modelName='characters/items/weapons/grenade_f1_lod1.model'),
 ThrowTypes.HOMEMADE_GRENADE: grenade(modelName='characters/items/weapons/homemade_grenade.model'),
 ThrowTypes.ATOMIC_GRENADE: grenade(modelName='characters/items/weapons/attach/node_rocket_lod1.model', explodeSFX='sfx/atomic_explode.xml'),
 ThrowTypes.GRENADE_MOLOTOV: grenade(modelName='characters/items/weapons/molotov_cocktail.model', explodeSFX='sfx/explosion_molotov.xml', particles='particles/molotov.xml', maxBounces=1, explodeOnFlyingEnded=True, isFXPersistent=True, allowed_targets=ALL_ALLOWED, timeDestroy=15),
 ThrowTypes.RGD5_GRENADE: grenade(modelName='characters/items/weapons/grenade_f1_lod1.model'),
 ThrowTypes.F1_FAKE_GRENADE: grenade(modelName='characters/items/weapons/grenade_f1_lod1.model', allowed_targets=NO_TARGETS),
 ThrowTypes.RGN_GRENADE: grenade(modelName='characters/items/weapons/grenade_f1_lod1.model', explodeOnFlyingEnded=True),
 ThrowTypes.RGO_GRENADE: grenade(modelName='characters/items/weapons/grenade_f1_lod1.model', explodeOnFlyingEnded=True),
 ThrowTypes.SNOW_GRENADE: grenade(modelName='characters/items/weapons/grenade_f1_lod1.model', modelSFX='sfx/anomaly_snowfield_hit.xml', allowed_targets=ONLY_AVATAR),
 ThrowTypes.FLASH_GRENADE: grenade(modelName='characters/items/weapons/grenade_f1_lod1.model'),
 ThrowTypes.WEB_GRENADE: grenade(modelName='characters/items/weapons/grenade_f1_lod1.model', explodeSFX='sfx/explosion_grenade_web.xml', allowed_targets=ONLY_AVATAR),
 ThrowTypes.POISON_GRENADE: grenade(modelName='characters/items/weapons/homemade_grenade.model', explodeSFX='sfx/explosion_grenade_poison.xml', explodeOnFlyingEnded=True, allowed_targets=ALL_ALLOWED),
 ThrowTypes.GLUE_GRENADE: grenade(modelName='characters/items/weapons/grenade_f1_lod1.model', explodeSFX='sfx/explosion_grenade_glue.xml', allowed_targets=ONLY_AVATAR),
 ThrowTypes.HOMEMADE_ACID_GRENADE: grenade(modelName='characters/items/weapons/grenade_f1_lod1.model', explodeSFX='sfx/explosion_grenade_acid.xml', explodeOnFlyingEnded=True, allowed_targets=ONLY_AVATAR),
 ThrowTypes.SMOKE_GRENADE: grenade(modelName='characters/items/weapons/homemade_grenade.model', explodeSFX='sfx/explosion_grenade_smoke.xml', allowed_targets=NO_TARGETS, isFXPersistent=0, timeDestroy=60.0),
 ThrowTypes.STONE: default(entityClassName='Stone', modelName='characters/items/misc/throw_rock_lod1.model'),
 ThrowTypes.BIO: default(entityClassName='Grenade', modelName='', maxBounces=0, modelSFX='sfx/Mob/jelly_range_spore.xml', explodeSFX='sfx/Mob/jelly_range_spore_expl.xml', explodeOnFlyingEnded=True, allowed_targets=NO_CREATURES),
 ThrowTypes.OUTCAST: default(entityClassName='Grenade', modelName='', maxBounces=0, modelSFX='sfx/Mob/outcast_range_spore.xml', allowed_targets=NO_CREATURES),
 ThrowTypes.TEST_CREATURE_GRENADE: grenade(modelName='characters/items/weapons/grenade_f1_lod1.model', modelSFX='particles/fonar_glow.xml', maxBounces=0, explodeOnFlyingEnded=True)}