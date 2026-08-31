# Embedded file name: scripts/client/soGUI/PVPmarker.py
import BWPersonality
import BigWorld
import soGUI.ScaleformDemo
import GUI
import traceback

class PVPmarker(object):
    """docstring for ClassName"""
    TIMEUPDATE = 0.015
    MARKERHEIGHT = 0.3
    CAM_FAR_PLANE = 0.3
    COLLIDE = False
    DEBUGPRNT = False
    scale = 100

    def __init__(self):
        path = 'scaleformUI/testHud.swf'
        self.fClip = soGUI.ScaleformDemo.ScaleformDemo.create(path, 0.0)
        self.pvpmarks = {}
        cmp = self.fClip
        cmp.horizontalPositionMode = cmp.verticalPositionMode = 'CLIP'
        cmp.widthMode = cmp.heightMode = 'CLIP'
        cmp.horizontalAnchor = 'CENTER'
        cmp.verticalAnchor = 'CENTER'
        cmp.colour = (255, 255, 255, 255)
        cmp.materialFX = 'BLEND'
        cmp.width = 2
        cmp.height = 2
        cmp.dragFocus = False
        cmp.crossFocus = False
        cmp.moveFocus = False
        cmp.focus = 0
        cmp.mouseButtonFocus = 0
        cmp.position = (0, 0, 0.2)
        GUI.reSort()
        self.tmpShader = GUI.MatrixShader()
        self.callbackID = 0
        BWPersonality.GUICore.generalLayer.addChild(self.fClip, 'PVPmarker')

    def update(self):
        self.callbackID = 0
        try:
            self._update()
            self.callbackID = BigWorld.callback(self.TIMEUPDATE, self.update)
        except:
            traceback.print_exc()
            self.hide()

    def getSacle(self, campos, pos3d):
        scale = 1000 / campos.distTo(pos3d)
        scale = max(scale, 30)
        scale = min(scale, 100)
        return scale

    def _update(self):
        p = BigWorld.player()
        campos = BigWorld.camera().position + BigWorld.camera().direction * self.CAM_FAR_PLANE
        pos2d = None
        w, h = BigWorld.screenSize()
        xf = w / (h / 500.0) / 2
        for eid, head in self.pvpmarks.iteritems():
            pos3d = head.position
            col = False
            if self.COLLIDE:
                col = BigWorld.collide(p.spaceID, campos, pos3d)
            if self.COLLIDE and col:
                self.fClip.script.viewX.invoke(('moveMarker',
                 eid,
                 -5000,
                 -5000,
                 0,
                 100))
                if self.DEBUGPRNT:
                    print 'marker hide', eid
            else:
                pos2d = self.tmpShader.calcWorldToScreen(pos3d + (0, self.MARKERHEIGHT, 0))
                self.fClip.script.viewX.invoke(('moveMarker',
                 eid,
                 pos2d.x * xf,
                 -pos2d.y * 250,
                 1,
                 self.getSacle(campos, pos3d)))
                if self.DEBUGPRNT:
                    print 'marker', eid, pos3d, pos2d.x * xf, -pos2d.y * 250

        return

    def show(self):
        if self.callbackID:
            BigWorld.cancelCallback(self.callbackID)
        self.fClip.visible = True
        self.update()

    def hide(self):
        if self.callbackID:
            BigWorld.cancelCallback(self.callbackID)
        self.fClip.visible = False
        print 'hide PVPmarker'

    def addMarker(self, userID, matrix):
        if not matrix:
            return
        self.pvpmarks[userID] = matrix
        self.fClip.script.viewX.invoke(('addMarker', userID))

    def updateMatrixMarker(self, userID, matrix):
        if not matrix:
            self.delMarker(userID)
            return
        self.pvpmarks[userID] = matrix

    def delMarker(self, userID):
        if userID in self.pvpmarks:
            del self.pvpmarks[userID]
        self.fClip.script.viewX.invoke(('delMarker', userID))

    def clearAll(self):
        self.pvpmarks = {}
        self.fClip.script.viewX.invoke(('delAllMarker',))