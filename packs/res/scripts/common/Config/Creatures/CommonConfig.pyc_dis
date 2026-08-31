# Embedded file name: scripts/common/Config/Creatures/CommonConfig.py
from Config import load_json, DATA_PATH
from Localization import lc
CREATURES_DATA_PATH = DATA_PATH + 'Creatures/'
COMMON_CONFIG_PATH = CREATURES_DATA_PATH + '__config__.json'
PRESETS_PATH = CREATURES_DATA_PATH + '__presets__.json'
COLLIDERS_PATH = CREATURES_DATA_PATH + 'Colliders/'
common_config = load_json(COMMON_CONFIG_PATH)
MODELS_ROOT = common_config['models_root']
stat_rate = common_config['stat_rate']
stat_base = common_config['stat_base']
colliders_files = common_config['colliders']
creature_type_to_file = {}
uniq_mob_names = {}
for str_type, file_name in common_config['creature_type_to_file'].items():
    creature_type = int(str_type)
    creature_type_to_file[creature_type] = file_name

for uniq_id, uniq_name_locale_path in common_config['uniq_names'].items():
    uniq_mob_names[uniq_id] = lc(uniq_name_locale_path)