# Embedded file name: scripts/client/SingleEntityTimedLight.py
import BigWorld
from Math import Vector3

class SingleEntityTimedLight:

    def createLight(self, attachTo = None, colour = (255, 255, 255, 0), timeCheck = True):
        self.light = BigWorld.PyChunkLight()
        self.light.diffuse = 1
        self.light.specular = 0
        self.light.innerRadius = 3
        self.light.outerRadius = 5
        self.light.position = self.position + (0, 1.0, 0)
        if attachTo != None:
            self.light.source = attachTo
        self.light.colour = colour
        self.light.specular = 0
        self.light.diffuse = 1
        self.light.visible = True
        if timeCheck:
            self.checkLightByTimeOfDay()
        return self.light

    def checkLightByTimeOfDay(self):
        if hasattr(self, 'isDestroyed'):
            if self.isDestroyed:
                return
        spaceTime = BigWorld.spaceTimeOfDay(self.spaceID)
        hours = int(spaceTime.split(':')[0])
        minutes = int(spaceTime.split(':')[1])
        if hours > 18 or hours < 8:
            lightEnabled = True
        else:
            lightEnabled = False
        self.light.visible = lightEnabled
        vc = Vector3()
        vc.setPitchYaw(self.pitch, self.yaw)
        xpos = self.position + vc + (0, 1.5, 0)
        if xpos.distSqrTo(self.light.position) > 0.1:
            self.light.position = xpos
        self.lightCallback = BigWorld.callback(0.1, self.checkLightByTimeOfDay)