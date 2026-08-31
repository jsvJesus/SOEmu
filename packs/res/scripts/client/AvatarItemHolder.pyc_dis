# Embedded file name: scripts/client/AvatarItemHolder.py
from ItemHolder import ItemHolder
import ItemsUtils
from Items import ItemsCatalog

class AvatarItemHolder(ItemHolder):

    def GetFiryingItemParams(self):
        if not ItemsUtils.CheckEquippedItemValidityClient(self):
            return (0.0,
             100.0,
             0,
             0,
             -1,
             0,
             {ItemsCatalog.WEAPON_ACCMOD_LYING: 2.0,
              ItemsCatalog.WEAPON_ACCMOD_AIM_LYING: 1.5,
              ItemsCatalog.WEAPON_ACCMOD_SNIPING_LYING: 1.1,
              ItemsCatalog.WEAPON_ACCMOD_KNEES: 3.0,
              ItemsCatalog.WEAPON_ACCMOD_AIM_KNEES: 2.5,
              ItemsCatalog.WEAPON_ACCMOD_SNIPING_KNEES: 2.0,
              ItemsCatalog.WEAPON_ACCMOD_STAND: 6.0,
              ItemsCatalog.WEAPON_ACCMOD_AIM_STAND: 5.0,
              ItemsCatalog.WEAPON_ACCMOD_SNIPING_STAND: 0.5,
              ItemsCatalog.WEAPON_SCOPEMOD_SNIPING_STAND: 5.0})
        fire_params = []
        fire_params.append(self.CurrentWeaponParam['Accuracy'])
        fire_params.append(self.CurrentWeaponParam['Range'])
        fire_params.append(self.CurrentWeaponParam['NumShots'])
        fire_params.append(self.CurrentWeaponParam['RateOfFire'])
        fire_params.append(self.CurrentWeaponParam['SFXParam'])
        fire_params.append(self.CurrentWeaponParam['FireType'])
        fire_params.append(ItemsUtils.unpackItemDict(self.CurrentWeaponParam['AccStandModsKeys'], self.CurrentWeaponParam['AccStandModsValues']))
        return fire_params

    def onFalseItemInHands(self):
        self.systemChatline('onFalseItemInHands')
        item_id = self.CurrentWeaponParam['ItemID']
        item_type = self.CurrentWeaponParam['ItemType']
        item = ItemsUtils.GetComplexItemByID(self, item_id)
        self.SetEquippedWeaponParams(item_id, item_type, item)

    def GetGrenadeThrowPossibility(self):
        if not ItemsUtils.CheckEquippedGrenadeValidityClient(self):
            return False
        else:
            item = ItemsUtils.GetComplexItemByID(self, self.ActiveGrenadeID)
            if item == None:
                self.cell.wipeItem(self.ActiveGrenadeID)
                return False
            return True

    def onQuestItemAction(self, item_id, quest_id):
        self.cell.QuestItemAction(item_id, quest_id)

    def GetActiveWeaponAccuracyDiff(self):
        if not ItemsUtils.CheckEquippedItemValidityClient(self):
            return ([-3000,
              1200,
              600,
              3500,
              3500],
             0,
             0,
             0)
        itemParam = self.CurrentWeaponParam
        return ([itemParam['AccuracyBorder'],
          itemParam['Kickback'],
          itemParam['AccuracyRecoil'],
          itemParam['MoveAccuracyLost'],
          itemParam['MoveAccuracyLost']],
         itemParam['GunType'],
         itemParam['SkillLevel'],
         self.ActiveItemType)