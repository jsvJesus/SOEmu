# Embedded file name: scripts/client/soGUI/soGPSMap.py
from Localization import lc
import BigWorld
import GUI
import BWPersonality
import Helpers.PyGUI as PyGUI
import soGUI
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from soGUI.soTabletScreen import soTabletScreen
from soGUI.soToolTipComponent import soToolTipComponent
from copy import deepcopy
from soGUI.soPanComponent import soPanComponent
from soGUI.soButton import soButton, soButtonWTT
from Helpers.PyGUI import PyGUIEvent
from soGUI.soDropDownList import soDropDownList, soDropDownList2
from functools import partial
from MapNotes import MapNotes
from Helpers.BWCoroutine import *
from soGUI.data import GUIEvents
from gui_const import GUI_ID
from Keys import *

class soGPSMark(PyGUIBase, soToolTipComponent):
    factoryString = 'soGUI.soGPSMark'
    TYPEMAP = {MapNotes.TYPE_PLAYER: BigWorld.PyTextureProvider('soGUI/maps/Misc/mapMark_player.tga'),
     MapNotes.TYPE_WANTED: BigWorld.PyTextureProvider('soGUI/maps/Misc/mapMark_wanted.tga'),
     MapNotes.TYPE_CUSTOM: BigWorld.PyTextureProvider('soGUI/maps/Misc/mapMark_custom.tga'),
     MapNotes.TYPE_AREA: BigWorld.PyTextureProvider('soGUI/maps/Misc/mapMark_city.tga'),
     MapNotes.TYPE_AREA_AUTO: BigWorld.PyTextureProvider('soGUI/maps/Misc/mapMark_unlockPOI.tga'),
     MapNotes.TYPE_NPC: BigWorld.PyTextureProvider('soGUI/maps/Misc/mapMark_questNPC.tga'),
     MapNotes.TYPE_NPC_AUTO: BigWorld.PyTextureProvider('soGUI/maps/Misc/mapMark_questNPC.tga'),
     MapNotes.TYPE_RESPAWN_POINT: BigWorld.PyTextureProvider('soGUI/maps/Misc/mapMark_respawn.tga'),
     MapNotes.TYPE_UNCERTAIN_AREA: BigWorld.PyTextureProvider('soGUI/maps/Misc/uncertain_point/uncertainP.texanim')}
    HIGHLIGHT_TEXTURE = BigWorld.PyTextureProvider('soGUI/maps/Misc/highlighter.tga')
    APPEAR_SPEED = 0.1
    APPEAR_START_SCALE = 0.1
    APPEAR_END_SCALE = 1.0
    APPEAR_ANIM_FRAMECOUNT = 10

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        soToolTipComponent.__init__(self, component, None, None)
        self.tiptext1 = '!!!!!'
        component.script = self
        self.pressed = False
        self.markType = MapNotes.TYPE_CUSTOM
        self.direction = 0.0
        self.HLanim = None
        self.color = (255, 255, 255, 125)
        self.setupRoot()
        self.setupIcon()
        self.setupHighlighter()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 30
        cmp.height = 30
        cmp.crossFocus = False
        cmp.mouseButtonFocus = False
        cmp.moveFocus = False

    def setupIcon(self):
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 30
        cmp.height = 30
        cmp.position = (0.0, 0.0, 0.2)
        cmp.crossFocus = True
        cmp.mouseButtonFocus = True
        cmp.moveFocus = True
        cmp.script = self
        self.component.addChild(cmp, 'icon')

    def setupHighlighter(self):
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = self.color
        cmp.materialFX = 'BLEND'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.25)
        cmp.visible = False
        cmp.texture = self.HIGHLIGHT_TEXTURE
        self.component.addChild(cmp, 'hl')

    def setMarkInfo(self, id, type):
        self.toolTipID = id
        self.interfaceID = BWPersonality.GUICore.GUI_ID_PDAMAP
        self.id = id
        self.markType = type
        self.component.icon.texture = self.TYPEMAP[type]

    def setDirection(self, dir):
        self.direction = dir
        if self.markType is not MapNotes.TYPE_UNCERTAIN_AREA:
            self.component.widthMode = self.component.heightMode = 'PIXEL'
            self.component.width = self.component.height = 20
        else:
            w, h = self._calcHLSize()
            self.component.widthMode = self.component.heightMode = 'CLIP'
            self.component.width = w
            self.component.height = h

    def setColor(self, color):
        self.color = color
        if self.markType is MapNotes.TYPE_UNCERTAIN_AREA:
            self.component.hl.colour = color

    def isPlayer(self):
        if self.markType == MapNotes.TYPE_PLAYER:
            return True

    def getCoords(self):
        return (self.component.position.x, self.component.position.y)

    def handleMouseEnterEvent(self, component):
        if component is not self.component.icon:
            return False
        if self.markType is MapNotes.TYPE_UNCERTAIN_AREA:
            self.component.hl.visible = True
            self.HLanim = self.appearAnim()
            self.HLanim.run()
        self.pressed = self.pressed and BigWorld.isKeyDown(KEY_LEFTMOUSE)
        soToolTipComponent.handleMouseEnterEvent(self, component)
        return True

    def handleMouseLeaveEvent(self, component):
        if self.HLanim is not None:
            self.HLanim.stop()
            self.HLanim = None
        self.component.hl.visible = False
        soToolTipComponent.handleMouseLeaveEvent(self, component)
        return True

    def handleMouseButtonEvent(self, comp, event):
        key = event.key
        down = event.isKeyDown()
        if key == KEY_LEFTMOUSE:
            if down:
                self.onLeftClick()
        if key == KEY_RIGHTMOUSE:
            if down:
                self.onRightClick()
        return True

    def handleMouseEvent(self, comp, event):
        return True

    def onLeftClick(self):
        BWPersonality.GUICore.GPSEvent(soGUI.soGPSMap.EVENT_MARKLEFT, [self.id, self.markType])

    def onRightClick(self):
        BWPersonality.GUICore.GPSEvent(soGUI.soGPSMap.EVENT_MARKRIGHT, [self.id, self.markType])

    def _calcHLSize(self):
        parentSpace = self.component.parent.parent.script
        aspect = parentSpace.width / parentSpace.height
        zoom = parentSpace.zoomPresets[parentSpace.zoomPreset]
        width = self.direction * zoom
        height = self.direction * aspect * zoom
        return [width, height]

    @BWMemberCoroutine
    def appearAnim(self):
        curScale = self.APPEAR_START_SCALE
        step = (self.APPEAR_END_SCALE - self.APPEAR_START_SCALE) / float(self.APPEAR_ANIM_FRAMECOUNT)
        while curScale < self.APPEAR_END_SCALE:
            self.component.hl.width = 2.0 * curScale
            self.component.hl.height = 2.0 * curScale
            curScale += step
            yield BWWaitForPeriod(self.APPEAR_SPEED / float(self.APPEAR_ANIM_FRAMECOUNT))

        self.component.hl.width = 2.0
        self.component.hl.height = 2.0


class soSpaceMap(PyGUIBase, soPanComponent):
    factoryString = 'soGUI.soSpaceMap'

    def __init__(self, component, textureName, GPSobj, textureWidth = 100, textureHeight = 100, friendlyName = lc('soGPSMap.soGUI.STRING_208_19'), zoomPresets = [2.0, 1.0, 0.5], defaultPreset = 0, spaceID = None):
        PyGUIBase.__init__(self, component)
        soPanComponent.__init__(self, component)
        component.script = self
        self.width = textureWidth
        self.height = textureHeight
        self.spaceName = friendlyName
        self.texture = textureName
        self.spaceID = spaceID
        self.GPSparent = GPSobj
        self.zoomPresets = zoomPresets
        self.zoomPreset = defaultPreset
        self.viewAnchor = (0.0, 0.0)
        self.marks = {}
        soSpaceMap.setupRoot(self)
        self.setupMap()
        self.updateMap()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 786
        cmp.height = 483
        cmp.position = (393, 0, 0.2)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.visible = False
        cmp.mouseButtonFocus = True
        cmp.dragFocus = True

    def setupMap(self):
        cmp = GUI.Window()
        cmp.textureName = self.texture
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = self.width * self.zoomPresets[self.zoomPreset]
        cmp.height = self.height * self.zoomPresets[self.zoomPreset]
        cmp.position = (0.0, 0.0, 0.5)
        cmp.angle = 180
        cmp.flip = 1
        self.component.addChild(cmp, 'spaceMap')

    def addMark(self, id, type, coords, dir, col):
        mark = soGPSMark(GUI.Window())
        cmp = mark.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.position = (coords[0], coords[1], 0.2)
        self.component.spaceMap.addChild(cmp, 'mark' + str(id))
        self.marks[id] = cmp
        mark.setMarkInfo(id, type)
        mark.setDirection(dir)
        mark.setColor(col)

    def removeMark(self, id):
        if self.marks.has_key(id):
            self.marks[id].script.clearAllChildren(self.marks[id])
            self.marks[id].script = None
            self.component.spaceMap.delChild(self.marks[id])
            del self.marks[id]
            return True
        else:
            return False

    def updateMap(self):
        self.component.spaceMap.width = self.width * self.zoomPresets[self.zoomPreset]
        self.component.spaceMap.height = self.height * self.zoomPresets[self.zoomPreset]
        self.component.widthMode = self.component.heightMode = 'LEGACY'
        lW, lH = self.component.width, self.component.height
        self.component.widthMode = self.component.heightMode = 'PIXEL'
        self.component.spaceMap.widthMode = self.component.spaceMap.heightMode = 'LEGACY'
        mW, mH = self.component.spaceMap.width, self.component.spaceMap.height
        self.component.spaceMap.widthMode = self.component.spaceMap.heightMode = 'PIXEL'
        sW, sH = (2.0, 2.0)
        offsetW = (mW - lW) / sW
        offsetH = (mH - lH) / sH
        c_offsetW = mW / sW
        c_offsetH = mH / sH
        self.component.minScroll = (-offsetW, -offsetH)
        self.component.maxScroll = (offsetW, offsetH)
        self.centeringMinScroll = (-c_offsetW, -c_offsetH)
        self.centeringMaxScroll = (c_offsetW, c_offsetH)

    def updateMark(self, id, type, coords):
        cmp = self.marks[id]
        mark = cmp.script
        mark.setMarkInfo(id, type)
        cmp.position = (coords[0], coords[1], 0.2)

    def hasMark(self, id):
        if self.marks.has_key(id):
            return True
        else:
            return False

    def clearMarks(self):
        self.marks.clear()
        for mark in self.marks:
            self.component.spaceMap.delChild(self.marks[mark])

    def show(self):
        self.component.visible = True

    def hide(self):
        self.component.visible = False

    def handleMouseButtonEvent(self, comp, event):
        key = event.key
        down = event.isKeyDown()
        pos = event.cursorPosition
        handled = soPanComponent.handleMouseButtonEvent(self, comp, event)
        cmp = self.component.spaceMap
        cmp.widthMode = cmp.heightMode = 'CLIP'
        clipPos = cmp.screenToLocal((pos[0], pos[1]))
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        if key == KEY_RIGHTMOUSE:
            if down:
                BWPersonality.GUICore.GPSEvent(soGUI.soGPSMap.EVENT_MAPCONTEXT, (clipPos, self.spaceID))
        return True

    def zoomIn(self, fromBtn = False):
        if self.zoomPreset > 0:
            self.zoomPreset -= 1
            cmp = self.component.spaceMap
            if not fromBtn:
                mpos = GUI.mcursor().position
                cmp.widthMode = cmp.heightMode = 'CLIP'
                self.viewAnchor = cmp.screenToLocal((mpos[0], mpos[1]))
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                self.updateMap()
                self.GPSparent.centerOnMouse()
            else:
                self.component.widthMode = self.component.heightMode = 'CLIP'
                cmp.widthMode = cmp.heightMode = 'CLIP'
                sX, sY = self.component.localToScreen((0.0, 0.0))
                self.viewAnchor = cmp.screenToLocal((sX - self.component.scroll.x, sY - self.component.scroll.y))
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                self.component.widthMode = self.component.heightMode = 'PIXEL'
                self.updateMap()
                self.GPSparent.centerOnCenter()

    def zoomOut(self, fromBtn = False):
        if self.zoomPreset == len(self.zoomPresets) - 1:
            return
        checkZoom = self.zoomPresets[self.zoomPreset + 1]
        if self.width * checkZoom >= self.component.width and self.height * checkZoom >= self.component.height:
            self.zoomPreset += 1
            cmp = self.component.spaceMap
            if not fromBtn:
                mpos = GUI.mcursor().position
                cmp.widthMode = cmp.heightMode = 'CLIP'
                self.viewAnchor = cmp.screenToLocal((mpos[0], mpos[1]))
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                self.updateMap()
                self.GPSparent.centerOnMouse()
            else:
                self.component.widthMode = self.component.heightMode = 'CLIP'
                cmp.widthMode = cmp.heightMode = 'CLIP'
                sX, sY = self.component.localToScreen((0.0, 0.0))
                self.viewAnchor = cmp.screenToLocal((sX - self.component.scroll.x, sY - self.component.scroll.y))
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                self.component.widthMode = self.component.heightMode = 'PIXEL'
                self.updateMap()
                self.GPSparent.centerOnCenter()

    def getFriendlyName(self):
        return self.spaceName

    def handleMouseEvent(self, comp, event):
        handled = soPanComponent.handleMouseEvent(self, comp, event)
        dz = event.dz
        if dz < 0:
            self.zoomOut()
        if dz > 0:
            self.zoomIn()
        return handled

    def panUp(self):
        sW, sH = BigWorld.screenSize()
        dy = 25
        self.component.scroll.y -= 2.0 / (sH / dy)

    def panDown(self):
        sW, sH = BigWorld.screenSize()
        dy = -25
        self.component.scroll.y -= 2.0 / (sH / dy)

    def panLeft(self):
        sW, sH = BigWorld.screenSize()
        dx = -25
        self.component.scroll.x -= 2.0 / (sW / dx)

    def panRight(self):
        sW, sH = BigWorld.screenSize()
        dx = 25
        self.component.scroll.x -= 2.0 / (sW / dx)

    def fini(self):
        self.GPSparent = None
        return

    def handleMouseEnterEvent(self, comp):
        handled = soPanComponent.handleMouseEnterEvent(self, comp)
        return handled

    def handleMouseLeaveEvent(self, comp):
        handled = soPanComponent.handleMouseLeaveEvent(self, comp)
        return handled

    def handleDragStartEvent(self, *args):
        return False

    def handleDragStopEvent(self, *args):
        return False


class soGPSMap(PyGUIBase):
    factoryString = 'soGUI.soGPSMap'
    EVENT_MAPCONTEXT = 0
    EVENT_MARKLEFT = 1
    EVENT_MARKRIGHT = 2
    DIRECTION_UP = 0
    DIRECTION_RIGHT = 1
    DIRECTION_DOWN = 2
    DIRECTION_LEFT = 3
    currentMap = 'spaces/city_lubech'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        GOLD_STEPS = [6.967,
         5.041,
         3.648,
         2.64,
         1.91,
         1.382,
         1.0]
        self.MAPLIST = {'spaces/main': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/map_mainspace.dds', self, 1000, 1000, lc('soGPSMap.soGUI.STRING_500_104'), spaceID='spaces/main'),
         'spaces/so_origins': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_so_origins.dds', self, 500, 500, lc('soGPSMap.soGUI.STRING_501_113'), [ 1.572 * x for x in GOLD_STEPS[4:] ], 1, spaceID='spaces/so_origins'),
         'spaces/novaya': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_novaya.dds', self, 1400, 1400, lc('soGPSMap.soGUI.STRING_502_107'), [ 0.5615 * x for x in GOLD_STEPS[3:] ], 1, spaceID='spaces/novaya'),
         'spaces/tunguska': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_tunguska.dds', self, 2000, 2000, lc('soGPSMap.soGUI.STRING_503_111'), [ 0.393 * x for x in GOLD_STEPS[2:] ], 1, spaceID='spaces/tunguska'),
         'spaces/steppe': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_steppe.dds', self, 2000, 2000, lc('soGPSMap.soGUI.STRING_504_107'), [ 0.393 * x for x in GOLD_STEPS[2:] ], 1, spaceID='spaces/steppe'),
         'spaces/steppe_dust': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_steppe_dust.dds', self, 2000, 2000, lc('soGPSMap.soGUI.STRING_steppe_dust'), [ 0.393 * x for x in GOLD_STEPS[2:] ], 1, spaceID='spaces/steppe_dust'),
         'spaces/vesuvius': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_vesuvius.dds', self, 2500, 2500, lc('soGPSMap.soGUI.STRING_505_111'), [ 0.262 * x for x in GOLD_STEPS[1:] ], 2, spaceID='spaces/vesuvius'),
         'spaces/volcano': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_volkano.dds', self, 500, 500, lc('soGPSMap.soGUI.STRING_506_107'), [ 1.572 * x for x in GOLD_STEPS[4:] ], 2, spaceID='spaces/volcano'),
         'spaces/city_lubech': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_city_lubech.dds', self, 1500, 1500, lc('soGPSMap.soGUI.STRING_507_117'), [ 0.5615 * x for x in GOLD_STEPS[3:] ], -1, spaceID='spaces/city_lubech'),
         'spaces/outlands': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_outlands.dds', self, 4000, 4000, lc('soGPSMap.soGUI.STRING_508_112'), [ 0.1965 * x for x in GOLD_STEPS[0:] ], 2, spaceID='spaces/outlands'),
         'spaces/outlands_caravan': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_outlands_caravan.dds', self, 10000, 2000, lc('soGPSMap.soGUI.minimap_outlands_caravan'), [ 0.393 * x for x in GOLD_STEPS[0:] ], 1, spaceID='spaces/outlands_caravan'),
         'spaces/pk_prison01': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_pk_prison01.dds', self, 400, 400, lc('soGPSMap.soGUI.minimap_pk_prison01'), [ 1.572 * x for x in GOLD_STEPS[4:] ], 1, spaceID='spaces/pk_prison01'),
         'spaces/lubech_uderground': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_lubech_underground.dds', self, 512, 512, lc('soGPSMap.soGUI.minimap_lubech_underground'), [ 1.572 * x for x in GOLD_STEPS[4:] ], 2, spaceID='spaces/lubech_uderground'),
         'spaces/outlands_airport': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_outlands_airport.dds', self, 2000, 2000, lc('soGPSMap.soGUI.minimap_outlands_airport'), [ 0.393 * x for x in GOLD_STEPS[0:] ], 1, spaceID='spaces/outlands_airport'),
         'spaces/dm_outlands_village': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_dm_outlands_village.dds', self, 4000, 4000, lc('soGPSMap.soGUI.minimap_dm_outlands_village'), [ 0.393 * x for x in GOLD_STEPS[0:] ], 1, spaceID='spaces/dm_outlands_village'),
         'spaces/dm_rocks': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_dm_rocks.dds', self, 500, 500, lc('soGPSMap.soGUI.minimap_dm_rocks'), [ 0.393 * x for x in GOLD_STEPS[0:] ], 1, spaceID='spaces/dm_rocks'),
         'spaces/dm_ryabinushka': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_dm_ryabinushka.dds', self, 400, 800, lc('soGPSMap.soGUI.minimap_dm_ryabinushka'), [ 0.393 * x for x in GOLD_STEPS[0:] ], 1, spaceID='spaces/dm_ryabinushka'),
         'spaces/dm_snowland': soSpaceMap(GUI.Window(), 'soGUI/maps/worldMaps/minimap_dm_snowland.dds', self, 500, 500, lc('soGPSMap.soGUI.minimap_dm_snowland'), [ 0.393 * x for x in GOLD_STEPS[0:] ], 1, spaceID='spaces/dm_snowland')}
        self.maps = {}
        self.mapData = None
        self.charMap = 'spaces/so_origins'
        self.charData = None
        self.markData = {}
        self.setupRoot()
        self.setupMap()
        self.setupMapControls()
        self.setupStatusBar()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.width = 792
        cmp.height = 560
        cmp.position = (0.0, 0.0, 0.15)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.visible = False
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (14, 5, 0.3)
        cmp.text = lc('GUI.GPSMap.WINDOW_CAPTION')
        self.component.addChild(cmp, 'iLabel')

    def setupMapControls(self):
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 792
        cmp.height = 551
        cmp.position = (0, 0, 1.2)
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
        cmp.position = (786, 6, 0.2)
        self.component.addChild(cmp, 'closeBox')
        btn.onBound()
        btn._updateVisualState()
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/GPS_btns_small.xml')
        btn.onClick = partial(self.zoomHandler, 0)
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/GPS/zoomIn.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 25
        cmp.height = 25
        cmp.position = (735, 32, 0.1)
        self.component.addChild(cmp, 'zoomIn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/GPS_btns_small.xml')
        btn.onClick = partial(self.zoomHandler, 1)
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/GPS/zoomOut.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 25
        cmp.height = 25
        cmp.position = (760, 32, 0.1)
        self.component.addChild(cmp, 'zoomOut')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/GPS_btns_small.xml')
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/GPS/centerOnPlayer.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 25
        cmp.height = 25
        cmp.position = (700, 32, 0.1)
        self.component.addChild(cmp, 'centerOnPlayer')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/GPS_btns_small.xml')
        btn.onClick = partial(self.panBtnHandler, self.DIRECTION_UP)
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/GPS/arrow_up.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 25
        cmp.height = 25
        cmp.position = (384, 32, 0.1)
        self.component.addChild(cmp, 'panUp')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/GPS_btns_small.xml')
        btn.onClick = partial(self.panBtnHandler, self.DIRECTION_RIGHT)
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/GPS/arrow_right.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 25
        cmp.height = 25
        cmp.position = (761, 268, 0.1)
        self.component.addChild(cmp, 'panRight')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/GPS_btns_small.xml')
        btn.onClick = partial(self.panBtnHandler, self.DIRECTION_DOWN)
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/GPS/arrow_down.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 25
        cmp.height = 25
        cmp.position = (384, 487, 0.1)
        self.component.addChild(cmp, 'panDown')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        btn.initVSC('soGUI/visual_styles/GPS_btns_small.xml')
        btn.onClick = partial(self.panBtnHandler, self.DIRECTION_LEFT)
        cmp = btn.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.textureName = 'soGUI/maps/Controls/TabletPC/GPS/arrow_left.tga'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 25
        cmp.height = 25
        cmp.position = (6, 268, 0.1)
        self.component.addChild(cmp, 'panLeft')
        btn.onBound()
        btn.setVisualState('normal')
        ddl = soDropDownList2(GUI.Window(), width=140, height=25)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (547, 32, 0.1)
        self.component.addChild(cmp, 'maps')
        ddl.onBound()
        maps = []
        for mapID in self.MAPLIST:
            map = [mapID, self.MAPLIST[mapID].getFriendlyName()]
            maps.append(map)

        if maps:
            ddl.addElements(maps)

    def setupMap(self):
        cmp = GUI.Window('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 786
        cmp.height = 491
        cmp.position = (3, 30, 0.2)
        cmp.textureName = ''
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'mapHolder')
        for map in self.MAPLIST:
            self.component.mapHolder.addChild(self.MAPLIST[map].component, map)
            self.maps[map] = self.MAPLIST[map].component

    def setupStatusBar(self):
        pass

    def viewMap(self, space = 'spaces/city_lubech'):
        if not self.maps.has_key(space):
            return False
        for map in self.maps:
            self.maps[map].script.hide()

        self.maps[space].script.show()
        soGPSMap.currentMap = space
        self.component.maps.script.setSelectionByValue(space, silent=True)
        return True

    def updatePlayer(self, oldData):
        self.maps[oldData['charSpace']].script.removeMark()

    def update(self):
        data = BWPersonality.GUICore.gpsDataSection
        SPACENAME = 0
        TYPE = 1
        COORDS = 2
        DIR = 3
        COL = 4
        if data.has_key('marks'):
            if self.markData != data['marks']:
                for markID in self.markData:
                    if not data['marks'].has_key(markID):
                        if self.MAPLIST.has_key(self.markData[markID][SPACENAME]):
                            self.maps[self.markData[markID][SPACENAME]].script.removeMark(markID)

                for markID in data['marks']:
                    if not self.MAPLIST.has_key(data['marks'][markID][SPACENAME]):
                        continue
                    if data['marks'][markID][TYPE] == MapNotes.TYPE_PLAYER:
                        self.charMap = data['marks'][markID][SPACENAME]
                    if self.markData.has_key(markID):
                        if self.markData[markID] != data['marks'][markID]:
                            if self.MAPLIST.has_key(self.markData[markID][SPACENAME]):
                                self.maps[self.markData[markID][SPACENAME]].script.removeMark(markID)
                            self.markData[markID] = deepcopy(data['marks'][markID])
                            if self.MAPLIST.has_key(self.markData[markID][SPACENAME]):
                                self.maps[self.markData[markID][SPACENAME]].script.addMark(markID, self.markData[markID][TYPE], self.markData[markID][COORDS], self.markData[markID][DIR], self.markData[markID][COL])
                    else:
                        self.markData[markID] = deepcopy(data['marks'][markID])
                        if self.MAPLIST.has_key(self.markData[markID][SPACENAME]):
                            self.maps[self.markData[markID][SPACENAME]].script.addMark(markID, self.markData[markID][TYPE], self.markData[markID][COORDS], self.markData[markID][DIR], self.markData[markID][COL])

        if data.has_key('spaces'):
            maps = []
            for mapID in data['spaces']:
                if not self.MAPLIST.has_key(mapID):
                    continue
                map = [mapID, self.MAPLIST[mapID].getFriendlyName()]
                maps.append(map)

            if maps:
                self.component.maps.script.clear()
                self.component.maps.script.addElements(maps)

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'gpsMap')
        BWPersonality.GUICore.setBestCursor()
        if BWPersonality.GUICore.gpsDataSection is not None:
            self.viewMap(self.charMap)
        else:
            self.viewMap('spaces/city_lubech')
        self.component.visible = True
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_SHOW, GUI_ID.GUI_ID_GPSMAP)
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.generalGUIEvent(GUIEvents.EVENT_HIDE, GUI_ID.GUI_ID_GPSMAP)

    def panBtnHandler(self, dir = 0):
        if dir == self.DIRECTION_UP:
            self.MAPLIST[soGPSMap.currentMap].panUp()
        if dir == self.DIRECTION_DOWN:
            self.MAPLIST[soGPSMap.currentMap].panDown()
        if dir == self.DIRECTION_LEFT:
            self.MAPLIST[soGPSMap.currentMap].panLeft()
        if dir == self.DIRECTION_RIGHT:
            self.MAPLIST[soGPSMap.currentMap].panRight()

    def zoomHandler(self, dir = 0):
        if dir:
            self.MAPLIST[soGPSMap.currentMap].zoomOut(True)
        else:
            self.MAPLIST[soGPSMap.currentMap].zoomIn(True)

    def centerOnCoords(self, coords, charMap):
        charMap = self.MAPLIST[charMap]
        if coords[0] <= 0:
            hTScroll = charMap.centeringMinScroll[0] * coords[0]
        else:
            hTScroll = charMap.centeringMaxScroll[0] * coords[0]
            hTScroll *= -1.0
        if coords[1] <= 0:
            vTScroll = charMap.centeringMinScroll[1] * coords[1]
            vTScroll *= -1.0
        else:
            vTScroll = charMap.centeringMaxScroll[1] * coords[1]
        charMap.component.scroll = (hTScroll, -vTScroll)

    def centerOnPlayer(self):
        if self.charMap:
            self.viewMap(self.charMap)
        else:
            return
        charMark = None
        charMap = self.MAPLIST[self.charMap]
        for mark in charMap.marks:
            if charMap.marks[mark].script.isPlayer():
                charMark = charMap.marks[mark].script

        if not charMark:
            return
        else:
            coords = charMark.getCoords()
            if coords[0] <= 0:
                hTScroll = charMap.centeringMinScroll[0] * coords[0]
            else:
                hTScroll = charMap.centeringMaxScroll[0] * coords[0]
                hTScroll *= -1.0
            if coords[1] <= 0:
                vTScroll = charMap.centeringMinScroll[1] * coords[1]
                vTScroll *= -1.0
            else:
                vTScroll = charMap.centeringMaxScroll[1] * coords[1]
            charMap.component.scroll = (hTScroll, -vTScroll)
            return

    def centerOnMouse(self):
        currMap = self.MAPLIST[soGPSMap.currentMap]
        cmp = currMap.component.spaceMap
        cmp.widthMode = cmp.heightMode = 'CLIP'
        pos = currMap.viewAnchor
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        if pos[0] <= 0:
            hTScroll = currMap.centeringMinScroll[0] * pos[0]
        else:
            hTScroll = currMap.centeringMaxScroll[0] * pos[0]
            hTScroll *= -1.0
        if pos[1] <= 0:
            vTScroll = currMap.centeringMinScroll[1] * pos[1]
            vTScroll *= -1.0
        else:
            vTScroll = currMap.centeringMaxScroll[1] * pos[1]
        currMap.component.scroll = (hTScroll, -vTScroll)

    def centerOnCenter(self):
        currMap = self.MAPLIST[soGPSMap.currentMap]
        cmp = currMap.component.spaceMap
        cmp.widthMode = cmp.heightMode = 'CLIP'
        pos = currMap.viewAnchor
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        if pos[0] <= 0:
            hTScroll = currMap.centeringMinScroll[0] * pos[0]
        else:
            hTScroll = currMap.centeringMaxScroll[0] * pos[0]
            hTScroll *= -1.0
        if pos[1] <= 0:
            vTScroll = currMap.centeringMinScroll[1] * pos[1]
            vTScroll *= -1.0
        else:
            vTScroll = currMap.centeringMaxScroll[1] * pos[1]
        currMap.component.scroll = (hTScroll, -vTScroll)

    def fini(self):
        soGPSMark.TYPEMAP = None
        for spaceMap in self.MAPLIST:
            self.MAPLIST[spaceMap].fini()

        soGPSMap.MAPLIST = None
        return

    @PyGUIEvent('centerOnPlayer', 'onClick')
    def centerBtnClick(self):
        self.centerOnPlayer()

    @PyGUIEvent('maps', 'onSelectedElement')
    def onSpaceClick(self, mapID):
        self.viewMap(mapID)

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()