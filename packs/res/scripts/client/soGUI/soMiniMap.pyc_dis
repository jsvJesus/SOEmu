# Embedded file name: scripts/client/soGUI/soMiniMap.py
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
from functools import partial
from soGUI.soButton import soButton
import BWPersonality
import traceback
from Settings import Settings
from Helpers.BWCoroutine import *

class soMiniMap(PyGUI.Window):
    factoryString = 'soGUI.soMiniMap'
    safeZones = []
    space_infos = {'spaces/so_origins': [(500, -500), 'soGUI/maps/worldMaps/minimap_so_origins.dds', (50, 50)],
     'spaces/outlands': [(4000, -4000), 'soGUI/maps/worldMaps/minimap_outlands.dds', (0, 0)],
     'spaces/city_lubech': [(1500, -1500), 'soGUI/maps/worldMaps/minimap_city_lubech.dds', (50, 50)],
     'spaces/lubech_uderground': [(512, -512), 'soGUI/maps/worldMaps/minimap_lubech_underground.dds', (50, 50)],
     'spaces/vesuvius': [(2500, -2500), 'soGUI/maps/worldMaps/minimap_vesuvius.dds', (50, 50)],
     'spaces/volcano': [(500, -500), 'soGUI/maps/worldMaps/minimap_volkano.dds', (50, 50)],
     'spaces/novaya': [(1400, -1400), 'soGUI/maps/worldMaps/minimap_novaya.dds', (0, 0)],
     'spaces/tunguska': [(2000, -2000), 'soGUI/maps/worldMaps/minimap_tunguska.dds', (0, 0)],
     'spaces/steppe': [(2000, -2000), 'soGUI/maps/worldMaps/minimap_steppe.dds', (0, 0)],
     'spaces/steppe_dust': [(2000, -2000), 'soGUI/maps/worldMaps/minimap_steppe_dust.dds', (0, 0)],
     'spaces/zoo': [(1000, -1000), 'soGUI/maps/worldMaps/map_mainspace.dds', (0, 0)],
     'spaces/zoo2': [(1000, -1000), 'soGUI/maps/worldMaps/map_mainspace.dds', (0, 0)],
     'spaces/main': [(1000, -1000), 'soGUI/maps/worldMaps/map_mainspace.dds', (0, 0)],
     'spaces/anomaly': [(1000, -1000), 'soGUI/maps/worldMaps/map_mainspace.dds', (0, 0)],
     'spaces/pk_prison01': [(400, -400), 'soGUI/maps/worldMaps/minimap_pk_prison01.dds', (0, 0)],
     'spaces/outlands_caravan': [(10000, -2000), 'soGUI/maps/worldMaps/minimap_outlands_caravan.dds', (0, 0)],
     'spaces/outlands_airport': [(2000, -2000), 'soGUI/maps/worldMaps/minimap_outlands_airport.dds', (0, 0)],
     'spaces/dm_outlands_village': [(4000, -4000), 'soGUI/maps/worldMaps/minimap_dm_outlands_village.dds', (0, 0)],
     'spaces/dm_rocks': [(500, -500), 'soGUI/maps/worldMaps/minimap_dm_rocks.dds', (50, 50)],
     'spaces/dm_ryabinushka': [(400, -800), 'soGUI/maps/worldMaps/minimap_dm_ryabinushka.dds', (0, 0)],
     'spaces/dm_snowland': [(500, -500), 'soGUI/maps/worldMaps/minimap_dm_snowland.dds', (50, 50)]}
    frame_textures = {'maximized': BigWorld.PyTextureProvider('soGUI/maps/minimap/frame.tga'),
     'minimized': BigWorld.PyTextureProvider('soGUI/maps/minimizedMMapFrame.tga')}

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        self.component.script = self
        self.playerIcon = None
        self.pIconID = -1
        self.setupRoot()
        self.setupMap()
        return

    def setupRoot(self):
        sW, sH = BigWorld.screenSize()
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 230
        cmp.height = 230
        cmp.position = (sW - 10, 10, 0.5)
        cmp.textureName = ''
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        BWPersonality.GUICore.worldLayer.addChild(cmp, 'minimap')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.1)
        cmp.visible = True
        cmp.texture = self.frame_textures['maximized']
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.component.addChild(cmp, 'border')
        btn = soButton(GUI.Window(''))
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 10
        cmp.height = 6
        cmp.position = (213, 4, 0.05)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/minimapMinimizeBtn.xml')
        btn.onBound()
        btn.buttonActive = True
        btn._updateVisualState()
        btn.onClick = self._minimizeBtnHandler
        self.component.addChild(cmp, 'minBtn')

    def setupMap(self):
        cmp = GUI.Simple('soGUI/maps/AvatarMiniMapIcon.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.width = 0.3
        cmp.height = 0.3
        cmp.position = (0.0, 0.0, 0.1)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        self.playerIcon = cmp
        self.component.addChild(cmp, 'playerIcon')
        cmp = GUI.Minimap()
        cmp.maskName = 'soGUI/maps/miniMapMask.tga'
        cmp.range = 200
        cmp.script = self
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.width = 230
        cmp.height = 230
        cmp.position = (0.0, 0.0, 0.5)
        cmp.rotate = False
        self.worldMapWidth = 9600
        self.worldMapHeight = -9600
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.simpleEntrySize = 7
        cmp.simpleEntryMap = 'soGUI/maps/AvatarMiniMapIcon.tga'
        cmp.textureName = 'soGUI/maps/Colours/black.bmp'
        self.component.addChild(cmp, 'map')

    @BWCoroutine
    def addPlayerIcon(self):
        while True:
            yield BWWaitForPeriod(0.1)
            try:
                self.pIconID = self.component.map.add(BigWorld.player().matrix, self.component.playerIcon)
                break
            except Exception as e:
                traceback.print_exc()
                continue

    def delPlayerIcon(self):
        if self.pIconID != -1:
            self.component.map.remove(self.pIconID)

    def changeMap(self, mapName):
        if not self.space_infos.has_key(mapName):
            return False
        self.component.map.delAllTextureLayers()
        texProv = BigWorld.PyTextureProvider(self.space_infos[mapName][1])
        self.component.map.addTextureLayer(1, texProv, self.space_infos[mapName][0], self.space_infos[mapName][2])
        try:
            if Settings().getSetting('minimapMinimize'):
                self.minimize()
            else:
                self.maximize()
        except Exception as e:
            traceback.print_exc()

        return True

    def addSafeZone(self, matrix, radius):
        safeZone = GUI.Simple('soGUI/maps/Misc/safeZone.bmp')
        safeZone.materialFX = 'BLEND'
        self.component.add(matrix, safeZone)

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.position = (sW - 10, 10, 0.5)

    def _minimizeBtnHandler(self):
        if self.component.minBtn.script.buttonActive:
            self.maximize()
        else:
            self.minimize()

    def bindToPlayer(self):
        self.component.map.viewpoint = BigWorld.player().matrix
        self.component.map.script.addPlayerIcon(self).run()

    def unbind(self):
        pass

    def fini(self):
        pass

    def minimize(self):
        self.component.height = 27
        self.component.border.texture = self.frame_textures['minimized']
        self.delPlayerIcon()
        self.playerIcon.visible = False
        self.component.map.visible = False
        BWPersonality.GUICore.systemMenu.doReposition()
        Settings().setSetting('minimapMinimize', True, True)

    def maximize(self):
        self.component.height = 230
        self.component.border.texture = self.frame_textures['maximized']
        self.addPlayerIcon(self).run()
        self.playerIcon.visible = True
        self.component.map.visible = True
        BWPersonality.GUICore.systemMenu.doReposition()
        Settings().setSetting('minimapMinimize', False, True)