# Embedded file name: scripts/client/Mailable.py
from collections import deque
from Settings import Settings
from Localization import lc
from MailableUtils import MailableKinds, MailKinds
import BWPersonality
from colorCodes import *
import BigWorld
from copy import copy
import re
from datetime import datetime
import time
from gui_const import CHAT_CONSOLE, GUI_ID
import chat_utils

class Mailable:

    def __init__(self):
        self.MailMessages = deque(maxlen=100)
        self.MailLastID = 0
        self.chatLines = deque(maxlen=100)
        self.currentLine = 0
        self.loadBadwords()
        self.loadBlacklist()
        self.lastChatAt = 0
        self.context_operation_target = None
        configdata = {CHAT_CONSOLE.TAB_ALL: (CHAT_CONSOLE.MESSAGE_ALL, True),
         CHAT_CONSOLE.TAB_CLAN: (CHAT_CONSOLE.MESSAGE_CLAN, True),
         CHAT_CONSOLE.TAB_FRIENDS: (CHAT_CONSOLE.MESSAGE_FRIENDS, True),
         CHAT_CONSOLE.TAB_PARTY: (CHAT_CONSOLE.MESSAGE_PARTY, True),
         CHAT_CONSOLE.TAB_PRIVATE: (CHAT_CONSOLE.MESSAGE_PRIVATE, True)}
        BWPersonality.GUICore.configChatConsole(configdata)
        return

    def loadBadwords(self):
        self.badwords = BWPersonality.game.badwords

    def loadBlacklist(self):
        self.blacklist = filter(lambda s: isinstance(s, basestring), Settings().getSetting('blacklist', []))

    def saveBlacklist(self):
        Settings().setSetting('blacklist', self.blacklist, flush=True)

    def setChatAbuse(self, v):
        Settings().setSetting('chatabuse', v, flush=True)

    def getChatAbuse(self):
        return Settings().getSetting('chatabuse', False)

    def ignore(self, name):
        name = name.strip()
        if not name in self.blacklist:
            name == self.name or self.blacklist.append(name)
            self.saveBlacklist()

    def unignore(self, name):
        if name in self.blacklist:
            self.blacklist.remove(name)
            self.saveBlacklist()

    def onChatOut(self, event, data):
        if event == CHAT_CONSOLE.EVENT_SEND:
            self.parseChatString(data)
            if not self.chatLines or self.chatLines[-1] != data:
                self.chatLines.append(data)
            self.currentLine = len(self.chatLines)
        elif event == CHAT_CONSOLE.EVENT_REPEAT:
            if not len(self.chatLines):
                return
            shift = -1 if data else 1
            self.currentLine = (self.currentLine + shift) % len(self.chatLines)
            BWPersonality.GUICore.chatPromt(self.chatLines[self.currentLine], replaceTag=True, eraseOld=True)

    def onEnterWorld(self):
        BWPersonality.GUICore.addListener('chatEvent', self.chatConsoleHandler)
        BWPersonality.GUICore.addListener('hlinkEvent', self.hlinkEventHandler)
        BWPersonality.GUICore.addListener('contextMenuEvent', self.chatContextHandler)
        BWPersonality.GUICore.chatClear()
        BWPersonality.GUICore.configChatConsole({'validator': self.inputValidator})

    def onLeaveWorld(self):
        BWPersonality.GUICore.removeListener('chatEvent', self.chatConsoleHandler)
        BWPersonality.GUICore.removeListener('hlinkEvent', self.hlinkEventHandler)
        BWPersonality.GUICore.removeListener('contextMenuEvent', self.chatContextHandler)
        BWPersonality.GUICore.configChatConsole({'validator': lambda newStr, wholeStr, offset: True})

    def parseChatString(self, string):
        if not string:
            return
        else:
            if hasattr(self, 'lastChatAt'):
                timePassed = BigWorld.time() - self.lastChatAt
                if timePassed < 1.0 or timePassed < 3.0 and self.lastChatString == string:
                    return
            self.lastChatAt = BigWorld.time()
            self.lastChatString = string

            def strReplace(string, olds, new):
                for old in olds:
                    string = string.replace(old, new)

                return string

            sepstr = [u',', u'?', u'  ']
            words = strReplace(string, sepstr, u' ').split()
            toNames = []
            last = None
            for word in words:
                if word[0] == u'@':
                    toNames.append(word[word.rfind(u'@') + 1:])
                    last = word[1:]
                else:
                    if last:
                        string = string[string.rfind(last) + len(last):].lstrip()
                    break

            toName = u','.join(toNames)
            if string:
                if string[0] == u'/':
                    self.SendMail(MailKinds.System, string, MailableKinds.Player, 0, toName)
                elif toName:
                    self.SendMail(MailKinds.Private, string, MailableKinds.Player, 0, toName)
                else:
                    self.SendMail(MailKinds.Default, string, MailableKinds.CommonChat)
            return

    def systemChatline(self, txt):
        if not txt:
            return
        self.putMessage(txt, chat_utils.MESSAGE_SYSTEM)

    def lootChatline(self, txt):
        if not txt:
            return
        self.putMessage(txt, chat_utils.MESSAGE_ITEMS)

    def questChatline(self, txt):
        if not txt:
            return
        self.putMessage(txt, chat_utils.MESSAGE_QUEST)

    def woundsChatline(self, txt):
        if not txt:
            return
        self.putMessage(txt, chat_utils.MESSAGE_DAMAGE_TAKEN)

    def damageChatline(self, txt):
        if not txt:
            return
        self.putMessage(txt, chat_utils.MESSAGE_DAMAGE_DEALT)

    def privateChatline(self, txt):
        if not txt:
            return
        self.putMessage(txt, chat_utils.MESSAGE_PRIVATE)

    def guildChatline(self, txt):
        if not txt:
            return
        self.putMessage(txt, chat_utils.MESSAGE_CLAN)

    def groupChatline(self, txt):
        if not txt:
            return
        self.putMessage(txt, chat_utils.MESSAGE_PARTY)

    def commonChatline(self, txt):
        if not txt:
            return
        self.putMessage(txt, chat_utils.MESSAGE_GENERAL)

    def remove_old_color_codes(self, txt):
        return ''.join(re.split('\\\\c[A-Z0-9]{8};?', txt))

    def __chatline__(self, txt, mask = CHAT_CONSOLE.MESSAGE_GENERAL):
        now = datetime.now()
        delta = now - datetime.utcnow()
        utcdelta = delta.days * 24 + delta.seconds // 3600
        timestamp = tf3_chat_timestamp + '%s %s' % ('(%s%s)' % ('+' if utcdelta > 0 else '', utcdelta) if utcdelta != 0 else '', now.strftime('%H:%M:%S'))
        txt = self.remove_old_color_codes(txt)
        BWPersonality.GUICore.chatPrint(mask, txt, timestamp)

    def ReceiveMail(self, mailID, mailKind, txt, fromKind, fromID, fromName):
        if not self.getChatAbuse():
            txt = self.clearBadwords(txt)
        if fromName in self.blacklist:
            return
        if mailKind == MailKinds.Private:
            chatstr = lc('Mailable.client.PRIVATE_TO_YOU') % (fromName, txt)
            self.privateChatline(chatstr)
        elif mailKind == MailKinds.System:
            self.systemChatline(chatstr)
        elif mailKind == MailKinds.Default:
            chatstr = '@%s: %s' % (fromName, txt)
            if fromKind == MailableKinds.Guildchat:
                self.guildChatline(chatstr)
            else:
                self.commonChatline(chatstr)

    def clearBadwords(self, string):
        newstr = copy(string)
        for word in re.compile(lc('Mailable.client.REGEX')).findall(string):
            if word.lower() in self.badwords:
                newstr = newstr.replace(word, ''.center(len(word), '*'))

        return newstr

    def SendMail(self, mailKind, txt, toKind, toID = None, toName = None):
        if not txt:
            return None
        else:
            if mailKind == MailKinds.Private:
                if toID in (None, 0):
                    toID = 0
                    if toName in (None, ''):
                        self.PythonLog('No recipient found')
                        return None
                else:
                    toName = u''
            elif mailKind == MailKinds.Default:
                if toKind == MailableKinds.CommonChat:
                    toID = 0
                    toName = u''
            elif mailKind == MailKinds.System and txt[0] == u'/':
                toID = 0
                toName = u''
            else:
                return None
            self.MailLastID += 1
            self.MailMessages.append(self.MailLastID)
            self.cell.SendMail(self.MailLastID, mailKind, txt, toKind, toID, toName)
            if not self.getChatAbuse():
                txt = self.clearBadwords(txt)
            if mailKind == MailKinds.Private:
                chatstr = lc('Mailable.client.PRIVATE_FROM_YOU') % (toName, txt)
                self.privateChatline(chatstr)
            elif mailKind == MailKinds.Default:
                if not txt.startswith('%'):
                    chatstr = lc('Mailable.client.COMMON_YOU') % txt
                    self.commonChatline(chatstr)
            elif mailKind == MailKinds.System:
                chatstr = txt
                self.systemChatline(chatstr)
            else:
                return None
            return None

    def SendPrivateMsg(self, MsgText, plrID = None, plrName = None):
        self.SendMail(MailKinds.Private, MsgText, MailableKinds.Player, plrID, plrName)

    def SendSystemCallback(self, mailID, txt):
        self.SendMail(mailID, MailKinds.System, txt, MailableKinds.Player, self.id, '')

    def PythonLog(self, txt):
        pass

    CONTEXT_INVITE_PARTY = 0
    CONTEXT_INVITE_CLAN = 1
    CONTEXT_ADD_TO_FRIEND = 2
    CONTEXT_ADD_TO_IGNORE = 3

    def chatConsoleHandler(self, event, data):
        if event == CHAT_CONSOLE.EVENT_SEND:
            if data:
                data = data.replace('&', '&amp;')
                data = data.replace('<', '&lt;')
                data = data.replace('>', '&gt;')
                data = data.replace('"', '&quot;')
                self.sendMessage(data)
                if not self.chatLines or self.chatLines[-1] != data:
                    self.chatLines.append(data)
                self.currentLine = len(self.chatLines)
        elif event == CHAT_CONSOLE.EVENT_REPEAT:
            if not len(self.chatLines):
                return
            shift = -1 if data else 1
            self.currentLine = (self.currentLine + shift) % len(self.chatLines)
            BWPersonality.GUICore.chatPromt(self.chatLines[self.currentLine], replaceTag=True, eraseOld=True)

    def chatConsoleCommand(self, cmd):
        return False

    def _isValidTargetMsg(self, msg):
        msgClass = chat_utils.getMsgClass(msg)
        if msgClass != chat_utils.MESSAGE_CLASS_TARGET:
            return False
        if len(msg) > chat_utils.MAX_MESSAGE_LEN:
            return False
        msgType = chat_utils.getMsgType(msg)
        if msgType in [chat_utils.MESSAGE_PARTY, chat_utils.MESSAGE_CLAN]:
            if msg[1:].strip():
                return True
        if msgType == chat_utils.MESSAGE_PRIVATE:
            nameAndMsg = msg.split(' ', 1)
            if len(nameAndMsg) < 2:
                return False
            if nameAndMsg[1].strip():
                return True
        return False

    def _isValidWorldMsg(self, msg):
        msgClass = chat_utils.getMsgClass(msg)
        if msgClass != chat_utils.MESSAGE_CLASS_WORLD:
            return False
        if len(msg) > chat_utils.MAX_MESSAGE_LEN:
            return False
        if msg[1:].strip():
            return True
        return False

    def _isValidCommand(self, msg):
        msgClass = chat_utils.getMsgClass(msg)
        if msgClass != chat_utils.MESSAGE_CLASS_COMMAND:
            return False
        if len(msg) > chat_utils.MAX_MESSAGE_LEN:
            return False
        return True

    def _makeTimeStamp(self, msgType):
        color = chat_utils.getColor(msgType)
        tStruct = time.localtime(time.time())
        return '{colorCode}[{h:0>2}:{m:0>2}:{s:0>2}]'.format(colorCode=color, h=tStruct.tm_hour, m=tStruct.tm_min, s=tStruct.tm_sec)

    def _sendTargetMsg(self, msg):
        self.base.targetMessage(msg)
        msg = self.clearBadwords(msg)
        msgType = chat_utils.getMsgType(msg)
        if msgType is None:
            return
        else:
            if msgType == chat_utils.MESSAGE_PRIVATE:
                nickAndTxt = msg[1:].split(' ', 1)
                nickName = nickAndTxt[0]
                message = None
                if len(nickAndTxt) > 1:
                    message = nickAndTxt[1]
                if message is not None:
                    formatted = self._formatRawMessage(message, msgType, nickName, True)
                    tStamp = self._makeTimeStamp(msgType)
                    mask = chat_utils.getMask(msgType)
                    self._printChatLine(formatted, mask, tStamp)
            return

    def _sendWorldMsg(self, msg):
        self.cell.worldMessage(msg)
        msg = self.clearBadwords(msg)
        msgType = chat_utils.getMsgType(msg)
        formatted = self._formatRawMessage(msg, msgType, u'', True)
        tStamp = self._makeTimeStamp(msgType)
        mask = chat_utils.getMask(msgType)
        if msgType is None:
            return
        else:
            self._printChatLine(formatted, mask, tStamp)
            return

    def _sendComand(self, command):
        if not self.chatConsoleCommand(command):
            self.cell.runCommand(command)

    def _makeHLink(self, sourceName):
        if sourceName.lower() == self.name.lower():
            return sourceName
        else:
            return u'<hlink={0};chatConsole_{0};normal>'.format(sourceName)

    def _formatRawMessage(self, raw_msg, msg_type, source, myMessage = False):
        color = u''
        tagStr = chat_utils.getChannelTag(msg_type)
        sourceStr = u''
        if source is not None and source != u'':
            sourceStr = self._makeHLink(source)
        if msg_type == chat_utils.MESSAGE_PRIVATE:
            if myMessage:
                return u'{0}{1}[{2}] -> {3}: {4}'.format(color, tagStr, lc('Common.chat.MESSAGE_FROM_ME_NAME'), sourceStr, raw_msg)
            else:
                return u'{0}{1} {2} [{3}]: {4}'.format(color, tagStr, lc('Common.chat.MESSAGE_FROM_DELIMETER'), sourceStr, raw_msg)
        if msg_type == chat_utils.MESSAGE_SYSTEM:
            return u'{0}{1}'.format(color, raw_msg)
        elif msg_type == chat_utils.MESSAGE_CLAN:
            return u'{0}{1}[{2}]: {3}'.format(color, tagStr, sourceStr, raw_msg)
        if msg_type == chat_utils.MESSAGE_GENERAL:
            if myMessage:
                return u'{0}{1}: {2}'.format(color, self.name, raw_msg)
            else:
                return u'{0}{1}: {2}'.format(color, sourceStr, raw_msg)
        if msg_type == chat_utils.MESSAGE_TRADE:
            if myMessage:
                return u'{0}{1}: {2}'.format(color, self.name, raw_msg[1:])
            else:
                return u'{0}{1}: {2}'.format(color, sourceStr, raw_msg)
        if msg_type == chat_utils.MESSAGE_PARTY:
            return u'{0}{1}[{2}]: {3}'.format(color, tagStr, sourceStr, raw_msg)
        elif msg_type == chat_utils.MESSAGE_DAMAGE_DEALT:
            return u'{0}{1}'.format(color, raw_msg)
        elif msg_type == chat_utils.MESSAGE_DAMAGE_TAKEN:
            return u'{0}{1}'.format(color, raw_msg)
        elif msg_type == chat_utils.MESSAGE_ITEMS:
            return u'{0}{1}'.format(color, raw_msg)
        elif msg_type == chat_utils.MESSAGE_QUEST:
            return u'{0}{1}'.format(color, raw_msg)
        elif msg_type == chat_utils.MESSAGE_NPC:
            return u'{0}{1}'.format(color, raw_msg)
        elif msg_type == chat_utils.MESSAGE_ANNOUNCMENT:
            return u'{0}{1}'.format(color, raw_msg)
        else:
            return u''

    def _printChatLine(self, txt, mask, tStamp):
        txt = txt.replace('&amp;', '&')
        txt = txt.replace('&lt;', '<')
        txt = txt.replace('&gt;', '>')
        txt = txt.replace('&quot;', '"')
        BWPersonality.GUICore.chatPrint(mask, txt, tStamp)

    def putMessage(self, msg, msg_type, source = u'', isDelayed = False):
        msg = self.clearBadwords(msg)
        formatted = self._formatRawMessage(msg, msg_type, source, False)
        tStamp = self._makeTimeStamp(msg_type)
        if isDelayed:
            cc = tStamp[:tStamp.find('>') + 1]
            formatted = u'{0}{1}'.format(cc, formatted)
            tStamp = u''
        mask = chat_utils.getMask(msg_type)
        BWPersonality.GUICore.chatPrint(mask, formatted, tStamp)
        if msg_type == chat_utils.MESSAGE_ANNOUNCMENT:
            self.systemMessage(msg, 4283453695L)

    def sendMessage(self, msg):
        if BigWorld.time() - self.lastChatAt < chat_utils.MIN_MESSAGE_FREQUENCY:
            return False
        self.lastChatAt = BigWorld.time()
        msgClass = chat_utils.getMsgClass(msg)
        if msgClass == chat_utils.MESSAGE_CLASS_TARGET:
            if self._isValidTargetMsg(msg):
                self._sendTargetMsg(msg)
                return True
            else:
                return False
        elif msgClass == chat_utils.MESSAGE_CLASS_WORLD:
            if self._isValidWorldMsg(msg):
                self._sendWorldMsg(msg)
                return True
            else:
                return False
        else:
            if msgClass == chat_utils.MESSAGE_CLASS_COMMAND:
                self._sendComand(msg)
                return True
            return False

    def inputValidator(self, newStr, wholeText, offset):
        if len(wholeText + newStr) > chat_utils.MAX_MESSAGE_LEN:
            return False
        return True

    def partyJoinRequest(self, nick):
        BigWorld.player().inviteInGroup((u'/invite', unicode(nick.decode('utf-8'))))

    def clanJoinRequest(self, nick):
        charname = nick.encode('utf-8')
        BigWorld.player().inviteFriendToClan(charname)

    def chatContextHandler(self, interface_id, id, caption, event):
        from soGUI import soContextMenuComponent
        if interface_id != GUI_ID.GUI_ID_CHATCONSOLE:
            self.context_operation_target = None
            return
        else:
            if event == soContextMenuComponent.EVENT_SELECT:
                if self.context_operation_target:
                    if id == self.CONTEXT_INVITE_PARTY:
                        self.partyJoinRequest(self.context_operation_target)
                    elif id == self.CONTEXT_INVITE_CLAN:
                        self.clanJoinRequest(self.context_operation_target)
                    elif id == self.CONTEXT_ADD_TO_FRIEND:
                        BigWorld.player().addFriend(self.context_operation_target.encode('utf-8'))
                    elif id == self.CONTEXT_ADD_TO_IGNORE:
                        BigWorld.player().addToBlackList(self.context_operation_target.encode('utf-8'))
            elif event == soContextMenuComponent.EVENT_CANCEL:
                self.context_operation_target = None
            return

    def hlinkEventHandler(self, event, data):
        from soGUI import soHyperLinkComponent
        id = data[0]
        if not isinstance(id, unicode):
            return
        if event == 2 and id.startswith('URL:'):
            import webbrowser
            webbrowser.open(id[4:])
        nick = u''
        if id.startswith(u'chatConsole_'):
            prefixAndNick = id.split('_', 1)
            if len(prefixAndNick) > 1:
                nick = prefixAndNick[1]
                if event == soHyperLinkComponent.EVENT_CLICK:
                    BWPersonality.GUICore.chatPromt(u'@{0} '.format(nick), replaceTag=True, eraseOld=True, activating=True)
                if event == soHyperLinkComponent.EVENT_RCLICK:
                    actions = {self.CONTEXT_INVITE_PARTY: lc('Common.chat.INVITE_PLAYER_PARTY').format(invited_nick=nick),
                     self.CONTEXT_INVITE_CLAN: lc('Common.chat.INVITE_PLAYER_CLAN').format(invited_nick=nick),
                     self.CONTEXT_ADD_TO_FRIEND: lc('Common.chat.CONTEXT_ADD_TO_FRIEND').format(Nick=nick),
                     self.CONTEXT_ADD_TO_IGNORE: lc('Common.chat.CONTEXT_ADD_TO_IGNORE').format(Nick=nick)}
                    self.context_operation_target = nick
                    BWPersonality.GUICore.showContextMenu(GUI_ID.GUI_ID_CHATCONSOLE, actions)