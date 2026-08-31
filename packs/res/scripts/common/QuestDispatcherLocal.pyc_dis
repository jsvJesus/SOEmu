# Embedded file name: scripts/common/QuestDispatcherLocal.py
from Localization import lc
import BigWorld
import ResMgr
import Math
import Quest
import GUITextUtils
from copy import copy
import Localization
from Config import Creatures
CONTENTQUESTS = range(10, 16)
QUEST_FILE = 'Quests.xml'
SCENARIO_FILE = 'Scenarios.xml'
RES_PATH_RUS = 'scripts/common/data/Quests/RUS/'
RES_PATH_ENG = 'scripts/common/data/Quests/ENG/'
RES_PATH_SCENARIO = 'scripts/common/data/Quests/'
Quests = {}
Scenarios = {}

def parseAll():
    if not Quests:
        parseQuestsInf()
    if not Scenarios:
        parseScenariosInf()
        fillScenarioQuests()


def parseQuestsInf():

    def parseReputation(input_string):
        ret = []
        if input_string:
            fractions = input_string.split(',')
            for f in fractions:
                fraction_info = f.split(':')
                ret.append(dict(fractionID=int(fraction_info[0]), status=int(fraction_info[1]) if fraction_info[0] else 0))

        return ret

    def getItemsInf(xmlObject):
        ret = []
        for e in xmlObject.values():
            ret.append(dict(title=e['title'].asWideString, description=GUITextUtils.encode(e['description'].asWideString), itemID=e['itemID'].asInt, activation=e['activation'].asWideString))

        return ret

    def getEffectsInf(xmlObject):
        ret = []
        for e in xmlObject.values():
            ret.append(dict(id=e['id'].asInt, stack=e['stack'].asInt))

        return ret

    if Localization.Localization.globalLanguage == 'russian':
        filePath = RES_PATH_RUS + QUEST_FILE
    else:
        filePath = RES_PATH_ENG + QUEST_FILE
    resXML = ResMgr.openSection(filePath)
    ids = []
    for item in resXML.values():
        if item['QuestID'] not in ids:
            ids.append(item['QuestID'].asInt)
            quest = {'Information': {'Title': item['QuestInformation']['Title'].asWideString,
                             'Description': GUITextUtils.encode(item['QuestInformation']['Description'].asWideString),
                             'Items': getItemsInf(item['QuestInformation']['Items']),
                             'NPCs': [],
                             'onWin': item['QuestInformation']['onWin'].asWideString,
                             'onFailed': item['QuestInformation']['onFailed'].asWideString},
             'Target': {'onFin': item['Target']['onFin'].asInt,
                        'QuestType': item['Target']['QuestType'].asInt,
                        'ObjectType': item['Target']['ObjectType'].asInt,
                        'NumOfObjects': item['Target']['NumOfObjects'].asInt,
                        'ObjectName': item['Target']['ObjectName'].asString,
                        'ObjectAttr': item['Target']['ObjectAttr'].asInt,
                        'AObjectAttrs': [ int(subitem) for subitem in item['Target']['AObjectAttrs'].asString.split(',') if subitem != '' ],
                        'IsClan': item['Target']['IsClan'].asInt,
                        'IsGroup': item['Target']['IsGroup'].asInt,
                        'AreaName': item['Target']['AreaName'].asString,
                        'Time': item['Target']['Time'].asFloat},
             'Precondition': {'TakenPeriod': item['Precondition']['TakenPeriod'].asFloat,
                              'Repeat': item['Precondition']['Repeat'].asInt},
             'QuestRules': {'TeleportTo': {'spaceName': item['QuestRules']['TeleportTo'].asString,
                                           'spaceID': 0,
                                           'position': Math.Vector3(0, 0, 0)},
                            'Reputation': item['QuestRules']['Reputation'].asInt,
                            'TypeOfItems': [ int(subitem) for subitem in item['QuestRules']['TypeOfItems'].asString.split(',') if subitem != '' ],
                            'NumOfItems': [ int(subitem) for subitem in item['QuestRules']['NumOfItems'].asString.split(',') if subitem != '' ],
                            'AttrOfItems': [ int(subitem) for subitem in item['QuestRules']['AttrOfItems'].asString.split(',') if subitem != '' ],
                            'Scenarios': [ int(subitem) for subitem in item['QuestRules']['Scenarios'].asString.split(',') if subitem != '' ]},
             'Reward': {'TeleportTo': {'spaceName': item['Reward']['TeleportTo'].asString,
                                       'spaceID': 0,
                                       'position': Math.Vector3(0, 0, 0)},
                        'Expirience': [ float(subitem) for subitem in item['Reward']['Expirience'].asString.split(',') if subitem != '' ],
                        'TypeOfItems': [ int(subitem) for subitem in item['Reward']['TypeOfItems'].asString.split(',') if subitem != '' ],
                        'NumOfItems': [ int(subitem) for subitem in item['Reward']['NumOfItems'].asString.split(',') if subitem != '' ],
                        'AttrOfItems': [ int(subitem) for subitem in item['Reward']['AttrOfItems'].asString.split(',') if subitem != '' ],
                        'Credits': item['Reward']['Credits'].asFloat,
                        'EventCodes': [ int(subitem) for subitem in item['Reward']['EventCodes'].asString.split(',') if subitem != '' ],
                        'Unlimited': item['Reward']['Unlimited'].asInt,
                        'Difficulty': item['Reward']['Difficulty'].asInt,
                        'Fractions': [ int(subitem) for subitem in item['Reward']['Fractions'].asString.split(',') if subitem != '' ],
                        'KarmaPK': item['Reward']['KarmaPK'].asInt,
                        'Effects': getEffectsInf(item['Reward']['Effects'])},
             'Penalty': {'TeleportTo': {'spaceName': item['Penalty']['TeleportTo'].asString,
                                        'spaceID': 0,
                                        'position': Math.Vector3(0, 0, 0)},
                         'Expirience': [ float(subitem) for subitem in item['Penalty']['Expirience'].asString.split(',') if subitem != '' ],
                         'TypeOfItems': [ int(subitem) for subitem in item['Penalty']['TypeOfItems'].asString.split(',') if subitem != '' ],
                         'NumOfItems': [ int(subitem) for subitem in item['Penalty']['NumOfItems'].asString.split(',') if subitem != '' ],
                         'Credits': item['Penalty']['Credits'].asFloat},
             'Additional': {'IsSubQuest': item['Additional']['IsSubQuest'].asInt,
                            'ListOfSubQuest': [ int(subitem) for subitem in item['Additional']['ListOfSubQuest'].asString.split(',') if subitem != '' ],
                            'ShowProgress': item['Additional']['ShowProgress'].asInt,
                            'Holder': item['Additional']['Holder'].asString},
             'QuestID': item['QuestID'].asInt,
             'Version': item['Version'].asInt}
            if quest['Target']['QuestType'] in [Quest.TYPE_KILLMOBS, Quest.TYPE_KILLMOBS_WITH_ONTEST] and quest['Target']['ObjectAttr']:
                new_attr = Creatures.get_subtype_index(quest['Target']['ObjectType'], str(quest['Target']['ObjectAttr']))
                quest['Target']['ObjectAttr'] = new_attr
            Quests[quest['QuestID']] = quest


def parseScenariosInf():
    filePath = RES_PATH_SCENARIO + SCENARIO_FILE
    resXML = ResMgr.openSection(filePath)
    for item in resXML.values():
        if item['id'] not in Scenarios.keys():
            scenario = {'id': item['id'].asInt,
             'type': item['type'].asInt,
             'winif': [ int(subitem) for subitem in item['winif'].asString.split(',') if subitem != '' ],
             'mobs': [ {'type': mob['type'].asInt,
                      'goto': mob['goto'].asInt,
                      'count': mob['count'].asInt,
                      'level': mob['level'].asInt,
                      'update': mob['update'].asInt,
                      'wayName': mob['wayName'].asString} for mob in item['mobs'].values() ],
             'npcs': [ {'type': npc['type'].asInt,
                      'npcName': npc['npcName'].asString,
                      'wayName': npc['wayName'].asString,
                      'id': npc['id'].asInt,
                      'fractionID': npc['fractionID'].asInt} for npc in item['npcs'].values() ],
             'time': item['time'].asFloat}
            Scenarios[scenario['id']] = scenario


def fillScenarioQuests():
    for quest in Quests.values():
        for sID in quest['QuestRules']['Scenarios']:
            scenario = getScenarioOnID(sID)
            if scenario:
                npcs = [ dict(id=e['id'], name=u'') for e in scenario['npcs'] ]
                quest['Information']['NPCs'] += npcs


def getQuestsOnID(quest_id):
    parseAll()
    ret = []
    quest = Quests.get(quest_id)
    if quest:
        ret.append(quest)
        for subquest_id in quest['Additional']['ListOfSubQuest']:
            ret += getQuestsOnID(subquest_id)

    return ret


def getQuestOnID(quest_id):
    parseAll()
    quest = Quests.get(quest_id)
    return quest


def getQuests(quests_ids):
    parseAll()
    quests = []
    for quest_id in quests_ids:
        quest = getQuestOnID(quest_id)
        if quest:
            quests.append(quest)

    return quests


def getCachedQuestOnID(quest_id):
    parseAll()
    quest = copy(getQuestOnID(quest_id))
    if quest:
        quest['Information'] = dict(Items=quest['Information']['Items'], NPCs=quest['Information']['NPCs'], onWin=quest['Information']['onWin'], onFailed=quest['Information']['onFailed'])
        return quest


def getCachedQuestsOnID(quests_ids):
    parseAll()
    ret = copy(getQuestOnID(quests_ids))
    for quest in ret:
        quest['Information'] = dict(Items=quest['Information']['Items'], NPCs=quest['Information']['NPCs'], onWin=quest['Information']['onWin'], onFailed=quest['Information']['onFailed'])

    return ret


def getScenarioOnID(scenario_id):
    parseAll()
    scenario = Scenarios.get(scenario_id)
    return scenario


def getRootID(quest_id):
    parseAll()
    quest = Quests.get(quest_id)
    if quest:
        sub_quest = quest['Additional']['IsSubQuest']
        if sub_quest:
            return getRootID(sub_quest)
    return 0


def getQuestTreeIDs(quest_id):
    parseAll()
    tree = []
    quest = Quests.get(quest_id)
    if quest:
        tree.append(quest_id)
        for subquest_id in quest['Additional']['ListOfSubQuest']:
            tree += getQuestTreeIDs(subquest_id)

    return tree


def getScenario(scenario_id):
    scenario = Scenarios.get(scenario_id)
    return scenario


def loadQuests(questsIDs, cachedIDs, versionIDs):
    parseAll()
    quests = []
    cached_quests = []
    for quest_id in questsIDs:
        quest = getQuestOnID(quest_id)
        if quest:
            if quest_id in cachedIDs and versionIDs[cachedIDs.index(quest_id)] == quest['Version']:
                cached_quest = getCachedQuestOnID(quest_id)
                if cached_quest:
                    cached_quests.append(cached_quest)
            else:
                quest.append(quest)

    return (quests, cached_quests)