# Embedded file name: scripts/client/PostProcessing/Effects/SSAOChain.py
import BigWorld
from PostProcessing.RenderTargets import *
from PostProcessing.Phases import *
from PostProcessing import Effect
from PostProcessing.Effects import implementEffectFactory

@implementEffectFactory('SSAO Low Quality', 'Compute screen space ambient occlusion low quality.')
def SSAO_LQ():
    bbc = rt('backBufferCopy')
    bbcB = rt('backBufferCopyB')
    fpBuff = rt('R16F')
    p1 = buildBackBufferCopyPhase(bbc)
    p2 = Phase()
    p2.filterQuad = TransferQuad()
    p2.material = Material('shaders/post_processing/ssao_linear_depth.fx')
    p2.material.srcBlend = BW_BLEND_ONE
    p2.material.destBlend = BW_BLEND_ZERO
    p2.renderTarget = fpBuff
    p2.clearRenderTarget = False
    p2.name = 'Prepare linear depth map'
    p3 = Phase()
    p3.filterQuad = TransferQuad()
    p3.material = Material('shaders/post_processing/ssaovo_q1.fx')
    p3.material.sceneDepthTex = fpBuff.texture
    p3.material.srcBlend = BW_BLEND_ONE
    p3.material.destBlend = BW_BLEND_ZERO
    p3.renderTarget = bbcB
    p3.clearRenderTarget = False
    p3.name = 'Compute SSAO'
    e = Effect()
    e.name = 'SSAO Volumetric Obscurance'
    phases = [p1, p2, p3]
    e.phases = phases
    return e


@implementEffectFactory('SSAO Medium Quality', 'Compute screen space ambient occlusion.')
def SSAO_MQ():
    bbc = rt('backBufferCopy')
    bbcB = rt('backBufferCopyB')
    fpBuff = rt('R16F')
    p1 = buildBackBufferCopyPhase(bbc)
    p2 = Phase()
    p2.filterQuad = TransferQuad()
    p2.material = Material('shaders/post_processing/ssao_linear_depth.fx')
    p2.material.srcBlend = BW_BLEND_ONE
    p2.material.destBlend = BW_BLEND_ZERO
    p2.renderTarget = fpBuff
    p2.clearRenderTarget = False
    p2.name = 'Prepare linear depth map'
    p3 = Phase()
    p3.filterQuad = TransferQuad()
    p3.material = Material('shaders/post_processing/ssaovo_q2.fx')
    p3.material.sceneDepthTex = fpBuff.texture
    p3.material.srcBlend = BW_BLEND_ONE
    p3.material.destBlend = BW_BLEND_ZERO
    p3.renderTarget = bbcB
    p3.clearRenderTarget = False
    p3.name = 'Compute SSAO'
    e = Effect()
    e.name = 'SSAO Volumetric Obscurance'
    phases = [p1, p2, p3]
    e.phases = phases
    return e


@implementEffectFactory('SSAO High Quality', 'Compute screen space ambient occlusion.')
def SSAO_HQ():
    bbc = rt('backBufferCopy')
    bbcB = rt('backBufferCopyB')
    fpBuff = rt('R16F')
    p1 = buildBackBufferCopyPhase(bbc)
    p2 = Phase()
    p2.filterQuad = TransferQuad()
    p2.material = Material('shaders/post_processing/ssao_linear_depth.fx')
    p2.material.srcBlend = BW_BLEND_ONE
    p2.material.destBlend = BW_BLEND_ZERO
    p2.renderTarget = fpBuff
    p2.clearRenderTarget = False
    p2.name = 'Prepare linear depth map'
    p3 = Phase()
    p3.filterQuad = TransferQuad()
    p3.material = Material('shaders/post_processing/ssaovo_q3.fx')
    p3.material.sceneDepthTex = fpBuff.texture
    p3.material.srcBlend = BW_BLEND_ONE
    p3.material.destBlend = BW_BLEND_ZERO
    p3.renderTarget = bbcB
    p3.clearRenderTarget = False
    p3.name = 'Compute SSAO'
    e = Effect()
    e.name = 'SSAO Volumetric Obscurance'
    phases = [p1, p2, p3]
    e.phases = phases
    return e


@implementEffectFactory('SSAO Very High Quality', 'Compute screen space ambient occlusion.')
def SSAO_VHQ():
    bbc = rt('backBufferCopy')
    bbcB = rt('backBufferCopyB')
    fpBuff = rt('R16F')
    p1 = buildBackBufferCopyPhase(bbc)
    p2 = Phase()
    p2.filterQuad = TransferQuad()
    p2.material = Material('shaders/post_processing/ssao_linear_depth.fx')
    p2.material.srcBlend = BW_BLEND_ONE
    p2.material.destBlend = BW_BLEND_ZERO
    p2.renderTarget = fpBuff
    p2.clearRenderTarget = False
    p2.name = 'Prepare linear depth map'
    p3 = Phase()
    p3.filterQuad = TransferQuad()
    p3.material = Material('shaders/post_processing/ssaovo_q4.fx')
    p3.material.sceneDepthTex = fpBuff.texture
    p3.material.srcBlend = BW_BLEND_ONE
    p3.material.destBlend = BW_BLEND_ZERO
    p3.renderTarget = bbcB
    p3.clearRenderTarget = False
    p3.name = 'Compute SSAO'
    e = Effect()
    e.name = 'SSAO Volumetric Obscurance'
    phases = [p1, p2, p3]
    e.phases = phases
    return e


buildTransferPhase

@implementEffectFactory('SSAO display', 'Display SSAO. Must have SSAO effect before!')
def SSAOCombine():
    bbc = rt('backBufferCopy')
    bbcB = rt('backBufferCopyB')
    p1 = buildPhase(bbcB, None, 'shaders/post_processing/ssao_comb.fx', straightTransfer4Tap, BW_BLEND_ONE, BW_BLEND_ZERO)
    p1.name = 'SSAO combine'
    p1.material.inputTexture = bbcB.texture
    p1.material.ScreenTexture = bbc.texture
    e = Effect()
    e.name = 'Display SSAO'
    phases = [p1]
    e.phases = phases
    return e


@implementEffectFactory('SSAO Test out', 'Display raw SSAO effect. Must have SSAO effect before!')
def SSAORaw():
    bbc = rt('backBufferCopy')
    bbcB = rt('backBufferCopyB')
    p1 = buildTransferPhase(bbcB)
    p1.name = 'SSAO Raw'
    p1.material.inputTexture = bbcB.texture
    e = Effect()
    e.name = 'Display raw SSAO'
    phases = [p1]
    e.phases = phases
    return e