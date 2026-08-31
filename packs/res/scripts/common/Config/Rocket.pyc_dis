# Embedded file name: scripts/common/Config/Rocket.py
from Items import ItemsCatalog
DEFAULT_TYPE = None
MODEL, TRAIL_SFX, EXPLODE_SFX = range(3)
params = {DEFAULT_TYPE: {MODEL: 'characters/items/weapons/attach/node_rocket_rpg7_lod1.model',
                TRAIL_SFX: 'particles/fire_rocket02.xml',
                EXPLODE_SFX: 'sfx/grenade_explode.xml'},
 ItemsCatalog.AMMO_RPG7_HP_TAN['TypeID']: {}}
default_params = params[DEFAULT_TYPE]

def get_model(item_type):
    cfg = params.get(item_type, default_params)
    return cfg.get(MODEL, default_params[MODEL])


def get_trail_sfx(item_type):
    cfg = params.get(item_type, default_params)
    return cfg.get(TRAIL_SFX, default_params[TRAIL_SFX])


def get_explode_sfx(item_type):
    cfg = params.get(item_type, default_params)
    return cfg.get(EXPLODE_SFX, default_params[EXPLODE_SFX])