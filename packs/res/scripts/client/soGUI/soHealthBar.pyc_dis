# Embedded file name: scripts/client/soGUI/soHealthBar.py
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import BWPersonality
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Keys import *
from soGUI.soButton import soButtonWTT, soButton
from soGUI.soToolTipComponent import soToolTipComponent

class soHealthBar(PyGUIBase):
    factoryString = 'soGUI.soHealthBar'
    FACTION_MARK_FOREIGNERS = 0
    FACTION_MARK_LOCALS = 1
    FACTION_MARK_LONERS = 2
    ANOMALY_RADIATION, ANOMALY_ELECTRICITY, ANOMALY_FIRE, ANOMALY_CHEMICAL, ANOMALY_GRAVITY, ANOMALY_PSIONICS = xrange(6)
    fIconTextures = {FACTION_MARK_FOREIGNERS: BigWorld.PyTextureProvider('soGUI/maps/Factions/foreigners.tga'),
     FACTION_MARK_LOCALS: BigWorld.PyTextureProvider('soGUI/maps/Factions/locals.tga'),
     FACTION_MARK_LONERS: BigWorld.PyTextureProvider('soGUI/maps/Factions/loners.tga')}
    EVENT_CONTEXT = 0
    EVENT_PARTYSETTINGS = 1
    TTID_PL_MARK = 'gui_player_frame_PLMARK'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.pressed = False
        self.interfaceID = BWPersonality.GUICore.GUI_ID_PLAYERFRAME
        self.setupRoot()
        self.setupFrame()
        self.setupBars()
        self.setupShaders()
        self.setupAnomalyMeter()
        self.hungry_value = 0.0
        self.hp_value = 0.0
        self.HP_BLINK_TIME = 0.3
        self.HUNGRY_BLINK_TIME = 0.7
        BigWorld.callback(self.HUNGRY_BLINK_TIME, self.updateHungryBlink)
        BigWorld.callback(self.HP_BLINK_TIME, self.updateHPBlink)

    def updateHungryBlink(self):
        BigWorld.callback(self.HUNGRY_BLINK_TIME, self.updateHungryBlink)
        if self.hungry_value:
            self.component.hungryIcon.visible = True
        else:
            self.component.hungryIcon.visible = not self.component.hungryIcon.visible

    def updateHPBlink(self):
        BigWorld.callback(self.HP_BLINK_TIME, self.updateHPBlink)
        if self.hp_value > 0.25:
            BWPersonality.game.GUICore.healthBarGUI.component.healthBar.colour.x = 255
            BWPersonality.game.GUICore.healthBarGUI.component.healthBar.height = 10.0
        else:
            red = BWPersonality.game.GUICore.healthBarGUI.component.healthBar.colour.x
            BWPersonality.game.GUICore.healthBarGUI.component.healthBar.colour.x = 255 if red != 255 else 150
            height = BWPersonality.game.GUICore.healthBarGUI.component.healthBar.height
            BWPersonality.game.GUICore.healthBarGUI.component.healthBar.height = 10.0 if height != 10.0 else 12.0

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.width = 223
        cmp.height = 81
        cmp.position = (3, 3, 0.3)

    def setupFrame(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = 'soGUI/maps/HealthBar/frame.tga'
        cmp.width = 223
        cmp.height = 62
        cmp.position = (0, 0, 1.0)
        cmp.mouseButtonFocus = True
        cmp.script = self
        self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = u'_empty_name_'
        cmp.position = (11, 10, 0.2)
        self.component.addChild(cmp, 'pName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = u'0'
        cmp.position = (210, 29, 0.2)
        self.component.addChild(cmp, 'pLevel')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 16
        cmp.position = (40, 18, 0.3)
        self.component.addChild(cmp, 'pIcon')
        cmp = GUI.Simple('soGUI/maps/PartyFrames/20/PLMark.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 21
        cmp.position = (202, 10, 0.3)
        cmp.visible = False
        self.component.addChild(cmp, 'plMark')
        btn = soButtonWTT(GUI.Window(), 'player_frame_party_settings')
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 15
        cmp.height = 15
        cmp.position = (202, 39, 1.0)
        btn.initVSC('soGUI/visual_styles/partyOptionsBtn.xml')
        btn.onBound()
        btn._updateVisualState()
        btn.onClick = self.partySettingHandler
        self.component.addChild(cmp, 'settings')
        cmp = GUI.Simple('soGUI/maps/HealthBar/health_icon.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 10
        cmp.height = 10
        cmp.position = (8, 19, 0.3)
        cmp.visible = True
        self.component.addChild(cmp, 'healthIcon')
        cmp = GUI.Simple('soGUI/maps/HealthBar/hungry_icon.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 10
        cmp.height = 10
        cmp.position = (8, 32, 0.3)
        cmp.visible = True
        self.component.addChild(cmp, 'hungryIcon')
        cmp = GUI.Simple('soGUI/maps/HealthBar/stamina_icon.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 10
        cmp.height = 10
        cmp.position = (8, 45, 0.3)
        cmp.visible = True
        self.component.addChild(cmp, 'staminaIcon')
        cmp = GUI.Simple('soGUI/maps/Icons/ability/icon_perk_boost_perception.jpg')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 50
        cmp.height = 60
        cmp.position = (150, 20, 0.5)
        cmp.visible = 0
        self.component.addChild(cmp, 'NinjaIcon')

    def setupBars(self):
        cmp = GUI.Simple('soGUI/maps/HealthBar/health.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 180
        cmp.height = 10
        cmp.position = (21, 19, 0.7)
        self.component.addChild(cmp, 'healthBar')
        cmp = GUI.Simple('soGUI/maps/HealthBar/hungry.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 180
        cmp.height = 10
        cmp.position = (21, 32, 0.7)
        self.component.addChild(cmp, 'hungryBar')
        cmp = GUI.Simple('soGUI/maps/HealthBar/stamina.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 180
        cmp.height = 10
        cmp.position = (21, 45, 0.7)
        self.component.addChild(cmp, 'staminaBar')

    def setupAnomalyMeter(self):
        for i in xrange(6):
            cmp = GUI.Window('soGUI/maps/HealthBar/AnomalyMeter/cell.tga')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.width = 19
            cmp.height = 19
            cmp.crossFocus = True
            cmp.script = self
            cmp.position = (6 + i * 19, 62, 0.7)
            self.component.addChild(cmp, 'anomalyCell{0}'.format(i))
            cmp = GUI.Simple('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.width = 19
            cmp.height = 19
            cmp.mapping = ((0.0, 0.0),
             (0.0, 0.3333333),
             (1.0, 0.3333333),
             (1.0, 0.0))
            cmp.visible = False
            cmp.position = (0, 0, 0.7)
            if i == self.ANOMALY_CHEMICAL:
                cmp.textureName = 'soGUI/maps/HealthBar/AnomalyMeter/chemical.tga'
            elif i == self.ANOMALY_ELECTRICITY:
                cmp.textureName = 'soGUI/maps/HealthBar/AnomalyMeter/electricity.tga'
            elif i == self.ANOMALY_FIRE:
                cmp.textureName = 'soGUI/maps/HealthBar/AnomalyMeter/fire.tga'
            elif i == self.ANOMALY_GRAVITY:
                cmp.textureName = 'soGUI/maps/HealthBar/AnomalyMeter/gravity.tga'
            elif i == self.ANOMALY_PSIONICS:
                cmp.textureName = 'soGUI/maps/HealthBar/AnomalyMeter/psionics.tga'
            elif i == self.ANOMALY_RADIATION:
                cmp.textureName = 'soGUI/maps/HealthBar/AnomalyMeter/radiation.tga'
            cell = getattr(self.component, 'anomalyCell{0}'.format(i), None)
            if cell:
                cell.addChild(cmp, 'icon')

        return

    def setupShaders(self):
        hShader = GUI.ClipShader()
        sShader = GUI.ClipShader()
        hungryShader = GUI.ClipShader()
        hShader.speed = 0
        sShader.speed = 0
        hungryShader.speed = 0
        hShader.mode = sShader.mode = hungryShader.mode = 'RIGHT'
        hShader.value = sShader.value = hungryShader.value = 1.0
        self.component.healthBar.addShader(hShader, 'clipper')
        self.component.staminaBar.addShader(sShader, 'clipper')
        self.component.hungryBar.addShader(hungryShader, 'clipper')

    def partySettingHandler(self):
        BWPersonality.GUICore.playerFrameEvent(self.EVENT_PARTYSETTINGS, None)
        return

    def update(self):
        if BWPersonality.GUICore.healthDataSection.has_key('name'):
            self.component.pName.text = BWPersonality.GUICore.healthDataSection['name']
        if BWPersonality.GUICore.healthDataSection.has_key('level'):
            self.component.pLevel.text = BWPersonality.GUICore.healthDataSection['level']
        if BWPersonality.GUICore.healthDataSection.has_key('cp'):
            pass
        if BWPersonality.GUICore.healthDataSection.has_key('health'):
            self.hp_value = self.component.healthBar.clipper.value = BWPersonality.GUICore.healthDataSection['health']
        if BWPersonality.GUICore.healthDataSection.has_key('stamina'):
            self.component.staminaBar.clipper.value = BWPersonality.GUICore.healthDataSection['stamina']
        if BWPersonality.GUICore.healthDataSection.has_key('isPL'):
            self.component.plMark.visible = BWPersonality.GUICore.healthDataSection['isPL']
            self.component.settings.script.buttonDisabled = not BWPersonality.GUICore.healthDataSection['isPL']
        if BWPersonality.GUICore.healthDataSection.has_key('hungry'):
            val = BWPersonality.GUICore.healthDataSection['hungry']
            self.component.hungryBar.clipper.value = val
            self.hungry_value = val
        if BWPersonality.GUICore.healthDataSection.has_key('thirst'):
            pass
        if BWPersonality.GUICore.healthDataSection.has_key('anomalies'):
            for anomaly in BWPersonality.GUICore.healthDataSection['anomalies']:
                cell = getattr(self.component, 'anomalyCell{0}'.format(anomaly), None)
                cell.icon.visible = True
                if BWPersonality.GUICore.healthDataSection['anomalies'][anomaly] == 0:
                    cell.icon.visible = False
                elif BWPersonality.GUICore.healthDataSection['anomalies'][anomaly] == 1:
                    cell.icon.mapping = ((0.0, 0.0),
                     (0.0, 0.3333333),
                     (1.0, 0.3333333),
                     (1.0, 0.0))
                elif BWPersonality.GUICore.healthDataSection['anomalies'][anomaly] == 2:
                    cell.icon.mapping = ((0.0, 0.3333333),
                     (0.0, 0.6666667),
                     (1.0, 0.6666667),
                     (1.0, 0.3333333))
                elif BWPersonality.GUICore.healthDataSection['anomalies'][anomaly] == 3:
                    cell.icon.mapping = ((0.0, 0.6666667),
                     (0.0, 1.0),
                     (1.0, 1.0),
                     (1.0, 0.6666667))

        return

    def handleMouseButtonEvent(self, comp, event):
        if not event.isMouseButton():
            return False
        down = event.isKeyDown()
        key = event.key
        if key == KEY_RIGHTMOUSE:
            if down:
                self.pressed = True
            elif self.pressed:
                self.pressed = False
                BWPersonality.GUICore.playerFrameEvent(self.EVENT_CONTEXT, None)
            return True
        else:
            return False

    def handleMouseEnterEvent(self, component):
        if component is self.component.plMark:
            BWPersonality.GUICore.toolTipEvent(self.TTID_PL_MARK, self.interfaceID, soToolTipComponent.EVENT_SHOW)
            return True
        else:
            for anomalyType in [self.ANOMALY_CHEMICAL,
             self.ANOMALY_ELECTRICITY,
             self.ANOMALY_FIRE,
             self.ANOMALY_GRAVITY,
             self.ANOMALY_PSIONICS,
             self.ANOMALY_RADIATION]:
                cmp = getattr(self.component, 'anomalyCell{0}'.format(anomalyType), None)
                if component is cmp:
                    BWPersonality.GUICore.toolTipEvent(anomalyType, self.interfaceID, soToolTipComponent.EVENT_SHOW)
                    return True

            return False

    def handleMouseLeaveEvent(self, component):
        if component is self.component.plMark:
            BWPersonality.GUICore.toolTipEvent(self.TTID_PL_MARK, self.interfaceID, soToolTipComponent.EVENT_HIDE)
            return True
        else:
            for anomalyType in [self.ANOMALY_CHEMICAL,
             self.ANOMALY_ELECTRICITY,
             self.ANOMALY_FIRE,
             self.ANOMALY_GRAVITY,
             self.ANOMALY_PSIONICS,
             self.ANOMALY_RADIATION]:
                cmp = getattr(self.component, 'anomalyCell{0}'.format(anomalyType), None)
                if component is cmp:
                    BWPersonality.GUICore.toolTipEvent(anomalyType, self.interfaceID, soToolTipComponent.EVENT_HIDE)
                    return True

            return False

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'healthBar')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False