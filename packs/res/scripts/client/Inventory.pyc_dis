# Embedded file name: scripts/client/Inventory.py
"""
Created on 28.07.2010

@author: leviathan
"""
from copy import copy
import colorCodes
from Items import ItemsCatalog
from Settings import Settings
import BWPersonality
import BigWorld
import ItemsUtils
import WorkbenchUtil
from soGUI.soActionBar import soActionBar
from soGUI.soInventoryScreen import soInventoryScreen
import soGUI.soInventoryScreen
import soGUI.soCraftGUI
import Helpers.Listener as Listener
import ResMgr
from encodings import utf_8
import traceback
from mhlib import isnumeric
import Stats
import CharacterUtils
from Perks import PerkList
from CharacterUtils import CharacterConst
from FiringDefs import DamageTypes
from FiringDefs import FiringDefs
from Perks import PerkCatalog
from GPSMap import GPSMap
from functools import partial
import gui_jokes
from MapNotes import MapNotes
import BWPersonality
from soGUI.soCharacterScreen import soCharacterScreen2
import math
import Math
from soGUI.soCrosshairs import soTargettingGUI
from Localization import lc, openLocalizeSection
import msgbox_templates
from gui_const import INVENTORY
from gui_const import NPC_VENDOR
from gui_const import REPAIR
from gui_const import MESSAGEBOX
from gui_const import ITEM_CACHE
import utils
from Math import Vector3
SCOPE_MULTIPLER_TABLE = {ItemsCatalog.SCOPE_BASIC: [1.5, soTargettingGUI.SCOPETUBE_DEFAULT, soTargettingGUI.SCOPELENS_DEFAULT],
 ItemsCatalog.SCOPE_USSR_COLLIMATOR: [1.2, soTargettingGUI.SCOPETUBE_COLLIMATOR_1, soTargettingGUI.SCOPELENS_COLLIMATOR_1],
 ItemsCatalog.SCOPE_USSR_4X: [4.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_PSO1],
 ItemsCatalog.SCOPE_USSR_6X: [6.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_PO6],
 ItemsCatalog.SCOPE_USSR_8X: [8.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_PO6],
 ItemsCatalog.SCOPE_USSR_12X: [12.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_PO6],
 ItemsCatalog.SCOPE_NATO_COLLIMATOR: [1.2, soTargettingGUI.SCOPETUBE_COLLIMATOR_2, soTargettingGUI.SCOPELENS_COLLIMATOR_1],
 ItemsCatalog.SCOPE_NATO_ASSAULT: [1.5, soTargettingGUI.SCOPETUBE_ASSAULT, soTargettingGUI.SCOPELENS_PENEK],
 ItemsCatalog.SCOPE_NATO_SNIPER_3X: [3.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_CROSS],
 ItemsCatalog.SCOPE_NATO_SNIPER_4X: [4.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_CROSS],
 ItemsCatalog.SCOPE_NATO_SNIPER_6X: [6.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_DOT],
 ItemsCatalog.SCOPE_NATO_SNIPER_8X: [8.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_DOT],
 ItemsCatalog.SCOPE_NATO_SNIPER_12X: [12.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_DOT],
 ItemsCatalog.SCOPE_USSR_VAR_X2: [2.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_PO6],
 ItemsCatalog.SCOPE_USSR_VAR_4X: [4.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_PO6],
 ItemsCatalog.SCOPE_USSR_VAR_6X: [6.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_PO6],
 ItemsCatalog.SCOPE_USSR_VAR_8X: [8.0, soTargettingGUI.SCOPETUBE_SNIPER, soTargettingGUI.SCOPELENS_PO6]}
MAX_KEY_BAR_LENGTH = 10
MAX_QUICK_BAR_LINES = 10
QUICK_DATA_POS, QUICK_TYPE_POS = (0, 1)
QUICK_BAR_EMPTY, QUICK_BAR_ITEM, QUICK_BAR_SKILL, QUICK_BAR_CHAT = xrange(4)

class Inventory:

    def Initialize(self):
        self.itemChangeTimer = None
        self.ReportChangedItemDict = {}
        self.updateInventoryTimer = None
        BWPersonality.GUICore.addListener('toolTipEvent', self.ToolTipEnable)
        BWPersonality.GUICore.addListener('skillEvent', self.SkillEvent)
        BWPersonality.GUICore.addListener('pcTradeEvent', self.ExchangeEvent)
        BWPersonality.GUICore.addListener('itemCacheEvent', self.ItemCacheEvent)
        BWPersonality.GUICore.addListener('itemCacheUserFireEvent', self.itemCacheUserFireEvent)
        BWPersonality.GUICore.addListener('itemCacheWarehouseEvent', self.itemCacheWarehouseEvent)
        BWPersonality.GUICore.addListener('GPSEvent', self.GPSEvent)
        BWPersonality.GUICore.addListener('inventoryEvent', self.inventoryEvent)
        BWPersonality.GUICore.addListener('tradeEvent', self.tradeEvent)
        BWPersonality.GUICore.addListener('craftEvent', self.craftEvent)
        BWPersonality.GUICore.addListener('charScreenEvent', self.charScreenEvent)
        BWPersonality.GUICore.addListener('packageSellEvent', self.NPCBarterEvent)
        BWPersonality.GUICore.addListener('actionBarEvent', self.actionBarEvent)
        BWPersonality.GUICore.addListener('repairEvent', self.repairEvent)
        self.items_to_drop = []
        self.ToSellList = []
        self.SellMode = NPC_VENDOR.MODE_SELL_FOR_MONEY
        self.InitNPCBarter()
        self.inventoryFilter = Settings().getSetting('inventoryFilter', 63)
        self.itemcacheFilter = Settings().getSetting('itemcacheFilter', 63)
        self.tradeFilter = Settings().getSetting('tradeFilter', 63)
        self.InitNameStrings()
        self.InitWeaponAmmo()
        self.InitSkillData()
        self.InitGUI()
        self.InitGPSProvider(BWPersonality.currentSpace)
        self.InitCraft()
        self.InitTrade()
        self.InitRepair()
        self.InitItemCache()
        self.InitItemPositions()
        self.playerExchangeInProgress = False
        if not hasattr(self, 'position_dict'):
            self.inventoryPositionList = []
        self.CheckAllItemsInPosList()
        self.InitQuickBar()
        self.InitPlayerTrade()
        self.UpdateInventory()
        return

    def InitPlayerTrade(self):
        self.PCTradeItems = []
        self.PCTradeMoney = 0
        self.PCTradeGold = 0
        self.exchange_timer_id = 0
        self.isTrade = False

    def onLeaveTalkingNPC(self):
        self.InitNPCBarter()
        self.InitTrade()
        self.InitItemCache()
        self.InitRepair()
        self.UpdateInventory()
        BWPersonality.GUICore.showStartSale(False)
        BWPersonality.GUICore.contextMenu.hide()

    def CheckQuickBarToAppendNewLines(self):
        quick_bar_lines_number = len(self.quickSlotBar)
        if self.quickSlotActiveLineNumber > quick_bar_lines_number:
            num_rows_to_add = self.quickSlotActiveLineNumber - quick_bar_lines_number
            for index in xrange(num_rows_to_add):
                self.quickSlotBar.append([ [0, QUICK_BAR_EMPTY] for x in xrange(MAX_KEY_BAR_LENGTH) ])

    def UseQuickSlot(self, num_slot):
        try:
            current_line = self.quickSlotBar[self.quickSlotActiveLineNumber - 1]
        except IndexError as e:
            print e
            return

        try:
            used_slot = current_line[num_slot]
        except IndexError as e:
            print e
            return

        if used_slot[QUICK_TYPE_POS] == QUICK_BAR_ITEM:
            item_id = used_slot[QUICK_DATA_POS]
            item = ItemsUtils.GetComplexItemByID(self, item_id)
            self.DoItemDefaultAction(item)

    def UseQuickLine(self, num_slot):
        num_slot += 1
        if len(self.quickSlotBar) >= num_slot:
            self.quickSlotActiveLineNumber = num_slot
        self.UpdateQuickBar()

    def actionBarEvent(self, event, data):
        if event == soGUI.soActionBar.EVENT_REMOVE:
            self.EmptyQuickSlot(data)
        if event == soGUI.soActionBar.EVENT_USE:
            self.UseQuickSlot(data)
        if event == soGUI.soActionBar.EVENT_CONTEXT:
            pass
        if event == soGUI.soActionBar.EVENT_MOVE:
            self.SwapQuickSlotBar(data)
        if event == soGUI.soActionBar.EVENT_BARSCROLL:
            if data > 0:
                if self.IsQuickBarLineEmpty(self.quickSlotActiveLineNumber - 1):
                    if self.quickSlotActiveLineNumber < MAX_QUICK_BAR_LINES:
                        self.quickSlotActiveLineNumber += 1
                        self.CheckQuickBarToAppendNewLines()
            elif data < 0:
                if self.quickSlotActiveLineNumber > 1:
                    self.quickSlotActiveLineNumber -= 1
        self.UpdateQuickBar()

    def IsQuickBarLineEmpty(self, lineNumber):
        try:
            current_line = self.quickSlotBar[self.quickSlotActiveLineNumber - 1]
        except IndexError as e:
            print e
            return

        for entry in current_line:
            if entry[QUICK_TYPE_POS] != QUICK_BAR_EMPTY:
                return True

        return False

    def DoItemDefaultAction(self, item):
        if item:
            if self.ItemLocked(item):
                return
            item_type = item['complexItemType']
            item_class = ItemsCatalog.GetItemClass(item_type)
            if item_class == ItemsCatalog.WEAPON:
                if not ItemsUtils.IsItemEquipped(self, item['complexItemID']):
                    self.putOnItem(item)
            elif item_class == ItemsCatalog.CLOTH:
                if not ItemsUtils.IsItemEquipped(self, item['complexItemID']):
                    self.putOnItem(item)
            elif item_class == ItemsCatalog.EXPLOSION:
                if not ItemsUtils.IsItemEquipped(self, item['complexItemID']):
                    self.equipItem(item)
            elif item_class == ItemsCatalog.BUFF:
                self.useItem(item)
            elif item_class == ItemsCatalog.AMMO:
                self.LoadAmmoInCurrentWeapon(item['complexItemID'])
            elif item_class == ItemsCatalog.GADGET:
                if not ItemsUtils.IsItemEquipped(self, item['complexItemID']):
                    self.putOnItem(item)
            elif item_class == ItemsCatalog.ARTIFACT:
                if not ItemsUtils.IsItemEquipped(self, item['complexItemID']):
                    self.putOnItem(item)

    def UpdateQuickBar(self):
        data = {}
        data['line_number'] = str(self.quickSlotActiveLineNumber)
        try:
            current_line = self.quickSlotBar[self.quickSlotActiveLineNumber - 1]
        except IndexError as e:
            print e
            return

        slots = []
        for entry_index in xrange(len(current_line)):
            quick_entry = current_line[entry_index]
            slot_dict = {'icon': '',
             'abovetext': str(entry_index + 1)[-1],
             'low_right_number': ''}
            if quick_entry[QUICK_TYPE_POS] == QUICK_BAR_EMPTY:
                slots.append(slot_dict)
                continue
            if quick_entry[QUICK_TYPE_POS] == QUICK_BAR_ITEM:
                item_id = quick_entry[QUICK_DATA_POS]
                item = ItemsUtils.GetComplexItemByID(self, item_id)
                if item:
                    item_type = item['complexItemType']
                    icon_name = ItemsUtils.GetIconName(item, item_type)
                    low_right_number = ItemsUtils.GetDisplayValue(item)
                    above_text = str(entry_index + 1)[-1]
                    slot_dict = {'icon': icon_name,
                     'abovetext': above_text,
                     'low_right_number': low_right_number}
                else:
                    current_line[entry_index] = [0, QUICK_BAR_EMPTY]
            slots.append(slot_dict)

        data['slots'] = slots
        BWPersonality.GUICore.setActionBarData(data)

    def AddItemToQuickSlot(self, item, slot_number):
        try:
            current_line = self.quickSlotBar[self.quickSlotActiveLineNumber - 1]
        except IndexError as e:
            print e
            return

        try:
            updated_slot = current_line[slot_number]
        except IndexError as e:
            print e
            return

        updated_slot = [item['complexItemID'], QUICK_BAR_ITEM]
        current_line[slot_number] = updated_slot
        self.quickSlotBar[self.quickSlotActiveLineNumber - 1] = current_line
        self.cell.SaveQuickBar(self.quickSlotBar, self.quickSlotActiveLineNumber)

    def EmptyQuickSlot(self, slot_number):
        try:
            current_line = self.quickSlotBar[self.quickSlotActiveLineNumber - 1]
        except IndexError as e:
            print e
            return

        self.quickSlotBar[self.quickSlotActiveLineNumber - 1][slot_number] = [0, QUICK_BAR_EMPTY]
        self.cell.SaveQuickBar(self.quickSlotBar, self.quickSlotActiveLineNumber)

    def SwapQuickSlotBar(self, data):
        for slot_number in data:
            if slot_number >= MAX_KEY_BAR_LENGTH:
                return

        self.quickSlotBar[self.quickSlotActiveLineNumber - 1][data[0]], self.quickSlotBar[self.quickSlotActiveLineNumber - 1][data[1]] = self.quickSlotBar[self.quickSlotActiveLineNumber - 1][data[1]], self.quickSlotBar[self.quickSlotActiveLineNumber - 1][data[0]]
        self.cell.SaveQuickBar(self.quickSlotBar, self.quickSlotActiveLineNumber)

    def InitQuickBar(self):
        self.CheckQuickBarToAppendNewLines()

    def CreateFakeItem(self, item_type, forGold = False):
        item = ItemsUtils.CreateComplexItem(0, item_type, [], [], 0)
        if forGold:
            item['forGold'] = forGold
        return item

    def IsItemFake(self, item):
        return ItemsUtils.IsItemFake(item)
        if item['complexItemID'] == 0:
            return True
        else:
            return False

    def InitItemPositions(self):
        items_positions = xrange(len(self.CarryingItems))

    def InitItemCache(self):
        self.cacheObjectID = None
        self.cacheMode = None
        BWPersonality.GUICore.showItemCache(False)
        return

    def InitRepair(self, event = False):
        self.ToolTipRepairIDFunc = None
        if not event:
            BWPersonality.GUICore.showRepairMode(False)
        return

    def charScreenEvent(self, action, item):
        item_id = item['complexItemID']
        from soGUI.soCharacterScreen import soCharacterScreen2
        if action == soCharacterScreen2.EVENT_UNEQUIP:
            self.InventoryPutOff(item)
        if action == soCharacterScreen2.EVENT_USE:
            pass
        if action == soCharacterScreen2.EVENT_REPAIR:
            BWPersonality.GUICore.showRepairMode(False)
            self.ThrowRepairID(item_id)
        if action == soCharacterScreen2.EVENT_CONTEXT:
            self.context_menu_item = item
            if self.context_menu_item:
                actions = {ItemsCatalog.CAN_UNEQUIP: lc('Inventory.TO_BACKPACK'),
                 ItemsCatalog.CAN_INFO: lc('Inventory.INFO')}
                self.StartInventoryContextMenu(actions, BWPersonality.GUICore.GUI_ID_INVENTORY)

    def InventoryPutOff(self, item):

        def put_off_listener(event):
            if event == gui_jokes.askUserYesNo.YES:
                self.putOffItem(item)

        item_type = item['complexItemType']
        if ItemsCatalog.GetItemClass(item_type) == ItemsCatalog.ARTIFACT:
            item_param = ItemsCatalog.GetItemParam(item_type)
            destroy_percent = item_param.get('UnequipDestroyChance', 0.0)
            if destroy_percent > 0.0:
                gui_jokes.askUserYesNo(lc('Inventory.client.ARTIFACT_UNEQUIP'), colorCodes.tf3_regular_text_color + lc('Inventory.client.ARTIFACT_UNEQUIP_TEXT').format(destroy_percent), put_off_listener)
                return
        self.putOffItem(item)

    def SetInventoryFilter(self, filter_mask):
        self.inventoryFilter = filter_mask
        self.UpdateInventory()

    def SetItemCacheFilter(self, filter_mask):
        self.itemcacheFilter = filter_mask
        self.RedrawItemCache()

    def SetTradeFilter(self, filter_mask):
        self.tradeFilter = filter_mask
        self.UpdateTradeInterface()

    def addStabToArtefactContainer(self, containerId, stabId):
        self.cell.addStabToArtefactContainer(containerId, stabId)

    def useDueTintWeapon(self, weaponID, dyeId):
        self.cell.useDueTintWeapon(weaponID, dyeId)

    def inventoryEvent(self, action, item):
        if action == INVENTORY.EVENT_MOVE:
            if self.ItemLocked(item[0]):
                return
            if self.ItemLocked(item[1]):
                return
            if item[0] and item[1]:
                if item[0]['complexItemType'] == item[1]['complexItemType']:
                    self.UniteItems(item[1], item[0])
                else:
                    result, error_code = ItemsUtils.canUseDyeTint(item[0], item[1])
                    if result:
                        if not error_code:

                            def put_dye_listener(event):
                                if event == gui_jokes.askUserYesNo.YES:
                                    self.useDueTintWeapon(item[0]['complexItemID'], item[1]['complexItemID'])

                            msg = lc('Inventory.ASK_USE_TINT').format(ItemsUtils.GetItemName(item[1]['complexItemType']), ItemsUtils.GetItemName(item[0]['complexItemType']))
                            gui_jokes.askUserYesNo('', msg, put_dye_listener)
                        else:
                            print 'Error canUseDyeTint', error_code
                            if ItemsUtils.FAIL_USE_TINT_OLD_TINT == error_code:
                                self.systemChatline(lc('Inventory.FAIL_USE_TINT_OLD_TINT'))
                            if ItemsUtils.FAIL_USE_TINT_NO_TINT == error_code:
                                self.systemChatline(lc('Inventory.FAIL_CANUSEDYETINT'))
                        return
                    result, part_type, error_code = ItemsUtils.CanAttachItem(self, item[0], item[1])
                    if result:
                        self.AttachItem(item[0]['complexItemID'], item[1]['complexItemID'])
                    elif error_code == ItemsUtils.FAIL_ARTEFACT_DEAD:
                        self.ReportCodedMessage(error_code)
                    elif ItemsUtils.CanAddStabToArtefactContainer(self, item[0], item[1]):
                        self.addStabToArtefactContainer(item[0]['complexItemID'], item[1]['complexItemID'])
                    else:
                        self.ChangeItemSlotNumber(item[1], item[0])
            return
        if action == INVENTORY.EVENT_TOQUICKBAR:
            if self.ItemLocked(item[0]):
                return
            self.AddItemToQuickSlot(*item)
            self.UpdateQuickBar()
            return
        if self.ItemLocked(item):
            return
        if action == INVENTORY.EVENT_EQUIP:
            self.DoItemDefaultAction(item)
        elif action == INVENTORY.EVENT_FILTERCHANGE:
            self.SetInventoryFilter(item)
        elif action == INVENTORY.EVENT_CONTEXT:
            self.context_menu_item = item
            if self.context_menu_item:
                actions = self.GetItemActions(self.context_menu_item)
                self.StartInventoryContextMenu(actions, BWPersonality.GUICore.GUI_ID_INVENTORY)
        elif action == INVENTORY.EVENT_DROP:
            self.InventoryDropItem(item)
        elif action == INVENTORY.EVENT_DELETE:
            self.InventoryDeleteItem(item)
        elif action == INVENTORY.EVENT_REPAIR:
            BWPersonality.GUICore.showRepairMode(False)
            self.ThrowRepairID(item['complexItemID'])
        elif action == INVENTORY.EVENT_ACTION:
            pass
        else:
            return

    def LockItemToDrop(self, item):
        self.items_to_drop.append(item['complexItemID'])

    def InventoryDropItem(self, item):

        def drop_listener(event):
            if event == gui_jokes.askUserYesNo.YES:
                self.dropItem(item)
            elif event == gui_jokes.askUserYesNo.NO:
                self.NeedToUpdateInventory()
            elif event == gui_jokes.askUserYesNo.CLOSED:
                self.NeedToUpdateInventory()

        gui_jokes.askUserYesNo(lc('Inventory.ITEM_DROP'), colorCodes.tf3_regular_text_color + lc('Inventory.RLY_DROP'), drop_listener)

    def InventoryDeleteItem(self, item):

        def delete_listener(event):
            if event == gui_jokes.askUserYesNo.YES:
                self.deleteItem(item)
                self.NeedToUpdateInventory()
            elif event == gui_jokes.askUserYesNo.NO:
                self.NeedToUpdateInventory()
            elif event == gui_jokes.askUserYesNo.CLOSED:
                self.NeedToUpdateInventory()

        gui_jokes.askUserYesNo(lc('Inventory.ITEM_DELETE'), colorCodes.tf3_regular_text_color + lc('Inventory.RLY_DELETE'), delete_listener)

    def StartInventoryContextMenu(self, actions, interface_id):
        BWPersonality.GUICore.addListener('contextMenuEvent', self.ContextMenuEvent)
        BWPersonality.GUICore.showContextMenu(interface_id, actions)

    def InitGPSProvider(self, space_name):
        self.GPSProvider = GPSMap(space_name)

    def UpdateGPSMap(self):
        marks = self.GPSProvider.GetMapMarks(self.position, self.mapNotes)
        BWPersonality.GUICore.setGPSdata(marks)

    def GPSNoteCallback(self, text = u''):
        name = text
        coords = self.GPSNoteData[0]
        space_name = self.GPSNoteData[1]
        position = self.GPSProvider.GetObjectAbsouluteCoords(coords[0], coords[1], space_name)
        flag = MapNotes.TYPE_CUSTOM
        self.makeMapNote(space_name, position, name, flag)

    def BugNoteCallback(self, text = u''):
        report_text = text
        position = self.GPSProvider.GetObjectAbsouluteCoords(self.BugNoteData[0], self.BugNoteData[1])
        self.reportBug(position, report_text)

    def GPSEvent(self, event, data):
        if event == soGUI.soGPSMap.EVENT_MAPCONTEXT:
            if data:
                self.context_menu_item = data
                actions = self.GetGPSContextActions()
                self.StartInventoryContextMenu(actions, BWPersonality.GUICore.GUI_ID_PDAMAP)
        if event == soGUI.soGPSMap.EVENT_MARKLEFT:
            pass
        if event == soGUI.soGPSMap.EVENT_MARKRIGHT:
            if data:
                mark_type = data[1]
                if mark_type == MapNotes.TYPE_CUSTOM:
                    mark_id = data[0]
                    self.context_menu_item = mark_id
                    actions = self.GetGPSMarkActios()
                    self.StartInventoryContextMenu(actions, BWPersonality.GUICore.GUI_ID_PDAMAP)

    def DeleteCustomGPSMark(self, data):
        if self.getMapNote(data)['flags'] == MapNotes.TYPE_CUSTOM:
            self.DeleteGPSMarks(data)

    def AddCustomGPSMark(self, data):
        self.GPSNoteData = data
        gui_jokes.inputBox(lc('Inventory.ADD_MARK'), colorCodes.tf3_regular_text_color + lc('Inventory.MARK_NOTES'), self.GPSNoteCallback)

    def reportBugEvent(self, data):
        gui_jokes.inputBox(lc('Inventory.BUG_REPORT'), u' ', self.BugNoteCallback)
        self.BugNoteData = data

    def GetGPSMarkActios(self):
        returning_list = {ItemsCatalog.CAN_DELETE_MARK: lc('Inventory.DELETE_MARK')}
        return returning_list

    def GetGPSContextActions(self):
        returning_list = {ItemsCatalog.CAN_ADD_MARK: lc('Inventory.ADD_MARK'),
         ItemsCatalog.CAN_REPORT_BUG: lc('Inventory.BUG_REPORT')}
        if self.clientAccessLevel >= 5:
            returning_list[ItemsCatalog.CAN_TELEPORT] = lc('Inventory.DO_TELEPORT')
        return returning_list

    def GetTradeContextActions(self):
        returning_list = {ItemsCatalog.CAN_BUY_TRADE: lc('Inventory.BUY_IT'),
         ItemsCatalog.CAN_INFO_TRADE: lc('Inventory.INFO')}
        return returning_list

    def InitGUI(self):
        listIcons = []
        for key in ItemsCatalog.WEAPONS.keys():
            param = ItemsCatalog.GetItemParam(key)
            listIcons.append(param['IconName'])
            listIcons.extend(param.get('TintsNames', {}).values())

        for key in ItemsCatalog.AMMOS.keys():
            listIcons.append(ItemsCatalog.GetItemParam(key)['IconName'])

        for key in ItemsCatalog.EXPLOSIONS.keys():
            listIcons.append(ItemsCatalog.GetItemParam(key)['IconName'])

        for key in ItemsCatalog.PARTS.keys():
            listIcons.append(ItemsCatalog.GetItemParam(key)['IconName'])

        for key in ItemsCatalog.BUFFS.keys():
            try:
                listIcons.append(ItemsCatalog.GetItemParam(key)['IconName'])
            except:
                print '\nsee Items.py item TypeID:', key
                raise

        for key in ItemsCatalog.CLOTHS.keys():
            try:
                listIcons.append(ItemsCatalog.GetItemParam(key)['IconName'])
            except Exception as e:
                print e
                print key
                raise

        for key in ItemsCatalog.GADJETS.keys():
            listIcons.append(ItemsCatalog.GetItemParam(key)['IconName'])

        for key in ItemsCatalog.LOOTS.keys():
            listIcons.append(ItemsCatalog.GetItemParam(key)['IconName'])

        for key in ItemsCatalog.ARTIFACTS.keys():
            listIcons.append(ItemsCatalog.GetItemParam(key)['IconName'])

        listIcons = list(set(listIcons))
        BWPersonality.GUICore.prepareInventoryIcons(listIcons)
        print 'inventory pre load texture gui', self

    def SkillEvent(self, data, event):
        if event == soGUI.soSkillScreen.EVENT_SELECT:
            if data in CharacterConst.combat_skills_ready_names:
                skill_type = PerkList.COMBAT
            elif data in CharacterConst.survival_skills_ready_names:
                skill_type = PerkList.SURVIVAL
            elif data in CharacterConst.other_skills_ready_names:
                skill_type = PerkList.OTHER
            else:
                return
            BWPersonality.GUICore.setSkillInfo(self.GetSkillText(skill_type, data))
        elif event == soGUI.soSkillScreen.EVENT_LEARNSKILL:
            if data in CharacterConst.combat_skills_ready_names:
                skill_type = PerkList.COMBAT
            elif data in CharacterConst.survival_skills_ready_names:
                skill_type = PerkList.SURVIVAL
            elif data in CharacterConst.other_skills_ready_names:
                skill_type = PerkList.OTHER
            else:
                return
            self.addPointsToSkill(skill_type, data)
        elif event == soGUI.soSkillScreen.EVENT_LEARNFEAT:
            if data[1] in CharacterConst.combat_skills_ready_names:
                skill_type = PerkList.COMBAT
            elif data[1] in CharacterConst.survival_skills_ready_names:
                skill_type = PerkList.SURVIVAL
            elif data[1] in CharacterConst.other_skills_ready_names:
                skill_type = PerkList.OTHER
            else:
                return
            self.learnPerk(skill_type, data[1], self.GetPerkID(data[0], data[1], data[2]))

    def GetPerkName(self, perkID):
        try:
            return self.PerkNames[perkID][0]
        except:
            return u''

    def GetPerkDiscription(self, perkID):
        try:
            return self.PerkNames[perkID][1]
        except:
            return u''

    def InitSkillData(self):
        BWPersonality.GUICore.skillData(self.GetSkillDict())

    def Destroy(self):
        BWPersonality.GUICore.removeListener('toolTipEvent', self.ToolTipEnable)
        BWPersonality.GUICore.removeListener('skillEvent', self.SkillEvent)
        BWPersonality.GUICore.removeListener('pcTradeEvent', self.ExchangeEvent)
        BWPersonality.GUICore.removeListener('itemCacheEvent', self.ItemCacheEvent)
        BWPersonality.GUICore.removeListener('itemCacheUserFireEvent', self.itemCacheUserFireEvent)
        BWPersonality.GUICore.removeListener('itemCacheWarehouseEvent', self.itemCacheWarehouseEvent)
        BWPersonality.GUICore.removeListener('GPSEvent', self.GPSEvent)
        BWPersonality.GUICore.removeListener('inventoryEvent', self.inventoryEvent)
        BWPersonality.GUICore.removeListener('tradeEvent', self.tradeEvent)
        BWPersonality.GUICore.removeListener('craftEvent', self.craftEvent)
        BWPersonality.GUICore.removeListener('charScreenEvent', self.charScreenEvent)
        BWPersonality.GUICore.removeListener('packageSellEvent', self.NPCBarterEvent)
        BWPersonality.GUICore.removeListener('actionBarEvent', self.actionBarEvent)
        BWPersonality.GUICore.removeListener('repairEvent', self.repairEvent)
        Settings().setSetting('inventoryFilter', self.inventoryFilter, flush=True)
        Settings().setSetting('itemcacheFilter', self.itemcacheFilter, flush=True)
        Settings().setSetting('tradeFilter', self.tradeFilter, flush=True)

    def ItemCacheEvent(self, action, data):
        if action == ITEM_CACHE.EVENT_FILTERCHANGE:
            self.SetItemCacheFilter(data)
            return
        if self.cacheMode == ItemsUtils.CACHE_MODE_SAFEBOX:
            if action == ITEM_CACHE.EVENT_TAKE:
                self.RestoreItem(self.cacheObjectID, data)
            elif action == ITEM_CACHE.EVENT_GIVE:
                self.StoreItem(self.cacheObjectID, data)
        elif self.cacheMode in (ItemsUtils.CACHE_MODE_CONTAIER, ItemsUtils.CACHE_MODE_USERFIRE):
            if action == ITEM_CACHE.EVENT_TAKE:
                self.GetItemFromContainer(self.cacheObjectID, data)
            elif action == ITEM_CACHE.EVENT_GIVE:
                self.PutItemToContainer(self.cacheObjectID, data)

    def itemCacheUserFireEvent(self, action, data):
        if action == ITEM_CACHE.EVENT_FILTERCHANGE:
            self.SetItemCacheFilter(data)
            return
        if self.cacheMode == ItemsUtils.CACHE_MODE_SAFEBOX:
            if action == ITEM_CACHE.EVENT_TAKE:
                self.RestoreItem(self.cacheObjectID, data)
            elif action == ITEM_CACHE.EVENT_GIVE:
                self.StoreItem(self.cacheObjectID, data)
        elif self.cacheMode in (ItemsUtils.CACHE_MODE_CONTAIER, ItemsUtils.CACHE_MODE_USERFIRE):
            if action == ITEM_CACHE.EVENT_TAKE:
                self.GetItemFromContainer(self.cacheObjectID, data)
            elif action == ITEM_CACHE.EVENT_GIVE:
                self.PutItemToContainer(self.cacheObjectID, data)

    def itemCacheWarehouseEvent(self, action, data):
        if action == ITEM_CACHE.EVENT_FILTERCHANGE:
            self.SetItemCacheFilter(data)
            return
        if action == ITEM_CACHE.EVENT_TAKE:
            print 'inventory itemCacheWarehouseEvent, ITEM_CACHE.EVENT_TAKE', [data]
            self.GetItemFromWarehouse(self.cacheObjectID, data)
        elif action == ITEM_CACHE.EVENT_GIVE:
            print 'inventory itemCacheWarehouseEvent, ITEM_CACHE.EVENT_GIVE', [data]
            self.PutItemToWarehouse(self.cacheObjectID, data)

    def InitNameStrings(self):
        self.DamageNames = {DamageTypes.MELEE: lc('Inventory.client.HAND_TO_HAND'),
         DamageTypes.BULLET: lc('Inventory.client.FIREARMS'),
         DamageTypes.EXPLOSION: lc('Inventory.client.EXPLOSION'),
         DamageTypes.FALL: lc('Inventory.client.FALLING'),
         DamageTypes.ARMOR_PIERCING: lc('Inventory.client.ARMOR_PIERCING'),
         DamageTypes.BLEED: lc('Inventory.client.BLEEDING'),
         DamageTypes.MAGNETIC: lc('Inventory.client.MAGNETIC'),
         DamageTypes.COLD: lc('Inventory.client.COLD'),
         DamageTypes.GRAVITATION: lc('Inventory.client.GRAVITY'),
         DamageTypes.ELECTROSTATIC: lc('Inventory.client.ELECTRICITY'),
         DamageTypes.INFRARED: lc('Inventory.client.INFRARED'),
         DamageTypes.RADIATION: lc('Inventory.client.RADIATION'),
         DamageTypes.PSY: lc('Inventory.client.PSY'),
         DamageTypes.BIO: lc('Inventory.client.BIO'),
         DamageTypes.AUDIO: lc('Inventory.client.ACOUSTIC'),
         DamageTypes.AUDIOSELF: lc('Inventory.client.SELF_ACOUSTIC'),
         DamageTypes.NIFF: lc('Inventory.client.NOTHING')}
        self.ReliabilityNames = {ItemsCatalog.RELIABILITY_LOW: lc('Inventory.client.LOW'),
         ItemsCatalog.RELIABILITY_AVARAGE: lc('Inventory.client.AVARAGE'),
         ItemsCatalog.RELIABILITY_MEDIUM: lc('Inventory.client.MEDIUM'),
         ItemsCatalog.RELIABILITY_HIGH: lc('Inventory.client.HIGH'),
         ItemsCatalog.RELIABILITY_MAX: lc('Inventory.client.MAXIMUM')}
        self.AccuracyVariancesNames = {ItemsCatalog.ACCURACY_LOW_VARIANCE_BORDER: lc('Inventory.client.LOW'),
         ItemsCatalog.ACCURACY_MEDIUM_VARIANCE_BORDER: lc('Inventory.client.AVARAGE'),
         ItemsCatalog.ACCURACY_HIGH_VARIANCE_BORDER: lc('Inventory.client.MEDIUM'),
         ItemsCatalog.ACCURACY_ULTRA_VARIANCE_BORDER: lc('Inventory.client.HIGH'),
         ItemsCatalog.ACCURACY_TEST_VARIANCE_BORDER: lc('Inventory.client.TEST')}
        self.AccuracyMoveLostNames = {ItemsCatalog.ACCURACY_LOW_MOVE_LOST: lc('Inventory.client.LOW'),
         ItemsCatalog.ACCURACY_MEDIUM_MOVE_LOST: lc('Inventory.client.MEDIUM'),
         ItemsCatalog.ACCURACY_HIGH_MOVE_LOST: lc('Inventory.client.MEDIUM'),
         ItemsCatalog.ACCURACY_ULTRA_MOVE_LOST: lc('Inventory.client.HIGH'),
         ItemsCatalog.ACCURACY_TEST_MOVE_LOST: lc('Inventory.client.TEST')}
        self.KickbackNames = {ItemsCatalog.ACCURACY_VERY_LOW_KICKBACK: lc('Inventory.client.VERY_LOW'),
         ItemsCatalog.ACCURACY_LOW_KICKBACK: lc('Inventory.client.LOW'),
         ItemsCatalog.ACCURACY_MEDIUM_KICKBACK: lc('Inventory.client.MEDIUM'),
         ItemsCatalog.ACCURACY_HIGH_KICKBACK: lc('Inventory.client.MEDIUM'),
         ItemsCatalog.ACCURACY_STRONG_KICKBACK: lc('Inventory.client.STRONG'),
         ItemsCatalog.ACCURACY_TEST_KICKBACK: lc('Inventory.client.TEST')}
        self.RecoilNames = {ItemsCatalog.ACCURACY_FAST_RECOIL: lc('Inventory.client.FAST'),
         ItemsCatalog.ACCURACY_MODERATE_RECOIL: lc('Inventory.client.MODERATE'),
         ItemsCatalog.ACCURACY_AVARAGE_RECOIL: lc('Inventory.client.AVARAGE'),
         ItemsCatalog.ACCURACY_SLOW_RECOIL: lc('Inventory.client.SLOW'),
         ItemsCatalog.ACCURACY_TEST_RECOIL: lc('Inventory.client.TEST')}
        self.BodyPartsNames = {FiringDefs.HEAD: lc('Inventory.client.HEAD'),
         FiringDefs.TORSO: lc('Inventory.client.TORSO'),
         FiringDefs.LEG_UPPER: lc('Inventory.client.LEG_UPPER'),
         FiringDefs.LEG_LOWER: lc('Inventory.client.LEG_LOWER'),
         FiringDefs.FACE: lc('Inventory.client.FACE'),
         FiringDefs.FOREARM: lc('Inventory.client.FOREARM'),
         FiringDefs.ARM: lc('Inventory.client.ARM'),
         FiringDefs.HEART: lc('Inventory.client.HEART'),
         FiringDefs.GROIN: lc('Inventory.client.GROIN')}
        self.WeaponMasteryNames = {ItemsCatalog.SKILL_LEVEL_BASIC: lc('Inventory.client.COMMON'),
         ItemsCatalog.SKILL_LEVEL_ADVANCED: lc('Inventory.client.RARE'),
         ItemsCatalog.SKILL_LEVEL_PROFESSIONAL: lc('Inventory.client.EXPERT')}
        perk_string_data = openLocalizeSection('PerkStrings')
        Perk_names = {}
        for entry in perk_string_data.items():
            if entry[0] == 'perk':
                Perk_names[entry[1]['id'].asInt] = [entry[1]['Name'].asString.decode('utf-8'), entry[1]['Description'].asString.decode('utf-8')]

        Perk_names[0] = [u'', u'']
        self.PerkNames = Perk_names

    def GetPerkText(self, tree_name, skill_name, feat_pos):
        perk_id = self.GetPerkID(tree_name, skill_name, feat_pos)
        if not perk_id:
            return u''
        perk = PerkCatalog.GetPerkByID(perk_id)
        string = self.GetPerkName(perk_id) + u'\n'
        string += lc('Inventory.client.COST').format(perk['Cost']) + u'\n'
        string += lc('Inventory.client.SKILL_LEVEL_CAP').format(perk['NeedSkillValue']) + u'\n'
        if perk.has_key('VisualValue'):
            value = perk['VisualValue']
        else:
            value = perk['Value']
        string += self.GetPerkDiscription(perk_id).replace('$value', str(value)) + u'\n'
        for prereq_perk_id in perk['Prerequisites']:
            string += lc('Inventory.client.REQUIRENMENTS') % self.GetPerkName(prereq_perk_id) + u'\n'

        return string

    def ToolTipEnable(self, id, interface_id, event):

        def GetItemString(item):

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

            item_type = item['complexItemType']
            item_param = ItemsCatalog.GetItemParam(item_type)
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_inconstant_param = ItemsUtils.GetComplexItemInconstanParams(item, self)
            string = self.GetItemName(item, item_inconstant_param)
            if item_class == ItemsCatalog.WEAPON:
                damage_add = lambda x, y: [x[0] + y[0], x[1] + y[1]]
                string += u'\n'
                loaded_munition_type = item_inconstant_param[ItemsCatalog.INC_LOADED_MUNITION_TYPE]
                loaded_munition_param = ItemsCatalog.GetItemParam(loaded_munition_type)
                main_damage_summary = copy(item_param['DamageMain'])
                add_damage_summary = copy(item_param['DamageAdditional'])
                penetration_summary = item_param['Penetration']
                if loaded_munition_param:
                    main_damage_summary = utils.add_dicts(main_damage_summary, loaded_munition_param['DamageMain'], damage_add)
                    add_damage_summary = utils.add_dicts(add_damage_summary, loaded_munition_param['DamageAdditional'], damage_add)
                    penetration_summary += loaded_munition_param['Penetration']
                string += self.GetPenetrationString(penetration_summary, lc('Inventory.client.PENETRATION_SUM'))
                string += self.GetDamageString(main_damage_summary, add_damage_summary)
                string += u'\n' + lc('Inventory.client.ADAPTATION').format(round(CharacterUtils.GetWeaponAdaptivity(self, item_type) * 100.0, 1))
                string += u'\n' + lc('Inventory.client.STATE').format(ItemsUtils.GetItemConditionPercentString(None, None, False, item_param, item_inconstant_param))
                if loaded_munition_type:
                    string += u'\n' + lc('Inventory.client.NUM_ARMED').format(item_inconstant_param[ItemsCatalog.INC_MUNITION_NUMBER]) + u' ' + ItemsUtils.GetItemName(loaded_munition_type)
                string += u'\n' + lc('Inventory.client.APPROXIMATE_COST').format(ItemsUtils.GetItemCost(item)) + lc('Inventory.client.ROUBLES')
                if item_inconstant_param[ItemsCatalog.INC_IS_BROKEN] > 0:
                    string += u'\n' + lc('Inventory.client.WEAPON_JAMMED')
            elif item_class == ItemsCatalog.CLOTH:
                string += u'\n' + lc('Inventory.client.STATE').format(ItemsUtils.GetItemConditionPercentString(None, None, False, item_param, item_inconstant_param))
                string += u'\n' + lc('Inventory.client.APPROXIMATE_COST').format(ItemsUtils.GetItemCost(item)) + lc('Inventory.client.ROUBLES')
                if item_inconstant_param[ItemsCatalog.INC_CONDITION_VALUE] == 0:
                    string += u'\n' + lc('Inventory.client.ITEM_BROKEN')
            elif item_class == ItemsCatalog.AMMO:
                string += u'\n' + lc('Inventory.client.NUMBER').format(item_inconstant_param[ItemsCatalog.INC_ROUND_NUMBER])
                string += u'\n' + lc('Inventory.client.APPROXIMATE_COST').format(ItemsUtils.GetItemCost(item)) + lc('Inventory.client.ROUBLES')
            elif item_class == ItemsCatalog.BUFF:
                if 'IsArtefactContainer' in item_param:
                    num_uses = item_inconstant_param.get(ItemsCatalog.INC_USES_CONTAINER_NUMBER, 0)
                    max_uses = item_param['MaxUseArtefact']
                    if num_uses > max_uses:
                        num_uses = max_uses
                    try:
                        string += u'\n' + lc('Inventory.client.NUM_USES_ARTEF_CONTAINER').format(max_uses - num_uses, max_uses)
                    except:
                        traceback.print_exc()
                        string += u'\n %s/%s' % (num_uses, max_uses)

                    if item['itemList']:
                        string += u'\n' + lc('Inventory.client.ARTEFACT_IN_CONTAINER') + '\n'
                        for sub_item in item['itemList']:
                            power_time = ItemsUtils.GetArtefactInContainerDepleetionTime(sub_item)
                            string += ' - ' + ItemsUtils.GetItemName(sub_item['itemType']) + ' : %s \n' % timeToString(power_time)

                    else:
                        string += u'\n' + lc('Inventory.client.ARTEFACT_IN_CONTAINER_EMPTY')
                else:
                    string += u'\n' + lc('Inventory.client.NUM_USES').format(item_inconstant_param[ItemsCatalog.INC_USES_NUMBER])
                string += u'\n' + lc('Inventory.client.APPROXIMATE_COST').format(ItemsUtils.GetItemCost(item)) + lc('Inventory.client.ROUBLES')
            elif item_class == ItemsCatalog.ARTIFACT:
                power_time = ItemsUtils.GetArtefactDepleetionTime(item, item_param, self.timeServerDiff)
                if power_time == None:
                    string += u'\n' + lc('Inventory.client.ARTIFACT_CHARGE_FULL')
                elif power_time < 0.0:
                    string += u'\n' + lc('Inventory.client.ARTIFACT_CHARGE_DEPLEETED')
                else:
                    string += u'\n' + lc('Inventory.client.ARTIFACT_CHARGE_REMAINING') % timeToString(power_time)
                string += u'\n' + lc('Inventory.client.APPROXIMATE_COST').format(ItemsUtils.GetItemCost(item)) + lc('Inventory.client.ROUBLES')
            else:
                string += u'\n' + lc('Inventory.client.APPROXIMATE_COST').format(ItemsUtils.GetItemCost(item)) + lc('Inventory.client.ROUBLES')
            if ItemsUtils.IsQuestItem(item, item_inconstant_param):
                quest_name = self.getQTitle(item_inconstant_param[ItemsCatalog.IS_QUEST_ITEM])
                if quest_name:
                    string += u'\n' + lc('Inventory.client.BELONGS_TO_QUEST') % quest_name
                else:
                    string += u'\n' + lc('Inventory.client.QUEST_ITEM')
            if ItemsUtils.IsPersonalItem(item, item_inconstant_param):
                string += u'\n' + lc('Inventory.client.PERSONAL_ITEM')
            item_ttl = ItemsUtils.GetItemDestroyTime(item, item_param)
            if item_ttl is not None:
                string += u'\n' + lc('Inventory.client.ITEM_TIME_TO_LIVE').format(timeToString(item_ttl))
            return string

        if id == None or event == None:
            return
        else:
            if event == soGUI.soToolTipComponent.EVENT_SHOW:
                if interface_id == BWPersonality.GUICore.GUI_ID_INVENTORY or interface_id == BWPersonality.GUICore.GUI_ID_CHARSCREEN:
                    if interface_id == BWPersonality.GUICore.GUI_ID_ITEMCACHE:
                        item = ItemsUtils.GetComplexItemByID(self, id)
                    else:
                        if isinstance(id, int):
                            return
                        item = id
                    if self.IsItemFake(item):
                        item_type = item['complexItemType']
                        if item_type == ItemsCatalog.ARTIFACT_ADD_BLANK['TypeID']:
                            string = lc('Inventory.client.ARTIFACT_UNLOCK')
                            BWPersonality.GUICore.showToolTip(colorCodes.tf3_regular_text_color + string, '')
                    elif item:
                        if self.ToolTipRepairIDFunc:
                            string = self.ToolTipRepairIDFunc(item)
                        else:
                            string = GetItemString(item)
                        BWPersonality.GUICore.showToolTip(colorCodes.tf3_regular_text_color + string, '')
                elif interface_id == BWPersonality.GUICore.GUI_ID_PCTRADE:
                    item = id[1]
                    source = id[0]
                    if item == None:
                        return
                    string = GetItemString(item)
                    BWPersonality.GUICore.showToolTip(colorCodes.tf3_regular_text_color + string, '')
                elif interface_id == BWPersonality.GUICore.GUI_ID_PACKAGESELL:
                    item = id
                    if self.IsItemFake(item):
                        item_type = item['complexItemType']
                        string = ItemsUtils.GetItemName(item_type, tintItem=item)
                    else:
                        string = GetItemString(item)
                    BWPersonality.GUICore.showToolTip(colorCodes.tf3_regular_text_color + string, '')
                elif interface_id == BWPersonality.GUICore.GUI_ID_ACTIONBAR:
                    bar_slot = self.quickSlotBar[self.quickSlotActiveLineNumber - 1][id]
                    if bar_slot[QUICK_TYPE_POS] == QUICK_BAR_ITEM:
                        item_id = bar_slot[QUICK_DATA_POS]
                        item = ItemsUtils.GetComplexItemByID(self, item_id)
                        if item:
                            string = GetItemString(item)
                            BWPersonality.GUICore.showToolTip(colorCodes.tf3_regular_text_color + string, '')
                elif interface_id == BWPersonality.GUICore.GUI_ID_SKILLS:
                    string = self.GetPerkText(id[0], id[1], id[2])
                    if string:
                        BWPersonality.GUICore.showToolTip(colorCodes.tf3_regular_text_color + string, '')
                elif interface_id == BWPersonality.GUICore.GUI_ID_NPCTRADE:
                    item = id[0]
                    if item:
                        if id[0] == NPC_VENDOR.UPPER_REGION or self.TradeMode == soGUI.soNPCTradeGUI.MODE_BUY:
                            item_type = item['complexItemType']
                            string = ItemsUtils.GetItemName(item_type, tintItem=item) + u'\n'
                            try:
                                trader = BigWorld.entities[self.TraderID]
                            except:
                                return

                            trade_entry = ItemsUtils.GetTraderAssortmentEntry(trader, item_type)
                            if trade_entry == None:
                                print 'entry is none', trader, self.TraderID
                                return
                            if trade_entry['Number'] != ItemsCatalog.INFINITY:
                                string += lc('Inventory.client.NUMBER').format(trade_entry['Number']) + u'\n'
                            else:
                                string += lc('Inventory.client.NUMBER_INFIFNITY') + u'\n'
                            sell_cost = ItemsUtils.GetTraderSellCost(trade_entry)
                            cost_string = u''
                            if sell_cost[ItemsUtils.COST_CREDIT] > 0:
                                cost_string += str(sell_cost[ItemsUtils.COST_CREDIT]) + lc('Inventory.client.ROUBLES_FULL') + u'\n'
                            if sell_cost[ItemsUtils.COST_GOLD] > 0:
                                cost_string += str(sell_cost[ItemsUtils.COST_GOLD]) + lc('Inventory.client.GOLD_FULL') + u'\n'
                            string += lc('Inventory.client.COST').format(cost_string)
                            if trader.pMoney != ItemsCatalog.INFINITY:
                                string += lc('Inventory.client.TRADER_NUM_MONEY').format(trader.pMoney) + lc('Inventory.client.ROUBLES')
                        else:
                            string = GetItemString(item)
                    else:
                        string = u''
                    BWPersonality.GUICore.showToolTip(colorCodes.tf3_regular_text_color + string, '')
                elif interface_id == BWPersonality.GUICore.GUI_ID_PDAMAP:
                    if type(id) == unicode:
                        BWPersonality.GUICore.showToolTip(colorCodes.tf3_regular_text_color + id, '')
                    else:
                        BWPersonality.GUICore.showToolTip(colorCodes.tf3_regular_text_color + self.getMapNoteText(id), '')
            return

    def InitTrade(self):
        self.TraderID = 0
        self.TraderAssortment = None
        self.ClearTrade()
        BWPersonality.GUICore.showTrade(False)
        return

    def ClearTrade(self):
        self.ToSellList = []
        self.ToBuyList = []
        self.TradeMode = soGUI.soNPCTradeGUI.MODE_BUY

    def MoveToBuy(self, item_type):
        if len(self.ToBuyList) <= ItemsUtils.MAX_ITEMS_TO_TRADE:
            try:
                trader = BigWorld.entities[self.TraderID]
            except:
                print 'no trader'
                return

            trade_item_type = item_type['complexItemType']
            trade_entry = ItemsUtils.GetTraderAssortmentEntry(trader, trade_item_type)
            if not trade_entry:
                trade_entry = ItemsUtils.GetTraderAssortmentEntryByClanID(trader, trade_item_type, self.cellClanID)
                if not trade_entry:
                    print 'no trade ware entry by clan'
                    return
            num_ware = trade_entry['Number']
            print 'num_ware', num_ware
            if num_ware != ItemsCatalog.INFINITY:
                filter_function = lambda list_item: list_item['complexItemType'] == trade_item_type
                if len(filter(filter_function, self.ToBuyList)) >= num_ware:
                    return
            self.ToBuyList.append(item_type)
        if self.TradeMode != soGUI.soNPCTradeGUI.MODE_BUY:
            self.TradeMode = soGUI.soNPCTradeGUI.MODE_BUY
            self.ClearSell()

    def MoveToSell(self, item_id):
        if item_id not in self.ToSellList:
            if len(self.ToSellList) <= ItemsUtils.MAX_ITEMS_TO_TRADE:
                self.ToSellList.append(item_id)
        if self.TradeMode != soGUI.soNPCTradeGUI.MODE_SELL:
            self.TradeMode = soGUI.soNPCTradeGUI.MODE_SELL
            self.ClearBuy()

    def DoTrade(self):
        print 'DoTrade::', self.TradeMode, soGUI.soNPCTradeGUI.MODE_SELL
        if self.TradeMode == soGUI.soNPCTradeGUI.MODE_SELL:
            for item in self.ToSellList:
                trader_id = self.TraderID
                gold_item_cost = ItemsUtils.GetGoldItemCost(item)
                can_be_sold_for_gold = ItemsCatalog.GetItemParam(item['complexItemType']).get('SoldForGold', 0)
                if gold_item_cost > 0 and not can_be_sold_for_gold:

                    def SellGoldCallback(event, data):
                        if event == MESSAGEBOX.EVENT_BTNPRESS:
                            if data['btn'] == MESSAGEBOX.BTN_YES:
                                self.SellItem(trader_id, item)

                    msgbox_templates.ask_yes_no('Inventory.DoTrade', lc('Common.Messages.GOLD_SELL_TITLE'), lc('Common.Messages.GOLD_SELL_MESSAGE'), callback=SellGoldCallback)
                else:
                    self.SellItem(trader_id, item)

        elif ItemsUtils.CheckMaxItemNumber(self, len(self.ToBuyList)):
            for item in self.ToBuyList:
                self.BuyItem(self.TraderID, item, item.get('forGold', 0))
                print 'DoTrade::--BuyItem, ', self.TraderID, item

        else:
            self.ReportFail(ItemsUtils.FAIL_MAX_ITEMS)
            print 'DoTrade::--ReportFail, ItemsUtils.FAIL_MAX_ITEMS', ItemsUtils.FAIL_MAX_ITEMS
            return
        self.ClearTrade()

    def CancelBuy(self, item):
        if item in self.ToBuyList:
            self.ToBuyList.remove(item)

    def CancelSell(self, item):
        if item in self.ToSellList:
            self.ToSellList.remove(item)

    def ClearBuy(self):
        self.ToBuyList = []

    def ClearSell(self):
        self.ToSellList = []

    def chandeSellMode(self, mode):
        if self.SellMode == NPC_VENDOR.MODE_SELL_FOR_MONEY:
            ItemsUtils.BY_FOR_GOLD = 0
        elif self.SellMode == NPC_VENDOR.MODE_SELL_FOR_GOLD:
            ItemsUtils.BY_FOR_GOLD = 1

    def tradeEvent(self, action, item):
        if action == NPC_VENDOR.EVENT_WANNASELL:
            self.MoveToSell(item)
        elif action == NPC_VENDOR.EVENT_WANNABUY:
            self.MoveToBuy(item)
        elif action == NPC_VENDOR.EVENT_ACTION:
            if item[1] == NPC_VENDOR.UPPER_REGION:
                self.MoveToBuy(item[0])
        elif action == NPC_VENDOR.EVENT_FILTER:
            self.SetTradeFilter(item)
        elif action == NPC_VENDOR.EVENT_CANCEL:
            if self.TradeMode == soGUI.soNPCTradeGUI.MODE_BUY:
                self.CancelBuy(item)
            elif self.TradeMode == soGUI.soNPCTradeGUI.MODE_SELL:
                self.CancelSell(item)
        elif action == NPC_VENDOR.EVENT_SELL_MODE:
            self.SellMode = item
            self.chandeSellMode(action)
        elif action == NPC_VENDOR.EVENT_CLEAR:
            self.ClearTrade()
        elif action == NPC_VENDOR.EVENT_MODE:
            if self.TradeMode == soGUI.soNPCTradeGUI.MODE_BUY:
                self.ClearBuy()
            elif self.TradeMode == soGUI.soNPCTradeGUI.MODE_SELL:
                self.ClearSell()
            self.TradeMode = item
        elif action == NPC_VENDOR.EVENT_APPLY:
            self.DoTrade()
        elif action == NPC_VENDOR.EVENT_CONTEXT:
            self.context_menu_item = item
            actions = self.GetTradeContextActions()
            self.StartInventoryContextMenu(actions, BWPersonality.GUICore.GUI_ID_NPCTRADE)
        self.UpdateTradeInterface()
        self.UpdateInventory()

    def ItemLocked(self, item):
        if item:
            if isinstance(item, int):
                return False
            id = item['complexItemID']
            if item['fromEntityID']:
                return True
            for sell_item in self.ToSellList:
                if id == sell_item['complexItemID']:
                    return True

            if id in self.craftItemList:
                return True
            if id in self.NPCBarterItemList:
                return True
            if id in self.items_to_drop:
                return True
            for item in self.ExchangeProperties.ItemsToExchange:
                if id == item.complexItemID:
                    return True

            for item in self.PCTradeItems:
                if id == item['complexItemID']:
                    return True

        return False

    def ItemLockedByShop(self, item):
        if item:
            if isinstance(item, int):
                return False
            id = item['complexItemID']
            if id in self.StoredItemsInShop:
                return True
        return False

    def UpdateTradeInterface(self):
        try:
            trader_entity = BigWorld.entities[self.TraderID]
        except KeyError:
            return

        items_list = []
        cost_str = {}

        def setForGold(entry, forGold):
            entry = dict(entry)
            entry['forGold'] = forGold
            return entry

        forGold = 0
        if self.SellMode == NPC_VENDOR.MODE_SELL_FOR_MONEY:
            assort = [ setForGold(z, 0) for z in trader_entity.Assortment ]
            if self.isCanBuyInClanShop:
                assort.extend(map(lambda x: setForGold(x, 0), filter(lambda x: ItemsUtils.CanItemBeBoughtForGold(x['Type']) == 0, ItemsUtils.getTraderAssortmentByClanID(self, trader_entity))))
        elif self.SellMode == NPC_VENDOR.MODE_SELL_FOR_GOLD:
            forGold = 1
            assort = [ setForGold(z, 1) for z in trader_entity.donateAssortment ]
            if self.isCanBuyInClanShop:
                assort.extend(map(lambda x: setForGold(x, 1), filter(lambda x: ItemsUtils.CanItemBeBoughtForGold(x['Type']) == 1, ItemsUtils.getTraderAssortmentByClanID(self, trader_entity))))
            if hasattr(trader_entity, 'for_gold_item_list'):
                for typeID in trader_entity.for_gold_item_list:
                    entry = {'Type': typeID,
                     'MarginSell': 0,
                     'MarginBuy': 0,
                     'BuyOnly': 0,
                     'SellOnly': 0,
                     'Number': ItemsCatalog.INFINITY,
                     'ResupplyNumber': 0,
                     'forGold': 1}
                    assort.append(entry)

        assort = [ dict(entr) for entr in assort ]
        for entry in assort:
            if not entry['BuyOnly']:
                curr_selling_item_cost = ItemsUtils.GetTraderSellCost(entry, forGold)
                item_cost_string = u''
                if curr_selling_item_cost[ItemsUtils.COST_CREDIT] > 0:
                    item_cost_string = str(curr_selling_item_cost[ItemsUtils.COST_CREDIT]) + lc('Inventory.client.ROUBLES')
                if curr_selling_item_cost[ItemsUtils.COST_GOLD] > 0:
                    item_cost_string += str(curr_selling_item_cost[ItemsUtils.COST_GOLD]) + lc('Inventory.client.GOLD')
                try:
                    items_list.append(self.CreateFakeItem(entry['Type'], entry.get('forGold')))
                except:
                    print 'ENTRY:', (entry,)

                cost_str[entry['Type']] = item_cost_string

        wares_ids = []
        wares_ids_tmp = self.itemFilterFunction(items_list, None, self.tradeFilter)
        for item in wares_ids_tmp:
            wares_ids.append((item, cost_str.get(item['complexItemType'], u'?')))

        self.TraderAssortment = wares_ids
        if self.TradeMode == soGUI.soNPCTradeGUI.MODE_BUY:
            show_list = self.ToBuyList
            get_entry_func = partial(ItemsUtils.GetTraderAssortmentEntry, trader_entity, clanid=self.cellClanID)
            cost_func = lambda c: ItemsUtils.GetTraderSellCost(get_entry_func(c['complexItemType']), c.get('forGold'))
        else:
            show_list = self.ToSellList
            cost_func = lambda c: ItemsUtils.GetTraderBuyCost(c, self, trader_entity)
        total_cost = [0, 0]
        for curr_item in show_list:
            item_cost = cost_func(curr_item)
            total_cost[ItemsUtils.COST_CREDIT] += item_cost[ItemsUtils.COST_CREDIT]
            total_cost[ItemsUtils.COST_GOLD] += item_cost[ItemsUtils.COST_GOLD]

        total_cost_string = str(round(total_cost[ItemsUtils.COST_CREDIT], 2)) + lc('Inventory.client.ROUBLES_FULL')
        if total_cost[ItemsUtils.COST_GOLD] > 0:
            total_cost_string += str(round(total_cost[ItemsUtils.COST_GOLD], 2)) + lc('Inventory.client.GOLD_FULL')
        BWPersonality.GUICore.setTradeData({'items': wares_ids,
         'transit': show_list,
         'mode': self.TradeMode,
         'outcome': total_cost_string})
        return

    def StartTrading(self, trader_assortment, trader_id):
        BWPersonality.GUICore.showInventory()
        BWPersonality.GUICore.showTrade()
        self.TraderAssortment = trader_assortment
        self.TraderID = trader_id
        self.ClearTrade()
        self.UpdateTradeInterface()

    def NPCRepairTooltip(self, item):
        try:
            trader_entity = BigWorld.entities[self.TraderID]
        except KeyError:
            trader_entity = None

        repair_cost, margin = ItemsUtils.GetRepairCost(item, self, trader_entity)
        if repair_cost:
            string = u'\n' + lc('Inventory.client.REPAIR_COST').format(repair_cost)
        else:
            string = u'\n' + lc('Inventory.client.REPAIR_NOT_NEEDED')
        return string

    def PlayerRepairTooltip(self, item):
        repair_cost, margin = ItemsUtils.GetRepairCost(item, self)
        if repair_cost:
            string = lc('Inventory.client.MAY_BE_REAPIRED')
        else:
            string = lc('Inventory.client.REPAIR_NOT_NEEDED')
        return string

    def StartNPCRepair(self, trader_id):
        self.TraderID = trader_id
        func = partial(self.NPCRepair, self.TraderID)
        self.AddNeededRepairIdFunc(func, self.NPCRepairTooltip)

    def ChooseRepairItem(self, repair_kit_id):
        func = partial(self.StartItemRepair, repair_kit_id)
        self.AddNeededRepairIdFunc(func, self.PlayerRepairTooltip)

    def AddNeededRepairIdFunc(self, func, tooltip_func):
        self.NeededRepairIDFunc = func
        self.ToolTipRepairIDFunc = tooltip_func
        BWPersonality.GUICore.showInventory()
        BWPersonality.GUICore.showRepairMode(True)

    def ThrowRepairID(self, id):
        func = self.NeededRepairIDFunc
        func(id)
        self.NeededRepairIDFunc = None
        self.ToolTipRepairIDFunc = None
        return

    def GetTraderName(self, trader_id):
        try:
            trader_entity = BigWorld.entities[trader_id]
        except:
            return u''

        return trader_entity.npcName

    def GetStoresItems(self, trader_name):
        for entry in self.StoredItems:
            if entry.TraderName == trader_name:
                return entry.Items

        return []

    def GetContainerStoresItems(self, trader_entity):
        return trader_entity.CarryingItems

    def StartItemCache(self, object_id, cache_mode):
        self.cacheObjectID = object_id
        self.cacheMode = cache_mode
        if cache_mode == ItemsUtils.CACHE_MODE_USERFIRE:
            BWPersonality.GUICore.showUserFire(True, object_id)
        elif cache_mode == ItemsUtils.CACHE_MODE_WAREHOUSE:
            BWPersonality.GUICore.showWarehouse(True, object_id)
            trader = BigWorld.entities[self.cacheObjectID]
            BigWorld.player().getWarehouseData(trader.id)
        else:
            print 'OPEN WAREHOUSE'
            BWPersonality.GUICore.showItemCache(True, cache_mode)
        BWPersonality.GUICore.showInventory()
        self.NeedToUpdateItemCache()

    def RedrawItemCache(self):
        if self.cacheMode == ItemsUtils.CACHE_MODE_SAFEBOX:
            trader_name = self.GetTraderName(self.cacheObjectID)
            item_list = self.GetStoresItems(trader_name)
            StoredItemsInShop = self.StoredItemsInShop[:]
            item_list = self.itemFilterFunction(item_list, None, self.itemcacheFilter)
            BWPersonality.GUICore.setItemCacheData({'items': item_list,
             'caption': lc('Inventory.client.ItemStorage'),
             'filters': self.itemcacheFilter,
             'slots_string': str(len(item_list)) + u'/' + str(self.GetMaxItemStorageNumber(trader_name))})
        elif self.cacheMode == ItemsUtils.CACHE_MODE_CONTAIER:
            try:
                container_entity = BigWorld.entities[self.cacheObjectID]
            except:
                item_list = []
            else:
                item_list = self.GetContainerStoresItems(container_entity)

            item_list = self.itemFilterFunction(item_list, None, self.itemcacheFilter)
            BWPersonality.GUICore.setItemCacheData({'items': item_list,
             'caption': container_entity.name,
             'filters': self.itemcacheFilter})
        elif self.cacheMode == ItemsUtils.CACHE_MODE_USERFIRE:
            try:
                container_entity = BigWorld.entities[self.cacheObjectID]
            except:
                item_list = []
            else:
                item_list = self.GetContainerStoresItems(container_entity)

            BWPersonality.GUICore.setItemCacheDataUserFire({'items': item_list,
             'caption': container_entity.name,
             'filters': self.itemcacheFilter})
        elif self.cacheMode == ItemsUtils.CACHE_MODE_WAREHOUSE:
            trader = BigWorld.entities[self.cacheObjectID]
            warehouse_data = trader.getStoredItems(BigWorld.player().clanID)
            if warehouse_data:
                data = dict(items=warehouse_data.storedItems, money=warehouse_data.money, gold=warehouse_data.gold, filters=self.itemcacheFilter)
                BWPersonality.GUICore.setWarehouseData(data)
        return

    def EndTrading(self):
        self.TraderID = None
        self.TraderAssortment = None
        return

    def GetItemActions(self, item):
        returning_list = {ItemsCatalog.CAN_DROP: lc('Inventory.client.DROP'),
         ItemsCatalog.CAN_INFO: lc('Inventory.client.INFO')}
        item_type = item['complexItemType']
        item_class = ItemsCatalog.GetItemClass(item_type)
        if item_class in [ItemsCatalog.WEAPON, ItemsCatalog.CLOTH]:
            returning_list[ItemsCatalog.CAN_PUT_ON] = lc('Inventory.client.EQUIP')
            returning_list[ItemsCatalog.CAN_REPAIR] = lc('Inventory.client.REPAIR')
            for sub_item in item['itemList']:
                returning_list[sub_item['itemID']] = lc('Inventory.client.REMOVE') + ItemsUtils.GetItemName(sub_item['itemType'], tintItem=item)

        elif item_class == ItemsCatalog.BUFF:
            param = ItemsCatalog.GetItemParam(item_type)
            if 'IsArtefactContainer' in param and param['IsArtefactContainer']:
                for sub_item in item['itemList']:
                    returning_list[sub_item['itemID']] = lc('Inventory.client.EXTRACT') + ' : ' + ItemsUtils.GetItemName(sub_item['itemType'])

            else:
                returning_list[ItemsCatalog.CAN_USE] = lc('Inventory.client.USE')
                if param['CanUseOnTarget']:
                    returning_list[ItemsCatalog.CAN_USE_ON_TARGET] = lc('Inventory.client.USE_ON_TARGET')
        elif item_class == ItemsCatalog.AMMO:
            returning_list[ItemsCatalog.CAN_LOAD_IN_WEAPON] = lc('Inventory.client.LOAD_AMMO')
            item_inconstant_param = ItemsUtils.GetComplexItemInconstanParams(item)
            if item_inconstant_param[ItemsCatalog.INC_ROUND_NUMBER] > 1:
                returning_list[ItemsCatalog.CAN_SPARE] = lc('Inventory.client.DIVIDE')
        elif item_class in [ItemsCatalog.EXPLOSION]:
            returning_list[ItemsCatalog.CAN_EQUIP] = lc('Inventory.client.EQUIP')
            item_inconstant_param = ItemsUtils.GetComplexItemInconstanParams(item)
            if item_inconstant_param[ItemsCatalog.INC_ROUND_NUMBER] > 1:
                returning_list[ItemsCatalog.CAN_SPARE] = lc('Inventory.client.DIVIDE')
        elif item_class in [ItemsCatalog.GADGET]:
            param = ItemsCatalog.GetItemParam(item_type)
            if ItemsUtils.IsItemEquipable(None, param):
                returning_list[ItemsCatalog.CAN_PUT_ON] = lc('Inventory.client.EQUIP')
            if param['Action'] != ItemsCatalog.GADJET_ACTION_NONE:
                returning_list[ItemsCatalog.CAN_USE] = lc('Inventory.client.USE')
        elif item_class == ItemsCatalog.LOOT:
            item_inconstant_param = ItemsUtils.GetComplexItemInconstanParams(item)
            param = ItemsCatalog.GetItemParam(item_type)
            if 'CanUse' in param and param['CanUse']:
                returning_list[ItemsCatalog.CAN_USE] = lc('Inventory.client.USE')
            if 'CanUseOnTarget' in param and param['CanUseOnTarget']:
                returning_list[ItemsCatalog.CAN_USE_ON_TARGET] = lc('Inventory.client.USE_ON_TARGET')
            if item_inconstant_param[ItemsCatalog.INC_WARE_NUMBER] > 1:
                returning_list[ItemsCatalog.CAN_SPARE] = lc('Inventory.client.DIVIDE')
        item_quest_id = ItemsUtils.GetQuestItemID(item)
        if item_quest_id > 0:
            action_text = self.GetQuestItemActionText(item_type, item_quest_id)
            if action_text:
                returning_list[ItemsCatalog.CAN_QUEST] = action_text
        return returning_list

    def GetBodyPartName(self, key):
        return self.BodyPartsNames[key]

    def GetDamageName(self, key):
        return self.DamageNames[key]

    def GetReliabilityName(self, key):
        return self.ReliabilityNames[key]

    def GetAccuracyVariancesName(self, key):
        return self.AccuracyVariancesNames[key]

    def GetAccuracyMoveLostName(self, key):
        return self.AccuracyMoveLostNames[key]

    def GetKickbackName(self, key):
        return self.KickbackNames[key]

    def GetRecoilName(self, key):
        return self.RecoilNames[key]

    def GetWeaponMasteryName(self, key):
        return self.WeaponMasteryNames[key]

    def GetPenetrationString(self, peneration, core_penetration_string):
        if peneration == FiringDefs.BASE_PENETRATION:
            add_str = lc('Inventory.client.PENETRATION_100')
        elif peneration < FiringDefs.BASE_PENETRATION:
            add_str = lc('Inventory.client.PENETRATION_MORE_100').format(FiringDefs.BASE_PENETRATION - peneration)
        else:
            add_str = lc('Inventory.client.PENETRATION_LESS_100').format(peneration - FiringDefs.BASE_PENETRATION)
        text = core_penetration_string.format(peneration, add_str) + u'\n'
        return text

    def GetDamageString(self, damageMain, damageAdditional):
        text = u''
        damage_str = u''
        for key in damageMain.keys():
            damage_str += self.GetDamageName(key) + u' ' + lc('Inventory.client.FROM_TO').format(damageMain[key][0], damageMain[key][1]) + u'; '

        text += lc('Inventory.client.MAIN_DAMAGE').format(damage_str)
        text += u'\n'
        damage_str = u''
        for key in damageAdditional.keys():
            damage_str += self.GetDamageName(key) + u' ' + lc('Inventory.client.FROM_TO').format(damageAdditional[key][0], damageAdditional[key][1]) + u'; '

        text += lc('Inventory.client.ADDITIONAL_DAMAGE').format(damage_str)
        return text

    def GetItemInfoText(self, item_type, item = None):
        text = u''
        if item != None:
            text += self.GetItemName(item) + u'\n'
        else:
            text += ItemsUtils.GetItemName(item_type) + u'\n'
        item_class = ItemsCatalog.GetItemClass(item_type)
        item_param = ItemsCatalog.GetItemParam(item_type)
        FireWood = item_param.get('FireWood', None)
        CookingTime = item_param.get('CookingTime', None)
        CookingTo = item_param.get('CookingTo', None)
        if FireWood:
            text += lc('Inventory.client.FireWood').format(FireWood) + u'\n'
        if CookingTime:
            text += lc('Inventory.client.CookingTime').format(CookingTime) + u'\n'
        if CookingTo:
            text += lc('Inventory.client.CookingTo').format(ItemsUtils.GetItemName(CookingTo)) + u'\n'
        if item_class == ItemsCatalog.WEAPON:
            text += lc('Inventory.client.LEVEL').format(item_param['Level']) + u'\n'
            text += self.GetPenetrationString(item_param['Penetration'], lc('Inventory.client.PENETRATION'))
            text += self.GetDamageString(item_param['DamageMain'], item_param['DamageAdditional'])
            text += u'\n'
            text += lc('Inventory.client.RANGE').format(item_param['Range']) + u'\n'
            text += lc('Inventory.client.WEIGHT').format(item_param['Weight']) + u'\n'
            text += lc('Inventory.client.ACCURACY').format(item_param['Accuracy']) + u'\n'
            text += lc('Inventory.client.FIRE_RATE').format(item_param['RateOfFire']) + u'\n'
            text += lc('Inventory.client.FAIL_TOLERANCE') % self.GetReliabilityName(item_param['FailTolerance']) + u'\n'
            text += lc('Inventory.client.ACCURACY_BORDER') % self.GetAccuracyVariancesName(item_param['AccuracyBorder']) + u'\n'
            text += lc('Inventory.client.MOVE_ACCURACY_LOST') % self.GetAccuracyMoveLostName(item_param['MoveAccuracyLost']) + u'\n'
            text += lc('Inventory.client.KICKBACK') % self.GetKickbackName(item_param['Kickback']) + u'\n'
            text += lc('Inventory.client.ACURACY_RECOIL') % self.GetRecoilName(item_param['AccuracyRecoil']) + u'\n'
            text += lc('Inventory.client.SKILL_LEVEL') % self.GetWeaponMasteryName(item_param['SkillLevel']) + u'\n'
            text += lc('Inventory.client.NUM_AMMO_IN_MAGAZINE').format(item_param['AmmoCapacity']) + u'\n'
            used_text = u''
            ammo_type = item_param['AmmoType']
            for ammo in ItemsCatalog.AMMOS:
                ammo_param = ItemsCatalog.GetItemParam(ammo)
                if ammo_param['AmmoType'] == ammo_type:
                    used_text += ItemsUtils.GetItemName(ammo_param['TypeID']) + u'; '

            text += lc('Inventory.client.AMMO_USES').format(used_text)
            text += u'\n'
            install_str = u''
            for part_type in item_param['PartsCanUse']:
                install_str += ItemsUtils.GetItemName(part_type) + u'; '

            text += lc('Inventory.client.CAN_INSTALL').format(install_str)
            text += u'\n'
            text += lc('Inventory.client.COST').format(item_param['Cost']) + u'\n'
        if item_class == ItemsCatalog.CLOTH:
            text += lc('Inventory.client.LEVEL').format(item_param['Level']) + u'\n'
            text += lc('Inventory.client.DEFENCE') + u'\n'
            for body_part in item_param['Defence'].keys():
                text += '| ' + self.GetBodyPartName(body_part) + u' : \n'
                part_defence_dict = item_param['Defence'][body_part]
                for key in part_defence_dict:
                    text += u'|   + ' + self.GetDamageName(key) + u' : ' + str(part_defence_dict[key] / 10) + '%\n'

                text += u'\n'

            text += lc('Inventory.client.WEIGHT').format(item_param['Weight']) + u'\n'
            text += lc('Inventory.client.COST').format(item_param['Cost']) + u'\n'
        if item_class == ItemsCatalog.AMMO:
            text += lc('Inventory.client.LEVEL').format(item_param['Level']) + u'\n'
            text += self.GetPenetrationString(item_param['Penetration'], lc('Inventory.client.PENETRATION'))
            text += self.GetDamageString(item_param['DamageMain'], item_param['DamageAdditional'])
            text += u'\n'
            text += lc('Inventory.client.NUM_AMMO_IN_PACK').format(item_param['PackageSize']) + u'\n'
            used_text = u''
            ammo_type = item_param['AmmoType']
            for weapon in ItemsCatalog.WEAPONS:
                weapon_param = ItemsCatalog.GetItemParam(weapon)
                if weapon_param['AmmoType'] == ammo_type:
                    used_text += ItemsUtils.GetItemName(weapon_param['TypeID']) + u'; '

            text += lc('Inventory.client.MAY_BE_USED_BY').format(used_text)
            text += u'\n'
            text += lc('Inventory.client.WEIGHT').format(item_param['Weight']) + u'\n'
            text += lc('Inventory.client.COST').format(item_param['Cost']) + u'\n'
        if item_class == ItemsCatalog.BUFF:
            text += self.GetReceiptInfo(item_param)
            text += lc('Inventory.client.LEVEL').format(item_param['Level']) + u'\n'
            text += lc('Inventory.client.WEIGHT').format(item_param['Weight']) + u'\n'
            text += lc('Inventory.client.COST').format(item_param['Cost']) + u'\n'
        if item_class in [ItemsCatalog.EXPLOSION]:
            text += lc('Inventory.client.LEVEL').format(item_param['Level']) + u'\n'
            text += self.GetPenetrationString(item_param['Penetration'], lc('Inventory.client.PENETRATION'))
            text += self.GetDamageString(item_param['DamageMain'], item_param['DamageAdditional'])
            text += u'\n'
            text += lc('Inventory.client.NUM_PIECES').format(item_param['NumPieces']) + u'\n'
            text += lc('Inventory.client.WAVE_RADIUS').format(item_param['WaveRadius']) + u'\n'
            text += lc('Inventory.client.WEIGHT').format(item_param['Weight']) + u'\n'
            text += lc('Inventory.client.COST').format(item_param['Cost']) + u'\n'
        if item_class in [ItemsCatalog.GADGET]:
            text += lc('Inventory.client.LEVEL').format(item_param['Level']) + u'\n'
            text += lc('Inventory.client.WEIGHT').format(item_param['Weight']) + u'\n'
            text += lc('Inventory.client.COST').format(item_param['Cost']) + u'\n'
        if item_class == ItemsCatalog.LOOT:
            text += lc('Inventory.client.LEVEL').format(item_param['Level']) + u'\n'
            text += lc('Inventory.client.WEIGHT').format(item_param['Weight']) + u'\n'
            text += lc('Inventory.client.COST').format(item_param['Cost']) + u'\n'
        if item != None:
            text += self.GetItemDescription(item) + u'\n'
        else:
            text += ItemsUtils.GetItemDescription(item_type)
        return text

    def GetReceiptInfo(self, item_param):
        text = u''
        needWorkbenchType = item_param.get('needWorkbenchType', None)
        if needWorkbenchType:
            text += lc('Inventory.client.needWorkbenchType').format(WorkbenchUtil.getName(needWorkbenchType)) + u'\n'
        if item_param.has_key('NeededResourcess'):
            resource_string = u'\n'
            for item_type, number in item_param['NeededResourcess'].items():
                resource_string += '   ' + ItemsUtils.GetItemName(item_type) + ' : ' + str(number) + ';\n'

            text += lc('Inventory.client.NEEDED_RESOURCES').format(resource_string) + u'\n'
        if item_param.has_key('NeededSkill'):
            needed_skill_string = u'\n'
            for skill_name, value in item_param['NeededSkill'].items():
                needed_skill_string += '   ' + CharacterUtils.GetSkillFriendlyName(skill_name) + ' : ' + str(value) + ';\n'

            text += lc('Inventory.client.NEEDED_SKILLS').format(needed_skill_string) + u'\n'
        if item_param.has_key('CraftChance'):
            text += lc('Inventory.client.SUCCES_CHANCE').format(item_param['CraftChance']) + u'\n'
        return text

    def ContextMenuEvent(self, interface_id, id, caption, event):
        try:
            if interface_id not in [BWPersonality.GUICore.GUI_ID_PDAMAP, BWPersonality.GUICore.GUI_ID_INVENTORY, BWPersonality.GUICore.GUI_ID_NPCTRADE]:
                return
            if self.isDestroyed:
                return
            if event == soGUI.soContextMenuComponent.EVENT_SELECT:
                item = self.context_menu_item
                if id == ItemsCatalog.CAN_PUT_ON:
                    self.putOnItem(item)
                elif id == ItemsCatalog.CAN_USE:
                    self.useItem(item)
                elif id == ItemsCatalog.CAN_USE_ON_TARGET:
                    self.useItemOnTarget(item['complexItemID'])
                elif id == ItemsCatalog.CAN_DROP:
                    self.InventoryDropItem(item)
                elif id == ItemsCatalog.CAN_REPAIR:
                    self.StartItemRepair(0, item['complexItemID'])
                elif id == ItemsCatalog.CAN_INFO:
                    info_text = self.GetItemInfoText(item['complexItemType'], item)
                    msgbox_templates.text_and_ok('Inventory.ItemInfo', lc('Inventory.client.INFO'), colorCodes.tf3_regular_text_color + info_text)
                elif id == ItemsCatalog.CAN_LOAD_IN_WEAPON:
                    self.LoadAmmoInCurrentWeapon(item['complexItemID'])
                elif id == ItemsCatalog.CAN_UNLOAD:
                    pass
                elif id == ItemsCatalog.CAN_SPARE:

                    def number_check(newStr, wholeText, offset):
                        full_text = wholeText[0:offset] + newStr + wholeText[offset:]
                        if not full_text.isdigit():
                            return False
                        if wholeText:
                            if int(full_text) <= ItemsUtils.GetItemNumber(item):
                                return True
                            return False
                        return True

                    msgbox_templates.input_box_ok_cancel('Inventory.SpareCalback', lc('Inventory.client.DIVIDE_PROCESS'), colorCodes.tf3_regular_text_color + lc('Inventory.client.HOW_MUCH_ITEMS_DEVIDE'), callback=self.SpareCalback, default='1', input_validator=number_check)
                elif id == ItemsCatalog.CAN_EQUIP:
                    self.equipItem(item)
                elif id >= ItemsCatalog.MAX_ITEM_NUMBER:
                    self.DatachItem(item['complexItemID'], id)
                elif id == ItemsCatalog.CAN_ADD_MARK:
                    self.AddCustomGPSMark(item)
                elif id == ItemsCatalog.CAN_DELETE_MARK:
                    self.DeleteCustomGPSMark(item)
                elif id == ItemsCatalog.CAN_REPORT_BUG:
                    self.reportBugEvent(item)
                else:
                    if id == ItemsCatalog.CAN_TELEPORT:
                        position = self.GPSProvider.GetObjectAbsouluteCoords(self.context_menu_item[0][0], self.context_menu_item[0][1], self.context_menu_item[1])
                        BWPersonality.game.JumpToNextSpace(position, soGUI.soGPSMap.currentMap)
                        return
                    if id == ItemsCatalog.CAN_INFO_TRADE:
                        info_text = self.GetItemInfoText(item['complexItemType'])
                        msgbox_templates.text_and_ok('Inventory.ItemInfo', lc('Inventory.client.INFO'), colorCodes.tf3_regular_text_color + info_text)
                    elif id == ItemsCatalog.CAN_BUY_TRADE:
                        self.MoveToBuy(item)
                        self.UpdateTradeInterface()
                    elif id == ItemsCatalog.CAN_QUEST:
                        self.QuestItemAction(item['complexItemID'], ItemsUtils.GetQuestItemID(item))
                    elif id == ItemsCatalog.CAN_UNEQUIP:
                        self.InventoryPutOff(item)
                BWPersonality.GUICore.removeListener('contextMenuEvent', self.ContextMenuEvent)
            elif event == soGUI.soContextMenuComponent.EVENT_SHOW:
                pass
            elif event == soGUI.soContextMenuComponent.EVENT_CANCEL:
                BWPersonality.GUICore.removeListener('contextMenuEvent', self.ContextMenuEvent)
        except Exception as e:
            traceback.print_exc()

    def SpareCalback(self, event, data):
        if event == MESSAGEBOX.EVENT_BTNPRESS:
            if data['btn'] == MESSAGEBOX.BTN_OK:
                text = data['add_controls']['edit_box']
                if isnumeric(text):
                    quantity = int(text)
                    if self.ItemLocked(self.context_menu_item):
                        return
                    print text
                    self.BeginSpare(self.context_menu_item, quantity)

    def addItem(self):
        self.listeners.addedItems()

    def UseItem(self, complexItem):
        item_class = ItemsCatalog.GetItemClass(complexItem['complexItemType'])
        if item_class == ItemsCatalog.WEAPON:
            self.putOnItem(complexItem)
        elif item_class == ItemsCatalog.CLOTH:
            self.putOnItem(complexItem)
        elif item_class == ItemsCatalog.EXPLOSION:
            self.equipItem(complexItem)
        elif item_class == ItemsCatalog.BUFF:
            self.putOnItem(complexItem)
        elif item_class == ItemsCatalog.LOOT:
            self.putOnItem(complexItem)

    def WeaponSplash(self, item):
        if item != 0:
            BWPersonality.GUICore.weaponSelect(item)

    def UpdateSkill(self):
        BWPersonality.GUICore.skillData(self.GetSkillDict())

    def set_KnowingRecipes(self, old):
        self.UpgradeCraft()

    def set_StoredItems(self, old_value):
        self.NeedToUpdateItemCache()

    def set_StoredItemsInShop(self, old_value):
        self.NeedToUpdateItemCache()

    def set_ItemsWeight(self, old_value):
        self.NeedToUpdateInventory()

    def InitWeaponAmmo(self):
        if ItemsUtils.CheckEquippedItemValidityClient(self):
            equippingItem = ItemsUtils.GetComplexItemByID(self, self.ActiveItemID)
            if equippingItem != None:
                complexItemType = self.ActiveItemType
                item_class = ItemsCatalog.GetItemClass(complexItemType)
                if item_class == ItemsCatalog.WEAPON:
                    self.SetActiveWeaponAmmo(self.ActiveItemAmmo)
        return

    def SetActiveWeaponAmmo(self, ammo_num):
        self.CurrentWeaponAmmo = ammo_num
        self.NeedToUpdateWeaponIcon()

    def set_CreditNumber(self, oldType = None):
        self.InformMoneyChange(oldType, self.CreditNumber)
        self.NeedToUpdateInventory()

    def set_GoldCreditNumber(self, oldType = None):
        self.InformGoldChange(oldType, self.GoldCreditNumber)
        self.NeedToUpdateInventory()

    def set_CombatExperience(self, oldType = None):
        self.InformExpChange(oldType, self.CombatExperience, CharacterConst.COMBAT_EXPIRIENCE)

    def set_SurvivalExperience(self, oldType = None):
        self.InformExpChange(oldType, self.SurvivalExperience, CharacterConst.SURVIVAL_EXPIRIENCE)

    def set_OtherExperience(self, oldType = None):
        self.InformExpChange(oldType, self.OtherExperience, CharacterConst.OTHER_EXPIRIENCE)

    def set_ActiveItemID(self, oldType = None):
        if self.ActiveItemID:
            equippingItem = ItemsUtils.GetComplexItemByID(self, self.ActiveItemID)
            equippedItemType = equippingItem['complexItemType']
            item_class = ItemsCatalog.GetItemClass(equippedItemType)
            self.OnActiveItemChanged()
            if item_class == ItemsCatalog.WEAPON:
                self.SetActiveWeaponAmmo(self.ActiveItemAmmo)
                return
        self.CurrentWeaponAmmo = 0

    def OnActiveItemChanged(self):
        pass

    def set_ActiveGrenadeID(self, oldType = None):
        self.NeedToUpdateInventory()

    def set_ActiveWeaponSet(self, oldType = None):
        self.NeedToUpdateInventory()

    def set_ActiveGadjetSet(self, oldType = None):
        self.NeedToUpdateInventory()

    def set_ActiveArtifactList(self, oldType = None):
        self.NeedToUpdateInventory()

    def set_CarryingItems(self, oldType = None):
        self.NeedToUpdateInventory()

    def NeedToUpdateInventory(self):
        self.UpdateInventory()

    def NeedToUpdateTradeInterface(self, trader_id):
        if trader_id != self.TraderID:
            return
        self.UpdateTradeInterface()

    def NeedToUpdateWeaponIcon(self):
        self.UpdateWaeponIcon()

    def NeedToUpdateItemCache(self):
        self.RedrawItemCache()

    def NeedToCloseItemCache(self, object_mb):
        if self.cacheObjectID == object_mb.id:
            BWPersonality.GUICore.showItemCache(False)
            self.InitItemCache()

    def UpdateItemChanged(self):
        for key in self.ReportChangedItemDict:
            number_dict = self.ReportChangedItemDict.get(key, 0)
            if number_dict > 0:
                if self.canItemBeAdded():
                    string = lc('Inventory.client.ITEM_ADDED').format(ItemsUtils.GetItemName(key))
                else:
                    continue
            elif number_dict < 0:
                string = lc('Inventory.client.ITEM_LOST').format(ItemsUtils.GetItemName(key))
            else:
                continue
            number_dict = abs(number_dict)
            if number_dict > 1:
                string += u'(' + str(number_dict) + lc('Inventory.client.NUM_ITEMS_CLOSE_BRACKET')
            self.lootChatline(string)

        self.ReportChangedItemDict = {}

    def onItemChanged(self, type, number, id):
        if self.itemChangeTimer is not None:
            BigWorld.cancelCallback(self.itemChangeTimer)
        if self.ReportChangedItemDict.has_key(type):
            self.ReportChangedItemDict[type] += number
        else:
            self.ReportChangedItemDict[type] = number
        self.itemChangeTimer = BigWorld.callback(0.5, self.UpdateItemChanged)
        return

    def onItemAdded(self, type, number, id):
        self.onItemChanged(type, number, id)

    def onItemLost(self, type, number, id):
        self.onItemChanged(type, -number, id)

    def GetSuffix(self, num_money_str, const_list):
        num_money_str = num_money_str.lstrip('-')
        if len(num_money_str) > 0:
            first_digit = int(num_money_str[-1])
            if len(num_money_str) >= 2:
                second_digit = int(num_money_str[-2])
                if second_digit == 1:
                    return const_list[2]
            if first_digit == 1:
                return const_list[0]
            if first_digit > 1 and first_digit < 5:
                return const_list[1]
            if first_digit >= 5 or first_digit == 0:
                return const_list[2]

    def InformMoneyChange(self, old_money, new_money):
        if old_money >= new_money:
            money_change = old_money - new_money
            num_money_str = str(money_change)
            money_str = lc('Inventory.client.SPENDED').format(num_money_str, self.GetSuffix(num_money_str, [lc('Inventory.client.SUFFIXES_1'), lc('Inventory.client.SUFFIXES_2'), lc('Inventory.client.SUFFIXES_3')]))
        else:
            money_change = new_money - old_money
            num_money_str = str(money_change)
            money_str = lc('Inventory.client.GAINED').format(num_money_str, self.GetSuffix(num_money_str, [lc('Inventory.client.SUFFIXES_1'), lc('Inventory.client.SUFFIXES_2'), lc('Inventory.client.SUFFIXES_3')]))
        self.lootChatline(money_str)

    def InformGoldChange(self, old_money, new_money):
        if old_money >= new_money:
            money_change = old_money - new_money
            num_money_str = str(money_change)
            money_str = lc('Inventory.client.SPENDED').format(num_money_str, self.GetSuffix(num_money_str, [lc('Inventory.client.SUFFIXES_4'), lc('Inventory.client.SUFFIXES_5'), lc('Inventory.client.SUFFIXES_6')]))
        else:
            money_change = new_money - old_money
            num_money_str = str(money_change)
            money_str = lc('Inventory.client.GAINED').format(num_money_str, self.GetSuffix(num_money_str, [lc('Inventory.client.SUFFIXES_4'), lc('Inventory.client.SUFFIXES_5'), lc('Inventory.client.SUFFIXES_6')]))
        self.lootChatline(money_str)

    def InformExpChange(self, old_exp, new_exp, exp_type):
        if exp_type == CharacterConst.COMBAT_EXPIRIENCE:
            ending = lc('Inventory.client.COMBAT_EXPIRIENCE')
        elif exp_type == CharacterConst.SURVIVAL_EXPIRIENCE:
            ending = lc('Inventory.client.SURVIVAL_EXPIRIENCE')
        elif exp_type == CharacterConst.OTHER_EXPIRIENCE:
            ending = lc('Inventory.client.OTHER_EXPIRIENCE')
        exp_change = new_exp - old_exp
        num_exp_str = str(exp_change)
        exp_str = lc('Inventory.client.GAINED').format(num_exp_str, self.GetSuffix(num_exp_str, [lc('Inventory.client.SUFFIXES_7'), lc('Inventory.client.SUFFIXES_8'), lc('Inventory.client.SUFFIXES_9')])) + u' ' + ending
        self.questChatline(exp_str)

    def GetCharacterEquippedItemsList(self):
        cloth_parts_dict = {ItemsCatalog.MASK: soCharacterScreen2.INDEX_FACE,
         ItemsCatalog.HAT: soCharacterScreen2.INDEX_HEAD,
         ItemsCatalog.BACKPACK: soCharacterScreen2.INDEX_BACKPACK,
         ItemsCatalog.HANDS: soCharacterScreen2.INDEX_PALMS,
         ItemsCatalog.ARMOR: soCharacterScreen2.INDEX_ARMOR,
         ItemsCatalog.SHIRT: soCharacterScreen2.INDEX_CHEST,
         ItemsCatalog.PANTS: soCharacterScreen2.INDEX_LEGS,
         ItemsCatalog.BOOTS: soCharacterScreen2.INDEX_FEET}
        equip_list = ItemsUtils.GetEquipListIDs(self)
        blank_models_list = [ItemsCatalog.MASK_BLANK['TypeID'],
         ItemsCatalog.HAT_BLANK['TypeID'],
         ItemsCatalog.WEAPONMAIN_BLANK['TypeID'],
         ItemsCatalog.WEAPONPISTOL_BLANK['TypeID'],
         ItemsCatalog.BACKPACK_BLANK['TypeID'],
         ItemsCatalog.GLOVES_BLANK['TypeID'],
         ItemsCatalog.ARMOR_BLANK['TypeID'],
         ItemsCatalog.SHIRT_BLANK['TypeID'],
         ItemsCatalog.GADGET_ADD_BLANK['TypeID'],
         ItemsCatalog.PANTS_BLANK['TypeID'],
         ItemsCatalog.BOOTS_BLANK['TypeID'],
         ItemsCatalog.ARTIFACT_ADD_BLANK['TypeID'],
         ItemsCatalog.ARTIFACT_ADD_BLANK['TypeID'],
         ItemsCatalog.ARTIFACT_ADD_BLANK['TypeID'],
         ItemsCatalog.GRENADE_ADD_BLANK['TypeID']]
        equipped_item_list = [ self.CreateFakeItem(x) for x in blank_models_list ]
        artifact_counter = 0
        artifact_slots = [soCharacterScreen2.INDEX_ARTIFACT1, soCharacterScreen2.INDEX_ARTIFACT2, soCharacterScreen2.INDEX_ARTIFACT3]
        for id in equip_list:
            item = ItemsUtils.GetComplexItemByID(self, id)
            if item:
                item_type = item['complexItemType']
                item_class = ItemsCatalog.GetItemClass(item_type)
                items_param = ItemsCatalog.GetItemParam(item_type)
                if item_class == ItemsCatalog.WEAPON:
                    gun_type = items_param['GunType']
                    gun_priority = ItemsUtils.GetWeaponPriority(gun_type)
                    if gun_priority == ItemsCatalog.SECONDARY:
                        equipped_item_list[soCharacterScreen2.INDEX_SECONDARY] = item
                    else:
                        equipped_item_list[soCharacterScreen2.INDEX_PRIMARY] = item
                elif item_class == ItemsCatalog.CLOTH:
                    parts_covered = items_param['ArmorType'][:]
                    main_part = parts_covered.pop(0)
                    while not cloth_parts_dict.has_key(main_part) and len(parts_covered) > 0:
                        main_part = parts_covered.pop(0)

                    equipped_item_list[cloth_parts_dict[main_part]] = item
                    for fake_part in parts_covered:
                        if cloth_parts_dict.has_key(fake_part):
                            equipped_item_list[cloth_parts_dict[fake_part]] = self.CreateFakeItem(item_type)

                elif item_class == ItemsCatalog.GADGET:
                    equipped_item_list[soCharacterScreen2.INDEX_UNDERWARE] = item
                elif item_class == ItemsCatalog.EXPLOSION:
                    equipped_item_list[soCharacterScreen2.INDEX_THROW] = item
                elif item_class == ItemsCatalog.ARTIFACT:
                    try:
                        slot_id = artifact_slots[artifact_counter]
                    except IndexError:
                        continue

                    equipped_item_list[slot_id] = item
                    artifact_counter += 1

        return equipped_item_list

    def UpdateInventory(self):

        def reallyUpdateInventory():
            if self.isDestroyed:
                return
            else:
                self.systemChatline('UpdateInventory')
                self.CheckAllItemsInPosList()
                items = self.GetItemsList()
                BWPersonality.GUICore.setInventoryData(items, (self.ItemsWeight,
                 self.GetStatValue(Stats.ch_MaxWeight),
                 len(self.CarryingItems),
                 ItemsUtils.MAX_AVATAR_ITEMS), (self.CreditNumber, self.GoldCreditNumber), self.inventoryFilter)
                character_screen_data = {'items': self.GetCharacterEquippedItemsList(),
                 'displayName': self.name,
                 'charStats': self.GetAllStatsList()}
                BWPersonality.GUICore.setCharScreenData(character_screen_data)
                self.items_to_drop = filter(lambda x: ItemsUtils.GetComplexItemByID(self, x) != None, self.items_to_drop)
                self.UpdateWaeponIcon()
                self.updateInventoryTimer = None
                self.UpdateQuickBar()
                return

        if self.updateInventoryTimer is not None:
            BigWorld.cancelCallback(self.updateInventoryTimer)
        self.updateInventoryTimer = BigWorld.callback(0.5, reallyUpdateInventory)
        return

    def UpdateWaeponIcon(self):

        def get_weapon_string(set_slot_name):
            weapon_id = self.ActiveWeaponSet[set_slot_name]
            weapon_item = ItemsUtils.GetComplexItemByID(self, weapon_id)
            if weapon_item:
                if weapon_id == self.ActiveItemID:
                    ammo_type = self.ActiveItemAmmoType
                    weapon_string = str(self.CurrentWeaponAmmo) + '/' + str(ItemsUtils.GetItemQuanity(self.CarryingItems, ammo_type, ItemsCatalog.ITEM_TYPE_VOID))
                    inconstant_param = None
                else:
                    inconstant_param = ItemsUtils.GetComplexItemInconstanParams(weapon_item)
                    ammo_type = inconstant_param[ItemsCatalog.INC_LOADED_MUNITION_TYPE]
                    weapon_string = str(inconstant_param[ItemsCatalog.INC_MUNITION_NUMBER]) + '/' + str(ItemsUtils.GetItemQuanity(self.CarryingItems, ammo_type, ItemsCatalog.ITEM_TYPE_VOID))
                if ammo_type:
                    weapon_name = ItemsUtils.GetItemName(ammo_type, fGetShortName=True)
                else:
                    weapon_name = lc('Inventory.client.NO')
            else:
                weapon_name = lc('Inventory.client.NO')
                weapon_string = '0'
            return (weapon_name, weapon_string)

        primary_weapon_name, primary_weapon_string = get_weapon_string('PrimarySlotID')
        secondary_weapon_name, secondary_weapon_string = get_weapon_string('SecondarySlotID')
        grenade_id = self.ActiveGrenadeID
        grenade_item = equippingGrenade = ItemsUtils.GetComplexItemByID(self, grenade_id)
        if grenade_item:
            grenade_inconstant_param = ItemsUtils.GetComplexItemInconstanParams(grenade_item)
            grenade_string = str(grenade_inconstant_param[ItemsCatalog.INC_ROUND_NUMBER])
            grenade_name = self.GetItemName(grenade_item, grenade_inconstant_param, True)
        else:
            grenade_name = lc('Inventory.client.NO')
            grenade_string = '0'
        data = {'primary_name': primary_weapon_name,
         'secondary_name': secondary_weapon_name,
         'throw_name': grenade_name,
         'primary_count': primary_weapon_string,
         'secondary_count': secondary_weapon_string,
         'throw_count': grenade_string}
        BWPersonality.GUICore.setMunitionsData(data)

    def UpdateExchange(self, opponent_entity):

        def credit_check(newStr, wholeText, offset):
            full_text = wholeText[0:offset] + newStr + wholeText[offset:]
            if not full_text.isdigit():
                return False
            if wholeText:
                if int(full_text) <= self.CreditNumber:
                    return True
                return False
            return True

        def gold_check(newStr, wholeText, offset):
            print 'CHECK:', newStr, wholeText, offset
            full_text = wholeText[0:offset] + newStr + wholeText[offset:]
            if not full_text.isdigit():
                return False
            if wholeText:
                if int(full_text) <= self.GoldCreditNumber:
                    return True
                return False
            return True

        opponentName = opponent_entity.name
        my_name = self.name
        my_exhange_list = self.GetTradingItemList()
        opponent_exhange_list = opponent_entity.ExchangeProperties.ItemsToExchange if opponent_entity.ExchangeProperties.fOffer else []
        trade_data = {'player_name': my_name,
         'contractor_name': opponentName,
         'contractor_money': str(opponent_entity.ExchangeProperties.CreditsToExchange),
         'contractor_gold': str(opponent_entity.ExchangeProperties.GoldToExchange),
         'player_items': my_exhange_list,
         'contractor_items': opponent_exhange_list,
         'player_confirmation': self.ExchangeProperties.fOffer,
         'contractor_confirmation': opponent_entity.ExchangeProperties.fOffer,
         'message': lc('Common.Messages.OPPONENT_ACCEPT') if opponent_entity.ExchangeProperties.fAccept else '',
         'input_validator': credit_check,
         'input_gold_validator': gold_check,
         'transaction_confirmed': self.ExchangeProperties.fAccept}
        if self.ExchangeProperties.fOffer:
            trade_data['player_money'] = str(self.ExchangeProperties.CreditsToExchange)
            trade_data['player_gold'] = str(self.ExchangeProperties.GoldToExchange)
        BWPersonality.GUICore.setPCTradeData(trade_data)

    def UpdatePCTradeMoney(self, money, gold = 0):
        trade_data = {}
        trade_data['player_money'] = str(money)
        trade_data['player_gold'] = str(gold)
        BWPersonality.GUICore.setPCTradeData(trade_data)

    def InformExchangeTimer(self, num_seconds_to_end):
        UPDATE_PERIOD = 1.0
        if self.ExchangeProperties.fOffer and self.ExchangeProperties.fAccept:
            if num_seconds_to_end > 0:
                trade_data = {'message': lc('Common.Messages.EXCHANGE_WILL_START_IN').format(str(num_seconds_to_end))}
                self.exchange_timer_id = BigWorld.callback(UPDATE_PERIOD, partial(self.InformExchangeTimer, num_seconds_to_end - 1))
            else:
                trade_data = {'message': ''}
            BWPersonality.GUICore.setPCTradeData(trade_data)

    def ExchangeEvent(self, event, data):
        from gui_const import PC_TRADE
        if event == PC_TRADE.EVENT_ADDITEM:
            if data:
                if data not in self.PCTradeItems:
                    self.PCTradeItems.append(data)
                    self.NeedToUpdateExchangeInterface()
        if event == PC_TRADE.EVENT_DELITEM:
            if data:
                if data in self.PCTradeItems:
                    self.PCTradeItems.remove(data)
                    self.NeedToUpdateExchangeInterface()
        if event == PC_TRADE.EVENT_OFFER:
            for item in self.PCTradeItems:
                self.cell.AddItemToTrade(item['complexItemID'])

            self.cell.SetMoneyToTrade(self.PCTradeMoney)
            self.cell.SetGoldToTrade(self.PCTradeGold)
            self.cell.SetOffer(1)
            print 'PC_TRADE.EVENT_OFFER:', self.PCTradeMoney, self.PCTradeGold
        if event == PC_TRADE.EVENT_CONFIRM:
            self.cell.SetConfirm(1)
        if event == PC_TRADE.EVENT_CANCEL:
            self.cell.CancelTrade(0)
            if self.exchange_timer_id:
                BigWorld.cancelCallback(self.exchange_timer_id)
            self.InitPlayerTrade()
            self.UpdatePCTradeMoney(0)
        if event == PC_TRADE.EVENT_ABORT:
            self.cell.CancelTrade(1)
            self.InitPlayerTrade()
            self.UpdatePCTradeMoney(0)
            self.NeedToUpdateInventory()
        if event == PC_TRADE.EVENT_MONEYSET:
            if data != None:
                if isnumeric(data):
                    num_money = int(data)
                    self.PCTradeMoney = num_money
        if event == PC_TRADE.EVENT_GOLDSET:
            if data != None:
                if isnumeric(data):
                    num_gold = int(data)
                    self.PCTradeGold = num_gold
        return

    def CanPlayerTrade(self):
        if self.playerExchangeInProgress:
            return False
        else:
            return True

    def ExchangeEnded(self):
        self.isTrade = False
        self.playerExchangeInProgress = False
        self.NeedToUpdateInventory()
        BWPersonality.GUICore.showPCTrade(False)

    def ShowExchange(self):
        self.playerExchangeInProgress = True
        BWPersonality.GUICore.showPCTrade()
        self.NeedToUpdateExchangeInterface()

    def GetReceiptName(self, number):
        return ItemsUtils.GetItemName(number)

    def GetReceiptDescription(self, number):
        string = u''
        param = ItemsCatalog.GetItemParam(number)
        if param:
            string += self.GetReceiptInfo(param)
        string += u'\n'
        string += ItemsUtils.GetItemDescription(number)
        return string

    def GetReceiptIcon(self, number):
        if number:
            receipt_param = ItemsCatalog.GetItemParam(number)
            result_type = receipt_param['CraftResult'].keys()[0]
            result_param = ItemsCatalog.GetItemParam(result_type)
            return result_param['IconName']
        return ''

    def InitCraft(self):
        self.craftItemList = []
        self.craftSelectedReceipt = 0
        self.craftAutofill = False
        self.UpgradeCraft()

    def UpgradeCraft(self):
        remove_list = []
        for item in self.craftItemList:
            if not ItemsUtils.GetComplexItemByID(self, item):
                remove_list.append(item)

        for remove_item in remove_list:
            self.craftItemList.remove(remove_item)

        data = {'recipes': self.GetReceiptList(),
         'items': self.craftItemList,
         'description': self.GetReceiptDescription(self.craftSelectedReceipt),
         'autofill': self.craftAutofill,
         'icon': self.GetReceiptIcon(self.craftSelectedReceipt)}
        BWPersonality.GUICore.setCraftData(data)

    def craftEvent(self, event, data):
        if event == soGUI.soCraftGUI.EVENT_SELECT:
            self.craftSelectedReceipt = data
            if self.craftAutofill:
                resource_dict = self.GetReceiptPartsList(self.craftSelectedReceipt)
                self.craftItemList = self.FillContainerWithResourceIDs(resource_dict)
            self.UpgradeCraft()
        elif event == soGUI.soCraftGUI.EVENT_AUTOFILL:
            self.craftAutofill = data
            self.UpgradeCraft()
        elif event == soGUI.soCraftGUI.EVENT_CRAFT:
            self.startCraft(self.craftSelectedReceipt, self.craftItemList)
        elif event == soGUI.soCraftGUI.EVENT_CLEAR:
            self.craftItemList = []
            self.UpgradeCraft()
        elif event == soGUI.soCraftGUI.EVENT_ADDITEM:
            item_id = data['complexItemID']
            if item_id not in self.craftItemList:
                self.craftItemList.append(item_id)
                self.UpgradeCraft()
        elif event == soGUI.soCraftGUI.EVENT_DELITEM:
            if data in self.craftItemList:
                self.craftItemList.remove(data)
                self.UpgradeCraft()
        self.NeedToUpdateInventory()

    def InitNPCBarter(self):
        self.NPCBarterItemList = []
        self.NPCbarterautofill = False
        self.NPCbarterHideUnaffordable = False
        self.NPCBarterSelectedList = -1
        BWPersonality.GUICore.showPackageSell(False)

    def UpdateNPCBarter(self, UpdatePacks = True):
        try:
            trader = BigWorld.entities[self.TraderID]
        except:
            return

        data = {}
        if UpdatePacks:
            packs = []
            for index in xrange(len(trader.BarterAssortment)):
                if self.NPCbarterHideUnaffordable:
                    can_add = True
                    resourse_dict = ItemsUtils.ConvertTypesListToDict(trader.BarterAssortment[index]['resourceItems'], True)
                    for key in resourse_dict:
                        num_item_to_add = resourse_dict[key]
                        player_num_item = ItemsUtils.GetItemQuanity(self.CarryingItems, key)
                        if player_num_item < num_item_to_add:
                            can_add = False

                    if can_add:
                        packs.append([index, lc(trader.BarterAssortment[index]['barterListName'])])
                else:
                    packs.append([index, lc(trader.BarterAssortment[index]['barterListName'])])

            data['packs'] = packs
        offered_items = []
        requested_items = []
        if self.NPCBarterSelectedList >= 0:
            try:
                barter_list = trader.BarterAssortment[self.NPCBarterSelectedList]
            except:
                print 'Barter KeyError'
                return

            for item_type in barter_list['resultItems']:
                requested_items.append(self.CreateFakeItem(item_type))

            for item_id in self.NPCBarterItemList:
                offered_items.append(ItemsUtils.GetComplexItemByID(self, item_id))

            resourse_dict = ItemsUtils.ConvertTypesListToDict(barter_list['resourceItems'], True)
            for resurce_type in resourse_dict:
                number_already_added = ItemsUtils.GetItemQuanity(offered_items, resurce_type)
                needed_number = resourse_dict[resurce_type]
                if needed_number > number_already_added:
                    num_to_add_fake = needed_number - number_already_added
                    num_to_add_fake = math.ceil(num_to_add_fake / ItemsUtils.GetDefaultItemNumber(resurce_type))
                    for dummy in xrange(num_to_add_fake):
                        offered_items.append(self.CreateFakeItem(resurce_type))

        data['autofill'] = self.NPCbarterautofill
        data['hideUnaffordable'] = self.NPCbarterHideUnaffordable
        data['rewardItems'] = requested_items
        data['payItems'] = offered_items
        BWPersonality.GUICore.setPackageSellData(data)

    def StartNPCBarter(self, trader_entity):
        self.InitNPCBarter()
        BWPersonality.GUICore.showInventory()
        BWPersonality.GUICore.showPackageSell()
        self.TraderID = trader_entity.id
        self.UpdateNPCBarter()

    def GetNPCBarterResourceDict(self):
        try:
            trader = BigWorld.entities[self.TraderID]
        except:
            return (ItemsUtils.FAIL_NO_TRADER, None)

        resourse_dict = {}
        if self.NPCBarterSelectedList >= 0:
            try:
                barter_list = trader.BarterAssortment[self.NPCBarterSelectedList]
            except:
                return (ItemsUtils.FAIL_CANT_SELL, None)

            resourse_dict = ItemsUtils.ConvertTypesListToDict(barter_list['resourceItems'], True)
        return resourse_dict

    def FillContainerWithResourceIDs(self, resource_dict):
        container = []
        for resource_key in resource_dict:
            resource_type = resource_key
            resource_num = resource_dict[resource_key]
            items_generator = ItemsUtils.GetComplexItemByTypeGenerator(self, resource_type)
            while ItemsUtils.GetItemQuanity([ ItemsUtils.GetComplexItemByID(self, x) for x in container ], resource_type) < resource_num:
                try:
                    item = items_generator.next()
                except StopIteration:
                    break

                if item:
                    item_id = item['complexItemID']
                    if not ItemsUtils.IsItemEquipped(self, item_id):
                        if item_id not in container:
                            container.append(item_id)
                else:
                    break

        return container

    def NPCBarterEvent(self, event, data):

        def AddItemIDToNPCBarterList(item_id):
            if item_id not in self.NPCBarterItemList:
                self.NPCBarterItemList.append(item_id)

        def RemoveItemIDToNPCBarterList(item_id):
            if item_id in self.NPCBarterItemList:
                self.NPCBarterItemList.remove(item_id)

        if event == soGUI.soPackageSellGUI.EVENT_PACKSELECT:
            self.NPCBarterSelectedList = data
            if self.NPCbarterautofill:
                resource_dict = self.GetNPCBarterResourceDict()
                self.NPCBarterItemList = self.FillContainerWithResourceIDs(resource_dict)
            self.UpdateNPCBarter(False)
            return
        if event == soGUI.soPackageSellGUI.EVENT_AUTOFILL:
            self.NPCbarterautofill = data
        elif event == soGUI.soPackageSellGUI.EVENT_HIDEUNAFFORDABLE:
            self.NPCbarterHideUnaffordable = data
        elif event == soGUI.soPackageSellGUI.EVENT_BUY:
            self.startNPCBarter(self.TraderID, self.NPCBarterSelectedList, self.NPCBarterItemList)
            self.NPCBarterItemList = []
        elif event == soGUI.soPackageSellGUI.EVENT_CLEAR:
            self.NPCBarterItemList = []
        elif event == soGUI.soPackageSellGUI.EVENT_ITEMADD:
            item_id = data['complexItemID']
            AddItemIDToNPCBarterList(item_id)
        elif event == soGUI.soPackageSellGUI.EVENT_ITEMREMOVE:
            item_id = data['complexItemID']
            RemoveItemIDToNPCBarterList(item_id)
        elif event == soGUI.soPackageSellGUI.EVENT_ITEMCONTEXT:
            pass
        elif event == soGUI.soPackageSellGUI.EVENT_CLOSE:
            self.NPCBarterItemList = []
        self.UpdateNPCBarter()
        self.NeedToUpdateInventory()

    def AddItemToSlotList(self, id):
        self.inventoryPositionList.append(id)

    def RemoveItemSlotList(self, id):
        self.inventoryPositionList.remove(id)

    def ChangeItemSlotNumber(self, old, new):
        old_id = old['complexItemID']
        new_id = new['complexItemID']
        new_id = self.inventoryPositionList.index(new_id)
        self.inventoryPositionList.remove(old_id)
        self.inventoryPositionList.insert(new_id, old_id)
        self.NeedToUpdateInventory()

    def GetItemBySlotNumber(self, needed_slot_number):
        id = self.inventoryPositionList[needed_slot_number]
        item = ItemsUtils.GetComplexItemByID(self, id)
        if item:
            return item
        del self.inventoryPositionList[needed_slot_number]

    def CheckAllItemsInPosList(self):
        equip_list = ItemsUtils.GetEquipListIDs(self)
        all_unequipped_items_ds = []
        for item in self.CarryingItems:
            if item['complexItemID'] not in equip_list:
                if item['complexItemID'] not in self.inventoryPositionList:
                    self.AddItemToSlotList(item['complexItemID'])
                all_unequipped_items_ds.append(item['complexItemID'])

        index = 0
        length = len(self.inventoryPositionList)
        while index < length:
            id = self.inventoryPositionList[index]
            if id not in all_unequipped_items_ds:
                self.RemoveItemSlotList(id)
                length = len(self.inventoryPositionList)
            else:
                index += 1

    def itemFilterFunction(self, item_sequence, item_lambda, filter_integer):

        def CheckBit(value, bit):
            if value & bit:
                return True
            else:
                return False

        item_list = []
        for item_id in item_sequence:
            if item_lambda is not None:
                item = item_lambda(item_id)
            else:
                item = item_id
            item_class = ItemsCatalog.GetItemClass(item['complexItemType'])
            if ItemsUtils.IsQuestItem(item):
                item_class = ItemsCatalog.QUEST
            bit_names_dict = {ItemsCatalog.WEAPON: INVENTORY.FILTER_WEAPON,
             ItemsCatalog.CLOTH: INVENTORY.FILTER_ARMOR,
             ItemsCatalog.ARTIFACT: INVENTORY.FILTER_ARTIFACT,
             ItemsCatalog.GADGET: INVENTORY.FILTER_CONSUMABLE,
             ItemsCatalog.BUFF: INVENTORY.FILTER_CONSUMABLE,
             ItemsCatalog.PART: INVENTORY.FILTER_WEAPON,
             ItemsCatalog.AMMO: INVENTORY.FILTER_WEAPON,
             ItemsCatalog.EXPLOSION: INVENTORY.FILTER_WEAPON,
             ItemsCatalog.LOOT: INVENTORY.FILTER_MISC,
             ItemsCatalog.QUEST: INVENTORY.FILTER_QUEST}
            if CheckBit(filter_integer, bit_names_dict[item_class]):
                item_param = ItemsCatalog.GetItemParam(item['complexItemType'])
                item_list.append(item)

        return item_list

    def itemFilterBySellMode(self, item_id):
        if self.SellMode == NPC_VENDOR.MODE_SELL_FOR_MONEY:
            return True
        if self.SellMode == NPC_VENDOR.MODE_SELL_FOR_GOLD:
            if ItemsUtils.CanItemBeBoughtForGold(item_id):
                return True
        return False

    def GetItemsList(self):
        return self.itemFilterFunction(self.inventoryPositionList, partial(ItemsUtils.GetComplexItemByID, self, getNotAppruved=True), self.inventoryFilter)

    def GetItemDescription(self, item, inconstant_param = None):
        if inconstant_param == None:
            if item != None:
                inconstant_param = ItemsUtils.GetComplexItemInconstanParams(item)
        questID = ItemsUtils.GetQuestItemID(item, inconstant_param)
        item_type = item['complexItemType']
        if inconstant_param != None:
            qInfo = self.getQItemInfo(questID, item_type)
            if qInfo != None:
                item_str = qInfo[1]
                if item_str:
                    return item_str
        return ItemsUtils.GetItemDescription(item_type)

    def GetItemName(self, item, inconstant_param = None, fGetShortName = False):
        if inconstant_param == None:
            if item != None:
                inconstant_param = ItemsUtils.GetComplexItemInconstanParams(item)
        questID = ItemsUtils.GetQuestItemID(item, inconstant_param)
        item_type = item['complexItemType']
        if inconstant_param != None:
            qInfo = self.getQItemInfo(questID, item_type)
            if qInfo != None:
                item_str = qInfo[0]
                if item_str:
                    return item_str
        return ItemsUtils.GetItemName(item_type, fGetShortName, tintItem=item)

    def setCrosshairSlide(self, xangle, fOutOfRange, forced = False, visible = True):
        xangle *= 0.5
        if xangle > math.pi / 2:
            xangle = math.pi / 2
        scope_type = self.snipingScopeType
        if scope_type != ItemsCatalog.NONE_TYPE and self.sniping:
            data = {'heap_mode': soTargettingGUI.HEAP_NONE,
             'scope_tube': SCOPE_MULTIPLER_TABLE[scope_type][1],
             'scope_lens': SCOPE_MULTIPLER_TABLE[scope_type][2],
             'scope_blur': soTargettingGUI.SCOPEBLUR_DEFAULT,
             'inaccuracy': (0.0, 0.0),
             'out_of_range': False}
        else:
            data = {'heap_mode': soTargettingGUI.HEAP_DEFAULT,
             'scope_tube': soTargettingGUI.SCOPETUBE_NONE,
             'scope_lens': soTargettingGUI.SCOPELENS_NONE,
             'scope_blur': soTargettingGUI.SCOPEBLUR_NONE,
             'inaccuracy': (xangle, xangle),
             'out_of_range': fOutOfRange}
        BWPersonality.GUICore.setCrosshairsData(data)

    def repairEvent(self, event, data):
        if event == REPAIR.EVENT_STATE:
            if not data:
                self.InitRepair(True)