# Embedded file name: scripts/common/Config/Anomalies/CommonConfig.py
from Config import load_json, DATA_PATH
ANOMALIES_DATA_PATH = DATA_PATH + 'Anomalies/'
COMMON_CONFIG_PATH = ANOMALIES_DATA_PATH + '__config__.json'
common_config = load_json(COMMON_CONFIG_PATH)
base_lifetime = common_config['stat_base']['lifetime']
type_to_name = {}
name_to_type = {}
for str_type, anomaly_name in common_config['type_to_name'].items():
    type = int(str_type)
    type_to_name[type] = anomaly_name
    name_to_type[anomaly_name] = type

terrains_config = common_config['terrains']