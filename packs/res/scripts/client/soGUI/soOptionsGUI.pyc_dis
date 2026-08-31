# Embedded file name: scripts/client/soGUI/soOptionsGUI.py
from Localization import lc
import BigWorld
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
import BWPersonality
import Helpers.PyGUI.PyGUIBase as PyGUIBase
from Helpers.PyGUI import PyGUIEvent
from soGUI.soButton import soButton
from soGUI.soSlider import soSlider
from soGUI.soDropDownList import soDropDownList, soDropDownList2
from soGUI.soCheckBox import soCheckBox
from functools import partial
from soGUI.soTableComponent import soTableComponent2, soTablePropsStructure, soTableElemPropsStructure
from soGUI.soEditField import soEditField2
from soGUI.soScrollBar import soScrollBar2
from Keys import *
from math import ceil, floor
from Helpers import BWKeyBindings
MODIFIER_CODES = []
from Helpers.PyGUI.Window import DraggableWindow
import random
from functools import partial

def clear():
    while len(GUI.roots()):
        GUI.delRoot(GUI.roots()[0])


def _deleteComponent(t):
    if t.parent:
        t.parent.delChild(t)
    else:
        GUI.delRoot(t)


class TestWindow(PyGUIBase):
    factoryString = 'soGUI.TestWindow'
    settings_list = ['TEXTURE_QUALITY',
     'SHADOWS_QUALITY',
     'TEXTURE_FILTERING',
     'SPEEDTREE_QUALITY',
     'WATER_QUALITY',
     'SSAO',
     'FAR_PLANE',
     'WATER_SIMULATION',
     'SHADOWS_COUNT',
     'TERRAIN_MESH_RESOLUTION',
     'FOOT_PRINTS',
     'god rays',
     'FLORA_DENSITY',
     'DYNAMIC_SHADOW']

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.interfaceID = BWPersonality.GUICore.GUI_ID_OPTIONS
        self.setupRoot()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.position = (0.0, 0.0, 0.04)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 600
        cmp.height = 400
        cmp.visible = False
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, '111')
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
        cmp.position = (580, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        data = self.getData()
        additionValue = BWPersonality.settings.getAdditionOptionValue()
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1081_13')
        cmp.position = (10, 40, 0.3)
        self.component.addChild(cmp, 'textureQualityLabel')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (10, 60, 0.1)
        self.component.addChild(cmp, 'texture_quality')
        ddl.onBound()
        options = data['TEXTURE_QUALITY']['options']
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByText(options[data['TEXTURE_QUALITY']['current']], True, silent=True)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1082_13')
        cmp.position = (10, 100, 0.3)
        self.component.addChild(cmp, 'shadowQualityLabel')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (10, 120, 0.1)
        self.component.addChild(cmp, 'shadows_quality')
        ddl.onBound()
        options = data['SHADOWS_QUALITY']['options']
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByText(options[data['SHADOWS_QUALITY']['current']], True, silent=True)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1083_13')
        cmp.position = (10, 160, 0.3)
        self.component.addChild(cmp, 'textureFilteringLabel')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (10, 180, 0.1)
        self.component.addChild(cmp, 'texture_filtering')
        ddl.onBound()
        options = data['TEXTURE_FILTERING']['options']
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByText(options[data['TEXTURE_FILTERING']['current']], True, silent=True)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1084_13')
        cmp.position = (10, 220, 0.3)
        self.component.addChild(cmp, 'speedtreeQuality')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (10, 240, 0.1)
        self.component.addChild(cmp, 'speedtree_quality')
        ddl.onBound()
        options = data['SPEEDTREE_QUALITY']['options']
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByText(options[data['SPEEDTREE_QUALITY']['current']], True, silent=True)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1085_13')
        cmp.position = (200, 40, 0.3)
        self.component.addChild(cmp, 'waterQuality')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (200, 60, 0.1)
        self.component.addChild(cmp, 'water_quality')
        ddl.onBound()
        options = data['WATER_QUALITY']['options']
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByText(options[data['WATER_QUALITY']['current']], True, silent=True)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1086_13')
        cmp.position = (200, 100, 0.3)
        self.component.addChild(cmp, 'ssao')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (200, 120, 0.1)
        self.component.addChild(cmp, 'SSAO')
        ddl.onBound()
        options = additionValue['SSAO'][1]
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByValue(additionValue['SSAO'][0], True)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1087_13')
        cmp.position = (200, 160, 0.3)
        self.component.addChild(cmp, 'farPlane')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (200, 180, 0.1)
        self.component.addChild(cmp, 'far_plane')
        ddl.onBound()
        options = data['FAR_PLANE']['options']
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByText(options[data['FAR_PLANE']['current']], True, silent=True)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1088_13')
        cmp.position = (200, 220, 0.3)
        self.component.addChild(cmp, 'waterSimulation')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (200, 240, 0.1)
        self.component.addChild(cmp, 'water_simulation')
        ddl.onBound()
        options = data['WATER_SIMULATION']['options']
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByText(options[data['WATER_SIMULATION']['current']], True, silent=True)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1089_13')
        cmp.position = (390, 40, 0.3)
        self.component.addChild(cmp, 'shadowsCount')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (390, 60, 0.1)
        self.component.addChild(cmp, 'shadows_count')
        ddl.onBound()
        options = data['SHADOWS_COUNT']['options']
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByText(options[data['SHADOWS_COUNT']['current']], True, silent=True)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1093_13')
        cmp.position = (390, 100, 0.3)
        self.component.addChild(cmp, 'footPrints')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (390, 120, 0.1)
        self.component.addChild(cmp, 'foot_prints')
        ddl.onBound()
        options = data['FOOT_PRINTS']['options']
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByText(options[data['FOOT_PRINTS']['current']], True, silent=True)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1095_13')
        cmp.position = (390, 160, 0.3)
        self.component.addChild(cmp, 'godRays')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (390, 180, 0.1)
        self.component.addChild(cmp, 'god_rays')
        ddl.onBound()
        options = additionValue['god rays'][1]
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByValue(additionValue['god rays'][0], True)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1094_13')
        cmp.position = (390, 220, 0.3)
        self.component.addChild(cmp, 'floraDensity')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (390, 240, 0.1)
        self.component.addChild(cmp, 'flora_density')
        ddl.onBound()
        options = data['FLORA_DENSITY']['options']
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByText(options[data['FLORA_DENSITY']['current']], True, silent=True)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = 'Dynamic Shadow'
        cmp.position = (390, 280, 0.3)
        self.component.addChild(cmp, 'dynamicShadow')
        ddl = soDropDownList2(GUI.Window(), width=150, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (390, 300, 0.1)
        self.component.addChild(cmp, 'dynamicShadow_list')
        ddl.onBound()
        options = data['DYNAMIC_SHADOW']['options']
        ddl.addElements(list(enumerate(options)))
        ddl.setSelectionByText(options[data['DYNAMIC_SHADOW']['current']], True, silent=True)
        self.setupButtons()

    def setupButtons(self):
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = u'Ok'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 64
        cmp.height = 29
        cmp.position = (347, 367, 0.5)
        self.component.addChild(cmp, 'okSettinsBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soOptionsGUI.soGUI.STRING_159_19')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 64
        cmp.height = 29
        cmp.position = (415, 367, 0.5)
        self.component.addChild(cmp, 'cancelSettinsBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soOptionsGUI.soGUI.STRING_180_19')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 28
        cmp.position = (485, 367, 0.5)
        self.component.addChild(cmp, 'applySettinsBtn')
        btn.onBound()
        btn.setVisualState('normal')

    def getData(self):
        data = {}
        setList = filter(lambda x, sl = self.settings_list: x[0] in sl, BigWorld.graphicsSettings())
        for setting in setList:
            data[setting[0]] = {'name': setting[3],
             'options': [ x[2] for x in setting[2] ],
             'current': setting[1]}

        return data

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.generalLayer.addChild(self.component, 'add')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        BWPersonality.GUICore.updateTopmostObjects()

    def applySettings(self):
        data = {}
        data['TEXTURE_QUALITY'] = self.component.texture_quality.script.getSelection()[1]
        data['SHADOWS_QUALITY'] = self.component.shadows_quality.script.getSelection()[1]
        data['TEXTURE_FILTERING'] = self.component.texture_filtering.script.getSelection()[1]
        data['SPEEDTREE_QUALITY'] = self.component.speedtree_quality.script.getSelection()[1]
        data['WATER_QUALITY'] = self.component.water_quality.script.getSelection()[1]
        data['SSAO'] = self.component.SSAO.script.getSelection()[1]
        data['FAR_PLANE'] = self.component.far_plane.script.getSelection()[1]
        data['WATER_SIMULATION'] = self.component.water_simulation.script.getSelection()[1]
        data['SHADOWS_COUNT'] = self.component.shadows_count.script.getSelection()[1]
        data['FOOT_PRINTS'] = self.component.foot_prints.script.getSelection()[1]
        data['god rays'] = self.component.god_rays.script.getSelection()[1]
        data['FLORA_DENSITY'] = self.component.flora_density.script.getSelection()[1]
        data['DYNAMIC_SHADOW'] = self.component.dynamicShadow.script.getSelection()[1]
        BWPersonality.GUICore.optionsGUI.setCustomPreset()
        self._sendEvent(soOptionsGUI2.EVENT_APPLY_SETTINGS, data)

    def _sendEvent(self, event, data):
        BWPersonality.GUICore.optionsEvent(event, data)

    def handleKeyEvent(self, event):
        key = event.key
        char = event.character
        mods = event.modifiers
        down = event.isKeyDown()
        print 'key: ', key
        return False

    @PyGUIEvent('closeBox', 'onClick')
    @PyGUIEvent('cancelSettinsBtn', 'onClick')
    def onCloseBox(self):
        self.hide()

    @PyGUIEvent('okSettinsBtn', 'onClick')
    def onOK(self):
        self.applySettings()
        self.hide()

    @PyGUIEvent('applySettinsBtn', 'onClick')
    def onApply(self):
        self.applySettings()


class soOptionsGUI(PyGUIBase):
    factoryString = 'soGUI.soOptionsGUI'
    EVENT_APPLY = 0
    EVENT_FS = 1

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupFrame()
        self.setupControls()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 279
        cmp.height = 393
        cmp.position = (0.0, 0.0, 0.0)
        cmp.textureName = ''
        cmp.visible = False
        cmp.mouseButtonFocus = True
        cmp.crossFocus = True

    def setupFrame(self):
        cmp = GUI.Simple('soGUI/maps/Options/window.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 279
        cmp.height = 393
        cmp.position = (0, 0, 1.0)
        self.component.addChild(cmp, 'frameCmp')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (97, 16, 0.9)
        cmp.text = lc('soOptionsGUI.soGUI.STRING_80_13')
        self.component.addChild(cmp, 'options_label')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (22, 51, 0.9)
        cmp.text = lc('soOptionsGUI.soGUI.STRING_91_13')
        self.component.addChild(cmp, 'screenRes_label')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (22, 136, 0.9)
        cmp.text = lc('soOptionsGUI.soGUI.STRING_102_13')
        self.component.addChild(cmp, 'detail_label')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (22, 212, 0.9)
        cmp.text = lc('soOptionsGUI.soGUI.STRING_113_13')
        self.component.addChild(cmp, 'effectsVolume_label')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.font = 'ruRU_calibri_default.font'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (22, 285, 0.9)
        cmp.text = lc('soOptionsGUI.soGUI.STRING_124_13')
        self.component.addChild(cmp, 'musicVolume_label')

    def setupControls(self):
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = u'Ok'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 64
        cmp.height = 29
        cmp.position = (17, 346, 0.5)
        self.component.addChild(cmp, 'okBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soOptionsGUI.soGUI.STRING_159_19')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 64
        cmp.height = 29
        cmp.position = (85, 346, 0.5)
        self.component.addChild(cmp, 'cancelBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soOptionsGUI.soGUI.STRING_180_19')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 28
        cmp.position = (155, 346, 0.5)
        self.component.addChild(cmp, 'applyBtn')
        btn.onBound()
        btn.setVisualState('normal')
        slider = soSlider(GUI.Window())
        cmp = slider.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (22, 233, 0.1)
        slider.onBound()
        self.component.addChild(cmp, 'sfxSlider')
        slider.setLimits(0.0, 1.0)
        slider = soSlider(GUI.Window())
        cmp = slider.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (22, 300, 0.1)
        slider.onBound()
        self.component.addChild(cmp, 'musicSlider')
        slider.setLimits(0.0, 1.0)
        ddl = soDropDownList(GUI.Window(), soGUI.DropDownListPropsStructure(DDLWidth=228, DDLHeight=150, btnW=29, btnH=29, DDLElemHeight=18, sorted=False))
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (22, 152, 0.1)
        self.component.addChild(cmp, 'details')
        ddl.onBound()
        ddl = soDropDownList(GUI.Window(), soGUI.DropDownListPropsStructure(DDLWidth=228, DDLHeight=150, btnW=29, btnH=29, DDLElemHeight=18, sorted=False))
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (22, 68, 0.1)
        self.component.addChild(cmp, 'resolution')
        ddl.onBound()
        cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=lc('soOptionsGUI.soGUI.STRING_240_73')))
        cmp = cb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (44, 109, 0.4)
        self.component.addChild(cmp, 'fullScreen')
        cb.onBound()

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.systemLayer.addChild(self.component, 'options')
        self.component.visible = True
        self.update()
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()

    def update(self):
        data = BWPersonality.GUICore.optionsDataSection
        if data is None:
            return
        else:
            if data.has_key('resolution_list'):
                self.component.resolution.script.clear()
                for resolution in data['resolution_list']:
                    self.component.resolution.script.addElement(resolution)

            if data.has_key('detail_levels'):
                self.component.details.script.clear()
                for detail in data['detail_levels']:
                    self.component.details.script.addElement(detail)

            if data.has_key('sfx_volume'):
                self.component.sfxSlider.script.setValue(data['sfx_volume'])
            if data.has_key('music_volume'):
                self.component.musicSlider.script.setValue(data['music_volume'])
            if data.has_key('resolution'):
                self.component.resolution.script.setSelection(data['resolution'])
            if data.has_key('detail_level'):
                self.component.details.script.setSelection(data['detail_level'])
            if data.has_key('fullscreen'):
                if data['fullscreen']:
                    self.component.fullScreen.script.setActive()
                else:
                    self.component.fullScreen.script.setInactive()
            return

    def applySettings(self):
        data = {'resolution': self.component.resolution.script.getSelection(),
         'details': self.component.details.script.getSelection(),
         'sfx': self.component.sfxSlider.script.getValue(),
         'music': self.component.musicSlider.script.getValue(),
         'fullscreen': self.component.fullScreen.script.isChecked()}
        BWPersonality.GUICore.optionsEvent(self.EVENT_APPLY, data)

    def fullScreenStatus(self, checked = True):
        BWPersonality.GUICore.optionsEvent(self.EVENT_FS, checked)

    def close(self):
        pass

    @PyGUIEvent('okBtn', 'onClick')
    def okBtnClicked(self):
        self.applySettings()
        BWPersonality.GUICore.showOptions(False)

    @PyGUIEvent('cancelBtn', 'onClick')
    def cancelBtnClicked(self):
        BWPersonality.GUICore.showOptions(False)

    @PyGUIEvent('applyBtn', 'onClick')
    def applyBtnClicked(self):
        self.applySettings()

    @PyGUIEvent('fullScreen', 'onStateChange')
    def fullScreenCheck(self):
        self.fullScreenStatus(self.component.fullScreen.script.isChecked())


class soOptionsGUI2(PyGUIBase):
    factoryString = 'soGUI.soOptionsGUI2'
    TAB_KEYBOARD = 0
    TAB_MOUSE = 1
    TAB_AUDIO = 2
    TAB_VIDEO = 3
    EVENT_OK = 0
    EVENT_CANCEL = 1
    EVENT_APPLY = 2
    EVENT_OPTIONSET = 3
    EVENT_EXPERTOK = 4
    EVENT_EXPERTCANCEL = 5
    EVENT_KEYBINDS_DEFAULT = 6
    EVENT_KEYBINDS_CLEAR = 7
    EVENT_APPLY_SETTINGS = 8
    SOUND_QUALITY_LOW = 0
    SOUND_QUALITY_MED = 1
    SOUND_QUALITY_HIGH = 2
    VIDEO_QUALITY_CUSTOM = 0
    VIDEO_QUALITY_LOW = 1
    VIDEO_QUALITY_NORMAL = 2
    VIDEO_QUALITY_HIGH = 3
    VIDEO_QUALITY_ULTRA = 4
    CONTROLTYPE_SLIDER = 0
    CONTROLTYPE_CHECKBOX = 1
    CONTROLTYPE_COMBO = 2
    KEYBINDER_PROMT = lc('soOptionsGUI.soGUI.STRING_359_19')
    TAB_LABELS = {TAB_KEYBOARD: lc('soOptionsGUI.soGUI.STRING_362_18'),
     TAB_MOUSE: lc('soOptionsGUI.soGUI.STRING_363_15'),
     TAB_AUDIO: lc('soOptionsGUI.soGUI.STRING_364_15'),
     TAB_VIDEO: lc('soOptionsGUI.soGUI.STRING_365_15')}
    VQ_LABELS = {VIDEO_QUALITY_CUSTOM: lc('soOptionsGUI.soGUI.STRING_369_26'),
     VIDEO_QUALITY_LOW: lc('soOptionsGUI.soGUI.STRING_370_23'),
     VIDEO_QUALITY_NORMAL: lc('soOptionsGUI.soGUI.STRING_371_26'),
     VIDEO_QUALITY_HIGH: lc('soOptionsGUI.soGUI.STRING_372_24'),
     VIDEO_QUALITY_ULTRA: lc('soOptionsGUI.soGUI.STRING_373_25')}
    SQ_LABELS = {SOUND_QUALITY_LOW: lc('soOptionsGUI.soGUI.STRING_377_23'),
     SOUND_QUALITY_MED: lc('soOptionsGUI.soGUI.STRING_378_23'),
     SOUND_QUALITY_HIGH: lc('soOptionsGUI.soGUI.STRING_379_24')}

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.interfaceID = BWPersonality.GUICore.GUI_ID_OPTIONS
        self.currentTab = None
        self.expertWnd = None
        self.keyBindAction = None
        self.evoScroll = 0
        self.evoMaxScroll = 0
        self.keyTable_captionDS = {'font': 'ruRU_calibri_default.font',
         'color': (28, 28, 28, 255),
         'hoverColor': (28, 28, 28, 255),
         'selectColor': (28, 28, 28, 255),
         'toolTipID': None,
         'contentColor': (175, 166, 112, 255),
         'contentColorHover': (175, 166, 112, 255),
         'contentColorSelect': (175, 166, 112, 255)}
        self.keyTable_dataDS = {'font': 'ruRU_calibri_default.font',
         'color': (255, 255, 255, 0),
         'hoverColor': (255, 255, 255, 0),
         'selectColor': (28, 28, 28, 255),
         'toolTipID': None,
         'contentColor': (175, 166, 112, 255),
         'contentColorHover': (175, 166, 112, 255),
         'contentColorSelect': (175, 166, 112, 255)}
        self.keyTable_dataDS2 = {'font': 'ruRU_calibri_default.font',
         'color': (255, 255, 255, 0),
         'hoverColor': (255, 255, 255, 0),
         'selectColor': (28, 28, 28, 255),
         'toolTipID': None,
         'contentColor': (255, 112, 112, 255),
         'contentColorHover': (255, 112, 112, 255),
         'contentColorSelect': (255, 112, 112, 255)}
        self.setupRoot()
        self.setupKeyBoard()
        self.setupMouse()
        self.setupAudio()
        self.setupVideo()
        self.setupKeyBinder()
        self.tabSelect(self.TAB_KEYBOARD)
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.position = (0.0, 0.0, 0.04)
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 529
        cmp.height = 403
        cmp.visible = False
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'frameCmp')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = u'Ok'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (199, 370, 0.5)
        self.component.addChild(cmp, 'okBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soOptionsGUI.soGUI.STRING_488_19')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (309, 370, 0.5)
        self.component.addChild(cmp, 'cancelBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soOptionsGUI.soGUI.STRING_509_19')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (418, 370, 0.5)
        self.component.addChild(cmp, 'applyBtn')
        btn.onBound()
        btn.setVisualState('normal')
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
        cmp.position = (505, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.component.addChild(cmp, 'closeBox')
        for i, tab in enumerate([self.TAB_KEYBOARD,
         self.TAB_MOUSE,
         self.TAB_AUDIO,
         self.TAB_VIDEO]):
            btn = soButton(GUI.Window())
            cmp = btn.component
            cmp.verticalPositionMode = cmp.horizontalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.width = 110
            cmp.height = 21
            cmp.position = (8 + i * 110, 7, 0.4)
            btn.buttonStyle = soButton.TOGGLEBUTTON_STYLE
            btn.onClick = partial(self.tabSelect, tab)
            btn.initVSC('soGUI/visual_styles/skillTab.xml')
            btn.onBound()
            btn.setVisualState('normal')
            cmp.label.text = self.TAB_LABELS[tab]
            self.component.addChild(btn.component, 'tab' + str(tab))

    def setupKeyBoard(self):
        wnd = GUI.Window()
        wnd.horizontalPositionMode = wnd.verticalPositionMode = 'PIXEL'
        wnd.widthMode = wnd.heightMode = 'PIXEL'
        wnd.horizontalAnchor = 'LEFT'
        wnd.verticalAnchor = 'TOP'
        wnd.materialFX = 'BLEND'
        wnd.colour = (255, 255, 255, 255)
        wnd.width = 521
        wnd.height = 334
        wnd.position = (4, 31, 0.2)
        wnd.visible = False
        self.component.addChild(wnd, 'wnd' + str(self.TAB_KEYBOARD))
        cmp = GUI.Frame2('soGUI/maps/Controls/window_frame/options_inner_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        wnd.addChild(cmp, 'innerFrame')
        cmp = GUI.Frame2('soGUI/maps/Controls/window_frame/options_inner_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 521
        cmp.height = 35
        cmp.position = (0, 299, 0.4)
        wnd.addChild(cmp, 'btnFrame')
        rows = []
        rows.append([(25, 'TOP'), {'action': {'props': soTableElemPropsStructure(dataStyles=self.keyTable_captionDS),
                     'data': {'text': lc('soOptionsGUI.soGUI.STRING_604_131')}},
          'key1': {'props': soTableElemPropsStructure(dataStyles=self.keyTable_captionDS),
                   'data': {'text': lc('soOptionsGUI.soGUI.STRING_605_108')}},
          'key2': {'props': soTableElemPropsStructure(dataStyles=self.keyTable_captionDS),
                   'data': {'text': lc('soOptionsGUI.soGUI.STRING_606_108')}}}])
        tbl = soTableComponent2(GUI.Window(), soTablePropsStructure(tableHeight=298, tableWidth=520, innerBorderColor=(85, 85, 85, 255)))
        cmp = tbl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (1, 1, 0.5)
        wnd.addChild(cmp, 'keyTable')
        tbl.onBound()
        tbl.addCols([['action', 220], ['key1', 150], ['key2', 134]])
        tbl.addRows(rows)
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soOptionsGUI.soGUI.STRING_636_19')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (3, 302, 0.3)
        wnd.addChild(cmp, 'defaultBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soOptionsGUI.soGUI.STRING_657_19')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (291, 302, 0.3)
        wnd.addChild(cmp, 'modBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soOptionsGUI.soGUI.STRING_678_19')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (406, 302, 0.3)
        wnd.addChild(cmp, 'clearBtn')
        btn.onBound()
        btn.setVisualState('normal')

    def setupMouse(self):
        wnd = GUI.Window()
        wnd.horizontalPositionMode = wnd.verticalPositionMode = 'PIXEL'
        wnd.widthMode = wnd.heightMode = 'PIXEL'
        wnd.horizontalAnchor = 'LEFT'
        wnd.verticalAnchor = 'TOP'
        wnd.materialFX = 'BLEND'
        wnd.colour = (255, 255, 255, 255)
        wnd.width = 521
        wnd.height = 334
        wnd.position = (4, 31, 0.2)
        wnd.visible = False
        self.component.addChild(wnd, 'wnd' + str(self.TAB_MOUSE))
        cmp = GUI.Frame2('soGUI/maps/Controls/window_frame/options_inner_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        wnd.addChild(cmp, 'innerFrame')
        slider = soSlider(GUI.Window(), width=401, height=16, steps=101, visualSteps=20)
        cmp = slider.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (23, 245, 0.1)
        slider.onBound()
        wnd.addChild(cmp, 'sens')
        slider.setLimits(0.0, 1.0)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_733_13')
        cmp.position = (23, 226, 0.6)
        wnd.addChild(cmp, 'sensLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = u'0.00'
        cmp.position = (23, 270, 0.6)
        wnd.addChild(cmp, 'minSens')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = u'1.00'
        cmp.position = (424, 270, 0.6)
        wnd.addChild(cmp, 'maxSens')
        edit = soEditField2(GUI.Window(), height=20, width=52)
        edit.onBound()
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (449, 238, 0.2)
        wnd.addChild(cmp, 'sensEdit')
        cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=lc('soOptionsGUI.soGUI.STRING_774_73')))
        cmp = cb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (26, 30, 0.4)
        wnd.addChild(cmp, 'mouseInvert')
        cb.onBound()
        cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=lc('soOptionsGUI.soGUI.STRING_785_73')))
        cmp = cb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (26, 55, 0.4)
        cmp.visible = False
        wnd.addChild(cmp, 'mouseFilter')
        cb.onBound()
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_804_13')
        cmp.position = (240, 39, 0.6)
        wnd.addChild(cmp, 'invertExplains')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (85, 85, 85, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_815_13')
        cmp.position = (240, 64, 0.6)
        cmp.visible = False
        wnd.addChild(cmp, 'filterExplains')

    def setupAudio(self):
        wnd = GUI.Window()
        wnd.horizontalPositionMode = wnd.verticalPositionMode = 'PIXEL'
        wnd.widthMode = wnd.heightMode = 'PIXEL'
        wnd.horizontalAnchor = 'LEFT'
        wnd.verticalAnchor = 'TOP'
        wnd.materialFX = 'BLEND'
        wnd.colour = (255, 255, 255, 255)
        wnd.width = 521
        wnd.height = 334
        wnd.position = (4, 31, 0.2)
        wnd.visible = False
        self.component.addChild(wnd, 'wnd' + str(self.TAB_AUDIO))
        cmp = GUI.Frame2('soGUI/maps/Controls/window_frame/options_inner_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        wnd.addChild(cmp, 'innerFrame')
        slider = soSlider(GUI.Window(), width=161, height=16, steps=101, visualSteps=20)
        cmp = slider.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (26, 88, 0.1)
        slider.onBound()
        wnd.addChild(cmp, 'musicVol')
        slider.setLimits(0.0, 100.0)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_864_13')
        cmp.position = (26, 73, 0.6)
        wnd.addChild(cmp, 'musicLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = u'0.00'
        cmp.position = (26, 117, 0.6)
        wnd.addChild(cmp, 'minMusic')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = u'100.00'
        cmp.position = (187, 117, 0.6)
        wnd.addChild(cmp, 'maxMusic')
        slider = soSlider(GUI.Window(), width=161, height=16, steps=101, visualSteps=20)
        cmp = slider.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (26, 207, 0.1)
        slider.onBound()
        wnd.addChild(cmp, 'sfxVol')
        slider.setLimits(0.0, 100.0)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_908_13')
        cmp.position = (26, 188, 0.6)
        wnd.addChild(cmp, 'sfxLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = u'0.00'
        cmp.position = (26, 233, 0.6)
        wnd.addChild(cmp, 'minSfx')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = u'100.00'
        cmp.position = (187, 233, 0.6)
        wnd.addChild(cmp, 'maxSfx')
        edit = soEditField2(GUI.Window(), height=20, width=60)
        edit.onBound()
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (207, 85, 0.2)
        wnd.addChild(cmp, 'musicEdit')
        edit = soEditField2(GUI.Window(), height=20, width=60)
        edit.onBound()
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (207, 200, 0.2)
        wnd.addChild(cmp, 'sfxEdit')
        ddl = soDropDownList2(GUI.Window(), width=211, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (297, 83, 0.1)
        cmp.visible = False
        wnd.addChild(cmp, 'quality')
        ddl.onBound()
        elems = [[self.SOUND_QUALITY_LOW, lc('soOptionsGUI.soGUI.STRING_971_29')], [self.SOUND_QUALITY_MED, lc('soOptionsGUI.soGUI.STRING_972_29')], [self.SOUND_QUALITY_HIGH, lc('soOptionsGUI.soGUI.STRING_973_30')]]
        ddl.addElements(elems)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_984_13')
        cmp.position = (297, 69, 0.6)
        cmp.visible = False
        wnd.addChild(cmp, 'audioQualityLabel')

    def setupVideo(self):
        wnd = GUI.Window()
        wnd.horizontalPositionMode = wnd.verticalPositionMode = 'PIXEL'
        wnd.widthMode = wnd.heightMode = 'PIXEL'
        wnd.horizontalAnchor = 'LEFT'
        wnd.verticalAnchor = 'TOP'
        wnd.materialFX = 'BLEND'
        wnd.colour = (255, 255, 255, 255)
        wnd.width = 521
        wnd.height = 334
        wnd.position = (4, 31, 0.2)
        wnd.visible = False
        self.component.addChild(wnd, 'wnd' + str(self.TAB_VIDEO))
        cmp = GUI.Frame2('soGUI/maps/Controls/window_frame/options_inner_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        wnd.addChild(cmp, 'innerFrame')
        ddl = soDropDownList2(GUI.Window(), width=211, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (294, 57, 0.1)
        wnd.addChild(cmp, 'resolution')
        ddl.onBound()
        ddl = soDropDownList2(GUI.Window(), width=211, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (294, 122, 0.1)
        wnd.addChild(cmp, 'quality')
        elems = [[self.VIDEO_QUALITY_CUSTOM, lc('soOptionsGUI.soGUI.STRING_369_26')],
         [self.VIDEO_QUALITY_LOW, lc('soOptionsGUI.soGUI.STRING_1038_29')],
         [self.VIDEO_QUALITY_NORMAL, lc('soOptionsGUI.soGUI.STRING_1039_32')],
         [self.VIDEO_QUALITY_HIGH, lc('soOptionsGUI.soGUI.STRING_1040_30')],
         [self.VIDEO_QUALITY_ULTRA, lc('soOptionsGUI.soGUI.STRING_1041_31')]]
        ddl.onBound()
        ddl.addElements(elems)
        ddl = soDropDownList2(GUI.Window(), width=211, height=24)
        cmp = ddl.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (294, 188, 0.1)
        wnd.addChild(cmp, 'screenMode')
        ddl.onBound()
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1068_13')
        cmp.position = (294, 42, 0.6)
        wnd.addChild(cmp, 'resolutionLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1080_13')
        cmp.position = (294, 108, 0.6)
        wnd.addChild(cmp, 'qualityLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1091_13')
        cmp.position = (294, 174, 0.6)
        wnd.addChild(cmp, 'screenModeLabel')
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soOptionsGUI.soGUI.STRING_509_20')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 120
        cmp.height = 29
        cmp.position = (395, 300, 0.5)
        wnd.addChild(cmp, 'addBtn')
        btn.onBound()
        btn.setVisualState('normal')
        slider = soSlider(GUI.Window(), width=161, height=25, steps=101, visualSteps=20)
        cmp = slider.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (26, 60, 0.1)
        cmp.visible = False
        slider.onBound()
        wnd.addChild(cmp, 'gamma')
        slider.setLimits(0.0, 1.0)
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1115_13')
        cmp.visible = False
        cmp.position = (26, 42, 0.6)
        wnd.addChild(cmp, 'gammaLabel')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = u'0.00'
        cmp.visible = False
        cmp.position = (26, 84, 0.6)
        wnd.addChild(cmp, 'minGamma')
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
        cmp.text = u'1.00'
        cmp.visible = False
        cmp.position = (187, 84, 0.6)
        wnd.addChild(cmp, 'maxGamma')
        edit = soEditField2(GUI.Window(), height=20, width=52)
        edit.onBound()
        cmp = edit.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.position = (207, 53, 0.2)
        cmp.visible = False
        wnd.addChild(cmp, 'gammaEdit')
        cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=lc('soOptionsGUI.soGUI.STRING_1159_73')))
        cmp = cb.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.position = (294, 263, 0.4)
        wnd.addChild(cmp, 'windowed')
        cb.onBound()

    def setupExpertVideo(self, data):
        if self.expertWnd is not None:
            if hasattr(BWPersonality.GUICore.generalLayer, 'expertVideoOptions'):
                BWPersonality.GUICore.generalLayer.delChild(self.expertWnd)
            self.expertWnd = None
        wnd = GUI.Window()
        wnd.horizontalPositionMode = wnd.verticalPositionMode = 'PIXEL'
        wnd.widthMode = wnd.heightMode = 'PIXEL'
        wnd.horizontalAnchor = 'LEFT'
        wnd.verticalAnchor = 'TOP'
        wnd.materialFX = 'BLEND'
        wnd.colour = (255, 255, 255, 255)
        wnd.width = 439
        wnd.height = 403
        wnd.position = (4, 31, 0.2)
        self.expertWnd = wnd
        cmp = GUI.Text('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.font = 'ruRU_Cyrvetica_Extra_16title.font'
        cmp.text = lc('soOptionsGUI.soGUI.STRING_1216_13')
        cmp.position = (10, 16, 0.2)
        wnd.addChild(cmp, 'wndCaption')
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
        cmp.position = (415, 6, 0.3)
        closeBox.initVSC('soGUI/visual_styles/closeBox.xml')
        closeBox.onBound()
        closeBox.setVisualState('normal')
        self.expertWnd.addChild(cmp, 'closeBox')
        closeBox.onClick = self._expertCancel
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = u'Ok'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (219, 370, 0.5)
        self.expertWnd.addChild(cmp, 'okBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn.onClick = self._expertOk
        btn = soButton(GUI.Window())
        cmp = btn.component
        btn.initVSC('soGUI/visual_styles/defaultBtn.xml')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.label.font = 'ruRU_calibri_default.font'
        cmp.label.text = lc('soOptionsGUI.soGUI.STRING_1269_19')
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 101
        cmp.height = 29
        cmp.position = (328, 370, 0.5)
        self.expertWnd.addChild(cmp, 'cancelBtn')
        btn.onBound()
        btn.setVisualState('normal')
        btn.onClick = self._expertCancel
        wnd = GUI.Window()
        wnd.horizontalPositionMode = wnd.verticalPositionMode = 'PIXEL'
        wnd.widthMode = wnd.heightMode = 'PIXEL'
        wnd.horizontalAnchor = 'LEFT'
        wnd.verticalAnchor = 'TOP'
        wnd.materialFX = 'BLEND'
        wnd.colour = (255, 255, 255, 255)
        wnd.width = 415
        wnd.height = 309
        wnd.position = (4, 43, 0.2)
        self.expertWnd.addChild(wnd, 'workArea')
        scroll = soScrollBar2(GUI.Window(), width=16, height=332)
        cmp = scroll.component
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.position = (418, 32, 0.6)
        self.expertWnd.addChild(cmp, 'vScroll')
        scroll.setVisualState('normal')
        scroll.onBound()
        scroll.setSteps(0)
        scroll.scrollUp = self.EVO_scrolledUP
        scroll.scrollDown = self.EVO_scrolledDOWN
        scroll.scrollMoved = self.EVO_vScrollMoved
        cmp = GUI.Frame2('soGUI/maps/Controls/inventory/inventoryFrame2.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 2.0
        cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.95)
        self.expertWnd.addChild(cmp, 'outerFrame')
        cmp = GUI.Frame2('soGUI/maps/Controls/window_frame/options_inner_frame.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'TOP'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 431
        cmp.height = 334
        cmp.position = (4, 31, 0.9)
        self.expertWnd.addChild(cmp, 'innerFrame')
        for i, control in enumerate(data):
            if control[0] is self.CONTROLTYPE_CHECKBOX:
                cb = soCheckBox(GUI.Window(), soGUI.CheckBoxPropsStructure(labelText=u''))
                cmp = cb.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.colour = (255, 255, 255, 255)
                cmp.materialFX = 'BLEND'
                cmp.position = (187, i * 25, 0.4)
                wnd.addChild(cmp, 'expertOption' + str(control[1]))
                cb.onBound()
                cb.onStateChange = partial(self.expertEvent, control[1], control[0])
            elif control[0] is self.CONTROLTYPE_COMBO:
                ddl = soDropDownList2(GUI.Window(), width=211, height=24)
                cmp = ddl.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.widthMode = cmp.heightMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.position = (187, i * 25, 0.4)
                wnd.addChild(cmp, 'expertOption' + str(control[1]))
                ddl.onBound()
                ddl.addElements(control[3])
                ddl.onSelectedElement = partial(self.expertEvent, control[1], control[0])
            elif control[0] is self.CONTROLTYPE_SLIDER:
                slider = soSlider(GUI.Window(), width=211, height=22, steps=101, visualSteps=20)
                cmp = slider.component
                cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
                cmp.horizontalAnchor = 'LEFT'
                cmp.verticalAnchor = 'TOP'
                cmp.position = (187, i * 25, 0.1)
                slider.onBound()
                wnd.addChild(cmp, 'expertOption' + str(control[1]))
                slider.setLimits(control[3][0], control[3][1])
                slider.onValueChanged__ = partial(self.expertEvent, control[1], control[0])
            cmp = GUI.Text('')
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.font = 'ruRU_Cyrvetica_Extra_12i.font'
            cmp.text = control[2]
            cmp.position = (18, 2 + i * 25, 0.6)
            wnd.addChild(cmp, 'expertOptionLabel' + str(control[1]))

        visCount = floor(self.expertWnd.workArea.height / 25.0)
        scrollCount = len(data) - visCount
        if scrollCount < 0:
            scrollCount = 0
        self.evoMaxScroll = scrollCount
        self.expertWnd.vScroll.script.setSteps(scrollCount)
        self.expertWnd.workArea.maxScroll = (0, 100.0)
        return

    def setupKeyBinder(self):
        wnd = GUI.Window()
        wnd.horizontalPositionMode = wnd.verticalPositionMode = 'CLIP'
        wnd.widthMode = wnd.heightMode = 'CLIP'
        wnd.horizontalAnchor = 'CENTER'
        wnd.verticalAnchor = 'CENTER'
        wnd.materialFX = 'BLEND'
        wnd.colour = (120, 120, 120, 125)
        wnd.width = 2.0
        wnd.height = 2.0
        wnd.position = (0.0, 0.0, 0.05)
        wnd.moveFocus = True
        wnd.crossFocus = True
        wnd.mouseButtonFocus = True
        self.keyBinder = wnd
        cmp = GUI.Simple('')
        cmp.textureName = 'soGUI/maps/Colours/white.tga'
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = 'CLIP'
        cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (0, 0, 0, 125)
        cmp.width = 2.0
        cmp.height = 100
        cmp.position = (0.0, 0.0, 0.95)
        self.keyBinder.addChild(cmp, 'innerFrame')

    def _shutdownTabWnd(self, tab):
        if tab == self.TAB_MOUSE:
            mWnd = getattr(self.component, 'wnd' + str(self.TAB_MOUSE))
            edit = mWnd.sensEdit.script
            if edit.isEditActive():
                edit.onReturn()
        if tab == self.TAB_AUDIO:
            aWnd = getattr(self.component, 'wnd' + str(self.TAB_AUDIO))
            if aWnd.musicEdit.script.isEditActive():
                aWnd.musicEdit.script.onReturn()
            if aWnd.sfxEdit.script.isEditActive():
                aWnd.sfxEdit.script.onReturn()
        if tab == self.TAB_VIDEO:
            vWnd = getattr(self.component, 'wnd' + str(self.TAB_VIDEO))
            if vWnd.gammaEdit.script.isEditActive():
                vWnd.gammaEdit.script.onReturn()

    def tabSelect(self, tab):
        for _tab in [self.TAB_KEYBOARD,
         self.TAB_MOUSE,
         self.TAB_AUDIO,
         self.TAB_VIDEO]:
            tabCmp = getattr(self.component, 'tab' + str(_tab))
            tabCmp.script.buttonActive = False if tab != _tab else True
            tabCmp.script._updateVisualState()
            wnd = self._getTabWnd(_tab)
            wnd.visible = False if tab != _tab else True
            if _tab != tab:
                self._shutdownTabWnd(_tab)

        self.currentTab = tab
        BWPersonality.GUICore.checkAllTopmostComponents()

    def _getTabWnd(self, tab):
        wnd = getattr(self.component, 'wnd' + str(tab))
        return wnd

    def setCustomPreset(self):
        vWnd = getattr(self.component, 'wnd' + str(self.TAB_VIDEO))
        vWnd.quality.script.setSelectionByValue(self.VIDEO_QUALITY_CUSTOM, silent=False)

    def showExperts(self, doShow = True):
        if not self.expertWnd:
            return
        if doShow:
            if not hasattr(BWPersonality.GUICore.generalLayer, 'expertVideoOptions'):
                BWPersonality.GUICore.generalLayer.addChild(self.expertWnd, 'expertVideoOptions')
        elif hasattr(BWPersonality.GUICore.generalLayer, 'expertVideoOptions'):
            BWPersonality.GUICore.generalLayer.delChild(self.expertWnd)

    def showKeyBinder(self, message = u'', doShow = True, action = None):
        self.keyBindAction = action
        if doShow:
            BWPersonality.GUICore.registerKeyHook(self._keyHook)
        else:
            BWPersonality.GUICore.registerKeyHook(None)
        return

    def _keyHook(self, event):
        if self.keyBindAction:
            if event.key == KEY_ESCAPE:
                self.showKeyBinder(doShow=False)
                return True
            if event.key in MODIFIER_CODES:
                return True
            keyCodes = (event.key,)
            if event.isShiftDown():
                keyCodes += (KEY_RSHIFT,)
            if event.isCtrlDown():
                keyCodes += (KEY_RCONTROL,)
            if event.isAltDown():
                keyCodes += (KEY_RALT,)
            BWPersonality.GUICore.optionsEvent(self.EVENT_OPTIONSET, ['keybinds',
             self.keyBindAction[0],
             self.keyBindAction[1],
             keyCodes])
        self.showKeyBinder(doShow=False)
        return True

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.generalLayer.addChild(self.component, 'options')
        self.component.visible = True
        BWPersonality.GUICore.setBestCursor()
        return

    def hide(self):
        self.component.visible = False
        BWPersonality.GUICore.setBestCursor()
        self.showExperts(False)
        BWPersonality.GUICore.updateTopmostObjects()

    def _updateKeys(self, data):
        keyWnd = getattr(self.component, 'wnd' + str(self.TAB_KEYBOARD))
        tbl = keyWnd.keyTable.script
        rows = []
        rows.append([(25, 'TOP'), {'action': {'props': soTableElemPropsStructure(dataStyles=self.keyTable_captionDS),
                     'data': {'text': lc('soOptionsGUI.soGUI.STRING_1532_131')}},
          'key1': {'props': soTableElemPropsStructure(dataStyles=self.keyTable_captionDS),
                   'data': {'text': lc('soOptionsGUI.soGUI.STRING_1533_108')}},
          'key2': {'props': soTableElemPropsStructure(dataStyles=self.keyTable_captionDS),
                   'data': {'text': lc('soOptionsGUI.soGUI.STRING_1534_108')}}}])
        for index, action in enumerate(data):
            dataDS = self.keyTable_dataDS
            if action[4]:
                dataDS = self.keyTable_dataDS2
            rows.append([(25, 'MIDDLE'), {'action': {'props': soTableElemPropsStructure(dataStyles=dataDS),
                         'data': {'text': action[3],
                                  'action_id': action[0]}},
              'key1': {'props': soTableElemPropsStructure(dataStyles=self.keyTable_dataDS, dataType=5),
                       'data': {'text': action[1],
                                'btnVS': 'soGUI/visual_styles/defaultBtnEmpty.xml'}},
              'key2': {'props': soTableElemPropsStructure(dataStyles=self.keyTable_dataDS, dataType=5),
                       'data': {'text': action[2],
                                'btnVS': 'soGUI/visual_styles/defaultBtnEmpty.xml'}}}])

        tbl.clearTable()
        tbl.addRows(rows)

    def _updateMouse(self, data):
        mWnd = getattr(self.component, 'wnd' + str(self.TAB_MOUSE))
        mWnd.sensEdit.script.setValue(str(data['sensivity']))
        mWnd.sens.script.setValue(data['sensivity'], False)
        if data['invert']:
            mWnd.mouseInvert.script.setActive()
        else:
            mWnd.mouseInvert.script.setInactive()
        if data['filter']:
            mWnd.mouseFilter.script.setActive()
        else:
            mWnd.mouseFilter.script.setInactive()

    def _updateAudio(self, data):
        aWnd = getattr(self.component, 'wnd' + str(self.TAB_AUDIO))
        aWnd.musicVol.script.setValue(data['music'], False)
        aWnd.sfxVol.script.setValue(data['sfx'], False)
        aWnd.musicEdit.script.setValue(str(data['music']))
        aWnd.sfxEdit.script.setValue(str(data['sfx']))
        aWnd.quality.script.setSelectionByValue(data['quality'], silent=True)

    def _updateVideo(self, data):
        vWnd = getattr(self.component, 'wnd' + str(self.TAB_VIDEO))
        vWnd.quality.script.setSelectionByText(self.VQ_LABELS[data['quality']], True, silent=True)
        vWnd.resolution.script.setSelectionByText(data['resolution'], True, silent=True)
        print '_updateVideo'
        vWnd.screenMode.script.setSelectionByText(data['screen_mode'], True, silent=True)
        if data['windowed']:
            vWnd.windowed.script.setActive()
        else:
            vWnd.windowed.script.setInactive()
        vWnd.gamma.script.setValue(data['gamma'], False)
        vWnd.gammaEdit.script.setValue(str(data['gamma']))

    def _updateExpert(self, data):
        for option in data:
            cmp = getattr(self.expertWnd.workArea, 'expertOption' + str(option))
            if isinstance(cmp.script, soCheckBox):
                if data[option]:
                    cmp.script.setActive()
                else:
                    cmp.script.setInactive()
            elif isinstance(cmp.script, soSlider):
                cmp.script.setValue(data[option], False)
            elif isinstance(cmp.script, soDropDownList2):
                cmp.script.setSelectionByText(data[option], silent=True)

    def _updateResolutions(self, data):
        wnd = getattr(self.component, 'wnd' + str(self.TAB_VIDEO))
        ddl = wnd.resolution.script
        ddl.clear()
        ddl.addElements(data)
        print '_updateResolutions'

    def _updateScreenModes(self, data):
        wnd = getattr(self.component, 'wnd' + str(self.TAB_VIDEO))
        ddl = wnd.screenMode.script
        ddl.clear()
        ddl.addElements(data)
        print '_updateScreenModes'

    def update(self):
        data = BWPersonality.GUICore.optionsDataSection
        if data.has_key('resolution_list'):
            self._updateResolutions(data['resolution_list'])
        if data.has_key('screen_modes'):
            self._updateScreenModes(data['screen_modes'])
        if data.has_key('expert_setup'):
            self.setupExpertVideo(data['expert_setup'])
        if data.has_key('keybinds'):
            self._updateKeys(data['keybinds'])
        if data.has_key('mouse'):
            self._updateMouse(data['mouse'])
        if data.has_key('audio'):
            self._updateAudio(data['audio'])
        if data.has_key('video'):
            self._updateVideo(data['video'])
        if data.has_key('expert_settings'):
            self._updateExpert(data['expert_settings'])

    def expertEvent(self, event, data, selection = None):
        if data is self.CONTROLTYPE_CHECKBOX:
            cbCmp = getattr(self.expertWnd.workArea, 'expertOption' + str(event))
            selOpt = cbCmp.script.isChecked()
            BWPersonality.GUICore.optionsEvent(self.EVENT_OPTIONSET, ['expert_settings', event, selOpt])
        elif data is self.CONTROLTYPE_COMBO:
            BWPersonality.GUICore.optionsEvent(self.EVENT_OPTIONSET, ['expert_settings', event, selection])
        elif data is self.CONTROLTYPE_SLIDER:
            sCmp = getattr(self.expertWnd.workArea, 'expertOption' + str(event))
            selOpt = sCmp.script.getValue()
            BWPersonality.GUICore.optionsEvent(self.EVENT_OPTIONSET, ['expert_settings', event, selOpt])

    def _sendEvent(self, event, data):
        BWPersonality.GUICore.optionsEvent(event, data)

    def _expertOk(self):
        self._sendEvent(self.EVENT_EXPERTOK, None)
        self.showExperts(False)
        return

    def _expertCancel(self):
        self._sendEvent(self.EVENT_EXPERTCANCEL, None)
        self.showExperts(False)
        return

    @PyGUIEvent('wnd' + str(TAB_KEYBOARD) + '.keyTable', 'onElementEvent')
    def onKeyTableElem(self, col, row, event, data):
        keyWnd = getattr(self.component, 'wnd' + str(self.TAB_KEYBOARD))
        tbl = keyWnd.keyTable.script
        if row == 0:
            return
        if event == 'RIGHTMOUSE':
            tbl.clearSelection()
            tbl.selectRow(row)
        elif event == 'LEFTMOUSE':
            tbl.clearSelection()
            tbl.selectRow(row)

    @PyGUIEvent('wnd' + str(TAB_KEYBOARD) + '.keyTable', 'onEditEvent')
    def onKeyTableEdit(self, col, row, event, data):
        keyWnd = getattr(self.component, 'wnd' + str(self.TAB_KEYBOARD))
        tbl = keyWnd.keyTable.script
        if row == 0:
            return
        if event == 'BUTTON':
            tbl.clearSelection()
            tbl.selectRow(row)

    @PyGUIEvent('wnd' + str(TAB_KEYBOARD) + '.defaultBtn', 'onClick', 0)
    @PyGUIEvent('wnd' + str(TAB_KEYBOARD) + '.modBtn', 'onClick', 1)
    @PyGUIEvent('wnd' + str(TAB_KEYBOARD) + '.clearBtn', 'onClick', 2)
    def onKeybindsBtns(self, btnN):
        keyWnd = getattr(self.component, 'wnd' + str(self.TAB_KEYBOARD))
        tbl = keyWnd.keyTable.script
        selection = tbl.getSelection()
        row = None
        if selection:
            row = tbl.getRowByIndex(selection[0][1])
        actionID = None
        caption = u''
        if row:
            actionID = row['action']['data']['action_id']
            caption = row['action']['data']['text']
        if btnN == 0:
            BWPersonality.GUICore.optionsEvent(self.EVENT_KEYBINDS_DEFAULT, None)
        elif btnN == 1:
            if actionID is not None:
                self.showKeyBinder(lc('soOptionsGUI.soGUI.STRING_1701_23') + caption + lc('soOptionsGUI.soGUI.STRING_1701_98'), True, [actionID, 'key1'])
        elif btnN:
            if actionID is not None:
                BWPersonality.GUICore.optionsEvent(self.EVENT_KEYBINDS_CLEAR, actionID)
        return

    @PyGUIEvent('wnd' + str(TAB_MOUSE) + '.sens', 'onValueChanged')
    def onMouseSensSlider(self, step, val):
        mWnd = getattr(self.component, 'wnd' + str(self.TAB_MOUSE))
        mWnd.sensEdit.script.setValue(str(val))
        BWPersonality.GUICore.optionsEvent(self.EVENT_OPTIONSET, ['mouse', 'sensivity', val])

    @PyGUIEvent('wnd' + str(TAB_MOUSE) + '.sensEdit', 'eventLostFocus')
    def onMouseSensEdit(self):
        mWnd = getattr(self.component, 'wnd' + str(self.TAB_MOUSE))
        val = mWnd.sensEdit.script.getValue()
        mWnd.sens.script.setValue(float(val), False)
        BWPersonality.GUICore.optionsEvent(self.EVENT_OPTIONSET, ['mouse', 'sensivity', float(val)])

    @PyGUIEvent('wnd' + str(TAB_MOUSE) + '.mouseInvert', 'onStateChange', 0)
    @PyGUIEvent('wnd' + str(TAB_MOUSE) + '.mouseFilter', 'onStateChange', 1)
    def onMouseCBs(self, cbN):
        mWnd = getattr(self.component, 'wnd' + str(self.TAB_MOUSE))
        if cbN == 0:
            BWPersonality.GUICore.optionsEvent(self.EVENT_OPTIONSET, ['mouse', 'invert', mWnd.mouseInvert.script.isChecked()])
        elif cbN == 1:
            BWPersonality.GUICore.optionsEvent(self.EVENT_OPTIONSET, ['mouse', 'filter', mWnd.mouseFilter.script.isChecked()])

    @PyGUIEvent('wnd' + str(TAB_AUDIO) + '.musicVol', 'onValueChanged', 0)
    @PyGUIEvent('wnd' + str(TAB_AUDIO) + '.sfxVol', 'onValueChanged', 1)
    def onAudioSliders(self, sliderN, step, val):
        aWnd = getattr(self.component, 'wnd' + str(self.TAB_AUDIO))
        if sliderN == 0:
            aWnd.musicEdit.script.setValue(str(val))
            self._sendEvent(self.EVENT_OPTIONSET, ['audio', 'music', val])
        elif sliderN == 1:
            aWnd.sfxEdit.script.setValue(str(val))
            self._sendEvent(self.EVENT_OPTIONSET, ['audio', 'sfx', val])

    @PyGUIEvent('wnd' + str(TAB_AUDIO) + '.musicEdit', 'eventLostFocus', 0)
    @PyGUIEvent('wnd' + str(TAB_AUDIO) + '.sfxEdit', 'eventLostFocus', 1)
    def onAudioEdits(self, editN):
        aWnd = getattr(self.component, 'wnd' + str(self.TAB_AUDIO))
        if editN == 0:
            val = aWnd.musicEdit.script.getValue()
            aWnd.musicVol.script.setValue(float(val), False)
            self._sendEvent(self.EVENT_OPTIONSET, ['audio', 'music', float(val)])
        elif editN == 1:
            val = aWnd.sfxEdit.script.getValue()
            aWnd.sfxVol.script.setValue(float(val), False)
            self._sendEvent(self.EVENT_OPTIONSET, ['audio', 'sfx', float(val)])

    @PyGUIEvent('wnd' + str(TAB_AUDIO) + '.quality', 'onSelectedElement')
    def onAudioQuality(self, qID):
        aWnd = getattr(self.component, 'wnd' + str(self.TAB_AUDIO))
        self._sendEvent(self.EVENT_OPTIONSET, ['audio', 'quality', qID])

    @PyGUIEvent('wnd' + str(TAB_VIDEO) + '.gamma', 'onValueChanged')
    def onGammaSlider(self, step, val):
        vWnd = getattr(self.component, 'wnd' + str(self.TAB_VIDEO))
        vWnd.gammaEdit.script.setValue(str(val))
        self._sendEvent(self.EVENT_OPTIONSET, ['video', 'gamma', val])

    @PyGUIEvent('wnd' + str(TAB_VIDEO) + '.gammaEdit', 'eventLostFocus')
    def onGammaEdit(self):
        vWnd = getattr(self.component, 'wnd' + str(self.TAB_VIDEO))
        val = vWnd.gammaEdit.script.getValue()
        vWnd.gamma.script.setValue(float(val), False)
        self._sendEvent(self.EVENT_OPTIONSET, ['video', 'gamma', float(val)])

    @PyGUIEvent('wnd' + str(TAB_VIDEO) + '.resolution', 'onSelectedElement', 0)
    @PyGUIEvent('wnd' + str(TAB_VIDEO) + '.quality', 'onSelectedElement', 1)
    @PyGUIEvent('wnd' + str(TAB_VIDEO) + '.screenMode', 'onSelectedElement', 2)
    def onVideoCombos(self, cbN, elemID):
        vWnd = getattr(self.component, 'wnd' + str(self.TAB_VIDEO))
        if cbN == 0:
            self._sendEvent(self.EVENT_OPTIONSET, ['video', 'resolution', elemID])
        elif cbN == 1:
            self._sendEvent(self.EVENT_OPTIONSET, ['video', 'quality', elemID])
        elif cbN == 2:
            self._sendEvent(self.EVENT_OPTIONSET, ['video', 'screen_mode', elemID])

    @PyGUIEvent('wnd' + str(TAB_VIDEO) + '.windowed', 'onStateChange')
    def onWindowedCB(self):
        vWnd = getattr(self.component, 'wnd' + str(self.TAB_VIDEO))
        state = vWnd.windowed.script.isChecked()
        self._sendEvent(self.EVENT_OPTIONSET, ['video', 'windowed', state])

    def onExpertBtnClick(self):
        self.showExperts(True)

    @PyGUIEvent('okBtn', 'onClick')
    def onMainOk(self):
        self._sendEvent(self.EVENT_OK, None)
        self.hide()
        return

    @PyGUIEvent('applyBtn', 'onClick')
    def onMainApply(self):
        self._sendEvent(self.EVENT_APPLY, None)
        return

    @PyGUIEvent('cancelBtn', 'onClick')
    def onMainCancel(self):
        self._sendEvent(self.EVENT_CANCEL, None)
        self.hide()
        return

    @PyGUIEvent('closeBox', 'onClick')
    def onCloseBox(self):
        self.hide()

    def EVO_srollHandler(self, event, data):
        sW, sH = BigWorld.screenSize()
        iRelH = 25 / sH * 2.0
        if event == 'UP':
            if self.evoScroll > 0:
                self.evoScroll -= 1
            else:
                self.evoScroll = 0
        elif event == 'DOWN':
            if self.evoScroll < self.evoMaxScroll:
                self.evoScroll += 1
            else:
                self.evoScroll = self.evoMaxScroll
        elif event == 'MOVE':
            self.evoScroll = data
            if self.evoScroll < 0:
                self.evoScroll = 0
            if self.evoScroll > self.evoMaxScroll:
                self.evoScroll = self.evoMaxScroll
        self.expertWnd.vScroll.script.setValue(self.evoScroll)
        self.expertWnd.workArea.scroll = (0, iRelH * self.evoScroll)

    def EVO_scrolledUP(self):
        self.EVO_srollHandler('UP', None)
        return

    def EVO_scrolledDOWN(self):
        self.EVO_srollHandler('DOWN', None)
        return

    def EVO_vScrollMoved(self, newVal):
        self.EVO_srollHandler('MOVE', newVal)

    @PyGUIEvent('wnd' + str(TAB_VIDEO) + '.addBtn', 'onClick')
    def onAddClick(self):
        add = TestWindow(GUI.Window())
        add.onBound()
        add.show()