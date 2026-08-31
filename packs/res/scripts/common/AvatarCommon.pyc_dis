# Embedded file name: scripts/common/AvatarCommon.py
__author__ = 'muzhig'
from Items import ItemsCatalog

class AvatarCommon:

    def GetFiringStandAccuracyMod(self, accuracy_mods):
        if self.crouching:
            if self.sniping:
                if self.GetEquippedItemSnipingAbility() != [ItemsCatalog.NONE_TYPE]:
                    stand_mod = accuracy_mods[ItemsCatalog.WEAPON_ACCMOD_SNIPING_KNEES]
                else:
                    stand_mod = accuracy_mods[ItemsCatalog.WEAPON_ACCMOD_AIM_KNEES]
            else:
                stand_mod = accuracy_mods[ItemsCatalog.WEAPON_ACCMOD_KNEES]
        elif self.sniping:
            if self.GetEquippedItemSnipingAbility() != [ItemsCatalog.NONE_TYPE]:
                stand_mod = accuracy_mods[ItemsCatalog.WEAPON_ACCMOD_SNIPING_STAND]
            else:
                stand_mod = accuracy_mods[ItemsCatalog.WEAPON_ACCMOD_AIM_STAND]
        else:
            stand_mod = accuracy_mods[ItemsCatalog.WEAPON_ACCMOD_STAND]
        return stand_mod