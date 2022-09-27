from typing import List
import numpy as np


class GaussianState:
    __doc__ = "This class holds a possibly multi dimensional state in canonical form"

    def __init__(self, dimensionality: int, eta: np.ndarray = None, lam: np.ndarray = None):
        """
        Initialize a gaussian state
        :param dimensionality: number of dimensions of the state
        :param eta: canonical form of mean
        :param lam: canonical form of the covariance matrix
        """
        self.dim = dimensionality
        if eta is not None and len(eta) == self.dim:
            self.eta = eta
        else:
            self.eta = np.zeros(self.dim)

        if lam is not None and lam.shape == (self.dim, self.dim):
            self.lam = lam
        else:
            self.lam = np.zeros([self.dim, self.dim])


class VariableNode:
    __doc__ = "Represents a gaussian distributed multi dimensional random variable in a factor graph."

    def __init__(self, dimensions: int, idx: int):
        """
        Initialize the belief and prior with gaussian states
        :param dimensions: the dimensions of the gaussian state
        :param idx: an id unique over all variable nodes.
        """
        self.idx = idx
        self.belief = GaussianState(dimensions)
        self.prior = GaussianState(dimensions)
        self.dimensions = dimensions
        self.adj_factors = []  # will be filled by Factors on creation

        self.mu = np.zeros(dimensions)  # for debug/output purpose
        self.sigma = np.zeros([dimensions, dimensions])  # for debug/output purpose

    def update_belief(self):
        """
        Updates the belief of a variable node & sends a message to all adjacent factors
        """
        eta = self.prior.eta.copy()
        lam = self.prior.lam.copy()
        for factor in self.adj_factors:
            eta_message, lam_message = factor.get_message_for(self)
            eta += eta_message
            lam += lam_message

        self.belief.eta = eta
        self.belief.lam = lam
        self.sigma = np.linalg.inv(self.belief.lam)  # Just for debugging/output
        self.mu = self.sigma @ self.belief.eta  # Just for debugging/output

        # Send message with updated belief to adjacent factors
        for factor in self.adj_factors:
            eta_message, lam_message = factor.get_message_for(self)
            factor.receive_message_from(self.idx, eta - eta_message, lam - lam_message)


class FactorNode:
    __doc__ = "Factor node modelling the dependencies between variable nodes as a gaussian distribution."

    def __init__(self, factor: GaussianState, adj_variable_nodes: List[VariableNode]):
        """
        Initialize internal variables & adds itself to all adjacent variable nodes
        :param factor: The gaussian factor of this factor node. Has to have the same dim. as all adj. variable nodes
        :param adj_variable_nodes: all variable nodes, which are adjacent to this factor node
        """
        self.factor = factor
        self.adj_variable_nodes = adj_variable_nodes
        self.adj_variable_messages = {}
        self.messages_to_adj_variables = {}

        number_of_conditional_variables = 0  # just as a sanity check
        for variable_node in self.adj_variable_nodes:
            variable_node.adj_factors.append(self)  # bind factor to variable
            number_of_conditional_variables += variable_node.dimensions
            self.adj_variable_messages[variable_node.idx] = variable_node.belief
            self.messages_to_adj_variables[variable_node.idx] = GaussianState(variable_node.dimensions)

        assert (self.factor.dim == number_of_conditional_variables)

    def receive_message_from(self, variable_idx: int, eta_message: np.ndarray, lam_message: np.ndarray):
        """
        Stores the new variable to factor message for the next iteration
        :param variable_idx: the idx of the variable where the message originated from
        :param eta_message: the eta part of the message
        :param lam_message: the lambda part of the message
        """
        self.adj_variable_messages[variable_idx].lam = lam_message
        self.adj_variable_messages[variable_idx].eta = eta_message

    def get_message_for(self, variable_node: VariableNode):
        """
        Simple getter function to retrieve the correct message for a given variable node
        :param variable_node: message from this factor to variable_node
        :return: eta_message and lam_message
        """
        return self.messages_to_adj_variables[variable_node.idx].eta, self.messages_to_adj_variables[
            variable_node.idx].lam

    def compute_outgoing_messages(self):
        """
        Computes all factor to variable messages for adjacent variable nodes.
        The results are stored in a class variable

        See this blog post Appendix B for the equations: https://gaussianbp.github.io/
        """
        current_variable_position = 0
        for variable_node in self.adj_variable_nodes:
            eta_factor, lam_factor = self.factor.eta.copy(), self.factor.lam.copy()

            # For every node take the product of factor and incoming messages
            current_factor_position = 0
            for other_variables in self.adj_variable_nodes:
                if variable_node != other_variables:
                    start = current_factor_position
                    end = current_factor_position + other_variables.dimensions
                    eta_factor[start:end] += self.adj_variable_messages[other_variables.idx].eta
                    lam_factor[start:end, start:end] += self.adj_variable_messages[other_variables.idx].lam
                current_factor_position += other_variables.dimensions

            # Marginalization to variable node
            # - First "reorder" variable_nodes's elements to the top
            cur_dims = variable_node.dimensions
            start = current_variable_position
            end = current_variable_position + cur_dims
            eta_a = eta_factor[start:end]  # information vector of variable_node
            eta_b = np.concatenate((eta_factor[:start], eta_factor[end:]))  # information vector of the rest

            lam_aa = lam_factor[start:end, start:end]
            lam_ab = np.hstack((lam_factor[start:end, :start], lam_factor[start:end, end:]))
            lam_ba = np.vstack((lam_factor[:start, start:end], lam_factor[end:, start:end]))
            lam_bb = np.block([[lam_factor[:start, :start], lam_factor[:start, end:]],
                               [lam_factor[end:, :start], lam_factor[end:, end:]]])

            # - Then marginalize according to https://ieeexplore.ieee.org/document/4020357
            new_message_eta = eta_a - lam_ab @ np.linalg.inv(lam_bb) @ eta_b
            new_message_lam = lam_aa - lam_ab @ np.linalg.inv(lam_bb) @ lam_ba
            self.messages_to_adj_variables[variable_node.idx].eta = new_message_eta
            self.messages_to_adj_variables[variable_node.idx].lam = new_message_lam

            current_variable_position += variable_node.dimensions


class FactorGraph:
    __doc__ = "Orchestrate the gaussian belief propagation algorithm."

    def __init__(self, variable_nodes: List[VariableNode], factor_nodes: List[FactorNode]):
        self.variable_nodes = variable_nodes
        self.factor_nodes = factor_nodes

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

    def synchronous_iteration(self):
        """
        Triggers a single synchronous iteration over all nodes (factor and variable nodes)
        """
        self.compute_all_messages()
        self.update_all_beliefs()
