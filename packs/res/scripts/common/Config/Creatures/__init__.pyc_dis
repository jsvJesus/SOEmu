# Embedded file name: scripts/common/Config/Creatures/__init__.py
from Config import load_json
from Config.Compiler import ConfigCompilerError
from Config.Creatures import CommonConfig
from CommonConfig import CREATURES_DATA_PATH, creature_type_to_file, uniq_mob_names
from Config.Creatures.Compiler import CreatureConfigCompiler
from Subtypes import SubtypesCompiler
import json
from Config.Creatures.Constants import *
from CommonConfig import MODELS_ROOT

def getLoots(mob_type, mob_sub_type):
    mob_file_name = creature_type_to_file[mob_type]
    path = CREATURES_DATA_PATH + mob_file_name
    json_data = open(path)
    data = json.load(json_data)
    loots = data.get('randomLoot')
    if loots.get(str(mob_sub_type)) is None:
        return loots.get('0').get('groups')
    else:
        return loots.get(str(mob_sub_type)).get('groups')


def get_type_config(mob_type):
    try:
        mob_type_config = get_type_config.cache[mob_type]
    except KeyError:
        mob_file_name = creature_type_to_file[mob_type]
        path = CREATURES_DATA_PATH + mob_file_name
        config = load_json(path)
        if config is None:
            raise IOError("DESIGNER_ERROR: Config.Creatures.get_type_config: can't open file {0}".format(path))
        try:
            mob_type_config = SubtypesCompiler(config, CreatureConfigCompiler, debug_name=mob_file_name).compile()
        except (ConfigCompilerError,
         KeyError,
         IndexError,
         ValueError,
         TypeError) as e:
            print 'DESIGNER_ERROR: Creature config: type {0}'.format(mob_type)
            raise

        mob_type_config['__filename__'] = mob_file_name
        get_type_config.cache[mob_type] = mob_type_config

    return mob_type_config


get_type_config.cache = {}

def get_config(mob_type, mob_level = KEYWORDS.DEFAULT_LEVEL):
    mob_type_config = get_type_config(mob_type)
    try:
        return mob_type_config[mob_level]
    except KeyError:
        return mob_type_config[get_subtype_index(mob_type, KEYWORDS.DEFAULT_LEVEL)]


def get_subtype_name(mob_type, subtype):
    return get_config(mob_type, subtype)[SUBTYPE_NAME]


def get_subtype_index(mob_type, subtype_name):
    mob_type_config = get_type_config(mob_type)
    try:
        return mob_type_config[SUBTYPE_INDEX_BY_NAME][subtype_name]
    except KeyError:
        print 'Creatures config: get_subtype_index: no such subtype {0} for type {1}'.format(subtype_name, mob_type)
        return None

    return None


def get_state_name(mob_type, mob_level, state_id):
    config = get_config(mob_type, mob_level)
    return '{0}({1})'.format(config[STATES][state_id]['__name__'], state_id)


def get_mob_name(mob_type, mob_level):
    return get_config(mob_type, mob_level)[NAME]


def get_uniq_mob_name(uniq_id):
    return uniq_mob_names.get(uniq_id)


def get_creatures_types():
    return creature_type_to_file.keys()