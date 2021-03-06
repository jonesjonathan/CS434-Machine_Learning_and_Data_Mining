import numpy as np
import math
import sys
import csv
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

maxPow = (math.log(sys.float_info.max))-0.1
minPow = (math.log(sys.float_info.min))+0.1

def readFile(fileName):
    f = open(fileName, 'r+')
    return csv.reader(f)

#parse csv file and split data into x and y
def parseCSV(path):
    data = readFile(path)
    grayscale = []
    digits = []
    for row in data:
        row = [float(item)*(1.0/255.0) for item in row]
        grayscale.append(row[0:256])
        digits.append(row[-1])
    grayscale = np.array(grayscale)
    digits = np.array(digits)

    return grayscale, digits

#Uses the weight vector from gradient descent to calculate estimated results and compares them with actual
#results. The number of successful comparisons is tallied up and converted into a percentage at the end and returned
def accuracy(X, Y, w):
    success = 0
    n = len(X)
    for i in range(0, n):
        wT = np.multiply(w.T, -1)
        pow = np.dot(wT, X[i])
        if(pow >= maxPow):
            exp = 1
        elif(pow <= minPow):
            exp = 0
        else:
            exp = np.exp(pow)
        result = 1.0 / (1.0 + exp)

        #round results to either 0 or 1
        if round(result, 0) == Y[i]:
            success = success + 1
        return ((float(success) / float(n)) * 100)

def main():
    itr = 20 #iterate 20 times
    lmb = sys.argv[3]
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    learn = 0.01

    
    trGrayscale, trDigits = parseCSV(arg1)
    teGrayscale, teDigits = parseCSV(arg2)


    trainingAccuracy = []
    testingAccuracy = []
   
    for f in range(1, itr):
        n = len(trGrayscale)
        w = np.array([])
        # a single iteration
        for i in range(f):
            gradient = np.array([])
            for k in range(0, n):
                wT = np.multiply(w.T, -1)
                pow = np.dot(wT, trGrayscale[k]) if len(w) else np.multiply(-1, np.sum(trGrayscale[k]))
                if(pow >= maxPow):
                    exp = 1
                elif(pow <= minPow):
                    exp = 0
                else:
                    exp = np.exp(pow)
                result = 1.0 / (1.0 + exp)
                gradient = gradient + (trGrayscale[k] * np.subtract(result, trDigits[k])) if len(gradient) else (trGrayscale[k] * np.subtract(result, trDigits[k]))
            w = np.subtract(w, learn * gradient) if len(w) else learn*gradient
    
        # store training accuracy at specific lambda
        trainingAccuracy.append(accuracy(trGrayscale, trDigits, w))
        testingAccuracy.append(accuracy(teGrayscale, teDigits, w))

    #plot results
    x = np.arange(1, itr)
    plt.xlabel('Iterations')
    plt.ylabel('Accuracy')
    plt.title("Accuracy vs Iterations with Lambda = " + str(lmb))
    plt.plot(x, trainingAccuracy, 'b-', label="Training")
    plt.plot(x, testingAccuracy, 'r-', label="Testing")
    plt.legend()
    plt.savefig('q2_3-PLOT-lmb' + str(lmb).replace('.', ''))

main()