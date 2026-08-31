# Embedded file name: scripts/client/soGUI/PVPScore.py
import BWPersonality
import BigWorld
import soGUI.ScaleformDemo
import GUI
import time
import traceback
import csconstans

class PVPScore(object):
    """docstring for ClassName"""
    TIMEUPDATE = 0.02
    MARKERHEIGHT = 0.3
    CAM_FAR_PLANE = 0.3
    scale = 100
    playerListVisible = False

    def __init__(self):
        self.lastData = None
        print 'create PVPScore'
        self.gamePlay = -1
        pathTimer = 'scaleformUI/statTimer.swf'
        pathScore = 'scaleformUI/scorebarDM.swf'
        pathTScore = 'scaleformUI/scorebarTDM.swf'
        self.fClipDMscore = soGUI.ScaleformDemo.ScaleformDemo.create(pathScore, 0.0)
        cmp = self.fClipDMscore
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2.7
        cmp.height = 2
        w, h = BigWorld.screenSize()
        cmp.position = (w / 2, 0, 0.1)
        GUI.reSort()
        cmp.focus = 1
        cmp.mouseButtonFocus = 1
        cmp.visible = 0
        BWPersonality.GUICore.generalLayer.delChild('PVPScoreDM')
        BWPersonality.GUICore.generalLayer.addChild(self.fClipDMscore, 'PVPScoreDM')
        self.fClipTDMscore = soGUI.ScaleformDemo.ScaleformDemo.create(pathTScore, 0.0)
        cmp = self.fClipTDMscore
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2.7
        cmp.height = 2
        w, h = BigWorld.screenSize()
        cmp.position = (w / 2, 0, 0.1)
        GUI.reSort()
        cmp.focus = 1
        cmp.mouseButtonFocus = 1
        cmp.visible = 0
        BWPersonality.GUICore.generalLayer.delChild('PVPScoreTDM')
        BWPersonality.GUICore.generalLayer.addChild(self.fClipTDMscore, 'PVPScoreTDM')
        self.fClipTimer = soGUI.ScaleformDemo.ScaleformDemo.create(pathTimer, 0.0)
        self.fClipTimer.script.ignoreHandleKeyEvent = True
        cmp = self.fClipTimer
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 300
        cmp.height = 100
        w, h = BigWorld.screenSize()
        cmp.position = (w / 2, 0.0, 0.1)
        GUI.reSort()
        cmp.focus = 1
        cmp.mouseButtonFocus = 1
        BWPersonality.GUICore.generalLayer.delChild('PVPScoreTimer')
        BWPersonality.GUICore.generalLayer.addChild(self.fClipTimer, 'PVPScoreTimer')
        self.fClipDMscore.script.setExternalInterfaceCallback(self.externalInterfaceHandler)
        self.fClipTimer.script.setExternalInterfaceCallback(self.externalInterfaceHandler)
        return

    def externalInterfaceHandler(self, cmd, args):
        print 'calb:', [cmd, args]
        if cmd == 'playerSelect':
            self.onPlayerSelect(args[0])
        if cmd == 'setVisibleScore':
            self.onSetVisibleScore(args[0])
        if cmd == 'changeVisibleScore':
            self.changeVisibleScore()

    def getClip(self):
        if self.gamePlay == csconstans.GAMEPLAY_DM:
            return self.fClipDMscore
        return self.fClipTDMscore

    def setScoreData(self, data):
        self.lastData = data
        print 'create setScoreData'
        if self.gamePlay != data.gameInfo.gamePlay:
            self.gamePlay = data.gameInfo.gamePlay
            self.fClipDMscore.visible = False
            self.fClipTDMscore.visible = False
            self.getClip().visible = True
        clip = self.getClip()
        if not data:
            return
        clip.script.viewX.invoke(('clearPlayerList',))
        meeName = getattr(BigWorld.player(), 'name', u'')
        spectarots = ''
        MeScore = 0
        for player in data.players:
            if player.name == meeName:
                MeScore = int(player.kills)
            if player.teamID == csconstans.TEAM_NO:
                spectarots = spectarots + player.name + '; '
            else:
                clip.script.viewX.invoke(('appendToPlayerList',
                 player.teamID,
                 player.name.encode('utf8'),
                 player.kills,
                 player.deaths,
                 0,
                 meeName == player.name))

        clip.script.viewX.invoke(('setSpectatorNamesString', spectarots))
        clip.script.viewX.invoke(('sortPlayersList',))
        LimitCountPlayers = data.gameInfo.maxPlayers
        CountPlayers = len(data.players)
        timeServerDiff = BigWorld.player().timeServerDiff
        if data.gameInfo.gamePlay in [csconstans.GAMEPLAY_DM, csconstans.GAMEPLAY_TEAM_DM]:
            clientstarttime = data.gameInfo.gameTimeStart + timeServerDiff
            timeLimit = data.gameInfo.gameTimeLimit
        else:
            clientstarttime = data.gameInfo.roundTimeStart + timeServerDiff
            timeLimit = data.gameInfo.roundTimeLimit
        timeLostSec = -(time.time() - (clientstarttime + timeLimit))
        redWins = str(data.gameInfo.teamRedWins)
        blueWins = str(data.gameInfo.teamBlueWins)
        if data.gameInfo.gamePlay == csconstans.GAMEPLAY_DM:
            redWins = blueWins = ''
        limitWins = '/ %s' % data.gameInfo.winLimit
        clip.script.viewX.invoke(('updateGameInfo',
         timeLostSec,
         MeScore,
         redWins,
         blueWins,
         limitWins,
         CountPlayers,
         LimitCountPlayers))
        self.fClipTimer.script.viewX.invoke(('updateTimer', timeLostSec))
        self.fClipTimer.script.viewX.invoke(('setScore', redWins, blueWins))
        self.fClipTimer.script.viewX.invoke(('setTeam', BigWorld.player().teamID))

    def changeTeamPVP(self, *e):
        self.fClipTimer.script.viewX.invoke(('setTeam', BigWorld.player().teamID))

    def setVisibleScore(self, value):
        self.getClip().visible = value
        BWPersonality.GUICore.setBestCursor()

    def onSetVisibleScore(self, value):
        self.playerListVisible = value

    def onPlayerSelect(self, name):
        pass

    def changeVisibleScore(self):
        self.getClip().visible = not self.getClip().visible
        BWPersonality.GUICore.setBestCursor()

    def scoreBarVisible(self):
        return self.getClip().visible

    def onSetBestCursor(self, cursor):
        print 'onSetBestCursor', cursor
        self.fClipTimer.focus = cursor
        self.fClipTimer.mouseButtonFocus = cursor
        if not cursor:
            self.fClipDMscore.visible = False
            self.fClipTDMscore.visible = False

    def pvpScoreWinTeam(self, teamID):
        msg = u'\u041f\u041e\u0411\u0415\u0414\u0410' if teamID == BigWorld.player().teamID else u'\u041f\u041e\u0420\u0410\u0416\u0415\u041d\u0418\u0415'
        self._showHeadMsg(msg, True)

    def pvpScoreWinPlayer(self, playerName):
        msg = u'\u041f\u041e\u0411\u0415\u0414\u0410' if playerName == BigWorld.player().name else u'\u041f\u041e\u0420\u0410\u0416\u0415\u041d\u0418\u0415, \u043f\u043e\u0431\u0435\u0434\u0438\u043b %s' % playerName
        self._showHeadMsg(msg, True)

    def pvpScoreStartRound(self):
        msg = u''
        if self.lastData:
            msg = getGamplayName(self.lastData.gameInfo.gamePlay)
        self._showHeadMsg(msg)

    def _showHeadMsg(self, msg, doShow = False):
        clip = self.getClip()
        clip.script.viewX.invoke(('setHeadMsg', msg))
        if doShow:
            self.setVisibleScore(True)

    def show(self):
        self.fClipTimer.visible = True

    def hide(self):
        self.fClipDMscore.visible = False
        self.fClipTDMscore.visible = False
        self.fClipTimer.visible = False


def getGamplayName(idGameplay):
    d = {csconstans.GAMEPLAY_DM: u'\u0412\u0441\u0435 \u043f\u0440\u043e\u0442\u0438\u0432 \u0432\u0441\u0435\u0445',
     csconstans.GAMEPLAY_TEAM_DM: u'\u041a\u043e\u043c\u0430\u043d\u0434\u0430 \u043d\u0430 \u043a\u043e\u043c\u0430\u043d\u0434\u0443',
     csconstans.GAMEPLAY_BOMB: u'BOMB',
     csconstans.GAMEPLAY_FLAG: u'FLAG'}
    return d.get(idGameplay, u'@@@@@@@@@@@@')