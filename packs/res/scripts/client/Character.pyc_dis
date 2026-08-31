# Embedded file name: scripts/client/Character.py
"""
Created on 17.08.2010

@author: leviathan
"""
import CharacterUtils
import BigWorld
from Perks import PerkList
from Perks import PerkCatalog
from CharacterUtils import CharacterConst

class Character:

    def GetMaxStamina(self):
        return CharacterUtils.GetMaxStamina(self)

    def CanSniping(self, gun_type):
        return CharacterUtils.CanSniping(self, gun_type)

    def getReloadTimeModifyer(self, gun_type, item_type):
        return CharacterUtils.getReloadTimeModifyer(self, gun_type, item_type)

    def getEquipTimeModifyer(self, gun_type):
        return CharacterUtils.getEquipTimeModifyer(self, gun_type)

    def onGetMaxWeight(self):
        return CharacterUtils.CalculateMaxWeight(self)

    def GetKickbackModifyer(self, gun_type, weapon_mastery, item_type):
        return CharacterUtils.GetKickbackModifyer(self, gun_type, weapon_mastery, item_type)

    def GetAccuracyModifyer(self):
        return CharacterUtils.GetAccuracyModifyer(self)

    def GetMoveShootModifyer(self):
        return CharacterUtils.GetMoveShootModifyer(self)

    def GetThrowModifyer(self):
        return CharacterUtils.GetThrowModifyer(self)

    def GetMaxLaunchedGrenadesNumber(self):
        return CharacterUtils.GetMaxLaunchedGrenadesNumber(self)

    def GetAllStatsList(self):
        list = []
        list.append((CharacterUtils.GetStatistic(self, 'Strength'), 0))
        list.append((CharacterUtils.GetStatistic(self, 'Intelligence'), 0))
        list.append((CharacterUtils.GetStatistic(self, 'Agility'), 0))
        list.append((CharacterUtils.GetStatistic(self, 'Endurance'), 0))
        list.append((CharacterUtils.GetStatistic(self, 'Perception'), 0))
        list.append((CharacterUtils.GetStatistic(self, 'Psy'), 0))
        return list

    def GetSummaryLevel(self):
        return CharacterUtils.GetSummaryLevel(self)

    def addPointsToSkill(self, skill_type, skill_name, value = 1):
        if skill_type == PerkList.COMBAT:
            if self.CombatSkillPoints < value:
                return
        elif skill_type == PerkList.SURVIVAL:
            if self.SurvivalSkillPoints < value:
                return
        elif skill_type == PerkList.OTHER:
            if self.OtherSkillPoints < value:
                return
        self.cell.addPointsToSkill(skill_type, skill_name, value)

    def learnPerk(self, skill_type, skill_name, perk_id):
        if skill_type == PerkList.COMBAT:
            skill_dict = self.CombatSkills
            perk_property = self.CombatPerkPoints
        elif skill_type == PerkList.SURVIVAL:
            skill_dict = self.SurvivalSkills
            perk_property = self.SurvivalPerkPoints
        elif skill_type == PerkList.OTHER:
            skill_dict = self.OtherSkills
            perk_property = self.OtherPerkPoints
        perk = PerkCatalog.GetPerkByID(perk_id)
        if perk['Cost'] > perk_property:
            print 'no perk points'
            return
        if [skill_type, skill_name] in perk['MasterSkill']:
            if perk['NeedSkillValue'] <= skill_dict[skill_name]['SkillValue']:
                for prerequired_perk in perk['Prerequisites']:
                    if prerequired_perk not in skill_dict[skill_name]['PerkList']:
                        break
                else:
                    if perk['PerkType'] not in skill_dict[skill_name]['PerkList'] or perk['Repeatable'] == 1:
                        print 'learning perk'
                        self.cell.addPerkToSkill(skill_type, skill_name, perk_id)
                    else:
                        print 'Already learned'
            else:
                print 'low skill value'
        else:
            print 'not this perk'

    def GetPerkID(self, tree_name, skill_name, feat_pos):
        perk_id = self.SkillVisualData[tree_name][0][skill_name]['PerkList'][feat_pos]
        return perk_id

    def GetPerkStatus(self, tree_name, skill_name, feat_pos):
        perk_id = self.GetPerkID(tree_name, skill_name, feat_pos)
        if perk_id == 0:
            return CharacterConst.PERK_STATUS_LOCKED
        skill_value = self.SkillVisualData[tree_name][0][skill_name]['Value']
        learned_perks = self.SkillVisualData[tree_name][0][skill_name]['LearntPerks']
        perk = PerkCatalog.GetPerkByID(perk_id)
        perk_status = CharacterConst.PERK_STATUS_LOCKED
        if perk['PerkType'] in learned_perks and perk['Repeatable'] == 0:
            perk_status = CharacterConst.PERK_STATUS_KNOWN
        elif perk['NeedSkillValue'] <= skill_value:
            for prerequired_perk in perk['Prerequisites']:
                if prerequired_perk not in learned_perks:
                    break
            else:
                if perk['PerkType'] in learned_perks and perk['Repeatable'] == 1:
                    perk_status = CharacterConst.PERK_STATUS_KNOWN_CAN_TAKE
                else:
                    perk_status = CharacterConst.PERK_STATUS_CAN_TAKE
        return perk_status

    def GetPerkIcon(self, tree_name, skill_name, feat_pos):
        perk_id = self.GetPerkID(tree_name, skill_name, feat_pos)
        if perk_id == 0:
            return ''
        perk = PerkCatalog.GetPerkByID(perk_id)
        return perk['IconName']

    def GetSkillDict(self):

        def FillSkillTreeDict(tree_skills_dict, names_list, TreeID, GetSkillValueFunction, GetPerkValueFunction):

            def GetInsPos(list, value):
                pos = len(list)
                for index in xrange(pos):
                    if list[index] > value:
                        pos = index
                        return pos

                return pos

            def SetPerkToLists(prereqs_list, ids_list, prereq, perk_id):
                insert_position = GetInsPos(prereqs_list, prereq)
                prereqs_list.insert(insert_position, prereq)
                ids_list.insert(insert_position, perk_id)

            for name in names_list:
                skill_dict = {}
                skill_dict['Value'] = GetSkillValueFunction(self, name)
                skill_dict['LearntPerks'] = GetPerkValueFunction(self, name)
                prereqs_list = []
                ids_list = []
                for perk in PerkList.ALL_PERKS.values():
                    if [TreeID, name] in perk['MasterSkill']:
                        SetPerkToLists(prereqs_list, ids_list, perk['NeedSkillValue'], perk['PerkType'])

                preqs_counter = 0
                for preq in CharacterConst.DUMMYS_PERK_PREQ_LIST:
                    if preqs_counter >= CharacterConst.MAX_PERK_NUMBER:
                        break
                    this_preqs = filter(lambda x: x == preq, prereqs_list)
                    if len(this_preqs):
                        preqs_counter += len(this_preqs)
                    else:
                        SetPerkToLists(prereqs_list, ids_list, preq, 0)
                        preqs_counter += 1

                skill_dict['PerkList'] = ids_list
                tree_skills_dict[name] = skill_dict

        combat_skills_dict = {}
        FillSkillTreeDict(combat_skills_dict, CharacterConst.combat_skills_ready_names, PerkList.COMBAT, CharacterUtils.GetCombatSkillValue, CharacterUtils.GetCombatPerkValue)
        surviaval_skills_dict = {}
        FillSkillTreeDict(surviaval_skills_dict, CharacterConst.survival_skills_ready_names, PerkList.SURVIVAL, CharacterUtils.GetSurvivalSkillValue, CharacterUtils.GetSurvivalPerkValue)
        other_skills_dict = {}
        FillSkillTreeDict(other_skills_dict, CharacterConst.other_skills_ready_names, PerkList.OTHER, CharacterUtils.GetOtherSkillValue, CharacterUtils.GetOtherPerkValue)
        combat_expirience = self.CombatExperience
        combat_level = self.CharacterCombatLevel
        combat_skill_points = self.CombatSkillPoints
        combat_perk_points = self.CombatPerkPoints
        survival_expirience = self.SurvivalExperience
        survival_level = self.CharacterSurvivalLevel
        survival_skill_points = self.SurvivalSkillPoints
        survival_perk_points = self.SurvivalPerkPoints
        other_expirience = self.OtherExperience
        other_level = self.CharacterOtherLevel
        other_skill_points = self.OtherSkillPoints
        other_perk_points = self.OtherPerkPoints
        self.SkillVisualData = dict(Combat=[combat_skills_dict,
         combat_expirience,
         combat_level,
         combat_skill_points,
         combat_perk_points], Survival=[surviaval_skills_dict,
         survival_expirience,
         survival_level,
         survival_skill_points,
         survival_perk_points], Other=[other_skills_dict,
         other_expirience,
         other_level,
         other_skill_points,
         other_perk_points])
        return self.SkillVisualData

    def redrawSkillData(self):
        self.UpdateSkill()

    def GetMaxEquippedArtifactNumber(self):
        return CharacterUtils.GetMaxEquippedArtifactNumber(self)