# Embedded file name: scripts/common/Config/Anomalies/__init__.py
from Config import load_json
from Config.Compiler import ConfigCompilerError, ConfigCompiler
from Config.Anomalies import CommonConfig
from CommonConfig import type_to_name, ANOMALIES_DATA_PATH, terrains_config
from Config.Anomalies.Compiler import anomaly_compiler, terrains_compiler
from Config.Anomalies.Constants import *

def get_config(type):
    try:
        type_config = get_config.cache[type]
    except KeyError:
        anomaly_name = type_to_name[type]
        file_name = anomaly_name + '.json'
        path = ANOMALIES_DATA_PATH + file_name
        config = load_json(path)
        if config is None:
            raise IOError("DESIGNER_ERROR: Config.Anomalies.get_config: can't open file {0}".format(path))
        try:
            type_config = anomaly_compiler.compile('root', config)
        except (ConfigCompilerError,
         KeyError,
         IndexError,
         ValueError,
         TypeError) as e:
            print 'DESIGNER_ERROR: Anomaly config: type {0}'.format(type)
            raise

        type_config['__filename__'] = file_name
        get_config.cache[type] = type_config

    return type_config


get_config.cache = {}
terrains = terrains_compiler.compile('root', terrains_config)

def get_anomalies_for_terrain(terrain_id):
    if terrain_id == 49:
        print '___', terrains[terrain_id], '  ', terrain_id
    return terrains[terrain_id]