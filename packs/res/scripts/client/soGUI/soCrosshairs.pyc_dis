# Embedded file name: scripts/client/soGUI/soCrosshairs.py
import BigWorld
import BWPersonality
import GUI
import soGUI
from Helpers.PyGUI import PyGUIBase
from Math import Matrix

class soTargettingGUI(PyGUIBase):
    factoryString = 'soGUI.soTargettingGUI'
    INTERACTION_NONE = 0
    INTERACTION_CAN = 1
    INTERACTION_CANNOT = 2
    HEAP_NONE = 0
    HEAP_DEFAULT = 1
    SCOPELENS_NONE = 0
    SCOPELENS_DEFAULT = 1
    SCOPELENS_COLLIMATOR_1 = 2
    SCOPELENS_COLLIMATOR_2 = 3
    SCOPELENS_COLLIMATOR_3 = 4
    SCOPELENS_COLLIMATOR_4 = 5
    SCOPELENS_COLLIMATOR_5 = 6
    SCOPELENS_CROSS = 7
    SCOPELENS_DOT = 8
    SCOPELENS_PENEK = 9
    SCOPELENS_PO6 = 10
    SCOPELENS_PSO1 = 11
    SCOPETUBE_NONE = 0
    SCOPETUBE_DEFAULT = 1
    SCOPETUBE_COLLIMATOR_1 = 2
    SCOPETUBE_COLLIMATOR_2 = 3
    SCOPETUBE_ASSAULT = 4
    SCOPETUBE_SNIPER = 5
    SCOPEBLUR_NONE = 0
    SCOPEBLUR_DEFAULT = 1
    SCOPEBLUR_4X3 = 2
    SCOPEBLUR_5X4 = 3
    SCOPEBLUR_16X9 = 4
    SCOPEBLUR_16X10 = 5
    INTERACTION_TEXTURES = {INTERACTION_CAN: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/cursor_action-enable.tga'),
     INTERACTION_CANNOT: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/cursor_action-disable.tga')}
    HEAP_TEXTURES = {HEAP_DEFAULT: BigWorld.PyTextureProvider('soGUI/maps/Colours/white.tga')}
    SCOPELENS_TEXTURES = {SCOPELENS_DEFAULT: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/Snipe01.tga'),
     SCOPELENS_COLLIMATOR_1: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/scope_reticle_collimator_1.tga'),
     SCOPELENS_COLLIMATOR_2: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/scope_reticle_collimator_2.tga'),
     SCOPELENS_CROSS: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/scope_reticle_cross.tga'),
     SCOPELENS_DOT: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/scope_reticle_dot.tga'),
     SCOPELENS_PENEK: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/scope_reticle_penek.tga'),
     SCOPELENS_PO6: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/scope_reticle_po6.tga'),
     SCOPELENS_PSO1: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/scope_reticle_pso1.tga')}
    SCOPETUBE_TEXTURES = {SCOPETUBE_DEFAULT: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/scope_aim_sniper.tga'),
     SCOPETUBE_ASSAULT: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/scope_aim_assault.tga'),
     SCOPETUBE_COLLIMATOR_1: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/scope_aim_collimator_1.tga'),
     SCOPETUBE_COLLIMATOR_2: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/scope_aim_collimator_2.tga'),
     SCOPETUBE_SNIPER: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/scope_aim_sniper.tga')}
    SCOPEBLUR_TEXTURES = {SCOPEBLUR_DEFAULT: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/aim_masks/mask_16-10_1680-1050.tga'),
     SCOPEBLUR_4X3: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/aim_masks/mask_4-3_1400-1050.tga'),
     SCOPEBLUR_5X4: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/aim_masks/mask_5-4_1280-1024.tga'),
     SCOPEBLUR_16X9: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/aim_masks/mask_16-9_1920-1080.tga'),
     SCOPEBLUR_16X10: BigWorld.PyTextureProvider('soGUI/maps/Crosshairs/aim_masks/mask_16-10_1680-1050.tga')}

    def __init__(self, component):
        PyGUIBase.__init__(self, component)
        component.script = self
        self.inacuracy = 0.0
        self.setupRoot()
        self.setupContent()
        self._downSampleIfNotPresent()
        self._checkAspects()

    def setupRoot(self):
        cmp = self.component
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 1.6)
        cmp.visible = False

    def setupContent(self):
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 1
        cmp.height = 20
        cmp.position = (0.0, 0.0, 0.1)
        hUPMP = Matrix()
        hUPMP.translation = (0.0, 0.0, 0.0)
        shader = GUI.MatrixShader()
        shader.eta = 0
        shader.blend = True
        shader.target = hUPMP
        cmp.addShader(shader, 'mover')
        self.component.addChild(cmp, 'heapUP')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'LEFT'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 20
        cmp.height = 1
        cmp.position = (0.0, 0.0, 0.1)
        cmp.angle = 90
        rUPMP = Matrix()
        rUPMP.translation = (0.0, 0.0, 0.0)
        shader = GUI.MatrixShader()
        shader.eta = 0
        shader.blend = True
        shader.target = rUPMP
        cmp.addShader(shader, 'mover')
        self.component.addChild(cmp, 'heapRIGHT')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'TOP'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 1
        cmp.height = 20
        cmp.position = (0.0, 0.0, 0.1)
        cmp.angle = 180
        dUPMP = Matrix()
        dUPMP.translation = (0.0, 0.0, 0.0)
        shader = GUI.MatrixShader()
        shader.eta = 0
        shader.blend = True
        shader.target = dUPMP
        cmp.addShader(shader, 'mover')
        self.component.addChild(cmp, 'heapDOWN')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'RIGHT'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = 20
        cmp.height = 1
        cmp.position = (0.0, 0.0, 0.1)
        cmp.angle = 270
        lUPMP = Matrix()
        lUPMP.translation = (0.0, 0.0, 0.0)
        shader = GUI.MatrixShader()
        shader.eta = 0
        shader.blend = True
        shader.target = lUPMP
        cmp.addShader(shader, 'mover')
        self.component.addChild(cmp, 'heapLEFT')
        cmp = GUI.Simple('')
        cmp.widthMode = cmp.heightMode = 'PIXEL'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.width = cmp.height = 3
        cmp.position = (0.0, 0.0, 0.1)
        self.component.addChild(cmp, 'heapCENTER')
        self.component.heapCENTER.visible = True
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'BOTTOM'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.height = 2.0
        cmp.width = self._getWidthByHeight(cmp.height)
        cmp.position = (0.0, -1.0, 0.2)
        self.component.addChild(cmp, 'scopeTube')
        cmp = GUI.Simple('')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.materialFX = 'BLEND'
        cmp.colour = (255, 255, 255, 255)
        cmp.height = 1.39
        cmp.width = self._getWidthByHeight(cmp.height)
        cmp.position = (0.0, 0.0, 0.3)
        self.component.addChild(cmp, 'scopeLens')
        cmp = GUI.Gobo('soGUI/maps/Crosshairs/aim_masks/mask_16-10_1680-1050.tga')
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = cmp.height = 2.0
        cmp.position = (0.0, 0.0, 0.4)
        cmp.visible = False
        self.component.addChild(cmp, 'scopeBlur')

    def setInaccuracyArc(self, r, speed = 0.1):
        self.inacuracy = r
        fov = BigWorld.projection().fov
        iaR = 1.0 / (fov / r) if r else 0.0
        self.component.heapUP.mover.eta = speed
        self.component.heapUP.mover.target.translation = (0.0, iaR, 0.0)
        self.component.heapRIGHT.mover.eta = speed
        self.component.heapRIGHT.mover.target.translation = (self._getWidthByHeight(iaR), 0.0, 0.0)
        self.component.heapDOWN.mover.eta = speed
        self.component.heapDOWN.mover.target.translation = (0.0, -iaR, 0.0)
        self.component.heapLEFT.mover.eta = speed
        self.component.heapLEFT.mover.target.translation = (-self._getWidthByHeight(iaR), 0.0, 0.0)

    def show(self):
        if self.component.parent is None:
            BWPersonality.GUICore.worldLayer.addChild(self.component, 'targettingGUI')
        self.component.visible = True
        return

    def hide(self):
        self.component.visible = False

    def only_dot(self, on = False):
        if on:
            self.component.heapUP.visible = False
            self.component.heapRIGHT.visible = False
            self.component.heapDOWN.visible = False
            self.component.heapLEFT.visible = False
            self.component.heapCENTER.colour.alpha = 255
        if not on and self.component.heapCENTER.visible:
            self.component.heapUP.visible = True
            self.component.heapRIGHT.visible = True
            self.component.heapDOWN.visible = True
            self.component.heapLEFT.visible = True
            self.component.heapCENTER.colour.alpha = 100

    def _checkAspects(self):
        sW, sH = BigWorld.screenSize()
        aR = sW / sH
        maskAR = 16 / 10.0
        cut = (1 - 1 / (maskAR / aR)) / 2.0
        mapping = ((cut, 0.0),
         (cut, 1.0),
         (1.0 - cut, 1.0),
         (1.0 - cut, 0.0))
        self.component.scopeBlur.mapping = mapping

    def _updateHeapMode(self, data):
        if data == self.HEAP_NONE:
            self.component.heapUP.textureName = ''
            self.component.heapRIGHT.textureName = ''
            self.component.heapDOWN.textureName = ''
            self.component.heapLEFT.textureName = ''
            self.component.heapCENTER.textureName = ''
            return
        self.component.heapUP.texture = self.HEAP_TEXTURES[data]
        self.component.heapRIGHT.texture = self.HEAP_TEXTURES[data]
        self.component.heapDOWN.texture = self.HEAP_TEXTURES[data]
        self.component.heapLEFT.texture = self.HEAP_TEXTURES[data]
        self.component.heapCENTER.texture = self.HEAP_TEXTURES[data]

    def _updateBlur(self, data):
        import PostProcessing
        c = list(PostProcessing.chain())
        ch = []
        for e in c:
            if e.name != 'Sniper Scope Blur':
                ch.append(e)

        PostProcessing.chain(ch)
        self.component.scopeBlur.visible = False
        self.component.scopeBlur.secondaryTexture = None
        if data == self.SCOPEBLUR_NONE:
            return
        else:
            self.component.scopeBlur.texture = self.SCOPEBLUR_TEXTURES[data]
            effect = PostProcessing.blur()
            effect.name = 'Sniper Scope Blur'
            effect.phases[-1].renderTarget = BigWorld.RenderTarget('sniperBlur', -3, -3)
            effect.phases[-1].material.additionalAlpha = 1.0
            c = list(PostProcessing.chain())
            c.append(effect)
            PostProcessing.chain(c)
            self.effect = effect
            self.component.scopeBlur.secondaryTexture = effect.phases[-1].renderTarget.texture
            self.component.scopeBlur.freeze = None
            self.component.scopeBlur.visible = True
            return

    def _updateOOR(self, data):
        alpha = 255
        if data:
            alpha = 128
        self.component.heapUP.colour.alpha = alpha
        self.component.heapRIGHT.colour.alpha = alpha
        self.component.heapDOWN.colour.alpha = alpha
        self.component.heapLEFT.colour.alpha = alpha

    def recoverFromLoading(self):
        self._downSampleIfNotPresent()

    def _updateTube(self, data):
        self.component.scopeTube.textureName = ''
        if data == self.SCOPETUBE_NONE:
            return
        self.component.scopeTube.texture = self.SCOPETUBE_TEXTURES[data]

    def _updateLens(self, data):
        self.component.scopeLens.textureName = ''
        if data == self.SCOPELENS_NONE:
            return
        self.component.scopeLens.texture = self.SCOPELENS_TEXTURES[data]

    def update(self):
        data = BWPersonality.GUICore.crosshairsDataSection
        if data.has_key('heap_mode'):
            self._updateHeapMode(data['heap_mode'])
        if data.has_key('inaccuracy'):
            self.setInaccuracyArc(data['inaccuracy'][0], data['inaccuracy'][1])
        if data.has_key('scope_blur'):
            self._updateBlur(data['scope_blur'])
        if data.has_key('scope_tube'):
            self._updateTube(data['scope_tube'])
        if data.has_key('scope_lens'):
            self._updateLens(data['scope_lens'])
        if data.has_key('out_of_range'):
            self._updateOOR(data['out_of_range'])

    def _getWidthByHeight(self, h):
        sW, sH = BigWorld.screenSize()
        ar = sW / sH
        return h / ar

    def _downSampleIfNotPresent(self):
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

    def doReposition(self):
        self._checkAspects()
        self.component.scopeTube.width = self._getWidthByHeight(self.component.scopeTube.height)
        self.component.scopeLens.width = self._getWidthByHeight(self.component.scopeLens.height)

    def fini(self):
        soTargettingGUI.INTERACTION_TEXTURES = None
        soTargettingGUI.HEAP_TEXTURES = None
        soTargettingGUI.SCOPELENS_TEXTURES = None
        soTargettingGUI.SCOPETUBE_TEXTURES = None
        soTargettingGUI.SCOPEBLUR_TEXTURES = None
        return