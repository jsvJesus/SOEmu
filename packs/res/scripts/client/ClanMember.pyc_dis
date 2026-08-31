# Embedded file name: scripts/client/ClanMember.py
"""
Created on 29.09.2011

@author: Madcat
"""
import BigWorld
import gui_jokes
from PlayerAvatarForSoClanScreen import PlayerAvatarForSoClanScreen
from time import time
import gui_jokes
import BWPersonality
from gui_const import OBJECTIVE_TRACKER
import Clan
from Localization import lc
from gui_const import MESSAGEBOX

class ClanMember(PlayerAvatarForSoClanScreen):
    debug_dict = dict()
    BASE_CAPTURE_ID = '_base'
    FLAG_CAPTURE_ID = '_flag'
    flag_name_by_id = {1: lc('Clans.Messages.PRVT'),
     2: lc('Clans.Messages.CPR'),
     0: lc('Clans.Messages.SRGT')}
    base_tracker = dict()
    reinfp_tracker = dict()

    def __init__(self):
        for objective_id in BWPersonality.GUICore.getCurrentObjectives():
            BWPersonality.GUICore.delObjective(self.BASE_CAPTURE_ID)

    def clanRosterUpdate(self, roster):
        PlayerAvatarForSoClanScreen.clanRosterUpdate(self, roster)

    def clanMemberRosterUpdate(self, member):
        PlayerAvatarForSoClanScreen.clanMemberRosterUpdate(self, member)

    def clanRanksUpdate(self, ranks, self_id):
        PlayerAvatarForSoClanScreen.clanRanksUpdate(self, ranks, self_id)

    def clanBasesUpdate(self, basesData):
        PlayerAvatarForSoClanScreen.clanBasesUpdate(self, basesData)

    def baseAreaStatusUpdate(self, data, serverTime):
        bases = []
        for e in data:
            base = {'name': e['name'],
             'nextPVPTimeStart': time(),
             'nextPVPTimeEnd': time() + 3600,
             'staff': []}
            for ex in e['npcPoints']:
                expires = 0
                for es in e['npcStates']:
                    if es['name'] == ex['name']:
                        expires = es['expiresAt'] - serverTime
                        break

                base['staff'].append({'staffName': ex['name'],
                 'id': ex['id'],
                 'staffLimitTotal': 1,
                 'staffCurrentTotal': 0,
                 'staffList': self.getStaffListForNPCType(ex['type'], ex['maxLevel'], expires),
                 'staffExpire': expires})

            bases.append(base)

        self.clanBasesUpdate(bases)

    def showClanCreateDialog(self, isRepeat):
        if isRepeat:
            text = lc('Clans.Interface.INCORRECT_CLAN_NAME')
        else:
            text = lc('Clans.Interface.ENTER_CLAN_NAME')
        gui_jokes.inputBox(text, u' ', self.onTryCreateClan)

    def onTryCreateClan(self, text):
        self.base.createClan(text.encode('utf-8'))

    def GetHolderClanID(self):
        return self.GetClanID()

    def GetClanID(self):
        return self.cellClanID

    def showBaseTraker(self):
        if self.show_tracker & Clan.TRACKER_BASE:
            data = {'caption': lc('Clans.Interface.BASE') + u':{0}'.format(self.base_tracker['clan_name'] or lc('Clans.Interface.STATE_FREE')),
             'track_data': []}
            if self.base_tracker['time']:
                self.base_tracker['time'] -= 1
                status = lc('Clans.Interface.BEFORE_CAPTURE_START') + u':'
                if self.base_tracker['status'] in [Clan.BASE_STATE_IN_CAPTIVITY, Clan.BASE_STATE_WAIT_FOR_FLAGS_UPDATE]:
                    status = lc('Clans.Interface.BEFORE_CAPTURE_STOP')
                elif self.base_tracker['status'] in [Clan.BASE_STATE_WAIT_FOR_ENEMIES_LEAVE]:
                    status = lc('Clans.Interface.BEFORE_DEFEND_START')
                minute, seconds = divmod(self.base_tracker['time'], 60)
                hour, minute = divmod(minute, 60)
                status += u'{0}:{1}:{2}'.format(int(hour), int(minute), int(seconds))
                data['track_data'].append({'data_type': OBJECTIVE_TRACKER.DATATYPE_PLAINTEXT,
                 'data': status})
            if self.base_tracker.has_key('flags') and self.base_tracker['status'] in [Clan.BASE_STATE_IN_CAPTIVITY, Clan.BASE_STATE_WAIT_FOR_FLAGS_UPDATE]:
                statistic_dict = dict()
                for f in self.flag_name_by_id:
                    statistic_dict[f] = [lc('Clans.Interface.POINT') + self.flag_name_by_id[f], 0, 0]

                for flag in self.base_tracker['flags']:
                    if flag['state'] == Clan.FLAG_STATE_CAPTURED:
                        statistic_dict[flag['level']][1] += 1
                    statistic_dict[flag['level']][2] += 1

                for stat_key in [0, 2, 1]:
                    stat = statistic_dict[stat_key]
                    text = stat[0] + u':' + str(stat[1]) + u'/' + str(stat[2])
                    data['track_data'].append({'data_type': OBJECTIVE_TRACKER.DATATYPE_PLAINTEXT,
                     'data': text})

                for flag in self.base_tracker['flags']:
                    stat = u''
                    progr = flag['progress']
                    if flag['state'] in [Clan.FLAG_STATE_IN_CAPTIVITY]:
                        stat = lc('Clans.Interface.IS_BEING_CAPTURED') + str(int(flag['progress'])) + u'%   ' + flag['winning_clanName']
                    elif flag['state'] in [Clan.FLAG_STATE_CAPTURED]:
                        stat = lc('Clans.Interface.IS_CAPTURED') + flag['winning_clanName']
                    if stat:
                        cur_flag_info = lc('Clans.Interface.POINT') + self.flag_name_by_id.get(flag['level'], u'') + stat
                        data['track_data'].append({'data_type': OBJECTIVE_TRACKER.DATATYPE_PLAINTEXT,
                         'data': cur_flag_info})

            if self.BASE_CAPTURE_ID in BWPersonality.GUICore.getCurrentObjectives():
                BWPersonality.GUICore.setObjective(self.BASE_CAPTURE_ID, data)
            else:
                BWPersonality.GUICore.addObjective(self.BASE_CAPTURE_ID, OBJECTIVE_TRACKER.PRIORITY_HIGHEST, data)
            BigWorld.callback(1.0, self.showBaseTraker)

    def onLeaveBase(self):
        BWPersonality.GUICore.delObjective(self.BASE_CAPTURE_ID)

    def showReinfTracker(self):
        if self.show_tracker & Clan.TRACKER_REINFP:
            clan_name = self.reinfp_tracker['clan_name']
            progress = u''
            if self.reinfp_tracker['status'] == Clan.RFP_STATE_IN_CAPTIVITY:
                progress = str(self.reinfp_tracker['progress'])
                if progress > 0:
                    progress = ''.join([progress, u'%'])
            if not clan_name:
                clan_name = lc('Clans.Interface.STATE_FREE')
            data = {'caption': lc('Clans.Interface.REINFORCEMENT_POINT') + u'{0}:{1}'.format(progress, clan_name),
             'track_data': []}
            status = lc('Clans.Interface.BEFORE_CAPTURE_START') + u':'
            if self.reinfp_tracker['status'] in [Clan.RFP_STATE_IN_CAPTIVITY]:
                status = lc('Clans.Interface.BEFORE_CAPTURE_STOP') + u':'
            minute, seconds = divmod(self.reinfp_tracker['time'], 60)
            hour, minute = divmod(minute, 60)
            status += u'{0}:{1}:{2}'.format(int(hour), int(minute), int(seconds))
            data['track_data'].append({'data_type': OBJECTIVE_TRACKER.DATATYPE_PLAINTEXT,
             'data': status})
            if self.FLAG_CAPTURE_ID in BWPersonality.GUICore.getCurrentObjectives():
                BWPersonality.GUICore.setObjective(self.FLAG_CAPTURE_ID, data)
            else:
                BWPersonality.GUICore.addObjective(self.FLAG_CAPTURE_ID, OBJECTIVE_TRACKER.PRIORITY_HIGHEST, data)

    def onLeaveRFPoint(self):
        BWPersonality.GUICore.delObjective(self.FLAG_CAPTURE_ID)

    def showClanWars(self):
        if len(self.clanEnemies) == 0:
            warList = lc('Clans.Messages.YOUR_CLAN_HAS_NO_WARS')
        else:
            warList = lc('Clans.Messages.YOUR_CLAN_IS_IN_WAR_WITH')
            warList += ', '.join(self.clanEnemies).decode('utf-8')
        self.guildChatline(warList)
        if len(self.clanHostiles) == 0:
            warList = lc('Clans.Messages.THERE_IS_NO_CLANS_WHICH_ARE_IN_WAR_WITH_YOU')
        else:
            warList = lc('Clans.Messages.THERE_IS_CLANS_WHICH_ARE_IN_WAR_WITH_YOU')
            warList += ', '.join(self.clanHostiles).decode('utf-8')
        self.guildChatline(warList)

    def tellAboutClanStatus(self, data, stringData, status):
        message = u''
        if status == Clan.STATUS_CLAN_NAME_IS_OCCUPIED:
            message = lc('Clans.Messages.CLAN_NAME_IS_OCCUPIED')
        elif status == Clan.STATUS_CLAN_NAME_IS_TOO_SHORT:
            message = lc('Clans.Messages.CLAN_NAME_IS_TOO_SHORT')
        elif status == Clan.STATUS_CLAN_NAME_IS_TOO_LONG:
            message = lc('Clans.Messages.CLAN_NAME_IS_TOO_LONG')
        elif status == Clan.STATUS_CLAN_NAME_HAVE_TOO_MUCH_UNDERLINE:
            message = lc('Clans.Messages.CLAN_NAME_HAVE_TOO_MUCH_UNDERLINE')
        elif status == Clan.STATUS_CLAN_NAME_CANT_ENDS_WITH_UNDERLINE:
            message = lc('Clans.Messages.CLAN_NAME_CANT_ENDS_WITH_UNDERLINE')
        elif status == Clan.STATUS_CLAN_NAME_CANT_BEGIN_WITH_UNDERLINE:
            message = lc('Clans.Messages.CLAN_NAME_CANT_BEGIN_WITH_UNDERLINE')
        elif status == Clan.STATUS_CLAN_NAME_HAVE_FORBIDDEN_CHAR:
            message = lc('Clans.Messages.CLAN_NAME_HAVE_FORBIDDEN_CHAR')
        elif status == Clan.STATUS_CLAN_HAVE_BEEN_DELETED:
            message = lc('Clans.Messages.CLAN_HAVE_BEEN_DELETED')
        elif status == Clan.STATUS_CLAN_HAVE_BEEN_CREATED:
            message = lc('Clans.Messages.CLAN_HAVE_BEEN_CREATED')
        elif status == Clan.STATUS_YOR_CLAN_IS_NOT_EXIST:
            message = lc('Clans.Messages.YOR_CLAN_IS_NOT_EXIST')
        elif status == Clan.STATUS_PLAYER_HAVE_LEAVE_CLAN:
            message = lc('Clans.Messages.PLAYER_HAVE_LEAVE_CLAN').format(stringData[0])
        elif status == Clan.STATUS_YOU_HAVE_LEAVE_THE_CLAN:
            message = lc('Clans.Messages.YOU_HAVE_LEAVE_THE_CLAN')
        elif status == Clan.STATUS_YOU_CANT_LEAVE_CLAN_BECAUSE_YOU_ARE_LEADER:
            message = lc('Clans.Messages.YOU_CANT_LEAVE_CLAN_BECAUSE_YOU_ARE_LEADER')
        elif status == Clan.STATUS_YOU_ARE_NOT_MEMBER_OF_THE_GROUP:
            message = lc('Clans.Messages.YOU_ARE_NOT_MEMBER_OF_THE_GROUP')
        elif status == Clan.STATUS_YOU_CANT_KICK_YOURSELF:
            message = lc('Clans.Messages.YOU_CANT_KICK_YOURSELF')
        elif status == Clan.STATUS_YOU_HAVE_NOT_RIGHT_TO_KICK:
            message = lc('Clans.Messages.YOU_HAVE_NOT_RIGHT_TO_KICK')
        elif status == Clan.STATUS_YOU_CANT_KICK_THE_LEADER:
            message = lc('Clans.Messages.YOU_CANT_KICK_THE_LEADER')
        elif status == Clan.STATUS_PLAYER_HAS_BEEN_KICKED_KICK_WITH_REASON:
            message = lc('Clans.Messages.PLAYER_HAS_BEEN_KICKED_KICK_WITH_REASON').format(stringData[0], stringData[1], stringData[2])
        elif status == Clan.STATUS_PLAYER_HAS_BEEN_KICKED:
            message = lc('Clans.Messages.PLAYER_HAS_BEEN_KICKED').format(stringData[0], stringData[1])
        elif status == Clan.STATUS_PLAYER_HAS_BENN_PROMOTED_TO_THE_RANK:
            message = lc('Clans.Messages.PLAYER_HAS_BENN_PROMOTED_TO_THE_RANK').format(stringData[0], stringData[1], stringData[2])
        elif status == Clan.STATUS_PLAYER_HAS_BENN_DEMOTED_TO_THE_RANK:
            message = lc('Clans.Messages.PLAYER_HAS_BENN_DEMOTED_TO_THE_RANK').format(stringData[0], stringData[1], stringData[2])
        elif status == Clan.STATUS_CLAN_LEADER_HAS_CHANGED:
            message = lc('Clans.Messages.CLAN_LEADER_HAS_CHANGED').format(stringData[0])
        elif status == Clan.STATUS_YOU_HAVE_NOT_RIGHT_TO_INVITE:
            message = lc('Clans.Messages.YOU_HAVE_NOT_RIGHT_TO_INVITE')
        elif status == Clan.STATUS_YOU_ARE_NOT_IN_CLAN:
            message = lc('Clans.Messages.YOU_ARE_NOT_IN_CLAN')
        elif status == Clan.STATUS_YOU_HAVE_NOT_RIGHT_TO_START_WAR:
            message = lc('Clans.Messages.YOU_HAVE_NOT_RIGHT_TO_START_WAR')
        elif status == Clan.STATUS_YOU_HAVE_NOT_RIGHT_TO_STOP_WAR:
            message = lc('Clans.Messages.YOU_HAVE_NOT_RIGHT_TO_STOP_WAR')
        elif status == Clan.STATUS_YOU_CANT_START_WAR_WITH_YOUR_OWN_CLAN:
            message = lc('Clans.Messages.YOU_CANT_START_WAR_WITH_YOUR_OWN_CLAN')
        elif status == Clan.STATUS_CANT_FIND_CLAN_TO_WAR:
            message = lc('Clans.Messages.CANT_FIND_CLAN_TO_WAR')
        elif status == Clan.STATUS_CANT_FIND_CLAN_TO_STOP_WAR:
            message = lc('Clans.Messages.CANT_FIND_CLAN_TO_STOP_WAR')
        elif status == Clan.STATUS_YOU_HAVE_REFUSED_TO_JOIN_IN_CLAN:
            message = lc('Clans.Messages.YOU_HAVE_REFUSED_TO_JOIN_IN_CLAN')
        elif status == Clan.STATUS_YOU_HAVE_JOINED_IN_CLAN:
            message = lc('Clans.Messages.YOU_HAVE_JOINED_IN_CLAN')
        elif status == Clan.STATUS_YOUR_INVITATION_IS_OUT_OF_DATE:
            message = lc('Clans.Messages.YOUR_INVITATION_IS_OUT_OF_DATE')
        elif status == Clan.STATUS_THERE_IS_NO_CLAN_MEMBER_WITH_NAME:
            message = lc('Clans.Messages.THERE_IS_NO_CLAN_MEMBER_WITH_NAME').format(stringData[0])
        elif status == Clan.STATUS_THERE_IS_NO_CLAN_WITH_NAME:
            message = lc('Clans.Messages.THERE_IS_NO_CLAN_WITH_NAME').format(stringData[0])
        elif status == Clan.STATUS_YOU_MUST_LEAVE_FROM_THE_CLAN_BEFORE_CREATE_NEW:
            message = lc('Clans.Messages.YOU_MUST_LEAVE_FROM_THE_CLAN_BEFORE_CREATE_NEW')
        elif status == Clan.STATUS_YOU_CANT_CREATE_CLAN_WITH_THIS_NAME:
            message = lc('Clans.Messages.YOU_CANT_CREATE_CLAN_WITH_THIS_NAME')
        elif status == Clan.STATUS_YOU_CANT_JOIN_TO_THIS_CLAN:
            message = lc('Clans.Messages.YOU_CANT_JOIN_TO_THIS_CLAN')
        elif status == Clan.STATUS_YOU_CANT_LEAVE_BEFORE_YOU_ARE_LEADER:
            message = lc('Clans.Messages.YOU_CANT_LEAVE_BEFORE_YOU_ARE_LEADER')
        elif status == Clan.STATUS_YOU_MUST_LEAVE_FROM_THE_CLAN_BEFORE_YOU_WILL_BE_JOINED:
            message = lc('Clans.Messages.YOU_MUST_LEAVE_FROM_THE_CLAN_BEFORE_YOU_WILL_BE_JOINED').format(stringData[0])
        elif status == Clan.STATUS_PLAYER_CANT_ACCEPT_YOUR_OFFER_BEACUSE_HE_IS_ALREADY_IN_CLAN:
            message = lc('Clans.Messages.PLAYER_CANT_ACCEPT_YOUR_OFFER_BEACUSE_HE_IS_ALREADY_IN_CLAN').format(stringData[0])
        elif status == Clan.STATUS_YOU_INVITATION_HAS_BEEN_SENT:
            message = lc('Clans.Messages.YOU_INVITATION_HAS_BEEN_SENT')
        elif status == Clan.STATUS_YOU_CAN_INVITE_THIS_PLAYER_IN_TIME:
            message = lc('Clans.Messages.YOU_CAN_INVITE_THIS_PLAYER_IN_TIME').format(data[0], data[1], data[2], data[3])
        elif status == Clan.STATUS_YOU_HAVE_BEEN_INVITED:
            message = lc('Clans.Messages.YOU_HAVE_BEEN_INVITED').format(stringData[0])
        if message:
            self.guildChatline(message)

    def checkClanRights(self, right):
        return self.clanRights & right

    def onEnterRFPoint(self):
        self.showReinfTracker()

    def onEnterBase(self):
        self.showBaseTraker()

    def onLeaveWorld(self):
        for objective_id in BWPersonality.GUICore.getCurrentObjectives():
            BWPersonality.GUICore.delObjective(objective_id)

    def onEnterWorld(self):
        if self.show_tracker & Clan.TRACKER_REINFP:
            self.showReinfTracker()
        if self.show_tracker & Clan.TRACKER_BASE:
            self.showBaseTraker()

    def set_clanName(self, old_value):
        self.clanRoster['cName'] = self.clanName.decode('utf-8')

    def set_clanHostiles(self, old_value):
        pass

    def set_clanEnemies(self, old_value):
        pass

    def leaveClan(self):

        def listener(event, data):
            if event == MESSAGEBOX.EVENT_BTNPRESS:
                if data['btn'] == MESSAGEBOX.BTN_YES:
                    self.base.leaveClan()

        BWPersonality.GUICore.showMsgBox(id='clan_leave', isModal=False, x=0.0, y=0.0, width=300, caption=lc('Clans.Interface.LEAVE_TITLE'), forcePos=False, parent_gui_id=None, bind_to_parent=False, btn_set=[{'type': MESSAGEBOX.BTN_YES,
          'width': 80}, {'type': MESSAGEBOX.BTN_NO,
          'width': 80}], timeout=10, closeBox=True, defaultAction=MESSAGEBOX.BTN_NO, addControls=[{'type': MESSAGEBOX.ADDCONTROL_TEXTFIELD,
          'ID': 'main_txt_field',
          'text': lc('Clans.Interface.LEAVE_QUESTION'),
          'hAnchor': MESSAGEBOX.ANCHOR_CENTER}], callback=listener)
        return