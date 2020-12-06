from LinearRegression import LinearRegression
from LogRegression import LogRegression
from sklearn.linear_model import LogisticRegression

import pandas as pd
from ReadDF import readDF_Log



class ChanceModel:
    def __init__(self, margin_mapping):
        self.margin_mapping = margin_mapping
        self.reg = LogisticRegression()
        self.reg = LinearRegression()

    def getChance(self, margin):
        if margin not in self.margin_mapping.keys():
            return 0

        return self.margin_mapping[margin].getWinFraction()

    def getChanceLinear(self, margin):
        return self.reg.predict(margin)

    def getChanceLog(self, X):
        return self.reg.predict_log_proba(X)

    def fitRegression(self):
        x_list = list()
        y_list = list()

        for key,value in self.margin_mapping.items():
            x_list.append(key)
            y_list.append(value.getWinFraction())

        self.reg.fit(x_list,y_list)
