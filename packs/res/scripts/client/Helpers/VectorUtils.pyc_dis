# Embedded file name: scripts/client/Helpers/VectorUtils.py
from Math import Vector3
from random import random
from math import pi, sin, cos

def getXYZbyY(ortY):
    """ get basis by Y unit vector"""
    ortY = Vector3(ortY)
    ortY.normalise()
    ortX = Vector3(0, 1, 0) * ortY
    ortX.normalise()
    ortZ = ortX * ortY
    ortZ.normalise()
    return (ortX, ortY, ortZ)


def getXYZbyZ(ortZ):
    """ get basis by Z unit vector"""
    ortZ = Vector3(ortZ)
    ortZ.normalise()
    ortX = Vector3(0, 1, 0) * ortZ
    ortX.normalise()
    ortY = ortZ * ortX
    ortY.normalise()
    return (ortX, ortY, ortZ)


def getTriangleByZ(normal):
    """ Z means unit vector """
    A = Vector3(-0.667, -0.333, 0)
    B = Vector3(0, 0.667, 0)
    C = Vector3(0.667, -0.333, 0)
    X, Y, Z = getXYZbyZ(normal)
    A = expressInBasis(A, X, Y, Z)
    B = expressInBasis(B, X, Y, Z)
    C = expressInBasis(C, X, Y, Z)
    return (A, B, C)


def expressInBasis(vector, x_axis, y_axis, z_axis):
    """ X, Y and Z must be unit vectors """
    return x_axis * vector[0] + y_axis * vector[1] + z_axis * vector[2]


def pointsOnCone(angle, ray_number):
    points = list()
    for i in xrange(ray_number):
        azimuth = (random() * 2 - 1) * pi
        zenith = random() * (0.5 * angle) % (2 * pi)
        points.append((sin(zenith) * sin(azimuth), cos(zenith), sin(zenith) * cos(azimuth)))

    return points