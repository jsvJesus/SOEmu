# Embedded file name: scripts/client/PlayerAvatarForSoClanScreen.py
import BigWorld
import soGUI
import gui_jokes
from functools import partial
import BWPersonality
import Clan
from Localization import lc

class PlayerAvatarForSoClanScreen:

    def clanBasesUpdate(self, basesData):
        self.basesData = basesData
        baseList = []
        for e in basesData:
            baseList.append(e['name'].decode('utf-8'))

        BWPersonality.GUICore.clanData({'bases': baseList})

    def onBaseNPCSelected(self, npcSpotName):
        npc = self.findBaseNPCBySpotName(npcSpotName)
        selectedData = {'staffTypes': [lc('PlayerAvatarForSoClanScreen.client.STRING_176_6'), lc('PlayerAvatarForSoClanScreen.client.STRING_177_6'), lc('PlayerAvatarForSoClanScreen.client.STRING_178_6')],
         'staffDescription': lc('PlayerAvatarForSoClanScreen.client.STRING_180_23'),
         'shiftCost': 14000,
         'staffExpire': 5000,
         'staffIcon': 'soGUI/maps/test/testIcon.tga'}
        BWPersonality.GUICore.clanData(self.clanRoster)

    def findBaseByName(self, name):
        for e in self.basesData:
            if e['name'] == name:
                return e

    def onBaseSelected(self, baseName):
        self.selectedBase = self.findBaseByName(baseName)

    def findBaseNPCBySpotName(self, npcSpotName):
        for e in self.selectedBase['staff']:
            if e['staffName'] == npcSpotName:
                return e

    def findBaseNPCBySpotAndLevelName(self, npcSpotName, npcLevelName):
        xStaff = self.findBaseNPCBySpotName(npcSpotName)
        for e in xStaff['staffList']:
            if e['selectorName'] == npcLevelName:
                return e

    def clanRanksUpdate(self, ranks, self_id):

        def sortOnOrder(a, b):
            orderA = self.clanRoster['ranksData'][a][0]
            orderB = self.clanRoster['ranksData'][b][0]
            if orderA == orderB:
                return 0
            elif orderA > orderB:
                return -1
            else:
                return 1

        if not hasattr(self, 'clanRoster'):
            self.clanRoster = {}
        if not self.clanRoster.has_key('ranksData'):
            self.clanRoster['ranksData'] = {}
        rankNames = []
        for rank in ranks:
            name = rank['name'].decode('utf-8')
            rankNames.append(name)
            self.clanRoster['ranksData'][name] = [rank['order'], rank['options'], rank['id']]

        rankNames.sort(sortOnOrder)
        self.clanRoster['ranks'] = rankNames
        BWPersonality.GUICore.clanData(dict(ranks=self.clanRoster['ranks'], ranksData=self.clanRoster['ranksData'], rights=self.clanRoster.get('rights', [])))

    def getDurationText(self, duration):
        ret = u''
        if duration:
            day = int(duration / 86400)
            if day > 0:
                ret += u' {0} '.format(day) + lc('Clans.Messages.DAYS')
                duration -= day * 86400
            hours = int(duration / 3600)
            if hours > 0:
                ret += u' {0} '.format(hours) + lc('Clans.Messages.HOURS')
                duration -= hours * 3600
            minutes = int(duration / 60)
            if minutes > 0:
                ret += u' {0} '.format(minutes) + lc('Clans.Messages.MINUTES')
                duration -= minutes * 60
            elif not ret:
                ret += u' ' + lc('Clans.Messages.LESS_THEN_MINUTE')
        return ret

    def getRank(self, member):
        rankName = ''
        if self.clanRoster.has_key('ranksData'):
            for key in self.clanRoster['ranksData'].keys():
                if member['rank'] == self.clanRoster['ranksData'][key][0]:
                    rankName = key
                    break

        if rankName == '':
            print 'Rank NOT FOUND', member['name'], ' ', member['rank']
        return rankName

    def clanMemberRosterUpdate(self, member):
        if hasattr(self, 'clanRoster') and self.clanRoster:
            from time import time
            if member['lastLogin'] == 0:
                onlineStr = lc('Clans.Interface.ONLINE')
            else:
                onlineStr = lc('Clans.Interface.LAST_TIME').format(self.getDurationText(int(time() - member['lastLogin'])))
            rankName = self.getRank(member)
            newDict = {}
            newDict[member['name'].decode('utf-8')] = member['name'].decode('utf-8')
            if not self.clanRoster['members'].has_key(member['name'].decode('utf-8')):
                BWPersonality.GUICore.addMembers(newDict)
            self.clanRoster['members'][member['name'].decode('utf-8')] = [unicode('0'), rankName, onlineStr]
            newDict[member['name'].decode('utf-8')] = self.clanRoster['members'][member['name'].decode('utf-8')]
            BWPersonality.GUICore.setMembers(newDict)
            return

    def clanRosterUpdate(self, roster):
        from time import time
        dt = self.clanRoster
        dt['cName'] = self.clanName.decode('utf-8')
        dt['members'] = {}
        for e in roster:
            if e['lastLogin'] == 0:
                onlineStr = lc('Clans.Interface.ONLINE')
            else:
                onlineStr = lc('Clans.Interface.LAST_TIME').format(self.getDurationText(int(time() - e['lastLogin'])))
            rankName = self.getRank(e)
            dt['members'][e['name'].decode('utf-8')] = [unicode('0'), rankName, onlineStr]
            if e['name'].decode('utf-8') == self.name:
                dt['self'] = e

        dt['rights'] = [(lc('PlayerAvatarForSoClanScreen.client.STRING_335_6'),
          Clan.CLANRIGHT_EDITRANKS,
          True,
          False),
         (lc('PlayerAvatarForSoClanScreen.client.STRING_336_6'),
          Clan.CLANRIGHT_PROMOTE,
          True,
          False),
         (lc('PlayerAvatarForSoClanScreen.client.STRING_337_6'),
          Clan.CLANRIGHT_INVITE,
          True,
          False),
         (lc('PlayerAvatarForSoClanScreen.client.STRING_338_6'),
          Clan.CLANRIGHT_CLANKICK,
          True,
          False),
         (lc('PlayerAvatarForSoClanScreen.client.STRING_339_6'),
          Clan.CLANRIGHT_DAILYQUOTES,
          True,
          False),
         (lc('PlayerAvatarForSoClanScreen.client.STRING_340_6'),
          Clan.CLANRIGHT_BASESUPERVISOR,
          True,
          False),
         (lc('PlayerAvatarForSoClanScreen.client.STRING_341_6'),
          Clan.CLANRIGHT_WARMASTER,
          True,
          False),
         (lc('PlayerAvatarForSoClanScreen.client.STRING_342_6'),
          Clan.CLANRIGHT_ITEMUSE,
          True,
          False),
         (lc('PlayerAvatarForSoClanScreen.client.USED_DONATE_SHOP'),
          Clan.CLANRIGHT_USED_DONATE_SHOP,
          True,
          False)]
        dt['allRights'] = [[lc('PlayerAvatarForSoClanScreen.client.STRING_345_6'),
          Clan.CLANRIGHT_EDITRANKS,
          True,
          False],
         [lc('PlayerAvatarForSoClanScreen.client.STRING_346_6'),
          Clan.CLANRIGHT_PROMOTE,
          True,
          False],
         [lc('PlayerAvatarForSoClanScreen.client.STRING_347_6'),
          Clan.CLANRIGHT_INVITE,
          True,
          False],
         [lc('PlayerAvatarForSoClanScreen.client.STRING_348_6'),
          Clan.CLANRIGHT_CLANKICK,
          True,
          False],
         [lc('PlayerAvatarForSoClanScreen.client.STRING_349_6'),
          Clan.CLANRIGHT_DAILYQUOTES,
          True,
          False],
         [lc('PlayerAvatarForSoClanScreen.client.STRING_350_6'),
          Clan.CLANRIGHT_BASESUPERVISOR,
          True,
          False],
         [lc('PlayerAvatarForSoClanScreen.client.STRING_351_6'),
          Clan.CLANRIGHT_WARMASTER,
          True,
          False],
         [lc('PlayerAvatarForSoClanScreen.client.STRING_352_6'),
          Clan.CLANRIGHT_ITEMUSE,
          True,
          False],
         [lc('PlayerAvatarForSoClanScreen.client.USED_DONATE_SHOP'),
          Clan.CLANRIGHT_USED_DONATE_SHOP,
          True,
          False]]
        if not dt.has_key('ranksData'):
            dt['ranksData'] = {}
        if not dt.has_key('ranks'):
            dt['ranks'] = []
        self.clanRoster = dt
        BWPersonality.GUICore.clanData(dict(rights=self.clanRoster['rights'], self=self.clanRoster['self'] if self.clanRoster.has_key('self') else dict(), cName=self.clanRoster['cName'], members=self.clanRoster['members'], allRights=self.clanRoster['allRights']))
        self.updateClanRights()

    def clanEvent(self, event, data):
        try:
            if data.__class__.__name__ != 'unicode':
                print 'PlayerAvatar::clanEvent', event, data
            else:
                print 'PlayerAvatar::clanEvent', event, data.encode('utf-8')
        except:
            print 'PlayerAvatar::clanEvent', event, '[data not printable]'

        def renameresult(xname, xdata):
            rank = self.getNamedRank(xname)
            cmd = u'/clanrankname ' + unicode(rank[2]) + ' ' + xdata
            self.sendMessage(cmd)

        if event == soGUI.soClanScreen2.EVENT_RANKSELECT:
            if self.clanRoster is not None:
                self.clanRoster['rights'] = self.getRightsListForNamedRank(data)
                BWPersonality.GUICore.clanData({'rights': self.clanRoster['rights']})
        elif event == soGUI.soClanScreen2.EVENT_EDITRIGHT:
            rank = self.getNamedRank(data[0])
            if rank:
                bit = 1 << data[1]
                if data[2]:
                    rank[1] |= bit
                else:
                    rank[1] &= ~bit
                cmd = u'/clanrankoptions ' + unicode(rank[2]) + u' ' + unicode(rank[1])
                self.sendMessage(cmd)
            else:
                print "Can't find selected rank"
        elif event == soGUI.soClanScreen2.EVENT_EDITRANK:
            gui_jokes.inputBox(lc('Clans.Interface.RANK_NAME_TITLE'), lc('Clans.Interface.RANK_NAME_QUESTION') + u':', partial(renameresult, data))
        elif event == soGUI.soClanScreen2.EVENT_BASESELECT:
            base = self.findBaseByName(data.encode('utf-8'))
            self.selectedBase = base
            staffList = []
            for e in base['staff']:
                staffList.append(e['staffName'].decode('utf-8'))

            BWPersonality.GUICore.clanData({'staffList': staffList,
             'staffTypes': []})
            self.selectedStaff = None
        elif event == soGUI.soClanScreen2.EVENT_STAFFTYPESELECT:
            sel = data[0].encode('utf-8')
            found = False
            for e in self.selectedBase['staff']:
                if e['staffName'] == sel:
                    found = True
                    staff = e
                    break

            if not found:
                return
            self.selectedStaff = staff
            staffTypes = []
            for e in staff['staffList']:
                staffTypes.append(e['selectorName'].decode('utf-8'))

            BWPersonality.GUICore.clanData({'staffTypes': staffTypes})
        elif event == soGUI.soClanScreen2.EVENT_STAFFNAMESELECT:
            found = False
            for e in self.selectedStaff['staffList']:
                if e['selectorName'] == data.encode('utf-8'):
                    found = True
                    npc = e
                    break

            if not found:
                return
            npcDict = {'staffDescription': npc['selectorDesc'].decode('utf-8'),
             'shiftCost': npc['shiftCost'],
             'staffExpire': npc['staffExpire']}
            if npc.has_key('staffIcon'):
                npcDict['staffIcon'] = npc['staffIcon']
            BWPersonality.GUICore.clanData(npcDict)
        elif event == soGUI.soClanScreen2.EVENT_CHANGEPVPTIME:
            pass
        elif event == soGUI.soClanScreen2.EVENT_FIREPERSONEL:
            npc = self.findBaseNPCBySpotAndLevelName(self.selectedStaff['staffName'], data[1].encode('utf-8'))
            cmd = u'/clanfire ' + unicode(self.selectedBase['name'].decode('utf-8')) + u' ' + unicode(self.selectedStaff['id']) + u' ' + unicode(npc['level'])
            self.sendMessage(cmd)
        elif event == soGUI.soClanScreen2.EVENT_HIREPERSONEL:
            npc = self.findBaseNPCBySpotAndLevelName(self.selectedStaff['staffName'], data[1].encode('utf-8'))
            cmd = u'/clanhire ' + unicode(self.selectedBase['name'].decode('utf-8')) + u' ' + unicode(self.selectedStaff['id']) + u' ' + unicode(npc['level'])
            self.sendMessage(cmd)
        return

    def getOwnClanRank(self):
        if self.clanRoster.has_key('self'):
            rankID = self.clanRoster['self']['rank']
            for key in self.clanRoster['ranksData']:
                if self.clanRoster['ranksData'][key][2] == rankID:
                    return self.clanRoster['ranksData'][key]

        return None

    def checkOwnClanRight(self, rightNum):
        rank = self.getOwnClanRank()
        if rank:
            return rank[1] & 1 << rightNum
        else:
            return False

    def checkChangeOnOwner(self, target_name):
        name = self.name
        own_rank = self.getOwnClanRank()
        if own_rank and target_name != name:
            return own_rank[0] == 1000
        else:
            return False

    def getNamedRank(self, name):
        if self.clanRoster.has_key('ranksData'):
            if self.clanRoster['ranksData'].has_key(name):
                rank = self.clanRoster['ranksData'][name]
                return rank
        return None

    def updateClanRights(self):
        if self.clanRoster.has_key('self'):
            rankName = None
            rankID = self.clanRoster['self']['rank']
            for key in self.clanRoster['ranksData']:
                if self.clanRoster['ranksData'][key][0] == rankID:
                    rankName = key

            rt = self.getRightsListForNamedRank(rankName)
            if rt:
                rightsIDsOnly = [ e[1] for e in rt if e[3] ]
                BWPersonality.GUICore.setClanRights(rightsIDsOnly)
        return

    def getRightsListForNamedRank(self, name):
        ownRank = self.getOwnClanRank()
        if self.clanRoster.has_key('ranksData'):
            if self.clanRoster['ranksData'].has_key(name):
                canEditRights = self.checkOwnClanRight(0)
                rank = self.clanRoster['ranksData'][name]
                rights = []
                for num in xrange(len(self.clanRoster['allRights'])):
                    rights.append(self.clanRoster['allRights'][num])
                    if rank[1] & 1 << num:
                        rights[-1][3] = True
                    else:
                        rights[-1][3] = False
                    if canEditRights and rank[0] < ownRank[0]:
                        rights[-1][2] = True
                    else:
                        rights[-1][2] = False

                return rights

    def getStaffListForNPCType(self, npcType, maxLevel, expires):
        xlist = []
        if npcType == 0:
            for level in range(maxLevel):
                xlist.append({'npcType': npcType,
                 'level': level + 1,
                 'selectorName': lc('PlayerAvatarForSoClanScreen.client.STRING_594_25', True) + str(level + 1) + ')',
                 'selectorDesc': lc('PlayerAvatarForSoClanScreen.client.STRING_595_25', True),
                 'shiftCost': 5000 * (level + 1),
                 'staffCurrent': 0,
                 'staffExpire': expires})

        elif npcType == 1:
            for level in range(maxLevel):
                xlist.append({'npcType': npcType,
                 'level': level + 1,
                 'selectorName': lc('PlayerAvatarForSoClanScreen.client.STRING_607_25', True) + str(level + 1) + ')',
                 'selectorDesc': lc('PlayerAvatarForSoClanScreen.client.STRING_608_25', True),
                 'shiftCost': 5000 * (level + 1),
                 'staffCurrent': 0,
                 'staffExpire': expires})

        if npcType == 2:
            for level in range(maxLevel):
                xlist.append({'npcType': npcType,
                 'level': level,
                 'selectorName': lc('PlayerAvatarForSoClanScreen.client.STRING_620_25', True) + str(level) + ')',
                 'selectorDesc': lc('PlayerAvatarForSoClanScreen.client.STRING_621_25', True),
                 'shiftCost': 5000 * (level + 1),
                 'staffCurrent': 0,
                 'staffExpire': expires})

        if npcType == 3:
            for level in range(maxLevel):
                xlist.append({'npcType': npcType,
                 'level': level + 1,
                 'selectorName': lc('PlayerAvatarForSoClanScreen.client.STRING_633_25', True) + str(level + 1) + ')',
                 'selectorDesc': lc('PlayerAvatarForSoClanScreen.client.STRING_634_25', True),
                 'shiftCost': 5000 * (level + 1),
                 'staffCurrent': 0,
                 'staffExpire': expires})

        return xlist

    def findNpcDataByName(self, selName):
        pass