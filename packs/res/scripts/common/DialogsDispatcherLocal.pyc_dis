# Embedded file name: scripts/common/DialogsDispatcherLocal.py
from Localization import lc
import Localization
import BigWorld
import ResMgr
from NPCs import NPCs
from copy import copy
DIALOG_FILE = 'Dialogs.xml'
RES_PATH_RUS = 'scripts/common/data/Quests/RUS/'
RES_PATH_ENG = 'scripts/common/data/Quests/ENG/'
Dialogs = {}

def parseDialogInf():
    print 'DialogsDispatcher::parseDialogInf dialogs is {0}'.format(Dialogs)

    def parseReputation(input):
        ret = []
        if input:
            ret = [ dict(fractionID=int(fr[0]), min=float(fr[2].replace(',', '.')) if fr[2] else 0, max=float(fr[3].replace(',', '.')) if fr[3] else 0, type=int(fr[1])) for fr in [ e.split(':') for e in input.split(';') ] ]
        return ret

    if Localization.Localization.globalLanguage == 'russian':
        filePath = RES_PATH_RUS + DIALOG_FILE
    else:
        filePath = RES_PATH_ENG + DIALOG_FILE
    resXML = ResMgr.openSection(filePath)
    for item in resXML.values():
        Holders = item['Holder'].asString.split(',')
        for holder in Holders:
            dialog = dict(DialogID=item['DialogID'].asInt, Version=item['Version'].asInt, Holder=item['Holder'].asString.split(',')[0], Title=item['Title'].asWideString, Text=item['Text'].asWideString, Nodes=[ int(strnode) for strnode in item['Nodes'].asString.split(',') if strnode != '' ], Precondition=dict(ListOfNecessaryQuests=dict(listOfCompletedQuests=[ int(str) for str in item['Precondition']['ListOfNecessaryQuests']['listOfCompletedQuests'].asString.split(',') if str != '' ], listOfOpenedQuests=[ int(str) for str in item['Precondition']['ListOfNecessaryQuests']['listOfOpenedQuests'].asString.split(',') if str != '' ], listOfOnTestQuests=[ int(str) for str in item['Precondition']['ListOfNecessaryQuests']['listOfOnTestQuests'].asString.split(',') if str != '' ], listOfFailedtQuests=[ int(str) for str in item['Precondition']['ListOfNecessaryQuests']['listOfFailedQuests'].asString.split(',') if str != '' ]), ListOfMustNoQuests=dict(listOfCompletedQuests=[ int(str) for str in item['Precondition']['ListOfMustNoQuests']['listOfCompletedQuests'].asString.split(',') if str != '' ], listOfOpenedQuests=[ int(str) for str in item['Precondition']['ListOfMustNoQuests']['listOfOpenedQuests'].asString.split(',') if str != '' ], listOfOnTestQuests=[ int(str) for str in item['Precondition']['ListOfMustNoQuests']['listOfOnTestQuests'].asString.split(',') if str != '' ], listOfFailedtQuests=[ int(str) for str in item['Precondition']['ListOfMustNoQuests']['listOfFailedQuests'].asString.split(',') if str != '' ]), tests=[ int(str) for str in item['Precondition']['tests'].asString.split(',') if str != '' ], Reputation=parseReputation(item['Precondition']['Reputation'].asString), KarmaPK=[ int(str) for str in item['Precondition']['KarmaPK'].asString.split(',') if str != '' ]), Actions=dict(Exit=item['Actions']['Exit'].asInt, ToDialog=item['Actions']['ToDialog'].asInt, Event=item['Actions']['Event'].asInt, GetQuest=[ int(str) for str in item['Actions']['GetQuest'].asString.split(',') if str != '' ], CompleteQuest=[ int(str) for str in item['Actions']['CompleteQuest'].asString.split(',') if str != '' ], Data=item['Actions']['Data'].asString), RootDialog=item['NodeCoordinates']['RootDialog'].asString)
            if not dialog['Nodes'] and not dialog['Actions']['ToDialog']:
                dialog['Exit'] = 1
            if not Dialogs.has_key(dialog['Holder']):
                Dialogs[dialog['Holder']] = dict()
            Dialogs[dialog['Holder']][dialog['DialogID']] = dialog


def getDialogs(npc_name, dialog_ids):
    dialogs = []
    if not Dialogs:
        parseDialogInf()
    dialogs_npc = Dialogs.get(npc_name, {})
    for dialog_id in dialog_ids:
        dialog = dialogs_npc.get(dialog_id)
        if dialog:
            dialogs.append(dialog)

    return dialogs


def getCachedDialogs(npc_name, dialog_ids):
    cached_dialogs = []
    dialogs = copy(getDialogs(npc_name, dialog_ids))
    for dialog in dialogs:
        cached_dialog = copy(dialog)
        del cached_dialog['Title']
        del cached_dialog['Text']
        cached_dialogs.append(cached_dialog)

    return cached_dialogs


def getDialog(npc_name, dialog_id):
    dialogs = getDialogs(npc_name, [dialog_id])
    if dialogs:
        return dialogs[0]


def getNPCDialogs(npc_name):
    if not Dialogs:
        parseDialogInf()
    dialogs_npc = Dialogs.get(npc_name, {})
    if dialogs_npc:
        return dialogs_npc.values()
    return []


def hasDialogsForMe(me_name):
    if not Dialogs:
        parseDialogInf()
    return bool(Dialogs.get(me_name))