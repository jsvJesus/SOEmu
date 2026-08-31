# Embedded file name: scripts/common/Config/Creatures/Subtypes.py
import copy
import re
from utils import get_first, is_identifier, hierarchy_get, hierarchy_set, add_nonexistent
from Config import load_json
from Config.Creatures.CommonConfig import CREATURES_DATA_PATH
from Config.Creatures.Constants import *
KW = KEYWORDS

class SubtypesError(Exception):
    pass


def get_key_and_settings(key_composite):
    key_splitted = key_composite.replace(' ', '').split(',')
    key, key_settings = key_splitted[0], key_splitted[1:]
    return (key, key_settings)


def get_parent_name(settings):
    for setting in settings:
        ind = setting.find(KW.PARENT)
        if ind != -1:
            return setting[ind + len(KW.PARENT):]

    return None


def get_parent(settings):
    parent_name = get_parent_name(settings)
    if get_parent.cache is None:
        get_parent.cache = load_json(CREATURES_DATA_PATH + '__presets__.json')
    return get_parent.cache.get(parent_name)


get_parent.cache = None

def apply_parent_data(object, settings):
    parent = copy.deepcopy(get_parent(settings))
    if parent:
        if isinstance(object, dict):
            add_nonexistent(object, parent)
        elif isinstance(object, list):
            object.extend(parent)


class SubtypesCompiler:

    def __init__(self, config, mob_compiler_class = None, debug_name = ''):
        self.mob_compiler_class = mob_compiler_class
        self.debug_name = debug_name
        self.reset(config)

    def reset(self, config):
        self.index_to_subtype = []
        self.configs_by_lv = {KW.DEFAULT_LEVEL: self.create_default_config(config)}
        self.preprocess_by_levels(config)

    def compile(self):
        if self.mob_compiler_class is None:
            print 'SubtypesCompiler: mob compiler class is not defined.'
            return
        else:
            self.index_to_subtype = sorted(self.configs_by_lv.keys())
            configs_by_lv = {}
            for i, subtype_name in enumerate(self.index_to_subtype):
                configs_by_lv[i] = self.configs_by_lv[subtype_name]

            self.configs_by_lv = configs_by_lv
            compiled = {SUBTYPE_INDEX_BY_NAME: {}}
            for subtype_ind, subtype_config in self.configs_by_lv.items():
                compiled[subtype_ind] = self.mob_compiler_class().compile(None, subtype_config)
                name = self.index_to_subtype[subtype_ind]
                compiled[subtype_ind][SUBTYPE_NAME] = name
                compiled[SUBTYPE_INDEX_BY_NAME][name] = subtype_ind

            return compiled

    def create_default_config(self, config):
        """Create config with no config keywords."""
        default_config = copy.deepcopy(config)

        def apply_default_settings_recursive(obj):
            if isinstance(obj, dict):
                for key_composite, value in obj.items():
                    key, settings = get_key_and_settings(key_composite)
                    if KW.BYLEVEL in settings:
                        try:
                            default_object = value[KW.DEFAULT_LEVEL]
                        except KeyError:
                            print 'DESIGNER_ERROR: no default object in {0} "{1}"'.format(self.debug_name, key_composite)
                            raise

                        apply_parent_data(default_object, settings)
                        apply_default_settings_recursive(default_object)
                        obj[key] = default_object
                        del obj[key_composite]
                    else:
                        apply_parent_data(value, settings)
                        del obj[key_composite]
                        obj[key] = value
                        apply_default_settings_recursive(value)

            elif isinstance(obj, list):
                for value in obj:
                    apply_default_settings_recursive(value)

        apply_default_settings_recursive(default_config)
        return default_config

    def get_config_by_level(self, level):
        """Return config for specified level (If don't exist, create it using default config)."""
        try:
            return self.configs_by_lv[level]
        except KeyError:
            cfg = self.configs_by_lv[level] = copy.deepcopy(self.configs_by_lv[KW.DEFAULT_LEVEL])
            return cfg

    def set_by_lv_object(self, level, path, object, settings):
        config_by_lv = self.get_config_by_level(level)
        obj_to_change = hierarchy_get(config_by_lv, path, use_default=False)
        if isinstance(obj_to_change, dict):
            if KW.FULL_OVERRIDE in settings:
                hierarchy_set(config_by_lv, path, object)
            else:
                obj_to_change.update(object)
        elif isinstance(obj_to_change, list):
            if KW.PREPEND in settings:
                parent_obj = hierarchy_get(config_by_lv, path[:-1], use_default=False)
                parent_obj[path[-1]] = object + obj_to_change
            elif KW.APPEND in settings:
                obj_to_change.extend(object)
            else:
                hierarchy_set(config_by_lv, path, object)
        else:
            parent_obj = hierarchy_get(config_by_lv, path[:-1], use_default=False)
            parent_obj[path[-1]] = object

    re_one_lv = re.compile('^(?P<level>\\w+)((,(?P<opts>[,\\w]*))|)$')
    re_multi_lv = re.compile('^\\[(?P<level>[,\\w]+)\\]((,(?P<opts>[,\\w]*))|)$')

    @staticmethod
    def get_levels_and_opts(lv_composite):
        lv_comp_no_spaces = lv_composite.replace(' ', '')
        for regexp in [SubtypesCompiler.re_multi_lv, SubtypesCompiler.re_one_lv]:
            res = re.match(regexp, lv_comp_no_spaces)
            if res:
                return (res.group('level').split(','), res.group('opts').split(',') if res.group('opts') else [])
        else:
            raise SubtypesError('Invalid level header format:{0}'.format(lv_composite))

    def preprocess_by_levels(self, config):

        def preprocess_by_levels_recursive(obj, path = None):
            path = path if path is not None else []
            if isinstance(obj, list):
                for i, value in enumerate(obj):
                    preprocess_by_levels_recursive(value, path + [i])

            elif isinstance(obj, dict):
                for key_composite, value in obj.items():
                    key, settings = get_key_and_settings(key_composite)
                    if KW.BYLEVEL in settings:
                        local_path = path + [key]
                        preprocess_by_levels_recursive(value[KW.DEFAULT_LEVEL], path + [key])
                        seen_levels = set()
                        for lv_composite, by_lv_value in value.items():
                            if lv_composite == KW.DEFAULT_LEVEL:
                                continue
                            str_lvs, settings_lv = self.get_levels_and_opts(lv_composite)
                            for str_lv in str_lvs:
                                if str_lv in seen_levels:
                                    raise SubtypesError('Duplicate level', str_lv)
                                seen_levels.add(str_lv)
                                self.set_by_lv_object(str_lv, local_path, by_lv_value, settings_lv)

                    else:
                        preprocess_by_levels_recursive(value, path + [key])

            return

        preprocess_by_levels_recursive(config)
        return