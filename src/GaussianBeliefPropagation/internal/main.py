import numpy as np

from GBP import *


def generate_variable_nodes(num_variable_nodes: int, dims=1) -> List[VariableNode]:
    nodes = []
    for i in range(num_variable_nodes):
        nodes.append(VariableNode(dims, i))
    return nodes


def smoothing(means: List[np.ndarray]) -> np.ndarray:
    # assert (len(means) == 2, "Smoothing factor is only defined on two variable nodes. Num vars: " + str(len(means)))
    return means[0] - means[1]


def smoothing_jac(linearization_point: List[np.ndarray]) -> np.ndarray:
    return np.array([1, 1])


def generate_smoothing_factors(v_nodes: List[VariableNode]) -> List[FactorNode]:
    f_nodes = []
    for i in range(len(v_nodes) - 1):
        adj_vars = [v_nodes[i], v_nodes[i + 1]]
        meas_fn = smoothing
        meas_noise = np.array([0.1])
        measurement = 0.
        jac_fn = smoothing_jac
        f_nodes.append(FactorNode(adj_vars, meas_fn, meas_noise, measurement, jac_fn, []))
    return f_nodes


def measurement_fn(means: List[np.ndarray], x_pos_i: float, x_pos_j: float, x_pos_of_measurement: float) -> np.ndarray:
    x_m = x_pos_of_measurement
    x_i = x_pos_i
    x_j = x_pos_j
    y_i = means[0][0]
    y_j = means[1][0]
    lam = (x_m - x_i) / (x_j - x_i)
    return (1 - lam) * y_i + lam * y_j


def measurement_fn_jac(means: List[np.ndarray], x_pos_i: float, x_pos_j: float,
                       x_pos_of_measurement: float) -> np.ndarray:
    x_m = x_pos_of_measurement
    x_i = x_pos_i
    x_j = x_pos_j
    lam = (x_m - x_i) / (x_j - x_i)
    return np.array([(1 - lam), lam])


def generate_measurement_factors(v_nodes: List[VariableNode], num_measurements: int = 10) -> List[FactorNode]:
    f_nodes = []
    for i in range(num_measurements):
        measurement_x_pos = np.random.random()
        idx_var_node = int(measurement_x_pos * (len(v_nodes) - 1))

        adj_vars = [v_nodes[idx_var_node], v_nodes[idx_var_node + 1]]
        measurement = np.random.random()
        meas_fn = measurement_fn
        meas_noise = np.array([0.1])
        jac_fn = measurement_fn_jac
        f_nodes.append(FactorNode(adj_vars, meas_fn, meas_noise, measurement, jac_fn,
                                  [i / len(v_nodes), (i + 1) / len(v_nodes), measurement_x_pos]))

    return f_nodes


if __name__ == "__main__":
    variable_nodes = generate_variable_nodes(5)
    factor_nodes = generate_measurement_factors(variable_nodes)
    factor_nodes.extend(generate_smoothing_factors(variable_nodes))
    factor_graph = FactorGraph(variable_nodes, factor_nodes)

    factor_graph.synchronous_iteration()
    factor_graph.synchronous_iteration()
