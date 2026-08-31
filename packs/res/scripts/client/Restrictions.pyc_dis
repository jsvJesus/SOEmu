# Embedded file name: scripts/client/Restrictions.py
__author__ = 'leviathan'
import BigWorld
import time
from RestrictionsUtils import RestrictionCommon
import BWPersonality
from CallbackHelpers import callback

class Restrictions(RestrictionCommon):
    CALLBACK_ID_STR = 'restriction_channel_'

    def __init__(self):
        self.InitRestrictionArray()
        self.RestrictionActionNames = {}
        self.ClientChannelServerWaiting = {}
        self.RestrictionCallbacks = {}

    def UpdateRestrictions(self):
        return
        index = 0
        for channel in self.restrictions:
            time_left = channel - time.time()
            if time_left < 0:
                time_left = 0
            BWPersonality.GUICore.drawLabel(text='channel ' + str(index) + ' = ' + str(time_left), id=index, x=235, y=7 + 13 * index)
            index += 1

    def DoAction(self, channel, action_duration, name = u'', callback_func = None):
        if action_duration > 0.0:
            self.ClientChannelServerWaiting[channel] = 0
            self.RestrictionActionNames[channel] = name
            self.RestrictionCallbacks[channel] = callback_func

    def CheckRestriction(self, channel):
        client_waiting_restrict = self.ClientChannelServerWaiting.get(channel, 0)
        if client_waiting_restrict:
            self.cell.ConfirmRestriction(channel)
        else:
            if callback.findFirst(self.CALLBACK_ID_STR + str(channel)) is not None:
                return False
            return RestrictionCommon.CheckRestriction(self, channel)
        return

    def ServerRestrict(self, channel, action_duration):
        self.ClientChannelServerWaiting[channel] = 0
        name = self.RestrictionActionNames.get(channel, u'')
        callback_func = self.RestrictionCallbacks.pop(channel, None)
        if callback_func:
            callback(callback_func, action_duration, id=self.CALLBACK_ID_STR + str(channel))
        RestrictionCommon.DoAction(self, channel, action_duration)
        if action_duration != None or action_duration > 0.0:
            data = ['RUN',
             action_duration,
             name,
             0]
            BWPersonality.GUICore.setCastBarData(data)
        return