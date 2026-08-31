# Embedded file name: scripts/client/Characteristics.py
__author__ = 'leviathan'
import Stats
import BWPersonality
from functools import partial
SHOW_STATS = False

class Characteristics(Stats.CommonCharacteristics):

    def __init__(self):
        for stat_index in xrange(Stats.NUM_STATS):
            stat_name = Stats.CharacteristicsNames[stat_index]
            set_func_name = 'set_ch_' + stat_name
            setattr(self, set_func_name, partial(self.ClientSetFunc, stat_index))

    def ClientSetFunc(self, stat_index, old_value):
        if SHOW_STATS:
            for stat in xrange(Stats.NUM_STATS):
                stat_name = Stats.CharacteristicsNames[stat]
                BWPersonality.GUICore.drawLabel(text=stat_name + ' = ' + str(self.GetStatValue(stat)), id=stat, x=235, y=7 + 13 * stat)

        if stat_index == Stats.ch_MoveSpeed:
            self.UpdateVelocity()