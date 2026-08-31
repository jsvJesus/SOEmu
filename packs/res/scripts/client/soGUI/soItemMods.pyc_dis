# Embedded file name: scripts/client/soGUI/soItemMods.py
from Localization import lc
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import BWPersonality
import Avatar
from soGUI.soDropDownList import soDropDownList
from soGUI.soButton import soButton
from soGUI.soInventoryScreen import soInventoryScreen
from Helpers.PyGUI import PyGUIEvent
from Helpers.BWCoroutine import *
import Helpers.Listener as Listener
from soGUI.soInventoryScreen import soInventorySlot
from Items import ItemsCatalog
import ItemsUtils
import math

class soItemMods(PyGUI.Window, Listener.Listenable):
    factoryString = 'soGUI.soItemMods'
    WEAPON_SLOTW = 256
    WEAPON_SLOTH = 128
    LEFT_OFFSET = 5
    TOP_OFFSET = 5
    MODS_WINDOWH = WEAPON_SLOTH + TOP_OFFSET * 2 + 300
    MODS_WINDOWW = WEAPON_SLOTW + LEFT_OFFSET * 2
    MODS_CAPTIONH = 32
    MODS_CAPTIONW = MODS_WINDOWW
    MODS_FRAMEW = MODS_WINDOWW
    CAPTION_TEXTURE = 'soGUI/maps/Controls/window_frame/genericWindowFrame.tga'
    FRAME_TEXTURE = 'soGUI/maps/Controls/window_frame/genericWindowFrame.tga'
    ACTION_APPLY_MODS = 0
    ACTION_ROLLBACK_MODS = 1

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        Listener.Listenable.__init__(self)
        component.script = self
        self.captionText = ''
        self.weaponRender = None
        self.item = None
        self.parts = []
        self.addedParts = []
        self.setupRoot()
        self.setupWindow()
        self.setupWeapon()
        self.setupSlots()
        self.setupOkCancel()
        self.initListeners().run()
        return

    def getInventoryInstance(self):
        if isinstance(BigWorld.player(), Avatar.PlayerAvatar):
            if hasattr(BigWorld.player(), 'playerGUI'):
                if hasattr(BigWorld.player().playerGUI, 'inventory'):
                    return BigWorld.player().playerGUI.inventory.script
        return None

    def setupRoot(self):
        self.component.visible = False
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.verticalAnchor = 'CENTER'
        self.component.horizontalAnchor = 'CENTER'
        self.component.textureName = ''
        self.component.width = soItemMods.MODS_WINDOWW
        self.component.height = soItemMods.MODS_WINDOWH
        self.component.dropFocus = True
        self.component.moveFocus = True
        self.component.crossFocus = True

    def setupWindow(self):

        def setupCaption():
            captionCmp = GUI.Frame2(soItemMods.CAPTION_TEXTURE)
            captionCmp.widthMode = captionCmp.heightMode = 'PIXEL'
            captionCmp.horizontalPositionMode = captionCmp.verticalPositionMode = 'CLIP'
            captionCmp.horizontalAnchor = 'LEFT'
            captionCmp.verticalAnchor = 'TOP'
            captionCmp.position = (-1.0, 1.0, 0.0)
            captionCmp.width = soItemMods.MODS_CAPTIONW
            captionCmp.height = soItemMods.MODS_CAPTIONH
            captionCmp.colour = (255, 255, 255, 255)
            captionCmp.materialFX = 'BLEND'
            captionCmp.visible = True
            labelCmp = GUI.Text('')
            labelCmp.horizontalAnchor = 'CENTER'
            labelCmp.verticalAnchor = 'CENTER'
            labelCmp.horizontalPositionMode = labelCmp.verticalPositionMode = 'CLIP'
            labelCmp.font = 'ruRU_calibri_default.font'
            labelCmp.colour = (255, 255, 255, 255)
            labelCmp.materialFX = 'BLEND'
            labelCmp.visible = True
            closeBox = soButton(GUI.Window())
            closeBox.component.widthMode = closeBox.component.heightMode = 'PIXEL'
            closeBox.component.horizontalAnchor = 'RIGHT'
            closeBox.component.verticalAnchor = 'TOP'
            closeBox.component.horizontalPositionMode = closeBox.component.verticalPositionMode = 'CLIP'
            closeBox.component.colour = (255, 255, 255, 255)
            closeBox.component.materialFX = 'BLEND'
            closeBox.component.position = (1.0, 1.0, 0.0)
            closeBox.component.width = 45
            closeBox.component.height = 32
            closeBox.initVSC('soGUI/visual_styles/closeBtn.xml')
            closeBox.onBound()
            captionCmp.addChild(labelCmp, 'label')
            captionCmp.addChild(closeBox.component, 'closeBox')
            self.component.addChild(captionCmp, 'caption')

        def setupWorkFrame():
            mainFrame = GUI.Frame2(soItemMods.FRAME_TEXTURE)
            mainFrame.horizontalPositionMode = mainFrame.verticalPositionMode = 'CLIP'
            mainFrame.widthMode = mainFrame.heightMode = 'PIXEL'
            mainFrame.horizontalAnchor = 'LEFT'
            mainFrame.verticalAnchor = 'BOTTOM'
            mainFrame.width = soItemMods.MODS_FRAMEW
            mainFrame.height = soItemMods.MODS_WINDOWH - soItemMods.MODS_CAPTIONH
            mainFrame.position = (-1.0, -1.0, 0.0)
            mainFrame.colour = (255, 255, 255, 255)
            mainFrame.materialFX = 'BLEND'
            self.component.addChild(mainFrame, 'theFrame')

        setupCaption()
        setupWorkFrame()

    def setupWeapon(self):
        pixelW = soGUI.getPixelWidth(self.component)
        pixelH = soGUI.getPixelHeight(self.component)
        weaponMod = soDropDownList(GUI.Window(), soGUI.DropDownListPropsStructure(DDLWidth=self.WEAPON_SLOTW, btnW=0, btnH=self.WEAPON_SLOTH))
        cmp = weaponMod.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (-1.0 + pixelW * self.LEFT_OFFSET, 1.0 - pixelH * (self.MODS_CAPTIONH + self.TOP_OFFSET), 0.0)
        weaponMod.onBound()
        self.component.addChild(cmp, 'weaponMod')
        if self.item is not None:
            models = None
            self.weaponRender = BigWorld.PyModelRenderer(self.WEAPON_SLOTW, self.WEAPON_SLOTH)
            if len(self.parts) < 1:
                models = BigWorld.Model(*self.getItemSources(self.item))
            else:
                combinedModel = self.getItemSources(self.item)
                for part in self.parts:
                    combinedModel.append(*self.getItemSources(part))

                models = BigWorld.Model(*combinedModel)
            self.weaponRender.models = [models]
            models.zoomExtents(False, 1.0)
            models.rotate(math.pi / 4.0 * 2, (0.0, 1.0, 0.0))
            models.rotate(math.pi / 4.0, (1.0, 0.0, 0.0))
            models.scale = (3.0, 3.0, 3.0)
            models.position = (0.0, -0.2, -0.2)
            self.weaponRender.render()
            cmp.selectionView.glyph.widthMode = 'CLIP'
            cmp.selectionView.glyph.heightMode = 'CLIP'
            cmp.selectionView.glyph.width = 2.0
            cmp.selectionView.glyph.height = 2.0
            cmp.selectionView.glyph.position = (0.0, 0.0, 0.0)
            cmp.selectionView.glyph.texture = self.weaponRender.texture
        return

    def getItemSources(self, item):
        models_list = ItemsCatalog.GetItemParam(item['complexItemType'])['ModelNames'].values()
        for sub_item in item.itemList:
            sub_item_params = ItemsCatalog.GetItemParam(sub_item['itemType'])
            if sub_item_params:
                models_list += sub_item_params['ModelNames'].values()

        return models_list

    def getItemChildren(self, item):
        self.parts = item['itemList']

    def setupSlots(self):
        for part in self.parts:
            self.component.weaponMod.script.addElement('')

    def setupOkCancel(self):
        okBtn = soButton(GUI.Window())
        okcmp = okBtn.component
        okcmp.verticalPositionMode = okcmp.horizontalPositionMode = 'CLIP'
        okcmp.widthMode = okcmp.heightMode = 'PIXEL'
        okcmp.horizontalAnchor = 'CENTER'
        okcmp.verticalAnchor = 'BOTTOM'
        okcmp.width = 70
        okcmp.height = 30
        okcmp.position = (-0.5, -1.0 + soGUI.getPixelHeight(self.component) * 3, 0.0)
        self.component.addChild(okcmp, 'okBtn')
        okBtn.initVSC('soGUI/visual_styles/defaultBtnSmall.xml')
        okBtn.onBound()
        okBtn.setVisualState('normal')
        okcmp.label.text = 'Ok'
        cancelBtn = soButton(GUI.Window())
        cancelcmp = cancelBtn.component
        cancelcmp.verticalPositionMode = cancelcmp.horizontalPositionMode = 'CLIP'
        cancelcmp.widthMode = cancelcmp.heightMode = 'PIXEL'
        cancelcmp.horizontalAnchor = 'CENTER'
        cancelcmp.verticalAnchor = 'BOTTOM'
        cancelcmp.width = 70
        cancelcmp.height = 30
        cancelcmp.position = (0.5, -1.0 + soGUI.getPixelHeight(self.component) * 3, 0.0)
        self.component.addChild(cancelcmp, 'cancelBtn')
        cancelBtn.initVSC('soGUI/visual_styles/defaultBtnSmall.xml')
        cancelBtn.onBound()
        cancelBtn.setVisualState('normal')
        cancelcmp.label.text = lc('soItemMods.soGUI.STRING_253_25')

    def modifyItem(self, item, action):
        if action == soInventoryScreen.ACTION_MODIFY:
            if ItemsCatalog.GetItemClass(item['complexItemType']) == ItemsCatalog.WEAPON:
                self.item = item
                self.parts = self.getItemChildren(item)
                self.setupWeapon()
                self.setupSlots()
                self.component.visible = True
            if ItemsCatalog.GetItemClass(item['complexItemType']) == ItemsCatalog.PART:
                canAttach, partType = ItemsUtils.CanAttachItem(BigWorld.player(), self.item, item)
                if canAttach:
                    self.parts.append(item)
                    self.setupWeapon()
                    self.setupSlots()

    @PyGUIEvent('caption.closeBox', 'onClick')
    def onCloseBox(self):
        self.item = None
        self.parts = []
        self.addedParts = []
        self.component.visible = False
        return

    @PyGUIEvent('okBtn', 'onClick')
    def onOk(self):
        self.listeners.modifyEvent(self.item, self.addedParts, soItemMods.ACTION_APPLY_MODS)

    @PyGUIEvent('cancelBtn', 'onClick')
    def onCancel(self):
        self.listeners.modifyEvent(self.item, self.parts, soItemMods.ACTION_ROLLBACK_MODS)
        self.onCloseBox()

    @BWMemberCoroutine
    def initListeners(self):
        listening = False
        while not listening:
            yield BWWaitForPeriod(0.5)
            if isinstance(BigWorld.player(), Avatar.PlayerAvatar):
                if hasattr(BigWorld.player(), 'playerGUI'):
                    if hasattr(BigWorld.player(), 'listeners'):
                        BigWorld.player().playerGUI.inventory.script.addListener('slotEvent', self.modifyItem)
                        listening = True

    def handleDragEnterEvent(self, comp, dragged):
        return True

    def handleDropEvent(self, component, dropped):
        if isinstance(dropped.script, soInventorySlot):
            dropped.script.modify()
        return True