# Embedded file name: scripts/client/soGUI/soIncomingDamageGUI.py
import BigWorld
import GUI
import BWPersonality
import Helpers.PyGUI as PyGUI
import soGUI
from Helpers.BWCoroutine import *

class soIncomingDamageGUI(PyGUI.PyGUIBase):
    factoryString = 'soGUI.soIncomingDamageGUI'
    DIRECTION_NONE = 0
    DIRECTION_NORTH = 1
    DIRECTION_SOUTH = 2
    DIRECTION_WEST = 3
    DIRECTION_EAST = 4
    DAMAGE_PHYSICAL = 1
    DAMAGE_ELECTRICAL = 2
    DAMAGE_RADIATION = 3
    DAMAGE_FIRE = 4
    DAMAGE_POISON = 5
    DAMAGE_CHEMICAL = 6
    DAMAGE_COLOURS = {DAMAGE_PHYSICAL: (255, 50, 50, 255),
     DAMAGE_ELECTRICAL: (50, 80, 255, 255),
     DAMAGE_RADIATION: (180, 180, 50, 255),
     DAMAGE_FIRE: (255, 150, 50, 255),
     DAMAGE_POISON: (50, 255, 50, 255),
     DAMAGE_CHEMICAL: (255, 200, 50, 255)}
    UP_TEXTURE = 'soGUI/maps/Misc/upHurt.tga'
    DOWN_TEXTURE = 'soGUI/maps/Misc/downHurt.tga'
    EAST_TEXTURE = 'soGUI/maps/Misc/eastHurt.tga'
    WEST_TEXTURE = 'soGUI/maps/Misc/westHurt.tga'

    def __init__(self, component):
        PyGUI.PyGUIBase.__init__(self, component)
        component.script = self
        self.nAlphaShader = None
        self.sAlphaShader = None
        self.wAlphaShader = None
        self.eAlphaShader = None
        self.setupRoot()
        self.setupAlphaShaders()
        self.setupDamageView()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'LEGACY'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.widthMode = 'PIXEL'
        cmp.heightMode = 'PIXEL'
        cmp.width = 600
        cmp.height = 600
        cmp.position = (0.0, 0.0, 0.0)
        cmp.colour = (255, 255, 255, 255)
        cmp.textureName = ''
        cmp.visible = True

    def setupAlphaShaders(self):
        self.nAlphaShader = GUI.AlphaShader()
        self.nAlphaShader.speed = 0.4
        self.nAlphaShader.mode = 'ALL'
        self.nAlphaShader.alpha = 0.0
        self.sAlphaShader = GUI.AlphaShader()
        self.sAlphaShader.speed = 0.4
        self.sAlphaShader.mode = 'ALL'
        self.sAlphaShader.alpha = 0.0
        self.sAlphaShader.reset()
        self.wAlphaShader = GUI.AlphaShader()
        self.wAlphaShader.speed = 0.4
        self.wAlphaShader.mode = 'ALL'
        self.wAlphaShader.alpha = 0.0
        self.wAlphaShader.reset()
        self.eAlphaShader = GUI.AlphaShader()
        self.eAlphaShader.speed = 0.4
        self.eAlphaShader.mode = 'ALL'
        self.eAlphaShader.alpha = 0.0
        self.eAlphaShader.reset()

    def setupDamageView(self):
        north = GUI.Simple(self.UP_TEXTURE)
        north.horizontalPositionMode = north.verticalPositionMode = 'CLIP'
        north.widthMode = north.heightMode = 'PIXEL'
        north.horizontalAnchor = 'LEFT'
        north.verticalAnchor = 'TOP'
        north.width = self.component.width
        north.height = 120
        north.position = (-1.0, 1.0, 0.5)
        north.colour = (255, 255, 255, 255)
        north.materialFX = 'BLEND'
        north.addShader(self.nAlphaShader, 'fader')
        north.visible = True
        self.component.addChild(north, 'NDamage')
        south = GUI.Simple(self.DOWN_TEXTURE)
        south.horizontalPositionMode = south.verticalPositionMode = 'CLIP'
        south.widthMode = south.heightMode = 'PIXEL'
        south.horizontalAnchor = 'LEFT'
        south.verticalAnchor = 'BOTTOM'
        south.width = self.component.width
        south.height = 120
        south.position = (-1.0, -1.0, 0.5)
        south.colour = (255, 255, 255, 255)
        south.materialFX = 'BLEND'
        south.addShader(self.sAlphaShader, 'fader')
        south.visible = True
        self.component.addChild(south, 'SDamage')
        west = GUI.Simple(self.WEST_TEXTURE)
        west.horizontalPositionMode = west.verticalPositionMode = 'CLIP'
        west.widthMode = west.heightMode = 'PIXEL'
        west.horizontalAnchor = 'LEFT'
        west.verticalAnchor = 'TOP'
        west.width = 120
        west.height = self.component.height
        west.position = (-1.0, 1.0, 0.5)
        west.colour = (255, 255, 255, 255)
        west.materialFX = 'BLEND'
        west.addShader(self.wAlphaShader, 'fader')
        west.visible = True
        self.component.addChild(west, 'WDamage')
        east = GUI.Simple(self.EAST_TEXTURE)
        east.horizontalPositionMode = east.verticalPositionMode = 'CLIP'
        east.widthMode = east.heightMode = 'PIXEL'
        east.horizontalAnchor = 'RIGHT'
        east.verticalAnchor = 'TOP'
        east.width = 120
        east.height = self.component.height
        east.position = (1.0, 1.0, 0.5)
        east.colour = (255, 255, 255, 255)
        east.materialFX = 'BLEND'
        east.addShader(self.eAlphaShader, 'fader')
        east.visible = True
        self.component.addChild(east, 'EDamage')

    def show(self, severity, direction, dmgType):
        if severity <= 0:
            return
        else:
            if self.component.parent is None:
                GUI.addRoot(self.component)
            if direction == self.DIRECTION_NORTH:
                self.component.NDamage.colour = self.DAMAGE_COLOURS[dmgType]
                self.component.NDamage.fader.alpha = severity
                self.component.NDamage.fader.reset()
                self.component.NDamage.fader.alpha = 0
            elif direction == self.DIRECTION_SOUTH:
                self.component.SDamage.colour = self.DAMAGE_COLOURS[dmgType]
                self.component.SDamage.fader.alpha = severity
                self.component.SDamage.fader.reset()
                self.component.SDamage.fader.alpha = 0
            elif direction == self.DIRECTION_WEST:
                self.component.WDamage.colour = self.DAMAGE_COLOURS[dmgType]
                self.component.WDamage.fader.alpha = severity
                self.component.WDamage.fader.reset()
                self.component.WDamage.fader.alpha = 0
            elif direction == self.DIRECTION_EAST:
                self.component.EDamage.colour = self.DAMAGE_COLOURS[dmgType]
                self.component.EDamage.fader.alpha = severity
                self.component.EDamage.fader.reset()
                self.component.EDamage.fader.alpha = 0
            elif direction == self.DIRECTION_NONE:
                self.component.EDamage.colour = self.DAMAGE_COLOURS[dmgType]
                self.component.EDamage.fader.alpha = severity
                self.component.EDamage.fader.reset()
                self.component.EDamage.fader.alpha = 0
                self.component.WDamage.colour = self.DAMAGE_COLOURS[dmgType]
                self.component.WDamage.fader.alpha = severity
                self.component.WDamage.fader.reset()
                self.component.WDamage.fader.alpha = 0
                self.component.SDamage.colour = self.DAMAGE_COLOURS[dmgType]
                self.component.SDamage.fader.alpha = severity
                self.component.SDamage.fader.reset()
                self.component.SDamage.fader.alpha = 0
                self.component.NDamage.colour = self.DAMAGE_COLOURS[dmgType]
                self.component.NDamage.fader.alpha = severity
                self.component.NDamage.fader.reset()
                self.component.NDamage.fader.alpha = 0
            return