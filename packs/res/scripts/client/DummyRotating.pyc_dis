# Embedded file name: scripts/client/DummyRotating.py
__author__ = 'yogi'
from Math import Matrix, MatrixAnimation
from math import pi
from Keys import *
import BigWorld

class DummyRotating(object):
    """        This singleton class rotate avatar dummy"""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DummyRotating, cls).__new__(cls)
        return cls.instance

    def init_motor(self, model):
        self.model = model
        self.angle = model.yaw
        self.base_matrix = Matrix()
        self.base_matrix.set(model.matrix)
        self.animation_matrix = MatrixAnimation()
        self.animation_matrix.keyframes = [(0.0, self.base_matrix)]
        self.animation_matrix.loop = False
        self.animation_matrix.time = 0.0
        self.motor = BigWorld.Servo(self.animation_matrix)
        self.model.addMotor(self.motor)

    def rotate(self, dx):
        mt = Matrix()
        self._angle(dx)
        mt.setRotateY(self.angle)
        mt.translation = self.base_matrix.translation
        self.motor.signal.time = 0.0
        self.motor.signal.keyframes = [(0.0, self.motor.signal.keyframes[-1][1]), (0.5, mt)]

    def _angle(self, dx):
        angle = float(dx) * 0.02
        if angle > pi:
            angle = pi
        elif angle < -pi:
            angle = -pi
        self.angle -= angle
        if self.angle > 2 * pi:
            self.angle -= 2 * pi
        elif self.angle > -2 * pi:
            self.angle += 2 * pi