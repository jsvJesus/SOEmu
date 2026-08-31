# Embedded file name: scripts/common/utils_bw.py
import os
import re
import math
import inspect
from random import random
from types import ClassType
import BigWorld
from Math import Vector3, Matrix
import ResMgr
from Localization import lc

def isBaseApp():
    return BigWorld.component == 'base'


def isClient():
    return BigWorld.component == 'client'


def isCellApp():
    return BigWorld.component == 'cell'


def get_class(class_name, module_name = None):
    """
            Loads class by name of class (and module optionally)
    
            >>> get_class('Avatar')
            <class 'Avatar.Avatar'>
            >>> get_class('Avatar.Avatar')
            <class 'Avatar.Avatar'>
            >>> get_class('Anomaly.AnomalyVisitor')
    
            <class 'Anomaly.AnomalyVisitor'>
    
    """
    if module_name is not None:
        class_parts = filter(None, class_name.split('.'))
        module_parts = filter(None, module_name.split('.'))
    else:
        parts = filter(None, class_name.split('.'))
        if not parts:
            return
        module_parts = parts[:-1]
        class_parts = [parts[-1]]
        if module_parts:
            module_name = '.'.join(module_parts)
        else:
            module_name = class_parts[0]
    m = __import__(module_name)
    for module_part in module_parts[1:]:
        m = getattr(m, module_part)

    for class_part in class_parts:
        m = getattr(m, class_part)

    return m


if isBaseApp():

    def is_entity(entity_or_mailbox):
        return isinstance(entity_or_mailbox, (BigWorld.Base, BigWorld.Proxy))


elif isCellApp():

    def is_entity(entity_or_mailbox):
        return isinstance(entity_or_mailbox, BigWorld.Entity)


else:

    def is_entity(entity_or_mailbox):
        return True


def get_classname(obj):
    if hasattr(obj, 'className'):
        if not getattr(obj, 'isDestroyed', None):
            return obj.className
        else:
            return repr(obj).split(' ', 1)[0]
    return obj.__class__.__name__


def if_not_destroyed(func):

    def if_not_destroyed_wrapper(self, *args, **kwargs):
        if not self.isDestroyed:
            return func(self, *args, **kwargs)

    return if_not_destroyed_wrapper


def isinstance_ext(entity_or_mailbox, classes_or_classnames, __cache = {}):
    """
            Extended isinstance
            works on entities, mailboxes
            class objects, classnames, dotted notation of package-module-classname
            
            isinstance_ext(entity,Avatar)
            isinstance_ext(entity,'Avatar')
            isinstance_ext(mailbox,['NPC','Creature'])
            isinstance_ext(mailbox,'AvatarInterface')
            isinstance_ext(mailbox,(Victim,'Damager'))
            isinstance_ext(entity,'Anomaly.AnomalyVisitor')
    """
    if classes_or_classnames.__class__ not in (list, tuple):
        classes_or_classnames = [classes_or_classnames]
    for class_or_classname in classes_or_classnames:
        if class_or_classname.__class__ == str:
            cls = None
            clsname = class_or_classname
        else:
            cls = class_or_classname
            clsname = class_or_classname.__name__
        ent_classname = get_classname(entity_or_mailbox)
        if ent_classname == clsname:
            return True
        cache_key = (ent_classname, clsname)
        if __cache.has_key(cache_key):
            if __cache[cache_key]:
                return True
        else:
            if cls is None:
                cls = get_class(class_or_classname)
            if is_entity(entity_or_mailbox):
                result = isinstance(entity_or_mailbox, cls)
            else:
                check_class = get_class(entity_or_mailbox.className)
                result = issubclass(check_class, cls)
            __cache[cache_key] = result
            if result:
                return True

    return False


def packDict(d):
    """Packs a dict into appropriate FixedDict of arrays."""
    return dict(keys=d.keys(), values=d.values())


def unpackDict(d):
    """Unpacks a dict from appropriate FixedDict of arrays."""
    return dict(zip(d['keys'], d['values']))


def writeDataSectionValue(datasection, key, value):
    """ call valid method on datasection regarding type of value """
    if isinstance(value, bool):
        datasection.writeBool(key, value)
    elif isinstance(value, basestring):
        datasection.writeString(key, value)
    elif isinstance(value, float):
        datasection.writeFloat(key, value)
    elif isinstance(value, int):
        datasection.writeInt(key, value)
    else:
        raise ValueError('This value type is not supported yet')


def printDataSection(data, level = 0):
    for k, v in data.items():
        print ' ' * level, '"' + k + '" : ', v.asString
        if type(v) == ResMgr.DataSection:
            printDataSection(v, level + 4)


def requires_instanceof(cls):

    def decorator(f):

        def wrapper(self, *a, **aa):
            if not isinstance_ext(self, cls):
                raise ValueError('%s must be subclass of %s' % (self.__class__.__name__, cls))
            return f(self, *a, **aa)

        return wrapper

    return decorator


def is_username_valid(username):
    pattern = lc('Account.VALID_USERNAME_REGEX')
    return bool(re.match(pattern, username.lower()))


def entities_in_range(entity, radius, class_names, position = None):
    """ Entity.entitiesInRange for list of classes.
        It was tested (BigWorld 2.0.5) that multiple calls to entitiesInRange with different classes
        is faster than one call to get all entites and manual search after.
    """
    return sum([ entity.entitiesInRange(radius, cls, position) for cls in class_names ], [])


def check_udo_loaded(udo_list, valid_class_names, attrib_name, drop_invalid = False):
    for i, udo in enumerate(udo_list):
        class_name = udo.__class__.__name__
        if class_name == 'UserDataObjectRef':
            return False
        if class_name in valid_class_names:
            try:
                getattr(udo, attrib_name)
            except BigWorld.UnresolvedUDORefException:
                return False

        elif drop_invalid:
            udo_list.pop(i)

    return True


def remove_invalid_udos(udo_list, valid_class_names):
    """Remove all invalid UDOs. UDOs must be loaded before run this func."""
    removed = []
    for i, udo in enumerate(udo_list):
        if udo.__class__.__name__ not in valid_class_names:
            removed.append(udo_list.pop(i))

    return removed


def get_enum_from_alias_widget(param_name):
    section = ResMgr.openSection('scripts/entity_defs/alias.xml/' + param_name + '/Widget')
    res = {}
    for _, v in section.items():
        res[v['display'].asString] = v['value'].asInt

    return res


entities_classes = tuple(ResMgr.openSection('scripts/entities.xml').keys())
if isClient():
    from Helpers.BWCoroutine import BWCoroutine, BWWaitForCondition, BWCoroutineTimeoutException, _BWCoroutineFunction, BWWaitForCoroutine

    @BWCoroutine
    def __wait__(condition_callable, on_success_callable, timeout = None, on_timeout_callable = None):
        try:
            if isinstance(condition_callable, _BWCoroutineFunction):
                yield BWWaitForCoroutine(condition_callable, timeout)
            else:
                yield BWWaitForCondition(condition_callable, timeout)
        except BWCoroutineTimeoutException:
            if callable(on_timeout_callable):
                on_timeout_callable()
            raise StopIteration()

        on_success_callable()


    def wait(condition_callable, on_success_callable, timeout = None, on_timeout_callable = None):
        __wait__(condition_callable, on_success_callable, timeout, on_timeout_callable).run()