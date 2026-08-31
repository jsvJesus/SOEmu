# Embedded file name: scripts/client/soGUI/soVisionModes.py
import BigWorld
import GUI
import soGUI
import Helpers.PyGUI as PyGUI
import BWPersonality
from Helpers.PyGUI.PyGUIBase import PyGUIBase
from Helpers.BWCoroutine import *
MODE_NORMAL = 0
MODE_SNIPER = 1

class soSniperVision(PyGUIBase):
    factoryString = 'soGUI.soSniperVision'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.effect = None
        self.setupRoot()
        self.setupContent()
        return

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 2.0)
        cmp.textureName = ''

    def setupContent(self):
        cmp = GUI.Gobo('soGUI/maps/Crosshairs/aim_masks/mask_4-3_1400-1050.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.1)
        self.component.addChild(cmp, 'gobo')

    def sniperBlur(self):
        self.downSampleIfNotPresent()
        import PostProcessing
        effect = PostProcessing.blur()
        effect.name = 'Sniper Scope Blur'
        effect.phases[-1].renderTarget = BigWorld.RenderTarget('sniperBlur', -3, -3)
        effect.phases[-1].material.additionalAlpha = 1.0
        c = list(PostProcessing.chain())
        c.append(effect)
        PostProcessing.chain(c)
        self.effect = effect
        self.component.gobo.secondaryTexture = effect.phases[-1].renderTarget.texture
        self.component.gobo.freeze = None
        return

    def downSampleIfNotPresent(self):
        import PostProcessing
        eC = PostProcessing.chain()
        doDS = True
        for effect in eC:
            if effect.name == 'Down Sample':
                doDS = False

        if doDS:
            dsE = PostProcessing.downSample()
            eC.append(dsE)
            PostProcessing.chain(eC)

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.generalLayer.addChild(self.component, 'sniperScopeVision')
        self.component.visible = True
        self.sniperBlur()
        return

    def hide(self):
        import PostProcessing
        self.component.visible = False
        c = list(PostProcessing.chain())
        ch = []
        for e in c:
            if e.name != 'Sniper Scope Blur':
                ch.append(e)

        PostProcessing.chain(ch)

    def setScope(self, scope):
        pass


class soBinocularsVision(PyGUIBase):
    factoryString = 'soGUI.soBinocularsVision'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self