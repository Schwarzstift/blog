import numpy as np

from GBP import *
from ContourFactors import *


class ContourPlottingViz:
    def __init__(self):
        pass

    def save_measurements(self, measurements: List[np.ndarray]):
        pass

    def save_prior_state(self, factor_graph: FactorGraph):
        pass

    def save_posterior_state(self, factor_graph: FactorGraph):
        pass

    def render(self):
        pass


# ---------------------------------- Factor Graph ------------------------------------
def generate_variable_nodes(num_variable_nodes: int) -> List[VariableNode]:
    variable_nodes = []
    for _ in range(num_variable_nodes):
        variable_nodes.append(VariableNode(2))
    return variable_nodes


def generate_distance_factor_nodes(variable_nodes: List[VariableNode], measurement_noise: np.ndarray,
                                   use_huber: bool) -> List[FactorNode]:
    factor_nodes = []
    for i in range(len(variable_nodes)):
        adj_vars = [variable_nodes[i], variable_nodes[i + 1]]
        meas_fn = distance_measurement_factor
        jac_fn = distance_measurement_factor_jac
        measurement = 0.  # ToDo think about this
        factor_nodes.append(FactorNode(adj_vars, meas_fn, measurement_noise, measurement, jac_fn, use_huber, []))
    return factor_nodes


def generate_smoothing_factor_nodes(variable_nodes: List[VariableNode], measurement_noise: np.ndarray,
                                    use_huber: bool) -> List[FactorNode]:
    factor_nodes = []
    for i in range(len(variable_nodes)):
        adj_vars = [variable_nodes[i], variable_nodes[i + 1]]
        meas_fn = smoothing_factor
        jac_fn = smoothing_factor_jac
        measurement = 0.  # ToDo think about this
        factor_nodes.append(FactorNode(adj_vars, meas_fn, measurement_noise, measurement, jac_fn, use_huber, []))
    return factor_nodes


def generate_measurement_factor_nodes(variable_nodes: List[VariableNode], measurement_noise: np.ndarray,
                                      use_huber: bool, measurements: List[np.ndarray]) -> List[FactorNode]:
    factor_nodes = []
    for i in range(len(measurements)):
        adj_vars = []  # ToDo implement me
        meas_fn = measurement_factor
        jac_fn = measurement_factor_jac
        measurement = 0.  # ToDo fill_me
        factor_nodes.append(FactorNode(adj_vars, meas_fn, measurement_noise, measurement, jac_fn, use_huber, []))
    return factor_nodes


# ------------------------------ Putting all together --------------------------------

def generate_prior(num_variable_nodes: int, measurement_noise: np.ndarray, use_huber: bool,
                   measurements: List[np.ndarray]) -> FactorGraph:
    variable_nodes = generate_variable_nodes(num_variable_nodes)
    factor_nodes = []
    factor_nodes.extend(generate_distance_factor_nodes(variable_nodes, measurement_noise, use_huber))
    factor_nodes.extend(generate_smoothing_factor_nodes(variable_nodes, measurement_noise, use_huber))
    factor_nodes.extend(generate_measurement_factor_nodes(variable_nodes, measurement_noise, use_huber, measurements))

    return FactorGraph(variable_nodes, factor_nodes)


def update_factor_graph(new_measurements: List[np.ndarray], factor_graph: FactorGraph) -> FactorGraph:
    # ToDo set state as prior
    # ToDO grow/shrink as needed
    return factor_graph


def sample_from_line(num_measurements: int) -> List[np.ndarray]:
    measurements = []
    for i in range(num_measurements):
        x, y = np.random.random(2)
        y *= 0.05
        measurements.append(np.array([x, y]))
    return measurements


def generate_measurements(num_range: List[int]) -> List[np.ndarray]:
    num_measurements = np.random.random_integers(*num_range)
    return sample_from_line(num_measurements)


def main():
    num_measurements_range = [10, 15]
    num_frames = 1
    num_variable_nodes = 2
    measurement_noise = np.array([[42]])
    use_huber = False

    viz = ContourPlottingViz()
    measurements = generate_measurements(num_measurements_range)
    factor_graph = generate_prior(num_variable_nodes, measurement_noise, use_huber, measurements)

    for _ in range(num_frames):
        viz.save_prior_state(factor_graph)
        factor_graph.fit()
        viz.save_posterior_state(factor_graph)

        measurements = generate_measurements(num_measurements_range)
        factor_graph = update_factor_graph(measurements, factor_graph)
    viz.render()


if __name__ == "__main__":
    main()
