import numpy as np


class ClassifierSimulator:
    def __init__(self, probability=0.7, neightbour=0.25, ground_truth=0, num_classes=3):
        self.num_classes = num_classes
        self.probability = probability  # probability of correct classification
        self.neighbour = neightbour  # probability of a similar class
        self.ground_truth = ground_truth
        self.measurement_model = self.__generate_measurement_model()

    def __generate_measurement_model(self):
        """
        Generates the pmf of the class distribution
        """
        meas_model = np.ones(self.num_classes)
        for i in range(self.num_classes):
            if i == self.ground_truth:
                meas_model[i] = self.probability
            elif i == (self.ground_truth + self.num_classes // 2) % self.num_classes:
                meas_model[i] = self.neighbour
            else:
                meas_model[i] = (1 - (self.probability + self.neighbour)) / (
                        self.num_classes - 2
                )
        return meas_model

    def generate_measurement(self):
        """
        Selects randomly a measurement from the measurement_model
        """
        measurement = np.zeros(self.num_classes)
        measurement_idx = np.random.choice(
            range(self.num_classes), 1, p=self.measurement_model
        )[0]
        measurement[measurement_idx] += 1
        return measurement
