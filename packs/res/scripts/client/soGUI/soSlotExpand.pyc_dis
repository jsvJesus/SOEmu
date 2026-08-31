# Embedded file name: scripts/client/soGUI/soSlotExpand.py
import BigWorld
import GUI
import BWPersonality
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.PyGUI import PyGUIEvent
from Localization import lc
from soGUI.soButton import soButton, soButtonWTT
from Items import ItemsCatalog
from utils import groupNumber
import ItemsUtils
import gui_jokes
import colorCodes
import math
import soGUI.soNumberBox

def timeToString(secs):
    if secs < 0:
        return u''
    hours = math.floor(secs / 3600.0)
    minutes = math.floor((secs - hours * 3600.0) / 60.0)
    seconds = secs - (hours * 3600.0 + minutes * 60.0)
    outH = str(int(hours)) if hours > 9 else u'0' + str(int(hours))
    outM = str(int(minutes)) if minutes > 9 else u'0' + str(int(minutes))
    outS = str(int(seconds)) if seconds > 9 else u'0' + str(int(seconds))
    if hours > 0:
        return u'' + outH + lc('Inventory.client.HOURS')
    if minutes > 0:
        return u'' + outM + lc('Inventory.client.MINUTES')
    if seconds >= 0:
        return u'' + outS + lc('Inventory.client.SECONDS')
    return u''


class SlotItemTT2(PyGUIBase):
    factoryString = 'soGUI.soSlotExpand'

    def __init__(self, component, width = 64, height = 64):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.component.width = width
        self.component.height = height
        self.setupRoot()
        self.setupContent()

    def setupRoot(self):
        pass

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/cellFrame2.tga')
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.component.width
        cmp.height = self.component.height
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.9)
        self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.component.width
        cmp.height = self.component.height
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.4)
        self.component.addChild(cmp, 'itemIcon')
        cmp = GUI.Simple('soGUI/maps/Controls/inventory/broken.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.component.width
        cmp.height = self.component.height
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.7)
        cmp.visible = False
        self.component.addChild(cmp, 'itemBroken')
        cmp = GUI.Simple('soGUI/maps/Icons/icon_item_painted.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.component.width / 5
        cmp.height = self.component.height / 5
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.component.width, cmp.height / 2, 0.7)
        cmp.visible = 0
        self.component.addChild(cmp, 'itemColored')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.component.width - 5, 5, 0.3)
        self.component.addChild(cmp, 'itemCount')

    def show(self, itemData):
        self.itemData = itemData
        if not itemData:
            self.component.visible = False
            return
        else:
            self.component.visible = True
            self.component.itemBroken.visible = False
            self.component.itemColored.visible = False
            item_type = itemData['complexItemType']
            item_id = itemData['complexItemID']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            item_level = item_params['Level']
            iconName = ItemsUtils.getTextureByTint(self.itemData)
            if not iconName:
                iconName = item_params['IconName']
            if BWPersonality.GUICore.iconTextures is not None:
                if iconName not in BWPersonality.GUICore.iconTextures.failedIDs:
                    if BWPersonality.GUICore.iconTextures.has_key(iconName):
                        self.component.itemIcon.texture = BWPersonality.GUICore.iconTextures[iconName]
                    else:
                        self.component.itemIcon.textureName = iconName
            else:
                self.component.itemIcon.textureName = iconName
            countStr = ItemsUtils.GetDisplayValue(itemData)
            countInt = int(countStr) if countStr.isdigit() else 0
            friendlyName = ItemsUtils.GetItemName(item_type, fGetShortName=True, tintItem=self.itemData)
            bigName = ItemsUtils.GetItemName(item_type, fGetShortName=False, tintItem=self.itemData)
            Cost = int(item_params.get('Cost', 0))
            self.component.itemCount.text = countStr
            item_state = ItemsUtils.GetItemConditionPercent(BigWorld.player(), self.itemData)
            if item_state <= 0.5:
                self.component.itemBroken.visible = True
            else:
                self.component.itemBroken.visible = False
            self.component.itemColored.visible = bool(ItemsUtils.getTintID(self.itemData))
            inconstantParam = ItemsUtils.GetComplexItemInconstanParams(self.itemData)
            if inconstantParam.get(ItemsCatalog.INC_ARTEFACT_DEAD, 0):
                self.component.itemBroken.visible = True
            return


class soSlotExpand(PyGUIBase):
    factoryString = 'soGUI.soSlotExpand'
    SLOTWIDTH = 64
    SLOTHEIGHT = 64
    SUBSLOTWIDTH = 25
    SUBSLOTHEIGHT = 25
    MAXSUBICONS = 4

    def __init__(self, component, width, height, dw, dh):
        PyGUIBase.__init__(self, component)
        component.script = self
        self._width = width
        self._height = height
        self._dw = dw
        self._dh = dh
        self.setupContent()

    def setupContent(self):
        slot = SlotItemTT2(GUI.Window(), self.SLOTWIDTH, self.SLOTHEIGHT)
        cmp = slot.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (0 + self._dw, 0 + self._dh, 0.9)
        cmp.width = 64
        cmp.height = 64
        self.component.addChild(cmp, 'slotItemTT')
        slot.onBound()
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'default_small.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH + 5 + self._dw, 0 + self._dh, 0.9)
        self.component.addChild(cmp, 'itemBigName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (125, 126, 102, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH + 5 + self._dw, 17 + self._dh, 0.3)
        self.component.addChild(cmp, 'itemCost')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (145, 146, 102, 255)
        cmp.materialFX = 'BLEND'
        cmp.multiline = 0
        cmp.text = u''
        cmp.position = (self.SLOTWIDTH + 5 + self._dw, 31 + self._dh, 0.3)
        self.component.addChild(cmp, 'subitemsCaption')
        for subicon in range(self.MAXSUBICONS):
            cmp = GUI.Frame2('soGUI/maps/Controls/inventory/cellFrame2.tga')
            cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.width = self.SUBSLOTWIDTH
            cmp.height = self.SUBSLOTHEIGHT
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (self.SLOTWIDTH + self._dw, 45 + self._dh + self.SUBSLOTHEIGHT * subicon, 0.9)
            self.component.addChild(cmp, 'subframeCmp_%s' % subicon)
            cmp = GUI.Simple('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.width = self.SUBSLOTWIDTH
            cmp.height = self.SUBSLOTHEIGHT
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (self.SLOTWIDTH + self._dw, 45 + self._dh + self.SUBSLOTHEIGHT * subicon, 0.9)
            self.component.addChild(cmp, 'subitemIcon_%s' % subicon)
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
            cmp.colour = (125, 126, 102, 255)
            cmp.materialFX = 'BLEND'
            cmp.text = ' asdasdawdawdawdawdawdawd'
            cmp.position = (self.SLOTWIDTH + self._dw + self.SUBSLOTWIDTH + 3, 45 + self._dh + self.SUBSLOTHEIGHT * subicon, 0.9)
            self.component.addChild(cmp, 'subname_%s' % subicon)

        subicon += 1
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.colour = (145, 126, 102, 255)
        cmp.materialFX = 'BLEND'
        cmp.text = ' '
        cmp.position = (self.SLOTWIDTH + self._dw + 3, 55 + self._dh + self.SUBSLOTHEIGHT * subicon, 0.99)
        self.component.addChild(cmp, 'allcost')

    def applyitem(self, itemData):
        item_type = itemData['complexItemType']
        item_id = itemData['complexItemID']
        item_class = ItemsCatalog.GetItemClass(item_type)
        item_params = ItemsCatalog.GetItemParam(item_type)
        item_level = item_params['Level']
        iconName = ItemsUtils.getTextureByTint(itemData)
        if not iconName:
            iconName = item_params['IconName']
        self.component.slotItemTT.script.show(itemData)
        countStr = ItemsUtils.GetDisplayValue(itemData)
        countInt = int(countStr) if countStr.isdigit() else 0
        friendlyName = ItemsUtils.GetItemName(item_type, fGetShortName=True, tintItem=itemData)
        bigName = ItemsUtils.GetItemName(item_type, fGetShortName=False, tintItem=itemData)
        Cost = int(item_params.get('Cost', 0))
        self.component.itemBigName.text = bigName
        CostStr = lc('tmplocal.strings.str32') % groupNumber(str(Cost), ' ')
        if countInt > 1:
            CostStr += u'  x%s = %s' % (countStr, groupNumber(str(Cost * countInt), ' '))
        CostStr += u'\u0440.'
        self.component.itemCost.text = CostStr
        self.component.subitemsCaption.text = u''
        itemList = itemData['itemList']
        for subicon in range(self.MAXSUBICONS):
            subframeCmp = getattr(self.component, 'subframeCmp_%s' % subicon)
            subitemIcon = getattr(self.component, 'subitemIcon_%s' % subicon)
            subname = getattr(self.component, 'subname_%s' % subicon)
            subframeCmp.visible = False
            subitemIcon.visible = False
            subname.visible = False

        for subiconI, subitem in enumerate(itemList):
            sub_item_type = subitem['itemType']
            sub_itemParam = ItemsCatalog.GetItemParam(sub_item_type)
            subcost = int(sub_itemParam.get('Cost', 0))
            subframeCmp = getattr(self.component, 'subframeCmp_%s' % subiconI)
            subitemIcon = getattr(self.component, 'subitemIcon_%s' % subiconI)
            subname = getattr(self.component, 'subname_%s' % subiconI)
            subframeCmp.visible = True
            subitemIcon.visible = True
            subname.visible = True
            power_time = ItemsUtils.GetArtefactInContainerDepleetionTime(subitem)
            subtime = u''
            if power_time:
                subtime = u' %s  ' % timeToString(power_time)
            subname.text = ItemsUtils.GetItemName(sub_item_type, fGetShortName=1) + subtime + '  + %s' % subcost
            iconName = sub_itemParam['IconName']
            if BWPersonality.GUICore.iconTextures is not None:
                if iconName not in BWPersonality.GUICore.iconTextures.failedIDs:
                    if BWPersonality.GUICore.iconTextures.has_key(iconName):
                        subitemIcon.texture = BWPersonality.GUICore.iconTextures[iconName]
                    else:
                        subitemIcon.textureName = iconName
            else:
                subitemIcon.textureName = iconName
            Cost += subcost

        if itemList:
            self.component.subitemsCaption.text = lc('tmplocal.strings.str33')
            allsum = lc('tmplocal.strings.str34') % groupNumber(str(Cost), ' ')
            if countInt > 1:
                allsum += u'  x%s = %s' % (countStr, groupNumber(str(Cost * countInt), ' '))
            allsum += u'\u0440.'
            self.component.allcost.text = allsum
        else:
            self.component.allcost.text = u''
        return

    def doReposition(self, sW, sH):
        pass