import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from GBP import *

np.random.seed(44)


# np.random.seed(43)


# ---------------------------- VISUALIZATION ------------------------------------
class ContourFittingViz:
    def __init__(self, v_nodes: List[VariableNode], measurements: List[np.ndarray], num_iterations):
        self.fig, self.ax = plt.subplots()
        self.ax.set_ylim(0, 1)
        self.measurements_x, self.measurements_y = zip(*measurements)
        self.num_iterations = num_iterations

        self.x_positions = []
        y_positions = []
        num_vars = len(v_nodes)
        for i in range(num_vars):
            self.x_positions.append(v_nodes[i].x_pos)
            y_positions.append(v_nodes[i].mu)
        self.iterations = [y_positions]

    def render(self):

        self.ax.scatter(self.measurements_x, self.measurements_y)
        self.ax.scatter(self.x_positions, self.iterations[0])

        def animate(t):
            self.ax.clear()
            self.ax.set_ylim(0, 1)
            self.ax.set_title("Iteration: " + str(t))
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('Height')
            self.ax.scatter(self.measurements_x, self.measurements_y)
            self.ax.scatter(self.x_positions, self.iterations[t])

        ani = FuncAnimation(self.fig, animate, frames=self.num_iterations, repeat=False)
        plt.show()

    def add_iteration(self, v_nodes: List[VariableNode]):
        y_positions = []
        for v in v_nodes:
            y_positions.append(v.mu)
        self.iterations.append(y_positions)


# ---------------------- FACTOR GRAPH SPECIFIC STUFF ----------------------------
def generate_variable_nodes(num_variable_nodes: int, dims) -> List[VariableNode]:
    nodes = []
    for i in range(num_variable_nodes):
        node = VariableNode(dims)
        node.x_pos = i / (num_variable_nodes - 1)

        nodes.append(node)
    return nodes


def smoothing(means: List[np.ndarray]) -> np.ndarray:
    # assert (len(means) == 2, "Smoothing factor is only defined on two variable nodes. Num vars: " + str(len(means)))
    return means[0] - means[1]


def smoothing_jac(linearization_point: List[np.ndarray]) -> np.ndarray:
    return np.array([1, -1])


def generate_smoothing_factors(v_nodes: List[VariableNode]) -> List[FactorNode]:
    f_nodes = []
    for i in range(len(v_nodes) - 1):
        adj_vars = [v_nodes[i], v_nodes[i + 1]]
        meas_fn = smoothing
        meas_noise = np.array([0.00004])
        measurement = 0.
        jac_fn = smoothing_jac
        f_nodes.append(FactorNode(adj_vars, meas_fn, meas_noise, measurement, jac_fn, []))
    return f_nodes


def measurement_fn(means: List[np.ndarray], x_pos_i: float, x_pos_j: float, x_pos_of_measurement: float) -> np.ndarray:
    x_m = x_pos_of_measurement
    x_i = x_pos_i
    x_j = x_pos_j
    y_i = means[0]
    y_j = means[1]
    lam = (x_m - x_i) / (x_j - x_i)
    return (1 - lam) * y_i + lam * y_j


def measurement_fn_jac(means: List[np.ndarray], x_pos_i: float, x_pos_j: float,
                       x_pos_of_measurement: float) -> np.ndarray:
    x_m = x_pos_of_measurement
    x_i = x_pos_i
    x_j = x_pos_j
    gamma = (x_m - x_i) / (x_j - x_i)
    return np.array([(1 - gamma), gamma])


def generate_measurement_factors(v_nodes: List[VariableNode], measurement_generator,
                                 num_measurements: int = 10) -> Tuple[List[FactorNode], List[np.ndarray]]:
    f_nodes = []
    gen_meas = []
    for i in range(num_measurements):
        measurement_x_pos, height_measurement = measurement_generator()
        idx_var_node = int(measurement_x_pos * (len(v_nodes) - 1))

        adj_vars = [v_nodes[idx_var_node], v_nodes[idx_var_node + 1]]
        meas_fn = measurement_fn
        meas_noise = np.array([0.00004])
        jac_fn = measurement_fn_jac
        f_nodes.append(FactorNode(adj_vars, meas_fn, meas_noise, height_measurement, jac_fn,
                                  [v_nodes[idx_var_node].x_pos, v_nodes[idx_var_node + 1].x_pos, measurement_x_pos]))
        gen_meas.append(np.array([measurement_x_pos, height_measurement]))

    return f_nodes, gen_meas


def generate_measurement_line():
    height_measurement = 0.7 + np.random.random() * 0.1
    x_pos = np.random.random()
    return x_pos, height_measurement


def generate_measurement_step():
    height_measurement = np.random.random() * 0.1
    x_pos = np.random.random()
    if x_pos > 0.5:
        height_measurement += 0.5
    return x_pos, height_measurement


def generate_measurement_rect():
    height_measurement = np.random.random() * 0.05
    x_pos = np.random.random()
    if x_pos > 0.33 and x_pos < 0.66:
        height_measurement += 0.5
    return x_pos, height_measurement


# ----------------------------------- PUTTING ALL TOGETHER -----------------------------
if __name__ == "__main__":
    num_var = 30
    num_measurements = 20
    variable_nodes = generate_variable_nodes(num_var, 1)
    factor_nodes, measurements = generate_measurement_factors(variable_nodes, generate_measurement_step,
                                                              num_measurements)
    factor_nodes.extend(generate_smoothing_factors(variable_nodes))

    factor_graph = FactorGraph(variable_nodes, factor_nodes)

    num_iters = 100
    viz = ContourFittingViz(variable_nodes, measurements, num_iters)

    for iter in range(num_iters):
        print("iteration: " + str(iter))
        factor_graph.synchronous_iteration()
        viz.add_iteration(variable_nodes)
    viz.render()
