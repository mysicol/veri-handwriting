import numpy
from enum import Enum
import random
import math
import os
from PIL import Image
import pickle

class Methods(Enum):
    DIRECT_LINEAR_REGRESSION = 0
    GRADIENT_LOGISTIC_REGRESSION = 1
    SVM = 2

def makeModels(imgdir, method=Methods.DIRECT_LINEAR_REGRESSION):
    MESSY = 0
    NEAT = 1

    datasets = {"a": [], "b": [], "c": [], "d": [], "e": [], "f": [], "g": [], "h": [],
                "i": [], "j": [], "k": [], "l": [], "m": [], "n": [], "o": [], "p": [],
                "q": [], "r": [], "s": [], "t": [], "u": [], "v": [], "w": [], "x": [],
                "y": [], "z": []}
    
    for filename in os.listdir(imgdir):
        parts = filename.split('.')
        im = Image.open(imgdir + "/" + filename)
        im = im.resize((40,40))
        im = numpy.array([im.getdata()], dtype=numpy.float64)
        im = im.reshape(-1, im.shape[1])
        im = im.flatten()
        im = numpy.array([im], dtype=numpy.float64)
        if parts[1] == "messy":
            im = [numpy.append(im[0], [MESSY], axis = 0)]
        else:
            im = [numpy.append(im[0], [NEAT], axis = 0)]
        if len(datasets[parts[0][0]]) == 0:
            datasets[parts[0][0]] = im
        else:
            datasets[parts[0][0]] = numpy.append(datasets[parts[0][0]], im, axis = 0)

    models = {}
    for letter in datasets:
        X = datasets[letter][:,:-1]
        Y = datasets[letter][:,[-1]]
        models[letter] = MLModel(X, Y, method)
    
    with open('weights.pkl', 'wb') as f:
        pickle.dump(models, f)
    
    print("Written successfully!")

class MLModel:
    def __init__(self, X, Y, method, learningRate=0.3, epochs=10000, epsilon=0.0000001):
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
        w = numpy.linalg.pinv((XwBias.T) @ XwBias) @ (XwBias.T) @ self.__Y
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