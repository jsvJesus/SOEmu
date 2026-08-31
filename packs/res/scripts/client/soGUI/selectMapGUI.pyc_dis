# Embedded file name: scripts/client/soGUI/selectMapGUI.py
import BigWorld
import BWPersonality
import GUI
import time
import Scaleform
import Keys
import Helpers.PyGUI as PyGUI
import weakref
import traceback
from bwdebug import *

class SelectMapGUI(PyGUI.PyGUIBase):
    calb = None

    def __init__(self, component):
        self.callbackID = 0
        self.listIDRooms = set()
        PyGUI.PyGUIBase.__init__(self, component)
        BWPersonality.GUICore.generalLayer.addChild(component, 'SelectMapGUI')
        self.bk = Background(GUI.Window())
        self.bk.onBound()

    @staticmethod
    def create(movieName = 'scaleformUI/select_map5.swf', backgroundAlpha = 0):
        wde = BigWorld.worldDrawEnabled()
        BigWorld.worldDrawEnabled(False)
        view, movie = Scaleform.createMovieInstance(movieName)
        BigWorld.worldDrawEnabled(wde)
        if view is None:
            ERROR_MSG("Error loading Scaleform movie '%s'" % (movieName,))
            return
        else:
            view.backgroundAlpha = backgroundAlpha
            component = GUI.Flash(view)
            component.width = 2
            component.height = 2
            component.materialFX = 'BLEND'
            component.focus = True
            component.mouseButtonFocus = True
            component.crossFocus = True
            component.moveFocus = True
            component.dragFocus = True
            component.script = SelectMapGUI(component)
            component.script.viewX = view
            component.script.movieX = movie
            component.widthMode = component.heightMode = 'CLIP'
            component.horizontalAnchor = 'CENTER'
            component.verticalAnchor = 'CENTER'
            component.position = (0.0, 0.0, 0.5)
            component.horizontalPositionMode = component.verticalPositionMode = 'CLIP'
            view.setExternalInterfaceCallback(component.script.externalInterfaceHandler)
            return component

    def externalInterfaceHandler(self, cmd, args):
        if cmd == 'createMap':
            self.createMap(args)
        if cmd == 'connectToMap':
            self.connect2Map(args)
        if cmd == 'exit':
            BWPersonality.GUICore.showSelectMap(False)
        if self.calb:
            self.calb(cmd, args)

    def clearMapInfo(serlf):
        self.viewX.invoke(('clearMapList',))

    def updatePVPRoomsIDs(self, listIDRooms):
        if not listIDRooms:
            self.viewX.invoke(('clearMapList',))

    def updateMapInfo(self, data, listIDRooms):
        listIDRooms = set(listIDRooms)
        if self.listIDRooms:
            for servID in self.listIDRooms.difference(listIDRooms):
                self.viewX.invoke(('removeServer', servID))

        self.listIDRooms = listIDRooms
        geometry = data.gameInfo.geometry.strip('space/')
        clientstarttime = data.gameInfo.gameTimeStart + BigWorld.player().timeServerDiff
        timeLimit = data.gameInfo.gameTimeLimit
        timeLostSec = -(time.time() - (clientstarttime + timeLimit))
        self.viewX.invoke(('appendToMapList',
         data.roomID,
         geometry,
         'RU:' + geometry,
         data.countPlayers,
         data.gameInfo['maxPlayers'],
         data.gameInfo['gamePlay'],
         data.gameInfo['connectType'],
         data.gameInfo['isUserType'],
         timeLostSec))

    def createMap(self, args):
        _, connectType, _, friendlyfire, _, winLimit, _, geometry, _, roundTimeLimit, _, gameTimeLimit, _, timeOfday, _, maxPlayers, _, gamePlay = args
        param = {'connectType': connectType,
         'title': u'',
         'gamePlay': gamePlay,
         'geometry': 'spaces/' + geometry,
         'winLimit': winLimit,
         'gameTimeLimit': gameTimeLimit * 60,
         'gameTimeStart': 0,
         'roundTimeStart': 0,
         'roundTimeLimit': roundTimeLimit * 60,
         'teamBlueWins': 0,
         'teamRedWins': 0,
         'isUserType': 0,
         'friendlyfire': friendlyfire,
         'maxPlayers': maxPlayers,
         'weather': '',
         'timeOfday': timeOfday}
        print 'createMap:', param
        BigWorld.player().base.createRoom(param)
        BigWorld.player().base.getAllRooms()

    def connect2Map(self, args):
        BigWorld.player().cell.connectToRoom(args[0])
        BWPersonality.GUICore.showSelectMap(False)

    def handleKeyEvent(self, event):
        return self.component.movie.handleKeyEvent(event)

    def handleMouseButtonEvent(self, comp, event):
        return self.component.movie.handleMouseButtonEvent(event)

    def handleMouseEvent(self, comp, event):
        return self.component.movie.handleMouseEvent(event)

    def allowAutoDefocus(self):
        return True

    def update(self):
        if self.callbackID:
            BigWorld.cancelCallback(self.callbackID)
        self.callbackID = 0
        try:
            BigWorld.player().base.getAllRooms()
            self.callbackID = BigWorld.callback(3, self.update)
        except:
            traceback.print_exc()
            self.hide()

    def show(self):
        self.visible = True
        self.viewX.visible = True
        self.mouseButtonFocus = True
        self.crossFocus = True
        self.moveFocus = True
        self.dragFocus = True
        self.focus = True
        self.component.mouseButtonFocus = True
        self.component.crossFocus = True
        self.component.moveFocus = True
        self.component.dragFocus = True
        self.component.focus = True
        self.bk.show()
        self.update()

    def hide(self):
        if self.callbackID:
            BigWorld.cancelCallback(self.callbackID)
        self.callbackID = 0
        self.visible = False
        self.viewX.visible = False
        self.mouseButtonFocus = False
        self.crossFocus = False
        self.moveFocus = False
        self.dragFocus = False
        self.focus = False
        self.component.mouseButtonFocus = 0
        self.component.crossFocus = 0
        self.component.moveFocus = 0
        self.component.dragFocus = 0
        self.component.focus = 0
        self.bk.hide()


class Background(PyGUI.PyGUIBase):
    factoryString = 'soGUI.Background'

    def __init__(self, component):
        PyGUI.PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 0, 0, 245)
        cmp.materialFX = 'BLEND'
        cmp.textureName = 'soGUI/maps/Colours/black.bmp'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        cmp.visible = False
        cmp.moveFocus = True
        cmp.crossFocus = True
        cmp.mouseButtonFocus = True

    def setupContent(self):
        pass

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.generalLayer.delChild('selectMapBack')
            BWPersonality.GUICore.generalLayer.addChild(self.component, 'selectMapBack')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False