# Embedded file name: scripts/common/chat_utils.py
from gui_const import CHAT_CONSOLE
from Localization import lc
import colorCodes
MESSAGE_DAMAGE_DEALT = 0
MESSAGE_DAMAGE_TAKEN = 1
MESSAGE_ITEMS = 2
MESSAGE_SYSTEM = 3
MESSAGE_QUEST = 4
MESSAGE_NPC = 5
MESSAGE_GENERAL = 6
MESSAGE_CLAN = 7
MESSAGE_PARTY = 8
MESSAGE_PRIVATE = 9
MESSAGE_FRIENDS = 10
MESSAGE_TRADE = 11
MESSAGE_ANNOUNCMENT = 12
MESSAGE_DAMAGE = MESSAGE_DAMAGE_DEALT
MESSAGE_CLASS_TARGET = 0
MESSAGE_CLASS_WORLD = 1
MESSAGE_CLASS_COMMAND = 2
TAG_CLAN = u'%'
TAG_PARTY = u'+'
TAG_PRIVATE = u'@'
TAG_COMMAND = u'/'
TAG_TRADE = u'#'
MAX_MESSAGE_LEN = 400
MIN_MESSAGE_FREQUENCY = 1
MAX_MESSAGE_COUNT = 200
GENERAL_RANGE = 20

def allTypes():
    return [MESSAGE_DAMAGE_DEALT,
     MESSAGE_DAMAGE_TAKEN,
     MESSAGE_ITEMS,
     MESSAGE_SYSTEM,
     MESSAGE_QUEST,
     MESSAGE_NPC,
     MESSAGE_GENERAL,
     MESSAGE_CLAN,
     MESSAGE_PARTY,
     MESSAGE_PRIVATE,
     MESSAGE_FRIENDS,
     MESSAGE_TRADE,
     MESSAGE_DAMAGE]


def getMask(msg_type):
    if msg_type == MESSAGE_DAMAGE_DEALT or msg_type == MESSAGE_DAMAGE_TAKEN:
        return CHAT_CONSOLE.MESSAGE_DAMAGE
    elif msg_type == MESSAGE_ITEMS:
        return CHAT_CONSOLE.MESSAGE_ITEMS
    elif msg_type == MESSAGE_SYSTEM or msg_type == MESSAGE_ANNOUNCMENT:
        return CHAT_CONSOLE.MESSAGE_SYSTEM
    elif msg_type == MESSAGE_QUEST:
        return CHAT_CONSOLE.MESSAGE_QUEST
    elif msg_type == MESSAGE_NPC:
        return CHAT_CONSOLE.MESSAGE_NPC
    elif msg_type == MESSAGE_GENERAL:
        return CHAT_CONSOLE.MESSAGE_GENERAL
    elif msg_type == MESSAGE_CLAN:
        return CHAT_CONSOLE.MESSAGE_CLAN
    elif msg_type == MESSAGE_PARTY:
        return CHAT_CONSOLE.MESSAGE_PARTY
    elif msg_type == MESSAGE_PRIVATE:
        return CHAT_CONSOLE.MESSAGE_PRIVATE
    elif msg_type == MESSAGE_FRIENDS:
        return CHAT_CONSOLE.MESSAGE_FRIENDS
    elif msg_type == MESSAGE_TRADE:
        return CHAT_CONSOLE.MESSAGE_TRADE
    else:
        return 0


def getChannelTag(msg_type):
    if msg_type == MESSAGE_DAMAGE_DEALT:
        return u''
    elif msg_type == MESSAGE_DAMAGE_TAKEN:
        return u''
    elif msg_type == MESSAGE_ITEMS:
        return u''
    elif msg_type == MESSAGE_SYSTEM:
        return u''
    elif msg_type == MESSAGE_QUEST:
        return u''
    elif msg_type == MESSAGE_NPC:
        return u''
    elif msg_type == MESSAGE_GENERAL:
        return u''
    elif msg_type == MESSAGE_CLAN:
        return u'[{0}]'.format(lc('Common.chat.CLAN_CHANNEL_MARK'))
    elif msg_type == MESSAGE_PARTY:
        return u'[{0}]'.format(lc('Common.chat.PARTY_CHANNEL_MARK'))
    elif msg_type == MESSAGE_PRIVATE:
        return u'[{0}]'.format(lc('Common.chat.PRIVATE_CHANNEL_MARK'))
    elif msg_type == MESSAGE_FRIENDS:
        return u''
    elif msg_type == MESSAGE_TRADE:
        return u'[{0}]'.format(lc('Common.chat.TRADE_CHANNEL_MARK'))
    elif msg_type == MESSAGE_ANNOUNCMENT:
        return u''
    else:
        return u''


def getColor(msg_type):
    if msg_type == MESSAGE_DAMAGE_DEALT:
        return colorCodes.tf3_chat_damage
    elif msg_type == MESSAGE_DAMAGE_TAKEN:
        return colorCodes.tf3_chat_wounds
    elif msg_type == MESSAGE_ITEMS:
        return colorCodes.tf3_chat_loot
    elif msg_type == MESSAGE_SYSTEM:
        return colorCodes.tf3_chat_system
    elif msg_type == MESSAGE_QUEST:
        return colorCodes.tf3_chat_quest
    elif msg_type == MESSAGE_NPC:
        return colorCodes.tf3_chat_NPC
    elif msg_type == MESSAGE_GENERAL:
        return colorCodes.tf3_chat_general
    elif msg_type == MESSAGE_CLAN:
        return colorCodes.tf3_chat_guild
    elif msg_type == MESSAGE_PARTY:
        return colorCodes.tf3_chat_group
    elif msg_type == MESSAGE_PRIVATE:
        return colorCodes.tf3_chat_pm
    elif msg_type == MESSAGE_FRIENDS:
        return colorCodes.tf3_chat_friend
    elif msg_type == MESSAGE_TRADE:
        return colorCodes.tf3_chat_trade
    elif msg_type == MESSAGE_ANNOUNCMENT:
        return colorCodes.tf3_chat_announcement
    else:
        return colorCodes.tf3_chat_default


def getMsgClass(msg):
    if not msg:
        return None
    elif msg[0] in [TAG_PRIVATE, TAG_PARTY, TAG_CLAN]:
        return MESSAGE_CLASS_TARGET
    elif msg[0] == TAG_COMMAND:
        return MESSAGE_CLASS_COMMAND
    else:
        return MESSAGE_CLASS_WORLD
        return None


def getMsgType(msg):
    if not msg:
        return None
    elif msg[0] == TAG_PRIVATE:
        return MESSAGE_PRIVATE
    elif msg[0] == TAG_COMMAND:
        return None
    elif msg[0] == TAG_CLAN:
        return MESSAGE_CLAN
    elif msg[0] == TAG_TRADE:
        return MESSAGE_TRADE
    elif msg[0] == TAG_PARTY:
        return MESSAGE_PARTY
    else:
        return MESSAGE_GENERAL
        return None