# Embedded file name: scripts/client/soGUI/data/RenderFeed.py
import BigWorld
import CameraNode
import Math
import math
from Helpers.BWCoroutine import *

class PaperDollFeed(object):

    def __init__(self, models, spaceName, width, height, callBack):
        self.paperSpaceName = spaceName
        self.paperSpaceReady = False
        self.paperSpaceCam = None
        self.paperSpaceID = 0
        self.paperDollPosition = None
        self.paperDoll = None
        self.textureProvider = None
        self.width = width
        self.height = height
        self.callBack = callBack
        self.buildPaperSpace().run()
        return

    @BWMemberCoroutine
    def buildPaperSpace(self):
        self.paperSpaceID = BigWorld.createSpace()
        BigWorld.addSpaceGeometryMapping(self.paperSpaceID, None, self.paperSpaceName)
        if not isinstance(self.paperSpaceCam, BigWorld.FreeCamera):
            self.paperSpaceCam = BigWorld.FreeCamera()
        self.paperSpaceCam.fixed = True
        m = Math.Matrix()
        m.setRotateYPR((0, 0, 0))
        m.translation = (50, 2, 50)
        m.invert()
        self.paperSpaceCam.set(m)
        self.paperSpaceCam.spaceID = self.paperSpaceID
        cameraNodes = []
        paperSpaceCameraList = []
        yield BWWaitForPeriod(0.1)
        loadStatus = 0.0
        self.paperSpaceReady = True
        self.setupTextureProvider()
        self.setupPaperDoll()
        return

    @BWMemberCoroutine
    def destroyPaperSpace(self):
        if self.paperSpaceID != None and not self.paperSpaceReady:
            yield BWWaitForCondition(lambda : self.paperSpaceReady)
        self.paperSpaceReady = False
        if self.paperSpaceCam == BigWorld.camera():
            BigWorld.camera(None)
        self.paperSpaceCam = None
        if self.paperSpaceID != None:
            BigWorld.clearSpace(self.paperSpaceID)
            BigWorld.releaseSpace(self.paperSpaceID)
            self.paperSpaceID = None
        return

    def setupPaperDoll(self):
        pass

    def fini(self):
        self.destroyPaperSpace().run()
        self.textureProvider = None
        return

    def setupTextureProvider(self):
        psr = BigWorld.PySceneRenderer(self.width, self.height)
        psr.cameras = [BigWorld.camera()]
        psr.dynamic = True
        self.textureProvider = psr
        self.textureProvider.render()
        self.callBack(self.textureProvider)