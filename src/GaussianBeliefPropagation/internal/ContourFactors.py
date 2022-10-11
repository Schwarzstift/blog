import numpy as np
from typing import List


def distance_measurement_factor(means: List[np.matrix], target_distance) -> np.matrix:
    a = means[0]
    b = means[1]
    return target_distance - np.linalg.norm(a - b)


def distance_measurement_factor_jac(means: List[np.matrix], target_distance) -> np.matrix:
    a = means[0]
    b = means[1]
    a_to_b = b - a
    a_to_b_length = np.linalg.norm(a_to_b)

    return np.matrix(np.resize(np.concatenate([-(a - b) / a_to_b_length, (a - b) / a_to_b_length]), (1, a.size * 2)))


# -------------------------------------------------------------------------------

def smoothing_factor(means: List[np.matrix]) -> np.matrix:
    # distance point to line
    a, b, c = means
    b_a = b - a
    c_a = c - a
    center = a + c_a / (np.linalg.norm(c_a) * 0.5)

    #projection = np.dot(b_a, c_a.T) / np.dot(c_a, c_a.T) * c_a + a
    distance = np.matrix(np.linalg.norm(center - b))
    return distance


def smoothing_factor_jac(means: List[np.matrix]) -> np.matrix:
    # wolfram alpha : jacobian of (||(b-a).(c-a)^T/((c-a).(c-a)^T)*(c-a)+a-b||)

    a, b, c = means
    c_a = c - a
    b_a = b - a
    one = np.ones_like(c_a)

    projection = np.dot(b_a, c_a.T) / np.dot(c_a, c_a.T) * c_a + a
    direction = np.sign(projection - b)

    # a_derivative = c_a * -np.asscalar((np.dot(b_a, c_a.T) * (np.dot(c_a, -c_a.T) + np.dot(-one, c_a.T))) / (
    #     np.square(np.dot(c_a, c_a.T)))) + c_a * np.asscalar(
    #     (np.dot(b_a, -c_a.T) + np.dot(-one, c_a.T)) / (np.dot(c_a, c_a.T))) - (
    #                         np.dot(b_a, c_a.T) / (np.dot(c_a, c_a.T))) + one

    b_derivative = (c_a * np.asscalar((np.dot(one, c_a.T)) / (np.dot(c_a, c_a.T)))) - one

    # c_derivative = (c_a * -np.asscalar(
    #     (np.dot(b_a, c_a.T) * (np.dot(c_a, c_a.T) + np.dot(one, c_a.T)) / (
    #         np.square(np.dot(c_a, c_a.T))))) + c_a * np.asscalar(np.dot(b_a, c_a.T) / np.dot(c_a, c_a.T)) + (
    #                     np.dot(b_a, c_a.T)) / (np.dot(c_a, c_a.T)))
    # ToDo Debug me
    return np.matrix(np.resize(
        np.array([np.zeros_like(b_derivative), np.multiply(b_derivative, direction), np.zeros_like(b_derivative)]),
        (1, a.size * 3)))


# -------------------------------------------------------------------------------

def measurement_factor(means: List[np.matrix]) -> np.matrix:
    pass


def measurement_factor_jac(means: List[np.matrix]) -> np.matrix:
    pass
