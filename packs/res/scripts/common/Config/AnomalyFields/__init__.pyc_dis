# Embedded file name: scripts/common/Config/AnomalyFields/__init__.py
import copy
from Config import load_json
from Config.Compiler import ConfigCompilerError
from Config.AnomalyFields.Compiler import pattern_compiler, lists_compiler
from Config.AnomalyFields.CommonConfig import AF_PATH, AF_ANOMALY_PATH, LISTS_PATH
from Config.AnomalyFields.Constants import *

def get_pattern_data(pattern_id, _cache = {}):
    try:
        return _cache[pattern_id]
    except KeyError:
        pattern_file_path = AF_PATH + pattern_id + '.json'
        pattern_data = load_json(pattern_file_path)
        try:
            _cache[pattern_id] = pattern_compiler.compile('root', pattern_data)
        except Exception:
            print 'DESIGNER_ERROR: AnomalyField config: pattern {0}'.format(pattern_id)
            raise

        return _cache[pattern_id]


def get_anomaly_config(pattern_id, group_id, cell_x, cell_z, param_name = None):
    pattern_data = get_pattern_data(pattern_id)
    anom_id = pattern_data[CELLS][cell_x][cell_z]
    anom_data = pattern_data[GROUPS][group_id][anom_id]
    if param_name is not None:
        return anom_data[param_name]
    else:
        return anom_data
        return


def getCellsXNum(pattern_id):
    return len(get_pattern_data(pattern_id)[CELLS])


def getCellsZNum(pattern_id):
    return len(get_pattern_data(pattern_id)[CELLS][0])


def get_pattern_list(list_name, _cache = {}):
    try:
        return _cache[list_name]
    except KeyError:
        lists_data = load_json(LISTS_PATH)
        try:
            _cache.update(lists_compiler.compile('root', lists_data))
        except (ConfigCompilerError,
         KeyError,
         IndexError,
         ValueError,
         TypeError) as e:
            print 'DESIGNER_ERROR: AnomalyField config: list {0}'.format(list_name)
            raise
        else:
            return _cache[list_name]