# Embedded file name: scripts/client/soGUI/data/TTFeed.py
from Localization import lc
import BWPersonality
from soGUI.soToolTipComponent import soToolTipComponent
import collections

class TTFeeder(object):

    def __init__(self):
        self.TTMap = {'hlink_test': u'HYPER LINK TEST TOOLTIP',
         'system_bar_quest': lc('TTFeed.data.STRING_13_25'),
         'system_bar_GPS': lc('TTFeed.data.STRING_14_23'),
         'system_bar_TPC': lc('TTFeed.data.STRING_15_23'),
         'system_bar_character': lc('TTFeed.data.STRING_16_29'),
         'system_bar_inventory': lc('TTFeed.data.STRING_17_29'),
         'rightsEditor_up': lc('TTFeed.data.STRING_18_24'),
         'rightsEditor_down': lc('TTFeed.data.STRING_19_26'),
         'rightsEditor_add': lc('TTFeed.data.STRING_20_25'),
         'rightsEditor_delete': lc('TTFeed.data.STRING_21_28'),
         'rightsEditor_edit': lc('TTFeed.data.STRING_22_26'),
         'party_frames_hidebuffs': lc('TTFeed.data.STRING_23_31'),
         'party_frames_showbuffs': lc('TTFeed.data.STRING_24_31'),
         'party_frames_maximize_member': lc('TTFeed.data.STRING_25_37'),
         'party_frames_minimize_member': lc('TTFeed.data.STRING_26_37'),
         'player_frame_party_settings': lc('TTFeed.data.STRING_27_36'),
         'PC_trade_enter_money': lc('TTFeed.data.STRING_28_29'),
         'chat_console_enter_btn': lc('TTFeed.data.STRING_29_31'),
         'chat_console_settings_btn': lc('TTFeed.data.STRING_30_34'),
         'leveling_gui_invest_experience': lc('TTFeed.data.STRING_31_39'),
         'premium_button': lc('TTFeed.data.button_premium'),
         'push_gold': lc('TTFeed.data.push_gold'),
         'push_money': lc('TTFeed.data.push_money'),
         'give_gold': lc('TTFeed.data.give_gold'),
         'give_money': lc('TTFeed.data.give_money')}

    def toolTipEvent(self, id, iid, event):
        if event == soToolTipComponent.EVENT_SHOW:
            if not isinstance(id, collections.Hashable):
                return
            if self.TTMap.has_key(id):
                BWPersonality.GUICore.showToolTip(self.TTMap[id], None)
        return