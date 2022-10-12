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
    return np.matrix(
        np.resize(np.array([np.zeros_like(a_derivative), b_derivative, np.zeros_like(c_derivative)]), (1, a.size * 3)))


# -------------------------------------------------------------------------------

def measurement_factor(means: List[np.matrix], measurement_point) -> np.matrix:
    distances2 = []
    distances = []
    sum_inv_dist = 0
    for p in means:
        dist = np.linalg.norm(measurement_point - p)
        distances2.append(dist * dist)
        distances.append(dist)
        sum_inv_dist += 1. / dist
    measurement = 0
    for i in range(len(means)):
        mean = means[i]
        dist = distances[i]
        dist2 = distances2[i]
        c = sum_inv_dist - 1 / dist
        w = np.linalg.norm((measurement_point - mean) / (dist2 * c + dist))
        measurement += dist * w
    return np.matrix(measurement)


def measurement_factor_jac(means: List[np.matrix], measurement_point) -> np.matrix:
    distances2 = []
    distances = []
    sum_inv_dist = 0
    for p in means:
        dist = np.linalg.norm(measurement_point - p)
        distances2.append(dist * dist)
        distances.append(dist)
        sum_inv_dist += 1. / dist
    direction_vectors = []
    for p, i in zip(means, range(len(means))):
        mean = means[i]
        dist = distances[i]
        dist2 = distances2[i]
        c = sum_inv_dist - 1 / dist
        w = np.linalg.norm((measurement_point - mean) / (dist2 * c + dist))

        direction = (measurement_point - p)

        fac = - (2 + 3 * c * dist) / (dist + 2 * c * dist * dist + c * c * dist * dist * dist)
        direction *= (w/dist + fac)
        direction_vectors.append(direction.flatten())
    return np.vstack(direction_vectors).flatten()
