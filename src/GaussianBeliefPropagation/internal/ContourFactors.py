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
    return -np.matrix(np.linalg.norm(np.dot(b_a, c_a.T) / np.dot(c_a, c_a.T) * c_a + a - b))


def smoothing_factor_jac(means: List[np.matrix]) -> np.matrix:
    # wolfram alpha : jacobian of (||(b-a).(c-a)^T/((c-a).(c-a)^T)*(c-a)-b+a||)

    a, b, c = means
    c_a = c - a
    b_a = b - a
    c_a_2 = np.dot(c_a, c_a.T)
    one = np.ones_like(c_a)

    fac = np.linalg.norm(c_a * np.asscalar((np.dot(b_a, c_a.T)) / c_a_2) + a - b)

    a_derivative = (c_a * -np.asscalar((np.dot(b_a, c_a.T) * (np.dot(c_a, -c_a.T) + np.dot(-one, c_a.T))) / (
        np.square(np.dot(c_a, c_a.T)))) + c_a * np.asscalar(
        (np.dot(b_a, -c_a.T) + np.dot(-one, c_a.T)) / (np.dot(c_a, c_a.T))) - (
                            np.dot(b_a, c_a.T) / (np.dot(c_a, c_a.T))) + one) * fac

    b_derivative = (c_a * np.asscalar((np.dot(one, c_a.T)) / (np.dot(c_a, c_a.T))) - one) * fac

    c_derivative = (c_a * -np.asscalar(
        (np.dot(b_a, c_a.T) * (np.dot(c_a, c_a.T) + np.dot(one, c_a.T)) / (
            np.square(np.dot(c_a, c_a.T))))) + c_a * np.asscalar(np.dot(b_a, c_a.T) / np.dot(c_a, c_a.T)) + (
                        np.dot(b_a, c_a.T)) / (np.dot(c_a, c_a.T))) * fac
    # ToDo Debug me
    return np.matrix(np.resize(np.array([a_derivative, b_derivative, c_derivative]), (1, a.size * 3)))


# -------------------------------------------------------------------------------

def measurement_factor(means: List[np.matrix]) -> np.matrix:
    pass


def measurement_factor_jac(means: List[np.matrix]) -> np.matrix:
    pass
