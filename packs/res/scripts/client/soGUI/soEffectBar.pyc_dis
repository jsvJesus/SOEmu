# Embedded file name: scripts/client/soGUI/soEffectBar.py
import BigWorld
import GUI
import BWPersonality
import Keys
import math
import ResMgr
import Helpers.PyGUI as PyGUI
import Helpers.BWKeyBindings as BWKeyBindings
import Helpers.Listener as Listener
from Helpers.BWKeyBindings import BWKeyBindingAction
from Helpers.PyGUI.VisualStateComponent import VisualState, VisualStateComponent
from functools import partial
from encodings import utf_8
DEFAULT_ICON = 'textures/icons/aptechka.tga'
DEFAULT_BORDER = 'soGUI/maps/Icons/bufs/icon_buff__edges.tga'

class soEffectBar(PyGUI.Window, BWKeyBindings.BWActionHandler, Listener.Listenable):
    factoryString = 'soGUI.soEffectBar'
    ACTION_USE = 0
    ACTION_DROP = 1
    BUTTONS_TOTAL = 7
    barData = None
    timerCallback = None
    updateFrequency = 0.1
    BUTTON_WIDTH = 69.0
    BUTTON_HEIGHT = 84.0
    BUTTON_SPACING = 5
    ICON_WIDTH = 64
    ICON_HEIGHT = 64
    DEBUFF_COUNTER_COLOR = (128.0, 0.0, 0.0, 255.0)
    DEBUFF_ICON_COLOR = (255.0, 0.0, 0.0, 255.0)
    DEBUFF_LABEL_COLOR = (126.0, 126.0, 255.0, 255.0)
    BUFF_COUNTER_COLOR = (0.0, 128.0, 0.0, 255.0)
    BUFF_ICON_COLOR = (0.0, 255.0, 0.0, 255.0)
    BUFF_LABEL_COLOR = (126.0, 126.0, 255.0, 255.0)
    NEUTRAL_COUNTER_COLOR = (126.0, 126.0, 255.0, 255.0)
    NEUTRAL_ICON_COLOR = (126.0, 126.0, 255.0, 255.0)
    NEUTRAL_LABEL_COLOR = (126.0, 126.0, 255.0, 255.0)

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        BWPersonality.gpd.keyBindings.addHandler(self)
        BWKeyBindings.BWActionHandler.setupActionList(self)
        self.component.script = self
        self.component.horizontalAnchor = 'RIGHT'
        self.component.verticalAnchor = 'TOP'
        self.component.horizontalPositionMode = 'CLIP'
        self.component.verticalPositionMode = 'CLIP'
        self.component.width = (self.BUTTON_WIDTH + self.BUTTON_SPACING) * self.BUTTONS_TOTAL
        self.component.height = self.BUTTON_HEIGHT
        self.effects = {}
        self.effectButtons = []
        data = ResMgr.openSection('scripts/client/data/EffectsClientData.xml', False)
        if data is not None:
            for entry in data.items():
                if entry[1].name.lower() == 'effect':
                    res = self.getEffectSection(entry[1])
                    self.effects[entry[1]['id'].asInt64] = res

        return

    def getEffectSection(self, data):
        res = {}
        res['id'] = data['id'].asInt64
        res['name'] = data['name'].asString
        res['icon'] = data['icon'].asString
        res['type'] = data['type'].asString
        res['desc'] = data['desc'].asString
        return res

    def makeButton(self, subPos, topText = '', bottomText = ''):
        effectButton = GUI.Window('')
        effectButton = soEffectButton(effectButton)
        effectButton.component.horizontalPositionMode = 'PIXEL'
        effectButton.component.verticalPositionMode = 'PIXEL'
        effectButton.component.horizontalAnchor = 'LEFT'
        effectButton.component.verticalAnchor = 'TOP'
        effectButton.component.position = (0 + (self.BUTTONS_TOTAL - 1) * self.BUTTON_WIDTH - (self.BUTTON_WIDTH + self.BUTTON_SPACING) * subPos, 0.0, 0.0)
        effectButton.component.widthMode = 'PIXEL'
        effectButton.component.heightMode = 'PIXEL'
        effectButton.component.width = self.BUTTON_WIDTH
        effectButton.component.height = self.BUTTON_HEIGHT
        effectButton.component.textureName = ''
        effectButton.component.colour = (255.0, 255.0, 255.0, 255.0)
        effectButton.component.visible = True
        effectButton.component.materialFX = 'BLEND'
        effectButtonLabel = GUI.Text(topText)
        effectButtonIcon = GUI.Simple('')
        effectButtonBorder = GUI.Simple('')
        effectButtonItemCount = GUI.Text(bottomText)
        effectButton.myLabel = effectButtonLabel
        effectButton.myLabel.horizontalPositionMode = 'CLIP'
        effectButton.myLabel.verticalPositionMode = 'CLIP'
        effectButton.myLabel.horizontalAnchor = 'CENTER'
        effectButton.myLabel.verticalAnchor = 'CENTER'
        effectButton.myLabel.widthMode = 'CLIP'
        effectButton.myLabel.heightMode = 'CLIP'
        effectButton.myLabel.width = 0.2
        effectButton.myLabel.height = 0.2
        effectButton.myLabel.colour = (255.0, 255.0, 255.0, 255.0)
        effectButton.myLabel.visible = True
        effectButton.myLabel.position = (0.0, -0.8, 0.0)
        effectButton.myLabel.font = 'system_tiny.font'
        effectButton.myCounter = effectButtonItemCount
        effectButton.myCounter.horizontalPositionMode = 'CLIP'
        effectButton.myCounter.verticalPositionMode = 'CLIP'
        effectButton.myCounter.horizontalAnchor = 'CENTER'
        effectButton.myCounter.verticalAnchor = 'CENTER'
        effectButton.myCounter.widthMode = 'CLIP'
        effectButton.myCounter.heightMode = 'CLIP'
        effectButton.myCounter.width = 0.2
        effectButton.myCounter.height = 0.2
        effectButton.myCounter.colour = (255.0, 255.0, 255.0, 255.0)
        effectButton.myCounter.visible = True
        effectButton.myCounter.position = (0.0, 0.8, 0.0)
        effectButton.myCounter.font = 'system_small.font'
        effectButton.myIcon = effectButtonIcon
        effectButton.myIcon.horizontalPositionMode = 'CLIP'
        effectButton.myIcon.verticalPositionMode = 'CLIP'
        effectButton.myIcon.horizontalAnchor = 'CENTER'
        effectButton.myIcon.verticalAnchor = 'CENTER'
        effectButton.myIcon.widthMode = 'PIXEL'
        effectButton.myIcon.heightMode = 'PIXEL'
        effectButton.myIcon.width = self.ICON_WIDTH
        effectButton.myIcon.height = self.ICON_HEIGHT
        effectButton.myIcon.colour = (255.0, 255.0, 255.0, 255.0)
        effectButton.myIcon.visible = True
        effectButton.myIcon.materialFX = 'BLEND'
        effectButton.myBorder = effectButtonBorder
        effectButton.myBorder.horizontalPositionMode = 'CLIP'
        effectButton.myBorder.verticalPositionMode = 'CLIP'
        effectButton.myBorder.horizontalAnchor = 'CENTER'
        effectButton.myBorder.verticalAnchor = 'CENTER'
        effectButton.myBorder.widthMode = 'PIXEL'
        effectButton.myBorder.heightMode = 'PIXEL'
        effectButton.myBorder.width = self.ICON_WIDTH
        effectButton.myBorder.height = self.ICON_HEIGHT
        effectButton.myBorder.textureName = ''
        effectButton.myBorder.colour = (255.0, 255.0, 255.0, 255.0)
        effectButton.myBorder.visible = True
        effectButton.myBorder.materialFX = 'BLEND'
        effectButton.component.addChild(effectButton.myLabel, 'Label')
        effectButton.component.addChild(effectButton.myIcon, 'Icon')
        effectButton.component.addChild(effectButton.myCounter, 'Counter')
        effectButton.component.addChild(effectButton.myBorder, 'Border')
        return effectButton

    def makeNameBar(self, subPos, topText = '', bottomText = ''):
        effectNameBar = GUI.Window('')
        effectNameBar = soEffectNameBar(effectNameBar)
        iconPos = (0.0, subPos * 1.0, 0.0)
        namePos = (0.25, subPos * 1.0, 0.0)
        stackPos = (0.35, subPos * 1.0, 0.0)
        timePos = (0.55, subPos * 1.0, 0.0)
        effectNameBar.component.horizontalPositionMode = 'CLIP'
        effectNameBar.component.verticalPositionMode = 'CLIP'
        effectNameBar.component.horizontalAnchor = 'LEFT'
        effectNameBar.component.verticalAnchor = 'TOP'
        effectNameBar.component.widthMode = 'CLIP'
        effectNameBar.component.heightMode = 'CLIP'
        effectNameBar.component.width = 1.0
        effectNameBar.component.height = 1.0
        effectNameBar.component.position = iconPos
        effectNameBar.component.textureName = ''
        effectNameBar.component.colour = (255.0, 255.0, 255.0, 255.0)
        effectNameBar.component.visible = True
        effectNameBar.component.materialFX = 'BLEND'
        effectNameBarLabel = GUI.Text(topText)
        effectNameBarIcon = GUI.Simple('')
        effectNameBarItemCount = GUI.Text(bottomText)
        effectNameBarName = GUI.Text('')
        effectNameBar.myLabel = effectNameBarLabel
        effectNameBar.myLabel.horizontalPositionMode = 'CLIP'
        effectNameBar.myLabel.verticalPositionMode = 'CLIP'
        effectNameBar.myLabel.horizontalAnchor = 'CENTER'
        effectNameBar.myLabel.verticalAnchor = 'CENTER'
        effectNameBar.myLabel.widthMode = 'CLIP'
        effectNameBar.myLabel.heightMode = 'CLIP'
        effectNameBar.myLabel.width = 1.0
        effectNameBar.myLabel.height = 1.0
        effectNameBar.myLabel.colour = self.DEBUFF_LABEL_COLOR
        effectNameBar.myLabel.visible = True
        effectNameBar.myLabel.position = timePos
        effectNameBar.myLabel.font = 'system_tiny.font'
        effectNameBar.myName = effectNameBarName
        effectNameBar.myName.horizontalPositionMode = 'CLIP'
        effectNameBar.myName.verticalPositionMode = 'CLIP'
        effectNameBar.myName.horizontalAnchor = 'LEFT'
        effectNameBar.myName.verticalAnchor = 'TOP'
        effectNameBar.myName.widthMode = 'CLIP'
        effectNameBar.myName.heightMode = 'CLIP'
        effectNameBar.myName.width = 1.0
        effectNameBar.myName.height = 1.0
        effectNameBar.myName.colour = self.DEBUFF_LABEL_COLOR
        effectNameBar.myName.visible = True
        effectNameBar.myName.position = timePos
        effectNameBar.myName.font = 'system_tiny.font'
        effectNameBar.myCounter = effectNameBarItemCount
        effectNameBar.myCounter.horizontalPositionMode = 'CLIP'
        effectNameBar.myCounter.verticalPositionMode = 'CLIP'
        effectNameBar.myCounter.horizontalAnchor = 'CENTER'
        effectNameBar.myCounter.verticalAnchor = 'CENTER'
        effectNameBar.myCounter.widthMode = 'CLIP'
        effectNameBar.myCounter.heightMode = 'CLIP'
        effectNameBar.myCounter.width = 1.0
        effectNameBar.myCounter.height = 1.0
        effectNameBar.myCounter.colour = self.DEBUFF_COUNTER_COLOR
        effectNameBar.myCounter.visible = True
        effectNameBar.myCounter.position = namePos
        effectNameBar.myCounter.font = 'system_small.font'
        effectNameBar.myIcon = effectNameBarIcon
        effectNameBar.myIcon.horizontalPositionMode = 'CLIP'
        effectNameBar.myIcon.verticalPositionMode = 'CLIP'
        effectNameBar.myIcon.horizontalAnchor = 'LEFT'
        effectNameBar.myIcon.verticalAnchor = 'TOP'
        effectNameBar.myIcon.widthMode = 'CLIP'
        effectNameBar.myIcon.heightMode = 'CLIP'
        effectNameBar.myIcon.width = self.ICON_WIDTH
        effectNameBar.myIcon.height = self.ICON_HEIGHT
        effectNameBar.myIcon.colour = self.DEBUFF_ICON_COLOR
        effectNameBar.myIcon.visible = True
        effectNameBar.myIcon.materialFX = 'BLEND'
        effectNameBar.component.addChild(effectNameBar.myLabel, 'Label')
        effectNameBar.component.addChild(effectNameBar.myIcon, 'Icon')
        effectNameBar.component.addChild(effectNameBar.myCounter, 'Counter')
        effectNameBar.component.addChild(effectNameBar.myName, 'Name')
        return effectNameBar

    def onBound(self):
        for i in range(self.BUTTONS_TOTAL):
            self.effectButtons.append(self.makeButton(i, '', ''))
            self.component.addChild(self.effectButtons[i].component, 'slot' + str(i))

    def setItems(self, newVal):
        self.barData = newVal
        try:
            slot0 = self.component.__getattribute__('slot' + str(0))
            self.updateBarData(True)
        except ReferenceError:
            BigWorld.callback(1.0, self.updateBarData(True))

    def getDurationText(self, duration):
        if duration >= 3600.0:
            return '%dh' % (duration / 3600.0)
        elif duration >= 60.0:
            return '%dm' % (duration / 60.0)
        elif duration >= 1.0:
            return '%d' % duration
        elif duration < 0:
            return ''
        else:
            return '%1.1f' % duration

    def shouldUpdateDuration(self, duration):
        if duration >= 3600.0:
            return duration % 60 * 60 < 1
        if duration >= 60.0:
            return duration % 60 < 1
        if duration >= 1.0:
            return True

    def stopUpdate(self):
        if self.timerCallback is not None:
            BigWorld.cancelCallback(self.timerCallback)
        return

    def updateSlotEffect(self, slot, eff):
        if eff is not None:
            slot.script.setTextures(eff['icon'])
            if eff['type'] == 'debuff':
                slot.Counter.colour = self.DEBUFF_COUNTER_COLOR
                slot.Label.colour = self.DEBUFF_LABEL_COLOR
                slot.Border.colour = self.DEBUFF_ICON_COLOR
            elif eff['type'] == 'buff':
                slot.Counter.colour = self.BUFF_COUNTER_COLOR
                slot.Label.colour = self.BUFF_LABEL_COLOR
                slot.Border.colour = self.BUFF_ICON_COLOR
            else:
                slot.Counter.colour = self.NEUTRAL_COUNTER_COLOR
                slot.Label.colour = self.NEUTRAL_LABEL_COLOR
                slot.Border.colour = self.NEUTRAL_ICON_COLOR
        else:
            slot.Counter.colour = self.NEUTRAL_COUNTER_COLOR
            slot.Label.colour = self.NEUTRAL_LABEL_COLOR
            slot.Border.colour = self.NEUTRAL_ICON_COLOR
        return

    def updateBarData(self, updateAll = False):
        if updateAll:
            if self.timerCallback is not None:
                BigWorld.cancelCallback(self.timerCallback)
        for i in range(min(self.BUTTONS_TOTAL, len(self.barData))):
            slot = self.component.__getattribute__('slot' + str(i))
            val = self.barData[i]
            if updateAll:
                eff = None
                if self.effects.has_key(val.id):
                    eff = self.effects[val.id]
                elif self.effects.has_key(-1):
                    eff = self.effects[-1]
                elif val.id == 1:
                    slot.Icon.textureName = 'textures/icons/loot_spider_small.tga'
                else:
                    slot.Icon.textureName = 'textures/icons/aptechka.tga'
                self.updateSlotEffect(slot, eff)
                slot.Counter.text = str(val.counter)
                slot.Label.text = self.getDurationText(val.duration)
            else:
                if val.duration > 0:
                    val.duration -= self.updateFrequency
                if self.shouldUpdateDuration(val.duration):
                    slot.Label.text = self.getDurationText(val.duration)

        if updateAll:
            if len(self.barData) > 0:
                r = range(i + 1, self.BUTTONS_TOTAL)
            else:
                r = range(self.BUTTONS_TOTAL)
            for j in r:
                slot = self.component.__getattribute__('slot' + str(j))
                slot.script.setEmpty()

        if len(self.barData) > 0:
            self.timerCallback = BigWorld.callback(self.updateFrequency, self.updateBarData)
        else:
            if self.timerCallback is not None:
                BigWorld.cancelCallback(self.timerCallback)
            self.timerCallback = None
        return


class soEffectButton(PyGUI.Window):
    factoryString = 'soGUI.soeffectButton'

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        self.component.script = self
        self.myLabel = None
        self.myIcon = None
        self.myCounter = None
        self.active = False
        return

    def setEmpty(self):
        self.component.textureName = ''
        self.myLabel.text = ''
        self.myIcon.textureName = ''
        self.myBorder.textureName = ''
        self.myIcon.texture = None
        self.myBorder.texture = None
        self.myCounter.text = ''
        self.active = False
        return

    def setTextures(self, iconTexture, borderTexture = DEFAULT_BORDER):

        def onGetTexture(res):
            if not self.active:
                return
            else:
                if iconTexture not in res.failedIDs:
                    self.myIcon.texture = res[iconTexture]
                elif DEFAULT_ICON not in res.failedIDs:
                    self.myIcon.texture = res[DEFAULT_ICON]
                else:
                    self.myIcon.texture = None
                if borderTexture not in res.failedIDs:
                    self.myBorder.texture = res[borderTexture]
                else:
                    self.myBorder.texture = None
                return

        self.active = True
        BigWorld.loadResourceListBG((iconTexture, borderTexture, DEFAULT_ICON), onGetTexture)


class soEffectNameBar(PyGUI.Window):
    factoryString = 'soGUI.soEffectNameBar'

    def __init__(self, component):
        PyGUI.Window.__init__(self, component)
        self.component.script = self
        self.myLabel = None
        self.myIcon = None
        self.myCounter = None
        self.myEffectName = None
        return

    def setEmpty(self):
        self.component.textureName = ''
        self.myLabel.text = ''
        self.myEffectName.text = ''
        self.myIcon.textureName = ''
        self.myCounter.text = ''