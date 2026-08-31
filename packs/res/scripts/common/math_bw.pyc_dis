# Embedded file name: scripts/common/math_bw.py
import math
import bisect
from random import random
from Math import Vector3, Matrix
neg_inf = float('-inf')
VECTOR3_INVALID = Vector3(neg_inf, neg_inf, neg_inf)
VECTOR3_ZERO = Vector3(0, 0, 0)
VECTOR3_UP = Vector3(0, 1, 0)

def angle_between_vectors(v1, v2):
    cos = v1.dot(v2) / (v1.length * v2.length)
    return math.acos(cos)


def rotate_by_yaw_pitch(vec, yaw, pitch):
    m = Matrix()
    m.setRotateYPR((yaw, pitch, 0))
    return m.applyVector(vec)


def randomPointInRadius(radius, center = Vector3(0, 0, 0)):
    angle = random() * 2 * math.pi
    pos = center + radius * Vector3(math.cos(angle), 0, math.sin(angle))
    return pos


def print_matrix(*matrix_providers):
    matrices = map(Matrix, matrix_providers)
    for row in range(0, 4):
        for matrix in matrices:
            for col in range(0, 4):
                print '%6.1f' % matrix.get(row, col),

            print ' | ',

        print '\n'


def weighted_random(weights):
    rnd = random() * sum(weights)
    for i, weight in enumerate(weights):
        rnd -= weight
        if rnd < 0:
            return i


class WeightedRandom:
    """ Select random index using weights.
            Runs faster than weighted_random func if you need several selections.
    """

    def __init__(self, weights):
        total_sum = float(sum(weights))
        self.weights = []
        prev_sum = 0
        for weight in weights:
            prev_sum += weight
            self.weights.append(prev_sum / total_sum)

    def get(self):
        return bisect.bisect(self.weights, random())


def distance_from_point_to_line(point, point_on_line, vector_of_line):
    point, point_on_line, vector_of_line = Vector3(point), Vector3(point_on_line), Vector3(vector_of_line)
    return ((point - point_on_line) * vector_of_line).length / vector_of_line.length


def is_point_in_cylinder(point, cylinder_cap_center, cylinder_vector, cylinder_radius):
    """ is_point_in_cylinder(impact_point, fire_src_point, fire_vector, valid_impact_threshold)"""
    return distance_from_point_to_line(point, cylinder_cap_center, cylinder_vector) <= cylinder_radius


def erf(x):
    """approximation of http://en.wikipedia.org/wiki/Error_function"""
    sign = 1 if x >= 0 else -1
    x = abs(x)
    t = 1.0 / (1.0 + 0.3275911 * x)
    return sign * (1.0 - ((((1.061405429 * t + -1.453152027) * t + 1.421413741) * t + -0.284496736) * t + 0.254829592) * t * math.exp(-x ** 2))