import operator;
import numpy;
import matplotlib.pyplot as plt;

def file2matrix(filename) :
    labelIndexDict = {"largeDoses" : 1, "smallDoses" : 2, "didntLike" : 3, "1" : 1, "2" : 2, "3" : 3}
    fr = open(filename)
    lines = fr.readlines()
    numberOfLines = len(lines)
    fr.close()
    returnMat  = numpy.zeros((numberOfLines, 3))
    classLabelVetctor = []
    index = 0
    for line in lines :
        line = line.strip()
        listFromLine = line.split('\t');
        returnMat[index, : ] = listFromLine[0:3];
        classLabelVetctor.append(labelIndexDict[listFromLine[-1]])
        index += 1
    return returnMat, classLabelVetctor

def normlize(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    m = dataSet.shape[0]
    ranges = maxVals - minVals
    normDataSet = dataSet - numpy.tile(minVals, (m, 1))
    normDataSet = normDataSet / numpy.tile(ranges, (m, 1))
    return normDataSet, ranges, minVals

def plotFigure(dataSet, labels):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(dataSet[:, 0], dataSet[:, 1], 15.0 * numpy.array(labels),
               15.0 * numpy.array(labels))
    plt.show()

def classify0(InX, dataSet, labels, k):
    m = dataSet.shape[0]
    diffMat = dataSet - numpy.tile(InX, (m, 1))
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis = 1)
    distances = sqDistances ** 0.5
    sortedDistIndices = distances.argsort()
    classCount = {}
    for i in range(k) :
        classLabel = labels[sortedDistIndices[i]]
        classCount[classLabel] = classCount.get(classLabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]

def datingClassTest():
    testRatio = 0.1
    datingDataMat, datingLabels = file2matrix(
        "/Users/songjianzhang/Code/machinelearninginaction/Ch02/datingTestSet.txt")
    testDatingDataMat, testDatingLabels = file2matrix("/Users/songjianzhang/Code/machinelearninginaction/Ch02/datingTestSet.txt")
    normDatingDataMat, ranges, minVals = normlize(datingDataMat)
    testNormDatingDataMat, testRanges, testMinVals = normlize(testDatingDataMat)
    sum = int(len(testDatingLabels) * testRatio)
    errorCount = 0
    for i in range(sum) :
        label = classify0(testNormDatingDataMat[i, : ], normDatingDataMat, datingLabels, 5)
        if label != testDatingLabels[i]:
            errorCount += 1
    errorRate = float(errorCount) / sum
    print("Error rate is %f" % errorRate)




if __name__ == '__main__' :
    datingClassTest()



