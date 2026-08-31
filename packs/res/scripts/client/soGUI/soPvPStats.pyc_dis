# Embedded file name: scripts/client/soGUI/soPvPStats.py
from Localization import lc
import BigWorld
import GUI
import BWPersonality
import soGUI
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI.PyGUIBase import PyGUIBase

class soPvPStats(PyGUIBase):
    factoryString = 'soGUI.soPvPStats'
    MODE_1T = 0
    MODE_2T = 1
    MODE_MT = 2
    STATUS_FIRST = 0
    STATUS_PLAYER = 1
    STATUS_PLAYERTEAM = 2

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.playerTeam = []
        self.enemy = []
        self.hideThird = True
        self.battleName = u''
        self.playerTeamName = u''
        self.enemyName = u''
        self.ptScore = (u'0', u'0', u'0')
        self.enemyScore = (u'0', u'0', u'0')
        self.oneTeamStatusCmps = []
        self.twoTeamsStatusCmps = []
        self.multiTeamsStatusCmps = []
        self.guiMode = self.MODE_1T
        self.setupRoot()
        self.setupTwoTeamsWnd()
        self.setupOneTeamWnd()
        self.setupMultiTeamsWnd()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 721
        cmp.height = 510
        cmp.textureName = ''
        cmp.visible = False
        cmp.position = (0.0, 0.0, 0.1)

    def setupTwoTeamsWnd(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 721
        cmp.height = 510
        cmp.visible = False
        cmp.position = (0, 0, 0.1)
        cmp.textureName = ''
        self.component.addChild(cmp, 'twoTeamsWnd')
        cmp = GUI.Frame2('soGUI/maps/Controls/pvpStats/frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 721
        cmp.height = 510
        cmp.position = (0, 0, 1.0)
        self.component.twoTeamsWnd.addChild(cmp, 'frame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_default_header.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.component.width / 2.0, 16, 0.9)
        cmp.text = u'PLACE_HOLDER'
        self.component.twoTeamsWnd.addChild(cmp, 'battleName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (181, 45, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_105_13')
        self.component.twoTeamsWnd.addChild(cmp, 'teamName1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (540, 45, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_115_13')
        self.component.twoTeamsWnd.addChild(cmp, 'teamName2')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (90, 1, 1, 51)
        cmp.materialFX = 'BLEND'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 358
        cmp.height = 390
        cmp.position = (2, 89, 0.95)
        self.component.twoTeamsWnd.addChild(cmp, 'teamColor1')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (2, 40, 125, 51)
        cmp.materialFX = 'BLEND'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 358
        cmp.height = 390
        cmp.position = (361, 89, 0.95)
        self.component.twoTeamsWnd.addChild(cmp, 'teamColor2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (15, 75, 0.9)
        cmp.text = u'#'
        self.component.twoTeamsWnd.addChild(cmp, 'pNumber1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (108, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_169_13')
        self.component.twoTeamsWnd.addChild(cmp, 'pName1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (250, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_179_13')
        cmp.visible = False
        self.component.twoTeamsWnd.addChild(cmp, 'pPoints1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (292, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_190_13')
        self.component.twoTeamsWnd.addChild(cmp, 'pKills1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (327, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_200_13')
        self.component.twoTeamsWnd.addChild(cmp, 'pDeaths1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (260, 493, 0.9)
        self.component.twoTeamsWnd.addChild(cmp, 'pTeamPoints1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (300, 493, 0.9)
        self.component.twoTeamsWnd.addChild(cmp, 'pTeamKills1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (340, 493, 0.9)
        self.component.twoTeamsWnd.addChild(cmp, 'pTeamDeaths1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (373, 75, 0.9)
        cmp.text = u'#'
        self.component.twoTeamsWnd.addChild(cmp, 'pNumber2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (465, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_249_13')
        self.component.twoTeamsWnd.addChild(cmp, 'pName2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (611, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_259_13')
        cmp.visible = False
        self.component.twoTeamsWnd.addChild(cmp, 'pPoints2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (650, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_270_13')
        self.component.twoTeamsWnd.addChild(cmp, 'pKills2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (689, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_280_13')
        self.component.twoTeamsWnd.addChild(cmp, 'pDeaths2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (620, 493, 0.9)
        self.component.twoTeamsWnd.addChild(cmp, 'pTeamPoints2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (660, 493, 0.9)
        self.component.twoTeamsWnd.addChild(cmp, 'pTeamKills2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (700, 493, 0.9)
        self.component.twoTeamsWnd.addChild(cmp, 'pTeamDeaths2')
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 717
        cmp.height = 1
        cmp.position = (2, 29, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 717
        cmp.height = 1
        cmp.position = (2, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 717
        cmp.height = 1
        cmp.position = (2, 88, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 717
        cmp.height = 1
        cmp.position = (2, 479, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (35, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.visible = False
        cmp.position = (240, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp, 'thirdLine1')
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (280, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (320, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 479
        cmp.position = (360, 29, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (394, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (599, 59, 0.9)
        cmp.visible = False
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp, 'thirdLine2')
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (639, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (679, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.twoTeamsWnd.addChild(cmp)
        for i in xrange(26):
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (16, 96 + i * 15, 0.8)
            cmp.text = str(i)
            self.component.twoTeamsWnd.addChild(cmp, 'pNumber1x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (36, 89 + i * 15, 0.8)
            cmp.text = lc('soPvPStats.soGUI.STRING_556_14') + str(i)
            self.component.twoTeamsWnd.addChild(cmp, 'pName1x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (260, 96 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.twoTeamsWnd.addChild(cmp, 'pPoints1x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (300, 96 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.twoTeamsWnd.addChild(cmp, 'pKills1x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (340, 96 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.twoTeamsWnd.addChild(cmp, 'pDeaths1x' + str(i))

        for i in xrange(26):
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (375, 96 + i * 15, 0.8)
            cmp.text = str(i)
            self.component.twoTeamsWnd.addChild(cmp, 'pNumber2x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (394, 89 + i * 15, 0.8)
            cmp.text = lc('soPvPStats.soGUI.STRING_616_14') + str(i)
            self.component.twoTeamsWnd.addChild(cmp, 'pName2x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (620, 96 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.twoTeamsWnd.addChild(cmp, 'pPoints2x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (660, 96 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.twoTeamsWnd.addChild(cmp, 'pKills2x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (700, 96 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.twoTeamsWnd.addChild(cmp, 'pDeaths2x' + str(i))

    def setupOneTeamWnd(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 539
        cmp.height = 481
        cmp.position = (0.0, 0.0, 0.1)
        cmp.visible = False
        cmp.textureName = ''
        self.component.addChild(cmp, 'oneTeamWnd')
        cmp = GUI.Frame2('soGUI/maps/Controls/pvpStats/frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 1.0)
        self.component.oneTeamWnd.addChild(cmp, 'frame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_default_header.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.component.oneTeamWnd.width / 2.0, 16, 0.9)
        cmp.text = u'PLACE_HOLDER'
        self.component.oneTeamWnd.addChild(cmp, 'battleName')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (60, 90, 1, 51)
        cmp.materialFX = 'BLEND'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 535
        cmp.height = 397
        cmp.position = (2, 59, 0.95)
        self.component.oneTeamWnd.addChild(cmp, 'teamColor')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (18, 45, 0.9)
        cmp.text = u'#'
        self.component.oneTeamWnd.addChild(cmp, 'pNumber')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (126, 37, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_725_13')
        self.component.oneTeamWnd.addChild(cmp, 'pName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (437, 45, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_735_13')
        cmp.visible = False
        self.component.oneTeamWnd.addChild(cmp, 'pPoints')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (477, 45, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_746_13')
        self.component.oneTeamWnd.addChild(cmp, 'pKills')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (517, 45, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_756_13')
        self.component.oneTeamWnd.addChild(cmp, 'pDeaths')
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 535
        cmp.height = 1
        cmp.position = (2, 29, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.oneTeamWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 535
        cmp.height = 1
        cmp.position = (2, 58, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.oneTeamWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 535
        cmp.height = 1
        cmp.position = (2, 456, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.oneTeamWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 428
        cmp.visible = False
        cmp.position = (417, 29, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.oneTeamWnd.addChild(cmp, 'thirdLine')
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 428
        cmp.position = (34, 29, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.oneTeamWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 428
        cmp.position = (457, 29, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.oneTeamWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 428
        cmp.position = (497, 29, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.oneTeamWnd.addChild(cmp)
        for i in xrange(26):
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (18, 70 + i * 15, 0.8)
            cmp.text = str(i)
            self.component.oneTeamWnd.addChild(cmp, 'pNumberx' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (35, 62 + i * 15, 0.8)
            cmp.text = lc('soPvPStats.soGUI.STRING_900_14') + str(i)
            self.component.oneTeamWnd.addChild(cmp, 'pNamex' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (437, 70 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.oneTeamWnd.addChild(cmp, 'pPointsx' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (477, 70 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.oneTeamWnd.addChild(cmp, 'pKillsx' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (517, 70 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.oneTeamWnd.addChild(cmp, 'pDeathsx' + str(i))

    def setupMultiTeamsWnd(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 721
        cmp.height = 510
        cmp.visible = False
        cmp.position = (0, 0, 0.1)
        cmp.textureName = ''
        self.component.addChild(cmp, 'multiTeamsWnd')
        cmp = GUI.Frame2('soGUI/maps/Controls/pvpStats/frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 721
        cmp.height = 510
        cmp.position = (0, 0, 1.0)
        self.component.multiTeamsWnd.addChild(cmp, 'frame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_default_header.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.component.width / 2.0, 16, 0.9)
        cmp.text = u'PLACE_HOLDER'
        self.component.multiTeamsWnd.addChild(cmp, 'battleName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (181, 45, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_981_13')
        self.component.multiTeamsWnd.addChild(cmp, 'teamName1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (540, 45, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_991_13')
        self.component.multiTeamsWnd.addChild(cmp, 'teamName2')
        cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (60, 90, 1, 51)
        cmp.materialFX = 'BLEND'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 358
        cmp.height = 390
        cmp.position = (2, 89, 0.95)
        self.component.multiTeamsWnd.addChild(cmp, 'teamColor1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (15, 75, 0.9)
        cmp.text = u'#'
        self.component.multiTeamsWnd.addChild(cmp, 'pNumber1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (108, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_1030_13')
        self.component.multiTeamsWnd.addChild(cmp, 'pName1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (250, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_1040_13')
        cmp.visible = False
        self.component.multiTeamsWnd.addChild(cmp, 'pPoints1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (292, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_1051_13')
        self.component.multiTeamsWnd.addChild(cmp, 'pKills1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (327, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_1061_13')
        self.component.multiTeamsWnd.addChild(cmp, 'pDeaths1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (260, 493, 0.9)
        self.component.multiTeamsWnd.addChild(cmp, 'pTeamPoints1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (300, 493, 0.9)
        self.component.multiTeamsWnd.addChild(cmp, 'pTeamKills1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (340, 493, 0.9)
        self.component.multiTeamsWnd.addChild(cmp, 'pTeamDeaths1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (373, 75, 0.9)
        cmp.text = u'#'
        self.component.multiTeamsWnd.addChild(cmp, 'pNumber2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (465, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_1110_13')
        self.component.multiTeamsWnd.addChild(cmp, 'pName2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (611, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_1120_13')
        cmp.visible = False
        self.component.multiTeamsWnd.addChild(cmp, 'pPoints2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (650, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_1131_13')
        self.component.multiTeamsWnd.addChild(cmp, 'pKills2')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (689, 75, 0.9)
        cmp.text = lc('soPvPStats.soGUI.STRING_1141_13')
        self.component.multiTeamsWnd.addChild(cmp, 'pDeaths2')
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 717
        cmp.height = 1
        cmp.position = (2, 29, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 717
        cmp.height = 1
        cmp.position = (2, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 717
        cmp.height = 1
        cmp.position = (2, 88, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.pixelSnap = False
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.tiled = True
        cmp.tileHeight = 1
        cmp.tileWidth = 1
        cmp.width = 717
        cmp.height = 1
        cmp.position = (2, 479, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (35, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.visible = False
        cmp.position = (240, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp, 'thirdLine1')
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (280, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (320, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 479
        cmp.position = (360, 29, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (394, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (599, 59, 0.9)
        cmp.visible = False
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp, 'thirdLine2')
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (639, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp)
        cmp = GUI.Simple('soGUI/maps/Controls/pvpStats/del.tga')
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
        cmp.height = 420
        cmp.position = (679, 59, 0.9)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        self.component.multiTeamsWnd.addChild(cmp)
        for i in xrange(26):
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (16, 96 + i * 15, 0.8)
            cmp.text = str(i)
            self.component.multiTeamsWnd.addChild(cmp, 'pNumber1x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (36, 89 + i * 15, 0.8)
            cmp.text = lc('soPvPStats.soGUI.STRING_1390_14') + str(i)
            self.component.multiTeamsWnd.addChild(cmp, 'pName1x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (260, 96 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.multiTeamsWnd.addChild(cmp, 'pPoints1x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (300, 96 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.multiTeamsWnd.addChild(cmp, 'pKills1x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (340, 96 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.multiTeamsWnd.addChild(cmp, 'pDeaths1x' + str(i))

        for i in xrange(26):
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (375, 96 + i * 15, 0.8)
            cmp.text = str(i)
            self.component.multiTeamsWnd.addChild(cmp, 'pNumber2x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (394, 89 + i * 15, 0.8)
            cmp.text = lc('soPvPStats.soGUI.STRING_1450_14') + str(i)
            self.component.multiTeamsWnd.addChild(cmp, 'pName2x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (620, 96 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.multiTeamsWnd.addChild(cmp, 'pPoints2x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (660, 96 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.multiTeamsWnd.addChild(cmp, 'pKills2x' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (700, 96 + i * 15, 0.8)
            cmp.text = u'100'
            self.component.multiTeamsWnd.addChild(cmp, 'pDeaths2x' + str(i))

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'pvpStats')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False

    def _attachStatus(self, index, status, mode, isEnemy = False):
        if status == self.STATUS_PLAYER:
            cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'CENTER'
            cmp.colour = (85, 85, 85, 102)
            cmp.materialFX = 'BLEND'
            cmp.tiled = True
            cmp.tileHeight = 1
            cmp.tileWidth = 1
            cmp.height = 15
            cmp.position = (2, 70 + index * 15, 0.94)
            if mode == self.MODE_1T:
                cmp.width = 535
                self.component.oneTeamWnd.addChild(cmp, 'status_' + str(status) + '_' + str(index))
                self.oneTeamStatusCmps.append(cmp)
        if status == self.STATUS_FIRST:
            cmp = GUI.Simple('soGUI/maps/Colours/white.tga')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'CENTER'
            cmp.colour = (85, 85, 85, 102)
            cmp.materialFX = 'BLEND'
            cmp.tiled = True
            cmp.tileHeight = 1
            cmp.tileWidth = 1
            cmp.height = 15
            cmp.position = (2, 70 + index * 15, 0.94)
            if mode == self.MODE_1T:
                cmp.width = 535
                self.component.oneTeamWnd.addChild(cmp, 'status_' + str(status) + '_' + str(index))
                self.oneTeamStatusCmps.append(cmp)

    def _removeStatusCmps(self):
        if self.guiMode == self.MODE_1T:
            for cmp in self.oneTeamStatusCmps:
                self.component.oneTeamWnd.delChild(cmp)
                cmp = None

        elif self.guiMode == self.MODE_2T:
            for cmp in self.twoTeamsStatusCmps:
                self.component.twoTeamsWnd.delChild(cmp)
                cmp = None

        elif self.guiMode == self.MODE_MT:
            for cmp in self.multiTeamsStatusCmps:
                self.component.multiTeamsWnd.delChild(cmp)
                cmp = None

        return

    def _updateMode(self):
        if self.guiMode == self.MODE_1T:
            self.component.twoTeamsWnd.visible = False
            self.component.multiTeamsWnd.visible = False
            self.component.oneTeamWnd.visible = True
        elif self.guiMode == self.MODE_2T:
            self.component.twoTeamsWnd.visible = True
            self.component.multiTeamsWnd.visible = False
            self.component.oneTeamWnd.visible = False
        elif self.guiMode == self.MODE_MT:
            self.component.twoTeamsWnd.visible = False
            self.component.oneTeamWnd.visible = False
            self.component.multiTeamsWnd.visible = True

    def _updateThirdCol(self):
        self.component.twoTeamsWnd.thirdLine1.visible = not self.hideThird
        self.component.twoTeamsWnd.thirdLine2.visible = not self.hideThird
        self.component.twoTeamsWnd.pPoints1.visible = not self.hideThird
        self.component.twoTeamsWnd.pPoints2.visible = not self.hideThird
        self.component.twoTeamsWnd.pTeamPoints1.visible = not self.hideThird
        self.component.twoTeamsWnd.pTeamPoints2.visible = not self.hideThird
        self.component.oneTeamWnd.thirdLine.visible = not self.hideThird
        self.component.oneTeamWnd.pPoints.visible = not self.hideThird
        self.component.multiTeamsWnd.thirdLine1.visible = not self.hideThird
        self.component.multiTeamsWnd.thirdLine2.visible = not self.hideThird
        self.component.multiTeamsWnd.pPoints1.visible = not self.hideThird
        self.component.multiTeamsWnd.pPoints2.visible = not self.hideThird
        self.component.multiTeamsWnd.pTeamPoints1.visible = not self.hideThird
        for i in xrange(26):
            cmp = getattr(self.component.twoTeamsWnd, 'pPoints1x' + str(i))
            cmp.visible = not self.hideThird
            cmp = getattr(self.component.twoTeamsWnd, 'pPoints2x' + str(i))
            cmp.visible = not self.hideThird
            cmp = getattr(self.component.oneTeamWnd, 'pPointsx' + str(i))
            cmp.visible = not self.hideThird
            cmp = getattr(self.component.multiTeamsWnd, 'pPoints1x' + str(i))
            cmp.visible = not self.hideThird
            cmp = getattr(self.component.multiTeamsWnd, 'pPoints2x' + str(i))
            cmp.visible = not self.hideThird

    def _updatePlayerTeam(self):
        self._removeStatusCmps()
        for i in xrange(26):
            numberCmp = getattr(self.component.twoTeamsWnd, 'pNumber1x' + str(i))
            nameCmp = getattr(self.component.twoTeamsWnd, 'pName1x' + str(i))
            pointsCmp = getattr(self.component.twoTeamsWnd, 'pPoints1x' + str(i))
            killsCmp = getattr(self.component.twoTeamsWnd, 'pKills1x' + str(i))
            deathsCmp = getattr(self.component.twoTeamsWnd, 'pDeaths1x' + str(i))
            if i < len(self.playerTeam):
                labelColour = (175, 166, 112, 255)
                if self.STATUS_PLAYER in self.playerTeam[i][5]:
                    labelColour = (255, 255, 255, 255)
                if self.playerTeam[i][4] < 0:
                    numberCmp.text = str(i + 1)
                else:
                    numberCmp.text = str(self.playerTeam[i][4])
                numberCmp.colour = labelColour
                nameCmp.colour = labelColour
                killsCmp.colour = labelColour
                deathsCmp.colour = labelColour
                pointsCmp.colour = labelColour
                nameCmp.text = self.playerTeam[i][0]
                pointsCmp.text = self.playerTeam[i][1]
                killsCmp.text = self.playerTeam[i][2]
                deathsCmp.text = self.playerTeam[i][3]
            else:
                numberCmp.text = u''
                nameCmp.text = u''
                pointsCmp.text = u''
                killsCmp.text = u''
                deathsCmp.text = u''
            numberCmp = getattr(self.component.oneTeamWnd, 'pNumberx' + str(i))
            nameCmp = getattr(self.component.oneTeamWnd, 'pNamex' + str(i))
            pointsCmp = getattr(self.component.oneTeamWnd, 'pPointsx' + str(i))
            killsCmp = getattr(self.component.oneTeamWnd, 'pKillsx' + str(i))
            deathsCmp = getattr(self.component.oneTeamWnd, 'pDeathsx' + str(i))
            if i < len(self.playerTeam):
                labelColour = (175, 166, 112, 255)
                if self.STATUS_PLAYER in self.playerTeam[i][5]:
                    labelColour = (255, 255, 255, 255)
                if self.playerTeam[i][4] < 0:
                    numberCmp.text = str(i + 1)
                else:
                    numberCmp.text = str(self.playerTeam[i][4])
                numberCmp.colour = labelColour
                nameCmp.colour = labelColour
                killsCmp.colour = labelColour
                deathsCmp.colour = labelColour
                pointsCmp.colour = labelColour
                nameCmp.text = self.playerTeam[i][0]
                pointsCmp.text = self.playerTeam[i][1]
                killsCmp.text = self.playerTeam[i][2]
                deathsCmp.text = self.playerTeam[i][3]
                for status in self.playerTeam[i][5]:
                    self._attachStatus(i, status, self.MODE_1T)

            else:
                numberCmp.text = u''
                nameCmp.text = u''
                pointsCmp.text = u''
                killsCmp.text = u''
                deathsCmp.text = u''
            numberCmp = getattr(self.component.multiTeamsWnd, 'pNumber1x' + str(i))
            nameCmp = getattr(self.component.multiTeamsWnd, 'pName1x' + str(i))
            pointsCmp = getattr(self.component.multiTeamsWnd, 'pPoints1x' + str(i))
            killsCmp = getattr(self.component.multiTeamsWnd, 'pKills1x' + str(i))
            deathsCmp = getattr(self.component.multiTeamsWnd, 'pDeaths1x' + str(i))
            if i < len(self.playerTeam):
                labelColour = (175, 166, 112, 255)
                if self.STATUS_PLAYER in self.playerTeam[i][5]:
                    labelColour = (255, 255, 255, 255)
                if self.playerTeam[i][4] < 0:
                    numberCmp.text = str(i + 1)
                else:
                    numberCmp.text = str(self.playerTeam[i][4])
                numberCmp.colour = labelColour
                nameCmp.colour = labelColour
                killsCmp.colour = labelColour
                deathsCmp.colour = labelColour
                pointsCmp.colour = labelColour
                nameCmp.text = self.playerTeam[i][0]
                pointsCmp.text = self.playerTeam[i][1]
                killsCmp.text = self.playerTeam[i][2]
                deathsCmp.text = self.playerTeam[i][3]
            else:
                numberCmp.text = u''
                nameCmp.text = u''
                pointsCmp.text = u''
                killsCmp.text = u''
                deathsCmp.text = u''

    def _updateEnemy(self):
        if self.guiMode == self.MODE_1T:
            return
        for i in xrange(26):
            numberCmp = getattr(self.component.twoTeamsWnd, 'pNumber2x' + str(i))
            nameCmp = getattr(self.component.twoTeamsWnd, 'pName2x' + str(i))
            pointsCmp = getattr(self.component.twoTeamsWnd, 'pPoints2x' + str(i))
            killsCmp = getattr(self.component.twoTeamsWnd, 'pKills2x' + str(i))
            deathsCmp = getattr(self.component.twoTeamsWnd, 'pDeaths2x' + str(i))
            if i < len(self.enemy):
                if self.enemy[i][4] < 0:
                    numberCmp.text = str(i + 1)
                else:
                    numberCmp.text = str(self.enemy[i][4])
                nameCmp.text = self.enemy[i][0]
                pointsCmp.text = self.enemy[i][1]
                killsCmp.text = self.enemy[i][2]
                deathsCmp.text = self.enemy[i][3]
            else:
                numberCmp.text = u''
                nameCmp.text = u''
                pointsCmp.text = u''
                killsCmp.text = u''
                deathsCmp.text = u''

        for i in xrange(26):
            numberCmp = getattr(self.component.multiTeamsWnd, 'pNumber2x' + str(i))
            nameCmp = getattr(self.component.multiTeamsWnd, 'pName2x' + str(i))
            pointsCmp = getattr(self.component.multiTeamsWnd, 'pPoints2x' + str(i))
            killsCmp = getattr(self.component.multiTeamsWnd, 'pKills2x' + str(i))
            deathsCmp = getattr(self.component.multiTeamsWnd, 'pDeaths2x' + str(i))
            if i < len(self.enemy):
                if self.enemy[i][4] < 0:
                    numberCmp.text = str(i + 1)
                else:
                    numberCmp.text = str(self.enemy[i][4])
                nameCmp.text = self.enemy[i][0]
                pointsCmp.text = self.enemy[i][1]
                killsCmp.text = self.enemy[i][2]
                deathsCmp.text = self.enemy[i][3]
            else:
                numberCmp.text = u''
                nameCmp.text = u''
                pointsCmp.text = u''
                killsCmp.text = u''
                deathsCmp.text = u''

    def _updateBattleName(self):
        self.component.twoTeamsWnd.battleName.text = self.battleName
        self.component.oneTeamWnd.battleName.text = self.battleName
        self.component.multiTeamsWnd.battleName.text = self.battleName

    def _updatePlayerTeamName(self):
        self.component.twoTeamsWnd.teamName1.text = self.playerTeamName
        self.component.multiTeamsWnd.teamName1.text = self.playerTeamName

    def _updateEnemyName(self):
        self.component.twoTeamsWnd.teamName2.text = self.enemyName
        self.component.multiTeamsWnd.teamName2.text = self.enemyName

    def _updatePlayerTeamScore(self):
        self.component.twoTeamsWnd.pTeamPoints1.text = self.ptScore[0]
        self.component.twoTeamsWnd.pTeamKills1.text = self.ptScore[1]
        self.component.twoTeamsWnd.pTeamDeaths1.text = self.ptScore[2]
        self.component.multiTeamsWnd.pTeamPoints1.text = self.ptScore[0]
        self.component.multiTeamsWnd.pTeamKills1.text = self.ptScore[1]
        self.component.multiTeamsWnd.pTeamDeaths1.text = self.ptScore[2]

    def _updateEnemyScore(self):
        self.component.twoTeamsWnd.pTeamPoints2.text = self.enemyScore[0]
        self.component.twoTeamsWnd.pTeamKills2.text = self.enemyScore[1]
        self.component.twoTeamsWnd.pTeamDeaths2.text = self.enemyScore[2]

    def update(self):
        data = BWPersonality.GUICore.pvpStatsDataSection
        if not data:
            return
        if data.has_key('guiMode'):
            self.guiMode = data['guiMode']
            self._updateMode()
        if data.has_key('hideThird'):
            self.hideThird = data['hideThird']
            self._updateThirdCol()
        if data.has_key('playerTeam'):
            self.playerTeam = data['playerTeam']
            self._updatePlayerTeam()
        if data.has_key('enemy'):
            self.enemy = data['enemy']
            self._updateEnemy()
        if data.has_key('battleName'):
            self.battleName = data['battleName']
            self._updateBattleName()
        if data.has_key('playerTeamName'):
            self.playerTeamName = data['playerTeamName']
            self._updatePlayerTeamName()
        if data.has_key('enemyName'):
            self.enemyName = data['enemyName']
            self._updateEnemyName()
        if data.has_key('playerTeamScore'):
            self.ptScore = data['playerTeamScore']
            self._updatePlayerTeamScore()
        if data.has_key('enemyScore'):
            self.enemyScore = data['enemyScore']
            self._updateEnemyScore()