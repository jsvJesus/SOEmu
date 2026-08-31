# Embedded file name: scripts/common/Config/Effects.py
import json
import Config
EFFECTS_PATH = Config.DATA_PATH + 'Effects.json'
try:
    import ResMgr
    dataSection = ResMgr.openSection(EFFECTS_PATH)
    data = json.loads(dataSection.asBinary)
except ImportError:
    print 'Config\\Effects.py ImportError ResMgr'
    configPath = Config.__file__
    parts = configPath.split('/')
    efConfigPath = '/'.join(parts[:-2]) + '/data/Effects.json'
    s = open(efConfigPath, 'r').read()
    data = json.loads(s)
except Exception as e:
    print 'Config\\Effects.py EEEERRRRooor ResMgr', e
    configPath = Config.__file__
    parts = configPath.split('\\')
    efConfigPath = '/'.join(parts[:-2]) + '/data/Effects.json'
    s = open(efConfigPath, 'r').read()
    data = json.loads(s)

effects = data['Effects']

class EffectNames(object):
    pass


for name, effect_id in effects.items():
    setattr(EffectNames, name, effect_id)

def get_effect_id(effect_name):
    try:
        return effects[effect_name]
    except KeyError:
        raise ValueError('No such effect', effect_name)