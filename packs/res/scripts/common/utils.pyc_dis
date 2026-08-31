# Embedded file name: scripts/common/utils.py
import os
import re
import gc
import types
from itertools import ifilter
import traceback
import sys
from collections import defaultdict

def hierarchy_get(fromDict, keys, default = None, use_default = True):
    """
            Works as dict.get, but for hierarchy of dicts/lists and list of keys, respectively.
            If use_default == False then errors will thow instead of returning default
    """
    try:
        if len(keys) == 0:
            return fromDict
    except TypeError:
        if use_default:
            return default
        raise

    try:
        current = fromDict
        for i in xrange(len(keys)):
            current = current[keys[i]]

        return current
    except TypeError as AttributeError:
        if use_default:
            return default
        raise
    except KeyError:
        if use_default:
            return default
        raise


def hierarchy_set(obj, keys, value, create_dicts = False):
    tmp_obj = obj
    for key in keys[:-1]:
        try:
            tmp_obj = tmp_obj[key]
        except KeyError as IndexError:
            if create_dicts:
                tmp_obj[key] = {}
                tmp_obj = tmp_obj[key]
            else:
                raise

    tmp_obj[keys[-1]] = value


def iterate_dict_leaves(d, return_path = False):
    """Iterate through hierarchy of dicts to get leaves"""

    def get_leaf_recursive(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                for inner_obj, inner_key in get_leaf_recursive(value):
                    yield (inner_obj, [key] + inner_key)

        else:
            yield (obj, [])

    for obj, path in get_leaf_recursive(d):
        if return_path:
            yield (obj, path)
        else:
            yield obj


def multi_get(d, *keys, **options):
    """ Return a tuple of values from dict by keys.
            options can have 'default' key (acts as default value in dict.get)
    """
    default = options.get('default')
    return tuple((d.get(key, default) for key in keys))


def hierarchial_update(dict_to, dict_from):
    """Updates a hierarchial dict using another dict. """

    def merge_objects_recursive(object_to, object_from):
        if isinstance(object_to, dict) and isinstance(object_from, dict):
            for key_from, value_from in object_from.items():
                object_to[key_from] = merge_objects_recursive(object_to.get(key_from), value_from)

            return object_to
        else:
            return object_from

    merge_objects_recursive(dict_to, dict_from)


def setattr_dict(object, values_dict):
    for key, value in values_dict.items():
        setattr(object, key, value)


def get_first(predicate, l, default = None):
    """Return first matching element of list, or default if not found."""
    try:
        return ifilter(predicate, l).next()
    except StopIteration:
        return default


def remove_first(predicate, l, default = None):
    """Remove and return first matching element of list, or default if not found."""
    for i, v in enumerate(l):
        if predicate(v):
            return l.pop(i)

    return default


def add_nonexistent(dictTo, dictFrom):
    """Add key:value pairs from dictFrom that are absent in dictTo."""
    for key, value in dictFrom.items():
        if key not in dictTo:
            dictTo[key] = value


def is_identifier(str):
    """Return True if str is valid Python identifier."""
    return bool(re.match(is_identifier.regexp, str))


is_identifier.regexp = re.compile('^[A-Za-z_]+\\w*$')

def dict_get(dictionary, key, default = None):
    """Get for PyFixedDictDataInstance."""
    try:
        return dictionary[key]
    except KeyError:
        return default


def has_branching(d):
    """Retrurn true if hierarchy of d has branching"""
    if isinstance(d, dict):
        if len(d) == 0:
            return False
        if len(d) == 1:
            for val in d.values():
                return has_branching(val)

        else:
            return True
    else:
        return False


def isDictOrFixedDict(val):
    if isinstance(val, dict):
        return True
    if val.__class__.__name__ == 'PyFixedDictDataInstance':
        return True
    return False


def safe_dicts_add(first, second):
    if first is not None and second is not None:
        return first + second
    elif first is not None:
        return first
    elif second is not None:
        return second
    else:
        return
        return


def add_dicts(first_dict, second_dict, custom_add_function = None, before_add_tree_function = None):
    if isDictOrFixedDict(first_dict) and isDictOrFixedDict(second_dict):
        for second_key in second_dict.keys():
            first_dict_value = first_dict.get(second_key)
            second_dict_value = second_dict[second_key]
            if first_dict_value is not None:
                first_dict[second_key] = add_dicts(first_dict_value, second_dict_value, custom_add_function, before_add_tree_function)
            elif before_add_tree_function:
                first_dict[second_key] = before_add_tree_function(second_dict_value)
            else:
                first_dict[second_key] = second_dict_value

        return first_dict
    elif custom_add_function is not None:
        return custom_add_function(first_dict, second_dict)
    else:
        return first_dict + second_dict
        return


def format_exc():
    exctype, ex, tb = sys.exc_info()
    try:
        md, ln, fn = traceback.extract_tb(tb)[-1][:3]
        path, md = os.path.split(md)
        result = '{classname}({message}) at `{modulename}`[line {line}] function `{function}`'.format(classname=ex.__class__.__name__, message=ex.args[0] if ex.args else '', modulename=md, line=ln, function=fn)
    finally:
        exctype = ex = tb = None

    return result


def deque_remove_by_index(dq, idx):
    l = len(dq)
    if idx <= l / 2:
        dq.rotate(-idx)
        dq.popleft()
        dq.rotate(idx)
    else:
        dq.rotate(l - 1 - idx)
        dq.pop()
        dq.rotate(idx - l + 1)


def get_items_count(items, key = lambda k: k):
    """Get a dict of counts, where keys is key(item), default keys == items."""
    res = defaultdict(int)
    for item in items:
        res[key(item)] += 1

    return res


def cached_results(func, _cache = {}):

    def call(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        try:
            return _cache[key]
        except TypeError:
            print "ERROR: can't use unhashable args in <cached_results> decorator.", args, kwargs
            raise
        except KeyError:
            _cache[key] = func(*args, **kwargs)
            return _cache[key]

    return call


def get_funcs_count():
    res = defaultdict(int)
    for obj in gc.get_objects():
        if isinstance(obj, types.FunctionType):
            res[obj.__name__] += 1

    return res


def get_funcs_count_sorted(top = 0, count = 0):
    funcs = [ (k, v) for k, v in get_funcs_count().items() if v > count ]
    return sorted(funcs, key=lambda kv: kv[1])[-top:]


def get_func_count(*func_names):
    """Return a list of funcs objects count, respectively."""
    key = lambda f: f.__name__
    res = [ get_items_count(get_all_funcs(), key=key)[f] for f in func_names ]
    return res


def get_object_by_id(obj_id):
    """Get object by internal Python id."""
    for obj in gc.get_objects():
        if id(obj) == obj_id:
            return obj


def force_unicode(s):
    if isinstance(s, unicode):
        return s
    if isinstance(s, str):
        return s.decode('utf-8')
    raise ValueError()


def force_utf8(s):
    if isinstance(s, str):
        return s
    if isinstance(s, unicode):
        return s.encode('utf-8')
    raise ValueError()


def groupNumber(number, sep = ' '):
    number = str(number)
    aftert = ''
    if '.' in number:
        number, aftert = number.split('.', 1)
    ln = list(number)
    ln.reverse()
    out = []
    for x, n in enumerate(ln):
        out.append(n)
        if x and not (x + 1) % 3 and x + 1 < len(ln):
            out.append(sep)

    out.reverse()
    number = ''.join(out)
    if aftert:
        number += '.' + aftert
    return number