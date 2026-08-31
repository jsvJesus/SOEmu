# Embedded file name: scripts/client/soGUI/soPartyFrames.py
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import BWPersonality
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Keys import *
from soGUI.soButton import soButton, soButtonWFT, soButtonWTT
from soCharEffectsFrame import soEffectSlot
from Helpers.BWCoroutine import *
from soGUI.soToolTipComponent import soToolTipComponent
from EffectUtils import EFFECT_TYPE
from soGUI.soHealthBar import soHealthBar

class soPartyMember(PyGUIBase):
    factoryString = 'soGUI.soPartyMember'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
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
        cmp.width = 153
        cmp.height = 27
        cmp.textureName = 'soGUI/maps/PartyFrames/frame.tga'
        cmp.visible = False
        cmp.mouseButtonFocus = True

    def setupContent(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 136
        cmp.height = 6
        cmp.position = (9, 18, 0.5)
        cmp.textureName = 'soGUI/maps/PartyFrames/hp.tga'
        self.component.addChild(cmp, 'hp_back')
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 136
        cmp.height = 6
        cmp.position = (9, 18, 0.5)
        cmp.textureName = 'soGUI/maps/PartyFrames/hp_full.tga'
        self.component.addChild(cmp, 'hp_front')
        shader = GUI.ClipShader()
        shader.mode = 'RIGHT'
        shader.value = 1.0
        shader.speed = 0.0
        self.component.hp_front.addShader(shader, 'clipper')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colourFormatting = True
        cmp.multiline = False
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (9, 1, 0.4)
        self.component.addChild(cmp, 'nick')

    def setHealth(self, health):
        self.component.hp_front.clipper.value = health

    def setNickname(self, nick):
        self.component.nick.text = nick
        if nick == '':
            self.component.visible = False
        else:
            self.component.visible = True

    def handleMouseButtonEvent(self, comp, event):
        down = event.isKeyDown()
        key = event.key
        modifiers = event.modifiers
        if key == KEY_RIGHTMOUSE:
            if down:
                BWPersonality.GUICore.partyEvent(soPartyFrames.EVENT_CONTEXT, self.component.nick.text)


class soPartyFrames(PyGUIBase):
    factoryString = 'soGUI.soPartyFrames'
    EVENT_CONTEXT = 0

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.members = []
        self.setupRoot()
        self.setupMembers()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 153
        cmp.height = 135
        cmp.position = (0, 200, 0.4)
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.visible = True
        BWPersonality.GUICore.worldLayer.addChild(cmp, 'partyFrames')

    def setupMembers(self):
        for i in xrange(5):
            member = soPartyMember(GUI.Window())
            cmp = member.component
            cmp.position = (0, 0 + i * 27, 0.5)
            member.setHealth(0.0)
            member.setNickname(u'')
            self.component.addChild(cmp, 'member' + str(i))

    def applyMembers(self):
        for i in xrange(5):
            member = self.component.__getattribute__('member' + str(i))
            member.script.setHealth(0.0)
            member.script.setNickname(u'')

        for member in self.members:
            nick = member[0]
            health = member[1]
            cmp = self.component.__getattribute__('member' + str(self.members.index(member)))
            cmp.script.setHealth(health)
            cmp.script.setNickname(nick)

    def update(self):
        data = BWPersonality.GUICore.partyDataSection
        self.members = data
        if len(data) < 1:
            self.component.visible = False
        else:
            self.component.visible = True
            self.applyMembers()


class soPartyMember2(PyGUIBase):
    factoryString = 'soGUI.soPartyMember2'
    MAXIMIZED_FRAME = BigWorld.PyTextureProvider('soGUI/maps/PartyFrames/20/maximized/frame.tga')
    MINIMIZED_FRAME = BigWorld.PyTextureProvider('soGUI/maps/PartyFrames/20/minimized/frame.tga')
    BARS_TEXTURES = {'HP': [BigWorld.PyTextureProvider('soGUI/maps/PartyFrames/20/maximized/HPBar.tga'), BigWorld.PyTextureProvider('soGUI/maps/PartyFrames/20/minimized/hpBar.tga')],
     'CP': [BigWorld.PyTextureProvider('soGUI/maps/PartyFrames/20/maximized/CPBar.tga'), BigWorld.PyTextureProvider('soGUI/maps/PartyFrames/20/minimized/cpBar.tga')],
     'SP': [BigWorld.PyTextureProvider('soGUI/maps/PartyFrames/20/maximized/staminaBar.tga'), BigWorld.PyTextureProvider('soGUI/maps/PartyFrames/20/minimized/staminaBar.tga')]}
    factionIcons = {soHealthBar.FACTION_MARK_FOREIGNERS: soHealthBar.fIconTextures[soHealthBar.FACTION_MARK_FOREIGNERS],
     soHealthBar.FACTION_MARK_LOCALS: soHealthBar.fIconTextures[soHealthBar.FACTION_MARK_LOCALS],
     soHealthBar.FACTION_MARK_LONERS: soHealthBar.fIconTextures[soHealthBar.FACTION_MARK_LONERS]}

    def __init__(self, component, id, data):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.maximized = None
        self.pressed = False
        self.id = id
        self.effects = {}
        self.memberData = data
        self.tC = 0
        self.interfaceID = BWPersonality.GUICore.GUI_ID_PARTYFRAMES
        self.setupRoot()
        self.setupContent()
        self.maximize()
        self.doReposition()
        self._applyMemberData()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = 'PIXEL'
        cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position.x = 0
        cmp.width = 0
        cmp.mouseButtonFocus = True

    def setupContent(self):
        cmp = GUI.Window()
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 201
        cmp.height = 58
        cmp.position = (0, 0, 0.9)
        self.component.addChild(cmp, 'frameWnd')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = u'____________1'
        cmp.position = (8, 10, 0.2)
        self.component.frameWnd.addChild(cmp, 'pName')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = u'0'
        cmp.position = (189, 26, 0.2)
        self.component.frameWnd.addChild(cmp, 'pLevel')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 16
        cmp.position = (4, 18, 0.3)
        self.component.frameWnd.addChild(cmp, 'pIcon')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (175, 166, 112, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_10i.font'
        cmp.text = u'Assault'
        cmp.position = (39, 23, 0.2)
        self.component.frameWnd.addChild(cmp, 'pClass')
        cmp = GUI.Simple('soGUI/maps/PartyFrames/20/PLMark.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 18
        cmp.height = 21
        cmp.position = (180, 34, 0.3)
        cmp.visible = False
        cmp.script = self
        cmp.crossFocus = True
        self.component.frameWnd.addChild(cmp, 'plMark')
        cmp = GUI.Window('soGUI/maps/PartyFrames/20/maximized/CPBar.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 157
        cmp.height = 6
        cmp.position = (22, 31, 0.3)
        self.component.frameWnd.addChild(cmp, 'cpBar')
        shader = GUI.ClipShader()
        shader.speed = 0.1
        shader.value = 0.0
        cmp.addShader(shader, 'clipper')
        cmp = GUI.Window('soGUI/maps/PartyFrames/20/maximized/HPBar.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 162
        cmp.height = 8
        cmp.position = (17, 37, 0.3)
        self.component.frameWnd.addChild(cmp, 'hpBar')
        shader = GUI.ClipShader()
        shader.speed = 0.1
        shader.value = 0.0
        cmp.addShader(shader, 'clipper')
        cmp = GUI.Window('soGUI/maps/PartyFrames/20/maximized/staminaBar.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 162
        cmp.height = 6
        cmp.position = (17, 47, 0.3)
        self.component.frameWnd.addChild(cmp, 'spBar')
        shader = GUI.ClipShader()
        shader.speed = 0.1
        shader.value = 0.0
        cmp.addShader(shader, 'clipper')
        btn = soButtonWTT(GUI.Window(), 'party_frames_hidebuffs')
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 15
        cmp.height = 13
        cmp.position = (166, 17, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/hideBuffsBtn.xml')
        btn.onBound()
        btn.buttonActive = True
        btn._updateVisualState()
        btn.onClick = self._toggleBuffsHandler
        self.component.frameWnd.addChild(cmp, 'hideBuffs')
        btn = soButtonWTT(GUI.Window(), 'party_frames_minimize_member')
        cmp = btn.component
        cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.width = 11
        cmp.height = 10
        cmp.position = (4, 35, 0.4)
        btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
        btn.initVSC('soGUI/visual_styles/minmaxPartyFrameBtn.xml')
        btn.onBound()
        btn._updateVisualState()
        btn.onClick = self._minmaxHandler
        self.component.frameWnd.addChild(cmp, 'minmax')

    def handleMouseButtonEvent(self, comp, event):
        if not event.isMouseButton():
            return False
        down = event.isKeyDown()
        key = event.key
        if key == KEY_RIGHTMOUSE:
            if down:
                self.pressed = True
            else:
                if self.pressed:
                    self.pressed = False
                    self.onClick()
                return True
        return False

    def onClick(self):
        BWPersonality.GUICore.partyEvent(soPartyFrames2.EVENT_CONTEXT, self.id)

    def maximize(self):
        if self.maximized:
            return
        self.maximized = True
        self.component.frameWnd.minmax.script.toolTipID = 'party_frames_minimize_member'
        cmp = self.component
        cmp.height = 58
        self.component.frameWnd.width = 201
        self.component.frameWnd.height = 58
        self.component.frameWnd.texture = self.MAXIMIZED_FRAME
        self.component.frameWnd.pIcon.visible = True
        self.component.frameWnd.pClass.visible = True
        self.component.frameWnd.pName.font = 'ruRU_Cyrvetica_Extra_12i.font'
        self.component.frameWnd.pLevel.visible = True
        self.component.frameWnd.plMark.position = (180, 34, 0.3)
        self.component.frameWnd.minmax.position = (4, 35, 0.4)
        self.component.frameWnd.hideBuffs.position = (166, 17, 0.4)
        self.component.frameWnd.cpBar.width = 157
        self.component.frameWnd.cpBar.height = 6
        self.component.frameWnd.cpBar.position = (22, 31, 0.3)
        self.component.frameWnd.cpBar.texture = self.BARS_TEXTURES['CP'][0]
        self.component.frameWnd.hpBar.width = 162
        self.component.frameWnd.hpBar.height = 8
        self.component.frameWnd.hpBar.position = (17, 37, 0.3)
        self.component.frameWnd.hpBar.texture = self.BARS_TEXTURES['HP'][0]
        self.component.frameWnd.spBar.width = 162
        self.component.frameWnd.spBar.height = 6
        self.component.frameWnd.spBar.position = (17, 47, 0.3)
        self.component.frameWnd.spBar.texture = self.BARS_TEXTURES['SP'][0]
        self.renderEffects()

    def minimize(self):
        if not self.maximized:
            return
        self.maximized = False
        self.component.frameWnd.minmax.script.toolTipID = 'party_frames_maximize_member'
        cmp = self.component
        cmp.height = 39
        self.component.frameWnd.width = 155
        self.component.frameWnd.height = 39
        self.component.frameWnd.texture = self.MINIMIZED_FRAME
        self.component.frameWnd.pIcon.visible = False
        self.component.frameWnd.pClass.visible = False
        self.component.frameWnd.pName.font = 'ruRU_Cyrvetica_Extra_12i.font'
        self.component.frameWnd.pLevel.visible = False
        self.component.frameWnd.plMark.position = (133, 15, 0.3)
        self.component.frameWnd.minmax.position = (5, 16, 0.4)
        self.component.frameWnd.hideBuffs.position = (136, 3, 0.4)
        self.component.frameWnd.cpBar.width = 114
        self.component.frameWnd.cpBar.height = 6
        self.component.frameWnd.cpBar.position = (18, 18, 0.3)
        self.component.frameWnd.cpBar.texture = self.BARS_TEXTURES['CP'][1]
        self.component.frameWnd.hpBar.width = 114
        self.component.frameWnd.hpBar.height = 6
        self.component.frameWnd.hpBar.position = (18, 23, 0.3)
        self.component.frameWnd.hpBar.texture = self.BARS_TEXTURES['HP'][1]
        self.component.frameWnd.spBar.width = 114
        self.component.frameWnd.spBar.height = 6
        self.component.frameWnd.spBar.position = (18, 28, 0.3)
        self.component.frameWnd.spBar.texture = self.BARS_TEXTURES['SP'][1]
        self.renderEffects()

    def _toggleBuffsHandler(self):
        self.showBuffs(self.component.frameWnd.hideBuffs.script.buttonActive)

    def _minmaxHandler(self):
        if self.component.frameWnd.minmax.script.buttonActive:
            self.minimize()
        else:
            self.maximize()

    def showBuffs(self, doShow = True):
        if doShow:
            self.component.frameWnd.hideBuffs.script.toolTipID = 'party_frames_hidebuffs'
        else:
            self.component.frameWnd.hideBuffs.script.toolTipID = 'party_frames_showbuffs'
        for id in self.effects:
            cmp = getattr(self.component, 'effect{0}'.format(id), None)
            if cmp:
                cmp.visible = doShow

        return

    def _applyMemberData(self):
        if self.memberData.has_key('name'):
            self.component.frameWnd.pName.text = self.memberData['name']
        if self.memberData.has_key('isPL'):
            self.component.frameWnd.plMark.visible = self.memberData['isPL']
        if self.memberData.has_key('class'):
            self.component.frameWnd.pClass.text = self.memberData['class']
        if self.memberData.has_key('icon'):
            self.component.frameWnd.pIcon.texture = self.factionIcons[self.memberData['icon']]
        if self.memberData.has_key('CP'):
            self.component.frameWnd.cpBar.clipper.value = self.memberData['CP']
        if self.memberData.has_key('HP'):
            self.component.frameWnd.hpBar.clipper.value = self.memberData['HP']
        if self.memberData.has_key('SP'):
            self.component.frameWnd.spBar.clipper.value = self.memberData['SP']
        if self.memberData.has_key('level'):
            self.component.frameWnd.pLevel.text = self.memberData['level']
        if self.memberData.has_key('out_of_range'):
            self.component.frameWnd.colour = (255, 0, 0, 255) if self.memberData['out_of_range'] else (255, 255, 255, 255)

    def setMemberData(self, data):
        self.memberData.update(data)
        self._applyMemberData()

    def isMaximized(self):
        return self.maximized

    def renderEffects(self):
        ids = self.effects.keys()
        buffs = []
        debuffs = []
        undef = []
        for id in ids:
            if self.effects[id][2] == EFFECT_TYPE.BUFF:
                buffs.append(id)
            elif self.effects[id][2] == EFFECT_TYPE.DEBUFF:
                debuffs.append(id)
            elif self.effects[id][2] == EFFECT_TYPE.UNDEFINED:
                undef.append(id)

        buffs.sort(lambda x, y: cmp(self.effects[x][4], self.effects[y][4]))
        debuffs.sort(lambda x, y: cmp(self.effects[x][4], self.effects[y][4]))
        undef.sort(lambda x, y: cmp(self.effects[x][4], self.effects[y][4]))
        sortedBuffs = buffs + debuffs + undef
        for i, id in enumerate(sortedBuffs):
            cmpt = getattr(self.component, 'effect{0}'.format(id))
            cmpt.horizontalPositionMode = cmpt.verticalPositionMode = 'PIXEL'
            cmpt.horizontalAnchor = 'LEFT'
            cmpt.verticalAnchor = 'TOP'
            cmpt.position = (self.component.frameWnd.width + i * 22, 0, 0.5)

    def _update(self):
        for id in self.effects:
            if not hasattr(self.component, 'effect' + str(id)):
                newEffect = soEffectSlot(GUI.Window())
                cmp = newEffect.component
                newEffect.setIcon(self.effects[id][0])
                newEffect.setID(id)
                newEffect.setTime(self.effects[id][1])
                newEffect.setType(self.effects[id][2])
                newEffect.setStack(self.effects[id][3])
                self.component.addChild(cmp, 'effect' + str(id))
                newEffect._applyData()
            else:
                effect = getattr(self.component, 'effect' + str(id)).script
                effect.setIcon(self.effects[id][0])
                effect.setID(id)
                effect.setTime(self.effects[id][1])
                effect.setType(self.effects[id][2])
                effect.setStack(self.effects[id][3])

        self.renderEffects()

    def setEffect(self, id, data):
        if not self.effects.has_key(id):
            self.effects[id] = data + [self.tC]
            self.tC += 1
        else:
            self.effects[id][:4] = data
        self._update()

    def delEffect(self, id):
        if self.effects.has_key(id):
            del self.effects[id]
            if hasattr(self.component, 'effect' + str(id)):
                cmp = getattr(self.component, 'effect' + str(id))
                self.component.delChild(cmp)
                cmp.script.fini()
            self._update()
            return True
        return False

    def clearEffects(self):
        effects = self.effects.keys()
        for id in effects:
            self.delEffect(id)

    def tick(self):
        for id in self.effects:
            if self.effects[id][1] > 0:
                self.effects[id][1] -= 1
            if hasattr(self.component, 'effect' + str(id)):
                cmp = getattr(self.component, 'effect' + str(id))
                cmp.script.tick()

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.width = sW

    def fini(self):
        self.clearAllChildren(self.component)
        self.component = None
        return

    def handleMouseEnterEvent(self, component):
        if component is self.component.frameWnd.plMark:
            BWPersonality.GUICore.toolTipEvent(soPartyFrames2.TTID_PL_MARK, self.interfaceID, soToolTipComponent.EVENT_SHOW)
            return True
        return False

    def handleMouseLeaveEvent(self, component):
        if component is self.component.frameWnd.plMark:
            BWPersonality.GUICore.toolTipEvent(soPartyFrames2.TTID_PL_MARK, self.interfaceID, soToolTipComponent.EVENT_HIDE)
            return True
        return False


class soPartyFrames2(PyGUIBase):
    factoryString = 'soGUI.soPartyFrames2'
    TTID_PL_MARK = 'gui_party_PLMARK'
    EVENT_CONTEXT = 0

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.ticker = None
        self.membersOrder = []
        self.members = {}
        self.interfaceID = BWPersonality.GUICore.GUI_ID_PARTYFRAMES
        self.setupRoot()
        self.setupContent()
        self.doReposition()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.widthMode = 'PIXEL'
        cmp.heightMode = 'PIXEL'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.height = 0
        cmp.position = (0, 200, 0.2)

    def setupContent(self):
        pass

    def setMember(self, id, data):
        if self.members.has_key(id):
            self.members[id].setMemberData(data)
        else:
            self.members[id] = soPartyMember2(GUI.Window(), id, data)
            self.membersOrder.append(id)
            cmp = self.members[id].component
            self.members[id].onBound()
            self.component.addChild(cmp, 'member' + str(id))
        self._rearrangeMembers()
        self.runTicker()
        self._updateHeight()

    def delMember(self, id):
        if self.members.has_key(id):
            cmp = self.members[id].component
            cmp.script.fini()
            self.component.delChild(cmp)
            del self.members[id]
            self.membersOrder.remove(id)
            self._rearrangeMembers()
            return True
        else:
            return False
        self._updateHeight()

    def clearMembers(self):
        for id in self.membersOrder:
            cmp = self.members[id].component
            cmp.script.fini()
            self.component.delChild(cmp)

        self.membersOrder = []
        self.members = {}
        self._updateHeight()

    def setMemberEffect(self, mmbrID, effID, data):
        if self.members.has_key(mmbrID):
            self.members[mmbrID].setEffect(effID, data)

    def delMemberEffect(self, mmbrID, effID):
        if self.members.has_key(mmbrID):
            self.members[mmbrID].delEffect(effID)

    def clearMemberEffects(self, mmbrID):
        if self.members.has_key(mmbrID):
            self.members[mmbrID].clearEffects()

    def _rearrangeMembers(self):
        lastHeight = 0
        for index, id in enumerate(self.membersOrder):
            mmbr = self.members[id]
            mmbr.component.position.y = lastHeight
            lastHeight += mmbr.component.height

    def _updateHeight(self):
        lastHeight = 0
        for index, id in enumerate(self.membersOrder):
            mmbr = self.members[id]
            mmbr.component.position.y = lastHeight
            lastHeight += mmbr.component.height

        self.component.height = lastHeight

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'partyFrames')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def showPartyFramesEffects(self, doShow):
        for id in self.members:
            cmp = getattr(self.component, 'member{0}'.format(id), None)
            if cmp:
                cmp.script.showBuffs(doShow)

        return

    def tick(self):
        for id in self.members:
            self.members[id].tick()

    def runTicker(self):
        if self.ticker is None:
            self.ticker = self.sharedTicker()
            self.ticker.run()
        return

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        self.component.width = sW
        for id in self.members:
            cmp = getattr(self.component, 'member{0}'.format(id), None)
            if cmp:
                cmp.script.doReposition()

        playerFrame = getattr(BWPersonality.GUICore.worldLayer, 'healthBar', None)
        if playerFrame:
            self.component.position.y = playerFrame.position.y + playerFrame.height + 1
        return

    @BWMemberCoroutine
    def sharedTicker(self):
        while len(self.members):
            yield BWWaitForPeriod(1.0)
            self.tick()

        self.ticker = None
        return