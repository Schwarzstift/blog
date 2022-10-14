import numpy as np
from typing import List

from numpy import ndarray


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
    c_a = c - a
    center = a + c_a * 0.5
    distance = np.linalg.norm(center - b)
    return np.matrix(distance)


def smoothing_factor_jac(means: List[np.matrix]) -> np.matrix:
    # wolfram alpha : jacobian of (||a+(c-a)*0.5-b||)
    a, b, c = means
    c_a = c - a

    direction_vector = a + c_a * 0.5 - b
    if np.any(direction_vector):
        unit_direction_vector = direction_vector / np.linalg.norm(direction_vector)
    else:
        unit_direction_vector = np.zeros_like(direction_vector)
    a_derivative = unit_direction_vector * 0.5
    b_derivative = unit_direction_vector * -1
    c_derivative = unit_direction_vector * 0.5
    return np.matrix(
        np.resize(np.array([np.zeros_like(a_derivative), b_derivative, np.zeros_like(c_derivative)]), (1, a.size * 3)))


# -------------------------------------------------------------------------------

def measurement_factor(means: List[np.matrix], measurement_point) -> np.matrix:
    distances = []
    sum_inv_dist = 0
    for p in means:
        dist = np.linalg.norm(measurement_point - p) ** 3
        # dist = np.asscalar((measurement_point - p) @ np.linalg.inv(np.matrix([[0.1, 0], [0, 0.1]])) @ (measurement_point - p).T)
        # dist = np.square(dist)
        distances.append(dist)
        sum_inv_dist += 1. / dist
    measurement = []
    for i in range(len(means)):
        mean = means[i]
        dist = distances[i]
        direction = measurement_point - mean

        measurement.append(direction * (1 / (dist * sum_inv_dist)))
    return -np.matrix(np.array(measurement)).flatten()


def measurement_factor_jac(means: List[np.matrix], measurement_point) -> ndarray:
    distances = []
    sum_dist = 0
    for p in means:
        dist = np.linalg.norm(measurement_point - p)
        distances.append(dist)
        sum_dist += dist
    direction_vectors = []
    for p, i in zip(means, range(len(means))):
        d = distances[i]

        direction = -1 + d / sum_dist - d * d * (sum_dist / d + 1) / (sum_dist * sum_dist)
        direction_vectors.append(-direction)

    return np.identity(len(means) * 2)
