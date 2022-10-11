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
    center = a + c_a * 0.5
    distance = np.linalg.norm(center - b)
    return np.matrix(distance)


def smoothing_factor_jac(means: List[np.matrix]) -> np.matrix:
    # wolfram alpha : jacobian of (||a+(c-a)*0.5-b||)
    a, b, c = means
    c_a = c - a

    direction_vector = a + c_a * 0.5 - b
    unit_direction_vector = direction_vector / np.linalg.norm(direction_vector)
    a_derivative = unit_direction_vector * 0.5
    b_derivative = unit_direction_vector * -1
    c_derivative = unit_direction_vector * 0.5
    return np.matrix(np.resize(np.array([np.zeros_like(a_derivative), b_derivative, np.zeros_like(c_derivative)]), (1, a.size * 3)))


# -------------------------------------------------------------------------------

def measurement_factor(means: List[np.matrix]) -> np.matrix:
    pass


def measurement_factor_jac(means: List[np.matrix]) -> np.matrix:
    pass
