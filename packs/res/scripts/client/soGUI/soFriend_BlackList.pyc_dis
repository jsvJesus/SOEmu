# Embedded file name: scripts/client/soGUI/soFriend_BlackList.py
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import BWPersonality
from Helpers.PyGUI.PyGUIBase import PyGUIBase
import gui_jokes
from Settings import Settings
from soGUI.soButton import soButton
from soGUI.soCheckBox import soCheckBox
from Helpers.PyGUI import PyGUIEvent
from gui_const import MESSAGEBOX
from Localization import lc
from soGUI.soTableComponent import soTableComponent2, soTablePropsStructure, soTableElemPropsStructure
from functools import partial

class FriendList(PyGUIBase):
    factoryString = 'soGUI.FriendList'
    TAB_FRIEND = 0
    TAB_BLACK = 1
    FRAME_TEXTURE = 'soGUI/maps/Controls/inventory/inventoryFrame2.tga'
    EVENT_SEND_MESSAGE = 0
    EVENT_DEL_FRIEND = 1
    EVENT_ADD_TO_GROUP = 2
    EVENT_ADD_TO_CLAN = 3
    EVENT_DEL_FROM_BLACKLIST = 0
    TAB_LABELS = {TAB_FRIEND: lc('GUI.FriendList.CaptionTabFriend'),
     TAB_BLACK: lc('GUI.FriendList.CaptionTabBlack')}

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        self.COLORFONTONLINE = (70, 161, 68, 255)
        self.COLORFONTOFFLINE = (140, 141, 126, 255)
        component.script = self
        self.friendTable_captionOnline = {'font': 'ruRU_calibri_default.font',
         'color': (28, 28, 28, 0),
         'hoverColor': (28, 28, 28, 0),
         'selectColor': (28, 28, 28, 255),
         'toolTipID': None,
         'contentColor': self.COLORFONTONLINE,
         'contentColorHover': self.COLORFONTONLINE,
         'contentColorSelect': self.COLORFONTONLINE}
        self.friendTable_captionOffline = {'font': 'ruRU_calibri_default.font',
         'color': (28, 28, 28, 0),
         'hoverColor': (28, 28, 28, 0),
         'selectColor': (28, 28, 28, 255),
         'toolTipID': None,
         'contentColor': self.COLORFONTOFFLINE,
         'contentColorHover': self.COLORFONTOFFLINE,
         'contentColorSelect': self.COLORFONTOFFLINE}
        self.sortOnNames = False
        self.Menu = None
        self.notifyState = None
        self.selectedFriend = None
        self.selectedIgnore = None
        self.blackList = []
        self.listFriend = []
        self.setupRoot()
        self.setupContent()
        self.setupFriends()
        self.setupBlackList()
        self.tabSelect(self.TAB_FRIEND)
        return

    def setupRoot(self):
        self.component.textureName = ''
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.width = 250
        self.component.height = 400
        self.component.position = (1.0, 0.3, 0.1)
        self.component.horizontalAnchor = 'RIGHT'
        self.component.verticalAnchor = 'TOP'
        self.component.visible = False

    def setupContent(self):
        self.frameCmp = GUI.Frame2(FriendList.FRAME_TEXTURE)
        self.frameCmp.horizontalPositionMode = self.frameCmp.verticalPositionMode = 'CLIP'
        self.frameCmp.widthMode = self.frameCmp.heightMode = 'CLIP'
        self.frameCmp.horizontalAnchor = 'CENTER'
        self.frameCmp.verticalAnchor = 'CENTER'
        self.frameCmp.visible = 1
        self.frameCmp.colour = (255, 255, 255, 255)
        self.frameCmp.materialFX = 'BLEND'
        self.frameCmp.width = 2.0
        self.frameCmp.height = 2.0
        self.frameCmp.position = (0.0, 0.0, 50.0)
        self.component.addChild(self.frameCmp, 'theFrame')
        closeBox = soButton(GUI.Window())
        cmp = closeBox.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (self.component.width - cmp.width + 8, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        closeBox.onClick = self.onCloseBox
        self.component.addChild(cmp, 'closeBox')
        for i, tab in enumerate([self.TAB_FRIEND, self.TAB_BLACK]):
            btn = soButton(GUI.Window())
            cmp = btn.component
            cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 120
            cmp.height = 17
            cmp.position = (2 + i * cmp.width, 30, 0.4)
            btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
            btn.onClick = partial(self.tabSelect, tab)
            btn.initVSC('soGUI/visual_styles/skillTab.xml')
            btn.onBound()
            btn.setVisualState('normal')
            cmp.label.text = self.TAB_LABELS[tab]
            self.component.addChild(btn.component, 'tab' + str(tab))

    def tabSelect(self, tab):
        for _tab in [self.TAB_FRIEND, self.TAB_BLACK]:
            tabCmp = getattr(self.component, 'tab' + str(_tab))
            tabCmp.script.buttonActive = False if tab != _tab else True
            tabCmp.script._updateVisualState()
            wnd = self._getTabWnd(_tab)
            wnd.visible = False if tab != _tab else True

    def setupFriends(self):
        wnd = GUI.Window()
        wnd.horizontalPositionMode = wnd.verticalPositionMode = 'PIXEL'
        wnd.widthMode = wnd.heightMode = 'PIXEL'
        wnd.horizontalAnchor = 'LEFT'
        wnd.verticalAnchor = 'TOP'
        wnd.materialFX = 'BLEND'
        wnd.colour = (255, 255, 255, 255)
        wnd.width = 242
        wnd.height = 312
        wnd.position = (4, 50, 0.2)
        wnd.visible = False
        self.component.addChild(wnd, 'wnd' + str(self.TAB_FRIEND))
        cmp = GUI.Frame2('soGUI/maps/Controls/window_frame/options_inner_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        cmp.visible = 1
        wnd.addChild(cmp, 'innerFrame')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 100
        cmp.height = 20
        cmp.position = (10, 370, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp.visible = 1
        btn.onClick = self.onAddFriend
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = lc('GUI.FriendList.add')
        self.component.addChild(btn.component, 'bAdd')
        cb = soCheckBox(GUI.Window(), default_style='soGUI/visual_styles/checkBoxSettings.xml')
        cb.onStateChange = self.notifyOnStateChange
        cmp = cb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (120, 370, 0.3)
        self.component.addChild(cmp, 'isNotify')
        cb.onBound()
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (154, 147, 100, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (140, 380, 0.3)
        cmp.text = lc('GUI.FriendList.isNotify')
        self.component.addChild(cmp, 'isNotifyCaption')
        self.notifyState = Settings().getNotifyFriendList()
        if self.notifyState:
            self.component.isNotify.script.setActive()
        else:
            self.component.isNotify.script.setInactive()
        tbl = soTableComponent2(GUI.Window(), soTablePropsStructure(tableHeight=310, tableWidth=242, outerBorderWidth=0, innerBorderWidth=0), isFriendList='True')
        cmp = tbl.component
        tbl.onElementEvent = self.onKeyTableElem
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (2, 0, 0.9)
        self.component.wnd0.addChild(cmp, 'TableFriends')
        tbl.onBound()
        tbl.addCols([['name', 220]])

    def setupBlackList(self):
        wnd = GUI.Window()
        wnd.horizontalPositionMode = wnd.verticalPositionMode = 'PIXEL'
        wnd.widthMode = wnd.heightMode = 'PIXEL'
        wnd.horizontalAnchor = 'LEFT'
        wnd.verticalAnchor = 'TOP'
        wnd.materialFX = 'BLEND'
        wnd.colour = (255, 255, 255, 255)
        wnd.width = 242
        wnd.height = 312
        wnd.position = (4, 50, 0.2)
        wnd.visible = False
        self.component.addChild(wnd, 'wnd' + str(self.TAB_BLACK))
        cmp = GUI.Frame2('soGUI/maps/Controls/window_frame/options_inner_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        wnd.addChild(cmp, 'innerFrame')
        tbl = soTableComponent2(GUI.Window(), soTablePropsStructure(tableHeight=310, tableWidth=242, outerBorderWidth=0, innerBorderWidth=0), isFriendList='True')
        cmp = tbl.component
        tbl.onElementEvent = self.onKeyTableElemBlackList
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (2, 0, 0.9)
        self.component.wnd1.addChild(cmp, 'TableBlackList')
        tbl.onBound()
        tbl.addCols([['name', 220]])

    def _getTabWnd(self, tab):
        wnd = getattr(self.component, 'wnd' + str(tab))
        return wnd

    def onCloseBox(self):
        self.hide()

    def onAddFriend(self):
        if self.component.tab0.script.buttonActive:
            gui_jokes.inputBox(lc('GUI.FriendList.addToFriendListCaption'), lc('GUI.FriendList.readFriendNameCaption'), self.addToFriendList)
        else:
            gui_jokes.inputBox(lc('GUI.FriendList.addToBlackListCaption'), lc('GUI.FriendList.readFriendNameCaption'), self.addToFriendList)

    def addToFriendList(self, text):
        if self.component.tab0.script.buttonActive:
            BigWorld.player().addFriend(text.encode('utf-8'))
        else:
            BigWorld.player().addToBlackList(text.encode('utf-8'))

    def onDelFriend(self, friendName):

        def deletingFriendCallback(event):
            if event == gui_jokes.askUserYesNo.YES:
                BigWorld.player().delFriend(friendName)

        text = lc('GUI.FriendList.deletingFromFriendList1') + ' ' + friendName.decode('utf8') + ' ' + lc('GUI.FriendList.deletingFromFriendList2')
        gui_jokes.askUserYesNo(lc('GUI.FriendList.delFriend'), text, deletingFriendCallback)

    def displayFriendList(self, wayOfSort):
        self.listFriend = BigWorld.player().getFriendList()
        self.listFriend.sort(key=lambda item: item[1], reverse=1)
        tbl = self.component.wnd0.TableFriends.script
        rows = []
        for i, friend in enumerate(self.listFriend):
            if friend[1] == 1:
                rows.append([(20, 'MIDDLE'), {'name': {'props': soTableElemPropsStructure(dataStyles=self.friendTable_captionOnline),
                           'data': {'text': friend[0].decode('utf8')}}}])
            else:
                rows.append([(20, 'MIDDLE'), {'name': {'props': soTableElemPropsStructure(dataStyles=self.friendTable_captionOffline),
                           'data': {'text': friend[0].decode('utf8')}}}])

        tbl.clearTable()
        tbl.addRows(rows)

    def onKeyTableElem(self, col, row, event, data):
        tbl = self.component.wnd0.TableFriends.script
        if event == 'RIGHTMOUSE':
            tbl.clearSelection()
            tbl.selectRow(row)
            self.selectedFriend = self.listFriend[row][0]
            actions = {self.EVENT_SEND_MESSAGE: lc('GUI.FriendList.sendMessage'),
             self.EVENT_DEL_FRIEND: lc('GUI.FriendList.delFriend'),
             self.EVENT_ADD_TO_GROUP: lc('GUI.FriendList.addToGroup'),
             self.EVENT_ADD_TO_CLAN: lc('GUI.FriendList.addToClan')}
            self.StartFriendNameContextMenu(actions, BWPersonality.GUICore.GUI_ID_FRIENDLISTPOPUP)
        elif event == 'LEFTMOUSE':
            tbl.clearSelection()
            tbl.selectRow(row)

    def StartFriendNameContextMenu(self, actions, interface_id):
        BWPersonality.GUICore.addListener('contextMenuEvent', self.FriendListContextMenuEvent)
        BWPersonality.GUICore.showContextMenu(interface_id, actions)

    def FriendListContextMenuEvent(self, interface_id, id, caption, event):
        if interface_id is not BWPersonality.GUICore.GUI_ID_FRIENDLISTPOPUP:
            return
        if event == soGUI.soContextMenuComponent.EVENT_SELECT:
            if id == self.EVENT_SEND_MESSAGE:
                BWPersonality.GUICore.chatConsole.component.edit.script.setValue('@' + self.selectedFriend.decode('utf-8') + ' ')
                BWPersonality.GUICore.chatConsole.component.edit.script.activate(True)
            elif id == self.EVENT_DEL_FRIEND:
                self.onDelFriend(self.selectedFriend)
            elif id == self.EVENT_ADD_TO_GROUP:
                BigWorld.player().inviteInGroup((u'/invite', unicode(self.selectedFriend.decode('utf-8'))))
            elif id == self.EVENT_ADD_TO_CLAN:
                BigWorld.player().inviteFriendToClan(self.selectedFriend)
            BWPersonality.GUICore.removeListener('contextMenuEvent', self.FriendListContextMenuEvent)

    def displayBlackList(self, wayOfSort = 0):
        self.blackList = BigWorld.player().getBlackList()
        tbl = self.component.wnd1.TableBlackList.script
        rows = []
        for i, name in enumerate(self.blackList):
            rows.append([(20, 'MIDDLE'), {'name': {'props': soTableElemPropsStructure(dataStyles=self.friendTable_captionOffline),
                       'data': {'text': name.decode('utf8')}}}])

        tbl.clearTable()
        tbl.addRows(rows)

    def blackLists(self):
        print 'DEBUG ', self.blackList

    def onKeyTableElemBlackList(self, col, row, event, data):
        tbl = self.component.wnd1.TableBlackList.script
        if event == 'RIGHTMOUSE':
            tbl.clearSelection()
            tbl.selectRow(row)
            self.selectedIgnore = self.blackList[row]
            actions = {self.EVENT_DEL_FROM_BLACKLIST: lc('GUI.FriendList.delFromBlackList')}
            self.StartBlackListContextMenu(actions, BWPersonality.GUICore.GUI_ID_BLACKLISTPOPUP)
        elif event == 'LEFTMOUSE':
            tbl.clearSelection()
            tbl.selectRow(row)

    def StartBlackListContextMenu(self, actions, interface_id):
        BWPersonality.GUICore.addListener('contextMenuEvent', self.BlackListContextMenuEvent)
        BWPersonality.GUICore.showContextMenu(interface_id, actions)

    def BlackListContextMenuEvent(self, interface_id, id, caption, event):
        if interface_id is not BWPersonality.GUICore.GUI_ID_BLACKLISTPOPUP:
            return
        if event == soGUI.soContextMenuComponent.EVENT_SELECT:
            if id == self.EVENT_DEL_FROM_BLACKLIST:
                BigWorld.player().delFromBlackList(self.selectedIgnore)
            BWPersonality.GUICore.removeListener('contextMenuEvent', self.FriendListContextMenuEvent)

    def isBlackList(self, name):
        return self.blackList.count(name)

    def notifyOnStateChange(self):
        self.notifyState = self.component.isNotify.script.isChecked()
        Settings().setNotifyFriendList(self.notifyState)

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'Lists')
        self.displayFriendList(0)
        self.displayBlackList(0)
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()