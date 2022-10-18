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
        dist = np.linalg.norm(measurement_point - p)
        # dist = np.asscalar(np.sqrt(
        #    (measurement_point - p) @ np.linalg.inv(np.matrix([[0.001, 0], [0, 0.001]])) @ (measurement_point - p).T))
        dist = dist ** 4
        distances.append(dist)
        sum_inv_dist += 1. / dist
    measurement = []
    min_dist_idx = np.argmin(distances)
    for i in range(len(means)):
        mean = means[i]
        dist = distances[i]
        direction = measurement_point - mean
        w = (1 / (dist * sum_inv_dist))
        measurement.append(direction * w)
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


# -------------------------------------------------------------------------------


def line_measurement_factor(means: List[np.matrix], measurement_point) -> np.matrix:
    best_measurement = None
    diff = np.finfo(float).max
    for i in range(len(means) - 1):
        a, b = means[i], means[i + 1]
        ab = b - a
        ab_length = np.linalg.norm(ab)
        m = measurement_point - a
        expected_num_points_on_line = 20.# ToDo find a way to boost a and b case
        projection_point = ((ab.T @ ab) / (ab @ ab.T) @ m.T + a.T).T
        if np.linalg.norm(projection_point - a + ab) < ab_length:
            # projection behind a
            measurement = [expected_num_points_on_line*(measurement_point - a), np.zeros_like(m)]
            reference_point = a
        elif np.linalg.norm(projection_point - b - ab) < ab_length:
            # projection behind b
            measurement = [np.zeros_like(m), expected_num_points_on_line*(measurement_point - b)]
            reference_point = b
        else:
            # projection on ab
            reference_point = projection_point
            projection_vector = measurement_point - projection_point
            residual = np.linalg.norm(projection_vector)
            lam = np.linalg.norm(projection_point - a) / ab_length
            a_vec = (reference_point - a)
            b_vec = (reference_point - b)

            expected_num_points_on_line = 20.
            b_vec *= lam/expected_num_points_on_line
            a_vec *= (1 - lam)/expected_num_points_on_line

            measurement = [(1 - lam) * projection_vector + a_vec, lam * projection_vector + b_vec]

        if len(means) > 2:
            if i == 0:
                measurement.append(np.zeros_like(m))
            else:
                measurement.insert(0, np.zeros_like(m))
        measurement = np.matrix(np.array(measurement)).flatten()
        d = np.linalg.norm(reference_point - measurement_point)
        if diff > d:
            diff = d
            best_measurement = measurement
    return -np.matrix(best_measurement).flatten()


def line_measurement_factor_jac(means: List[np.matrix], measurement_point) -> np.matrix:
    return np.identity(len(means) * 2)


# -------------------------------------------------------------------------------

def line_collapse_factor(means: List[np.matrix], measurements) -> np.matrix:
    a, b = means
    dist_to_a = [np.linalg.norm(a - m) for m in measurements]
    dist_to_b = [np.linalg.norm(b - m) for m in measurements]
    min_dist_idx_a = np.argmin(dist_to_a)
    min_dist_idx_b = np.argmin(dist_to_b)

    m_a = measurements[min_dist_idx_a]
    m_b = measurements[min_dist_idx_b]

    ab = b - a
    m = m_a - a
    projection_point_a = ((ab.T @ ab) / (ab @ ab.T) @ m.T + a.T).T

    m = m_b - a
    projection_point_b = ((ab.T @ ab) / (ab @ ab.T) @ m.T + a.T).T

    return -np.matrix(np.array([projection_point_a - a, projection_point_b - b])).flatten()


def line_collapse_factor_jac(means: List[np.matrix], collapse_force) -> np.matrix:
    return np.identity(len(means) * 2)
