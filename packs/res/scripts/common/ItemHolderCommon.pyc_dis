# Embedded file name: scripts/common/ItemHolderCommon.py
__author__ = 'Leviathan'
import ItemsUtils
from Items import ItemsCatalog

class ItemHolderCommon:

    def GetMaxEquippedArtifactNumber(self):
        return 0

    def CheckEquippedArtifactNumber(self):
        if len(self.ActiveArtifactList) >= self.GetMaxEquippedArtifactNumber():
            return False
        return True

    def GetMaxItemStorageNumber(self, trader_name):
        return ItemsUtils.DEFAULT_TRADER_STORAGE_SPACE

    def GetEquippedItemSnipingAbility(self):
        if self.ActiveItemType:
            equipped_item_param = ItemsCatalog.GetItemParam(self.ActiveItemType)
            gun_type = equipped_item_param['GunType']
            gun_priority = ItemsUtils.GetWeaponPriority(gun_type)
            if gun_priority == ItemsCatalog.SECONDARY:
                upgrade_dict = self.SecondaryWeaponUpgrades
            else:
                upgrade_dict = self.PrimaryWeaponUpgrades
            if upgrade_dict['ScopeType'] > 0:
                scope_item_param = ItemsCatalog.GetItemParam(upgrade_dict['ScopeType'])
                scope_type = scope_item_param['ScopeType']
            else:
                scope_type = equipped_item_param['ScopeType']
            if not isinstance(scope_type, list):
                scope_type = [scope_type]
            return scope_type

    def GetEquippedItemSnipingNightVisionAbility(self):
        if self.ActiveItemType:
            for item in self.CarryingItems:
                if item['complexItemType'] == self.ActiveItemType:
                    for subitem in item['itemList']:
                        subitem_param = ItemsCatalog.GetItemParam(subitem['itemType'])
                        if subitem_param.has_key('isNightVision') and subitem_param['isNightVision']:
                            return True