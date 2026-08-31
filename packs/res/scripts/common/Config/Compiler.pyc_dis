# Embedded file name: scripts/common/Config/Compiler.py
import sys
import traceback
import copy
from functools import partial
import utils
from Config.Damage import get_damage_type, get_body_zone
from Config.Effects import get_effect_id
from Localization import lc

class ConfigCompilerError(Exception):
    pass


class ConfigFormatError(ConfigCompilerError):
    pass


class ICompiler:

    def __init__(self, item_def = None, base_compiler = None, **options):
        self.item_def = item_def if item_def is not None else {}
        self.base_compiler = base_compiler
        self.params = options.get('params', {})
        self.indexed_dicts = {}
        self.convert_keys = self.item_def.get('convert_keys', {})
        self.has_default = self.item_def.has_key('default')
        if self.has_default:
            self.default = self.item_def['default']
            if self.item_def.get('compile_default'):
                self.default = self.compile(None, self.default)
        return

    def __str__(self):
        return '{0} {1}'.format(self.__class__, self.item_def)

    def precompile(self, name, value):
        """This phase is using to collect some data from config before compilation."""
        pass

    def compile(self, name, value):
        raise NotImplementedError('ItemCompiler.compile is not implemented.')

    def get_default(self):
        if self.has_default:
            return self.default
        raise ConfigFormatError('No default value specified for {0}'.format(self))

    def get_param(self, name):
        if self.base_compiler is not None:
            return self.base_compiler.get_param(name)
        else:
            return self.params[name]
            return

    def set_param(self, name, value):
        if self.base_compiler is not None:
            self.base_compiler.set_param(name, value)
        else:
            self.params[name] = value
        return

    def init_param_attrib(self, item_pram_name, attrib_name):
        """Init attribute with parameter value defined by item_param_name in item_def"""
        param_name = self.item_def.get(item_pram_name, None)
        if param_name is not None:
            self.__dict__[attrib_name] = self.get_param(param_name)
        else:
            self.__dict__[attrib_name] = None
        return

    def register_indexed_dict(self, dict_name, name_to_ind):
        self.indexed_dicts[dict_name] = name_to_ind

    def get_indexed_dict(self, dict_name):
        dct = self.indexed_dicts.get(dict_name)
        if dct is None and self.base_compiler is not None:
            return self.base_compiler.get_indexed_dict(dict_name)
        else:
            return dct
            return

    def get_index(self, dict_name, dict_key):
        dct = self.get_indexed_dict(dict_name)
        if dct:
            return dct[dict_key]

    def is_generator(self):
        """Return True if this compiler don't require data from config to compile itself."""
        return False

    def generate(self):
        pass


class DirectCompiler(ICompiler):

    def __init__(self, item_def, base_compiler = None, **options):
        pass

    def compile(self, name, value):
        return value


class NumberCompiler(ICompiler):

    def __init__(self, item_def, base_compiler = None, **options):
        ICompiler.__init__(self, item_def, base_compiler, **options)
        self.min = self.item_def.get('min', None)
        self.max = self.item_def.get('max', None)
        self.init_param_attrib('mult_param', 'mult')
        return

    def convert(self, value):
        if self.mult is not None:
            value *= self.mult
        if self.max is not None and value > self.max:
            value = self.max
        if self.min is not None and value < self.min:
            value = self.min
        return value

    def get_default(self):
        return self.convert(ICompiler.get_default(self))


class IntCompiler(NumberCompiler):

    def compile(self, name, value):
        return self.convert(int(value))


class FloatCompiler(NumberCompiler):

    def compile(self, name, value):
        return self.convert(float(value))


class BoolCompiler(ICompiler):

    def compile(self, name, value):
        return bool(value)


class StringCompiler(ICompiler):

    def __init__(self, item_def, base_compiler = None, **options):
        ICompiler.__init__(self, item_def, base_compiler, **options)
        self.init_param_attrib('add_before_param', 'add_before')

    def compile(self, name, value):
        if not isinstance(value, basestring):
            raise ConfigFormatError('StringCompiler: value <' + str(value) + '> is not a string')
        value = str(value)
        if self.add_before is not None:
            value = self.add_before + value
        return value


class ListCompiler(ICompiler):

    def __init__(self, item_def, base_compiler = None, **options):
        ICompiler.__init__(self, item_def, base_compiler, **options)
        value_compiler_def = item_def.get('value_compiler')
        if value_compiler_def:
            value_compiler_class = get_compiler(value_compiler_def)
            self.value_compiler = value_compiler_class(value_compiler_def, self)
        else:
            self.value_compiler = DirectCompiler(value_compiler_def, self)

    def compile(self, name, lst):
        return [ self.value_compiler.compile(name + str(i), value) for i, value in enumerate(lst) ]


class DictCompiler(ICompiler):

    def __init__(self, item_def, base_compiler = None, **options):
        ICompiler.__init__(self, item_def, base_compiler, **options)
        value_compiler_def = item_def.get('value_compiler')
        if value_compiler_def:
            value_compiler_class = get_compiler(value_compiler_def)
            self.value_compiler = value_compiler_class(value_compiler_def, self)
        else:
            self.value_compiler = DirectCompiler(value_compiler_def, self)
        key_compiler_def = item_def.get('key_compiler')
        if key_compiler_def:
            key_compiler_class = get_compiler(key_compiler_def)
            self.key_compiler = key_compiler_class(key_compiler_def, self)
        else:
            self.key_compiler = DirectCompiler(key_compiler_def, self)
        self.need_precompile = item_def.get('indexed_keys', False) and self.base_compiler

    def compile(self, name, dct):
        res = {}
        for key, value in dct.items():
            compiled_key = self.key_compiler.compile(None, key)
            compiled_value = self.value_compiler.compile(key, value)
            res[compiled_key] = compiled_value

        return res

    def precompile(self, name, dct):
        if self.need_precompile:
            names = sorted(dct.keys())
            name_to_ind = dict(((name, i + 1) for i, name in enumerate(names)))
            self.base_compiler.register_indexed_dict(name, name_to_ind)


class ConfigCompiler(ICompiler):

    def __init__(self, item_def, base_compiler = None, **options):
        ICompiler.__init__(self, item_def, base_compiler, **options)
        self.copy_dict = item_def.get('copy_dict')

    def compile(self, name, dct):
        self.value = copy.deepcopy(dct)
        config_compiled = copy.deepcopy(dct) if self.copy_dict else {}
        config_compiled['__name__'] = name
        compilers = {}
        for key, item_def in self.item_def['items'].items():
            compiler_class = get_compiler(item_def)
            compiler = compilers[key] = compiler_class(item_def, self)
            if self.value.has_key(key):
                compiler.precompile(key, self.value[key])
            elif item_def.get('required'):
                raise ConfigFormatError('Item {0} has no required key {1} for {2}'.format(name, key, compiler))

        for key, compiler in compilers.items():
            if self.value.has_key(key):
                try:
                    value = compiler.compile(key, self.value[key])
                except (KeyError,
                 IndexError,
                 ValueError,
                 TypeError) as e:
                    stack = traceback.format_list(traceback.extract_tb(sys.exc_info()[2]))
                    raise ConfigCompilerError((name, key, compiler), e, stack)

            elif compiler.is_generator():
                value = compiler.generate()
            elif compiler.has_default:
                value = compiler.get_default()
            else:
                continue
            config_compiled[self.convert_keys.get(key, key)] = value

        return config_compiled


class ListConfigCompiler(ICompiler):

    def compile(self, name, lst):
        config_compiled = []
        for i, value_def in enumerate(self.item_def['items']):
            compiler_class = get_compiler(value_def)
            compiler = compiler_class(value_def, self)
            value = compiler.compile(name + str(i), lst[i])
            config_compiled.append(value)

        return config_compiled


class ListToDictCompiler(ICompiler):
    """ Example:
            "sfx_self_interval": {
                    "compiler": COMPILER.LIST_TO_DICT,
                    "default": [0,1],
                "items": [
                        ["min", {"compiler": COMPILER.FLOAT}],
                        ["max", {"compiler": COMPILER.FLOAT}],
                    ]
            },
    """

    def compile(self, name, lst):
        config_compiled = {}
        for i, (key, value_def) in enumerate(self.item_def['items']):
            compiler_class = get_compiler(value_def)
            compiler = compiler_class(value_def, self)
            value = compiler.compile(key, lst[i])
            config_compiled[key] = value

        return config_compiled


class NameToIndexCompiler(ICompiler):

    def __init__(self, item_def, base_compiler = None, **options):
        ICompiler.__init__(self, item_def, base_compiler, **options)
        self.indexed_dict_name = item_def['indexed_dict']

    def compile(self, name, value):
        return self.get_index(self.indexed_dict_name, value)


class ItemCompiler(ICompiler):
    from Items import ItemsCatalog

    def compile(self, name, value):
        return getattr(ItemCompiler.ItemsCatalog, value)['TypeID']


class EffectCompiler(ICompiler):

    def compile(self, name, value):
        return get_effect_id(str(value))


class DamageCompiler(ICompiler):

    def compile(self, name, value):
        return get_damage_type(value)


class BodyZoneCompiler(ICompiler):

    def compile(self, name, value):
        return get_body_zone(value)


class LocalizationCompiler(ICompiler):

    def compile(self, name, value):
        return lc(value)


class COMPILER:
    DIRECT, CONFIG, CONFIG_LIST, LIST_TO_DICT, INT, FLOAT, BOOL, STRING, LIST, DICT, NAME_TO_INDEX, ITEM, DAMAGE, BODY_ZONE, EFFECT, LOCALIZATION = xrange(16)


COMMON_COMPILERS = {COMPILER.DIRECT: DictCompiler,
 COMPILER.CONFIG: ConfigCompiler,
 COMPILER.CONFIG_LIST: ListConfigCompiler,
 COMPILER.LIST_TO_DICT: ListToDictCompiler,
 COMPILER.INT: IntCompiler,
 COMPILER.FLOAT: FloatCompiler,
 COMPILER.BOOL: BoolCompiler,
 COMPILER.STRING: StringCompiler,
 COMPILER.LIST: ListCompiler,
 COMPILER.DICT: DictCompiler,
 COMPILER.NAME_TO_INDEX: NameToIndexCompiler,
 COMPILER.ITEM: ItemCompiler,
 COMPILER.DAMAGE: DamageCompiler,
 COMPILER.BODY_ZONE: BodyZoneCompiler,
 COMPILER.EFFECT: EffectCompiler,
 COMPILER.LOCALIZATION: LocalizationCompiler}

def get_compiler(item_def):
    try:
        compiler = item_def['compiler']
    except KeyError:
        print item_def
        raise

    return COMMON_COMPILERS.get(compiler, compiler)