import numpy
from enum import Enum
import random
import math

class Methods(Enum):
    DIRECT_LINEAR_REGRESSION = 0
    GRADIENT_LOGISTIC_REGRESSION = 1
    SVM = 2


class MLModel:
    def __init__(self, X, Y, method=Methods.DIRECT_LINEAR_REGRESSION, learningRate=0.3, epochs=10000, epsilon=0.0000001):
        self.__method = method
        self.__X = X
        self.__Y = Y
        match self.__method:
            case Methods.DIRECT_LINEAR_REGRESSION:
                self.__w = self.getDLRWeights()
            case Methods.GRADIENT_LOGISTIC_REGRESSION:
                self.__w = self.getGLRWeights(learningRate, epochs, epsilon)
            case Methods.SVM:
                self.__w = self.getSVMWeights()

    def getDLRWeights(self):
        XwBias = numpy.append(numpy.ones((self.__X.shape[0], 1)), self.__X, axis = 1)
        w = numpy.linalg.inv((XwBias.T) @ XwBias) @ (XwBias.T) @ self.__Y
        return w

    def getGLRWeights(self, learningRate, epochs, epsilon):
        m = numpy.mean(self.__X, axis=0, keepdims=True)
        s = numpy.std(self.__X, axis=0, ddof=1, keepdims=True)
        XZscored = (self.__X - m)/s
        XwBiasZscored = numpy.append(numpy.ones((XZscored.shape[0], 1)), XZscored, axis = 1)
        
        w = []
        for i in range(XwBiasZscored.shape[1]):
            temp = numpy.array([[random.uniform(-0.0001, 0.0001)]], dtype=float)
            if len(w) == 0:
                w = temp
            else:
                w = numpy.append(w, temp, axis = 0)

        Yhat = 1/(1 + math.e**(-(XwBiasZscored @ w)))
        for i in range(epochs):
            dJdw = (1 / self.__Y.shape[0]) * ((XwBiasZscored.T) @ (Yhat - self.__Y))
            w = w - (learningRate * dJdw)
            Yhat = 1/(1 + math.e**(-(XwBiasZscored @ w)))

        return w

    def getSVMWeights(self):
        m = numpy.mean(self.__X, axis=0, keepdims=True)
        s = numpy.std(self.__X, axis=0, ddof=1, keepdims=True)
        XZscored = (self.__X - m)/s
        XwBiasZscored = numpy.append(numpy.ones((XZscored.shape[0], 1)), XZscored, axis = 1)
        YNegPos = 2 * self.__Y - 1
        alpha = numpy.linalg.pinv(numpy.diag(YNegPos.T[0]) @ XwBiasZscored @ (XwBiasZscored.T) @ numpy.diag(YNegPos.T[0])) @ numpy.ones((XwBiasZscored.shape[0], 1))
        w = (XwBiasZscored.T) @ numpy.diag(YNegPos.T[0]) @ alpha
        return w

    def score(self, X):
        match self.__method:
            case Methods.DIRECT_LINEAR_REGRESSION:
                return self.directLinearRegression(X)
            case Methods.GRADIENT_LOGISTIC_REGRESSION:
                return self.gradientLogisticRegression(X)
            case Methods.SVM:
                return self.SVM(X)

    def directLinearRegression(self, X):
        XwBias = numpy.append(numpy.ones((X.shape[0], 1)), X, axis = 1)
        Yhat = XwBias @ self.__w
        return Yhat

    def gradientLogisticRegression(self, X):
        m = numpy.mean(X, axis=0, keepdims=True)
        s = numpy.std(X, axis=0, ddof=1, keepdims=True)
        XZscored = (X - m)/s
        XwBiasZscored = numpy.append(numpy.ones((XZscored.shape[0], 1)), XZscored, axis = 1)
        Yhat = 1/(1 + math.e**(-(XwBiasZscored @ self.__w)))
        return Yhat

    def SVM(self, X):
        m = numpy.mean(X, axis=0, keepdims=True)
        s = numpy.std(X, axis=0, ddof=1, keepdims=True)
        XZscored = (X - m)/s
        XwBiasZscored = numpy.append(numpy.ones((XZscored.shape[0], 1)), XZscored, axis = 1)
        Yhat = XwBiasZscored @ self.__w
        return Yhat


if __name__ == "__main__":
    X_TEST = numpy.array([[0,1,3],[8,1,1],[0,4,3],[1,2,2],[9,3,0]], dtype=float)
    Y_TEST = numpy.array([[1],[0],[1],[0],[0]], dtype=int)

    # Direct Linear Regression
    model = MLModel(X_TEST, Y_TEST, Methods.DIRECT_LINEAR_REGRESSION)
    Yhat = model.score(X_TEST)
    print("Yhat:", Yhat.shape)
    print(Yhat)
    print()
    print("Y_TEST:", Y_TEST.shape)
    print(Y_TEST)
    print()

    # Gradient Logistic Regression
    model = MLModel(X_TEST, Y_TEST, Methods.GRADIENT_LOGISTIC_REGRESSION)
    Yhat = model.score(X_TEST)
    print("Yhat:", Yhat.shape)
    print(Yhat)
    print()
    print("Y_TEST:", Y_TEST.shape)
    print(Y_TEST)
    print()

    # SVM
    model = MLModel(X_TEST, Y_TEST, Methods.SVM)
    Yhat = model.score(X_TEST)
    print("Yhat:", Yhat.shape)
    print(Yhat)
    print()
    print("Y_TEST:", Y_TEST.shape)
    print(Y_TEST)
    print()