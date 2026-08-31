# Embedded file name: scripts/common/Durations.py
__author__ = 'leviathan'
import ItemsUtils

def GetInformJammDuration(self, jamm_type):
    return 1.0


def GetUnJammDuration(self, unjamm_type):
    return 1.0


def GetReloadDuration(self, reload_type, item_type, num_ammo):
    if reload_type == ItemsUtils.RELOAD_AUTOGUN:
        duration = 3.0
    elif reload_type == ItemsUtils.RELOAD_AUTOGUN_SHORT:
        duration = 2.7
    elif reload_type == ItemsUtils.RELOAD_PISTOL:
        duration = 2.3
    elif reload_type == ItemsUtils.RELOAD_PISTOL_SHORT:
        duration = 2.0
    elif reload_type == ItemsUtils.RELOAD_BULLPUP:
        duration = 3.0
    elif reload_type == ItemsUtils.RELOAD_BULLPUP_BIG_MAGAZINE:
        duration = 4.5
    elif reload_type == ItemsUtils.RELOAD_BULLPUP_SHORT:
        duration = 2.7
    elif reload_type == ItemsUtils.RELOAD_LAUNCHER:
        duration = 5.0
    elif reload_type == ItemsUtils.RELOAD_BREECH_SHOTGUN:
        duration = 1.6 + num_ammo * 0.6
    elif reload_type == ItemsUtils.RELOAD_MANUAL:
        duration = 1.1 + num_ammo * 0.7
    elif reload_type == ItemsUtils.RELOAD_MANUAL_SHORT:
        duration = 0.5 + num_ammo * 0.7
    elif reload_type == ItemsUtils.RELOAD_MACHINEGUN_BELT:
        duration = 6.8
    else:
        duration = 3.0
    return duration * self.getReloadTimeModifyer(reload_type, item_type)


def GetEquipDuration(self, gun_type):
    duration = 1.0
    if gun_type != None:
        return duration * self.getEquipTimeModifyer(gun_type)
    else:
        return 0.0
        return


def GetPutOnDuration(self, equip_item_type, unequip_item_type):
    return 3.0


def GetItemUseDuration(self, item_type):
    return 5.0


def GetGrenadeThrowDuration(self, item_type):
    return 1.2


def GetStoneThrowDuration(self):
    return 0.8


def GetModificationDuration(self):
    return 2.0