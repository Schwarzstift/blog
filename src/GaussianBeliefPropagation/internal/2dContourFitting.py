import numpy as np
import matplotlib.pyplot as plt
from GBP import *
from ContourFactors import *
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

np.random.seed(42)


def confidence_ellipse(center, cov, ax, n_std=3.0, facecolor='none', **kwargs):
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the standard deviation of x from
    # the square-root of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = center[0]

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = center[1]

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


class ContourPlottingViz:
    def __init__(self):
        self.measurement_list = []
        self.prior_state_mu_list = []
        self.prior_state_cov_list = []
        self.posterior_state_mu_list = []
        self.posterior_state_cov_list = []

    def save_measurements(self, measurements: List[np.matrix]):
        self.measurement_list.append([np.asarray(m).flatten() for m in measurements])

    def save_state(self, factor_graph: FactorGraph):
        prior_mus = []
        prior_covs = []
        posterior_mus = []
        posterior_covs = []
        for node in factor_graph.variable_nodes:
            mu, cov = node.prior.get_values()
            prior_mus.append(np.asarray(mu).flatten())
            prior_covs.append(cov)
            mu, cov = node.belief.get_values()
            posterior_mus.append(np.asarray(mu).flatten())
            posterior_covs.append(cov)
        self.prior_state_mu_list.append(prior_mus)
        self.prior_state_cov_list.append(prior_covs)
        self.posterior_state_mu_list.append(posterior_mus)
        self.posterior_state_cov_list.append(posterior_covs)

    def render(self):
        fig, ax = plt.subplots(1, 1)

        def animate(t):
            ax.clear()
            ax.set_title("Iterations: " + str(t))
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            x, y = zip(*self.measurement_list[t])
            ax.scatter(x, y)

            x, y = zip(*self.prior_state_mu_list[t])
            ax.plot(x, y, marker="x", color="red")

            for mean, cov in zip(self.prior_state_mu_list[t], self.prior_state_cov_list[t]):
                confidence_ellipse(mean, cov, ax, 1., edgecolor="red", linestyle=':')

            x, y = zip(*self.posterior_state_mu_list[t])
            ax.plot(x, y, marker="x", color="purple")

            for mean, cov in zip(self.posterior_state_mu_list[t], self.posterior_state_cov_list[t]):
                confidence_ellipse(mean, cov, ax, 1., edgecolor="purple", linestyle=':')

        ani = FuncAnimation(fig, animate, frames=len(self.prior_state_mu_list), repeat=False)
        FFwriter = FFMpegWriter(fps=10)
        ani.save('animation.mp4', writer=FFwriter)
        plt.show()


# ---------------------------------- Factor Graph ------------------------------------
def generate_variable_nodes(num_variable_nodes: int) -> List[VariableNode]:
    variable_nodes = []
    for i in range(num_variable_nodes):
        cov_prior = np.matrix([[1000., 0.], [0., 1000.]])
        # pos_prior = np.random.random(2)

        a = (i / num_variable_nodes) * np.pi * 1.5
        r = 0.1
        rot_mat = np.matrix(np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]))
        center = np.matrix([0.5, 0.5])
        dir = np.matrix([1, 1]) @ rot_mat * r
        pos_prior = np.matrix(center + dir)

        # pos_prior = np.matrix([(i + 1) / (num_variable_nodes + 1) - 0.1, 0.5 + np.random.random() * 0.1])
        # pos_prior = np.matrix([0.5, 0.6])
        prior = GaussianState(2)
        prior.set_values(pos_prior, cov_prior)
        variable_nodes.append(VariableNode(2, prior))
    return variable_nodes


def generate_distance_factor_nodes(variable_nodes: List[VariableNode], measurement_noise: np.matrix,
                                   use_huber: bool, target_distance: float) -> List[FactorNode]:
    factor_nodes = []
    for i in range(len(variable_nodes) - 1):
        adj_vars = [variable_nodes[i], variable_nodes[i + 1]]
        meas_fn = distance_measurement_factor
        jac_fn = distance_measurement_factor_jac
        measurement = 0.
        factor_nodes.append(
            FactorNode(adj_vars, meas_fn, measurement_noise, measurement, jac_fn, use_huber, [target_distance]))
    return factor_nodes


def generate_smoothing_factor_nodes(variable_nodes: List[VariableNode], measurement_noise: np.matrix,
                                    use_huber: bool) -> List[FactorNode]:
    factor_nodes = []
    for i in range(1, len(variable_nodes) - 1):
        adj_vars = [variable_nodes[i - 1], variable_nodes[i], variable_nodes[i + 1]]
        meas_fn = smoothing_factor
        jac_fn = smoothing_factor_jac
        measurement = 0.
        factor_nodes.append(FactorNode(adj_vars, meas_fn, measurement_noise, measurement, jac_fn, use_huber, []))
    return factor_nodes


def generate_measurement_factor_nodes(variable_nodes: List[VariableNode], measurement_noise: np.matrix,
                                      use_huber: bool, measurements: List[np.matrix]) -> List[FactorNode]:
    factor_nodes = []
    for m in measurements:
        adj_vars = variable_nodes  # ToDo maybe implement gating
        meas_fn = measurement_factor
        jac_fn = measurement_factor_jac
        measurement = 0.
        factor_nodes.append(
            FactorNode(adj_vars, meas_fn, measurement_noise, measurement, jac_fn, use_huber, [m]))
    return factor_nodes


# ------------------------------ Putting all together --------------------------------
def generate_factors(variable_nodes, use_huber, measurements, target_distance):
    factor_nodes = []
    # factor_nodes.extend(generate_distance_factor_nodes(variable_nodes, np.matrix(0.0002), use_huber, target_distance))
    factor_nodes.extend(generate_smoothing_factor_nodes(variable_nodes, np.matrix(0.07), use_huber))
    factor_nodes.extend(
        generate_measurement_factor_nodes(variable_nodes, np.identity(len(variable_nodes) * 2) * 0.1, use_huber,
                                          measurements))
    return factor_nodes


def generate_prior(num_variable_nodes: int, use_huber: bool,
                   measurements: List[np.matrix], target_distance) -> FactorGraph:
    variable_nodes = generate_variable_nodes(num_variable_nodes)
    factor_nodes = generate_factors(variable_nodes, use_huber, measurements, target_distance)
    return FactorGraph(variable_nodes, factor_nodes)


def reset_variable_nodes(variable_nodes: List[VariableNode]):
    for v in variable_nodes:
        v.reset(np.identity(v.belief.lam.shape[0]) * 0.01)


def add_new_nodes(variable_nodes: List[VariableNode]):
    num_birth_components = 0
    birth_distance = 0.15
    i = 0
    while i < len(variable_nodes) - 1:
        v_i = variable_nodes[i]
        v_j = variable_nodes[i + 1]
        if np.linalg.norm(v_i.mu - v_j.mu) > birth_distance:
            new_mu = (v_i.mu + 0.5 * (v_j.mu - v_i.mu))
            new_sigma = (v_i.sigma + v_j.sigma) / 2.
            belief = GaussianState(v_i.dimensions)
            belief.set_values(new_mu.T, new_sigma)
            new_node = VariableNode(v_j.dimensions, belief)
            new_node.mu = new_mu
            new_node.sigma = new_sigma

            new_lam = (v_i.prior.lam + v_j.prior.lam) / 2.
            new_eta = (v_i.prior.eta + v_j.prior.eta) * 0.5
            prior = GaussianState(v_i.dimensions)
            prior.lam = new_lam
            prior.eta = new_eta

            new_node.prior = prior
            variable_nodes.insert(i + 1, new_node)
            num_birth_components += 1
            # continue
        i += 1
    # reset nodes
    for idx, v in zip(range(len(variable_nodes)), variable_nodes):
        v.adj_factors_idx = []
        v.factor_nodes = []
        v.idx = idx
    return num_birth_components


def give_birth(measurements, use_huber, target_distance, factor_graph) -> (FactorGraph, int):
    FactorNode.idx_counter = 0
    num_birth_components = add_new_nodes(factor_graph.variable_nodes)
    factor_nodes = generate_factors(factor_graph.variable_nodes, use_huber, measurements, target_distance)

    # ToDO shrink as needed
    return FactorGraph(factor_graph.variable_nodes, factor_nodes), num_birth_components


def update_factor_graph(new_measurements: List[np.matrix], use_huber, target_distance,
                        factor_graph: FactorGraph) -> (FactorGraph):
    variable_nodes = factor_graph.variable_nodes
    reset_variable_nodes(variable_nodes)
    FactorNode.idx_counter = 0
    factor_nodes = generate_factors(variable_nodes, use_huber, new_measurements, target_distance)

    # ToDO shrink as needed
    return FactorGraph(factor_graph.variable_nodes, factor_nodes)


def sample_from_line(num_measurements: int) -> List[np.matrix]:
    measurements = []
    for i in range(num_measurements):
        x, y = np.random.random(2)
        y = y * 0.05 + 0.5
        measurements.append(np.matrix([x, y]))
    return measurements


def sample_from_step(num_measurements: int) -> List[np.matrix]:
    measurements = []
    for i in range(num_measurements):
        x, y = np.random.random(2)
        y = y * 0.05 + 0.1
        if x > 0.5:
            y += 0.5

        measurements.append(np.matrix([x, y]))
    return measurements


def sample_from_circle(num_measurements: int) -> List[np.matrix]:
    measurements = []
    for i in range(num_measurements):
        a = np.random.random(1) * np.pi + 0.5
        r = 0.3
        rot_mat = np.matrix(np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]))
        center = np.matrix([0.5, 0.5])
        dir = np.matrix([1, 1]) @ rot_mat * r
        measurements.append(center + dir)
    return measurements


def sample_from_rect(num_measurements: int) -> List[np.matrix]:
    measurements = []
    for i in range(num_measurements):
        front_side = np.random.random() < 0.5
        dist = np.random.random()
        support_vect = np.array([0.1, 0.1])
        support_vect += support_vect * np.random.random() * 0.05
        dir_vect = np.array([0., 1.])
        if front_side:
            dir_vect = np.array([1., 0.])

        measurements.append(support_vect + (dir_vect * dist * 0.5))
    return measurements


def generate_measurements(num_range: List[int]) -> List[np.matrix]:
    num_measurements = np.random.randint(*num_range)
    return sample_from_rect(num_measurements)


def main():
    num_measurements_range = [30, 40]
    num_frames = 10
    num_variable_nodes = 2
    use_huber = False
    target_distance = 0.5

    viz = ContourPlottingViz()
    measurements = generate_measurements(num_measurements_range)
    viz.save_measurements(measurements)

    factor_graph = generate_prior(num_variable_nodes, use_huber, measurements, target_distance)

    for i in range(num_frames):
        print("New Measurement: " + str(i))
        total_iterations = 0
        num_new_components = True
        while num_new_components != 0:
            iterations = factor_graph.fit()
            total_iterations += iterations
            viz.save_state(factor_graph)
            viz.save_measurements(measurements)
            factor_graph, num_new_components = give_birth(measurements, use_huber, target_distance,
                                                          factor_graph)
            print("Iterations: " + str(iterations) + " added components: " + str(num_new_components))

        print("Total iterations: " + str(total_iterations))
        measurements = generate_measurements(num_measurements_range)
        viz.save_measurements(measurements)
        factor_graph = update_factor_graph(measurements, use_huber, target_distance, factor_graph)
    viz.render()


if __name__ == "__main__":
    main()
