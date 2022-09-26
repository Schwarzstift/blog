import numpy as np
import math


class DirichletFilter:
    def __init__(self, num_classes=3, measurement_period=0.05):
        self.num_classes = num_classes
        self.measurement_period = measurement_period  # average time between two measurements
        self.decay_factor = 0.95  # how much does the dirichlet distribution forget over time
        self.state = np.ones(num_classes) / num_classes  # uniform distribution as prior
        self.alpha = np.ones(num_classes)  # count values of the Dirichlet distribution

    def estimate_state(self):
        self.estimate_state_using_mean()

    def update(self, measurement):
        self.alpha += measurement
        self.estimate_state()

    def predict(self, time_delta):
        time_factor = time_delta / self.measurement_period
        self.alpha = self.alpha * (self.decay_factor ** time_factor)
        self.alpha = np.maximum(self.alpha, np.ones(self.num_classes))
        self.estimate_state()

    def merge(self, other):
        return self.merge_average(other)

    def calc_weights(self):
        return self.state * self.log_likelihood()

    def log_likelihood(self):
        return (
                math.lgamma(np.sum(self.alpha))
                + np.sum((self.alpha - 1) * (np.log(self.state)))
                - np.sum(np.array([math.lgamma(i) for i in self.alpha]))
        )

    def estimate_state_using_mean(self):
        self.state = self.alpha / np.sum(self.alpha)

    def estimate_state_using_mode(self):
        self.state = (self.alpha - 1) / (np.sum(self.alpha) - self.num_classes)

    def merge_average(self, other):
        merged_dirichlet = DirichletFilter()
        merged_dirichlet.alpha = (self.alpha + other.alpha) / 2.0
        merged_dirichlet.estimate_state()
        return merged_dirichlet

    def merge_addition(self, other):
        merged_dirichlet = DirichletFilter()
        merged_dirichlet.alpha = (self.alpha + other.alpha) / 2.0
        merged_dirichlet.estimate_state()
        return merged_dirichlet
