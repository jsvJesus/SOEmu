# Embedded file name: scripts/client/soGUI/soSystemMenu.py
import BigWorld
import GUI
import BWPersonality
import soGUI
import Helpers.PyGUI as PyGUI
from soGUI.soButton import soButton
from soGUI.soButton import soButtonWTT
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.PyGUI import PyGUIEvent
from functools import partial

class soSystemMenu(PyGUIBase):
    factoryString = 'soGUI.soSystemMenu'
    BTN_QUESTLOG, BTN_MAP, BTN_CLAN, BTN_SOCIAL, BTN_PEDIA, BTN_INVENTORY, BTN_EQUIPMENT, BTN_REPUTATION, BTN_PVP, BTN_SKILLS, BTN_PRIVATESTORE, BTN_CRAFT, BTN_MODIFICATION, BTN_MAINMENU = ALL_BTNS = xrange(14)
    DISABLED = [BTN_SOCIAL,
     BTN_PEDIA,
     BTN_MODIFICATION,
     BTN_PRIVATESTORE]

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupBtns()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 228
        cmp.height = 19
        if hasattr(BWPersonality.GUICore.worldLayer, 'minimap'):
            pos = BWPersonality.GUICore.worldLayer.minimap.position
            cmp.position = (pos.x - 115, pos.y + 229, 0.5)
        BWPersonality.GUICore.worldLayer.addChild(cmp, 'systemBar')
        cmp = GUI.Frame2('soGUI/maps/Controls/systemMenu/frame_fon.dds')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.9)
        self.component.addChild(cmp, 'backFrame')

    def setupBtns(self):

        def _makeVS(name_str):
            return 'soGUI/visual_styles/{0}.xml'.format(name_str)

        VSs = ['fastPanelJurnalBtn',
         'fastPanelMapBtn',
         'fastPanelGroupBtn',
         'fastPanelSocialBtn',
         'fastPanelEncyclopediaBtn',
         'fastPanelInventorylBtn',
         'fastPanelEquipmentBtn',
         'fastPanelFractionBtn',
         'fastPanelPvpBtn',
         'fastPanelSkillsBtn',
         'fastPanelTradeBtn',
         'fastPanelCraftBtn',
         'fastPanelModificBtn',
         'fastPanelMainMenuBtn']
        for btn_index in self.ALL_BTNS:
            btn = soButtonWTT(GUI.Window(), 'system_bar_{0}'.format(btn_index))
            btn.initVSC(_makeVS(VSs[btn_index]))
            btn.onClick = partial(self.onBtn, btn_index)
            if btn_index in self.DISABLED:
                btn.buttonDisabled = True
            cmp = btn.component
            cmp.horizontalPositionMode = cmp.verticalPositionMode = 'PIXEL'
            cmp.widthMode = cmp.heightMode = 'PIXEL'
            cmp.horizontalAnchor = 'LEFT'
            cmp.verticalAnchor = 'TOP'
            cmp.colour = (255, 255, 255, 255)
            cmp.materialFX = 'BLEND'
            cmp.width = 16
            cmp.height = 16
            cmp.position = (2 + 16 * btn_index, 1, 0.2)
            self.component.addChild(cmp, 'btn_{0}'.format(btn_index))
            btn.onBound()
            btn._updateVisualState()

    def refreshPoints(self):
        if BWPersonality.GUICore.skillsDataSection['Combat'][3] or BWPersonality.GUICore.skillsDataSection['Survival'][3] or BWPersonality.GUICore.skillsDataSection['Other'][3]:
            self.component.btn_9.colour = (120, 255, 255, 255)
        else:
            self.component.btn_9.colour = (255, 255, 255, 255)

    def doReposition(self):
        if hasattr(BWPersonality.GUICore.worldLayer, 'minimap'):
            pos = BWPersonality.GUICore.worldLayer.minimap.position
            height = BWPersonality.GUICore.worldLayer.minimap.height
            self.component.position = (pos.x - 115, pos.y + height, 0.5)

    def onBtn(self, btn):
        if btn == self.BTN_QUESTLOG:
            BWPersonality.GUICore.toggleQuestLog()
        elif btn == self.BTN_MAP:
            BWPersonality.GUICore.toggleMap()
        elif btn == self.BTN_EQUIPMENT:
            BWPersonality.GUICore.toggleCharScreen()
        elif btn == self.BTN_INVENTORY:
            BWPersonality.GUICore.toggleInventory()
        elif btn == self.BTN_MAINMENU:
            BWPersonality.GUICore.showIngameMenu(True)
        elif btn == self.BTN_CRAFT:
            BWPersonality.GUICore.toggleCraft()
        elif btn == self.BTN_PVP:
            BWPersonality.GUICore.toggleCharScreen()
            BWPersonality.GUICore.charScreen._switchToTab(2)
        elif btn == self.BTN_REPUTATION:
            BWPersonality.GUICore.toggleCharScreen()
            BWPersonality.GUICore.charScreen._switchToTab(1)
        elif btn == self.BTN_SKILLS:
            BWPersonality.GUICore.toggleSkillGUI()
        elif btn == self.BTN_CLAN:
            BWPersonality.GUICore.toggleClanGUI()