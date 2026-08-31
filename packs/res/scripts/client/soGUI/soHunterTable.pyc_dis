# Embedded file name: scripts/client/soGUI/soHunterTable.py
import traceback
import BigWorld
import BWPersonality
import GUI
import random
import colorCodes
import gui_jokes
import soGUI.soNumberBox
from Localization import lc
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soRadioButton import soRadioButton2, soRadioButton, RadioButtonPropsStructure
from utils import groupNumber
from soGUI.soButton import soButton, soButtonWTT
from Helpers.PyGUI import PyGUIEvent
from soGUI.soCheckBox import soCheckBox
from utils import groupNumber
MAPLIST = {'spaces/main': lc('soGPSMap.soGUI.STRING_500_104'),
 'spaces/so_origins': lc('soGPSMap.soGUI.STRING_501_113'),
 'spaces/novaya': lc('soGPSMap.soGUI.STRING_502_107'),
 'spaces/tunguska': lc('soGPSMap.soGUI.STRING_503_111'),
 'spaces/steppe': lc('soGPSMap.soGUI.STRING_504_107'),
 'spaces/steppe_dust': lc('soGPSMap.soGUI.STRING_steppe_dust'),
 'spaces/vesuvius': lc('soGPSMap.soGUI.STRING_505_111'),
 'spaces/volcano': lc('soGPSMap.soGUI.STRING_506_107'),
 'spaces/city_lubech': lc('soGPSMap.soGUI.STRING_507_117'),
 'spaces/outlands': lc('soGPSMap.soGUI.STRING_508_112'),
 'spaces/fukushima': lc('soGPSMap.soGUI.minimap_fukushima'),
 'spaces/outlands_caravan': lc('soGPSMap.soGUI.minimap_outlands_caravan'),
 'spaces/pk_prison01': lc('soGPSMap.soGUI.minimap_pk_prison01'),
 'spaces/lubech_uderground': lc('soGPSMap.soGUI.minimap_lubech_underground'),
 'spaces/outlands_airport': lc('soGPSMap.soGUI.minimap_outlands_airport'),
 'spaces/dm_outlands_village': lc('soGPSMap.soGUI.minimap_dm_outlands_village'),
 'spaces/dm_rocks': lc('soGPSMap.soGUI.minimap_dm_rocks'),
 'spaces/dm_ryabinushka': lc('soGPSMap.soGUI.minimap_dm_ryabinushka'),
 'spaces/dm_snowland': lc('soGPSMap.soGUI.minimap_dm_snowland')}

class RowItemH(PyGUIBase):

    def __init__(self, component, width, height, position, buyHandler, updateHandler):
        component.script = self
        PyGUIBase.__init__(self, component)
        self.width = width
        self.height = height
        self._dw = 2
        self._dh = 2
        self.buyHandler = buyHandler
        self.updateHandler = updateHandler
        self.position = position
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = self.width
        cmp.height = self.height
        cmp.position = self.position
        cmp = GUI.Simple('textures/default/bright_gray.jpg')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 100)
        cmp.materialFX = 'BLEND'
        cmp.width = self.component.width
        cmp.height = 1
        cmp.position = (5, self.height, 0.9)
        cmp.visible = 1
        self.component.addChild(cmp, 'frameDown')

    def setupContent(self):
        w = self.width
        h = self.height
        cmp = GUI.Text('WantedName')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'default_small.font'
        cmp.colour = (255, 100, 100, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (10, 10, 0.3)
        self.component.addChild(cmp, 'WantedName')
        cmp = GUI.Text('VictimName')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'default_small.font'
        cmp.colour = (200, 200, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (w / 5, 10, 0.3)
        self.component.addChild(cmp, 'VictimName')
        cmp = GUI.Text('lenHunters')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'default_small.font'
        cmp.colour = (200, 200, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (w / 5, 30, 0.3)
        self.component.addChild(cmp, 'lenHunters')
        cmp = GUI.Text('Cost')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'default_small.font'
        cmp.colour = (200, 200, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (w * 2 / 5.0, 10, 0.3)
        self.component.addChild(cmp, 'Cost')
        cmp = GUI.Text('TimeLost')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'default_small.font'
        cmp.colour = (200, 200, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (w * 3 / 5, 10, 0.3)
        self.component.addChild(cmp, 'TimeLost')
        cmp = GUI.Text('mapName')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'default_small.font'
        cmp.colour = (200, 200, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (w * 4 / 5.0, 10, 0.3)
        self.component.addChild(cmp, 'mapName')
        cmp = GUI.Text('online')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'default_small.font'
        cmp.colour = (100, 255, 100, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (w * 4 / 5.0, 29, 0.3)
        self.component.addChild(cmp, 'online')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.hunter.take')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 100
        cmp.height = 30
        cmp.position = (self.width, 25 + self._dh, 0.5)
        cmp.script.onClick = self._subscriptionDialog
        self.component.addChild(cmp, 'button_subscription')
        btn.onBound()
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('GUI.hunter.CancelOrder')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 130
        cmp.height = 30
        cmp.position = (self.width, 25 + self._dh, 0.5)
        cmp.script.onClick = self._removeOffender
        self.component.addChild(cmp, 'button_removeOffender')
        btn.onBound()

    def _removeOffender(self):
        BigWorld.player().removeOffender(self.WantedName)
        self.updateHandler()

    def _subscriptionDialog(self):
        self.buyHandler(self.WantedName, self.price, self.victim, self.mapName, self.timelost, self.online)

    def setItem(self, WantedName, price = 0, victim = u'', mapName = '', timelost = 0, online = False, lenHunters = 0, already = False, thisIsMy = False):
        self.WantedName = WantedName
        self.price = price
        self.victim = victim
        self.mapName = mapName
        self.timelost = timelost
        self.online = online
        self.lenHunters = lenHunters
        if not WantedName:
            self.component.visible = 0
            return
        self.component.visible = 1
        self.component.VictimName.text = victim
        self.component.WantedName.text = WantedName
        self.component.lenHunters.text = lc('GUI.hunter.hanters').format(lenHunters)
        self.component.Cost.text = groupNumber(price)
        self.component.TimeLost.text = unicode(timelost) + lc('Inventory.client.HOURS')
        if online:
            self.component.online.text = u'online'
            self.component.online.colour = (100, 255, 100, 255)
            self.component.mapName.text = mapName
        else:
            self.component.online.text = u'offline'
            self.component.online.colour = (100, 0, 0, 255)
            self.component.mapName.text = ''
        if already:
            self.component.button_subscription.script.setVisualState('disabled')
            self.component.button_subscription.script.buttonDisabled = True
        else:
            self.component.button_subscription.script.setVisualState('normal')
            self.component.button_subscription.script.buttonDisabled = False
        self.component.button_removeOffender.visible = thisIsMy
        self.component.button_subscription.visible = not thisIsMy


class soHunterTable(PyGUIBase):

    def __init__(self, component, w, h, posw, row):
        PyGUIBase.__init__(self, component)
        component.script = self
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = w
        cmp.height = h
        self.filterW = 200
        self.w = w
        self.h = h
        self.row = row
        self.posw = posw
        self._rows = []
        self.cbs = []
        self.page_start = 0
        self.last_index_item = 0
        self.old_page_start = 0
        self.old_last_index_item = 0
        self.all_index_item = 0
        self.activeWindowID = None
        self.activeWindowIDMoved = None
        self.setupContent()
        self.setupRows()
        self.setupFiltersContent()
        return

    def setupContent(self):
        tmpw = 330
        navigatepos = 5
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = u'|<'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 30
        cmp.height = 22
        cmp.position = (tmpw + 12, self.h + navigatepos, 0.5)
        cmp.script.onClick = self.buttonFindClick
        self.component.addChild(cmp, 'button_home')
        btn.onBound()
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = u'<'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 30
        cmp.height = 22
        cmp.position = (tmpw + 60, self.h + navigatepos, 0.5)
        cmp.script.onClick = self.buttonLeftClick
        self.component.addChild(cmp, 'button_left')
        btn.onBound()
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = u'>'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 30
        cmp.height = 22
        cmp.position = (tmpw + 60 + 32, self.h + navigatepos, 0.5)
        cmp.script.onClick = self.buttonRightClick
        self.component.addChild(cmp, 'button_right')
        btn.onBound()
        edit = soGUI.soNumberBox.soNumberBox(GUI.Window(), width=50, height=22, font='ruRU_Cyrvetica_Extra_10i.font', hOffset=5, vOffset=5)
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.position = (tmpw + 110, self.h + navigatepos, 0.5)
        cmp.script.onDefaultAction = self.goto
        self.component.addChild(cmp, 'NumberBox')
        edit.onBound()
        cmp = GUI.Text('---')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.colour = (255, 200, 120, 200)
        cmp.materialFX = 'BLEND'
        cmp.multiline = True
        cmp.position = (tmpw + 165, self.h - 25 + navigatepos, 1)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_page')
        cmp = GUI.Text(lc('GUI.hunter.caption'))
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (100, 100, 100, 255)
        cmp.materialFX = 'BLEND'
        cmp.multiline = True
        cmp.position = (tmpw + 165 + 90, self.h - 25 + navigatepos + 5, 1)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_info_beta')

    def setupFiltersContent(self):

        def xonStateChange():
            self.buttonFindClick()

        w = self.component.width
        sortBy = [(2, 10, lc('GUI.hunter.PK')),
         (1, w / 5.0, lc('GUI.hunter.injured')),
         (0, w * 2 / 5.0, lc('GUI.hunter.reward')),
         (3, w * 3 / 5.0, lc('GUI.hunter.remainingTime'))]
        for sortindex, wpos, caption in sortBy:
            rb = soRadioButton2(GUI.Window(), btnW=18, btnH=18, radioGroup='radiogr_sortBy_hunter', labelText=caption, bvisual_styles='soGUI/visual_styles/radioButton.xml')
            rb.onStateChange = xonStateChange
            rb.onBound()
            cmp = rb.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.position = (wpos, 23, 0.2)
            self.component.addChild(cmp, 'radio_%s' % sortindex)
            rb.setActive()

        cmp = GUI.Simple('textures/default/bright_gray.jpg')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 100)
        cmp.materialFX = 'BLEND'
        cmp.width = self.component.width
        cmp.height = 3
        cmp.position = (5, 30, 0.9)
        cmp.visible = 1
        self.component.addChild(cmp, 'frameUp')
        cmp = GUI.Text(u'')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (150, 150, 150, 255)
        cmp.materialFX = 'BLEND'
        cmp.multiline = True
        cmp.position = (w - 10, 23, 0.2)
        cmp.multiline = True
        self.component.addChild(cmp, 'label_listWanted')

    def getIndexSortBy(self):
        for index in range(3):
            cmp = getattr(self.component, 'radio_%s' % index, None)
            if cmp and cmp.script.isChecked():
                return index

        print 'getIndexSortBy = no isChecked? wtf7'
        return 0

    def setupRows(self):
        rowh = int(self.h / (self.row + 1.0))
        drowh = int(rowh + 2)
        roww = int(self.w - self.posw) - 1
        for index in range(self.row):
            position = (int(self.posw), 28 + int(drowh * index), 0.5)
            cb = RowItemH(GUI.Window(), roww, rowh, position, self.subscriptionDialog, self.updatePage)
            cmp = cb.component
            cb.setItem(None)
            self.component.addChild(cmp, 'sub_row_%s' % index)
            cb.onBound()
            self._rows.append(cb)

        return

    def goto(self):
        newStartPage = self.component.NumberBox.script.rawText
        if newStartPage.isdigit():
            page_start = int(newStartPage)
            page_len = self.row
            sortFlag = self.getIndexSortBy()
            forward = 1
            BigWorld.player().getHunterCatalogFiltered(sortFlag, forward, page_start, self.row)

    def updatePage(self):
        sortFlag = self.getIndexSortBy()
        BigWorld.player().getHunterCatalogFiltered(sortFlag, 1, self.page_start, self.row)

    def buttonFindClick(self):
        sortFlag = self.getIndexSortBy()
        BigWorld.player().getHunterCatalogFiltered(sortFlag, 1, 0, self.row)

    def buttonRightClick(self):
        sortFlag = self.getIndexSortBy()
        forward = 1
        if self.page_start > self.last_index_item:
            startfrom = self.page_start
        else:
            startfrom = self.last_index_item
        BigWorld.player().getHunterCatalogFiltered(sortFlag, forward, startfrom, self.row)

    def buttonLeftClick(self):
        sortFlag = self.getIndexSortBy()
        forward = 0
        if self.page_start < self.last_index_item:
            startfrom = self.page_start
        else:
            startfrom = self.last_index_item
        BigWorld.player().getHunterCatalogFiltered(sortFlag, forward, startfrom, self.row)

    def setData(self, data):
        dataitems = data['data']
        self.old_page_start = self.page_start
        self.old_last_index_item = self.last_index_item
        self.page_start = page_start = data['page_start']
        self.last_index_item = last_index_item = data['last_index_item']
        self.all_index_item = all_index_item = data['all_index_item']
        self.component.label_page.text = '%s-%s/%s' % (page_start, last_index_item + 1, all_index_item)
        listwanted = BigWorld.player().HUNTER_listOfWanted
        plname = BigWorld.player().name
        self.component.label_listWanted.text = lc('tmplocal.strings.str1') % (5 - len(listwanted))
        for cb, item in map(lambda a, b: (a, b), self._rows, dataitems):
            if item:
                victimName, WantedName, cost, timelost, (online, spaceID, position), lenHunters = item
                mappath, lcmapName = BWPersonality.GUICore.getSpaceName(spaceID)
                cb.setItem(WantedName, price=cost, victim=victimName, mapName=lcmapName, timelost=timelost, online=online, lenHunters=lenHunters, already=WantedName in listwanted, thisIsMy=plname == victimName)
            else:
                cb.setItem(None)

        return

    def subscriptionDialog(self, WantedName = '', price = 0, victim = '', mapName = '', timelost = '', online = ''):

        def foo(event):
            if event == gui_jokes.askUserYesNo.YES:
                BigWorld.player().subscriptionWanted(WantedName)
                self.updatePage()

        ca = colorCodes.tf3_regular_text_color
        cb = colorCodes.tf3_chat_pm
        cr = '<color=255255255000>'
        capt = lc('tmplocal.strings.str2')
        ask = lc('tmplocal.strings.str3') % (ca,
         cr,
         cb,
         WantedName) + '\n'
        if online:
            ask += lc('tmplocal.strings.str4') % (ca, cr, u'<color=100255100255>') + '\n'
        else:
            ask += lc('tmplocal.strings.str5') % (ca, cr, u'<color=255150150200>') + '\n'
        if mapName:
            ask += lc('tmplocal.strings.str6') % (ca,
             cr,
             cb,
             mapName) + '\n'
        ask += lc('tmplocal.strings.str7') % (ca,
         cr,
         cb,
         groupNumber(price)) + '\n'
        gui_jokes.askUserYesNo(capt, ask, foo)

    def handleKeyEvent(self, event):
        return False

    def scrolledUP(self):
        pass

    def scrolledDOWN(self):
        pass

    def show(self):
        self.component.moveFocus = True
        self.component.crossFocus = True
        self.component.focus = True
        self.buttonFindClick()

    def handleMouseEvent(self, cmp, event):
        return True