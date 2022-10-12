import sys
from typing import List, Callable, Tuple, Union, Any
import numpy as np
from copy import deepcopy


class GaussianState:
    __doc__ = "This class holds a possibly multi dimensional state in canonical form"

    def __init__(self, dimensionality: int):
        """
        Initialize a gaussian state
        :param dimensionality: number of dimensions of the state
        :param eta: canonical form of mean
        :param lam: canonical form of the covariance matrix
        """
        self.dim = dimensionality
        self.eta = np.matrix(np.zeros(self.dim))
        self.lam = np.zeros([self.dim, self.dim])

    def set_values(self, mu: np.matrix, sigma: np.matrix):
        """
        Sets and converts values from moment form to canonical form
        :param mu: mean
        :param sigma: covariance
        """
        self.lam = np.linalg.inv(sigma)
        self.eta = mu @ self.lam

    def get_values(self):
        """
        Return values in moment form
        :return: mean, cov
        """
        return np.linalg.inv(self.lam) @ self.eta.T, np.linalg.inv(self.lam)


class VariableNode:
    __doc__ = "Represents a gaussian distributed multi dimensional random variable in a factor graph."
    idx_counter = 0

    def __init__(self, dimensions: int, prior: GaussianState = None):
        """
        Initialize the belief and prior with gaussian states
        :param dimensions: the dimensions of the gaussian state
        :param prior: a prior of the variable
        """
        self.idx = VariableNode.idx_counter
        VariableNode.idx_counter += 1
        if prior is None:
            self.belief = GaussianState(dimensions)
            self.prior = GaussianState(dimensions)
        else:
            self.belief = deepcopy(prior)
            self.prior = deepcopy(prior)
        self.dimensions = dimensions
        self.adj_factors_idx = []  # will be filled by Factors on creation
        self.factor_nodes = []  # will be filled at the end by the FactorGraph

        self.mu = np.zeros(dimensions)  # for debug/output purpose
        self.sigma = np.zeros([dimensions, dimensions])  # for debug/output purpose

    def update_belief(self):
        """
        Updates the belief of a variable node & sends a message to all adjacent factors
        """
        eta = self.prior.eta.copy()
        lam = self.prior.lam.copy()
        for factor_idx in self.adj_factors_idx:
            factor = self.factor_nodes[factor_idx]
            eta_message, lam_message = factor.get_message_for(self.idx)
            eta += eta_message
            lam += lam_message

        # Ensure that matrix is positive-semi-definite
        lam = (lam + lam.T) / 2.
        lam -= np.identity(lam.shape[0]) * 1e-6

        self.belief.eta = eta
        self.belief.lam = lam
        if np.linalg.det(self.belief.lam) != 0:
            self.sigma = np.linalg.inv(self.belief.lam)  # Just for debugging/output
            self.mu = self.sigma @ self.belief.eta.T  # Just for debugging/output

        # Send message with updated belief to adjacent factors
        for factor_idx in self.adj_factors_idx:
            factor = self.factor_nodes[factor_idx]
            eta_message, lam_message = factor.get_message_for(self.idx)
            factor.receive_message_from(self.idx, eta - eta_message, lam - lam_message)


class FactorNode:
    __doc__ = "Factor node modelling the dependencies between variable nodes as a gaussian distribution."
    idx_counter = 0

    def __init__(self, adj_variable_nodes: List[VariableNode],
                 measurement_fn: Callable[[List[np.matrix], Any], np.matrix],
                 measurement_noise: np.matrix,
                 measurement: Union[np.matrix, float],
                 jacobian_fn: Callable[[List[np.matrix], Any], np.matrix],
                 huber_energy: bool,
                 args: Any):
        """
        Initialize internal variables & adds itself to all adjacent variable nodes
        :param adj_variable_nodes: all variable nodes, which are adjacent to this factor node
        :param measurement_fn: the measurement function
        :param measurement_noise: gaussian covariance matrix representing measurement noise
        :param measurement: the actual measurement
        :param jacobian_fn: the jacobian of the measurement function
        :param args: any additional args for the measurement/jacobian function
        """
        self.idx = FactorNode.idx_counter
        FactorNode.idx_counter += 1
        self.adj_variable_node_idxs = [v.idx for v in adj_variable_nodes]
        self.measurement_fn = measurement_fn
        self.measurement_noise = measurement_noise
        self.adaptive_measurement_noise_lam = np.linalg.inv(self.measurement_noise)
        self.measurement = measurement
        self.jacobian_fn = jacobian_fn
        self.args = args
        self.adj_variable_messages = {}
        self.messages_to_adj_variables = {}
        self.linearization_point = []
        self.variable_nodes = []  # will be set by the FactorGraph at the end
        self.huber_energy = huber_energy
        self.huber_mahalanobis_threshold = 0.1

        self.number_of_conditional_variables = 0
        for variable_node in adj_variable_nodes:
            variable_node.adj_factors_idx.append(self.idx)  # bind factor to variable
            self.number_of_conditional_variables += variable_node.dimensions
            self.adj_variable_messages[variable_node.idx] = deepcopy(variable_node.belief)
            self.messages_to_adj_variables[variable_node.idx] = GaussianState(variable_node.dimensions)
            self.linearization_point.append(np.zeros_like(variable_node.belief.eta))

        self.factor_eta = None
        self.factor_lam = None
        self.relinearize()
        self.compute_factor()

    def receive_message_from(self, variable_idx: int, eta_message: np.matrix, lam_message: np.matrix):
        """
        Stores the new variable to factor message for the next iteration
        :param variable_idx: the idx of the variable where the message originated from
        :param eta_message: the eta part of the message
        :param lam_message: the lambda part of the message
        """
        self.adj_variable_messages[variable_idx].lam = lam_message.copy()
        self.adj_variable_messages[variable_idx].eta = eta_message.copy()

    def get_message_for(self, variable_node_idx: int):
        """
        Simple getter function to retrieve the correct message for a given variable node
        :param variable_node_idx: idx of variable, which message should be returned
        :return: eta_message and lam_message
        """
        return self.messages_to_adj_variables[variable_node_idx].eta.copy(), \
               self.messages_to_adj_variables[variable_node_idx].lam.copy()

    def relinearize(self):
        """
        Calculates a new mean of adjacent variables, if possible. This used as the new linearization point.
        """
        linearization_point = []
        for belief in self.adj_variable_messages.values():
            if np.linalg.det(belief.lam) != 0:  # if possible relinearize
                mean = belief.eta @ np.linalg.inv(belief.lam)
                linearization_point.append(mean)  # Linearize around mean of adj. vars
            else:
                linearization_point.append(np.array([0.]))
        self.linearization_point = linearization_point
        self.compute_adaptive_noise()
        self.compute_factor()

    def compute_adaptive_noise(self):
        """
        Computes the adaptive measurement noise if enabled
        """
        if self.huber_energy:
            predicted_measurement = self.measurement_fn(self.linearization_point, *self.args)
            res = self.measurement - predicted_measurement

            mahalanobis_dist = np.linalg.norm(res) / np.sqrt(self.measurement_noise)
            if mahalanobis_dist > self.huber_mahalanobis_threshold:
                self.adaptive_measurement_noise_lam = np.linalg.inv(
                    self.measurement_noise * np.square(mahalanobis_dist) / (2 * (
                            self.huber_mahalanobis_threshold * mahalanobis_dist - 0.5 * np.square(
                        self.huber_mahalanobis_threshold))))
            else:
                self.adaptive_measurement_noise_lam = np.linalg.inv(self.measurement_noise)
        else:
            self.adaptive_measurement_noise_lam = np.linalg.inv(self.measurement_noise)

    def compute_factor(self):
        """
        Computes the factor of the factor node.
        Should be called, when the linearization point changes.
        """
        jacobian = self.jacobian_fn(self.linearization_point, *self.args)
        predicted_measurement = self.measurement_fn(self.linearization_point, *self.args)

        self.factor_eta = np.multiply(jacobian.T @ self.adaptive_measurement_noise_lam, (
                self.measurement - (predicted_measurement - (jacobian @ np.array(self.linearization_point).flatten()))))
        self.factor_eta = self.factor_eta.flatten()

        self.factor_lam = jacobian.T @ self.adaptive_measurement_noise_lam @ jacobian

        # Ensure that matrix is positive-semi-definite
        self.factor_lam = (self.factor_lam + self.factor_lam.T) / 2.
        self.factor_lam += np.identity(self.factor_lam.shape[0]) * 1e-6

    def compute_outgoing_messages(self):
        """
        Computes all factor to variable messages for adjacent variable nodes.
        The results are stored in a class variable

        See this blog post Appendix B for the equations: https://gaussianbp.github.io/
        """
        current_variable_position = 0
        for variable_node_idx in self.adj_variable_node_idxs:
            variable_node = self.variable_nodes[variable_node_idx]
            eta_factor, lam_factor = self.factor_eta.copy(), self.factor_lam.copy()

            # For every node take the product of factor and incoming messages
            current_factor_position = 0
            for other_variable_idx in self.adj_variable_node_idxs:
                other_variables = self.variable_nodes[other_variable_idx]
                if variable_node_idx != other_variable_idx:
                    start = current_factor_position
                    end = current_factor_position + other_variables.dimensions
                    eta_factor[:, start:end] += self.adj_variable_messages[other_variables.idx].eta
                    lam_factor[start:end, start:end] += self.adj_variable_messages[other_variables.idx].lam
                current_factor_position += other_variables.dimensions

            # Marginalization to variable node
            # - First "reorder" variable_nodes's (short a) elements to the top
            cur_dims = variable_node.dimensions
            start = current_variable_position
            end = current_variable_position + cur_dims
            eta_a = eta_factor[:, start:end]  # information vector of variable_node
            eta_b = np.block([eta_factor[:, :start], eta_factor[:, end:]])  # information vector of the rest

            lam_aa = lam_factor[start:end, start:end]
            lam_ab = np.hstack((lam_factor[start:end, :start], lam_factor[start:end, end:]))
            lam_ba = np.vstack((lam_factor[:start, start:end], lam_factor[end:, start:end]))
            lam_bb = np.block([[lam_factor[:start, :start], lam_factor[:start, end:]],
                               [lam_factor[end:, :start], lam_factor[end:, end:]]])

            # - Then marginalize according to https://ieeexplore.ieee.org/document/4020357
            new_message_eta = eta_a - (lam_ab @ np.linalg.inv(lam_bb) @ eta_b.T).T
            new_message_lam = lam_aa - lam_ab @ np.linalg.inv(lam_bb) @ lam_ba

            # Ensure that matrix is positive-semi-definite
            new_message_lam = (new_message_lam + new_message_lam.T) / 2.
            new_message_lam += np.identity(new_message_lam.shape[0]) * 1e-6

            self.messages_to_adj_variables[variable_node_idx].eta = new_message_eta
            self.messages_to_adj_variables[variable_node_idx].lam = new_message_lam

            current_variable_position += variable_node.dimensions


class FactorGraph:
    __doc__ = "Orchestrate the gaussian belief propagation algorithm."

    def __init__(self, variable_nodes: List[VariableNode], factor_nodes: List[FactorNode]):
        self.variable_nodes = variable_nodes
        self.factor_nodes = factor_nodes
        for v in self.variable_nodes:
            v.factor_nodes = self.factor_nodes
        for f in self.factor_nodes:
            f.variable_nodes = self.variable_nodes

    def compute_all_messages(self):
        """
        Calls all factors to update their outgoing messages
        """
        for factor_node in self.factor_nodes:
            factor_node.compute_outgoing_messages()

    def update_all_beliefs(self):
        """
        Calls all variable nodes to update their belief
        """
        for variable_node in self.variable_nodes:
            variable_node.update_belief()

    def relinearize_factors(self):
        """
        Calculates new linearization points for all factors if possible
        """
        for factor in self.factor_nodes:
            factor.relinearize()

    def synchronous_iteration(self):
        """
        Triggers a single synchronous iteration over all nodes (factor and variable nodes)
        """
        self.relinearize_factors()
        self.compute_all_messages()
        self.update_all_beliefs()

    def fit(self):
        """
        Calls synchronous iteration until a convergenz criteria is met or
        """
        for _ in range(1):
            self.synchronous_iteration()
        # ToDo implement me correctly
