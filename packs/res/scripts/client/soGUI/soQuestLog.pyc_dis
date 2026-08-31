# Embedded file name: scripts/client/soGUI/soQuestLog.py
from Localization import lc
import BigWorld
import BWPersonality
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
from soGUI.soList import soList, soList2, soList2ElementBase
from soGUI.soTextField import soTextField
from soGUI.soTextField import soTextField2
from soGUI.soTextField import soTxtFieldPropsStructure
from soGUI.soButton import soButton
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI import PyGUIBase
from soGUI.soTabletScreen import soTabletScreen
from gui_const import GUI_ID, QUESTLOG

class soQuestLog(PyGUI.PyGUIBase):
    factoryString = 'soGUI.soQuestLog'
    EVENT_SELECT = 0
    EVENT_CANCEL = 1
    EVENT_SHARE = 2

    def __init__(self, component):
        PyGUI.PyGUIBase.__init__(self, component)
        component.script = self
        self.questMap = {}
        self.setupRoot()
        self.setupQuestList()
        self.setupQuestControls()
        GUI.reSort()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 700
        cmp.height = 450
        cmp.position = (-1.0, 1.0, 0.15)
        cmp.textureName = ''
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.visible = False

    def setupQuestList(self):
        closeBox = soButton(GUI.Window())
        cmp = closeBox.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (346, 4, 0.1)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        frame = GUI.Frame2('soGUI/maps/con_frame.tga')
        cmp = frame
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 350
        cmp.height = 450
        cmp.position = (0, 0, 0.9)
        cmp.visible = True
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'logFrame')
        caption = GUI.Text(lc('soQuestLog.soGUI.STRING_87_21'))
        caption.font = 'ruRU_calibri_default.font'
        caption.colour = (155, 157, 71, 255)
        caption.materialFX = 'BLEND'
        caption.horizontalPositionMode = caption.verticalPositionMode = 'PIXEL'
        caption.horizontalAnchor = 'LEFT'
        caption.verticalAnchor = 'TOP'
        caption.position = (4, 4, 0.5)
        self.component.addChild(caption, 'caption')
        topLine = GUI.Simple('soGUI/maps/Colours/darkGrey.tga')
        topLine.tiled = True
        topLine.tileWidth = 1
        topLine.tileHeight = 1
        topLine.colour = (255, 255, 255, 255)
        topLine.materialFX = 'BLEND'
        topLine.verticalPositionMode = topLine.horizontalPositionMode = 'PIXEL'
        topLine.widthMode = topLine.heightMode = 'PIXEL'
        topLine.verticalAnchor = 'TOP'
        topLine.horizontalAnchor = 'LEFT'
        topLine.pixelSnap = False
        topLine.width = 346
        topLine.height = 1
        topLine.position = (2, 30, 0.4)
        self.component.addChild(topLine, 'topLine')
        questList = soList(GUI.Window(), soGUI.ListPropsStructure(width=350, height=420, isMultiSel=False, selectCallBack=self.onSelected, sorted=False))
        questList.component.horizontalPositionMode = questList.component.verticalPositionMode = 'PIXEL'
        questList.component.widthMode = questList.component.heightMode = 'PIXEL'
        questList.component.visible = True
        questList.component.verticalAnchor = 'TOP'
        questList.component.horizontalAnchor = 'LEFT'
        questList.component.position = (0, 31, 0.1)
        self.component.addChild(questList.component, 'list')
        questList.onBound()

    def setupQuestControls(self):
        frame = GUI.Frame2('soGUI/maps/con_frame.tga')
        cmp = frame
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 350
        cmp.height = 450
        cmp.position = (350, 0, 0.9)
        cmp.visible = True
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'manageFrame')
        topLine = GUI.Simple('soGUI/maps/Colours/darkGrey.tga')
        topLine.tiled = True
        topLine.tileWidth = 1
        topLine.tileHeight = 1
        topLine.colour = (255, 255, 255, 255)
        topLine.materialFX = 'BLEND'
        topLine.verticalPositionMode = topLine.horizontalPositionMode = 'PIXEL'
        topLine.widthMode = topLine.heightMode = 'PIXEL'
        topLine.verticalAnchor = 'TOP'
        topLine.horizontalAnchor = 'LEFT'
        topLine.pixelSnap = False
        topLine.width = 346
        topLine.height = 1
        topLine.position = (352, 30, 0.4)
        self.component.addChild(topLine, 'topLine2')
        bottomLine = GUI.Simple('soGUI/maps/Colours/darkGrey.tga')
        bottomLine.tiled = True
        bottomLine.tileWidth = 1
        bottomLine.tileHeight = 1
        bottomLine.colour = (255, 255, 255, 255)
        bottomLine.materialFX = 'BLEND'
        bottomLine.verticalPositionMode = bottomLine.horizontalPositionMode = 'PIXEL'
        bottomLine.widthMode = bottomLine.heightMode = 'PIXEL'
        bottomLine.verticalAnchor = 'TOP'
        bottomLine.horizontalAnchor = 'LEFT'
        bottomLine.pixelSnap = False
        bottomLine.width = 346
        bottomLine.height = 1
        bottomLine.position = (352, 415, 0.4)
        self.component.addChild(bottomLine, 'bottomLine')
        txt = soTextField2(GUI.Window(), soTxtFieldPropsStructure(width=346, height=384, textureless=True, autoScroll=False))
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (352, 31, 0.5)
        self.component.addChild(cmp, 'infoText')
        txt.onBound()
        shareBtn = soButton(GUI.Window())
        cmp = shareBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 169
        cmp.height = 29
        cmp.position = (354, 417, 0.1)
        shareBtn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        shareBtn.onBound()
        shareBtn.setVisualState('normal')
        cmp.label.text = lc('soQuestLog.soGUI.STRING_252_19')
        self.component.addChild(cmp, 'shareBtn')
        cancelBtn = soButton(GUI.Window())
        cmp = cancelBtn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 169
        cmp.height = 29
        cmp.position = (527, 417, 0.1)
        cancelBtn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cancelBtn.onBound()
        cancelBtn.setVisualState('normal')
        cmp.label.text = lc('soQuestLog.soGUI.STRING_270_19')
        self.component.addChild(cmp, 'cancelBtn')
        caption = GUI.Text(lc('soQuestLog.soGUI.STRING_275_21'))
        caption.font = 'ruRU_calibri_default.font'
        caption.colour = (155, 157, 71, 255)
        caption.materialFX = 'BLEND'
        caption.horizontalPositionMode = caption.verticalPositionMode = 'PIXEL'
        caption.horizontalAnchor = 'LEFT'
        caption.verticalAnchor = 'TOP'
        caption.position = (354, 4, 0.5)
        self.component.addChild(caption, 'questName')

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'questLog')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        self.onSelected()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, GUI_ID.GUI_ID_QUESTLOG)
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, GUI_ID.GUI_ID_QUESTLOG)

    def setDescription(self, description):
        txtField = self.component.infoText.script
        txtField.setText(description)

    def onSelected(self):
        if len(self.component.list.script.getSelection()) == 0:
            BWPersonality.GUICore.questLogEvent(0, self.EVENT_SELECT)
            return False
        caption = self.component.list.script.getSelection()[0]
        if self.questMap.has_key(caption):
            BWPersonality.GUICore.questLogEvent(self.questMap[caption], self.EVENT_SELECT)

    def update(self):
        dataSection = BWPersonality.GUICore.questLogDataSection
        if dataSection is None:
            self.component.list.script.clear()
            self.setDescription('')
            return
        else:
            self.component.list.script.clear()
            for quest in dataSection:
                id = quest['QuestID']
                title = quest['Title']
                self.questMap[title] = id
                self.component.list.script.addElement(title)

            return

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        BWPersonality.GUICore.showTabletPC(True)
        BWPersonality.GUICore.setBestCursor()

    @PyGUIEvent('shareBtn', 'onClick')
    def onShareClick(self):
        BWPersonality.GUICore.questLogEvent(None, self.EVENT_SHARE)
        return

    @PyGUIEvent('cancelBtn', 'onClick')
    def onCancelClick(self):
        BWPersonality.GUICore.questLogEvent(None, self.EVENT_CANCEL)
        return


QL_FRAME_NORMAL = BigWorld.PyTextureProvider('soGUI/maps/Group/frame_stroka.dds')
QL_FRAME_SELECT = BigWorld.PyTextureProvider('soGUI/maps/Group/framr_stroka_select.dds')
QL_ICON_FAILED = None
QL_ICON_COMPLETED = None
QL_ICON_TRACKED = BigWorld.PyTextureProvider('soGUI/maps/Controls/radialbox_small.tga')

def cleanup():
    del QL_FRAME_NORMAL
    del QL_FRAME_SELECT


class questlogElem(soList2ElementBase):
    factoryString = 'soGUI.questlogElem'

    def __init__(self, component, id, data):
        soList2ElementBase.__init__(self, component)
        component.script = self

    def setupRoot(self):
        soList2ElementBase.setupRoot(self)
        cmp = self.component
        cmp.horizontalAnchor = 'LEFT'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 281
        cmp.height = 23
        cmp.position.x = 0
        cmp.position.z = 0.1

    def setupContent(self):
        cmp = GUI.Frame2('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.width = cmp.height = 2.0
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0.0, 0.0, 0.9)
        cmp.texture = QL_FRAME_NORMAL
        self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 15

    def elementEvent(self, event, data):
        return None

    def isActive(self):
        return False

    def isEnabled(self):
        return False

    def activate(self, byUser = True):
        return False

    def deactivate(self, byUser = True):
        return False

    def enable(self):
        return False

    def disable(self):
        return False

    def getDims(self):
        return None

    def getID(self):
        return self.id

    def applyElemData(self):
        return None

    def setElemData(self, data):
        self.elemData = data
        self.applyElemData()


class soQuestLog_Rebirth(PyGUIBase):
    factoryString = 'soGUI.soQuestLog_Rebirth'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        self.interfaceID = GUI_ID.GUI_ID_QUESTLOG
        component.script = self
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 675
        cmp.height = 514
        cmp.position = (0.0, 0.0, 0.5)

    def setupContent(self):
        closeBox = soButton(GUI.Window())
        cmp = closeBox.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (346, 4, 0.1)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')

    def update(self):
        return None

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'questlog')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False