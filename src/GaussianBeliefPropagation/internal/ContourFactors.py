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

    return np.resize(np.concatenate([-(a-b) / a_to_b_length, (a-b) / a_to_b_length]), (1, a.size + b.size))


# -------------------------------------------------------------------------------

def smoothing_factor(means: List[np.ndarray]) -> np.ndarray:
    pass


def smoothing_factor_jac(means: List[np.ndarray]) -> np.ndarray:
    pass


# -------------------------------------------------------------------------------

def measurement_factor(means: List[np.ndarray]) -> np.ndarray:
    pass


def measurement_factor_jac(means: List[np.ndarray]) -> np.ndarray:
    pass
