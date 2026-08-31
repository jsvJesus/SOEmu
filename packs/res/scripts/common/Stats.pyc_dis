# Embedded file name: scripts/common/Stats.py
__author__ = 'leviathan'
from StatChanges import StatChanges
import cmath
import utils
from functools import partial
from bwdecorators import callableOnGhost
PLUS_INFINITY = float('+inf')
MINUS_INFINITY = float('-inf')
NUM_STATS = 15
ch_HitPoints, ch_MaxHitPoints, ch_CombatPoints, ch_MaxCombatPoints, ch_Stamina, ch_MaxStamina, ch_MoveSpeed, ch_Accuracy, ch_HitPointsRegeneration, ch_StaminaRegeneration, ch_CombatPointsRegeneration, ch_MaxWeight, ch_Defence, ch_Penetration, ch_DamageAbsorb = xrange(NUM_STATS)
LIST_PERMANENT, LIST_TEMPORARY = xrange(2)
CharacteristicsNames = ['HitPoints',
 'MaxHitPoints',
 'CombatPoints',
 'MaxCombatPoints',
 'Stamina',
 'MaxStamina',
 'MoveSpeed',
 'Accuracy',
 'HitPointsRegeneration',
 'StaminaRegeneration',
 'CombatPointsRegeneration',
 'MaxWeight',
 'Defence',
 'Penetration',
 'DamageAbsorb']

def GetDictValueListKey(dict, list_key):
    current_tree = dict
    for key in list_key:
        current_tree = current_tree[key]

    return current_tree


def SetDictValueListKey(dict, list_key, value):
    if len(list_key) < 1:
        return dict
    else:
        current_tree = dict
        for key in list_key[:-1]:
            try_tree = current_tree.get(key)
            if try_tree == None:
                current_tree[key] = {}
                current_tree = current_tree[key]
            else:
                current_tree = try_tree

        current_tree[list_key[-1]] = value
        return SetDictValueListKey(dict, list_key[:-1], current_tree)


def ValueToStat(value):
    create_stat_changer = StatChanges()
    create_stat_changer.before = value
    return create_stat_changer


def ClearStatTempValue(value):
    value['TemporaryOffset'] = 0
    return value


def AddChangeToStat(max_value, min_value, stat_dict, change_dict):
    if change_dict is not None:
        new_value = change_dict.getChangedValue(stat_dict['CurrentValue'])
        if not cmath.isinf(max_value):
            if new_value > max_value:
                new_value = max_value
        if not cmath.isinf(min_value):
            if new_value < min_value:
                new_value = min_value
        stat_dict['TemporaryOffset'] = new_value - stat_dict['CurrentValue']
    return stat_dict


def ConvertStatChangeTreeToStatTree(stat_default_value, tree):

    def ConvertFunc(stat_changer):
        return CreateStatDict(0, stat_changer.getChangedValue(stat_default_value))

    if utils.isDictOrFixedDict(tree):
        return ModifyAllDictValues(tree, ConvertFunc)
    else:
        return ConvertFunc(tree)


def ModifyAllDictValues(input_dict, modify_lambda):
    for key in input_dict:
        entry = input_dict[key]
        if isinstance(entry, dict):
            input_dict[key] = ModifyAllDictValues(entry, modify_lambda)
        else:
            input_dict[key] = modify_lambda(entry)

    return input_dict


def IsEntryComplexStat(entry):
    if entry.has_key('StatKeys') and entry.has_key('StatValues'):
        return True
    return False


def CreateStatDict(value, offset = 0, Maximum = PLUS_INFINITY, Minimum = MINUS_INFINITY):
    return {'CurrentValue': value,
     'TemporaryOffset': offset}


def IsStatDict(dict):
    if dict.has_key('CurrentValue') and dict.has_key('TemporaryOffset'):
        return True
    return False


def convertDictListToArrays(dict_list, create_stat_dict = False):
    return_list = []
    for dict_mb in dict_list:
        if utils.isDictOrFixedDict(dict_mb):
            if IsStatDict(dict_mb):
                return_list.append(dict_mb)
            else:
                keys, values = dict_mb.keys(), dict_mb.values()
                values = convertDictListToArrays(values, create_stat_dict)
                return_list.append({'StatKeys': keys,
                 'StatValues': values})
        elif create_stat_dict:
            return_list.append(CreateStatDict(dict_mb))
        else:
            return_list.append(dict_mb)

    return return_list


def convertArrayListToDicts(array_dict, convert_to_stat_dicts = False, pure = False):
    new_dict = dict(zip(array_dict['StatKeys'], array_dict['StatValues']))
    for index in new_dict.keys():
        dict_value = new_dict[index]
        if IsEntryComplexStat(dict_value):
            new_dict[index] = convertArrayListToDicts(dict_value, convert_to_stat_dicts)
        elif convert_to_stat_dicts:
            new_dict[index] = dict_value
        elif pure:
            new_dict[index] = dict_value['CurrentValue']
        else:
            new_dict[index] = dict_value['CurrentValue'] + dict_value['TemporaryOffset']

    return new_dict


def convertArrayListToDictsOfStatEntryes(array_dict):
    new_dict = dict(zip(array_dict['StatKeys'], array_dict['StatValues']))
    for index in new_dict.keys():
        dict_value = new_dict[index]
        if IsEntryComplexStat(dict_value):
            new_dict[index] = convertArrayListToDicts(dict_value)
        else:
            new_dict[index] = dict_value

    return new_dict


class CommonCharacteristics:

    def doStatWrite(self, stat_entry, stat_change_object, stat_index, default_value, max_value, min_value, complex_return_packed = False):
        if IsEntryComplexStat(stat_entry):
            if stat_change_object == None:
                stat_change_object = {}
            stat_change_object = self.StatChangeLoopback(stat_index, stat_change_object)
            current_stat_dict = convertArrayListToDicts(stat_entry, True)
            ModifyAllDictValues(current_stat_dict, ClearStatTempValue)
            current_stat_dict = utils.add_dicts(current_stat_dict, stat_change_object, custom_add_function=partial(AddChangeToStat, max_value, min_value), before_add_tree_function=partial(ConvertStatChangeTreeToStatTree, default_value))
            if complex_return_packed:
                return convertDictListToArrays([current_stat_dict])[0]
            else:
                return current_stat_dict
        else:
            if stat_change_object == None:
                stat_change_object = StatChanges()
            stat_change_object = self.StatChangeLoopback(stat_index, stat_change_object)
            if stat_change_object is not None:
                new_value = stat_change_object.getChangedValue(stat_entry['CurrentValue'])
                if not cmath.isinf(max_value):
                    if new_value > max_value:
                        new_value = max_value
                        self.OnStatMaxValue(stat_index, new_value)
                if not cmath.isinf(min_value):
                    if new_value < min_value:
                        new_value = min_value
                        self.OnStatMinValue(stat_index, new_value)
                stat_entry['TemporaryOffset'] = new_value - stat_entry['CurrentValue']
            return stat_entry
        return

    def StatGetRoutine(self, stat_index, pure = False):
        if not isinstance(stat_index, list):
            stat_index = [stat_index]
        core_stat_index = stat_index.pop(0)
        stat_name = CharacteristicsNames[core_stat_index]
        property_name = 'ch_' + stat_name
        stat_entry = getattr(self, property_name, None)
        if stat_entry != None:
            if stat_entry.has_key('Default'):
                default = stat_entry['Default']
            else:
                default = None
            if stat_index:
                current_entry_layer = stat_entry
                for current_stat_index in stat_index:
                    current_stat_dict = dict(zip(current_entry_layer['StatKeys'], current_entry_layer['StatValues']))
                    current_entry_layer = current_stat_dict.get(current_stat_index)
                    if current_entry_layer == None:
                        return default

                stat_entry = current_entry_layer
                if current_entry_layer == None:
                    return default
            if IsEntryComplexStat(stat_entry):
                return convertArrayListToDicts(stat_entry, pure=pure)
            elif pure:
                return stat_entry['CurrentValue']
            else:
                return stat_entry['CurrentValue'] + stat_entry['TemporaryOffset']
        return

    def GetStatValue(self, stat_index):
        return self.StatGetRoutine(stat_index)

    def GetStatPureValue(self, stat_index):
        return self.StatGetRoutine(stat_index, pure=True)

    def ChangeStatValue(self, stat_index, stat_change_object):
        """
        Arg: Stat Index (int), Change value(class: StatChange)
        """
        if not isinstance(stat_index, list):
            stat_index = [stat_index]
        core_stat_index = stat_index[0]
        stat_name = CharacteristicsNames[core_stat_index]
        property_name = 'ch_' + stat_name
        stat_entry = getattr(self, property_name, None)
        if stat_entry != None:
            stat_max = stat_entry['Maximum']
            stat_min = stat_entry['Minimum']
            if stat_entry.has_key('Default'):
                default = stat_entry['Default']
            else:
                default = None
            root_stat_point = stat_entry
            if stat_index[1:]:
                stat_dict = convertArrayListToDicts(stat_entry, True)
                current_tree = GetDictValueListKey(stat_dict, stat_index[1:])
                current_tree = self.doStatWrite(current_tree, stat_change_object, stat_index, default, stat_max, stat_min)
                stat_dict = SetDictValueListKey(stat_dict, stat_index[1:], current_tree)
                stat_dict['Maximum'] = stat_max
                stat_dict['Minimum'] = stat_min
                if default is not None:
                    stat_dict['Default'] = default
                setattr(self, property_name, convertDictListToArrays([stat_dict])[0])
            else:
                stat_entry = self.doStatWrite(stat_entry, stat_change_object, stat_index, default, stat_max, stat_min, True)
                stat_entry['Maximum'] = stat_max
                stat_entry['Minimum'] = stat_min
                if default is not None:
                    stat_entry['Default'] = default
                setattr(self, property_name, stat_entry)
        else:
            return
        self.OnStatValueChanged(core_stat_index, self.GetStatValue(core_stat_index))
        return

    def SetStatValue(self, stat_index, new_value):
        """
        For special use. To change stat use ChangeStatValue
        """
        if new_value != None:
            if not isinstance(stat_index, list):
                stat_index = [stat_index]
            core_stat_index = stat_index.pop(0)
            stat_name = CharacteristicsNames[core_stat_index]
            property_name = 'ch_' + stat_name
            stat_entry = getattr(self, property_name, None)
            if stat_entry != None:
                stat_max = stat_entry['Maximum']
                stat_min = stat_entry['Minimum']
                if stat_entry.has_key('Default'):
                    default = stat_entry['Default']
                else:
                    default = None
                if stat_index:
                    old_stat_value = convertArrayListToDicts(stat_entry)
                    curr_tree = old_stat_value
                    for key in stat_index[:-1]:
                        curr_tree = curr_tree[key]

                    curr_tree[stat_index[-1]] = new_value
                    new_value = old_stat_value
                if IsEntryComplexStat(stat_entry):
                    stat_entry = convertDictListToArrays([new_value], True)[0]
                    if default is not None:
                        stat_dict['Default'] = default
                    stat_entry['Maximum'] = stat_max
                    stat_entry['Minimum'] = stat_min
                else:
                    if not cmath.isinf(stat_entry['Maximum']):
                        if new_value > stat_entry['Maximum']:
                            new_value = stat_entry['Maximum']
                            self.OnStatMaxValue(core_stat_index, new_value)
                    if not cmath.isinf(stat_entry['Minimum']):
                        if new_value < stat_entry['Minimum']:
                            new_value = stat_entry['Minimum']
                            self.OnStatMinValue(core_stat_index, new_value)
                    stat_entry['CurrentValue'] = new_value
                    stat_entry['TemporaryOffset'] = 0.0
                setattr(self, property_name, stat_entry)
            else:
                return
            self.OnStatValueChanged(core_stat_index, self.GetStatValue(core_stat_index))
        return

    def SetStatDefaultValue(self, stat_index, value):
        if value != None:
            if isinstance(stat_index, list):
                print 'Default Value can only be set for core complex stat key'
                return
            stat_name = CharacteristicsNames[stat_index]
            property_name = 'ch_' + stat_name
            stat_entry = getattr(self, property_name, None)
            if stat_entry != None:
                if IsEntryComplexStat(stat_entry):
                    stat_entry['Default'] = value
                    setattr(self, property_name, stat_entry)
        return

    def SetStatMaxValue(self, stat_index, value):
        if value != None:
            if isinstance(stat_index, list):
                return
            stat_name = CharacteristicsNames[stat_index]
            property_name = 'ch_' + stat_name
            stat_entry = getattr(self, property_name, None)
            if stat_entry != None:
                stat_entry['Maximum'] = value
                if not cmath.isinf(value):
                    if stat_entry['CurrentValue'] > value:
                        stat_entry['CurrentValue'] = value
                        self.OnStatValueChanged(stat_index, value)
                setattr(self, property_name, stat_entry)
            else:
                print 'No stat', stat_name
                return
        return

    def SetStatMinValue(self, stat_index, value):
        if value != None:
            if isinstance(stat_index, list):
                return
            stat_name = CharacteristicsNames[stat_index]
            property_name = 'ch_' + stat_name
            stat_entry = getattr(self, property_name, None)
            if stat_entry != None:
                stat_entry['Minimum'] = value
                if not cmath.isinf(value):
                    if stat_entry['CurrentValue'] < value:
                        stat_entry['CurrentValue'] = value
                        self.OnStatValueChanged(stat_index, value)
                setattr(self, property_name, stat_entry)
            else:
                print 'No stat', stat_name
                return
        return

    def InitStat(self, stat_index):
        self.SetStatMaxValue(stat_index, PLUS_INFINITY)
        self.SetStatMinValue(stat_index, MINUS_INFINITY)
        stat_name = CharacteristicsNames[stat_index]
        init_func_name = 'Init' + stat_name + 'Stat'
        initial_val = self.StartEventRoutine(init_func_name, stat_index)
        if initial_val != None:
            self.SetStatValue(stat_index, initial_val)
        self.ChangeStatValue(stat_index, None)
        return

    def StartEventRoutine(self, event_func_name, stat_index, param = None):
        func = getattr(self, event_func_name, None)
        if func:
            ret_value = func(stat_index) if param == None else func(stat_index, param)
            return ret_value
        else:
            return param

    def OnStatMinValue(self, stat_index, new_value):
        if isinstance(stat_index, list):
            core_index = stat_index[0]
        else:
            core_index = stat_index
        event_func_name = 'On' + CharacteristicsNames[core_index] + 'MinValue'
        self.StartEventRoutine(event_func_name, stat_index)

    def OnStatMaxValue(self, stat_index, new_value):
        if isinstance(stat_index, list):
            core_index = stat_index[0]
        else:
            core_index = stat_index
        event_func_name = 'On' + CharacteristicsNames[core_index] + 'MaxValue'
        self.StartEventRoutine(event_func_name, stat_index)

    def StatChangeLoopback(self, stat_index, stat_change_object):
        if isinstance(stat_index, list):
            core_index = stat_index[0]
        else:
            core_index = stat_index
        event_func_name = 'On' + CharacteristicsNames[core_index] + 'ChangeLoopback'
        return self.StartEventRoutine(event_func_name, stat_index, stat_change_object)

    def OnStatValueChanged(self, stat_index, new_value):
        if isinstance(stat_index, list):
            core_index = stat_index[0]
        else:
            core_index = stat_index
        event_func_name = 'On' + CharacteristicsNames[core_index] + 'Changed'
        self.StartEventRoutine(event_func_name, stat_index, new_value)
        self.EventOnStatChanged(stat_index, new_value)

    def EventOnStatChanged(self, stat_index, new_value):
        pass