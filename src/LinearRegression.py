class LinearRegression:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.mean_sqr_err = 0

    def fit(self,X,Y):
        n = len(X)
        alpha = 0.001

        a = 0
        b = 0


        epochs = 10000
        for i in range(epochs):
            Y_pred = list(map(lambda x: a+b*x, X))

            error = list()
            for k in range(n):
                error.append(Y_pred[k]-Y[k])

            mean_sqr_err = 0
            for e in error:
                mean_sqr_err += pow(e,2)
            mean_sqr_err = mean_sqr_err/n

            X_error = list()
            for k in range(n):
                X_error.append(error[k]*X[k])

            a = a - alpha*2*sum(error)/n
            b = b - alpha*2*sum(X_error)/n

            # if i%(epochs/10) == 0:
            #     print('Error: '+str(mean_sqr_err))


        # print('Error: '+str(mean_sqr_err))

        self.a = a
        self.b = b
        self.mean_sqr_err =  mean_sqr_err

    def predict(self, x):
        return self.a+self.b*x
