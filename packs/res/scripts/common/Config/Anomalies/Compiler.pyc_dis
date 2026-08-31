# Embedded file name: scripts/common/Config/Anomalies/Compiler.py
from Config.Compiler import ConfigCompiler, DictCompiler, EffectCompiler, ICompiler, COMPILER
from Config.Anomalies.Constants import *
from Config.Anomalies import CommonConfig
from utils_bw import get_enum_from_alias_widget

class DamageDistributionCompiler(ICompiler):

    def compile(self, name, value):
        return DamageDistribution.__dict__[value]


class NudgeTypeCompiler(ICompiler):

    def compile(self, name, value):
        return NudgeType.__dict__[value]


class TerrainCompiler(ICompiler):
    TERRAIN_TYPES = get_enum_from_alias_widget('TERRAIN_TYPE')

    def compile(self, name, value):
        return TerrainCompiler.TERRAIN_TYPES[value]


class AnomalyNameCompiler(ICompiler):

    def compile(self, name, value):
        return CommonConfig.name_to_type[value]


class EffectPairCompiler(ICompiler):

    def compile(self, name, value):
        return dict(id=EffectCompiler().compile('root', value[0]), stacks=value[1])


c = 'compiler'
anomaly_config_definition = {c: COMPILER.CONFIG,
 'items': {'difficultyMin': {c: COMPILER.INT,
                             'default': 3},
           'difficultyMax': {c: COMPILER.INT,
                             'default': 5},
           'lifetime': {c: COMPILER.FLOAT,
                        'mult_param': 'lifetime'},
           'artifacts': {c: COMPILER.LIST,
                         'default': [],
                         'value_compiler': {c: COMPILER.INT}},
           'artifact_spawn_chance': {c: COMPILER.FLOAT,
                                     'default': 1},
           'default_state': {c: COMPILER.NAME_TO_INDEX,
                             'indexed_dict': 'states',
                             'required': True},
           'height_up': {c: COMPILER.FLOAT,
                         'default': 3},
           'height_down': {c: COMPILER.FLOAT,
                           'default': 3},
           'states': {c: COMPILER.DICT,
                      'required': True,
                      'indexed_keys': True,
                      'key_compiler': {c: COMPILER.NAME_TO_INDEX,
                                       'indexed_dict': 'states'},
                      'value_compiler': {c: COMPILER.CONFIG,
                                         'items': {'radius': {c: COMPILER.FLOAT},
                                                   'radiusOut': {c: COMPILER.FLOAT},
                                                   'damage': {c: COMPILER.CONFIG,
                                                              'default': None,
                                                              'items': {'type': {c: COMPILER.DAMAGE,
                                                                                 'required': True},
                                                                        'value': {c: COMPILER.FLOAT,
                                                                                  'required': True},
                                                                        'penetration': {c: COMPILER.FLOAT,
                                                                                        'required': True},
                                                                        'body_zone': {c: COMPILER.BODY_ZONE,
                                                                                      'required': True},
                                                                        'frequency': {c: COMPILER.FLOAT,
                                                                                      'required': True},
                                                                        'distribution': {c: DamageDistributionCompiler,
                                                                                         'required': True}}},
                                                   'effects': {c: COMPILER.LIST,
                                                               'default': [],
                                                               'value_compiler': {c: EffectPairCompiler}},
                                                   'invisible': {c: COMPILER.BOOL,
                                                                 'default': False},
                                                   'hide_delay': {c: COMPILER.FLOAT,
                                                                  'default': 10},
                                                   'nudge_type': {c: NudgeTypeCompiler,
                                                                  'default': 'NONE'},
                                                   'nudge_interval': {c: COMPILER.FLOAT,
                                                                      'default': 0},
                                                   'teleport_enabled': {c: COMPILER.BOOL,
                                                                        'default': False},
                                                   'teleport_shotEnabled': {c: COMPILER.BOOL,
                                                                            'default': False},
                                                   'teleport_cooldown': {c: COMPILER.INT,
                                                                         'default': 1},
                                                   'movement_enabled': {c: COMPILER.BOOL,
                                                                        'default': False},
                                                   'particles': {c: COMPILER.STRING,
                                                                 'default': None},
                                                   'particlesOut': {c: COMPILER.STRING,
                                                                    'default': None},
                                                   'sfx_self': {c: COMPILER.STRING,
                                                                'default': None},
                                                   'sfx_self_interval': {c: COMPILER.LIST_TO_DICT,
                                                                         'default': [0, 1],
                                                                         'items': [['min', {c: COMPILER.FLOAT}], ['max', {c: COMPILER.FLOAT}]]},
                                                   'sfx_target': {c: COMPILER.STRING,
                                                                  'default': None},
                                                   'sound': {c: COMPILER.STRING,
                                                             'default': None}}}}}}
terrains_config_definition = {c: COMPILER.DICT,
 'default': {},
 'key_compiler': {c: TerrainCompiler},
 'value_compiler': {c: COMPILER.LIST,
                    'value_compiler': {c: AnomalyNameCompiler}}}
anomaly_compiler = ConfigCompiler(anomaly_config_definition, params={'lifetime': CommonConfig.base_lifetime})
terrains_compiler = DictCompiler(terrains_config_definition)