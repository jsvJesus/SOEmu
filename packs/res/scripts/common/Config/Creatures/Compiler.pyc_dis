# Embedded file name: scripts/common/Config/Creatures/Compiler.py
import ResMgr
from utils import get_first, is_identifier
from Config.Compiler import ConfigCompiler, ICompiler, COMPILER, StringCompiler
from Config.Creatures.Constants import *
from Config.Creatures.CommonConfig import COLLIDERS_PATH, stat_rate, stat_base, colliders_files
import Colliders

class PredicateCompiler(ICompiler):
    str_to_operator = {'less': ' < ',
     'more': ' > ',
     'equal': ' == '}

    def compile(self, name, value):
        return eval(self.parse_predicate(value))

    def parse_predicate(self, pred_data):
        parsed_predicate = 'lambda self:'

        def parse_recursive(pred_data, join_str = 'None'):
            parsed_conds = []
            for data in map(self.prepare_predicate, pred_data):
                pred_name = data['name']
                if pred_name == 'or':
                    parsed_cond = parse_recursive(data['predicates'], ' or ')
                elif pred_name == 'and':
                    parsed_cond = parse_recursive(data['predicates'], ' and ')
                elif pred_name == 'state':
                    state_ind = self.get_index(STATES, data['value'])
                    parsed_cond = 'self.get_logic_param("state") == ' + str(state_ind)
                elif is_identifier(pred_name):
                    oper = self.str_to_operator[data['operator']]
                    parsed_cond = "self.get_logic_param('" + pred_name + "')" + oper + str(data['value'])
                else:
                    parsed_cond = 'None'
                parsed_conds.append(parsed_cond)

            return '(' + join_str.join(parsed_conds) + ')'

        parsed_predicate += parse_recursive([pred_data])
        parse_recursive = None
        return parsed_predicate

    def prepare_predicate(self, pred_data):
        if not isinstance(pred_data, list) and not isinstance(pred_data, tuple):
            return pred_data
        elif pred_data[0] == 'or' or pred_data[0] == 'and':
            return {'name': pred_data[0],
             'predicates': pred_data[1]}
        else:
            return {'name': pred_data[0],
             'operator': pred_data[1],
             'value': pred_data[2]}


class ModelPathCompiler(StringCompiler):

    def precompile(self, name, value):
        model_path = self.compile(name, value)
        self.set_param('model_path', model_path)


class CollidersCompiler(ICompiler):

    def is_generator(self):
        return True

    def generate(self):
        model_path = self.get_param('model_path')
        file_path = COLLIDERS_PATH + colliders_files[model_path]
        return Colliders.get_colliders_cfg(file_path)


class CapsCompiler(ICompiler):
    caps_str_to_ind = {}
    for entry in ResMgr.openSection('scripts/common/capabilities.xml').values():
        if entry.name == 'state':
            ind = entry.asInt
            name = get_first(lambda sub_entry: sub_entry.name == 'name', entry.values()).asString
            caps_str_to_ind[name] = ind

    def compile(self, name, cap_name):
        return CapsCompiler.caps_str_to_ind[cap_name]


class StateTimerCompiler(ICompiler):

    def compile(self, name, value):
        return (value[STATE_TIMER_TIME], self.get_index(STATES, value[STATE_TIMER_STATE]))


conditions_def = {'compiler': COMPILER.LIST,
 'value_compiler': {'compiler': COMPILER.CONFIG,
                    'items': {'to_state': {'compiler': COMPILER.NAME_TO_INDEX,
                                           'indexed_dict': 'states',
                                           'required': True},
                              'predicate': {'compiler': PredicateCompiler}}}}
config_definition = {'compiler': COMPILER.CONFIG,
 'items': {NAME: {'compiler': COMPILER.LOCALIZATION,
                  'default': 'Creatures.UNDEFINED_CREATURE',
                  'compile_default': True},
           MODEL: {'compiler': ModelPathCompiler,
                   'default': ''},
           COLLIDERS: {'compiler': CollidersCompiler},
           MODEL_SCALE: {'compiler': COMPILER.FLOAT,
                         'default': 1},
           COEF_LEVEL: {'compiler': COMPILER.FLOAT,
                        'default': 99},
           FOOTSTEPS_SOUND: {'compiler': COMPILER.STRING,
                             'default': ''},
           FOOT_NODES: {'compiler': COMPILER.LIST,
                        'default': []},
           EXPERIENCE: {'compiler': COMPILER.FLOAT,
                        'default': 0},
           KARMA: {'compiler': COMPILER.FLOAT,
                   'default': 10},
           HEALTH: {'compiler': COMPILER.FLOAT,
                    'default': 1,
                    'mult_param': 'health_coef'},
           AGRO_RANGE: {'compiler': COMPILER.FLOAT,
                        'default': 1},
           LOSE_AGRO_RANGE: {'compiler': COMPILER.FLOAT,
                             'default': 1},
           GCD: {'compiler': COMPILER.FLOAT,
                 'default': 1},
           DEFAULT_STATE: {'compiler': COMPILER.NAME_TO_INDEX,
                           'indexed_dict': 'states',
                           'required': True},
           ACTIONS: {'compiler': COMPILER.DICT,
                     'default': {}},
           EVENTS: {'compiler': COMPILER.DICT,
                    'default': {}},
           HEIGHT: {'compiler': COMPILER.FLOAT,
                    'default': 1},
           WIDTH: {'compiler': COMPILER.FLOAT,
                   'default': 1},
           DECOMPOSE_TIME: {'compiler': COMPILER.LIST,
                            'default': [10, 20]},
           MELEE_DISTANCE: {'compiler': COMPILER.FLOAT,
                            'default': 1},
           MELEE_HEIGHT: {'compiler': COMPILER.FLOAT,
                          'default': 0},
           COMMON_CONDITIONS: conditions_def,
           TINTS: {'compiler': COMPILER.LIST,
                   'default': [],
                   'value_compiler': {'compiler': COMPILER.DICT,
                                      'key_compiler': {'compiler': COMPILER.STRING},
                                      'value_compiler': {'compiler': COMPILER.STRING}}},
           DEFENCE: {'compiler': COMPILER.DICT,
                     'default': {},
                     'key_compiler': {'compiler': COMPILER.DAMAGE},
                     'value_compiler': {'compiler': COMPILER.FLOAT}},
           LOOT: {'compiler': COMPILER.DICT,
                  'default': {},
                  'key_compiler': {'compiler': COMPILER.INT},
                  'value_compiler': {'compiler': COMPILER.STRING}},
           STATES: {'compiler': COMPILER.DICT,
                    'default': {},
                    'indexed_keys': True,
                    'key_compiler': {'compiler': COMPILER.NAME_TO_INDEX,
                                     'indexed_dict': 'states'},
                    'value_compiler': {'compiler': COMPILER.CONFIG,
                                       'items': {'entering_actions': {'compiler': COMPILER.DICT,
                                                                      'default': {}},
                                                 'persistent_actions': {'compiler': COMPILER.LIST,
                                                                        'default': []},
                                                 'speed': {'compiler': COMPILER.DICT,
                                                           'default': {}},
                                                 'movement_types': {'compiler': COMPILER.LIST,
                                                                    'default': []},
                                                 STATE_SPEED: {'compiler': COMPILER.DICT,
                                                               'default': {}},
                                                 STATE_CONDITIONS: conditions_def,
                                                 STATE_SKILLS: {'compiler': COMPILER.DICT,
                                                                'default': {},
                                                                'key_compiler': {'compiler': COMPILER.NAME_TO_INDEX,
                                                                                 'indexed_dict': 'skills'},
                                                                'value_compiler': {'compiler': COMPILER.FLOAT}},
                                                 'caps': {'compiler': COMPILER.LIST,
                                                          'default': [],
                                                          'value_compiler': {'compiler': CapsCompiler}},
                                                 'transitions': {'compiler': COMPILER.DICT,
                                                                 'default': {},
                                                                 'key_compiler': {'compiler': COMPILER.NAME_TO_INDEX,
                                                                                  'indexed_dict': 'states'},
                                                                 'value_compiler': {'compiler': COMPILER.DICT}},
                                                 'persistent_effects': {'compiler': COMPILER.DICT,
                                                                        'default': {},
                                                                        'key_compiler': {'compiler': COMPILER.INT},
                                                                        'value_compiler': {'compiler': COMPILER.DICT}},
                                                 STATE_TIMER: {'compiler': COMPILER.CONFIG_LIST,
                                                               'default': [],
                                                               'items': [{'compiler': COMPILER.FLOAT}, {'compiler': COMPILER.NAME_TO_INDEX,
                                                                          'indexed_dict': 'states'}]},
                                                 AGRO_RANGE: {'compiler': COMPILER.FLOAT},
                                                 LOSE_AGRO_RANGE: {'compiler': COMPILER.FLOAT}}}},
           SKILLS: {'compiler': COMPILER.DICT,
                    'default': {},
                    'indexed_keys': True,
                    'key_compiler': {'compiler': COMPILER.NAME_TO_INDEX,
                                     'indexed_dict': 'skills'},
                    'value_compiler': {'compiler': COMPILER.CONFIG,
                                       'copy_dict': True,
                                       'items': {SKILL_TYPE: {'compiler': COMPILER.STRING},
                                                 SKILL_CAST_RANGE: {'compiler': COMPILER.FLOAT},
                                                 SKILL_AOE_RADIUS: {'compiler': COMPILER.FLOAT},
                                                 SKILL_COOLDOWN: {'compiler': COMPILER.FLOAT},
                                                 SKILL_SELF_SFXES: {'compiler': COMPILER.LIST,
                                                                    'default': []},
                                                 SKILL_TARGET_SFXES: {'compiler': COMPILER.LIST,
                                                                      'default': []},
                                                 SKILL_ACTIONS: {'compiler': COMPILER.LIST,
                                                                 'default': []},
                                                 SKILL_EFFECTS: {'compiler': COMPILER.LIST,
                                                                 'default': [],
                                                                 'value_compiler': {'compiler': COMPILER.CONFIG_LIST,
                                                                                    'items': [{'compiler': COMPILER.EFFECT}, {'compiler': COMPILER.INT}]}},
                                                 SKILL_DAMAGE: {'compiler': COMPILER.CONFIG,
                                                                'default': None,
                                                                'items': {DMG_TYPE: {'compiler': COMPILER.DAMAGE},
                                                                          DMG_PENETRATION: {'compiler': COMPILER.FLOAT},
                                                                          DMG_BODY_ZONES: {'compiler': COMPILER.LIST,
                                                                                           'default': [],
                                                                                           'value_compiler': {'compiler': COMPILER.BODY_ZONE}},
                                                                          DMG_VALUE: {'compiler': COMPILER.CONFIG_LIST,
                                                                                      'required': True,
                                                                                      'items': [{'compiler': COMPILER.FLOAT,
                                                                                                 'mult_param': 'skill_dmg_coef'}, {'compiler': COMPILER.FLOAT,
                                                                                                 'mult_param': 'skill_dmg_coef'}]}}}}}}}}

class CreatureConfigCompiler(ConfigCompiler):

    def __init__(self):
        params = {'skill_dmg_coef': stat_rate * stat_base['damage'],
         'health_coef': stat_rate * stat_base['health']}
        ConfigCompiler.__init__(self, config_definition, params=params)