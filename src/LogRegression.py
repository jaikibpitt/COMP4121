import numpy as np
import pandas as pd
from numpy import exp

class LogRegression:
    def __init__(self):
        self.w = None
        self.X = None
        self.Y = None
        self.alpha = 0.001
        self.epochs = 10000

        self.observations = None
        self.features = None

    def fit(self, X, Y):
        self.observations, self.features = X.shape

        self.w = np.zeros(self.features)
        self.X = X
        self.Y = Y

        for i in range(self.epochs):
            self.update_weights()

    def predict(self):
          z = np.dot(self.X, self.w)
          sigmoid = 1.0 / (1 + np.exp(-z))
          return sigmoid

    def cost_function(self):
        predictions = self.predict()

        #Take the error when label=1
        class1_cost = -self.Y*np.log(predictions)

        #Take the error when label=0
        class2_cost = (1-self.Y)*np.log(1-predictions)

        #Take the sum of both costs
        cost = class1_cost - class2_cost

        #Take the average cost
        cost = cost.sum() / self.observations

        return cost

    def update_weights(self):
        N = len(self.X)

        #1 - Get Predictions
        predictions = self.predict()

        #2 Transpose features from (200, 3) to (3, 200)
        # So we can multiply w the (200,1)  cost matrix.
        # Returns a (3,1) matrix holding 3 partial derivatives --
        # one for each feature -- representing the aggregate
        # slope of the cost function across all observations
        gradient = np.dot(self.X.T,  predictions - self.Y)

        #3 Take the average cost derivative for each feature
        gradient /= N

        #4 - Multiply the gradient by our learning rate
        gradient *= self.alpha

        #5 - Subtract from our weights to minimize cost
        self.w -= gradient
