import numpy as np
from typing import List


def distance_measurement_factor(means: List[np.ndarray], target_distance) -> np.ndarray:
    a = means[0]
    b = means[1]
    return target_distance - np.linalg.norm(a - b)


def distance_measurement_factor_jac(means: List[np.ndarray], target_distance) -> np.ndarray:
    a = means[0]
    b = means[1]
    a_to_b = b - a
    a_to_b_length = np.linalg.norm(a_to_b)

    return np.resize(np.concatenate([-(a - b) / a_to_b_length, (a - b) / a_to_b_length]), (1, a.size * 2))


# -------------------------------------------------------------------------------

def smoothing_factor(means: List[np.ndarray]) -> np.ndarray:
    a, b, c = means
    b_a = a - b
    b_c = c - b
    return 2 * np.pi - np.arctan(np.dot(b_a, b_c) / (np.linalg.norm(b_a) * np.linalg.norm(b_c)))


def smoothing_factor_jac(means: List[np.ndarray]) -> np.ndarray:
    a, b, c = means
    b_a = a - b
    b_c = c - b
    dot = np.dot(b_a, b_c)
    norm = np.linalg.norm(b_a) * np.linalg.norm(b_c)
    arc_fac = 1. / np.sqrt(1. - np.square(dot / norm))
    a_derivative = arc_fac * (norm * b_c - dot * (b_a * np.linalg.norm(b_c) / np.linalg.norm(b_a))) / np.square(norm)
    c_derivative = arc_fac * (norm * b_a - dot * (b_c * np.linalg.norm(b_a) / np.linalg.norm(b_c))) / np.square(norm)
    b_derivative = arc_fac * (norm * (-a - c + 2 * b) - dot * (
            b_c * np.linalg.norm(b_a) / np.linalg.norm(b_c) + b_a * np.linalg.norm(b_c) / np.linalg.norm(
        b_a))) / np.square(norm)
    # ToDo Debug me
    return np.resize(np.concatenate([a_derivative, b_derivative, c_derivative]), (1, a.size * 3))


# -------------------------------------------------------------------------------

def measurement_factor(means: List[np.ndarray]) -> np.ndarray:
    pass


def measurement_factor_jac(means: List[np.ndarray]) -> np.ndarray:
    pass
