# Embedded file name: scripts/client/soGUI/soClanScreen.py
import BWPersonality
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import gui_jokes
from soGUI.soButton import soButton, soButtonWTT, soButtonWFT
from soGUI.soList import soList
from Helpers.PyGUI import PyGUIEvent
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soTabletScreen import soTabletScreen
from soGUI.soTableComponent import soTableComponent, tablePropsStructure
from soGUI.soDropDownList import soDropDownList, soDropDownList2
from soGUI.soScrollBar import soScrollBar, soScrollBar2
from Localization import lc
from soGUI.soCheckBox import soCheckBox
from functools import partial
from copy import deepcopy
from soGUI.soTextField import soTextField2
from soGUI.soTextField import soTxtFieldPropsStructure
from soGUI.soTableComponent import soTableComponent2, soTablePropsStructure, soTableElemPropsStructure
from math import ceil, floor
from Helpers.BWCoroutine import *
import Clan

class soClanScreen(PyGUI.Window):
    factoryString = 'soGUI.soClanScreen'


class soClanScreen2(PyGUIBase):
    factoryString = 'soGUI.soClanScreen2'
    DATA_MEMBERS = 0
    DATA_BASE = 1
    DATA_FINANCE = 2
    DATA_GENERAL = 3
    MODE_MEMBERS = 1
    MODE_FINANCE = 2
    MODE_BASES = 3
    EVENT_RANKSELECT = 0
    EVENT_EDITRIGHT = 1
    EVENT_MOVERANK = 2
    EVENT_ADDRANK = 3
    EVENT_DELRANK = 4
    EVENT_EDITRANK = 5
    EVENT_BASESELECT = 6
    EVENT_STAFFTYPESELECT = 7
    EVENT_STAFFNAMESELECT = 8
    EVENT_CHANGEPVPTIME = 9
    EVENT_FIREPERSONEL = 10
    EVENT_HIREPERSONEL = 11
    EVENT_CLANTRADER_SELECT = 0
    EVENT_CLANTRADER_USERINPUT = 1
    EVENT_CLANTRADER_APPLY = 2
    EVENT_CLANTRADER_CANCEL = 3

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.currentMode = None
        self.membersWnd = None
        self.financeWnd = None
        self.basesWnd = None
        self.memberTable_captionDS = {'font': 'ruRU_calibri_default.font',
         'color': (50, 50, 50, 255),
         'hoverColor': (50, 50, 50, 255),
         'selectColor': (50, 50, 50, 255),
         'toolTipID': None,
         'contentColor': (175, 166, 112, 255),
         'contentColorHover': (175, 166, 112, 255),
         'contentColorSelect': (175, 166, 112, 255)}
        self.memberTable_dataDS = {'font': 'ruRU_calibri_default.font',
         'color': (255, 255, 255, 0),
         'hoverColor': (255, 255, 255, 0),
         'selectColor': (28, 28, 28, 255),
         'toolTipID': None,
         'contentColor': (175, 166, 112, 255),
         'contentColorHover': (249, 233, 137, 255),
         'contentColorSelect': (249, 233, 137, 255)}
        self.clanTrade_captionDS = {'font': 'ruRU_calibri_default.font',
         'color': (33, 35, 30, 255),
         'hoverColor': (33, 35, 30, 255),
         'selectColor': (33, 35, 30, 255),
         'toolTipID': None,
         'contentColor': (175, 166, 112, 255),
         'contentColorHover': (175, 166, 112, 255),
         'contentColorSelect': (175, 166, 112, 255)}
        self.clanTrade_dataDS = {'font': 'ruRU_calibri_default.font',
         'color': (255, 255, 255, 0),
         'hoverColor': (255, 255, 255, 0),
         'selectColor': (28, 28, 28, 255),
         'toolTipID': None,
         'contentColor': (175, 166, 112, 255),
         'contentColorHover': (249, 233, 137, 255),
         'contentColorSelect': (249, 233, 137, 255)}
        self.clanTrade_unsavedDataDS = {'font': 'ruRU_calibri_default.font',
         'color': (35, 35, 25, 255),
         'hoverColor': (35, 35, 25, 255),
         'selectColor': (35, 35, 25, 255),
         'toolTipID': None,
         'contentColor': (175, 166, 112, 255),
         'contentColorHover': (249, 233, 137, 255),
         'contentColorSelect': (249, 233, 137, 255)}
        self.rightsCheckBoxes = []
        self.userRights = []
        self.members = []
        self.membersData = {}
        self.setupRoot()
        self.setupContent()
        self.setupGeneral()
        self.setupMembers()
        self.setupFinance()
        self.setupBases()
        self.pvpTimeLeft = 0
        self.shiftTimeLeft = 0
        self.sortType = [0, 0, 0]
        self.switchToMode(self.MODE_MEMBERS)
        self.baseMgrFillLevel = []
        self._applyBaseFillLevel()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 792
        cmp.height = 521
        cmp.position = (0.0, 0.0, 0.1)
        cmp.textureName = ''
        cmp.visible = False
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        cmp.dragFocus = True

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 792
        cmp.height = 444
        cmp.position = (0, 43, 1.2)
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
        cmp.position = (785, 49, 0.2)
        self.component.addChild(cmp, 'closeBox')
        btn.onBound()
        btn._updateVisualState()
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalAnchor = 'LEFT'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colourFormatting = True
        cmp.multiline = False
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (5, 48, 0.2)
        cmp.text = ''
        self.component.wndFrame.addChild(cmp, 'nameLabel')
        self.verticalIndentForBtn = 93
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
        cmp.width = 80
        cmp.height = 21
        cmp.position = (2, self.verticalIndentForBtn, 0.2)
        cmp.label.text = lc('GUI.ClanGUI.MEMBERS_TAB_LABEL')
        self.component.addChild(cmp, 'membersBtn')
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
        cmp.width = 80
        cmp.height = 21
        cmp.position = (81, self.verticalIndentForBtn, 0.2)
        cmp.label.text = lc('GUI.ClanGUI.FINANCE_TAB_LABEL')
        cmp.visible = 0
        self.component.addChild(cmp, 'financeBtn')
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
        cmp.width = 70
        cmp.height = 21
        cmp.position = (160, self.verticalIndentForBtn, 0.2)
        cmp.label.text = lc('GUI.ClanGUI.BASES_TAB_LABEL')
        cmp.visible = 0
        self.component.addChild(cmp, 'basesBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onClick = self.onInviteClanClick
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 140
        cmp.height = 25
        cmp.position = (640, 455, 0.2)
        cmp.visible = True
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.ClanGUI.INVITE_TO_CLAN')
        self.component.addChild(cmp, 'inviteToClanBtn')
        btn.onBound()
        btn.setVisualState('normal')

    def setupGeneral(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 792
        cmp.height = 444
        cmp.position = (0, 0, 1.0)
        cmp.textureName = ''
        cmp.visible = False
        self.component.addChild(cmp, 'generalWnd')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        btn.onClick = self.onRightsBtnClick
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 157
        cmp.height = 25
        cmp.position = (9, 455, 0.2)
        cmp.visible = True
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.Legacy.CONFIGURE_RIGHTS_LABEL')
        self.component.addChild(cmp, 'rightsBtn')
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
        cmp.width = 300
        cmp.height = 25
        cmp.position = (476, 455, 0.2)
        cmp.visible = True
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.Legacy.CLAN_TRADE_MANAGMENT_LABEL')
        self.component.generalWnd.addChild(cmp, 'clantradeBtn')
        btn.onBound()
        btn.setVisualState('normal')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 792
        cmp.height = 521
        cmp.position = (0, 0, 0.05)
        cmp.textureName = ''
        cmp.visible = False
        self.component.generalWnd.addChild(cmp, 'rightsWnd')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (0, 0, 0, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 792
        cmp.height = 444
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.position = (0, 71, 1.0)
        self.component.generalWnd.rightsWnd.addChild(cmp, 'backImg')
        rightsList = soList(GUI.Window(), soGUI.ListPropsStructure(width=245, height=335, isMultiSel=False, selectCallBack=self.onRankSelect, sorted=False))
        rightsList.component.horizontalPositionMode = rightsList.component.verticalPositionMode = 'PIXEL'
        rightsList.component.widthMode = rightsList.component.heightMode = 'PIXEL'
        rightsList.component.visible = True
        rightsList.component.verticalAnchor = 'TOP'
        rightsList.component.horizontalAnchor = 'LEFT'
        rightsList.component.position = (7, 108, 0.1)
        rightsList.component.listFrame.textureName = ''
        self.component.generalWnd.rightsWnd.addChild(rightsList.component, 'ranks')
        rightsList.onBound()
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 515
        cmp.height = 303
        cmp.position = (253, 108, 0.2)
        cmp.textureName = ''
        self.component.generalWnd.rightsWnd.addChild(cmp, 'rightsFrame')
        btn = soButtonWTT(GUI.Window(), 'rightsEditor_up')
        btn.initVSC('soGUI/visual_styles/btn_TPCRightsEditor.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/rightsEditor/button_up.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 28
        cmp.height = 28
        cmp.position = (14, 450, 0.1)
        self.component.generalWnd.rightsWnd.addChild(cmp, 'btnUp')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButtonWTT(GUI.Window(), 'rightsEditor_down')
        btn.initVSC('soGUI/visual_styles/btn_TPCRightsEditor.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/rightsEditor/button_down.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 28
        cmp.height = 28
        cmp.position = (49, 450, 0.1)
        self.component.generalWnd.rightsWnd.addChild(cmp, 'btnDown')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButtonWTT(GUI.Window(), 'rightsEditor_add')
        btn.initVSC('soGUI/visual_styles/btn_TPCRightsEditor.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/rightsEditor/button_add.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 28
        cmp.height = 28
        cmp.position = (116, 450, 0.1)
        self.component.generalWnd.rightsWnd.addChild(cmp, 'btnAdd')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButtonWTT(GUI.Window(), 'rightsEditor_delete')
        btn.initVSC('soGUI/visual_styles/btn_TPCRightsEditor.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/rightsEditor/button_delete.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 28
        cmp.height = 28
        cmp.position = (151, 450, 0.1)
        self.component.generalWnd.rightsWnd.addChild(cmp, 'btnDelete')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButtonWTT(GUI.Window(), 'rightsEditor_edit')
        btn.initVSC('soGUI/visual_styles/btn_TPCRightsEditor.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/rightsEditor/button_edit.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 28
        cmp.height = 28
        cmp.position = (181, 450, 0.1)
        self.component.generalWnd.rightsWnd.addChild(cmp, 'btnEdit')
        btn.onBound()
        btn.setVisualState('normal')
        closeBox = soButton(GUI.Window())
        cmp = closeBox.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (766, 76, 0.1)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        self.component.generalWnd.rightsWnd.addChild(cmp, 'rightsWndcloseBox')
        closeBox.onBound()
        closeBox.setVisualState('normal')

        def rightsWndhide():
            self.component.generalWnd.rightsWnd.visible = False
            self.membersWnd.visible = 1
            self.component.membersBtn.visible = 1
            self.component.financeBtn.visible = 0
            self.component.basesBtn.visible = 0
            self.component.generalWnd.rightsWnd.visible = 0
            self.component.generalWnd.visible = 0

        closeBox.onClick = rightsWndhide
        cmp = GUI.Simple('soGUI/maps/Controls/rightsEditor/del_grey.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 780
        cmp.height = 1
        cmp.position = (6, 73, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.generalWnd.rightsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/rightsEditor/del_grey.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 780
        cmp.height = 1
        cmp.position = (6, 107, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.generalWnd.rightsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/rightsEditor/del_grey.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 780
        cmp.height = 1
        cmp.position = (6, 443, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.generalWnd.rightsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/rightsEditor/del_grey.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 780
        cmp.height = 1
        cmp.position = (6, 482, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.generalWnd.rightsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/rightsEditor/del_grey.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 1
        cmp.height = 410
        cmp.position = (6, 73, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.generalWnd.rightsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/rightsEditor/del_grey.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 1
        cmp.height = 410
        cmp.position = (252, 73, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.generalWnd.rightsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/rightsEditor/del_grey.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 1
        cmp.height = 410
        cmp.position = (785, 73, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.generalWnd.rightsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/rightsEditor/del_green.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 778
        cmp.height = 33
        cmp.position = (7, 74, 1.0)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.generalWnd.rightsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/rightsEditor/del_green.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 778
        cmp.height = 38
        cmp.position = (7, 444, 1.0)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.generalWnd.rightsWnd.addChild(cmp)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (123, 89, 0.9)
        cmp.text = lc('GUI.Legacy.RANKS_LABEL')
        self.component.generalWnd.rightsWnd.addChild(cmp, 'ranksLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (509, 89, 0.9)
        cmp.text = lc('GUI.Legacy.RIGHTS_LABEL')
        self.component.generalWnd.rightsWnd.addChild(cmp, 'rightsLabel')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 792
        cmp.height = 521
        cmp.position = (0, 0, 0.05)
        cmp.textureName = ''
        cmp.visible = False
        self.component.generalWnd.addChild(cmp, 'clanTraderWnd')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (0, 0, 0, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 792
        cmp.height = 444
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.position = (0, 71, 1.0)
        self.component.generalWnd.clanTraderWnd.addChild(cmp, 'backImg')
        ddl = soDropDownList2(GUI.Window(), width=780, height=25)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (6, 80, 0.1)
        self.component.generalWnd.clanTraderWnd.addChild(cmp, 'baseList')
        ddl.onBound()
        ddl.onUserAction = partial(self.onClanTradeMgr, 'BASELIST', None)
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
        cmp.height = 25
        cmp.position = (519, 451, 0.1)
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.Legacy.APPLY_LABEL')
        self.component.generalWnd.clanTraderWnd.addChild(cmp, 'applyBtn')
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
        cmp.height = 25
        cmp.position = (642, 451, 0.1)
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.Legacy.CANCEL_LABEL')
        self.component.generalWnd.clanTraderWnd.addChild(cmp, 'cancelBtn')
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
        cmp.width = 25
        cmp.height = 25
        cmp.position = (747, 451, 0.1)
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = '_'
        self.component.generalWnd.clanTraderWnd.addChild(cmp, 'hideBtn')
        btn.onBound()
        btn.setVisualState('normal')

        def hideclanTraderWnd():
            self.component.generalWnd.clanTraderWnd.visible = False

        btn.onClick = hideclanTraderWnd
        tbl = soTableComponent2(GUI.Window(), soTablePropsStructure(tableHeight=342, tableWidth=780, innerBorderColor=(85, 85, 85, 255)))
        cmp = tbl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (3, 102, 0.0)
        self.component.generalWnd.clanTraderWnd.addChild(cmp, 'priceTable')
        tbl.onBound()
        tbl.addCols([['itemEnabled', 61],
         ['clanOnly', 61],
         ['itemName', 218],
         ['quantity', 39],
         ['baseCost', 64],
         ['buyCost', 64],
         ['sellClanCost', 64],
         ['sellNeutralCost', 64],
         ['sellFriendlyCost', 64],
         ['sellEnemyCost', 64]])
        rows = []
        rows.append([(47, 'TOP'), {'itemEnabled': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                          'data': {'text': lc('GUI.Legacy.TRADE_ITEM_CHOICE')}},
          'clanOnly': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                       'data': {'text': lc('GUI.Legacy.SELL_TO_CLAN_ONLY')}},
          'itemName': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                       'data': {'text': lc('GUI.Legacy.NAME')}},
          'quantity': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                       'data': {'text': lc('GUI.Legacy.QUANTITY_SHORT')}},
          'baseCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                       'data': {'text': lc('GUI.Legacy.BASE_COST')}},
          'buyCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                      'data': {'text': lc('GUI.Legacy.BUY_COST')}},
          'sellClanCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                           'data': {'text': lc('GUI.Legacy.COST_FOR_CLANMATES')}},
          'sellNeutralCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                              'data': {'text': lc('GUI.Legacy.COST_FOR_NEUTRALS')}},
          'sellFriendlyCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                               'data': {'text': lc('GUI.Legacy.COST_FOR_FRIENDS')}},
          'sellEnemyCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                            'data': {'text': lc('GUI.Legacy.COST_FOR_ENEMIES')}}}])
        rows.append([(30, 'TOP'), {'itemEnabled': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                          'data': {'text': u''}},
          'clanOnly': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                       'data': {'text': u''}},
          'itemName': {'props': soTableElemPropsStructure(spanLeft=2, dataStyles=self.clanTrade_captionDS),
                       'data': {'text': lc('GUI.Legacy.SET_COST_IN_PERCENTS')}},
          'buyCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']),
                      'data': {'text': u''}},
          'sellClanCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']),
                           'data': {'text': u''}},
          'sellNeutralCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']),
                              'data': {'text': u''}},
          'sellFriendlyCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']),
                               'data': {'text': u''}},
          'sellEnemyCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']),
                            'data': {'text': u''}}}])
        tbl.addRows(rows)
        return

    def setupMembers(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 792
        cmp.height = 521
        cmp.position = (0, 0, 1.0)
        cmp.textureName = ''
        cmp.visible = False
        cmp.filterType = 'POINT'
        cmp.pixelSnap = False
        self.component.addChild(cmp, 'membersWnd')
        self.membersWnd = cmp
        rows = []
        rows.append([(25, 'TOP'), {'name': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_captionDS),
                   'data': {'text': lc('GUI.Legacy.CLANMATE_NAME')}},
          'rank': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_captionDS),
                   'data': {'text': lc('GUI.Legacy.CLANMATE_RANK')}},
          'status': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_captionDS),
                     'data': {'text': lc('GUI.Legacy.CLANMAE_STATE')}}}])
        tbl = soTableComponent2(GUI.Window(), soTablePropsStructure(tableHeight=358, tableWidth=786, innerBorderColor=(85, 85, 85, 255)))
        cmp = tbl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (3, self.verticalIndentForBtn, 0.0)
        self.component.membersWnd.addChild(cmp, 'membersTable')
        tbl.onBound()
        tbl.addCols([['name', 294], ['rank', 190], ['status', 287]])
        tbl.addRows(rows)

    def setupFinance(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 792
        cmp.height = 521
        cmp.position = (0, 0, 1.0)
        cmp.textureName = ''
        cmp.visible = False
        self.component.addChild(cmp, 'financeWnd')
        self.financeWnd = cmp

    def setupBases(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 792
        cmp.height = 521
        cmp.position = (0, 0, 1.0)
        cmp.textureName = ''
        cmp.visible = False
        self.component.addChild(cmp, 'basesWnd')
        self.basesWnd = cmp
        ddl = soDropDownList2(GUI.Window(), width=780, height=25)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (6, 80, 0.1)
        self.component.basesWnd.addChild(cmp, 'baseList')
        ddl.onBound()
        ddl.onUserAction = partial(self.onBaseMgr, ['baseList'])
        ddl = soDropDownList2(GUI.Window(), width=398, height=25)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (377, 168, 0.1)
        self.component.basesWnd.addChild(cmp, 'nameList')
        ddl.onBound()
        ddl.onUserAction = partial(self.onBaseMgr, ['staffName'])
        hireList = soList(GUI.Window(), soGUI.ListPropsStructure(width=207, height=321, isMultiSel=False, selectCallBack=partial(self.onBaseMgr, ['staffType']), sorted=False))
        hireList.component.horizontalPositionMode = hireList.component.verticalPositionMode = 'PIXEL'
        hireList.component.widthMode = hireList.component.heightMode = 'PIXEL'
        hireList.component.visible = True
        hireList.component.verticalAnchor = 'TOP'
        hireList.component.horizontalAnchor = 'LEFT'
        hireList.component.position = (6, 157, 0.1)
        hireList.component.listFrame.textureName = ''
        self.component.basesWnd.addChild(hireList.component, 'hireList')
        hireList.onBound()
        cmp = GUI.Simple('soGUI/maps/Controls/baseMgr/delim.tga')
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 786
        cmp.height = 1
        cmp.position = (3, 114, 1.0)
        cmp.pixelSnap = False
        self.component.basesWnd.addChild(cmp, 'hline1')
        cmp = GUI.Simple('soGUI/maps/Controls/baseMgr/delim.tga')
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 786
        cmp.height = 1
        cmp.position = (3, 147, 1.0)
        cmp.pixelSnap = False
        self.component.basesWnd.addChild(cmp, 'hline2')
        cmp = GUI.Simple('soGUI/maps/Controls/baseMgr/delim.tga')
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 571
        cmp.height = 1
        cmp.position = (214, 399, 1.0)
        cmp.pixelSnap = False
        self.component.basesWnd.addChild(cmp, 'hline3')
        cmp = GUI.Simple('soGUI/maps/Controls/baseMgr/delim.tga')
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 571
        cmp.height = 1
        cmp.position = (214, 427, 1.0)
        cmp.pixelSnap = False
        self.component.basesWnd.addChild(cmp, 'hline4')
        cmp = GUI.Frame2('soGUI/maps/Controls/baseMgr/pvp_time_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 654
        cmp.height = 30
        cmp.position = (6, 116, 1.0)
        self.component.basesWnd.addChild(cmp, 'pvpTimeFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (60, 125, 0.9)
        cmp.text = lc('soClanScreen.soGUI.STRING_1540_13')
        self.component.basesWnd.addChild(cmp, 'timeFrameLbl')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (409, 125, 0.9)
        cmp.text = lc('soClanScreen.soGUI.STRING_1553_13')
        self.component.basesWnd.addChild(cmp, 'timeleftLbl')
        txt = soTextField2(GUI.Window(), soTxtFieldPropsStructure(autoSize=False, height=190, width=385, vScroll=False, textureless=True))
        cmp = txt.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalAnchor = 'LEFT'
        cmp.position = (375, 200, 0.2)
        txt.onBound()
        txt.setText('')
        self.component.basesWnd.addChild(cmp, 'staffDescription')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (420, 408, 0.9)
        cmp.text = u''
        self.component.basesWnd.addChild(cmp, 'shiftCost')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (413, 447, 0.85)
        cmp.text = u''
        self.component.basesWnd.addChild(cmp, 'expireTime')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 117
        cmp.height = 25
        cmp.position = (668, 119, 0.2)
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soClanScreen.soGUI.STRING_1611_19')
        self.component.basesWnd.addChild(cmp, 'changePvPTime')
        btn.onClick = partial(self.onBaseMgr, ['changeTime'])
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
        cmp.width = 117
        cmp.height = 25
        cmp.position = (224, 440, 0.2)
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soClanScreen.soGUI.STRING_1634_19')
        self.component.basesWnd.addChild(cmp, 'fireBtn')
        btn.onClick = partial(self.onBaseMgr, ['fire'])
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
        cmp.width = 117
        cmp.height = 25
        cmp.position = (660, 440, 0.2)
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soClanScreen.soGUI.STRING_1657_19')
        self.component.basesWnd.addChild(cmp, 'hireBtn')
        btn.onClick = partial(self.onBaseMgr, ['hire'])
        btn.onBound()
        btn.setVisualState('normal')
        cmp = GUI.Frame2('soGUI/maps/Controls/baseMgr/personel_mgr_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 573
        cmp.height = 321
        cmp.position = (213, 157, 0.95)
        self.component.basesWnd.addChild(cmp, 'personelMgrFrame')
        cmp = GUI.Frame2('soGUI/maps/Controls/baseMgr/personel_status_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 286
        cmp.height = 30
        cmp.position = (358, 436, 0.9)
        self.component.basesWnd.addChild(cmp, 'personelStatusFrame')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 143
        cmp.height = 221
        cmp.position = (224, 168, 0.85)
        self.component.basesWnd.addChild(cmp, 'icon')

    def _switchToTab(self, tab):
        visMsk = [False,
         False,
         False,
         False]
        visMsk[tab] = True
        self.component.membersBtn.script.buttonActive = visMsk[self.MODE_MEMBERS]
        self.component.membersBtn.script._updateVisualState()
        self.component.financeBtn.script.buttonActive = visMsk[self.MODE_FINANCE]
        self.component.financeBtn.script._updateVisualState()
        self.component.basesBtn.script.buttonActive = visMsk[self.MODE_BASES]
        self.component.basesBtn.script._updateVisualState()

    def switchToMode(self, mode):
        self._switchToTab(mode)
        if self.currentMode == mode:
            return
        self.currentMode = mode
        modeMask = [False,
         False,
         False,
         False]
        modeMask[mode] = True
        self.membersWnd.visible = modeMask[self.MODE_MEMBERS]

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'clanScreen')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def _updateGeneral(self):
        pass

    def _updateMembers(self):
        pass

    def _updateFinance(self):
        pass

    def _updateClanTrade(self):
        globalPricesIndex = 1
        data = BWPersonality.GUICore.clanTradeDataSection
        tbl = self.component.generalWnd.clanTraderWnd.priceTable.script
        if data.has_key('clanTraders'):
            self.component.generalWnd.clanTraderWnd.baseList.script.clear()
            for clanTrader in data['clanTraders']:
                self.component.generalWnd.clanTraderWnd.baseList.script.addElement(clanTrader)

        if data.has_key('clanTradeGlobalPrices'):
            buyPrice = data['clanTradeGlobalPrices'][0]
            clanPrice = data['clanTradeGlobalPrices'][1]
            neutralPrice = data['clanTradeGlobalPrices'][2]
            friendPrice = data['clanTradeGlobalPrices'][3]
            enemyPrice = data['clanTradeGlobalPrices'][4]
            row = [(30, 'TOP'), {'itemEnabled': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                              'data': {'text': u''}},
              'clanOnly': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                           'data': {'text': u''}},
              'itemName': {'props': soTableElemPropsStructure(spanLeft=2, dataStyles=self.clanTrade_captionDS),
                           'data': {'text': lc('soClanScreen.soGUI.STRING_1772_128')}},
              'buyCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                          'data': {'text': u''}},
              'sellClanCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                               'data': {'text': u''}},
              'sellNeutralCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                                  'data': {'text': u''}},
              'sellFriendlyCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                                   'data': {'text': u''}},
              'sellEnemyCost': {'props': soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS),
                                'data': {'text': u''}}}]
            tbl.delayRender(4)
            tbl.alterElem('buyCost', globalPricesIndex, soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']), {'text': str(buyPrice)})
            tbl.alterElem('sellClanCost', globalPricesIndex, soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']), {'text': str(clanPrice)})
            tbl.alterElem('sellNeutralCost', globalPricesIndex, soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']), {'text': str(neutralPrice)})
            tbl.alterElem('sellFriendlyCost', globalPricesIndex, soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']), {'text': str(friendPrice)})
            tbl.alterElem('sellEnemyCost', globalPricesIndex, soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']), {'text': str(enemyPrice)})
            ([(1001,
               (True, True),
               (False, True),
               lc('soClanScreen.soGUI.STRING_1789_39'),
               15,
               3500,
               (3000, True),
               (3550, True),
               (3700, True),
               (3600, True),
               (4500, False)), (1002,
               (False, False),
               (False, False),
               lc('soClanScreen.soGUI.STRING_1790_42'),
               1,
               1000000,
               (800000, False),
               (1100000, True),
               (1200000, False),
               (1150000, False),
               (1450000, True)), (1003,
               (True, True),
               (True, False),
               lc('soClanScreen.soGUI.STRING_1791_39'),
               2,
               30500,
               (29000, True),
               (31000, False),
               (32000, False),
               (31500, False),
               (34000, False))], 'add')
        if data.has_key('clanTradeItems'):
            items = data['clanTradeItems'][0]
            operation = data['clanTradeItems'][1]
            rows = []

            def resolveDataDS(colName, saved = None):
                if colName in ('itemEnabled', 'clanOnly', 'buyCost', 'sellClanCost', 'sellNeutralCost', 'sellFriendlyCost', 'sellEnemyCost'):
                    if not saved:
                        return self.clanTrade_unsavedDataDS
                    else:
                        return self.clanTrade_dataDS
                else:
                    return self.clanTrade_dataDS

            for item in items:
                rows.append([(25, 'MIDDLE', item[0]), {'itemEnabled': {'props': soTableElemPropsStructure(dataStyles=resolveDataDS('itemEnabled', item[1][1]), dataType=1, rights=['READ', 'EDIT']),
                                  'data': {'text': u'',
                                           'boolState': item[1][0]}},
                  'clanOnly': {'props': soTableElemPropsStructure(dataStyles=resolveDataDS('clanOnly', item[2][1]), dataType=1, rights=['READ', 'EDIT']),
                               'data': {'text': u'',
                                        'boolState': item[2][0]}},
                  'itemName': {'props': soTableElemPropsStructure(dataStyles=resolveDataDS('itemName')),
                               'data': {'text': item[3]}},
                  'quantity': {'props': soTableElemPropsStructure(dataStyles=resolveDataDS('quantity', item[4])),
                               'data': {'text': str(item[4])}},
                  'baseCost': {'props': soTableElemPropsStructure(dataStyles=resolveDataDS('baseCost', item[5])),
                               'data': {'text': str(item[5])}},
                  'buyCost': {'props': soTableElemPropsStructure(dataStyles=resolveDataDS('buyCost', item[6][1]), rights=['READ', 'EDIT']),
                              'data': {'text': str(item[6][0])}},
                  'sellClanCost': {'props': soTableElemPropsStructure(dataStyles=resolveDataDS('sellClanCost', item[7][1]), rights=['READ', 'EDIT']),
                                   'data': {'text': str(item[7][0])}},
                  'sellNeutralCost': {'props': soTableElemPropsStructure(dataStyles=resolveDataDS('sellNeutralCost', item[8][1]), rights=['READ', 'EDIT']),
                                      'data': {'text': str(item[8][0])}},
                  'sellFriendlyCost': {'props': soTableElemPropsStructure(dataStyles=resolveDataDS('sellFriendlyCost', item[9][1]), rights=['READ', 'EDIT']),
                                       'data': {'text': str(item[9][0])}},
                  'sellEnemyCost': {'props': soTableElemPropsStructure(dataStyles=resolveDataDS('sellEnemyCost', item[10][1]), rights=['READ', 'EDIT']),
                                    'data': {'text': str(item[10][0])}}}])

            if operation == 'add':
                tbl.addRows(rows)
            elif operation == 'remove':
                rowIndexes = []
                for item in items:
                    rowIdx = tbl.getRowIndexByAttachment(item[0])
                    if rowIdx >= 0:
                        rowIndexes.append(rowIdx)

                if rowIndexes:
                    tbl.removeRows(rowIndexes)
            elif operation == 'update':
                tbl.delayRender(len(rows) - 1)
                for row in rows:
                    rowIdx = tbl.getRowIndexByAttachment(row[0][2])
                    if rowIdx >= 0:
                        tbl.rewriteRow(rowIdx, row)

            elif operation == 'clear':
                tbl.clearRowRange(2)
                tbl.delayRender(4)
                tbl.alterElem('buyCost', globalPricesIndex, soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']), {'text': u''})
                tbl.alterElem('sellClanCost', globalPricesIndex, soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']), {'text': u''})
                tbl.alterElem('sellNeutralCost', globalPricesIndex, soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']), {'text': u''})
                tbl.alterElem('sellFriendlyCost', globalPricesIndex, soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']), {'text': u''})
                tbl.alterElem('sellEnemyCost', globalPricesIndex, soTableElemPropsStructure(dataStyles=self.clanTrade_captionDS, rights=['READ', 'EDIT']), {'text': u''})
        return

    def _timeToString(self, secs):
        hours = floor(secs / 3600.0)
        minutes = floor((secs - hours * 3600.0) / 60.0)
        seconds = secs - (hours * 3600.0 + minutes * 60.0)
        outH = str(int(hours)) if hours > 9 else u'0' + str(int(hours))
        outM = str(int(minutes)) if minutes > 9 else u'0' + str(int(minutes))
        outS = str(int(seconds)) if seconds > 9 else u'0' + str(int(seconds))
        return u'' + outH + u':' + outM + u':' + outS

    def _updateBases(self):
        bases = None
        staffList = None
        staffTypes = None
        staffDsc = None
        pvpTF = None
        timeLeft = None
        expire = None
        cost = None
        icon = None
        if BWPersonality.GUICore.clanDataSection.has_key('bases'):
            bases = BWPersonality.GUICore.clanDataSection['bases']
        if BWPersonality.GUICore.clanDataSection.has_key('staffList'):
            staffList = BWPersonality.GUICore.clanDataSection['staffList']
        if BWPersonality.GUICore.clanDataSection.has_key('staffTypes'):
            staffTypes = BWPersonality.GUICore.clanDataSection['staffTypes']
        if BWPersonality.GUICore.clanDataSection.has_key('timeTillNextPvP'):
            timeLeft = BWPersonality.GUICore.clanDataSection['timeTillNextPvP']
        if BWPersonality.GUICore.clanDataSection.has_key('PvPTimeframe'):
            pvpTF = BWPersonality.GUICore.clanDataSection['PvPTimeframe']
        if BWPersonality.GUICore.clanDataSection.has_key('staffDescription'):
            staffDsc = BWPersonality.GUICore.clanDataSection['staffDescription']
        if BWPersonality.GUICore.clanDataSection.has_key('shiftCost'):
            cost = BWPersonality.GUICore.clanDataSection['shiftCost']
        if BWPersonality.GUICore.clanDataSection.has_key('staffExpire'):
            expire = BWPersonality.GUICore.clanDataSection['staffExpire']
        if BWPersonality.GUICore.clanDataSection.has_key('staffIcon'):
            icon = BWPersonality.GUICore.clanDataSection['staffIcon']
        if bases is not None:
            self.basesWnd.baseList.script.clear()
            self.basesWnd.baseList.script.addElements(bases)
            if len(bases) > 0:
                self.baseMgrFillLevel.append('baseList')
            elif self.baseMgrFillLevel.__contains__('baseList'):
                self.baseMgrFillLevel.remove('baseList')
        if staffList is not None:
            self.basesWnd.hireList.script.clear()
            for staff in staffList:
                self.basesWnd.hireList.script.addElement(staff)

            if len(staffList) > 0:
                self.baseMgrFillLevel.append('staffTypes')
            elif self.baseMgrFillLevel.__contains__('staffTypes'):
                self.baseMgrFillLevel.remove('staffTypes')
        if staffTypes is not None:
            self.basesWnd.nameList.script.clear()
            for staffType in staffTypes:
                self.basesWnd.nameList.script.addElement(staffType)

            if len(staffTypes) > 0:
                self.baseMgrFillLevel.append('staffNames')
            elif self.baseMgrFillLevel.__contains__('staffNames'):
                self.baseMgrFillLevel.remove('staffNames')
        if timeLeft is not None:
            oldTime = self.pvpTimeLeft
            self.pvpTimeLeft = timeLeft
            if not oldTime:
                self.pvpTimeLeftChecker().run()
        if pvpTF is not None:
            self.basesWnd.timeFrameLbl.text = lc('soClanScreen.soGUI.STRING_1924_37') + pvpTF
        if staffDsc is not None:
            self.basesWnd.staffDescription.script.setText(staffDsc)
        if expire is not None:
            oldTime = self.shiftTimeLeft
            self.shiftTimeLeft = expire
            if not oldTime:
                self.shiftTimeChecker().run()
        if cost is not None:
            self.basesWnd.shiftCost.text = lc('soClanScreen.soGUI.STRING_1936_34') + str(cost)
        if icon is not None:
            self.basesWnd.icon.textureName = icon
        self._applyBaseFillLevel()
        return

    def _updateRightsEditor(self):
        if BWPersonality.GUICore.clanDataSection.has_key('rights'):
            rights = BWPersonality.GUICore.clanDataSection['rights']
            for rightCmp in self.rightsCheckBoxes:
                self.component.generalWnd.rightsWnd.rightsFrame.delChild(rightCmp)
                rightCmp = None

            for i, right in enumerate(rights):
                cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=right[0]))
                cmp = cb.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.position = (18, 12 + i * 25, 0.4)
                self.component.generalWnd.rightsWnd.rightsFrame.addChild(cmp, 'right' + str(right[1]))
                cb.onStateChange = partial(self.rightChecked, right[1])
                cb.onBound()
                self.rightsCheckBoxes.append(cmp)
                if not right[2]:
                    cb.disable()
                if right[3]:
                    cb.setActive()

        if BWPersonality.GUICore.clanDataSection.has_key('ranks'):
            ranks = BWPersonality.GUICore.clanDataSection['ranks']
            self.component.generalWnd.rightsWnd.ranks.script.clear()
            for rank in ranks:
                self.component.generalWnd.rightsWnd.ranks.script.addElement(rank)

        return

    def setMembers(self, data):
        tbl = self.component.membersWnd.membersTable.script
        for mEntry in data:
            rowIndex = tbl.getRowIndexByValue({'text': mEntry}, 'name')
            rank = data[mEntry][1]
            status = data[mEntry][2]
            name = mEntry
            rowData = [(25, 'MIDDLE'), {'name': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_dataDS),
                       'data': {'text': name}},
              'rank': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_dataDS),
                       'data': {'text': rank}},
              'status': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_dataDS),
                         'data': {'text': status}}}]
            tbl.rewriteRow(rowIndex, rowData)

    def addMembers(self, data):
        rows = []
        tbl = self.component.membersWnd.membersTable.script
        for mEntry in data:
            rank = data[mEntry][1]
            status = data[mEntry][2]
            name = mEntry
            rowData = [(25, 'MIDDLE'), {'name': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_dataDS),
                       'data': {'text': name}},
              'rank': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_dataDS),
                       'data': {'text': rank}},
              'status': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_dataDS),
                         'data': {'text': status}}}]
            rows.append(rowData)

        if rows:
            tbl.addRows(rows)

    def delMembers(self, data):
        rows = []
        tbl = self.component.membersWnd.membersTable.script
        for mName in data:
            rowIndex = tbl.getRowIndexByValue({'text': mName}, 'name')
            rows.append(rowIndex)

        if rows:
            tbl.removeRows(rows)

    def sortCaptionClick(self, col_name):
        rows = []
        cols = {'name': 0,
         'rank': 1,
         'status': 2}
        tbl = self.component.membersWnd.membersTable.script
        tbl.clearRowRange(1)

        def sortOfCaption(memb):
            return memb[cols[col_name]]

        if self.sortType[cols[col_name]] == 0:
            self.members.sort(key=sortOfCaption)
            self.sortType[cols[col_name]] = 1
        else:
            self.members.sort(key=sortOfCaption, reverse=True)
            self.sortType[cols[col_name]] = 0
        for member in self.members:
            rowData = [(25, 'MIDDLE'), {'name': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_dataDS),
                       'data': {'text': member[0]}},
              'rank': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_dataDS),
                       'data': {'text': member[1]}},
              'status': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_dataDS),
                         'data': {'text': member[2]}}}]
            rows.append(rowData)

        tbl.addRows(rows)

    def update(self):
        if BWPersonality.GUICore.clanTradeDataSection is not None:
            self._updateClanTrade()
        if BWPersonality.GUICore.clanDataSection is None:
            return
        else:
            rows = []
            if BWPersonality.GUICore.clanDataSection.has_key('members'):
                self.membersData = BWPersonality.GUICore.clanDataSection['members']
                tbl = self.component.membersWnd.membersTable.script
                tbl.clearRowRange(1)
                self.members = []
                for member in BWPersonality.GUICore.clanDataSection['members']:
                    rank = BWPersonality.GUICore.clanDataSection['members'][member][1]
                    status = BWPersonality.GUICore.clanDataSection['members'][member][2]
                    name = member
                    self.members.append((name, rank, status))
                    rowData = [(25, 'MIDDLE'), {'name': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_dataDS),
                               'data': {'text': name}},
                      'rank': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_dataDS),
                               'data': {'text': rank}},
                      'status': {'props': soTableElemPropsStructure(dataStyles=self.memberTable_dataDS),
                                 'data': {'text': status}}}]
                    rows.append(rowData)

                tbl.addRows(rows)
            if BWPersonality.GUICore.clanDataSection.has_key('cName'):
                self.component.wndFrame.nameLabel.text = lc('PlayerAvatarForSoClanScreen.client.CLAN_NAME_CAPTION').format(BWPersonality.GUICore.clanDataSection['cName'])
            data = BWPersonality.GUICore.clanDataSection
            if data.has_key('rights'):
                self._updateRightsEditor()
            if BWPersonality.GUICore.clanDataSection.has_key('bases') or BWPersonality.GUICore.clanDataSection.has_key('staffList') or BWPersonality.GUICore.clanDataSection.has_key('staffTypes') or BWPersonality.GUICore.clanDataSection.has_key('timeTillNextPvP') or BWPersonality.GUICore.clanDataSection.has_key('PvPTimeframe') or BWPersonality.GUICore.clanDataSection.has_key('staffDescription'):
                self._updateBases()
            return

    def rightChecked(self, rightID):
        check = None
        if hasattr(self.component.generalWnd.rightsWnd.rightsFrame, 'right' + str(rightID)):
            cmp = getattr(self.component.generalWnd.rightsWnd.rightsFrame, 'right' + str(rightID))
            check = cmp.script.isChecked()
        if check is None:
            print 'ERROR: ClanRights Editor wasnt initialised properly: missing checkbox'
            return
        else:
            sel = self.component.generalWnd.rightsWnd.ranks.script.getSelection()
            if len(sel) > 0:
                sel = sel[0]
            else:
                sel = None
            BWPersonality.GUICore.clanEvent(self.EVENT_EDITRIGHT, (sel, rightID, check))
            return

    def onRankSelect(self):
        if not hasattr(self.component.generalWnd.rightsWnd, 'ranks'):
            return
        sel = self.component.generalWnd.rightsWnd.ranks.script.getSelection()
        if len(sel) > 0:
            sel = sel[0]
        else:
            for rightCmp in self.rightsCheckBoxes:
                rightCmp.script.disable()
                rightCmp.script.setInactive()

            return
        BWPersonality.GUICore.clanEvent(self.EVENT_RANKSELECT, sel)

    def applyRights(self):
        rights = BWPersonality.GUICore.clanRights
        if Clan.CLANRIGHT_WARMASTER not in rights:
            pass
        if Clan.CLANRIGHT_PROMOTE not in rights:
            pass
        if Clan.CLANRIGHT_INVITE not in rights:
            pass
        if Clan.CLANRIGHT_DAILYQUOTES not in rights:
            pass
        if Clan.CLANRIGHT_CLANKICK not in rights:
            pass

    def _applyBaseFillLevel(self):
        self.basesWnd.baseList.visible = False
        self.basesWnd.hireList.visible = False
        self.basesWnd.nameList.visible = False
        self.basesWnd.pvpTimeFrame.visible = False
        self.basesWnd.timeFrameLbl.visible = False
        self.basesWnd.timeleftLbl.visible = False
        self.basesWnd.personelStatusFrame.visible = False
        self.basesWnd.personelMgrFrame.visible = False
        self.basesWnd.staffDescription.visible = False
        self.basesWnd.shiftCost.visible = False
        self.basesWnd.expireTime.visible = False
        self.basesWnd.changePvPTime.visible = False
        self.basesWnd.hireBtn.visible = False
        self.basesWnd.fireBtn.visible = False
        self.basesWnd.icon.visible = False
        if 'baseList' in self.baseMgrFillLevel:
            self.basesWnd.baseList.visible = True
            self.basesWnd.timeFrameLbl.visible = True
            self.basesWnd.timeleftLbl.visible = True
            self.basesWnd.changePvPTime.visible = True
            self.basesWnd.pvpTimeFrame.visible = True
        if 'staffTypes' in self.baseMgrFillLevel:
            self.basesWnd.hireList.visible = True
        if 'staffNames' in self.baseMgrFillLevel:
            self.basesWnd.personelStatusFrame.visible = True
            self.basesWnd.personelMgrFrame.visible = True
            self.basesWnd.nameList.visible = True
            self.basesWnd.staffDescription.visible = True
            self.basesWnd.shiftCost.visible = True
            self.basesWnd.expireTime.visible = True
            self.basesWnd.changePvPTime.visible = True
            self.basesWnd.hireBtn.visible = True
            self.basesWnd.fireBtn.visible = True
            self.basesWnd.icon.visible = True

    def onBaseMgr(self, event):
        data = None
        if event[0] == 'baseList':
            data = self.basesWnd.baseList.script.getSelection()[1]
            BWPersonality.GUICore.clanEvent(self.EVENT_BASESELECT, data)
        if event[0] == 'staffType':
            data = self.basesWnd.hireList.script.getSelection()[1]
            BWPersonality.GUICore.clanEvent(self.EVENT_STAFFTYPESELECT, data)
        if event[0] == 'staffName':
            data = self.basesWnd.nameList.script.getSelection()[1]
            BWPersonality.GUICore.clanEvent(self.EVENT_STAFFNAMESELECT, data)
        if event[0] == 'timeChange':
            data = self.basesWnd.baseList.script.getSelection()[1]
            BWPersonality.GUICore.clanEvent(self.EVENT_CHANGEPVPTIME, data)
        if event[0] == 'fire':
            data = (self.basesWnd.hireList.script.getSelection()[1], self.basesWnd.nameList.script.getSelection()[1])
            BWPersonality.GUICore.clanEvent(self.EVENT_FIREPERSONEL, data)
        if event[0] == 'hire':
            data = (self.basesWnd.hireList.script.getSelection()[1], self.basesWnd.nameList.script.getSelection()[1])
            BWPersonality.GUICore.clanEvent(self.EVENT_HIREPERSONEL, data)
        return

    def onClanTradeMgr(self, event, data):
        sendData = None
        if event == 'BASELIST':
            sendData = self.component.generalWnd.clanTraderWnd.baseList.script.getSelection()[1]
            BWPersonality.GUICore.clanTraderEvent(self.EVENT_CLANTRADER_SELECT, sendData)
        if event == 'APPLY':
            BWPersonality.GUICore.clanTraderEvent(self.EVENT_CLANTRADER_APPLY, sendData)
        if event == 'CANCEL':
            BWPersonality.GUICore.clanTraderEvent(self.EVENT_CLANTRADER_CANCEL, sendData)
        if event == 'TEXTINPUT':
            sendData = data
            BWPersonality.GUICore.clanTraderEvent(self.EVENT_CLANTRADER_USERINPUT, sendData)
        if event == 'CHECKBOX':
            sendData = data
            BWPersonality.GUICore.clanTraderEvent(self.EVENT_CLANTRADER_USERINPUT, sendData)
        return

    @PyGUIEvent('generalWnd.clanTraderWnd.priceTable', 'onElementEvent')
    def onClanTradeElem(self, col, row, event, data):
        tbl = self.component.generalWnd.clanTraderWnd.priceTable.script

    @PyGUIEvent('generalWnd.clanTraderWnd.priceTable', 'onEditEvent')
    def onClanTradeEdit(self, col, row, event, data):
        tbl = self.component.generalWnd.clanTraderWnd.priceTable.script
        itemId = tbl.getRowAttachmentByIndex(row)
        sendData = (col, itemId, data)
        self.onClanTradeMgr(event, sendData)

    @PyGUIEvent('generalWnd.clanTraderWnd.applyBtn', 'onClick')
    def onClanTradeApplyBtn(self):
        self.onClanTradeMgr('APPLY', None)
        return

    @PyGUIEvent('generalWnd.clanTraderWnd.cancelBtn', 'onClick')
    def onClanTradeCancelBtn(self):
        self.onClanTradeMgr('CANCEL', None)
        return

    @PyGUIEvent('membersBtn', 'onClick')
    def onMembersClick(self):
        self.switchToMode(self.MODE_MEMBERS)

    @PyGUIEvent('financeBtn', 'onClick')
    def onFinanceClick(self):
        self.switchToMode(self.MODE_FINANCE)

    @PyGUIEvent('basesBtn', 'onClick')
    def onBasesClick(self):
        self.switchToMode(self.MODE_BASES)

    def onRightsBtnClick(self):
        self.membersWnd.visible = False
        self.component.membersBtn.visible = 0
        self.component.financeBtn.visible = 0
        self.component.basesBtn.visible = 0
        self.component.generalWnd.rightsWnd.visible = 1
        self.component.generalWnd.visible = True

    def onInviteClanClick(self):

        def onClanIntive(text):
            BigWorld.player().inviteFriendToClan(text.encode('utf-8'))

        gui_jokes.inputBox(lc('GUI.ClanGUI.INVITE_TO_CLAN_CAPTION'), lc('GUI.ClanGUI.INVITE_TO_CLAN_TEXT'), onClanIntive)

    @PyGUIEvent('generalWnd.clantradeBtn', 'onClick')
    def onClantradeBtnClick(self):
        self.component.generalWnd.clanTraderWnd.visible = True

    @PyGUIEvent('generalWnd.rightsWnd.btnUp', 'onClick')
    def onUpBtn(self):
        sel = self.component.generalWnd.rightsWnd.ranks.script.getSelection()
        if len(sel) > 0:
            sel = sel[0]
            BWPersonality.GUICore.clanEvent(self.EVENT_MOVERANK, (sel, 'up'))

    @PyGUIEvent('generalWnd.rightsWnd.btnDown', 'onClick')
    def onDownBtn(self):
        sel = self.component.generalWnd.rightsWnd.ranks.script.getSelection()
        if len(sel) > 0:
            sel = sel[0]
            BWPersonality.GUICore.clanEvent(self.EVENT_MOVERANK, (sel, 'down'))

    @PyGUIEvent('generalWnd.rightsWnd.btnAdd', 'onClick')
    def onAddBtn(self):
        BWPersonality.GUICore.clanEvent(self.EVENT_ADDRANK, None)
        return

    @PyGUIEvent('generalWnd.rightsWnd.btnDelete', 'onClick')
    def onDeleteBtn(self):
        sel = self.component.generalWnd.rightsWnd.ranks.script.getSelection()
        if len(sel) > 0:
            sel = sel[0]
            BWPersonality.GUICore.clanEvent(self.EVENT_DELRANK, sel)

    @PyGUIEvent('generalWnd.rightsWnd.btnEdit', 'onClick')
    def onEditBtn(self):
        sel = self.component.generalWnd.rightsWnd.ranks.script.getSelection()
        if len(sel) > 0:
            sel = sel[0]
            BWPersonality.GUICore.clanEvent(self.EVENT_EDITRANK, sel)

    @PyGUIEvent('membersWnd.membersTable', 'onElementEvent')
    def onMembersElem(self, col, row, event, data):
        tbl = self.component.membersWnd.membersTable.script
        if row == 0:
            self.sortCaptionClick(col)
            return
        if event == 'RIGHTMOUSE':
            tbl.clearSelection()
            rowData = tbl.getRowByIndex(row)
            playerName = rowData['name']['data']['text']
            BWPersonality.GUICore.clanMemberActionsRequest(playerName)
            tbl.selectRow(row)
        elif event == 'LEFTMOUSE':
            tbl.clearSelection()

    @BWMemberCoroutine
    def pvpTimeLeftChecker(self):
        while self.pvpTimeLeft:
            self.pvpTimeLeft -= 1
            if self.pvpTimeLeft < 0:
                self.pvpTimeLeft = 0
            timerText = lc('soClanScreen.soGUI.STRING_2300_15')
            self.basesWnd.timeleftLbl.text = timerText + self._timeToString(self.pvpTimeLeft)
            yield BWWaitForPeriod(1.0)

        self.basesWnd.timeleftLbl.visible = False

    @BWMemberCoroutine
    def shiftTimeChecker(self):
        while self.shiftTimeLeft:
            self.shiftTimeLeft -= 1
            if self.shiftTimeLeft < 0:
                self.shiftTimeLeft = 0
            timerText = lc('soClanScreen.soGUI.STRING_2312_15')
            self.basesWnd.expireTime.text = timerText + self._timeToString(self.shiftTimeLeft)
            yield BWWaitForPeriod(1.0)

        self.basesWnd.expireTime.text = lc('soClanScreen.soGUI.STRING_2315_34')

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()