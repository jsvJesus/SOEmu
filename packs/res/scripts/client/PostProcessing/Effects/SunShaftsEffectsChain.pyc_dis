# Embedded file name: scripts/client/PostProcessing/Effects/SunShaftsEffectsChain.py
import BigWorld
from PostProcessing.RenderTargets import *
from PostProcessing.Phases import *
from PostProcessing import Effect
from PostProcessing.Effects import implementEffectFactory

@implementEffectFactory('Blur1x', 'Store multiple levels of blur of the scene in intermediate textures. Must have SunShaftsMaskGen effect before!')
def Blur1x(filterMode = 0):
    """This method creates and returns an effect that DOES NOT down-samples and
    blurs the back-buffer."""
    bbcB = rt('backBufferCopyB')
    bbcC = rt('backBufferCopyC')
    bh1 = buildBlurPhase(bbcB.texture, bbcC, True, filterMode, 1.0)
    bv1 = buildBlurPhase(bbcC.texture, bbcB, False, filterMode, 1.0)
    e = Effect()
    e.name = 'Blur 1x'
    phases = [bh1, bv1]
    e.phases = phases
    return e


@implementEffectFactory('Blur2x', 'Store multiple levels of blur of the scene in intermediate textures. Must have SunShaftsMaskGen effect before!')
def Blur2x(filterMode = 0):
    """This method creates and returns an effect that DOES NOT down-samples and
    blurs the back-buffer."""
    bbcB = rt('backBufferCopyB')
    bbcC = rt('backBufferCopyC')
    bh1 = buildBlurPhase(bbcB.texture, bbcC, True, filterMode, 1.0)
    bv1 = buildBlurPhase(bbcC.texture, bbcB, False, filterMode, 1.0)
    bh2 = buildBlurPhase(bbcB.texture, bbcC, True, filterMode, 1.0)
    bv2 = buildBlurPhase(bbcC.texture, bbcB, False, filterMode, 1.0)
    e = Effect()
    e.name = 'Blur 2x'
    phases = [bh1,
     bv1,
     bh2,
     bv2]
    e.phases = phases
    return e


@implementEffectFactory('SunShaftsMaskGen', 'Generate source from which SunSunShafts will build off.')
def SunShaftsMaskGen():
    bbc = rt('backBufferCopy')
    bbcB = rt('backBufferCopyB')
    p1 = buildBackBufferCopyPhase(bbc)
    p2 = buildPhase(bbc, bbcB, 'shaders/post_processing/SunShaftsMaskGen.fx', straightTransfer4Tap, BW_BLEND_ONE, BW_BLEND_ZERO)
    p2.name = 'Generate SunShafts Mask'
    p2.material.inputTexture = bbc.texture
    e = Effect()
    e.name = 'Generate Mask'
    phases = [p1, p2]
    e.phases = phases
    return e


@implementEffectFactory('SunShaftsCombine', 'Generate SunShafts. Must have ShaftsMaskGen effect before!')
def SunShaftsCombine():
    bbc = rt('backBufferCopy')
    bbcB = rt('backBufferCopyB')
    bbcC = rt('backBufferCopyC')
    p1 = buildPhase(bbcB, bbcC, 'shaders/post_processing/radial_blur.fx', straightTransfer4Tap, BW_BLEND_ONE, BW_BLEND_ZERO)
    p1.name = 'Blur occlusion mask'
    p1.material.inputTexture = bbcB.texture
    p2 = buildPhase(bbc, None, 'shaders/post_processing/SunShaftsCombine.fx', straightTransfer4Tap, BW_BLEND_SRCALPHA, BW_BLEND_INVSRCALPHA)
    p2.name = 'Generate SunShafts'
    p2.material.inputTexture = bbcC.texture
    p2.material.ScreenTexture = bbc.texture
    e = Effect()
    e.name = 'Generate and display SunShafts'
    phases = [p1, p2]
    e.phases = phases
    return e