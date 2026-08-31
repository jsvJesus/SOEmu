# Embedded file name: scripts/client/Quester.py
"""
Created on 02.09.2010

@author: Madcat
"""
import BigWorld
import Dialog
import Helpers.Caps
import Math
from Helpers.Caps import CAP_CAN_GIVE_QUEST
import BWPersonality
from soGUI.soQuestLog import soQuestLog
from soGUI.soTPCQuestLog import soTPCQuestLog
import Quest
import colorCodes
import PVPConst
import soGUI
import Config
from Items import ItemsCatalog
import re
import Dialog
import ResMgr
import gui_jokes
from Localization import lc
import DialogsDispatcherLocal as dd
import QuestDispatcherLocal as qd
import ItemsUtils

class Quester:
    groupOwnerMailbox = None
    selectedQuest = 0
    isDialogEventsOver = True
    NEXTREQUEST = dict(QuestID=Quest.JOURNAL_ID_NEXT, Title=colorCodes.questlog_next + lc('Quests.Journal.NEXT_TEN_BUTTON'))
    tutorialIDs = []
    tutorial_owner = 0
    ClientQuests = {}

    def __init__(self):
        self.ClientQuests = {}

    def tutorialGUIListener(self, event, data):
        if not self.passTutorial:
            self.cell.guiQuestCheck(data, event)

    def loadQuests(self):
        self.cell.loadQuests()

    def ManipulateQuesterTarget(self, entity):
        if entity:
            if getattr(entity, 'isDisableDialogs', 0):
                self.systemMessage('NPC disabled', 4294901760L)
                return
            if Helpers.Caps.CAP_CAN_TALK in entity.targetCaps or Helpers.Caps.CAP_CAN_USE in entity.targetCaps and 'npcDialogueGUI' not in BWPersonality.GUICore.getGUIMap():
                cachedIDs = [[], []]
                if hasattr(entity, 'npcName'):
                    cachedIDs = BWPersonality.cache.getDialogIDs(entity.npcName)
                elif hasattr(entity, 'triggerName'):
                    cachedIDs = BWPersonality.cache.getDialogIDs(entity.triggerName)
                self.cell.onStartTalk(entity.id, 0, Dialog.GET_WITH_CHECK, cachedIDs[0], cachedIDs[1])

    def updateJournal(self, quests):
        print 'Quester::updateJournal {0}'.format(quests)
        if self.selectedQuest in quests:
            print 'if self.selectedQuest in quests:'
            BWPersonality.GUICore.setQuestDescription(' ')
            self.base.getDescription(self.selectedQuest)

    def questLogHandler(self, data, event):
        if event == soQuestLog.EVENT_SELECT:
            self.selectedQuest = data
            BWPersonality.GUICore.setQuestDescription(' ')
            if data == Quest.JOURNAL_ID_NEXT:
                list_completed_quests = [ quest['QuestID'] for quest in self.ClientQuests.values() if quest['State'] == Quest.STATE_CLOSED and not quest['Additional']['IsSubQuest'] ]
                if list_completed_quests:
                    self.base.getNextTenCompleted(list_completed_quests)
            elif data:
                quest = self.getQuest(data)
                if quest and (quest['State'] == Quest.STATE_OPENED or quest['State'] == Quest.STATE_ONTEST):
                    self.base.getDescription(data)
                elif quest:
                    BWPersonality.GUICore.setQuestDescription(quest['Information']['Description'])
        elif event == soQuestLog.EVENT_CANCEL:
            quest = self.getQuest(self.selectedQuest)
            if quest and quest['State'] not in [Quest.STATE_CLOSED, Quest.STATE_FREEZ]:

                def listener(event):
                    if event == gui_jokes.askUserYesNoDelayDeafultNo.YES:
                        self.chooseCloseDialog(True, True)
                        self.base.removeQuestFromJournal(self.selectedQuest)
                        BWPersonality.GUICore.setQuestDescription(' ')

                quest = self.getQuest(self.selectedQuest)
                cancel_header = lc('Quests.Journal.CANCEL_QUEST_HEADER')
                cancel_question = lc('Quests.Journal.CANCEL_QUEST_QUESTION')
                gui_jokes.askUserYesNoDelayDeafultNo(cancel_header, cancel_question.format(quest['Information']['Title']), listener, 10.0)
        elif event == soQuestLog.EVENT_SHARE:
            pass

    def takeDescription(self, questIDs, descriptionList):
        rootID = questIDs[0]
        rootQuest = self.getQuest(rootID)
        if rootQuest:
            if rootQuest['Additional']['ShowProgress'] & Quest.SHOW_TUTORIAL:
                if rootQuest['Additional']['IsSubQuest'] == 0:
                    onSend = self.takeSubDescription(questIDs, descriptionList, rootQuest['QuestID'])
                    self.showTutorial(onSend)
            else:
                onSend = self.takeSubDescription(questIDs, descriptionList, self.selectedQuest)
                BWPersonality.GUICore.setQuestDescription(u' ')
                BWPersonality.GUICore.setQuestDescription(onSend)

    def takeSubDescription(self, questIDs, descriptionList, targetQuest):
        res = ''
        quest = self.getQuest(targetQuest)
        if quest:
            for index, id in enumerate(questIDs):
                if id == targetQuest:
                    description = self.gatherDescription(id, descriptionList[index])
                    if description:
                        res += '<n>' + description + '<n>'

            for subquestID in quest['Additional']['ListOfSubQuest']:
                res += self.takeSubDescription(questIDs, descriptionList, subquestID)

        return res

    def sendJournalInfo(self):
        opened = []
        closed = []
        state_msg = lc('Quests.Journal.STATE_FAILED')
        obj_infos = []
        for quest_id in self.ClientQuests:
            quest = self.getQuest(quest_id)
            obj_info = dict(id=quest_id, quest_type=quest['Target']['QuestType'], object_type=quest['Target']['ObjectType'], state=quest['State'])
            obj_infos.append(obj_info)
            if not quest['Additional']['IsSubQuest'] and quest['Additional']['ShowProgress'] & Quest.SHOW_JOURNAL:
                if quest['State'] == Quest.STATE_OPENED or quest['State'] == Quest.STATE_ONTEST:
                    opened.append(dict(Title=quest['Information']['Title'], QuestID=quest['QuestID']))
                elif quest['State'] == Quest.STATE_FAILED:
                    opened.append(dict(Title=colorCodes.journal_failedtitle + state_msg + colorCodes.journal_title + quest['Information']['Title'], QuestID=quest['QuestID']))
                else:
                    closed.append(dict(Title=quest['Information']['Title'], QuestID=quest['QuestID']))

        self.QuestObjInfo = obj_infos
        BWPersonality.GUICore.questLogData(opened, soTPCQuestLog.MODE_CURRENT)
        if closed:
            closed.append(self.NEXTREQUEST)
        BWPersonality.GUICore.questLogData(closed, soTPCQuestLog.MODE_COMPLETED)

    def gatherDescription(self, questID, desciption):
        quest = self.getQuest(questID)
        if quest:
            sAdd = u''
            if not quest['Additional']['IsSubQuest'] or quest['Additional']['ShowProgress'] and desciption:
                res = desciption.split(',')
                q_type = int(res[0])
                if q_type in [Quest.TYPE_KILLMOBS_WITH_ONTEST, Quest.TYPE_KILLMOBS]:
                    sAdd += lc('Quester.YOU_HAVE_KILLED') + res[1] + u'/' + res[2] + u'.'
                if q_type in [Quest.TYPE_FARM_AUTO, Quest.TYPE_FARM]:
                    sAdd += lc('Quester.YOU_HAVE_COLLECT') + res[1] + u'/' + res[2] + u'.'
                if sAdd:
                    sAdd = u'<n><alignment=right>' + sAdd
            description = quest['Information']['Description']
            if description:
                description = u'<alignment=left>' + colorCodes.tf3_journal_text + description + sAdd
            return description

    def startDialog(self, interactive_name, dialogs, cachedDialogs, orderIDs, sourceEntityID):
        dialogs = dd.getDialogs(interactive_name, dialogs)
        cachedDialogs = dd.getCachedDialogs(interactive_name, cachedDialogs)
        for cached_dialog in cachedDialogs:
            info = BWPersonality.cache.getCacheDialog(interactive_name, cached_dialog['DialogID'])
            cached_dialog = dict(cached_dialog)
            cached_dialog['Text'] = info['text']
            cached_dialog['Title'] = info['title']
            dialogs.append(cached_dialog)

        result = []
        for id in orderIDs:
            for dialog in dialogs:
                if dialog['DialogID'] == id:
                    result.append(dialog)
                    continue

        self.showGetQuestDialog(result, sourceEntityID)

    def checkQuestOver(self, questID):
        if 'CompleteQuest' in self.queryDialogRequest.keys():
            if questID in self.queryDialogRequest['CompleteQuest']:
                self.queryDialogRequest['CompleteQuest'].remove(questID)
            if not self.queryDialogRequest['CompleteQuest']:
                del self.queryDialogRequest['CompleteQuest']
                if self.dialogChoosenButton:
                    if self.isDialogEventsOver:
                        self.ContinueDialog()
                    else:
                        self.ContinueSameDialog()
                    self.isDialogEventsOver = True

    def checkQuestNotOver(self, questID):
        self.isDialogEventsOver = False
        if 'CompleteQuest' in self.queryDialogRequest.keys():
            if questID in self.queryDialogRequest['CompleteQuest']:
                self.queryDialogRequest['CompleteQuest'].remove(questID)
            if not self.queryDialogRequest['CompleteQuest']:
                del self.queryDialogRequest['CompleteQuest']
                if self.dialogChoosenButton:
                    if self.isDialogEventsOver:
                        self.ContinueDialog()
                    else:
                        self.ContinueSameDialog()
                    self.isDialogEventsOver = True

    def checkQuestGetted(self, questID):
        if 'GetQuest' in self.queryDialogRequest.keys():
            if questID in self.queryDialogRequest['GetQuest']:
                self.queryDialogRequest['GetQuest'].remove(questID)
            if not self.queryDialogRequest['GetQuest']:
                del self.queryDialogRequest['GetQuest']
                if self.dialogChoosenButton:
                    self.questerRequestCompleted()

    def closeDialog(self):
        self.chooseCloseDialog(True, True)
        data = [0]
        stringData = []
        self.tellAboutQuesterStatus(data, stringData, Quest.STATUS_NPC_IS_TOO_FAR)

    def replaceConst(self, quest):
        description_matches = re.findall('%NPC[0-9]+%', quest['Information']['Description'])
        if description_matches:
            for e in description_matches:
                id = int(e.replace('NPC', '').replace('%', ''))
                name = self.getNPCName(quest, id)
                quest['Information']['Description'] = quest['Information']['Description'].replace(e, name)

        return quest

    def getNPCName(self, quest, id):
        for e in quest['Information']['NPCs']:
            if e['id'] == id:
                return e['name']

        return u''

    def takeClientQuests(self, quests, cached_quests, order):
        for i, q in enumerate(quests):
            temp = qd.getQuestOnID(q['QuestID'])
            quests[i]['Information']['Title'] = temp['Information']['Title']
            quests[i]['Information']['Description'] = temp['Information']['Description']

        def get_quest(quests, quest_id):
            for quest in quests:
                if quest['QuestID'] == quest_id:
                    return quest

        for cached_quest in cached_quests:
            cache = BWPersonality.cache.getCacheQuest(cached_quest['Additional']['Holder'], cached_quest['QuestID'])
            if cache:
                cached_quest = dict(cached_quest)
                cached_quest['Information'] = dict(cached_quest['Information'])
                cached_quest['Information']['Title'] = cache['title']
                cached_quest['Information']['Description'] = cache['description']
                quests.append(cached_quest)

        resorted = []
        for quest_id in order:
            quest = get_quest(quests, quest_id)
            if quest:
                resorted.append(quest)

        quests = resorted
        for quest_id in order:
            if quest_id in self.ClientQuests:
                self.ClientQuests.pop(quest_id)

        for quest in quests:
            quest = self.replaceConst(quest)
            quest_id = quest['QuestID']
            if quest['State'] in [Quest.STATE_ONTEST, Quest.STATE_OPENED]:
                self.checkQuestGetted(quest['QuestID'])
            self.ClientQuests[quest_id] = quest
            self.base.onQLoadFin(quest['QuestID'])
            if quest['Additional']['ShowProgress'] & Quest.SHOW_TUTORIAL:
                if quest['Additional']['IsSubQuest'] == 0:
                    if not self.passTutorial and not self.tutorialIDs:
                        BWPersonality.GUICore.addListener('generalGUIEvent', self.tutorialGUIListener)
                        BWPersonality.GUICore.addListener('hlinkEvent', self.tutorialListener)
                    if quest['QuestID'] not in self.tutorialIDs:
                        self.tutorialIDs.append(quest['QuestID'])
                        self.base.getDescription(quest['QuestID'])
                else:
                    root_id = self.getRootID(quest['QuestID'])
                    if root_id:
                        self.base.getDescription(root_id)

        self.sendJournalInfo()
        self.base.onTakeQuestsOnClient(order)
        BWPersonality.cache.saveCacheQuest()
        for id in order:
            self.onQStateChange(id)

    def removeClientQuest(self, questID, reason):
        inTutorial = False
        quest = self.getQuest(questID)
        if quest:
            if quest['Additional']['ShowProgress'] & Quest.SHOW_TUTORIAL:
                inTutorial = True
            if reason == Quest.DEL_ONWIN:
                if quest['Additional']['ShowProgress'] & Quest.SHOW_ONWIN:
                    self.tellAboutQuesterStatus([questID], [], Quest.STATUS_ONWIN)
                if quest['Additional']['ShowProgress'] & Quest.SHOW_MESSAGE_CLOSE and not quest['Additional']['IsSubQuest']:
                    self.tellAboutQuesterStatus([questID], [], Quest.STATUS_CLOSED)
                if questID == self.selectedQuest:
                    BWPersonality.GUICore.setQuestDescription(' ')
                    self.selectedQuest = 0
                quest['State'] = Quest.STATE_CLOSED
                self.onQStateChange(questID)
            if reason == Quest.DEL_ONFAILED:
                if quest['Additional']['ShowProgress'] & Quest.SHOW_ONFAILED:
                    self.tellAboutQuesterStatus([questID], [], Quest.STATUS_ONFAILED)
                if quest['Additional']['ShowProgress'] & Quest.SHOW_MESSAGE_CLOSE and not quest['Additional']['IsSubQuest']:
                    self.tellAboutQuesterStatus([questID], [], Quest.STATUS_FAILED)
                if questID == self.selectedQuest:
                    BWPersonality.GUICore.setQuestDescription(' ')
                    self.selectedQuest = 0
                quest['State'] = Quest.STATE_FAILED
                self.onQStateChange(questID)
            if reason == Quest.DEL_ONWIN:
                if not quest['Additional']['IsSubQuest']:
                    quest['State'] = Quest.STATE_CLOSED
                else:
                    quest['State'] = Quest.STATE_CLOSED
                self.onQStateChange(questID)
            elif reason == Quest.DEL_ONFAILED:
                quest['State'] = Quest.STATE_FAILED
                self.onQStateChange(questID)
            else:
                self.ClientQuests.pop(questID)
                self.onQRemove(questID)
        if inTutorial and questID in self.tutorialIDs:
            self.tutorialIDs.remove(questID)
            if not self.tutorialIDs:
                self.hideTutorial()
            else:
                self.base.getDescription(self.tutorialIDs[-1])
        self.sendJournalInfo()
        self.checkQuestOver(questID)

    def getQuest(self, questID):
        quest = self.ClientQuests.get(questID)
        return quest

    def getQItemInfo(self, questID, itemID):
        quest = self.getQuest(questID)
        if quest:
            for item in quest['Information']['Items']:
                if item['itemID'] == itemID:
                    return (item['title'], item['description'], item['activation'])

        return None

    def getQTitle(self, questID):
        quest = self.getQuest(questID)
        if quest:
            return quest['Information']['Title']
        else:
            return None

    def getRootID(self, quest_id):
        quest = self.getQuest(quest_id)
        if quest:
            root_id = quest['Additional']['IsSubQuest']
            if not root_id:
                return quest_id
            else:
                return self.getRootID(root_id)

    def askOnJoinToGroup(self, ownerName):
        self.showGroupInvite(ownerName)

    def joinInGroup(self):
        self.base.joinInGroup()
        self.groupOwnerMailbox = None
        return

    def askOnGetReady(self):
        self.showGetReady()

    def askOnStartGroupQuest(self):
        self.showStartGroupQuest()

    def tellAboutQuesterStatus(self, data, stringData, status):

        def getItemName(itemID, attr):
            name = u''
            item = self.getQItemInfo(questID, itemID)
            if attr and item:
                name = item[0]
            if not name:
                name = ItemsUtils.GetItemName(itemID)
            return name

        def getCreatureName(mob_type, mob_level):
            return Config.Creatures.get_mob_name(mob_type, mob_level)

        message = u''
        questID = data[0]
        quest = self.getQuest(questID)
        if status == Quest.STATUS_WIPE_OVER:
            message = lc('Quests.Messages.WIPE_COMPLETE')
        elif status == Quest.STATUS_OPENED and quest:
            message = lc('Quests.Messages.MISSION_TAKEN').format(quest['Information']['Title'])
        elif status == Quest.STATUS_CLOSED and quest:
            message = lc('Quests.Messages.MISSION_COMPLETE').format(quest['Information']['Title'])
        elif status == Quest.STATUS_FAILED and quest:
            message = lc('Quests.Messages.MISSION_FAILED').format(quest['Information']['Title'])
        elif status == Quest.STATUS_SUCCESSFULL_COLLECT_ITEMS:
            questID, itemID, attr = data
            name = getItemName(itemID, attr)
            message = lc('Quests.Messages.COLLECT_COMPLETE').format(name)
        elif status == Quest.STATUS_ONPROCESS_COLLECT_ITEMS:
            questID, itemID, attr, numOfItem, needOfItem = data
            name = getItemName(itemID, attr)
            numOfItem = needOfItem if numOfItem > needOfItem else numOfItem
            message = lc('Quests.Messages.COLLECT_PROCESS').format(str(numOfItem), str(needOfItem), name)
        elif status == Quest.STATUS_FAILED_COLLECT_ITEMS:
            questID, itemID, attr = data
            name = getItemName(itemID, attr)
            message = lc('Quests.Messages.COLLECT_FAILED').format(name)
        elif status == Quest.STATUS_SUCCESSFULL_KILLED_CREATURE:
            questID, mobID, mobAttr = data
            name = getCreatureName(mobID, mobAttr)
            message = lc('Quests.Messages.FARM_COMPLETE').format(name)
        elif status == Quest.STATUS_ONPROCESS_KILLED_CREATURE:
            questID, mobID, mobAttr, count, neededCount = data
            name = getCreatureName(mobID, mobAttr)
            message = lc('Quests.Messages.FARM_PROCESS').format(str(count), str(neededCount), name)
        elif status == Quest.STATUS_NEED_MORE_MONEY:
            message = lc('Quests.Messages.MONEY_FAILED')
        elif status == Quest.STATUS_AREA_FOUNDED:
            areaName = stringData[0]
            message = lc('Quests.Messages.AREA_COMPLETED').format(areaName)
        elif status == Quest.STATUS_CANT_TELEPORT_TO_INSTANCE:
            message = lc('Quests.Messages.PARTI_INSTANCE_LEADER_ONLY')
        elif status == Quest.STATUS_NO_FREE_INSTANCE:
            message = lc('Quests.Messages.SERVER_TOO_BUSY')
        elif status == Quest.STATUS_ONWIN:
            message = quest['Information']['onWin']
        elif status == Quest.STATUS_ONFAILED:
            message = quest['Information']['onFailed']
        elif status == Quest.STATUS_JOURNAL_RENEW:
            message = lc('Quests.Messages.JOURNAL_UPDATED')
        elif status == Quest.STATUS_NPC_IS_TOO_FAR:
            message = lc('Quests.Messages.TOO_FAR')
        elif status == Quest.STATUS_CANT_TAKE_MISSION_NOW:
            message = lc('Quests.Messages.CANT_TAKE_MISSION_NOW').format(stringData[0], data[0], data[1])
        if message:
            self.questerMessageToConsole(message)

    def questerMessageToConsole(self, string):
        self.questChatline(string)

    def requestCache(self, quests_ids, versions):
        quest_ids = []
        cached_quest_ids = []
        for index, quest_id in enumerate(quests_ids):
            version = versions[index]
            quest = BWPersonality.cache.getCacheQuestOnID(quest_id)
            if not quest or quest['ver'] != version:
                quest_ids.append(quest_id)
            else:
                cached_quest_ids.append(quest_id)

        self.base.takeQuestsOnClient(quest_ids, cached_quest_ids)

    def startPVPPeriod(self, period, time):
        if period:
            BWPersonality.GUICore.showTimer(time, str(period), True)
        else:
            BWPersonality.GUICore.showTimer(0.0, '', False)

    def takePVPStat(self, type, id):
        if type == PVPConst.CLEAR_TYPE:
            self.PVPStatistic['users'] = []
            self.PVPStatistic['commands'] = []
            return
        if type == PVPConst.INC_COMMAND_WIN:
            for e in self.PVPStatistic['commands']:
                if e['command'] == id:
                    e['count'] += 1
                    return

            self.PVPStatistic['commands'].append(dict(command=id, count=1))
            for e in self.PVPStatistic['users']:
                e['counter'] = 0

            return
        for e in self.PVPStatistic['users']:
            if e['id'] == id:
                if type == PVPConst.INC_TYPE_DEATH:
                    e['deaths'] += 1
                elif type == PVPConst.INC_TYPE_FRAG:
                    e['counter'] += 1
                return

        self.PVPStatistic['users'].append(dict(id=id, name=u'', counter=1 if type == PVPConst.INC_TYPE_FRAG else 0, deaths=1 if type == PVPConst.INC_TYPE_DEATH else 0, command=0))
        self.cell.getPVPStatInfo(id)

    def takePVPStatInfo(self, infos):
        for info in infos:
            find = False
            for e in self.PVPStatistic['users']:
                if e['id'] == info['id']:
                    e['name'] = info['name']
                    e['command'] = info['command']
                    find = True
                    break

            if not find:
                self.PVPStatistic['users'].append(info)

    def showPVPStatistic(self):
        battleName = u''
        command = 0
        enemyName = lc('Quester.LIST_OF_TEAMS')
        scoreCommand = u''
        fragCommand = u''
        deathsCommand = u''
        scoreEnemy = u''
        fragEnemy = u''
        deathsEnemy = u''
        playerTeam = []
        enemy = []
        for e in self.PVPStatistic['users']:
            if e['id'] == self.id:
                command = e['command']
                break

        fragCommand = str(sum([ e['counter'] for e in self.PVPStatistic['users'] if e['command'] == command ]))
        deathsCommand = str(sum([ e['deaths'] for e in self.PVPStatistic['users'] if e['command'] == command ]))
        guiMode = soGUI.soPvPStats.MODE_MT if len(set([ e['command'] for e in self.PVPStatistic['users'] ])) > 2 else soGUI.soPvPStats.MODE_2T
        if guiMode == soGUI.soPvPStats.MODE_2T:
            commandEnemy = [ e['command'] for e in self.PVPStatistic['users'] if e['command'] != command ][0]
            enemyName = lc('Quester.TEAM') + str(commandEnemy)
            fragEnemy = str(sum([ e['counter'] for e in self.PVPStatistic['users'] if e['command'] == commandEnemy ]))
            deathsEnemy = str(sum([ e['deaths'] for e in self.PVPStatistic['users'] if e['command'] == commandEnemy ]))
            for e in self.PVPStatistic['users']:
                if e['command'] == command:
                    playerTeam.append((e['name'],
                     u'',
                     str(e['counter']),
                     str(e['deaths']),
                     -1,
                     []))
                else:
                    enemy.append((e['name'],
                     u'',
                     str(e['counter']),
                     str(e['deaths']),
                     -1,
                     []))

            commandGScore = u''
            enemyGScore = u''
            if self.PVPStatistic['commands']:
                for e in self.PVPStatistic['commands']:
                    if e['command'] == command:
                        enemyGScore = str(e['count'])
                    elif e['command'] == commandEnemy:
                        commandGScore = str(e['count'])

                battleName = commandGScore + u'\t\t:\t\t' + enemyGScore
        data = {'battleName': battleName,
         'playerTeamName': lc('Quester.TEAM') + str(command),
         'enemyName': enemyName,
         'guiMode': guiMode,
         'hideThird': False,
         'playerTeamScore': (scoreCommand, fragCommand, deathsCommand),
         'enemyScore': (scoreEnemy, fragEnemy, deathsEnemy),
         'playerTeam': playerTeam,
         'enemy': enemy}
        BWPersonality.GUICore.setPvPStatsData(data)
        BWPersonality.GUICore.showPvPStats(True)

    def hidePVPStatistic(self):
        BWPersonality.GUICore.showPvPStats(False)

    def setPVPStatus(self, status):
        self.PVPInfo['State'] = status

    def deleteTriggerMarkers(self, qID):
        for e in BigWorld.entities.values():
            if hasattr(e, 'quest') and e.quest == qID:
                e.removeQuestMarker()

    def addTriggerMarkers(self, qID):
        for e in BigWorld.entities.values():
            if hasattr(e, 'quest') and e.quest == qID:
                e.appendQuestMarker()

    def removeAllTriggerMarkers(self):
        for e in BigWorld.entities.values():
            if hasattr(e, 'quest'):
                e.removeQuestMarker()

    def onQStateChange(self, qID):
        from QuestObject import QuestObject
        quest = self.getQuest(qID)
        if quest:
            for e in BigWorld.entities.values():
                if isinstance(e, QuestObject) and e.questID == qID:
                    e.onChangeQuest(quest['State'])

    def onQRemove(self, qID):
        from QuestObject import QuestObject
        for e in BigWorld.entities.values():
            if isinstance(e, QuestObject) and e.questID == qID:
                e.onRemoveQuest()

    def showTutorial(self, text):
        position = [10, 100]
        close_link = u'<n><hlink={0};passTutorial;normal>'.format(lc('Quests.Messages.BAYPASS_TUTORIAL'))
        text += close_link
        text = text.replace(u'<alignment=right>', u'<alignment=left>')
        data = [position, text]
        BWPersonality.GUICore.setTutorialData(data)
        BWPersonality.GUICore.showTutorial()
        self.tutorial_owner = self.id

    def tutorialListener(self, event, data):
        if event == 2 and data[0].replace(' ', '') == u'passTutorial':
            self.base.removeQuestFromJournal(self.tutorialIDs[-1])

    def hideTutorial(self):
        BWPersonality.GUICore.showTutorial(False)
        try:
            BWPersonality.GUICore.removeListener('hlinkEvent', self.tutorialListener)
        except:
            pass

        try:
            BWPersonality.GUICore.removeListener('generalGUIEvent', self.tutorialGUIListener)
        except:
            pass

        self.tutorial_owner = 0

    def onEnterWorld(self):
        if self.tutorial_owner != self.id:
            BWPersonality.GUICore.showTutorial(False)
            self.tutorialIDs = []
            self.tutorial_owner = 0

    def onLeaveWorld(self):
        self.ClientQuests = dict()
        self.sendJournalInfo()
        BWPersonality.GUICore.setQuestDescription(u' ')
        try:
            BWPersonality.GUICore.removeListener('hlinkEvent', self.tutorialListener)
        except:
            print 'Has no hlinkEvent'

        try:
            BWPersonality.GUICore.removeListener('generalGUIEvent', self.tutorialGUIListener)
        except:
            print 'Has no generalGUIEvent'

    def set_passTutorial(self, value):
        pass