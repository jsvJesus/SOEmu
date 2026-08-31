# Embedded file name: scripts/client/soGUI/soInworldMarkers.py
import BigWorld
import GUI
import BWPersonality
import soGUI
import Helpers.PyGUI as PyGUI
import Math
from Math import Vector3
from math import cos
from math import sqrt
from math import pow
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.BWCoroutine import *
MAX_MARKERS = 30

class soInworldMarker(PyGUIBase):
    factoryString = 'soGUI.soInworldMarker'
    MARKER_PLAYER = 0
    MARKER_ITEM = 1
    MARKER_NPC = 2
    MARKER_PK = 100
    MARKER_WARDECLARED = 101
    MARKER_WARRECIEVED = 102
    MARKER_USE = 200
    MARKER_PICKUP = 201
    MARKER_TALK = 202
    MARKER_TRADE = 203
    MARKER_WANTED = 204
    FRAME_TEXTURE = BigWorld.PyTextureProvider('soGUI/maps/inworldMarkers/frame.tga')

    def __init__(self, component, ids = [MARKER_PLAYER], description = u'', alpha = 1.0):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.iconIDs = ids
        self.description = description
        self.alpha = alpha * 255.0
        self.setupRoot()
        self.setupMark()
        self.setupContent()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255,
         255,
         255,
         self.alpha)
        cmp.materialFX = 'BLEND'
        cmp.width = 0
        cmp.height = 0
        cmp.position = (0.0, 0.0, 1.5)
        cmp.textureName = ''

    def setupContent(self):
        iconHolder = None
        if len(self.iconIDs) > 0:
            cmp = GUI.Window('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = (255,
             255,
             255,
             self.alpha)
            cmp.materialFX = 'BLEND'
            cmp.width = 0
            cmp.height = 16
            cmp.position = (0.0, 1.0, 1.5)
            cmp.textureName = ''
            iconHolder = cmp
        for i, icon in enumerate(self.iconIDs):
            iconHolder.width += 16
            cmp = GUI.Simple('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 16
            cmp.height = 16
            cmp.colour = (255,
             255,
             255,
             self.alpha)
            cmp.materialFX = 'BLEND'
            cmp.position = (0 + i * 16, 0, 0.5)
            cmp.texture = soInworldMarkers.ICON_MAP[icon]
            iconHolder.addChild(cmp, 'icon' + str(i))

        if iconHolder:
            self.component.width = iconHolder.width
            self.component.height = iconHolder.height
            self.component.addChild(iconHolder, 'iconHolder')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (255,
         255,
         255,
         self.alpha)
        if self.MARKER_WANTED in self.iconIDs:
            cmp.colour = (255,
             150,
             150,
             self.alpha)
        cmp.colourFormatting = True
        cmp.multiline = True
        cmp.materialFX = 'BLEND'
        cmp.text = self.description
        calcStr = self.description
        colorCodes = []
        idx = 0
        while idx >= 0:
            idx = self.description.find(u'\\c', idx)
            if idx >= 0:
                colorCodes.append(idx)
                idx += 1

        for cc in colorCodes:
            calcStr = self.description[:cc] + self.description[cc + 11:]

        w, h = cmp.stringDimensions(calcStr)
        if w + 4 > self.component.width:
            self.component.width = w + 4
        if self.component.height > 0:
            self.component.height += h + 4
        else:
            self.component.height = h + 4
        vis_str = self.description.split('\n')
        for index, vis_part in enumerate(vis_str):
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'CENTER'
            cmp.verticalAnchor = 'BOTTOM'
            cmp.font = 'ruRU_calibri_default.font'
            cmp.colour = (255,
             255,
             255,
             self.alpha)
            if self.MARKER_WANTED in self.iconIDs:
                cmp.colour = (255,
                 150,
                 150,
                 self.alpha)
            cmp.colourFormatting = True
            cmp.multiline = True
            cmp.materialFX = 'BLEND'
            cmp.text = vis_part
            cmp.position = (self.component.width / 2, self.component.height - 2 - (len(vis_str) - (index + 1)) * (h / len(vis_str)), 0.5)
            self.component.addChild(cmp, 'description{0}'.format(index))

        cmp = GUI.Frame2('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.colour = (255,
         255,
         255,
         self.alpha)
        cmp.materialFX = 'BLEND'
        cmp.width = w + 4
        cmp.height = h + 4
        cmp.position = (self.component.width / 2, self.component.height, 1.0)
        cmp.texture = self.FRAME_TEXTURE
        self.component.addChild(cmp, 'backFrame')
        return

    def setupMark(self):
        self.clipMP = GUI.WorldToClipMP()
        shader = GUI.MatrixShader()
        shader.eta = 0
        shader.blend = True
        shader.target = self.clipMP
        self.component.addShader(shader, 'mover')

    def setMatrix(self, matrix):
        self.clipMP.target = matrix

    def setDescription(self, txt):
        pass

    def setDistance(self, dist):
        self.component.position.z = dist

    def fini(self):
        self.clearAllChildren(self.component)
        self.component.delShader('mover')
        self.component.script = None
        self.component = None
        self.clipMP = None
        return


class soInworldMarkers(PyGUIBase):
    factoryString = 'soGUI.soInworldMarkers'
    MAX_DISTANCE = 50.0
    MIN_DISTANCE = 0.0
    ICON_MAP = {soInworldMarker.MARKER_PLAYER: BigWorld.PyTextureProvider('soGUI/maps/inworldMarkers/player.tga'),
     soInworldMarker.MARKER_NPC: BigWorld.PyTextureProvider('soGUI/maps/inworldMarkers/NPC.tga'),
     soInworldMarker.MARKER_ITEM: BigWorld.PyTextureProvider('soGUI/maps/inworldMarkers/item.tga'),
     soInworldMarker.MARKER_USE: BigWorld.PyTextureProvider('soGUI/maps/inworldMarkers/use.tga'),
     soInworldMarker.MARKER_PICKUP: BigWorld.PyTextureProvider('soGUI/maps/inworldMarkers/pickUp.tga'),
     soInworldMarker.MARKER_TALK: BigWorld.PyTextureProvider('soGUI/maps/inworldMarkers/talk.tga'),
     soInworldMarker.MARKER_PK: BigWorld.PyTextureProvider('soGUI/maps/inworldMarkers/PK.tga'),
     soInworldMarker.MARKER_WARDECLARED: BigWorld.PyTextureProvider('soGUI/maps/inworldMarkers/declare_war.tga'),
     soInworldMarker.MARKER_WARRECIEVED: BigWorld.PyTextureProvider('soGUI/maps/inworldMarkers/recieve_war.tga'),
     soInworldMarker.MARKER_TRADE: BigWorld.PyTextureProvider('soGUI/maps/inworldMarkers/trade.tga'),
     soInworldMarker.MARKER_WANTED: BigWorld.PyTextureProvider('soGUI/maps/inworldMarkers/wanted.tga')}

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.markers = []
        self.setupRoot()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 1.1)
        cmp.visible = True
        BWPersonality.GUICore.worldLayer.addChild(cmp, 'inworldMarkers')

    def update(self):
        data = BWPersonality.GUICore.inworldMarkersDataSection[-MAX_MARKERS:]
        for marker in self.markers:
            self.component.delChild(marker.component)
            marker.fini()

        self.markers = []
        for marker in data:
            markerObj = soInworldMarker(GUI.Window(), marker[2], marker[0], marker[3])
            markerObj.onBound()
            cmp = markerObj.component
            self.markers.append(markerObj)
            self.component.addChild(cmp)
            markerObj.setMatrix(marker[1])

    def show(self):
        self.component.visible = True

    def hide(self):
        self.component.visible = False