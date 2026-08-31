# Embedded file name: scripts/client/UnstableScope.py
import BigWorld
import Math
import math
import random
from sounds import playSound
import copy

class UnstableScope:
    ADD_X, SUB_X, ADD_Y, SUB_Y = xrange(4)
    DEFAULT_SHIFT = 0.0005
    min_speed = 5e-05
    max_shift = 0.01
    TIMER_PERIOD = 0.02
    heart_mode = False
    fire_rocoiling = False
    soundHeart = None
    numShotsCounter = 0
    maxRecoilValue = 0.0

    def GetRecoilKoeff(self):
        if self.numShotsCounter == 0:
            return 1.0
        if self.numShotsCounter == 1:
            return 0.5
        return 0.25

    def SetMaxShift(self, angle):

        def GetLengthFromPointToLine(direction_vector, point, point_start_measure):
            A_member = 1 / direction_vector[0]
            B_member = -1 / direction_vector[1]
            C_member = -point[0] / direction_vector[0] + point[1] / direction_vector[1]
            length_to_line = abs((A_member * point_start_measure[0] + B_member * point_start_measure[1] + C_member) / math.sqrt(A_member * A_member + B_member * B_member))
            return length_to_line

        self.max_shift = abs(angle / 2.0)
        if GetLengthFromPointToLine(self.scopeVelocity, self.currentShift, [0.0, 0.0]) >= self.max_shift:
            self.SetReturnPoint()
        if not self.heart_mode:
            self.min_speed = self.max_shift / 50.0

    def StartHeartMode(self):
        self.heart_mode = True
        self.min_speed = self.max_shift / 700.0
        self.soundHeart = playSound('players/heartbeat/slow', BigWorld.player().model)

    def EndHeartMode(self):
        self.heart_mode = False
        if self.soundHeart:
            self.soundHeart.stop()

    def GetAngleByShift(self, shift_vector):
        current_shift_vector_norm = copy.copy(shift_vector)
        current_shift_vector_norm.normalise()
        angle = math.asin(current_shift_vector_norm[1])
        if current_shift_vector_norm[1] > 0:
            if current_shift_vector_norm[0] > 0:
                angle = angle
            else:
                angle = math.pi - angle
        elif current_shift_vector_norm[0] > 0:
            angle = math.pi * 2 + angle
        else:
            angle = math.pi - angle
        return angle

    def UpdateInaccuracyProvider(self):
        player_camera = BigWorld.camera()
        flat_camera_direction = Math.Vector2(player_camera.direction[0], player_camera.direction[2])
        flat_camera_direction.normalise()
        inaccuracy = Math.Vector4(self.currentShift[0], self.currentShift[1] * -flat_camera_direction[1], self.currentShift[1] * flat_camera_direction[0], 0.0)
        BigWorld.camera().inaccuracyProvider = inaccuracy

    def TwoVectorAngle(self, a, b):
        return math.acos(a.dot(b) / a.length * b.length)

    def updateUnstableScope(self):
        shift_length = self.currentShift.length
        if not self.fire_rocoiling:
            if self.heart_mode:
                speed_koeff = 0.05
            else:
                speed_koeff = 0.8 * ((self.max_shift - shift_length) / self.max_shift) + 0.2
                if speed_koeff < 0.2:
                    speed_koeff = 0.2
        else:
            speed_koeff = 2.0 * shift_length / self.maxRecoilValue + 1.0
        current_speed = self.shiftingSpeed * speed_koeff
        self.currentShift = self.currentShift + self.scopeVelocity.scale(current_speed)
        if shift_length >= self.max_shift:
            if not self.fire_rocoiling:
                angle = self.GetAngleByShift(self.currentShift)
                angle += math.pi
                self.scopeVelocity = self.GetRandomVector(angle, math.pi / 4)
            elif self.TwoVectorAngle(self.scopeVelocity, self.currentShift) < math.pi / 2.0 and shift_length >= self.max_shift * 2.0:
                self.SetReturnPoint()
                self.fire_rocoiling = False
        else:
            self.fire_rocoiling = False
        self.UpdateInaccuracyProvider()
        self.unstableScopeTimer = BigWorld.callback(self.TIMER_PERIOD, self.updateUnstableScope)

    def GetRandomVector(self, start_angle = math.pi, difference = math.pi):
        random_start_angle = start_angle - (difference * 2 * random.random() - difference)
        vector = Math.Vector2(math.cos(random_start_angle), math.sin(random_start_angle))
        vector.normalise()
        return vector

    def GetRandomPointInnerCircle(self, radius):
        point = self.GetRandomVector()
        point = point.scale(random.random() * radius)
        return point

    def beginScopeUnstable(self):
        self.shiftingSpeed = 0.001
        self.currentShift = Math.Vector2(0, 0)
        self.scopeVelocity = self.GetRandomVector()
        self.numShotsCounter = 0
        self.unstableScopeTimer = BigWorld.callback(self.TIMER_PERIOD, self.updateUnstableScope)

    def stopScopeUnstable(self):
        if self.unstableScopeTimer:
            BigWorld.cancelCallback(self.unstableScopeTimer)

    def SetReturnPoint(self):
        return_point = self.GetRandomPointInnerCircle(self.max_shift)
        self.scopeVelocity = Math.Vector2(return_point[0] - self.currentShift[0], return_point[1] - self.currentShift[1])
        self.scopeVelocity.normalise()

    def FireRecoil(self, recoil_value):
        self.maxRecoilValue = recoil_value[1]
        if self.currentShift.length > self.maxRecoilValue:
            if self.currentShift[0] > 0:
                recoil_vector = self.GetRandomVector(math.pi * 1.16, math.pi / 6.0)
            else:
                recoil_vector = self.GetRandomVector(math.pi * 1.833, math.pi / 6.0)
        else:
            recoil_vector = self.GetRandomVector(math.pi / 2.0, math.pi / 6.0)
        recoil_vector = recoil_vector.scale(recoil_value[0] * self.GetRecoilKoeff())
        self.fire_rocoiling = True
        angle = self.GetAngleByShift(recoil_vector)
        self.currentShift = self.currentShift + recoil_vector
        self.SetReturnPoint()
        self.numShotsCounter += 1
        self.UpdateInaccuracyProvider()

    def ResetScope(self):
        self.shiftingSpeed = 0.0
        self.currentShift = Math.Vector2(0, 0)
        self.scopeVelocity = Math.Vector2(0, 0)
        self.UpdateInaccuracyProvider()

    def UpdateKickBack(self):
        pass

    def SetCameraKickback(self, kickback_value):
        player_camera = BigWorld.camera()
        flat_camera_direction = Math.Vector2(player_camera.direction[0], player_camera.direction[2])
        flat_camera_direction.normalise()
        BigWorld.camera().inaccuracyProvider = Math.Vector4(0.0, kickback_value * -flat_camera_direction[1], kickback_value * flat_camera_direction[0], 0.0)
        if self.unstableScope:
            self.unstableScope.stopScopeUnstable()

    def __del__(self):
        BigWorld.camera().inaccuracyProvider = Math.Vector4(0, 0, 0, 0.0)
        self.EndHeartMode()