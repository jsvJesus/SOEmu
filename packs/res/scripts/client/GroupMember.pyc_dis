# Embedded file name: scripts/client/GroupMember.py
__author__ = 'Madcat'
import BigWorld
import soGUI
import Group
import gui_jokes
from Localization import lc
import BWPersonality
from gui_const import MESSAGEBOX

class GroupMember:

    def __init__(self):
        pass

    member_ids = []
    SHOW_ALL_EFFECTS_FRAME, HIDE_ALL_EFFECTS_FRAME, REMOVE_GROUP, LEAVE_GROUP = xrange(4)
    KICK_MEMBER, GET_LEADER = xrange(2)

    def updateGroupScreen(self):
        for member in self.ClientGroupInfo['members']:
            if member['id'] != self.id:
                data = {'level': u'',
                 'isPL': not bool(member['role']),
                 'CP': member['survive'],
                 'HP': member['health'],
                 'SP': member['stamina'],
                 'name': member['name'],
                 'class': u'',
                 'icon': soGUI.soHealthBar.FACTION_MARK_FOREIGNERS,
                 'out_of_range': bool(member['flag'] & Group.MEMBER_TOO_FAR)}
                self.setPartyMember(member['id'], data)
            else:
                data = {'isPL': not bool(member['role'])}
                self.setHealthBarData(data)

    def delMember(self, id):
        if id == 0:
            id = None
        self.delPartyMember(id)
        return

    def memberEffectUpdate(self, id, effect_list):
        if effect_list:
            for effect_id in effect_list:
                self.setPartyMemberEffect(id, effect_id)

        else:
            self.setPartyMemberEffect(id, None)
        return

    def getFrameActions(self):
        actions = dict()
        if self.ClientGroupInfo['members']:
            actions = {self.HIDE_ALL_EFFECTS_FRAME: lc('Groups.Interface.COMMAND_HIDE_EFFECT'),
             self.SHOW_ALL_EFFECTS_FRAME: lc('Groups.Interface.COMMAND_SHOW_EFFECT')}
            role = 1
            for member in self.ClientGroupInfo['members']:
                if member['id'] == self.id:
                    role = member['role']
                    break

            if role == 0:
                actions[self.REMOVE_GROUP] = lc('Groups.Interface.COMMAND_REMOVE_GROUP')
            else:
                actions[self.LEAVE_GROUP] = lc('Groups.Interface.COMMAND_LEAVE_GROUP')
            return actions

    def getMemberActions(self):
        actions = dict()
        for member in self.ClientGroupInfo['members']:
            if member['id'] == self.id and member['role'] == 0:
                actions = {self.KICK_MEMBER: lc('Groups.Interface.COMMAND_KICK_GROUP'),
                 self.GET_LEADER: lc('Groups.Interface.COMMAND_GET_LEADER')}

        return actions

    def recommendInvite(self, name, recommender_id):

        def listener(event, data):
            if event == MESSAGEBOX.EVENT_BTNPRESS:
                if data['btn'] == MESSAGEBOX.BTN_YES:
                    cmd = u'/invite ' + name
                    self.sendMessage(cmd)

        member = self.getClientMember(recommender_id)
        if member:
            BWPersonality.GUICore.showMsgBox(id='party_invite', isModal=False, x=0.0, y=0.0, width=300, caption=lc('Groups.Interface.RECOMMEND_HEADER').format(inviter), forcePos=False, parent_gui_id=None, bind_to_parent=False, btn_set=[{'type': MESSAGEBOX.BTN_YES,
              'width': 80}, {'type': MESSAGEBOX.BTN_NO,
              'width': 80}], timeout=10, closeBox=True, defaultAction=MESSAGEBOX.BTN_NO, addControls=[{'type': MESSAGEBOX.ADDCONTROL_TEXTFIELD,
              'ID': 'main_txt_field',
              'text': lc('Groups.Interface.RECOMMEND_QUESTION').format(member['name'], name),
              'hAnchor': MESSAGEBOX.ANCHOR_CENTER}], callback=listener)
        return

    def onGroupSettingsChanged(self):
        self.onPartySettingsChanged()

    def getClientMember(self, id):
        for member in self.ClientGroupInfo['members']:
            if member['id'] == id:
                return member

    def addTestMembers(self):
        test_member = dict(id=1, name=u'Rustam', health=100.0, role=1, stamina=0.0, survive=0.0, flag=0)
        test_member1 = dict(id=2, name=u'Lev    ', health=1.0, role=1, stamina=0.0, survive=0.0, flag=0)
        test_member_self = dict(id=self.id, name=self.name, health=1.0, role=0, stamina=0.0, survive=0.0, flag=0)
        self.ClientGroupInfo['members'].append(test_member)
        self.setPartyMemberEffect(test_member['id'], 5)
        self.setPartyMemberEffect(test_member['id'], 20)
        self.setPartyMemberEffect(test_member['id'], 7)
        self.ClientGroupInfo['members'].append(test_member1)
        self.setPartyMemberEffect(test_member1['id'], 20)
        self.setPartyMemberEffect(test_member1['id'], 8)
        self.ClientGroupInfo['members'].append(test_member_self)
        self.updateGroupScreen()

    def showParticipant(self):
        output = u''
        for member in self.ClientGroupInfo['members']:
            if not output:
                output += lc('Groups.Messages.YOUR_GROUP') + u'\n'
                output += member['name']
            else:
                output += member['name']
            if member['role'] == 0:
                output += lc('Groups.Messages.OWNER')
            if self.name == member['name']:
                output += lc('Groups.Messages.YOU')
            output += u'\n'

        if not output:
            output = lc('Groups.Messages.NOT_IN_GROUP')
        self.questerMessageToConsole(output)

    def tellAboutPartyStatus(self, data, stringData, status):
        message = u''
        if status == Group.STATUS_CANT_DESTROY_NOW:
            message = lc('Groups.Messages.CANT_DESTROY_NOW')
        elif status == Group.STATUS_GROUP_DESTROYED:
            message = lc('Groups.Messages.GROUP_DESTROYED')
        elif status == Group.STATUS_NOT_IN_GROUP:
            message = lc('Groups.Messages.NOT_IN_GROUP')
        elif status == Group.STATUS_CANT_LEAVE:
            message = lc('Groups.Messages.CANT_LEAVE')
        elif message == Group.STATUS_NOT_IN_YOUR_GROUP:
            message = lc('Groups.Messages.NOT_IN_YOUR_GROUP').format(stringData[0])
        elif message == Group.STATUS_IN_GROUP:
            message = lc('Groups.Messages.IN_GROUP')
        elif message == Group.STATUS_PLAYER_ALREADY_IN_GROUP:
            message = lc('Groups.Messages.PLAYER_ALREADY_IN_GROUP')
        elif message == Group.STATUS_HAS_JOINED:
            message = lc('Groups.Messages.HAS_JOINED').format(stringData[0])
        elif message == Group.STATUS_MAX_PLAYER_NUM:
            message = lc('Groups.Messages.MAX_PLAYER_NUM')
        elif message == Group.STATUS_LEADER_HAS_CHANGED:
            message = lc('Groups.Messages.LEADER_HAS_CHANGED').format(stringData[0])
        elif status == Group.STATUS_CANT_CHANGE:
            message = lc('Groups.Messages.CANT_CHANGE')
        elif status == Group.STATUS_CANT_FIND_PLAYER:
            message = lc('Groups.Messages.CANT_FIND_PLAYER')
        elif status == Group.STATUS_PLAYER_NOT_IN_GAME:
            message = lc('Groups.Messages.PLAYER_NOT_IN_GAME')
        elif status == Group.STATUS_YOU_CANT_INVITE_YOURSELF:
            message = lc('Groups.Messages.YOU_CANT_INVITE_YOURSELF')
        elif status == Group.STATUS_PLAYER_ALREADY_INVITED:
            message = lc('Groups.Messages.PLAYER_ALREADY_INVITED').format(stringData[0])
        if message:
            self.partyMessage(message)

    def showGroupInvite(self, ownerName):

        def listener(event, data):
            if event == MESSAGEBOX.EVENT_BTNPRESS:
                if data['btn'] == MESSAGEBOX.BTN_YES:
                    self.joinInGroup()
                else:
                    self.base.clearCurrentInviteInformation(1)

        BWPersonality.GUICore.showMsgBox(id='party_invite', isModal=False, x=0.0, y=0.0, width=300, caption=lc('Groups.Interface.INVITE_HEADER').format(ownerName), forcePos=False, parent_gui_id=None, bind_to_parent=False, btn_set=[{'type': MESSAGEBOX.BTN_YES,
          'width': 80}, {'type': MESSAGEBOX.BTN_NO,
          'width': 80}], timeout=10, closeBox=True, defaultAction=MESSAGEBOX.BTN_NO, addControls=[{'type': MESSAGEBOX.ADDCONTROL_TEXTFIELD,
          'ID': 'main_txt_field',
          'text': lc('Groups.Interface.INVITE_QUESTION').format(ownerName),
          'hAnchor': MESSAGEBOX.ANCHOR_CENTER}], callback=listener)
        return

    def partyMessage(self, string):
        self.questChatline(string)

    def destroyGroup(self):

        def listener(event):
            if event == gui_jokes.askUserYesNoDelayDeafultNo.YES:
                self.base.destroyGroup()

        gui_jokes.askUserYesNoDelayDeafultNo(u'', lc('Groups.Interface.DESSTROY_QUESTION'), listener, 10.0)

    def inviteInGroup(self, cmd):
        if len(cmd) >= 2:
            names = []
            names = [ unicode(name) for name in cmd[1:] if name ]
            self.base.onTryCreateGroup(names)
            self.systemChatline(lc('Groups.Messages.INVITATION_HAS_SENT'))

    def changeOwner(self, cmd):
        if len(cmd) >= 2:
            names = []
            names = [ unicode(name) for name in cmd[1:] ]
            self.base.tryChangeOwner(names[0])
            self.systemChatline(lc('Groups.Messages.CHANGE_LEADER_REQUEST_HAS_SENT'))

    def inviteRequest(self, cmd):
        if len(cmd) >= 2:
            names = []
            names = [ unicode(name) for name in cmd[1:] ]
            self.cell.onRecommendInvite(names)
            self.systemChatline(lc('Groups.Messages.INVITE_REQUEST_HAS_SENT'))