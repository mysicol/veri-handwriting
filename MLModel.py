import numpy
from enum import Enum

class Methods(Enum):
    DIRECT_LINEAR_REGRESSION = 0
    GRADIENT_LINEAR_REGRESSION = 1
    DIRECT_LOGISTIC_REGRESSION = 2
    GRADIENT_LOGISTIC_REGRESSION = 3
    SVM = 4
    KNN = 5


class MLModel:
    MESSY = 0
    NEAT = 1

    def __init__(self, X, Y, method=Methods.DIRECT_LINEAR_REGRESSION):
        self.__method = method
        self.__X = X
        self.__Y = Y
        match method:
            case Methods.DIRECT_LINEAR_REGRESSION:
                self.__w = self.getDLRWeights()
            case Methods.GRADIENT_LINEAR_REGRESSION:
                None
            case Methods.DIRECT_LOGISTIC_REGRESSION:
                None
            case Methods.GRADIENT_LOGISTIC_REGRESSION:
                None
            case Methods.SVM:
                None
            case Methods.KNN:
                None

    def getDLRWeights(self):
        XwBias = numpy.append(numpy.ones((self.__X.shape[0], 1)), self.__X, axis = 1)
        w = numpy.linalg.inv((XwBias.T) @ XwBias) @ (XwBias.T) @ self.__Y
        return w

    def score(self, X):
        match self.__method:
            case Methods.DIRECT_LINEAR_REGRESSION:
                return self.directLinearRegression(X)
            case Methods.GRADIENT_LINEAR_REGRESSION:
                None
            case Methods.DIRECT_LOGISTIC_REGRESSION:
                None
            case Methods.GRADIENT_LOGISTIC_REGRESSION:
                None
            case Methods.SVM:
                None
            case Methods.KNN:
                None

    def directLinearRegression(self, X):
        XwBias = numpy.append(numpy.ones((X.shape[0], 1)), X, axis = 1)
        Yhat = XwBias @ self.__w
        return Yhat

# Gradient Linear Regression
def gradientLinearRegression(X, Y):
    None

# Direct Logistic Regression
def directLogisticRegression(X, Y):
    None

# Gradient Logistic Regression
def gradientLogisticRegression(X, Y):
    None

# SVM
def svm(X, Y):
    None

# KNN
def knn(X, Y):
    None

if __name__ == "__main__":
    X_TEST = numpy.array([[0,1,3],[8,1,1],[0,4,3],[1,2,2],[9,3,0]], dtype=float)
    Y_TEST = numpy.array([[1],[0],[1],[0],[0]], dtype=int)

    model = MLModel(X_TEST, Y_TEST)
    Yhat = model.score(X_TEST)
    print("Yhat:", Yhat.shape)
    print(Yhat)
    print()
    print("Y_TEST:", Y_TEST.shape)
    print(Y_TEST)
    print()