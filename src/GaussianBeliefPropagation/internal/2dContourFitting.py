import numpy as np
import matplotlib.pyplot as plt
from GBP import *
from ContourFactors import *
from matplotlib.animation import FuncAnimation

np.random.seed(42)


class ContourPlottingViz:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.measurement_list = []
        self.prior_state_mu_list = []
        self.prior_state_cov_list = []
        self.posterior_state_mu_list = []
        self.posterior_state_cov_list = []

    def save_measurements(self, measurements: List[np.ndarray]):
        self.measurement_list.append(measurements)

    def save_state(self, factor_graph: FactorGraph):
        prior_mus = []
        prior_covs = []
        posterior_mus = []
        posterior_covs = []
        for node in factor_graph.variable_nodes:
            mu, cov = node.prior.get_values()
            prior_mus.append(mu)
            prior_covs.append(cov)
            mu, cov = node.belief.get_values()
            posterior_mus.append(mu)
            posterior_covs.append(cov)
        self.prior_state_mu_list.append(prior_mus)
        self.prior_state_cov_list.append(prior_covs)
        self.posterior_state_mu_list.append(posterior_mus)
        self.posterior_state_cov_list.append(posterior_covs)

    def render(self):
        fig, ax = plt.subplots(1, 1)

        def animate(t):
            ax.clear()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            x, y = zip(*self.measurement_list[0])
            ax.scatter(x, y)

            x, y = zip(*self.prior_state_mu_list[0])
            ax.plot(x, y, marker="x", color="red")
            x, y = zip(*self.posterior_state_mu_list[t])
            ax.plot(x, y, marker="x", color="yellow")

        ani = FuncAnimation(fig, animate, frames=self.num_frames, repeat=False)

        plt.show()


# ---------------------------------- Factor Graph ------------------------------------
def generate_variable_nodes(num_variable_nodes: int) -> List[VariableNode]:
    variable_nodes = []
    #i = 0
    for _ in range(num_variable_nodes):
        pos_prior = np.random.random(2)
        #pos_prior = np.array([i / 2. + 0.2, 0.5])
        #i+=1
        cov_prior = np.array([[100., 0.], [0., 100.]])
        prior = GaussianState(2)
        prior.set_values(pos_prior, cov_prior)
        variable_nodes.append(VariableNode(2, prior))
    return variable_nodes


def generate_distance_factor_nodes(variable_nodes: List[VariableNode], measurement_noise: np.ndarray,
                                   use_huber: bool, target_distance: float) -> List[FactorNode]:
    factor_nodes = []
    for i in range(len(variable_nodes) - 1):
        adj_vars = [variable_nodes[i], variable_nodes[i + 1]]
        meas_fn = distance_measurement_factor
        jac_fn = distance_measurement_factor_jac
        measurement = 0.  # ToDo think about this
        factor_nodes.append(
            FactorNode(adj_vars, meas_fn, measurement_noise, measurement, jac_fn, use_huber, [target_distance]))
    return factor_nodes


def generate_smoothing_factor_nodes(variable_nodes: List[VariableNode], measurement_noise: np.ndarray,
                                    use_huber: bool) -> List[FactorNode]:
    factor_nodes = []
    for i in range(len(variable_nodes) - 1):
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
                   measurements: List[np.ndarray], target_distance) -> FactorGraph:
    variable_nodes = generate_variable_nodes(num_variable_nodes)
    factor_nodes = []
    factor_nodes.extend(generate_distance_factor_nodes(variable_nodes, measurement_noise, use_huber, target_distance))
    # factor_nodes.extend(generate_smoothing_factor_nodes(variable_nodes, measurement_noise, use_huber))
    # factor_nodes.extend(generate_measurement_factor_nodes(variable_nodes, measurement_noise, use_huber, measurements))

    return FactorGraph(variable_nodes, factor_nodes)


def update_factor_graph(new_measurements: List[np.ndarray], factor_graph: FactorGraph) -> FactorGraph:
    # ToDo set state as prior
    # ToDO grow/shrink as needed
    return factor_graph


def sample_from_line(num_measurements: int) -> List[np.ndarray]:
    measurements = []
    for i in range(num_measurements):
        x, y = np.random.random(2)
        y = y * 0.05 + 0.5
        measurements.append(np.array([x, y]))
    return measurements


def generate_measurements(num_range: List[int]) -> List[np.ndarray]:
    num_measurements = np.random.randint(*num_range)
    return sample_from_line(num_measurements)


def main():
    num_measurements_range = [10, 15]
    num_frames = 10
    num_variable_nodes = 10
    measurement_noise = np.array([[0.01]])
    use_huber = False
    target_distance = 0.2

    viz = ContourPlottingViz(num_frames)
    measurements = generate_measurements(num_measurements_range)
    viz.save_measurements(measurements)

    factor_graph = generate_prior(num_variable_nodes, measurement_noise, use_huber, measurements, target_distance)

    for _ in range(num_frames):
        factor_graph.fit()
        viz.save_state(factor_graph)
    #
    #     measurements = generate_measurements(num_measurements_range)
    #     viz.save_measurements(measurements)
    #     factor_graph = update_factor_graph(measurements, factor_graph)
    viz.render()


if __name__ == "__main__":
    main()
