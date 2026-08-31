# Embedded file name: scripts/client/soGUI/soCharacterScreen.py
import BigWorld
import GUI
import BWPersonality
import soGUI
import math
import StalkerModel
import Helpers.PyGUI as PyGUI
from Helpers.PyGUI import PyGUIBase
from Helpers.Listener import Listenable
from functools import partial
from soGUI.soButton import soButton, soButtonWFT, soButtonWTT
from soGUI.soScrollBar import soScrollBar
from soGUI.soInventoryScreen import soInventorySlot
from Helpers.PyGUI import PyGUIEvent
from soGUI.data import RenderFeed
from Helpers.BWCoroutine import *
from soGUI.soToolTipComponent import soToolTipComponent
from Items import ItemsCatalog
import ItemsUtils
from soGUI.data import GUIEvents
from soGUI.soItemView import soItemView, soItemSlot
import soGUI.soItemView as module_soItemView
from Math import Vector4, Matrix
from Helpers.BWCoroutine import *
from math import ceil, floor
from soGUI.soList import soList2, soList2ElementBase
from Keys import *
from Localization import lc
from client_utils import get_entity_name

class soEquipSlot(soInventorySlot):
    factoryString = 'soGUI.soEquipSlot'

    def __init__(self, component):
        soInventorySlot.__init__(self, component)
        component.script = self
        component.dropFocus = False
        self.slotInfo = None
        self.interfaceID = soGUI.soGUICore.GUI_ID_CHARSCREEN
        return

    def haveItem(self):
        if self.slotInfo is not None:
            return True
        else:
            return False
            return

    def unEquiped(self):
        BWPersonality.GUICore.inventoryEvent(soGUI.soInventoryScreen.ACTION_UNEQUIP, self.slotInfo)

    def onLmb(self, comp, key, down, modifiers):
        if BWPersonality.GUICore.repairMode and self.slotInfo:
            BWPersonality.GUICore.charScreenEvent(soCharacterScreen.EVENT_REPAIR, self.slotInfo)

    def onRmb(self, comp, key, down, modifiers):
        BWPersonality.GUICore.charScreenEvent(soCharacterScreen.EVENT_CONTEXT, self.slotInfo)

    def onDoubleClick(self):
        return None

    def handleMouseEnterEvent(self, component):
        soInventorySlot.handleMouseEnterEvent(self, component)
        if BWPersonality.GUICore.repairMode and self.slotInfo:
            GUI.mcursor().shape = 'repair'
        return True

    def handleMouseLeaveEvent(self, component):
        soInventorySlot.handleMouseLeaveEvent(self, component)
        GUI.mcursor().shape = 'arrow'
        return True

    @BWMemberCoroutine
    def landingCheck(self):
        yield BWWaitForPeriod(0.5)


class soCharacterScreen(PyGUI.Window, Listenable):
    factoryString = 'soGUI.soCharacterScreen'
    BOTTOM_OFFSET = 30
    TYPICAL_OFFSET = 3
    FILTERFRAME_WIDTH = 128
    FILTERFRAME_HEIGHT = 30
    FILTERBTN_WIDTH = 20
    FILTERBTN_HEIGHT = 20
    RENDERFRAME_WIDTH = 200
    RENDERFRAME_HEIGHT = 300
    CAPTION_HEIGHT = 52
    INFOFRAME_WIDTH = RENDERFRAME_WIDTH
    INFOFRAME_HEIGHT = 32
    INFOWINDOW_WIDTH = INFOFRAME_WIDTH
    INFOWINDOW_HEIGHT = 150
    ITEM_WIDTH = 128
    ITEM_HEIGHT = 64
    SCROLL_WIDTH = 16
    SCROLL_STEP = ITEM_HEIGHT
    WINDOW_WIDTH = TYPICAL_OFFSET * 2 + RENDERFRAME_WIDTH + FILTERFRAME_WIDTH + SCROLL_WIDTH
    WINDOW_HEIGHT = TYPICAL_OFFSET + CAPTION_HEIGHT + RENDERFRAME_HEIGHT + INFOFRAME_HEIGHT + INFOWINDOW_HEIGHT + BOTTOM_OFFSET
    FILTER_WEAPONS = 1
    FILTER_ARMOR = 2
    FILTER_MISC = 4
    FILTER_CONSUMABLES = 8
    MAXIMUM_SLOTS = 17
    EVENT_CONTEXT = 0
    EVENT_REPAIR = 1

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        Listenable.__init__(self)
        component.script = self
        self.filterMask = self.FILTER_WEAPONS ^ self.FILTER_ARMOR ^ self.FILTER_MISC ^ self.FILTER_CONSUMABLES
        self.filterBtns = {}
        self.characterRender = None
        self.paperDoll = None
        self.needScroll = True
        self.vScroll = None
        self.statsWnd = None
        self.slots = []
        self.interfaceID = BWPersonality.GUICore.GUI_ID_CHARSCREEN
        self.setupRoot()
        self.setupFrames()
        self.setupMarkUp()
        self.setupItemFrame()
        self.setupCharacterRender()
        self.setupInfoFrame()
        self.setupCaption()
        self.setupScroll()
        self.setupCloseBox()
        self.updateScroll()
        GUI.reSort()
        return

    def onBound(self):
        PyGUI.Window.onBound(self)

    def setupRoot(self):
        cmp = self.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.verticalAnchor = 'CENTER'
        cmp.horizontalAnchor = 'CENTER'
        cmp.textureName = ''
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.dropFocus = True
        cmp.crossFocus = True
        cmp.moveFocus = True
        cmp.width = self.WINDOW_WIDTH
        cmp.height = self.WINDOW_HEIGHT
        cmp.position = (0.0, 0.0, 0.0)

    def setupMarkUp(self):
        topLine = GUI.Simple('soGUI/maps/Colours/darkGrey.tga')
        topLine.tiled = True
        topLine.tileHeight = 1
        topLine.tileWidth = 1
        topLine.colour = (255, 255, 255, 255)
        topLine.materialFX = 'BLEND'
        topLine.horizontalPositionMode = topLine.verticalPositionMode = 'PIXEL'
        topLine.widthMode = topLine.heightMode = 'PIXEL'
        topLine.horizontalAnchor = 'LEFT'
        topLine.verticalAnchor = 'TOP'
        topLine.width = self.WINDOW_WIDTH - 2 * self.TYPICAL_OFFSET
        topLine.height = 1
        topLine.position = (self.TYPICAL_OFFSET, self.CAPTION_HEIGHT, 0.1)
        self.component.addChild(topLine, 'topLine')
        middleLine = GUI.Simple('soGUI/maps/Colours/darkGrey.tga')
        middleLine.tiled = True
        middleLine.tileHeight = 1
        middleLine.tileWidth = 1
        middleLine.colour = (255, 255, 255, 255)
        middleLine.materialFX = 'BLEND'
        middleLine.horizontalPositionMode = middleLine.verticalPositionMode = 'PIXEL'
        middleLine.widthMode = middleLine.heightMode = 'PIXEL'
        middleLine.horizontalAnchor = 'LEFT'
        middleLine.verticalAnchor = 'TOP'
        middleLine.width = 1
        middleLine.height = self.WINDOW_HEIGHT - self.BOTTOM_OFFSET - self.CAPTION_HEIGHT
        middleLine.position = (self.RENDERFRAME_WIDTH + self.TYPICAL_OFFSET, self.CAPTION_HEIGHT, 0.1)
        self.component.addChild(middleLine, 'middleLine')
        underRenderLine = GUI.Simple('soGUI/maps/Colours/darkGrey.tga')
        underRenderLine.tiled = True
        underRenderLine.tileHeight = 1
        underRenderLine.tileWidth = 1
        underRenderLine.colour = (255, 255, 255, 255)
        underRenderLine.materialFX = 'BLEND'
        underRenderLine.horizontalPositionMode = underRenderLine.verticalPositionMode = 'PIXEL'
        underRenderLine.widthMode = underRenderLine.heightMode = 'PIXEL'
        underRenderLine.horizontalAnchor = 'LEFT'
        underRenderLine.verticalAnchor = 'TOP'
        underRenderLine.width = self.RENDERFRAME_WIDTH
        underRenderLine.height = 1
        underRenderLine.position = (self.TYPICAL_OFFSET, self.CAPTION_HEIGHT + self.RENDERFRAME_HEIGHT, 0.1)
        self.component.addChild(underRenderLine, 'underRenderLine')
        bottomLine = GUI.Simple('soGUI/maps/Colours/darkGrey.tga')
        bottomLine.tiled = True
        bottomLine.tileHeight = 1
        bottomLine.tileWidth = 1
        bottomLine.colour = (255, 255, 255, 255)
        bottomLine.materialFX = 'BLEND'
        bottomLine.horizontalPositionMode = bottomLine.verticalPositionMode = 'PIXEL'
        bottomLine.widthMode = bottomLine.heightMode = 'PIXEL'
        bottomLine.horizontalAnchor = 'LEFT'
        bottomLine.verticalAnchor = 'TOP'
        bottomLine.width = self.WINDOW_WIDTH - 2 * self.TYPICAL_OFFSET
        bottomLine.height = 1
        bottomLine.position = (self.TYPICAL_OFFSET, self.CAPTION_HEIGHT + self.RENDERFRAME_HEIGHT + self.INFOFRAME_HEIGHT + self.INFOWINDOW_HEIGHT + self.TYPICAL_OFFSET, 0.1)
        self.component.addChild(bottomLine, 'bottomLine')

    def setupCaption(self):
        charCaption = GUI.Text('')
        charCaption.verticalPositionMode = charCaption.horizontalPositionMode = 'CLIP'
        charCaption.horizontalAnchor = 'LEFT'
        charCaption.verticalAnchor = 'CENTER'
        charCaption.colour = (175, 166, 112, 255)
        charCaption.materialFX = 'BLEND'
        charCaption.font = 'ruRU_calibri_default.font'
        charCaption.text = get_entity_name(BigWorld.player(), utf8=True)
        charCaption.position = (-1.0 + soGUI.getPixelWidth(self.component) * 10, 1.0 - soGUI.getPixelHeight(self.component) * (self.CAPTION_HEIGHT / 2 + self.TYPICAL_OFFSET), 0.0)
        self.component.addChild(charCaption, 'charCaption')
        levelCaption = GUI.Text('')
        levelCaption.verticalPositionMode = levelCaption.horizontalPositionMode = 'CLIP'
        levelCaption.horizontalAnchor = 'LEFT'
        levelCaption.verticalAnchor = 'CENTER'
        levelCaption.colour = (175, 166, 112, 255)
        levelCaption.materialFX = 'BLEND'
        levelCaption.font = 'ruRU_calibri_default.font'
        levelCaption.text = u''
        levelCaption.position = (-1.0 + soGUI.getPixelWidth(self.component) * 150, 1.0 - soGUI.getPixelHeight(self.component) * (self.CAPTION_HEIGHT / 3 + self.TYPICAL_OFFSET), 0.0)
        self.component.addChild(levelCaption, 'levelCaption')
        classCaption = GUI.Text('')
        classCaption.verticalPositionMode = classCaption.horizontalPositionMode = 'CLIP'
        classCaption.horizontalAnchor = 'LEFT'
        classCaption.verticalAnchor = 'CENTER'
        classCaption.colour = (175, 166, 112, 255)
        classCaption.materialFX = 'BLEND'
        classCaption.font = 'ruRU_calibri_default.font'
        classCaption.text = u''
        classCaption.position = (-1.0 + soGUI.getPixelWidth(self.component) * 150, 1.0 - soGUI.getPixelHeight(self.component) * (self.CAPTION_HEIGHT / 3 * 2 + self.TYPICAL_OFFSET), 0.0)
        self.component.addChild(classCaption, 'classCaption')

    def setupFrames(self):
        windowFrame = GUI.Frame2('soGUI/maps/Controls/window_frame/genericWindowFrame2.tga')
        windowFrame.horizontalPositionMode = windowFrame.verticalPositionMode = 'CLIP'
        windowFrame.widthMode = windowFrame.heightMode = 'CLIP'
        windowFrame.verticalAnchor = 'CENTER'
        windowFrame.horizontalAnchor = 'CENTER'
        windowFrame.colour = (255, 255, 255, 255)
        windowFrame.materialFX = 'BLEND'
        windowFrame.width = 2.0
        windowFrame.height = 2.0
        windowFrame.position = (0.0, 0.0, 1.0)
        self.component.addChild(windowFrame, 'windowFrame')
        renderFrame = GUI.Frame2('soGUI/maps/Controls/window_frame/genericFrame.tga')
        renderFrame.horizontalPositionMode = renderFrame.verticalPositionMode = 'CLIP'
        renderFrame.widthMode = renderFrame.heightMode = 'PIXEL'
        renderFrame.verticalAnchor = 'TOP'
        renderFrame.horizontalAnchor = 'LEFT'
        renderFrame.colour = (255, 255, 255, 255)
        renderFrame.materialFX = 'BLEND'
        renderFrame.width = self.RENDERFRAME_WIDTH
        renderFrame.height = self.RENDERFRAME_HEIGHT
        renderFrame.position = (-1.0 + soGUI.getPixelWidth(self.component) * self.TYPICAL_OFFSET, 1.0 - soGUI.getPixelHeight(self.component) * self.CAPTION_HEIGHT, 0.0)
        self.component.addChild(renderFrame, 'renderFrame')

    def setupCharacterRender(self):
        renderTarget = GUI.Window()
        renderTarget.horizontalPositionMode = renderTarget.verticalPositionMode = 'CLIP'
        renderTarget.widthMode = renderTarget.heightMode = 'PIXEL'
        renderTarget.verticalAnchor = 'TOP'
        renderTarget.horizontalAnchor = 'LEFT'
        renderTarget.width = self.RENDERFRAME_WIDTH
        renderTarget.height = self.RENDERFRAME_HEIGHT
        renderTarget.colour = (255, 255, 255, 255)
        renderTarget.materialFX = 'BLEND'
        renderTarget.position = (-1.0 + soGUI.getPixelWidth(self.component) * self.TYPICAL_OFFSET, 1.0 - soGUI.getPixelHeight(self.component) * self.CAPTION_HEIGHT, 0.2)
        if self.characterRender is None:
            self.characterRender = BigWorld.PyModelRenderer(renderTarget.width, renderTarget.height)
        model_ref = StalkerModel.ComposePlayerModel(BigWorld.player())
        self.paperDoll = model_ref
        self.paperDoll.zoomExtents(True, 1.0)
        self.paperDoll.rotate(math.pi / 4.0 * 4, (0.0, 1.0, 0.0))
        self.paperDoll.rotate(math.pi / 6.0, (1.0, 0.0, 0.0))
        self.paperDoll.scale = (0.55, 0.5, 0.8)
        self.paperDoll.position = (0.0, 0.0, -0.5)
        autogunModel = BigWorld.player().getModelByNamesDict(BigWorld.player().GetEquippedItemModels(ItemsCatalog.ACTIVE))
        self.paperDoll.effectorright = autogunModel
        self.characterRender.dynamic = True
        self.characterRender.models = [self.paperDoll]
        if ItemsUtils.GetEquippedItemType(BigWorld.player()) != ItemsCatalog.NONE_TYPE:
            self.characterRender.models[0].Idle()
            pitchActionName = BigWorld.player().GetPitchActionName()
            pitchAction = self.characterRender.models[0].action(pitchActionName)
            pitchFrame = pitchAction.frameCount / 2
            pitchAction(0, None, 0, pitchFrame, pitchFrame)
            pitchActionName = BigWorld.player().GetPitchActionName()
            pitchAction = self.characterRender.models[0].action(pitchActionName)
            pitchFrame = pitchAction.frameCount / 2
            pitchAction(0, None, 0, pitchFrame, pitchFrame)
        else:
            self.characterRender.models[0].IdleUnarmed()
        self.characterRender.render()
        self.characterRender.addDirectionLight((1, 1, -1), (0.3, 0.3, 0.3, 1))
        self.characterRender.addDirectionLight((-1, -1, 1), (1, 1, 1, 1))
        renderTarget.texture = self.characterRender.texture
        self.component.addChild(renderTarget, 'char3D')
        return

    def playAnim(self, animType):
        self.characterRender.models[0].IdleForever()

    def onPaperDollLoaded(self):
        pass

    def setupCloseBox(self):
        closeBox = soButton(GUI.Window())
        cmp = closeBox.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 18
        cmp.position = (1.0 - soGUI.getPixelWidth(self.component) * self.TYPICAL_OFFSET, 1.0 - soGUI.getPixelHeight(self.component) * self.TYPICAL_OFFSET, 0.0)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')

    def setupItemFrame(self):

        def setupFilterFrame():
            filterHolder = GUI.Window()
            filterHolder.verticalPositionMode = filterHolder.horizontalPositionMode = 'CLIP'
            filterHolder.widthMode = filterHolder.heightMode = 'PIXEL'
            filterHolder.horizontalAnchor = 'RIGHT'
            filterHolder.verticalAnchor = 'TOP'
            filterHolder.width = self.FILTERFRAME_WIDTH
            filterHolder.height = self.FILTERFRAME_HEIGHT
            filterHolder.textureName = ''
            filterHolder.position = (1.0 - soGUI.getPixelWidth(self.component) * (self.SCROLL_WIDTH + self.TYPICAL_OFFSET), 1.0 - soGUI.getPixelHeight(self.component) * self.CAPTION_HEIGHT, 1.0)
            filterHolder.colour = (255, 255, 255, 255)
            filterHolder.materialFX = 'BLEND'
            self.component.addChild(filterHolder, 'filterTab')
            frame = GUI.Frame2('soGUI/maps/Controls/CharScreen/stats_head_frame.tga')
            frame.verticalPositionMode = frame.horizontalPositionMode = 'CLIP'
            frame.widthMode = frame.heightMode = 'CLIP'
            frame.horizontalAnchor = 'CENTER'
            frame.verticalAnchor = 'CENTER'
            frame.colour = (255, 255, 255, 255)
            frame.materialFX = 'BLEND'
            frame.width = 2.0
            frame.height = 2.0
            frame.position = (0.0, 0.0, 1.0)
            self.component.filterTab.addChild(frame, 'filterFrame')
            i = 0
            for filter in [self.FILTER_MISC,
             self.FILTER_CONSUMABLES,
             self.FILTER_ARMOR,
             self.FILTER_WEAPONS]:
                btn = soButton(GUI.Window())
                cmp = btn.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'RIGHT'
                cmp.verticalAnchor = 'CENTER'
                cmp.width = self.FILTERBTN_WIDTH
                cmp.height = self.FILTERBTN_HEIGHT
                cmp.position = (1.0 - soGUI.getPixelWidth(self.component.filterTab) * (self.FILTERBTN_WIDTH * i + self.TYPICAL_OFFSET), 0.0, 0.0)
                btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
                if filter == self.FILTER_WEAPONS:
                    btn.initVSC('soGUI/visual_styles/filterWeapons.xml')
                elif filter == self.FILTER_ARMOR:
                    btn.initVSC('soGUI/visual_styles/filterArmor.xml')
                elif filter == self.FILTER_CONSUMABLES:
                    btn.initVSC('soGUI/visual_styles/filterConsumables.xml')
                elif filter == self.FILTER_MISC:
                    btn.initVSC('soGUI/visual_styles/filterMisc.xml')
                else:
                    btn.initVSC('soGUI/visual_styles/filterBtn.xml')
                btn.onBound()
                self.component.filterTab.addChild(btn.component, 'filter' + str(filter))
                btn.setVisualState('normal')
                btn.onClick = partial(self.toggleFilter, filter)
                self.filterBtns[filter] = btn
                i += 1

        def setupItems():
            itemHolder = GUI.Window()
            itemHolder.horizontalPositionMode = itemHolder.verticalPositionMode = 'CLIP'
            itemHolder.widthMode = itemHolder.heightMode = 'PIXEL'
            itemHolder.verticalAnchor = 'TOP'
            itemHolder.horizontalAnchor = 'RIGHT'
            itemHolder.width = self.ITEM_WIDTH
            itemHolder.height = self.WINDOW_HEIGHT - self.CAPTION_HEIGHT - self.FILTERFRAME_HEIGHT - self.BOTTOM_OFFSET
            itemHolder.position = (1.0 - soGUI.getPixelWidth(self.component) * (self.SCROLL_WIDTH + self.TYPICAL_OFFSET), 1.0 - soGUI.getPixelHeight(self.component) * (self.CAPTION_HEIGHT + self.FILTERFRAME_HEIGHT), 0.2)
            itemHolder.textureName = ''
            itemHolder.scroll = (0.0, 0.0)
            self.component.addChild(itemHolder, 'itemsTab')
            for i in xrange(self.MAXIMUM_SLOTS):
                slot = soEquipSlot(GUI.Window())
                cmp = slot.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.width = self.ITEM_WIDTH
                cmp.height = self.ITEM_HEIGHT
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.position = (-1.0, 1.0 - soGUI.getPixelHeight(self.component.itemsTab) * self.ITEM_HEIGHT * i, 0.0)
                slot.setCounter(i)
                slot.iconWidth = self.ITEM_WIDTH
                slot.iconHeight = self.ITEM_HEIGHT
                slot.setIcon('soGUI/maps/Controls/listFrame.tga')
                self.slots.append(slot)
                self.component.itemsTab.addChild(cmp, 'slot' + str(i))

        setupFilterFrame()
        setupItems()

    def setupInfoFrame(self):

        def setupInfoTypeBar():
            infoTypeHolder = GUI.Window()
            infoTypeHolder.horizontalPositionMode = infoTypeHolder.verticalPositionMode = 'CLIP'
            infoTypeHolder.widthMode = infoTypeHolder.heightMode = 'PIXEL'
            infoTypeHolder.horizontalAnchor = 'LEFT'
            infoTypeHolder.verticalAnchor = 'TOP'
            infoTypeHolder.width = self.INFOFRAME_WIDTH
            infoTypeHolder.height = self.INFOFRAME_HEIGHT
            infoTypeHolder.position = (-1.0 + soGUI.getPixelWidth(self.component) * self.TYPICAL_OFFSET, 1.0 - soGUI.getPixelHeight(self.component) * (self.CAPTION_HEIGHT + self.RENDERFRAME_HEIGHT), 0.2)
            self.component.addChild(infoTypeHolder, 'infoTypeTab')
            infoTypeFrame = GUI.Frame2('soGUI/maps/Controls/CharScreen/stats_head_frame.tga')
            infoTypeFrame.horizontalPositionMode = infoTypeFrame.verticalPositionMode = 'CLIP'
            infoTypeFrame.widthMode = infoTypeFrame.heightMode = 'CLIP'
            infoTypeFrame.horizontalAnchor = 'CENTER'
            infoTypeFrame.verticalAnchor = 'CENTER'
            infoTypeFrame.width = 2.0
            infoTypeFrame.height = 2.0
            infoTypeFrame.position = (0.0, 0.0, 1.0)
            infoTypeFrame.colour = (255, 255, 255, 255)
            infoTypeFrame.materialFX = 'BLEND'
            self.component.infoTypeTab.addChild(infoTypeFrame, 'infoTypeFrame')
            infoTypeLabel = GUI.Text('')
            infoTypeLabel.horizontalPositionMode = infoTypeLabel.verticalPositionMode = 'CLIP'
            infoTypeLabel.horizontalAnchor = 'CENTER'
            infoTypeLabel.verticalAnchor = 'CENTER'
            infoTypeLabel.font = 'ruRU_calibri_default.font'
            infoTypeLabel.text = lc('soCharacterScreen.soGUI.STRING_639_24')
            infoTypeLabel.colour = (175, 166, 112, 255)
            infoTypeLabel.position = (0.0, 0.0, 1.0)
            self.component.infoTypeTab.addChild(infoTypeLabel, 'infoLabel')

        def setupInfoWindow():
            infoHolder = GUI.Window()
            infoHolder.horizontalPositionMode = infoHolder.verticalPositionMode = 'CLIP'
            infoHolder.widthMode = infoHolder.heightMode = 'PIXEL'
            infoHolder.horizontalAnchor = 'LEFT'
            infoHolder.verticalAnchor = 'BOTTOM'
            infoHolder.width = self.INFOWINDOW_WIDTH
            infoHolder.height = self.INFOWINDOW_HEIGHT
            infoHolder.position = (-1.0 + soGUI.getPixelWidth(self.component) * self.TYPICAL_OFFSET, -1.0 + soGUI.getPixelHeight(self.component) * (self.TYPICAL_OFFSET + self.BOTTOM_OFFSET), 0.0)
            self.component.addChild(infoHolder, 'infoTab')

        def setupCharStatsWnd():
            if self.statsWnd is not None:
                return
            else:
                self.statsWnd = GUI.Window()
                self.statsWnd.horizontalPositionMode = self.statsWnd.verticalPositionMode = 'CLIP'
                self.statsWnd.widthMode = self.statsWnd.heightMode = 'PIXEL'
                self.statsWnd.horizontalAnchor = 'LEFT'
                self.statsWnd.verticalAnchor = 'TOP'
                self.statsWnd.width = self.INFOWINDOW_WIDTH
                self.statsWnd.height = self.INFOWINDOW_HEIGHT
                self.statsWnd.position = (-1.0, 1.0, 0.0)
                self.statsWnd.textureName = ''
                self.statsWnd.colour = (255, 255, 255, 255)
                self.statsWnd.materialFX = 'BLEND'
                stats = BigWorld.player().GetAllStatsList()
                statsValues = {(0, 0): lc('soCharacterScreen.soGUI.STRING_693_13') + str(stats[0]),
                 (0, 1): lc('soCharacterScreen.soGUI.STRING_694_13') + str(stats[3]),
                 (1, 0): lc('soCharacterScreen.soGUI.STRING_695_13') + str(stats[1]),
                 (1, 1): lc('soCharacterScreen.soGUI.STRING_696_13') + str(stats[4]),
                 (2, 0): lc('soCharacterScreen.soGUI.STRING_697_13') + str(stats[2]),
                 (2, 1): lc('soCharacterScreen.soGUI.STRING_698_13') + str(stats[5])}
                for i in xrange(3):
                    for j in xrange(2):
                        statLabel = GUI.Text('')
                        statLabel.horizontalPositionMode = statLabel.verticalPositionMode = 'CLIP'
                        statLabel.horizontalAnchor = 'LEFT'
                        statLabel.verticalAnchor = 'TOP'
                        statLabel.font = 'ruRU_calibri_default.font'
                        statLabel.text = statsValues[i, j]
                        statLabel.colour = (175, 166, 112, 255)
                        statLabel.position = (-1.0 + soGUI.getPixelWidth(self.statsWnd) * self.TYPICAL_OFFSET, 1.0 - soGUI.getPixelHeight(self.statsWnd) * (self.INFOWINDOW_HEIGHT / 6 * (i * 2 + j) + self.TYPICAL_OFFSET), 1.0)
                        self.statsWnd.addChild(statLabel, 'stat' + str(i * 2 + j))

                return

        setupInfoTypeBar()
        setupInfoWindow()
        setupCharStatsWnd()
        self.component.infoTab.addChild(self.statsWnd, 'infoContent')

    def setupScroll(self):
        if not self.needScroll:
            return
        else:
            if self.vScroll is None:
                scrollComp = GUI.Window()
                self.vScroll = soScrollBar(scrollComp)
            self.vScroll.component.widthMode = self.vScroll.component.heightMode = 'PIXEL'
            self.vScroll.component.width = self.SCROLL_WIDTH
            self.vScroll.component.height = self.WINDOW_HEIGHT - self.CAPTION_HEIGHT - self.BOTTOM_OFFSET
            self.vScroll.component.horizontalAnchor = 'RIGHT'
            self.vScroll.component.verticalAnchor = 'TOP'
            self.vScroll.component.horizontalPositionMode = self.vScroll.component.verticalPositionMode = 'CLIP'
            self.vScroll.component.position = (1.0 - soGUI.getPixelWidth(self.component) * self.TYPICAL_OFFSET, 1.0 - soGUI.getPixelHeight(self.component) * self.CAPTION_HEIGHT, 0.2)
            self.vScroll.visible = True
            self.component.addChild(self.vScroll.component, 'vScroll')
            self.vScroll.initVSC('scripts/client/soGUI/schemas/soScrollBar_default.xml')
            self.vScroll.setVisualState('normal')
            self.vScroll.onBound()
            self.vScroll.makeLayout()
            self.vScroll.setupScrollingInfo(0)
            return

    def toggleFilter(self, filter):
        self.filterMask ^ filter

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'charScreen')
            self.applyItems()
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, self.interfaceID)
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, self.interfaceID)

    def applyStats(self):
        stats = BWPersonality.GUICore.charStatsDataSection
        if stats is None:
            return
        else:
            statsValues = {(0, 0): lc('soCharacterScreen.soGUI.STRING_775_12') + str(stats[0]),
             (0, 1): lc('soCharacterScreen.soGUI.STRING_776_12') + str(stats[3]),
             (1, 0): lc('soCharacterScreen.soGUI.STRING_777_12') + str(stats[1]),
             (1, 1): lc('soCharacterScreen.soGUI.STRING_778_12') + str(stats[4]),
             (2, 0): lc('soCharacterScreen.soGUI.STRING_779_12') + str(stats[2]),
             (2, 1): lc('soCharacterScreen.soGUI.STRING_780_12') + str(stats[5])}
            for i in xrange(3):
                for j in xrange(2):
                    cmp = self.statsWnd.__getattribute__('stat' + str(i * 2 + j))
                    cmp.text = statsValues[i, j]

            return

    def handleDragEnterEvent(self, comp, dragged):
        return True

    def handleDragLeaveEvent(self, comp, dragged):
        return True

    def handleDropEvent(self, component, dropped):
        if dropped.script.factoryString == 'soGUI.soInventorySlot':
            dropped.script.equip()
        elif isinstance(dropped.script, soInventorySlot2):
            dropped.script.equipItem()
        elif dropped.script.factoryString == 'soGUI.soEquipSlot':
            self.applyItems()
        return True

    def updateScroll(self):
        itemCount = 0
        for slot in self.slots:
            if slot.haveItem():
                itemCount += 1

        holderHeight = self.component.itemsTab.height
        screenH = BigWorld.screenHeight()
        self.scrollSteps = 0
        self.SCROLL_STEP = self.ITEM_HEIGHT / float(screenH) * 2.0

        def setMaxScroll():
            elementsHeight = self.ITEM_HEIGHT * itemCount
            heightDiff = elementsHeight - holderHeight
            self.scrollSteps = math.ceil(heightDiff / float(self.ITEM_HEIGHT))
            if heightDiff > 0:
                self.component.itemsTab.maxScroll.y = self.SCROLL_STEP * self.scrollSteps

        def setMinScroll():
            self.component.itemsTab.minScroll = (0.0, 0.0)

        setMaxScroll()
        setMinScroll()
        self.vScroll.setupScrollingInfo(self.scrollSteps)

    def handleMouseEvent(self, cmp, event):
        dx = event.dx
        dy = event.dy
        dz = event.dz
        position = event.cursorPosition
        if dz > 0:
            self.scrollUP()
            return True
        if dz < 0:
            self.scrollDN()
            return True
        return False

    def scrollUP(self):
        if self.component.itemsTab.scroll.y < self.component.itemsTab.minScroll.y:
            self.component.itemsTab.scroll.y = self.component.itemsTab.minScroll.y
        if self.component.itemsTab.scroll.y > self.component.itemsTab.minScroll.y:
            self.component.itemsTab.scroll.y -= self.SCROLL_STEP
            if self.component.itemsTab.scroll.y >= self.component.itemsTab.minScroll.y:
                self.vScroll.doStep(False)

    def scrollDN(self):
        if self.component.itemsTab.scroll.y > self.component.itemsTab.maxScroll.y:
            self.component.itemsTab.scroll.y = self.component.itemsTab.maxScroll.y
        if self.component.itemsTab.scroll.y < self.component.itemsTab.maxScroll.y:
            self.component.itemsTab.scroll.y += self.SCROLL_STEP
            self.vScroll.doStep(True)

    def applyItems(self):
        items = BigWorld.player().GetEquippedItemsList()
        for slot in self.slots:
            slot.empty(True)

        itemindex = 0
        for item in items:
            item_type = item['complexItemType']
            item_id = item['complexItemID']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            item_level = item_params['Level']
            cmp = self.component.itemsTab.__getattribute__('slot' + str(itemindex))
            cmp.script.setIcon(ItemsCatalog.GetItemParam(item['complexItemType'])['IconName'])
            cmp.script.setCounter(ItemsUtils.GetDisplayValue(item))
            cmp.script.setSlotInfo(item['complexItemID'])
            itemCondition = ItemsUtils.GetItemConditionPercentString(BigWorld.player(), ItemsUtils.GetComplexItemByID(BigWorld.player(), item_id))
            cmp.script.setItemCondition(itemCondition)
            shortName = BigWorld.player().GetItemName(item, fGetShortName=True)
            cmp.script.setItemString(shortName)
            itemindex += 1

        self.updateRender()
        self.updateScroll()
        self.component.charCaption.text = get_entity_name(BigWorld.player(), utf8=True)

    def updateRender(self):
        model_ref = StalkerModel.ComposePlayerModel(BigWorld.player())
        self.paperDoll = model_ref
        self.paperDoll.zoomExtents(True, 1.0)
        self.paperDoll.rotate(math.pi / 4.0 * 4, (0.0, 1.0, 0.0))
        self.paperDoll.rotate(math.pi / 6.0, (1.0, 0.0, 0.0))
        self.paperDoll.scale = (0.55, 0.5, 0.8)
        self.paperDoll.position = (0.0, 0.0, -0.5)
        autogunModel = BigWorld.player().getModelByNamesDict(BigWorld.player().GetEquippedItemModels(ItemsCatalog.ACTIVE))
        self.paperDoll.effectorright = autogunModel
        self.characterRender.models = [self.paperDoll]
        if ItemsUtils.GetEquippedItemType(BigWorld.player()) != ItemsCatalog.NONE_TYPE:
            self.characterRender.models[0].Idle()
            pitchActionName = BigWorld.player().GetPitchActionName()
            pitchAction = self.characterRender.models[0].action(pitchActionName)
            pitchFrame = pitchAction.frameCount / 2
            pitchAction(0, None, 0, pitchFrame, pitchFrame)
            pitchActionName = BigWorld.player().GetPitchActionName()
            pitchAction = self.characterRender.models[0].action(pitchActionName)
            pitchFrame = pitchAction.frameCount / 2
            pitchAction(0, None, 0, pitchFrame, pitchFrame)
        else:
            self.characterRender.models[0].IdleUnarmed()
        return

    @PyGUIEvent('vScroll', 'scrollUP')
    def scrolledUP(self):
        self.scrollUP()

    @PyGUIEvent('vScroll', 'scrollDN')
    def scrolledDN(self):
        self.scrollDN()

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()


class soRepElemFilter(soList2ElementBase):
    factoryString = 'soGUI.soRepElemFilter'
    EVENT_ACTIVATE = 0
    EVENT_DEACTIVATE = 1

    def __init__(self, component, id, data):
        soList2ElementBase.__init__(self, component, id, data)
        component.script = self

    def setupRoot(self):
        soList2ElementBase.setupRoot(self)
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 399
        cmp.height = 21
        cmp.position.x = 0
        cmp.position.z = 0.1
        cmp.horizontalAnchor = 'LEFT'

    def setupContent(self):
        btn = soButton(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 399
        cmp.height = 21
        cmp.position = (0, 0, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/repListFilterBtn.xml')
        btn.onBound()
        btn.buttonActive = True
        btn._updateVisualState()
        btn.onClick = self._btnHandler
        cmp.label.horizontalAnchor = 'LEFT'
        cmp.label.position.x = -0.8
        cmp.label.text = self.elemData['caption']
        self.component.addChild(cmp, 'btn')

    def _btnHandler(self):
        if self.component.btn.script.buttonActive:
            self.elementEvent(self.EVENT_ACTIVATE, self)
        else:
            self.elementEvent(self.EVENT_DEACTIVATE, self)

    def enable(self):
        self.component.btn.script.buttonDisabled = False
        self.component.btn.script._updateVisualState()
        return False

    def disable(self):
        self.component.btn.script.buttonDisabled = True
        self.component.btn.script._updateVisualState()
        return False

    def applyElemData(self):
        self.component.btn.label.text = self.elemData['caption']


class soRepElemProgress(soList2ElementBase):
    factoryString = 'soGUI.soRepElemProgress'
    EVENT_HIDEREP = 0
    EVENT_SHOWREP = 1
    EVENT_CONTEXT = 2
    EVENT_TTSHOW = 3
    EVENT_TTHIDE = 4

    def __init__(self, component, id, data):
        soList2ElementBase.__init__(self, component, id, data)
        component.script = self
        self.pressed = False
        self.lastPressed = 0

    def setupRoot(self):
        soList2ElementBase.setupRoot(self)
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 399
        cmp.height = 50
        cmp.position.x = 0
        cmp.position.z = 0.1
        cmp.horizontalAnchor = 'LEFT'
        cmp.mouseButtonFocus = True
        cmp.crossFocus = True

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/CharScreen/repElemFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 399
        cmp.height = 50
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'dFrame')
        cmp = GUI.Window('soGUI/maps/Controls/CharScreen/repProgress.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 379
        cmp.height = 11
        cmp.position = (10, 28, 0.5)
        self.component.addChild(cmp, 'pbar')
        cmp = GUI.Simple('soGUI/maps/Controls/CharScreen/slider.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 11
        cmp.height = 7
        cmp.position = (self.elemData['progress'], 1.0, 0.45)
        self.component.pbar.addChild(cmp, 'slider')
        cmp = GUI.Text('faction name')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.position = (32, 17, 0.45)
        cmp.text = self.elemData['name']
        self.component.addChild(cmp, 'fname')
        cmp = GUI.Text('0')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.position = (199, 35, 0.45)
        cmp.text = self.elemData['reputationPoints']
        self.component.addChild(cmp, 'repPoints')
        cmp = GUI.Text('relations')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
        cmp.position = (354, 17, 0.45)
        cmp.text = self.elemData['relations']
        self.component.addChild(cmp, 'frelations')
        btn = soButtonWTT(GUI.Window(''), 'hide_reputation')
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 9
        cmp.height = 9
        cmp.position = (13, 13, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/repListHide.xml')
        btn.onBound()
        btn.buttonActive = self.elemData['hidden']
        btn._updateVisualState()
        btn.onClick = self._hideRepHandler
        self.component.addChild(cmp, 'hideRep')

    def applyElemData(self):
        self.component.pbar.slider.position = (self.elemData['progress'], 1.0, 0.45)
        self.component.fname.text = self.elemData['name']
        self.component.frelations.text = self.elemData['relations']
        self.component.repPoints.text = self.elemData['reputationPoints']
        self.component.hideRep.script.buttonActive = self.elemData['hidden']
        self.component.hideRep.script._updateVisualState()

    def _hideRepHandler(self):
        if self.component.hideRep.script.buttonActive:
            self.elementEvent(self.EVENT_HIDEREP, self)
        else:
            self.elementEvent(self.EVENT_SHOWREP, self)

    def handleMouseLeaveEvent(self, cmp):
        self.elementEvent(self.EVENT_TTHIDE, self)
        return True

    def handleMouseEnterEvent(self, cmp):
        self.elementEvent(self.EVENT_TTSHOW, self)
        return True

    def handleMouseButtonEvent(self, cmp, event):
        if not event.isMouseButton():
            return False
        if event.isKeyDown():
            if event.key == KEY_LEFTMOUSE or event.key == KEY_RIGHTMOUSE:
                self.pressed = True
                if BigWorld.time() - self.lastPressed <= BWPersonality.GUICore.mouseDoubleClickSpeed:
                    self.onDblClick()
                self.lastPressed = BigWorld.time()
        if event.isKeyUp() and self.pressed:
            if event.key == KEY_LEFTMOUSE:
                self.onLClick()
            elif event.key == KEY_RIGHTMOUSE:
                self.onRClick()
        return True

    def onDblClick(self):
        return None

    def onLClick(self):
        return None

    def onRClick(self):
        self.elementEvent(self.EVENT_CONTEXT, self)


class soCharacterSlot(soItemSlot):
    factoryString = 'soGUI.soCharacterSlot'
    SLOTWIDTH = 64
    SLOTHEIGHT = 64

    def __init__(self, component, slotIndex, itemData = None, frameVisible = False):
        self.frameVisible = frameVisible
        soItemSlot.__init__(self, component, slotIndex, itemData, centerDProxy=True)
        component.script = self
        self.fake = False
        self.dragProxy = self.component.dragProxy
        self.proxyHolder = self.component
        self.proxyName = 'dragProxy'
        self._onDragStart = self.onDragStart
        self._onDragStop = self.onDragStop

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.dragFocus = True
        cmp.dropFocus = False
        cmp.crossFocus = True
        cmp.moveFocus = True
        cmp.mouseButtonFocus = True

    def setupContent(self):
        if self.frameVisible:
            cmp = GUI.Frame2('soGUI/maps/Controls/inventory/cellFrame2.tga')
            cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.width = self.SLOTWIDTH
            cmp.height = self.SLOTHEIGHT
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (0, 0, 0.9)
            self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 128)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.5)
        cmp.visible = False
        self.component.addChild(cmp, 'dragProxy')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = self.SLOTWIDTH
        cmp.height = self.SLOTHEIGHT
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (0, 0, 0.4)
        self.component.addChild(cmp, 'itemIcon')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (5, self.SLOTHEIGHT - 2, 0.3)
        self.component.addChild(cmp, 'itemName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (self.SLOTWIDTH - 5, 5, 0.3)
        self.component.addChild(cmp, 'itemCount')

    def _applyItemData(self):
        if self.haveItem():
            item_type = self.itemData['complexItemType']
            item_id = self.itemData['complexItemID']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            item_level = item_params['Level']
            iconName = item_params['IconName']
            if BWPersonality.GUICore.iconTextures is not None:
                if iconName not in BWPersonality.GUICore.iconTextures.failedIDs:
                    if BWPersonality.GUICore.iconTextures.has_key(iconName):
                        self.component.itemIcon.texture = BWPersonality.GUICore.iconTextures[iconName]
                    else:
                        self.component.itemIcon.textureName = iconName
            else:
                self.component.itemIcon.textureName = iconName
            countStr = ItemsUtils.GetDisplayValue(self.itemData)
            friendlyName = ItemsUtils.GetItemName(item_type, fGetShortName=True, tintItem=self.itemData)
            item_lock = BigWorld.player().ItemLocked(self.itemData)
            fake = BigWorld.player().IsItemFake(self.itemData)
            self.component.itemName.text = friendlyName
            self.component.itemCount.text = countStr
            self.lockSlot(item_lock)
            self.fakeSlot(fake)
        else:
            self.component.itemIcon.textureName = ''
            self.component.itemName.text = ''
            self.component.itemCount.text = ''
            self.lockSlot(False)
            self.fakeSlot(False)
        self.dragProxy.texture = self.component.itemIcon.texture
        return

    def unequip(self):
        BWPersonality.GUICore.charScreenEvent(soCharacterScreen2.EVENT_UNEQUIP, self.itemData)

    def onDragStart(self):
        if self.haveItem():
            self.dragProxy.visible = True
            return True
        return False

    def handleDragStartEvent(self, cmp):
        if self.fake:
            return False
        handled = soItemSlot.handleDragStartEvent(self, cmp)
        return handled

    def onDragStop(self):
        self.dragProxy.visible = False
        return True

    def fakeSlot(self, isFake = False):
        self.fake = isFake
        if self.fake:
            self.component.itemIcon.colour = (255, 255, 255, 128)
            self.component.itemName.visible = False
        else:
            self.component.itemIcon.colour = (255, 255, 255, 255)
            self.component.itemName.visible = True

    def lockSlot(self, doLock):
        soItemSlot.lockSlot(self, doLock)
        if self.locked:
            self.component.itemIcon.colour = (125, 125, 125, 255)
        else:
            self.component.itemIcon.colour = (255, 255, 255, 255)


class soCharacterScreen2(PyGUIBase):
    factoryString = 'soGUI.soCharacterScreen2'
    TAB_EQUIPMENT = 0
    TAB_REPUTATION = 1
    TAB_PVPSTATS = 2
    INDEX_FACE = 0
    INDEX_HEAD = 1
    INDEX_PRIMARY = 2
    INDEX_SECONDARY = 3
    INDEX_BACKPACK = 4
    INDEX_PALMS = 5
    INDEX_ARMOR = 6
    INDEX_CHEST = 7
    INDEX_UNDERWARE = 8
    INDEX_LEGS = 9
    INDEX_FEET = 10
    INDEX_ARTIFACT1 = 11
    INDEX_ARTIFACT2 = 12
    INDEX_ARTIFACT3 = 13
    INDEX_THROW = 14
    INDEX_NUM = 14
    EVENT_UNEQUIP = 0
    EVENT_USE = 1
    EVENT_CONTEXT = 2
    EVENT_REPAIR = 3
    EVENT_HIDEREP = 4
    EVENT_REPCONTEXT = 5
    CHARSTATID_STRENGTH = 0
    CHARSTATID_INTELLECT = 1
    CHARSTATID_DEXTIRITY = 2
    CHARSTATID_CONSTITUTION = 3
    CHARSTATID_PERCEPTION = 4
    CHARSTATID_PSIONICS = 5
    charStatsColMap = {'normal': Vector4(175, 166, 112, 255),
     'lowered': Vector4(145, 65, 50, 255),
     'buffed': Vector4(100, 140, 25, 255)}
    statsLabels = {CHARSTATID_STRENGTH: lc('GUI.CharacterGUI.CHARACTER_CHARACTERISTIC_STRENGTH'),
     CHARSTATID_INTELLECT: lc('GUI.CharacterGUI.CHARACTER_CHARACTERISTIC_INTELLIGENCE'),
     CHARSTATID_DEXTIRITY: lc('GUI.CharacterGUI.CHARACTER_CHARACTERISTIC_DEXTERITY'),
     CHARSTATID_CONSTITUTION: lc('GUI.CharacterGUI.CHARACTER_CHARACTERISTIC_CONSTITUTION'),
     CHARSTATID_PERCEPTION: lc('GUI.CharacterGUI.CHARACTER_CHARACTERISTIC_PERCEPTION'),
     CHARSTATID_PSIONICS: lc('GUI.CharacterGUI.CHARACTER_CHARACTERISTIC_PSIONICS')}
    tabLabels = {TAB_EQUIPMENT: lc('GUI.CharacterGUI.EQUIPMENT_TAB_LABEL'),
     TAB_REPUTATION: lc('GUI.CharacterGUI.REPUTATION_TAB_LABEL'),
     TAB_PVPSTATS: lc('GUI.CharacterGUI.PVP_STATISTICS_TAB_LABEL')}

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.interfaceID = BWPersonality.GUICore.GUI_ID_CHARSCREEN
        self.slots = {}
        self.statLabelCmps = {}
        self.pvpFlagTimer = 0
        self.pvpTicker = None
        self.repData = {}
        self.currentTab = self.TAB_EQUIPMENT
        self.setupRoot()
        self.setupContent()
        self.setupSlots()
        self.setupStats()
        self.setupTabBtns()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 427
        cmp.height = 579
        cmp.textureName = ''
        cmp.position = (0.0, 0.0, 0.5)
        cmp.visible = False

    def setupContent(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 497
        cmp.width = 427
        cmp.position = (0, 0, 0.9)
        self.component.addChild(cmp, 'mFrame')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (18, 6, 0.3)
        cmp.text = u''
        self.component.addChild(cmp, 'charName')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.1)
        self.component.addChild(cmp, 'wnd' + str(self.TAB_EQUIPMENT))
        eqWnd = cmp
        cmp = GUI.Frame2('soGUI/maps/Controls/CharScreen/eqDecFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 424
        cmp.width = 421
        cmp.position = (3, 50, 0.8)
        eqWnd.addChild(cmp, 'dFrame')
        cmp.dropFocus = True
        cmp.crossFocus = True
        cmp.dragFocus = True
        cmp.script = self
        cmp = GUI.Simple('soGUI/maps/Controls/CharScreen/char.jpg')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 394
        cmp.height = 404
        cmp.position = (13, 59, 0.7)
        eqWnd.addChild(cmp, 'charDoll')
        cmp = GUI.Window('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 200
        cmp.height = 93
        cmp.position = (10, 400, 0.85)
        eqWnd.addChild(cmp, 'artifactsWnd')
        cmp.dropFocus = True
        cmp.script = self
        artifactsMP = Matrix()
        artifactsMP.translation = (0.0, 0.0, 0.0)
        shader = GUI.MatrixShader()
        shader.eta = 0
        shader.blend = True
        shader.target = artifactsMP
        cmp.addShader(shader, 'mover')
        cmp = GUI.Frame2('soGUI/maps/Controls/CharScreen/eqBtFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 200
        cmp.height = 73
        cmp.position = (0, 0, 0.9)
        eqWnd.artifactsWnd.addChild(cmp, 'frame')
        btn = soButtonWFT(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.width = 74
        cmp.height = 21
        cmp.position = (10, 93, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/upturnedTab_charScreen.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = lc('GUI.CharacterGUI.ARTIFACTS_TAB_LABEL')
        eqWnd.artifactsWnd.addChild(cmp, 'artifactsTabBtn')
        cmp = GUI.Window('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 200
        cmp.height = 106
        cmp.position = (217, 387, 0.85)
        eqWnd.addChild(cmp, 'statsWnd')
        statsMP = Matrix()
        statsMP.translation = (0.0, 0.0, 0.0)
        shader = GUI.MatrixShader()
        shader.eta = 0
        shader.blend = True
        shader.target = statsMP
        cmp.addShader(shader, 'mover')
        cmp = GUI.Frame2('soGUI/maps/Controls/CharScreen/eqBtFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 200
        cmp.height = 86
        cmp.position = (0, 0, 0.9)
        eqWnd.statsWnd.addChild(cmp, 'frame')
        btn = soButtonWFT(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.width = 120
        cmp.height = 21
        cmp.position = (190, 106, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/upturnedTab_charScreen.xml')
        btn.onBound()
        btn.setVisualState('normal')
        cmp.label.text = lc('GUI.CharacterGUI.CHARACTERISTICS_TAB_LABEL')
        eqWnd.statsWnd.addChild(cmp, 'statsTabBtn')
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
        cmp.position = (403, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.1)
        cmp.visible = False
        self.component.addChild(cmp, 'wnd' + str(self.TAB_PVPSTATS))
        pvpWnd = cmp
        cmp = GUI.Frame2('soGUI/maps/Controls/CharScreen/eqDecFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 424
        cmp.width = 403
        cmp.position = (3, 50, 0.8)
        pvpWnd.addChild(cmp, 'dFrame')
        for i in xrange(5):
            cmp = GUI.Frame2('soGUI/maps/Controls/CharScreen/pvp_elem_frame.tga')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.height = 63
            cmp.width = 399
            cmp.position = (6, 53 + i * 65, 0.4)
            pvpWnd.addChild(cmp, 'elemFrame' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (13, 66 + i * 65, 0.3)
            pvpWnd.addChild(cmp, 'elem_1_' + str(i))
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'CENTER'
            cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
            cmp.colour = (175, 166, 112, 255)
            cmp.materialFX = 'BLEND'
            cmp.position = (200, 66 + i * 65, 0.3)
            pvpWnd.addChild(cmp, 'val_1_' + str(i))
            if i != 0:
                cmp = GUI.Text('')
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
                cmp.colour = (175, 166, 112, 255)
                cmp.materialFX = 'BLEND'
                cmp.position = (13, 83 + i * 65, 0.3)
                pvpWnd.addChild(cmp, 'elem_2_' + str(i))
                cmp = GUI.Text('')
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
                cmp.colour = (175, 166, 112, 255)
                cmp.materialFX = 'BLEND'
                cmp.position = (200, 83 + i * 65, 0.3)
                pvpWnd.addChild(cmp, 'val_2_' + str(i))
            else:
                cmp = GUI.Simple('soGUI/maps/Controls/CharScreen/progress_PvP_emp.tga')
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.width = 382
                cmp.height = 11
                cmp.position = (13, 81, 0.35)
                pvpWnd.addChild(cmp, 'pgBack')
                cmp = GUI.Simple('soGUI/maps/Controls/CharScreen/progress_PvP.tga')
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.width = 382
                cmp.height = 11
                cmp.position = (13, 81, 0.35)
                pvpWnd.addChild(cmp, 'elem_2_0')
                shader = GUI.ClipShader()
                shader.value = 1.0
                shader.speed = 0
                cmp.addShader(shader, 'clipper')
            if i != 1:
                cmp = GUI.Text('')
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
                cmp.colour = (175, 166, 112, 255)
                cmp.materialFX = 'BLEND'
                cmp.position = (13, 98 + i * 65, 0.3)
                pvpWnd.addChild(cmp, 'elem_3_' + str(i))
                cmp = GUI.Text('')
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.font = 'ruRU_Cyrvetica_Extra_14i.font'
                cmp.colour = (175, 166, 112, 255)
                cmp.materialFX = 'BLEND'
                cmp.position = (200, 98 + i * 65, 0.3)
                pvpWnd.addChild(cmp, 'val_3_' + str(i))

        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.1)
        cmp.visible = False
        self.component.addChild(cmp, 'wnd' + str(self.TAB_REPUTATION))
        repWnd = cmp
        cmp = GUI.Frame2('soGUI/maps/Controls/CharScreen/eqDecFrame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 421
        cmp.height = 444
        cmp.position = (3, 50, 0.8)
        repWnd.addChild(cmp, 'dFrame')
        repList = soList2(GUI.Window(), width=415, height=436, elemHandler=self._repElemHandler)
        cmp = repList.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (6, 54, 0.2)
        repWnd.addChild(cmp, 'repList')
        repList.onBound()

    def _repElemHandler(self, event, data):
        if isinstance(data, soRepElemFilter):
            if event == soRepElemFilter.EVENT_DEACTIVATE:
                repWnd = getattr(self.component, 'wnd' + str(self.TAB_REPUTATION))
                repList = repWnd.repList.script
                repList.removeElems(self.repData[data.id][0])
                self.repData[data.id][1] = True
            elif event == soRepElemFilter.EVENT_ACTIVATE:
                repWnd = getattr(self.component, 'wnd' + str(self.TAB_REPUTATION))
                repList = repWnd.repList.script
                idx = repList.getIndex(data.getID())
                repList.insertElems(idx + 1, self.repData[data.id][0])
                self.repData[data.id][1] = False
        if isinstance(data, soRepElemProgress):
            if event == soRepElemProgress.EVENT_CONTEXT:
                BWPersonality.GUICore.reputationEvent(self.EVENT_REPCONTEXT, data.getID())
            if event == soRepElemProgress.EVENT_TTSHOW:
                BWPersonality.GUICore.toolTipEvent(data.getID(), BWPersonality.GUICore.GUI_ID_REPSTATS, soToolTipComponent.EVENT_SHOW)
            if event == soRepElemProgress.EVENT_TTHIDE:
                BWPersonality.GUICore.toolTipEvent(data.getID(), BWPersonality.GUICore.GUI_ID_REPSTATS, soToolTipComponent.EVENT_HIDE)
            if event == soRepElemProgress.EVENT_HIDEREP:
                BWPersonality.GUICore.reputationEvent(self.EVENT_HIDEREP, [data.getID(), True])
            if event == soRepElemProgress.EVENT_SHOWREP:
                BWPersonality.GUICore.reputationEvent(self.EVENT_HIDEREP, [data.getID(), False])

    def setupTabBtns(self):
        btn = soButtonWFT(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 101
        cmp.height = 21
        cmp.position = (7, 30, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/charScreenTab.xml')
        btn.onBound()
        btn.buttonActive = True
        btn._updateVisualState()
        btn.onClick = partial(self._switchToTab, self.TAB_EQUIPMENT)
        cmp.label.text = self.tabLabels[self.TAB_EQUIPMENT]
        self.component.addChild(cmp, 'equipmentTab')
        btn = soButtonWFT(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 101
        cmp.height = 21
        cmp.position = (108, 30, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/charScreenTab.xml')
        btn.onBound()
        btn._updateVisualState()
        btn.onClick = partial(self._switchToTab, self.TAB_REPUTATION)
        cmp.label.text = self.tabLabels[self.TAB_REPUTATION]
        self.component.addChild(cmp, 'repTab')
        btn = soButtonWFT(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 101
        cmp.height = 21
        cmp.position = (209, 30, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/charScreenTab.xml')
        btn.onBound()
        btn._updateVisualState()
        btn.onClick = partial(self._switchToTab, self.TAB_PVPSTATS)
        cmp.label.text = self.tabLabels[self.TAB_PVPSTATS]
        self.component.addChild(cmp, 'pvpTab')

    def setupSlots(self):
        eqWnd = getattr(self.component, 'wnd' + str(self.TAB_EQUIPMENT))
        posMap = {self.INDEX_FACE: (55, 62, 0.5),
         self.INDEX_HEAD: (299, 60, 0.5),
         self.INDEX_SECONDARY: (13, 205, 0.5),
         self.INDEX_PRIMARY: (13, 137, 0.5),
         self.INDEX_BACKPACK: (46, 362, 0.5),
         self.INDEX_PALMS: (143, 398, 0.5),
         self.INDEX_ARMOR: (341, 135, 0.5),
         self.INDEX_CHEST: (341, 203, 0.5),
         self.INDEX_UNDERWARE: (341, 271, 0.5),
         self.INDEX_LEGS: (308, 362, 0.5),
         self.INDEX_FEET: (212, 398, 0.5),
         self.INDEX_THROW: (13, 273, 0.5)}
        for slotIndex in [self.INDEX_FACE,
         self.INDEX_HEAD,
         self.INDEX_SECONDARY,
         self.INDEX_PRIMARY,
         self.INDEX_BACKPACK,
         self.INDEX_PALMS,
         self.INDEX_ARMOR,
         self.INDEX_CHEST,
         self.INDEX_UNDERWARE,
         self.INDEX_LEGS,
         self.INDEX_FEET,
         self.INDEX_THROW]:
            slot = soCharacterSlot(GUI.Window(), slotIndex, None)
            slot.slotEvent = self._slotHandler
            cmp = slot.component
            cmp.position = posMap[slotIndex]
            eqWnd.addChild(cmp, 'slot' + str(slotIndex))
            self.slots[slotIndex] = slot

        for i, slotIndex in enumerate([self.INDEX_ARTIFACT1, self.INDEX_ARTIFACT2, self.INDEX_ARTIFACT3]):
            slot = soCharacterSlot(GUI.Window(), slotIndex, None, frameVisible=True)
            slot.slotEvent = self._slotHandler
            cmp = slot.component
            cmp.position = (4 + i * 64, 4, 0.3)
            eqWnd.artifactsWnd.addChild(cmp, 'slot' + str(slotIndex))
            self.slots[slotIndex] = slot

        return

    def setupStats(self):
        eqWnd = getattr(self.component, 'wnd' + str(self.TAB_EQUIPMENT))
        for i, statID in enumerate([self.CHARSTATID_STRENGTH,
         self.CHARSTATID_INTELLECT,
         self.CHARSTATID_DEXTIRITY,
         self.CHARSTATID_CONSTITUTION,
         self.CHARSTATID_PERCEPTION,
         self.CHARSTATID_PSIONICS]):
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = self.charStatsColMap['normal']
            cmp.materialFX = 'BLEND'
            cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
            cmp.text = self.statsLabels[statID]
            cmp.position = (8, 8 + i * 12, 0.5)
            eqWnd.statsWnd.addChild(cmp, 'stat' + str(statID))
            cmp.crossFocus = True
            cmp.script = self
            self.statLabelCmps[cmp] = statID
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'RIGHT'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = self.charStatsColMap['normal']
            cmp.materialFX = 'BLEND'
            cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
            cmp.text = u'0'
            cmp.position = (190, 8 + i * 12, 0.5)
            eqWnd.statsWnd.addChild(cmp, 'statValue' + str(statID))

    def _updateRepGroups(self, data):
        repWnd = getattr(self.component, 'wnd' + str(self.TAB_REPUTATION))
        repWnd.repList.script.clear()
        elems = []
        for group in data:
            elem = [group[0], soRepElemFilter, {'caption': group[1]}]
            elems.append(elem)
            self.repData[group[0]] = [[], False]

        repWnd.repList.script.addElems(elems)

    def _updateReps(self, data):
        repWnd = getattr(self.component, 'wnd' + str(self.TAB_REPUTATION))
        repList = repWnd.repList.script
        for repGroup in data:
            idx = repList.getIndex(repGroup)
            if idx is not None:
                elems = []
                self.repData[repGroup][0] = []
                if not len(data[repGroup]):
                    repList.disableElems([[repGroup]])
                else:
                    repList.enableElems([[repGroup]])
                for rep in data[repGroup]:
                    elem = [rep[0], soRepElemProgress, {'name': rep[1],
                      'relations': rep[2],
                      'progress': rep[3],
                      'hidden': rep[4],
                      'reputationPoints': rep[5]}]
                    elems.append(elem)
                    self.repData[repGroup][0].append(elem)

                if not self.repData[repGroup][1]:
                    repList.insertElems(idx + 1, elems)

        return

    def _updateRepData(self, data):
        repWnd = getattr(self.component, 'wnd' + str(self.TAB_REPUTATION))
        repList = repWnd.repList.script
        elems = []
        for rep in data:
            elem = [rep[0], {'name': rep[1],
              'relations': rep[2],
              'progress': rep[3],
              'hidden': rep[4]}]
            elems.append(elem)

        repList.updateElems(elems)

    def _updateItems(self, data):
        for index, item in enumerate(data):
            self.slots[index].setContent(item)

    def _updateName(self, data):
        self.component.charName.text = data

    def _updateStats(self, data):
        eqWnd = getattr(self.component, 'wnd' + str(self.TAB_EQUIPMENT))
        for index, stat in enumerate(data):
            valueLabel = getattr(eqWnd.statsWnd, 'statValue' + str(index), None)
            if valueLabel:
                valueLabel.text = str(stat[0])
                if stat[1] > 0:
                    valueLabel.colour = self.charStatsColMap['buffed']
                elif stat[1] < 0:
                    valueLabel.colour = self.charStatsColMap['lowered']
                else:
                    valueLabel.colour = self.charStatsColMap['normal']

        return

    def _updatePvP(self, data):
        pvpWnd = getattr(self.component, 'wnd' + str(self.TAB_PVPSTATS))
        getattr(pvpWnd, 'elem_1_' + str(1)).text = lc('soCharacterScreen.soGUI.killedInPVP')
        getattr(pvpWnd, 'val_1_' + str(1)).text = str(data[0])
        getattr(pvpWnd, 'val_1_' + str(1)).visible = 1
        getattr(pvpWnd, 'elem_1_' + str(1)).visible = 1
        getattr(pvpWnd, 'elem_1_' + str(2)).text = lc('soCharacterScreen.soGUI.killedInPK')
        getattr(pvpWnd, 'val_1_' + str(2)).text = str(data[1])
        getattr(pvpWnd, 'val_1_' + str(2)).visible = 1
        getattr(pvpWnd, 'elem_1_' + str(2)).visible = 1
        getattr(pvpWnd, 'elem_1_' + str(3)).text = lc('soCharacterScreen.soGUI.karma')
        getattr(pvpWnd, 'val_1_' + str(3)).text = str(data[2])
        getattr(pvpWnd, 'val_1_' + str(3)).visible = 1
        getattr(pvpWnd, 'elem_1_' + str(3)).visible = 1

    def _setPvPExpireTime(self, t):
        self.pvpFlagTimer = t
        if self.pvpTicker:
            self.pvpTicker.stop()
        self.pvpTicker = self.pvpFlagTicker()
        self.pvpTicker.run()

    def _extendArtifactsWnd(self, doExtend = True):
        eqWnd = getattr(self.component, 'wnd' + str(self.TAB_EQUIPMENT))
        sw, sh = BigWorld.screenSize()
        translation = (0.0, 0.0, 0.0)
        closedY = 400
        openedY = 473
        offset = 2.0 / (sh / (openedY - closedY))
        if doExtend:
            translation = (0.0, -offset, 0.0)
        eqWnd.artifactsWnd.mover.eta = 0.15
        eqWnd.artifactsWnd.mover.target.translation = translation

    def _extendStatsWnd(self, doExtend = True):
        eqWnd = getattr(self.component, 'wnd' + str(self.TAB_EQUIPMENT))
        sw, sh = BigWorld.screenSize()
        translation = (0.0, 0.0, 0.0)
        closedY = 387
        openedY = 473
        offset = 2.0 / (sh / (openedY - closedY))
        if doExtend:
            translation = (0.0, -offset, 0.0)
        eqWnd.statsWnd.mover.eta = 0.15
        eqWnd.statsWnd.mover.target.translation = translation

    def _toggleArtifactsWnd(self):
        eqWnd = getattr(self.component, 'wnd' + str(self.TAB_EQUIPMENT))
        self._extendArtifactsWnd(eqWnd.artifactsWnd.artifactsTabBtn.script.buttonActive)

    def _toggleStatsWnd(self):
        eqWnd = getattr(self.component, 'wnd' + str(self.TAB_EQUIPMENT))
        self._extendStatsWnd(eqWnd.statsWnd.statsTabBtn.script.buttonActive)

    def _switchToTab(self, tab):
        eqWnd = getattr(self.component, 'wnd' + str(self.TAB_EQUIPMENT))
        pvpWnd = getattr(self.component, 'wnd' + str(self.TAB_PVPSTATS))
        repWnd = getattr(self.component, 'wnd' + str(self.TAB_REPUTATION))
        self.component.equipmentTab.script.buttonActive = False
        self.component.repTab.script.buttonActive = False
        self.component.pvpTab.script.buttonActive = False
        eqWnd.visible = False
        if tab is self.TAB_EQUIPMENT:
            eqWnd.visible = True
            pvpWnd.visible = False
            repWnd.visible = False
            self.component.equipmentTab.script.buttonActive = True
        elif tab is self.TAB_PVPSTATS:
            eqWnd.visible = False
            pvpWnd.visible = True
            repWnd.visible = False
            self.component.pvpTab.script.buttonActive = True
        elif tab is self.TAB_REPUTATION:
            eqWnd.visible = False
            pvpWnd.visible = False
            repWnd.visible = True
            self.component.repTab.script.buttonActive = True
        self.component.equipmentTab.script._updateVisualState()
        self.component.repTab.script._updateVisualState()
        self.component.pvpTab.script._updateVisualState()
        if self.currentTab != tab:
            if self.currentTab == self.TAB_EQUIPMENT:
                BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, BWPersonality.GUICore.GUI_ID_CHARSCREEN)
            elif self.currentTab == self.TAB_PVPSTATS:
                BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, BWPersonality.GUICore.GUI_ID_REPSTATS)
            elif self.currentTab == self.TAB_REPUTATION:
                BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, BWPersonality.GUICore.GUI_ID_PVPSTATS)
            if tab == self.TAB_EQUIPMENT:
                BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, BWPersonality.GUICore.GUI_ID_CHARSCREEN)
            elif tab == self.TAB_PVPSTATS:
                BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, BWPersonality.GUICore.GUI_ID_REPSTATS)
            elif tab == self.TAB_REPUTATION:
                BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, BWPersonality.GUICore.GUI_ID_PVPSTATS)
        self.currentTab = tab

    def update(self):
        data = BWPersonality.GUICore.characterScreenDataSection
        if data.has_key('items'):
            self._updateItems(data['items'])
        if data.has_key('displayName'):
            self._updateName(data['displayName'])
        if data.has_key('charStats'):
            self._updateStats(data['charStats'])
        if data.has_key('pvp'):
            self._updatePvP(data['pvp'])
        if data.has_key('rep_groups'):
            self._updateRepGroups(data['rep_groups'])
        if data.has_key('rep_factions'):
            self._updateReps(data['rep_factions'])
        if data.has_key('rep_updates'):
            self._updateRepData(data['rep_updates'])

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'charScreen')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        if self.component.equipmentTab.script.buttonActive:
            BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, BWPersonality.GUICore.GUI_ID_CHARSCREEN)
        elif self.component.repTab.script.buttonActive:
            BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, BWPersonality.GUICore.GUI_ID_REPSTATS)
        elif self.component.pvpTab.script.buttonActive:
            BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, BWPersonality.GUICore.GUI_ID_PVPSTATS)
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        if self.component.equipmentTab.script.buttonActive:
            BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, BWPersonality.GUICore.GUI_ID_CHARSCREEN)
        elif self.component.repTab.script.buttonActive:
            BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, BWPersonality.GUICore.GUI_ID_REPSTATS)
        elif self.component.pvpTab.script.buttonActive:
            BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, BWPersonality.GUICore.GUI_ID_PVPSTATS)

    def _slotHandler(self, event, data):
        if event == module_soItemView.SLOTEVENT_RCLICK:
            BWPersonality.GUICore.charScreenEvent(self.EVENT_CONTEXT, data.itemData)
            return True
        if event == module_soItemView.SLOTEVENT_DBLCLICK:
            BWPersonality.GUICore.charScreenEvent(self.EVENT_USE, data.itemData)
            return True
        if event == module_soItemView.SLOTEVENT_LCLICK:
            if BWPersonality.GUICore.repairMode:
                BWPersonality.GUICore.charScreenEvent(self.EVENT_REPAIR, data.itemData)
                return True
        else:
            if event == module_soItemView.SLOTEVENT_MOUSEENTER:
                if BWPersonality.GUICore.repairMode and data.haveItem():
                    GUI.mcursor().shape = 'repair'
                BWPersonality.GUICore.toolTipEvent(data.itemData, self.interfaceID, soToolTipComponent.EVENT_SHOW)
                return True
            if event == module_soItemView.SLOTEVENT_MOUSELEAVE:
                GUI.mcursor().shape = 'arrow'
                BWPersonality.GUICore.toolTipEvent(data.itemData, self.interfaceID, soToolTipComponent.EVENT_HIDE)
                return True
        return False

    def handleDragEnterEvent(self, cmp, dragged):
        from soGUI.soInventoryScreen import soInventorySlot2
        if dragged.script is None:
            return False
        elif isinstance(dragged.script, soInventorySlot2):
            return True
        else:
            return False

    def handleDropEvent(self, cmp, dropped):
        from soGUI.soInventoryScreen import soInventorySlot2
        if dropped.script is None:
            return False
        elif isinstance(dropped.script, soInventorySlot2):
            dropped.script.equipItem()
            return True
        else:
            return False

    def handleMouseLeaveEvent(self, cmp):
        if cmp in self.statLabelCmps:
            BWPersonality.GUICore.toolTipEvent(self.statLabelCmps[cmp], self.interfaceID, soToolTipComponent.EVENT_HIDE)
        return True

    def handleMouseEnterEvent(self, cmp):
        if cmp in self.statLabelCmps:
            BWPersonality.GUICore.toolTipEvent(self.statLabelCmps[cmp], self.interfaceID, soToolTipComponent.EVENT_SHOW)
        return True

    def _alignWnd(self):
        sW, sH = BigWorld.screenSize()
        psX = (sW + self.component.width) / 2.0
        psY = (sH + self.component.height) / 2.0
        self.component.position = (psX, psY, 0.5)

    def timeToString(self, secs):
        if secs < 0:
            return u''
        hours = floor(secs / 3600.0)
        minutes = floor((secs - hours * 3600.0) / 60.0)
        seconds = secs - (hours * 3600.0 + minutes * 60.0)
        outH = str(int(hours)) if hours > 9 else u'0' + str(int(hours))
        outM = str(int(minutes)) if minutes > 9 else u'0' + str(int(minutes))
        outS = str(int(seconds)) if seconds > 9 else u'0' + str(int(seconds))
        return outH + u':' + outM + u':' + outS

    @BWMemberCoroutine
    def pvpFlagTicker(self):
        pvpWnd = getattr(self.component, 'wnd' + str(self.TAB_PVPSTATS))
        pvpWnd.val_2_1.text = self.timeToString(self.pvpFlagTimer)
        while self.pvpFlagTimer:
            yield BWWaitForPeriod(1.0)
            self.pvpFlagTimer -= 1
            pvpWnd.val_2_1.text = self.timeToString(self.pvpFlagTimer)

        pvpWnd.val_2_1.text = self.timeToString(self.pvpFlagTimer)
        self.pvpTicker = None
        return

    @PyGUIEvent('wnd' + str(TAB_EQUIPMENT) + '.artifactsWnd.artifactsTabBtn', 'onClick')
    def onArtifactsTabBtn(self):
        self._toggleArtifactsWnd()

    @PyGUIEvent('wnd' + str(TAB_EQUIPMENT) + '.statsWnd.statsTabBtn', 'onClick')
    def onStatsTabBtn(self):
        self._toggleStatsWnd()

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()