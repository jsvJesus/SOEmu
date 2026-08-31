# Embedded file name: scripts/client/soGUI/soBulletinBoard.py
import traceback
import BigWorld
import BWPersonality
import GUI
from soGUI.soTextField import soTextField3
from Localization import lc
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soButton import soButton, soButtonWTT
from soGUI.soTextField import soTextField3
import traceback
from Helpers.PyGUI import PyGUIEvent
import soGUI.soShopTabl
import soGUI.soHunterTable

class soBulletinBoard(PyGUIBase):
    factoryString = 'soGUI.soBulletinBoard'
    bdata = ('worldso', 'textNews', 'textQuest', 'sale', 'hunt')
    DISABLED_BUTTON = ()
    bNames = dict([ (x, lc('soBulletinBoard.%s' % x)) for x in bdata ])

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupContent()
        self.curentTab = self.bdata[0]

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        sW, sH = BigWorld.screenSize()
        cmp.width = sW
        cmp.height = sH
        cmp.position = (0, 0, 0.2)

    def setupContent(self):
        sW, sH = BigWorld.screenSize()
        w = sW
        h = sH - 70
        posw = 0
        FRAME_TEXTURE = 'soGUI/maps/Controls/inventory/inventoryFrame2.tga'
        self.frameCmp = GUI.Frame2(FRAME_TEXTURE)
        self.frameCmp.horizontalPositionMode = self.frameCmp.verticalPositionMode = 'PIXEL'
        self.frameCmp.widthMode = self.frameCmp.heightMode = 'PIXEL'
        self.frameCmp.horizontalAnchor = 'LEFT'
        self.frameCmp.verticalAnchor = 'TOP'
        self.frameCmp.visible = True
        self.frameCmp.colour = (255, 255, 255, 255)
        self.frameCmp.materialFX = 'BLEND'
        self.frameCmp.width = sW
        self.frameCmp.height = sH
        self.frameCmp.position = (0, 0, 0.5)
        self.component.addChild(self.frameCmp, 'frame1')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = lc('soBulletinBoard.bulletin')
        cmp.multiline = True
        cmp.position = (sW / 2, 5, 0.5)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_name')
        for txt in ('textNews', 'textQuest'):
            self.createTxtWidget(txt, w, h, posw)

        self.createTabButtons(self.bdata, posw, w)
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
        cmp.position = (w - 5, 5, 0)
        cmp.script.onClick = lambda : BWPersonality.GUICore.showBulletinBoard(False)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = u'@'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 30
        cmp.height = 22
        cmp.position = (sW - 5, sH - 32, 0.0)

        def foo():
            if BWPersonality.GUICore.chatConsole.component.edit.script.active:
                BWPersonality.GUICore.chatConsole.component.edit.script.activate(0)
            else:
                BWPersonality.GUICore.showChatConsole()
                BWPersonality.GUICore.chatConsole.component.edit.script.activate(1)

        cmp.script.onClick = foo
        self.component.addChild(cmp, 'button_chat')
        btn.onBound()
        sale = soGUI.soShopTabl.soShopTabl(GUI.Window(), w - 10, h, posw, 10)
        cmp = sale.component
        cmp.position = (posw, 56, 0)
        self.component.addChild(cmp, 'sale')
        sale.onBound()
        self.csale = sale
        hunters = soGUI.soHunterTable.soHunterTable(GUI.Window(), w - 10, h, posw, 10)
        cmp = hunters.component
        cmp.position = (posw, 56, 0)
        self.component.addChild(cmp, 'hunt')
        hunters.onBound()
        self.chunters = hunters
        cmp = GUI.Simple('soGUI/maps/worldMaps/WorldMapSO.dds')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = w
        cmp.height = h - 30
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 60, 0.0)
        cmp.visible = 1
        cmp.filterType = 'POINT'
        cmp.filterType = 'LINEAR'
        self.component.addChild(cmp, 'worldso')

    def createTabButtons(self, butParam, posw, w):
        bwidth = w / len(butParam)
        for i, name in enumerate(butParam):
            btn = soButton(GUI.Window())
            cmp = btn.component
            btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.label.font = 'ruRU_calibri_default.font'
            cmp.label.text = self.bNames.get(name, '???')
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.width = bwidth
            cmp.height = 25
            cmp.position = (posw + i * bwidth, 30, 0.3)
            cmp.script.onClick = lambda name = name: self.setViewTab(name)
            cmp.script.setDisabledState(name in self.DISABLED_BUTTON)
            self.component.addChild(cmp, 'button_%s' % name)
            btn.onBound()
            cmp = GUI.Simple('textures/default/bright_gray.jpg')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = (255, 255, 255, 120)
            cmp.materialFX = 'BLEND'
            cmp.width = bwidth - 5
            cmp.height = 1
            cmp.position = (posw + i * bwidth + 3, 55, 0.3)
            self.component.addChild(cmp, 'frame_button_%s' % name)

    def createTxtWidget(self, name, w, h, posw):
        sW, sH = BigWorld.screenSize()
        txt = soTextField3(GUI.Window(), width=w, height=h - 20, textWidth=-1, hScroll=False, vScroll=True, hideScroll=1, borderWidth=6, vOffset=3, hOffset=5, textureless=0, autosize=0)
        cmp = txt.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (posw, 51, 0)
        cmp.visible = 0
        txt.onBound()
        self.component.addChild(cmp, name)

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'soBulletinBoard')
        self.component.visible = True
        self.setViewTab('worldso')
        self.component.crossFocus = True
        self.component.moveFocus = True
        self.component.mouseButtonFocus = True
        return

    def hide(self):
        self.component.visible = False
        self.component.moveFocus = False
        self.component.crossFocus = False
        self.component.mouseButtonFocus = False

    def setViewTab(self, tabname):
        print 'setViewTab', tabname
        if tabname not in self.bdata:
            raise ValueError, tabname
        self.curentTab = tabname
        for name in self.bdata:
            cmp_bframe = getattr(self.component, 'frame_button_%s' % name, None)
            cmp_bframe.colour.alpha = 255 if name == tabname else 120
            cmp_text = getattr(self.component, name, None)
            if not cmp_text:
                continue
            cmp_text.visible = name == tabname
            if cmp_text.visible:
                try:
                    cmp_text.script.show()
                except Exception as e:
                    pass

        return

    def handleMouseLeaveEvent(self, cmp):
        return True

    def handleMouseEnterEvent(self, cmp):
        return True

    def handleMouseEvent(self, cmp, event):
        dz = event.dz
        position = event.cursorPosition
        if dz > 0:
            self.scrollCurentTab(1)
            return True
        if dz < 0:
            self.scrollCurentTab(0)
            return True
        return False

    def scrollCurentTab(self, up):
        cmp = getattr(self.component, self.curentTab, None)
        if not cmp:
            return
        else:
            if up:
                cmp.script.scrolledUP()
            else:
                cmp.script.scrolledDOWN()
            return

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.width = sW
        self.component.height = sH
        for name in self.bdata:
            self.component.delChild(name)
            self.component.delChild('button_%s' % name)

        self.component.delChild('frame1')
        self.component.delChild('label_name')
        self.component.delChild('closeBox')
        self.setupContent()

    def update(self):
        if not BWPersonality.GUICore.bulletinBoardDataSection:
            print 'BWPersonality.GUICore.bulletinBoardDataSection  None'
            return
        self.updateTextNews()
        self.updateTextQuest()

    def updateShop(self):
        self.csale.setData(BWPersonality.GUICore.bulletinBoardShopDataSection)

    def updateHunter(self):
        self.chunters.setData(BWPersonality.GUICore.bulletinBoardHunterDataSection)

    def updateTextNews(self):
        if BWPersonality.GUICore.bulletinBoardDataSection.has_key('textNews'):
            self.component.textNews.script.setText(BWPersonality.GUICore.bulletinBoardDataSection['textNews'])

    def updateTextQuest(self):
        if BWPersonality.GUICore.bulletinBoardDataSection.has_key('textQuest'):
            self.component.textQuest.script.setText(BWPersonality.GUICore.bulletinBoardDataSection['textQuest'])