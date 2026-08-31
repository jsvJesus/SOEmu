# Embedded file name: scripts/client/soGUI/soTPCQuestLog.py
from Localization import lc
import BigWorld
import GUI
import soGUI
import Helpers.PyGUI as PyGUI
import BWPersonality
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soButton import soButton, soButtonWFT
from soGUI.soTabletScreen import soTabletScreen
from soGUI.soList import soList
from soGUI.soTextField import soTextField2
from soGUI.soTextField import soTextField3
from soGUI.soTextField import soTxtFieldPropsStructure
from Helpers.PyGUI import PyGUIEvent
from soGUI.data import GUIEvents
from soGUI.soList import soList2, soList2ElementBase
from gui_const import GUI_ID, QUESTLOG

class soQuestElem(soList2ElementBase):
    factoryString = 'soGUI.soQuestElem'

    def __init__(self, component, id, data):
        soList2ElementBase.__init__(self, component, id, data)
        component.script = self

    def setupRoot(self):
        pass


class WantedItem(PyGUIBase):
    HEIGHT = 50
    WIDTH = 782

    def __init__(self, component, w):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.HEIGHT = w
        self.setupRoot()
        self.setupContent()
        self.component.visible = False

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = self.WIDTH
        cmp.height = self.HEIGHT
        cmp.position = (0, 0, 0.1)

    def setupContent(self):
        cmp = GUI.Simple('textures/default/white.jpg')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 0, 0, 190)
        cmp.materialFX = 'BLEND'
        cmp.width = self.WIDTH
        cmp.height = 1
        cmp.position = (2, self.HEIGHT, 0.3)
        self.component.addChild(cmp, 'frame1')
        cmp = GUI.Text('wanted_name')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 10, 0.3)
        self.component.addChild(cmp, 'wanted_name')
        cmp = GUI.Text('wanted_status')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (350, 10, 0.3)
        self.component.addChild(cmp, 'wanted_status')
        cmp = GUI.Text('wanted_map')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (520, 10, 0.3)
        self.component.addChild(cmp, 'wanted_map')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 100
        cmp.height = 30
        cmp.position = (self.WIDTH - 5, 7, 0.3)
        cmp.label.text = 'show in map'
        self.component.addChild(cmp, 'bth_show')
        btn.onClick = self._toMap
        btn.onBound()

    def setdata(self, data):
        print 'setdata', data
        if not data:
            self.component.visible = False
            return
        self.component.visible = True
        wantedname, subdata = data
        self.wantedname = wantedname
        self.subdata = subdata
        self.component.wanted_name.text = wantedname
        self.component.wanted_map.visible = False
        self.component.bth_show.visible = False
        if not subdata:
            self.component.wanted_status.text = u'end'
            self.component.wanted_status.colour = (255, 255, 255, 255)
            return
        isOnline, spaceID, position = subdata
        if not isOnline:
            self.component.wanted_status.text = u'offline'
            self.component.wanted_status.colour = (255, 100, 100, 255)
            return
        self.component.wanted_status.text = u'online'
        self.component.wanted_status.colour = (100, 255, 100, 255)
        if spaceID:
            mappath, lcmapName = BWPersonality.GUICore.getSpaceName(spaceID)
            self.component.wanted_map.visible = True
            self.component.wanted_map.text = lcmapName
        if position:
            self.component.bth_show.visible = True

    def _toMap(self):
        print '_toMap', self.subdata
        isOnline, spaceID, position = self.subdata
        mappath, lcmapName = BWPersonality.GUICore.getSpaceName(spaceID)
        BWPersonality.GUICore.showGPS()
        isshowmap = BWPersonality.GUICore.gpsGUI.viewMap(mappath)
        print 'isshowmap:', isshowmap
        if isshowmap:
            BWPersonality.GUICore.showQuestLog(False)
            maps = BWPersonality.GUICore.gpsGUI.maps
            from MapNotes import MapNotes
            from GPSMap import GPSMap
            self.GPSProvider = GPSMap(mappath)
            mappos = self.GPSProvider.GetObjectRelativeCoords(position, mappath)
            markname = self.wantedname.encode('utf8', 'ignore')
            maps[mappath].script.addMark(markname, MapNotes.TYPE_WANTED, mappos, 0.0, (255, 255, 255, 255))
            print 'mappos', mappos
            BWPersonality.GUICore.gpsGUI.centerOnCoords(mappos, mappath)
            charMap = BWPersonality.GUICore.gpsGUI.MAPLIST[BWPersonality.GUICore.gpsGUI.charMap]
            for mark in charMap.marks:
                if charMap.marks[mark].script.isPlayer():
                    charMark = charMap.marks[mark].script

            coords = charMark.getCoords()
            print 'isPlayer coords', coords


class ListWanted(PyGUIBase):
    factoryString = 'soGUI.ListWanted'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 792
        cmp.height = 550
        cmp.position = (0.0, 0.0, 0.1)
        cmp.textureName = ''
        cmp.visible = False

    def setupContent(self):
        self.rows = 9
        for i in range(self.rows):
            wanteditem = WantedItem(GUI.Window(), 40)
            cmp = wanteditem.component
            cmp.position = (0, 40 * i, 0.2)
            self.component.addChild(cmp, 'wanteditem_%s' % i)
            wanteditem.onBound()

    def update(self):
        print 'ListWanted update'
        BigWorld.player().getWantedPosition()

    def updateWanted(self):
        data = BWPersonality.GUICore.listWantedDataSection
        data = data + [ (name, None) for name in BigWorld.player().HUNTER_lostListOfWanted ]
        for i, item in map(lambda a, b: [a, b], range(self.rows), data):
            if i is None:
                return
            witem = getattr(self.component, 'wanteditem_%s' % i)
            witem.script.setdata(item)

        return


class soTPCQuestLog(PyGUIBase):
    factoryString = 'soGUI.soTPCQuestLog'
    MODE_CURRENT = 0
    MODE_COMPLETED = 1
    MODE_WANTED = 3
    EVENT_SELECT = 0
    EVENT_CANCEL = 1
    EVENT_SHARE = 2
    EVENT_TRACK = 3
    EVENT_VIEWCOMPLETED = 4
    EVENT_VIEWCURRENT = 5

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.mode = None
        self.selectedCurrent = None
        self.selectedCompleted = None
        self.setupRoot()
        self.setupContent()
        self.switchMode(self.MODE_CURRENT)
        self.interfaceID = BWPersonality.GUICore.GUI_ID_PDAQUEST
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 792
        cmp.height = 550
        cmp.position = (0.0, 0.0, 0.1)
        cmp.textureName = ''
        cmp.visible = False

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/TabletPC/questLog/doubleFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 786
        cmp.height = 393
        cmp.position = (3, 111, 1.1)
        cmp.visible = 1
        self.component.addChild(cmp, 'doubleFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (14, 67, 0.3)
        cmp.text = lc('GUI.QuestLog.WINDOW_CAPTION')
        self.component.addChild(cmp, 'iLabel')
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 792
        cmp.height = 480
        cmp.position = (0, 61, 1.2)
        self.component.addChild(cmp, 'wndFrame')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/closeBox.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (784, 67, 0.2)
        self.component.addChild(cmp, 'closeBox')
        btn.onBound()
        btn._updateVisualState()
        listw = ListWanted(GUI.Window())
        cmp = listw.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 0, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 786
        cmp.height = 393
        cmp.visible = False
        cmp.position = (3, 111, 0.2)
        self.component.addChild(cmp, 'listw')
        listw.onBound()
        btn = soButtonWFT(GUI.Window())
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/defaultTab.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 180
        cmp.height = 21
        cmp.position = (4, 111, 0.2)
        cmp.label.text = lc('GUI.QuestLog.ACTIVE_QUESTS_TAB_LABEL')
        self.component.addChild(cmp, 'currentBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButtonWFT(GUI.Window())
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/defaultTab.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 180
        cmp.height = 21
        cmp.position = (184, 111, 0.2)
        cmp.label.text = lc('GUI.QuestLog.COMPLETED_QUESTS_TAB_LABEL')
        self.component.addChild(cmp, 'completedBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButtonWFT(GUI.Window())
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/defaultTab.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 180
        cmp.height = 21
        cmp.position = (364, 111, 0.2)
        cmp.label.text = lc('GUI.QuestLog.WANTED_TAB_LABEL')
        btn.onClick = lambda : self.switchMode(self.MODE_WANTED)
        self.component.addChild(cmp, 'wantedBtn')
        btn.onBound()
        btn.setVisualState('normal')
        questList = soList(GUI.Window(), soGUI.ListPropsStructure(width=365, height=399, isMultiSel=False, selectCallBack=self.onSelected, sorted=False))
        questList.component.horizontalPositionMode = questList.component.verticalPositionMode = 'PIXEL'
        questList.component.widthMode = questList.component.heightMode = 'PIXEL'
        questList.component.visible = True
        questList.component.verticalAnchor = 'TOP'
        questList.component.horizontalAnchor = 'LEFT'
        questList.component.position = (4, 111, 0.1)
        questList.component.listFrame.textureName = ''
        self.component.addChild(questList.component, 'list')
        questList.onBound()
        txt = soTextField3(GUI.Window(), width=375, height=287, textWidth=-1, hScroll=False, vScroll=True, hideScroll=True, borderWidth=0, vOffset=0, hOffset=0, textureless=True, autosize=False)
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (380, 129, 0.2)
        self.component.addChild(cmp, 'questDescr')
        txt.onBound()
        cmp = GUI.Frame2('soGUI/maps/Controls/TabletPC/questLog/descriptionFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 419
        cmp.height = 383
        cmp.position = (364, 116, 1.0)
        self.component.addChild(cmp, 'descrFrame')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 100
        cmp.height = 32
        cmp.position = (365, 506, 0.2)
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soTPCQuestLog.soGUI.STRING_280_19')
        self.component.addChild(cmp, 'cancelBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 100
        cmp.height = 32
        cmp.position = (466, 506, 0.2)
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soTPCQuestLog.soGUI.STRING_303_19')
        self.component.addChild(cmp, 'shareBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 100
        cmp.height = 32
        cmp.position = (567, 506, 0.2)
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soTPCQuestLog.soGUI.STRING_327_19')
        self.component.addChild(cmp, 'trackBtn')
        btn.onBound()
        btn.buttonDisabled = True
        btn.setVisualState('disabled')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 100
        cmp.height = 32
        cmp.position = (667, 506, 0.2)
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = 'update'
        btn.onClick = self.component.listw.script.update
        self.component.addChild(cmp, 'updateWantedBtn')
        btn.onBound()
        btn.buttonDisabled = True
        btn.setVisualState('disabled')

    def setDescription(self, txt):
        self.component.questDescr.script.setText(txt)
        self.component.questDescr.script.setCursor(0, 0)

    def switchMode(self, mode):
        needUpdate = False
        if self.mode != mode:
            self.setDescription('')
            self.component.questDescr.script.setCursor(0, 0)
            self.mode = mode
            needUpdate = True
        if mode == self.MODE_WANTED:
            self._setStateBtn(self.component.wantedBtn)
            self._setStateBtn(self.component.updateWantedBtn)
            self._setStateBtn(self.component.currentBtn, False)
            self._setStateBtn(self.component.completedBtn, False)
        elif mode == self.MODE_CURRENT:
            self._setStateBtn(self.component.currentBtn)
            self._setStateBtn(self.component.completedBtn, False)
            self._setStateBtn(self.component.wantedBtn, False)
            self._setStateBtn(self.component.updateWantedBtn, False, disabled=1)
        else:
            self._setStateBtn(self.component.completedBtn)
            self._setStateBtn(self.component.currentBtn, False)
            self._setStateBtn(self.component.wantedBtn, False)
            self._setStateBtn(self.component.updateWantedBtn, False, disabled=1)
        if needUpdate:
            self.update()

    def _setStateBtn(self, btn, active = True, disabled = False):
        btn.script.buttonActive = active
        if disabled:
            btn.script.setVisualState('disabled')
            btn.script.buttonDisabled = True
        else:
            btn.script.setVisualState('active' if active else 'normal')
            btn.script.buttonDisabled = False

    def update(self):
        if self.mode == self.MODE_WANTED:
            self.component.questDescr.visible = False
            self.component.list.visible = False
            self.component.trackBtn.visible = False
            self.component.cancelBtn.visible = False
            self.component.shareBtn.visible = False
            self.component.descrFrame.visible = False
            self.component.listw.visible = True
            self.component.listw.script.update()
            return
        self.component.listw.visible = False
        self.component.questDescr.visible = True
        self.component.list.visible = True
        self.component.trackBtn.visible = True
        self.component.cancelBtn.visible = True
        self.component.shareBtn.visible = True
        self.component.descrFrame.visible = True
        if self.mode == self.MODE_CURRENT:
            quests = BWPersonality.GUICore.questLogDataSection['quests']
        else:
            quests = BWPersonality.GUICore.questLogDataSection['completed']
        self.component.list.script.clear()
        for quest in quests:
            id = quest['QuestID']
            title = quest['Title']
            self.component.list.script.addElement(title, id)

    def onSelected(self):
        if len(self.component.list.script.getSelection()) < 1:
            BWPersonality.GUICore.questLogEvent(0, self.EVENT_SELECT)
            return
        questName = self.component.list.script.getSelection()[0]
        questID = self.component.list.script.getAttachment(questName)
        if questID == questName:
            return
        BWPersonality.GUICore.questLogEvent(questID, self.EVENT_SELECT)

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'questLog')
        if len(self.component.list.script.getSelection()) < 1:
            if len(self.component.list.script.elements) > 0:
                self.component.list.script.elements[0] = 1
        self.onSelected()
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, GUI_ID.GUI_ID_QUESTLOG)
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, GUI_ID.GUI_ID_QUESTLOG)

    def updateWanted(self):
        """updateWanted"""
        self.component.listw.script.updateWanted()

    @PyGUIEvent('cancelBtn', 'onClick')
    def onCancelClick(self):
        BWPersonality.GUICore.questLogEvent(None, self.EVENT_CANCEL)
        return

    @PyGUIEvent('shareBtn', 'onClick')
    def onShareClick(self):
        BWPersonality.GUICore.questLogEvent(None, self.EVENT_SHARE)
        return

    @PyGUIEvent('trackBtn', 'onClick')
    def onTrackClick(self):
        BWPersonality.GUICore.questLogEvent(None, self.EVENT_TRACK)
        return

    @PyGUIEvent('completedBtn', 'onClick')
    def onCompletedClick(self):
        BWPersonality.GUICore.questLogEvent(None, self.EVENT_VIEWCOMPLETED)
        self.switchMode(self.MODE_COMPLETED)
        return

    @PyGUIEvent('currentBtn', 'onClick')
    def onCurrentClick(self):
        BWPersonality.GUICore.questLogEvent(None, self.EVENT_VIEWCURRENT)
        self.switchMode(self.MODE_CURRENT)
        return

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()