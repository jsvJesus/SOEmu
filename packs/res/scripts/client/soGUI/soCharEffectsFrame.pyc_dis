# Embedded file name: scripts/client/soGUI/soCharEffectsFrame.py
import BigWorld
import GUI
import BWPersonality
import soGUI
import Helpers.PyGUI as PyGUI
import soGUI.data.TextureFeed as TextureFeed
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.BWCoroutine import *
from soGUI.soToolTipComponent import soToolTipComponent
import Helpers.PyGUI.Utils as Utils
from math import floor, ceil
from EffectUtils import EFFECT_TYPE
from Localization import lc
HIGHLIGHT_MAP = {EFFECT_TYPE.BUFF: [(29, 42, 4, 255), (29, 42, 4, 255)],
 EFFECT_TYPE.DEBUFF: [(66, 6, 6, 255), (66, 6, 6, 255)],
 EFFECT_TYPE.UNDEFINED: [(255, 255, 255, 255), (255, 255, 255, 255)]}
BUFFFRAME_TEXTUREPROVIDER = BigWorld.PyTextureProvider('soGUI/maps/Controls/buffFrames/frame.tga')

class soEffectSlot(PyGUIBase, soToolTipComponent):
    factoryString = 'soGUI.soEffectSlot'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        soToolTipComponent.__init__(self, component, None)
        component.script = self
        self.toolTipID = None
        self.interfaceID = BWPersonality.GUICore.GUI_ID_EFFECTSFRAME
        self.expireTime = 0
        self.icon = None
        self.effectType = EFFECT_TYPE.UNDEFINED
        self.effectID = None
        self.stackSize = 0
        self.newIcon = False
        self.setupRoot()
        self.setupContent()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.width = 21
        cmp.height = 39
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.textureName = ''
        cmp.crossFocus = True

    def setupContent(self):
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 21
        cmp.height = 21
        cmp.position = (0, 8, 0.5)
        self.component.addChild(cmp, 'icon')
        cmp = GUI.Text('')
        cmp.font = 'ruRU_Cyrvetica_Extra_9.font'
        cmp.colour = (255, 255, 215, 255)
        cmp.materialFX = 'BLEND'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.position = (11, 34, 0.3)
        self.component.addChild(cmp, 'timer')
        cmp = GUI.Simple('soGUI/maps/Controls/buffFrames/frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.materialFX = 'BLEND'
        cmp.colour = HIGHLIGHT_MAP[EFFECT_TYPE.UNDEFINED][1]
        cmp.width = 21
        cmp.height = 39
        cmp.position = (0, 0, 0.4)
        self.component.addChild(cmp, 'buffFrame')
        cmp = GUI.Text('')
        cmp.font = 'ruRU_Cyrvetica_Extra_9.font'
        cmp.colour = (255, 255, 215, 255)
        cmp.materialFX = 'BLEND'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.position = (11, 5, 0.3)
        self.component.addChild(cmp, 'stacks')

    def setTime(self, secs):
        self.expireTime = secs

    def setID(self, id):
        self.effectID = id
        self.toolTipID = id

    def setIcon(self, icon):
        self.icon = icon
        self.newIcon = True

    def setType(self, eType):
        self.effectType = eType

    def setStack(self, stackSize):
        self.stackSize = stackSize

    def tick(self):
        if self.expireTime > 0:
            self.expireTime -= 1
        self._applyData()

    def _applyData(self):
        if self.newIcon:
            self.newIcon = False
            texture = TextureFeed.buffFeed.getBuffTexture(self.icon)
            if texture is None:
                self.component.icon.textureName = ''
            else:
                self.component.icon.texture = texture[0]
                Utils.applyMapping(self.component.icon, 'PIXEL', texture[1])
        if self.component.buffFrame.colour != HIGHLIGHT_MAP[self.effectType][1]:
            self.component.buffFrame.colour = HIGHLIGHT_MAP[self.effectType][1]
        timeStr = self.timeToString(self.expireTime)
        if self.component.timer.text != timeStr:
            self.component.timer.text = timeStr
        if self.stackSize > 0:
            self.component.stacks.text = str(self.stackSize)
        else:
            self.component.stacks.text = u''
        return

    def handleMouseEnterEvent(self, component):
        soToolTipComponent.handleMouseEnterEvent(self, component)
        return True

    def handleMouseLeaveEvent(self, component):
        soToolTipComponent.handleMouseLeaveEvent(self, component)
        return True

    def fini(self):
        self.clearAllChildren(self.component)
        self.component.script = None
        self.component = None
        return

    def timeToString(self, secs):
        if secs < 0:
            return u''
        hours = floor(secs / 3600.0)
        minutes = floor((secs - hours * 3600.0) / 60.0)
        seconds = secs - (hours * 3600.0 + minutes * 60.0)
        outH = str(int(hours)) if hours > 9 else u'0' + str(int(hours))
        outM = str(int(minutes)) if minutes > 9 else u'0' + str(int(minutes))
        outS = str(int(seconds)) if seconds > 9 else u'0' + str(int(seconds))
        if hours > 0:
            return u'' + outH + lc('GUI.General.HOURS_SHORTENING')
        if minutes > 0:
            return u'' + outM + lc('GUI.General.MINUTES_SHORTENING')
        if seconds >= 0:
            return u'' + outS + lc('GUI.General.SECONDS_SHORTENING')
        return u''


class soCharEffectsGUI(PyGUIBase):
    factoryString = 'soGUI.soCharEffectsGUI'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.effectsObj = []
        self.effects = {}
        self.tC = 0
        self.rawData = None
        self.ticker = None
        self.setupRoot()
        return

    def setupRoot(self):
        sW, sH = BigWorld.screenSize()
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 0
        cmp.height = 0
        pX = sW - 10
        pY = 10
        if hasattr(BWPersonality.GUICore.worldLayer, 'minimap'):
            pX = BWPersonality.GUICore.worldLayer.minimap.position.x - (BWPersonality.GUICore.worldLayer.minimap.width + 10)
        cmp.position = (pX, pY, 0.5)
        BWPersonality.GUICore.worldLayer.addChild(cmp, 'effectsFrame')

    def renderEffects(self):
        self.component.height = 39
        effectCount = len(self.effects)
        self.component.width = effectCount * 21 + (effectCount - 1)
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
            cmpt = getattr(self.component, 'effect' + str(id))
            cmpt.horizontalPositionMode = cmpt.verticalPositionMode = 'PIXEL'
            cmpt.horizontalAnchor = 'RIGHT'
            cmpt.verticalAnchor = 'TOP'
            cmpt.position = (self.component.width - i * 22, 0, 0.5)

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

        if len(self.effects) > 0 and self.ticker is None:
            self.ticker = self.sharedTicker()
            self.ticker.run()
        self.renderEffects()
        return

    def tick(self):
        for id in self.effects:
            if self.effects[id][1] > 0:
                self.effects[id][1] -= 1
            if hasattr(self.component, 'effect' + str(id)):
                cmp = getattr(self.component, 'effect' + str(id))
                cmp.script.tick()

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

    def show(self):
        self.component.visible = True

    def hide(self):
        self.component.visible = False

    def doReposition(self):
        sW, sH = BigWorld.screenSize()
        cmp = self.component
        pX = sW - 10
        pY = 10
        if hasattr(BWPersonality.GUICore.worldLayer, 'minimap'):
            pX = BWPersonality.GUICore.worldLayer.minimap.position.x - (BWPersonality.GUICore.worldLayer.minimap.width + 10)
        cmp.position = (pX, pY, 0.5)

    @BWMemberCoroutine
    def sharedTicker(self):
        while len(self.effects):
            yield BWWaitForPeriod(1.0)
            self.tick()

        self.ticker = None
        return