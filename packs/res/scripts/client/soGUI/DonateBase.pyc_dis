# Embedded file name: scripts/client/soGUI/DonateBase.py
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import BWPersonality
from Helpers.PyGUI.PyGUIBase import PyGUIBase
import gui_jokes
import ItemsUtils
from soGUI.soEditField import soEditField2
from Settings import Settings
from soGUI.soButton import soButton
from soGUI.soCheckBox import soCheckBox
from Helpers.PyGUI import PyGUIEvent
from gui_const import MESSAGEBOX
from Localization import lc
from soGUI.soTableComponent import soTableComponent2, soTablePropsStructure, soTableElemPropsStructure
from functools import partial

class DonatebaseGUI(PyGUIBase):
    factoryString = 'soGUI.DonatebaseGUI'
    FRAME_TEXTURE = 'soGUI/maps/Controls/inventory/inventoryFrame2.tga'
    widthWin = 1000
    heightWin = 300

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.COLORFONT = (70, 161, 68, 255)
        self.COLORFONT_FOR_CAPTION = (175, 166, 112, 255)
        self.data = []
        self.index = 1
        self.Table_caption = {'font': 'ruRU_calibri_default.font',
         'color': (50, 50, 50, 255),
         'hoverColor': (50, 50, 50, 255),
         'selectColor': (50, 50, 50, 255),
         'toolTipID': None,
         'contentColor': self.COLORFONT_FOR_CAPTION,
         'contentColorHover': self.COLORFONT_FOR_CAPTION,
         'contentColorSelect': self.COLORFONT_FOR_CAPTION}
        self.Table_content = {'font': 'ruRU_calibri_default.font',
         'color': (255, 255, 100, 0),
         'hoverColor': (255, 255, 100, 0),
         'selectColor': (28, 28, 28, 255),
         'toolTipID': None,
         'contentColor': self.COLORFONT,
         'contentColorHover': self.COLORFONT,
         'contentColorSelect': self.COLORFONT}
        self.setupRoot()
        self.setupContent()
        return

    def setupRoot(self):
        self.component.textureName = ''
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.horizontalPositionMode = self.component.verticalPositionMode = 'CLIP'
        self.component.width = self.widthWin
        self.component.height = self.heightWin
        self.component.position = (0.0, 0.0, 0.1)
        self.component.materialFX = 'BLEND'
        self.component.colour = (255, 255, 255, 255)
        self.component.horizontalAnchor = 'CENTER'
        self.component.verticalAnchor = 'CENTER'
        self.component.visible = False

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = self.heightWin
        cmp.width = self.widthWin
        cmp.position = (0, 0, 0.9)
        self.component.addChild(cmp, 'mFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.text = lc('GUI.DonateBase.title')
        cmp.position = (10, 5, 0.3)
        self.component.addChild(cmp, 'caption')
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
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 100
        cmp.height = 20
        cmp.position = (self.widthWin - 110, self.heightWin - 30, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp.visible = 1
        btn.onClick = self.onView
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = lc('GUI.DonateBase.view')
        self.component.addChild(btn.component, 'bView')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 120
        cmp.height = 20
        cmp.position = (self.widthWin - 230, self.heightWin - 30, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp.visible = 1
        btn.onClick = self.onCashback
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = lc('GUI.DonateBase.cashback')
        self.component.addChild(btn.component, 'bCancelEntry')
        tbl = soTableComponent2(GUI.Window(), soTablePropsStructure(tableHeight=self.heightWin - 80, tableWidth=self.widthWin - 10, outerBorderWidth=1, innerBorderWidth=1, innerBorderColor=(85, 85, 85, 255)), isDefaultScrollBar='FALSE')
        cmp = tbl.component
        tbl.onElementEvent = self.onKeyTableElem
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (5, 38, 0.9)
        self.component.addChild(cmp, 'TableDonateBase')
        tbl.onBound()
        widthCol = self.widthWin / 5
        tbl.addCols([['tenant', widthCol - 15],
         ['name', widthCol + 15],
         ['locate', widthCol],
         ['timeToSell', widthCol],
         ['stake', widthCol - 25]])

    def onDepositChange(self):
        BigWorld.player().setDeposit()

    def onDepositBack(self):
        BigWorld.player().depositBack()

    def setDeposit(self, value):
        self.component.depositValue.text = lc('GUI.DonateBase.deposit') + ': %s' % value

    def displayListDonateBase(self, data = []):
        table = self.component.TableDonateBase.script
        rows = []
        self.data = data
        is_owner = filter(lambda x, y = BigWorld.player().clanID: x[1] == y, data)
        print 'is_owner', is_owner
        if not is_owner:
            self.component.bView.script.setDisabledState(False)
        else:
            self.component.bView.script.setDisabledState(True)
        rows.append([(20, 'MIDDLE'), {'tenant': {'props': soTableElemPropsStructure(dataStyles=self.Table_caption),
                     'data': {'text': lc('GUI.DonateBase.tenant')}},
          'name': {'props': soTableElemPropsStructure(dataStyles=self.Table_caption),
                   'data': {'text': lc('GUI.DonateBase.name')}},
          'locate': {'props': soTableElemPropsStructure(dataStyles=self.Table_caption),
                     'data': {'text': lc('GUI.DonateBase.location')}},
          'timeToSell': {'props': soTableElemPropsStructure(dataStyles=self.Table_caption),
                         'data': {'text': lc('GUI.DonateBase.timeToSell')}},
          'stake': {'props': soTableElemPropsStructure(dataStyles=self.Table_caption),
                    'data': {'text': lc('GUI.DonateBase.stake')}}}])
        for temp in data:
            stake = temp[5]
            if temp[4]:
                stake = '-'
            rows.append([(20, 'MIDDLE'), {'tenant': {'props': soTableElemPropsStructure(dataStyles=self.Table_content),
                         'data': {'text': temp[4].decode('utf-8') or lc('GUI.DonateBase.noFartherRent')}},
              'name': {'props': soTableElemPropsStructure(dataStyles=self.Table_content),
                       'data': {'text': lc('DonateBases.name.%s' % temp[0])}},
              'locate': {'props': soTableElemPropsStructure(dataStyles=self.Table_content),
                         'data': {'text': lc('DonateBases.location.%s' % temp[0])}},
              'timeToSell': {'props': soTableElemPropsStructure(dataStyles=self.Table_content),
                             'data': {'text': temp[2]}},
              'stake': {'props': soTableElemPropsStructure(dataStyles=self.Table_content),
                        'data': {'text': stake}}}])

        table.clearTable()
        table.addRows(rows)

    def onKeyTableElem(self, col, row, event, data):
        tbl = self.component.TableDonateBase.script
        if row == 0:
            return
        self.index = row
        if event == 'LEFTMOUSE':
            tbl.clearSelection()
            tbl.selectRow(row)
        if self.data[self.index - 1][7] and not self.component.bView.script.buttonDisabled:
            self.component.bView.script.setDisabledState(False)
        else:
            self.component.bView.script.setDisabledState(True)

    def onCloseBox(self):
        self.hide()

    def onCashback(self):
        BigWorld.player().cashback()

    def onView(self):
        if self.index:
            BigWorld.player().getBaseByName(self.data[self.index - 1][0])

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'DonateBaseGUI')
        self.displayListDonateBase()
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()


class DetailViewStakeGUI(PyGUIBase):
    factoryString = 'soGUI.DetailViewStakeGUI'
    FRAME_TEXTURE = 'soGUI/maps/Controls/inventory/inventoryFrame2.tga'
    widthWin = 350
    heightWin = 380
    vIndent = 15
    COLORFONT = (140, 141, 126, 255)

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        self.component.textureName = ''
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.horizontalPositionMode = self.component.verticalPositionMode = 'CLIP'
        self.component.width = self.widthWin
        self.component.height = self.heightWin
        self.component.position = (0.0, 0.0, 0.1)
        self.component.materialFX = 'BLEND'
        self.component.colour = (255, 255, 255, 255)
        self.component.horizontalAnchor = 'CENTER'
        self.component.verticalAnchor = 'CENTER'
        self.component.visible = False

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = self.heightWin
        cmp.width = self.widthWin
        cmp.position = (0, 0, 0.9)
        self.component.addChild(cmp, 'mFrame')
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
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_small.font'
        cmp.colour = self.COLORFONT
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 30 + self.vIndent, 0.3)
        cmp.text = lc('GUI.DonateBase.DateEndRent')
        self.component.addChild(cmp, 'DateEndRentLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_small.font'
        cmp.colour = self.COLORFONT
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 60 + self.vIndent, 0.3)
        cmp.text = lc('GUI.DonateBase.DateEndAuction')
        self.component.addChild(cmp, 'DateEndAuctionLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_small.font'
        cmp.colour = self.COLORFONT
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 90 + self.vIndent, 0.3)
        cmp.text = lc('GUI.DonateBase.FartherRent')
        self.component.addChild(cmp, 'FartherRentLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_small.font'
        cmp.colour = self.COLORFONT
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 120 + self.vIndent, 0.3)
        cmp.text = lc('GUI.DonateBase.CountMemberAuction')
        self.component.addChild(cmp, 'CountMemberAuctionLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_small.font'
        cmp.colour = self.COLORFONT
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 150 + self.vIndent, 0.3)
        cmp.text = lc('GUI.DonateBase.LastStake')
        self.component.addChild(cmp, 'LastStakeLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_small.font'
        cmp.colour = self.COLORFONT
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 180 + self.vIndent, 0.3)
        cmp.text = lc('GUI.DonateBase.StepAuction')
        self.component.addChild(cmp, 'StepAuctionLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_small.font'
        cmp.colour = self.COLORFONT
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 210 + self.vIndent, 0.3)
        cmp.text = lc('GUI.DonateBase.IncStake')
        self.component.addChild(cmp, 'IncStakeLabel')
        edit = soEditField2(GUI.Window(), height=20, width=110)
        edit.onBound()
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (110, 240, 0.2)
        self.component.addChild(cmp, 'editIncStake')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 250
        cmp.height = 20
        cmp.position = (50, 270, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp.visible = 1
        btn.onClick = self.onIncStake
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = lc('GUI.DonateBase.bInc')
        self.component.addChild(btn.component, 'bIncStakes')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 250
        cmp.height = 20
        cmp.position = (50, 300, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp.visible = 1
        btn.onClick = self.onConfirmStake
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = lc('GUI.DonateBase.bConfirmStake')
        self.component.addChild(btn.component, 'bConfirmStake')

    def onConfirmStake(self):
        BigWorld.player().setNewPrice(int(self.component.editIncStake.script.getValue()))
        self.component.editIncStake.script.setValue('')

    def onIncStake(self):
        BigWorld.player().incByStep()

    def updateInfo(self, data = {}):
        values = {'clan': data['clan'].decode('utf-8') if data.has_key('clan') else '',
         'tenant': data['tenant'] if data.has_key('tenant') else lc('GUI.DonateBase.noFartherRent'),
         'timeToSell': data['timeToSell'] if data.has_key('timeToSell') else '',
         'minPrice': data['minPrice'] if data.has_key('minPrice') else '',
         'countMemberAuction': data['countMembers'] if data.has_key('countMembers') else '0',
         'lastStake': data['maxPrice'] if data.has_key('maxPrice') else '0',
         'stepAuction': data['stepAuction'] if data.has_key('stepAuction') else '0',
         'incStake': data['incStake'] if data.has_key('incStake') else '0'}
        self.component.DateEndRentLabel.text = ''
        self.component.DateEndAuctionLabel.text = ''
        self.component.FartherRentLabel.text = lc('GUI.DonateBase.FartherRent') + values['minPrice']
        self.component.CountMemberAuctionLabel.text = lc('GUI.DonateBase.CountMemberAuction') + values['countMemberAuction']
        self.component.LastStakeLabel.text = lc('GUI.DonateBase.LastStake') + values['lastStake']
        self.component.StepAuctionLabel.text = lc('GUI.DonateBase.StepAuction') + values['stepAuction']
        self.component.IncStakeLabel.text = lc('GUI.DonateBase.IncStake') + values['incStake']

    def onCloseBox(self):
        self.hide()

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'DetailViewStakeGUI')
        self.updateInfo()
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()


class ClanManagerNPCGUI(PyGUIBase):
    factoryString = 'soGUI.ClanManagerNPCGUI'
    FRAME_TEXTURE = 'soGUI/maps/Controls/inventory/inventoryFrame2.tga'
    widthWin = 350
    heightWin = 380
    vIndent = 15
    COLORFONT = (140, 141, 126, 255)

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.cost = ''
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        self.component.textureName = ''
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.horizontalPositionMode = self.component.verticalPositionMode = 'CLIP'
        self.component.width = self.widthWin
        self.component.height = self.heightWin
        self.component.position = (0.0, 0.0, 0.1)
        self.component.materialFX = 'BLEND'
        self.component.colour = (255, 255, 255, 255)
        self.component.horizontalAnchor = 'CENTER'
        self.component.verticalAnchor = 'CENTER'
        self.component.visible = False

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = self.heightWin
        cmp.width = self.widthWin
        cmp.position = (0, 0, 0.9)
        self.component.addChild(cmp, 'mFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.text = lc('GUI.DonateBase.title_manager')
        cmp.position = (10, 5, 0.3)
        self.component.addChild(cmp, 'caption')
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
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.font = 'ruRU_calibri_small.font'
        cmp.colour = self.COLORFONT
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 30 + self.vIndent, 0.3)
        cmp.text = ''
        self.component.addChild(cmp, 'greetingLabel')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 250
        cmp.height = 20
        cmp.position = (50, self.heightWin - (cmp.height + 10), 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp.visible = 1
        btn.onClick = self.onCloseBox
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = lc('GUI.IngameMenu.exit')
        self.component.addChild(btn.component, 'bExit')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 250
        cmp.height = 30
        cmp.position = (50, self.heightWin - 2 * (cmp.height + 10), 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp.visible = 1
        btn.onClick = self.onOpenWarehouse
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = lc('GUI.DonateBase.warehouse')
        self.component.addChild(btn.component, 'bWarehouse')
        btn = soButton(GUI.Window())
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 250
        cmp.height = 30
        cmp.position = (50, self.heightWin - 3 * (cmp.height + 10), 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        cmp.visible = 1
        btn.onClick = self.onGuardsClick
        btn.initVSC('soGUI/visual_styles/skillTab.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = lc('GUI.DonateBase.guards')
        self.component.addChild(btn.component, 'bManagement')

    def show(self, npc_id = 0):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'ClanManagerNPCGUI')
        self.npc_id = npc_id
        self.update()
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def update(self, data = {}):
        if data:
            self.component.greetingLabel.text = lc('GUI.DonateBase.greeting').format(name=lc('DonateBases.name.%s' % data['name']))
            self.cost = data['cost']

    def onCloseBox(self):
        self.hide()

    def onGuardsClick(self):

        def okey_callback(event):
            if event == gui_jokes.askUserYesNo.YES:
                BigWorld.player().guards_activate()

        gui_jokes.askUserYesNo(lc('GUI.DonateBase.guards'), lc('GUI.DonateBase.recruitment_text').format(cost=self.cost), okey_callback)

    def onOpenWarehouse(self):
        self.hide()
        BigWorld.player().StartItemCache(self.npc_id, ItemsUtils.CACHE_MODE_WAREHOUSE)