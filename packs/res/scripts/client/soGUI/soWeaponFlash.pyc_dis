# Embedded file name: scripts/client/soGUI/soWeaponFlash.py
import BigWorld
import BWPersonality
import GUI
import Helpers.PyGUI as PyGUI
import soGUI
from Items import ItemsCatalog
import ItemsUtils

class soWeaponFlash(PyGUI.PyGUIBase):
    factoryString = 'soGUI.soWeaponFlash'

    def __init__(self, component):
        PyGUI.PyGUIBase.__init__(self, component)
        component.script = self
        self.setupRoot()
        self.setupFader()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.width = 128
        cmp.height = 64
        cmp.position = (0.0, -0.5, 0.0)
        cmp.textureName = ''
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'

    def setupFader(self):
        self.fader = GUI.AlphaShader()
        self.fader.speed = 0.5
        self.alpha = 0.0
        self.mode = 'ALL'
        self.fader.reset()
        self.component.addShader(self.fader, 'fader')

    def show(self):
        if self.parent is None:
            if hasattr(BigWorld.player(), 'playerGUI'):
                BigWorld.player().playerGUI.addChild(self.component)
                self.component.visible = True
        return

    def update(self):
        item = BWPersonality.GUICore.currentWeaponDataSection
        if item is None:
            return
        else:
            item_type = item['complexItemType']
            item_id = item['complexItemID']
            item_class = ItemsCatalog.GetItemClass(item_type)
            item_params = ItemsCatalog.GetItemParam(item_type)
            item_level = item_params['Level']
            self.component.textureName = ItemsCatalog.GetItemParam(item_type)['IconName']
            self.component.fader.alpha = 1.0
            self.component.fader.reset()
            self.component.fader.alpha = 0.0
            return