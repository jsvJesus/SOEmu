# Embedded file name: scripts/common/Config/AnomalyFields/Compiler.py
from Config import load_json
from Config.Compiler import ConfigCompiler, DictCompiler, COMPILER, ICompiler
from Config.AnomalyFields import CommonConfig
from Config.AnomalyFields.CommonConfig import AF_ANOMALY_PATH
from Config.AnomalyFields.Constants import *
c = 'compiler'

class CellsCompiler(ICompiler):

    def compile(self, name, value):
        return [ map(int, reversed(row.split(','))) for row in value ]


class EffectsCompiler(ICompiler):

    def compile(self, name, value):
        res = []
        for effect in value:
            efData = EffectUtils.getEffect(effect['id'])
            if EffectUtils.SOURCE.EXTERNAL in efData['sources']:
                res.append(self.getEffectSourceDict(effect['id'], effect['stacks'], effect['modifier']))

        return res


class AnomalyDataCompiler(ICompiler):
    anom_data_config_def = {c: COMPILER.CONFIG,
     'items': {ANOM_NAME: {c: COMPILER.STRING,
                           'required': True},
               ANOM_EFFECTS: {c: COMPILER.LIST,
                              'value_compiler': {c: COMPILER.CONFIG,
                                                 'items': {EF_ID: {c: COMPILER.INT,
                                                                   'required': True},
                                                           EF_STACKS: {c: COMPILER.INT,
                                                                       'required': True},
                                                           EF_MODIFIER: {c: COMPILER.FLOAT,
                                                                         'required': True}}}},
               ANOM_SFXES: {c: COMPILER.CONFIG,
                            'items': {SFX_PERSIST: {c: COMPILER.LIST,
                                                    'default': [],
                                                    'value_compiler': {c: COMPILER.STRING}},
                                      SFX_REVEAL: {c: COMPILER.LIST,
                                                   'default': [],
                                                   'value_compiler': {c: COMPILER.STRING}},
                                      SFX_HIDE: {c: COMPILER.LIST,
                                                 'default': [],
                                                 'value_compiler': {c: COMPILER.STRING}},
                                      SFX_WARNING: {c: COMPILER.LIST,
                                                    'default': [],
                                                    'value_compiler': {c: COMPILER.STRING}}}}}}
    data_compiler = ConfigCompiler(anom_data_config_def)

    def compile(self, name, value):
        path = value.get('path')
        if path:
            return AnomalyDataCompiler().compile(name, load_json(AF_ANOMALY_PATH + path))
        else:
            return self.data_compiler.compile(name, value)


pattern_config_definition = {c: COMPILER.CONFIG,
 'items': {CELLS: {c: CellsCompiler},
           GROUPS: {c: COMPILER.DICT,
                    'value_compiler': {c: COMPILER.DICT,
                                       'key_compiler': {c: COMPILER.INT},
                                       'value_compiler': {c: AnomalyDataCompiler}}}}}
lists_config_definition = {c: COMPILER.DICT,
 'value_compiler': {c: COMPILER.LIST,
                    'value_compiler': {c: COMPILER.LIST_TO_DICT,
                                       'items': [[LIST_PATTERN, {c: COMPILER.STRING}], [LIST_GROUP, {c: COMPILER.STRING}]]}}}
pattern_compiler = ConfigCompiler(pattern_config_definition)
lists_compiler = DictCompiler(lists_config_definition)