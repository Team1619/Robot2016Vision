import copy


class Stabilizer:

    def __init__(self, sampleSize, threshold=0):
        self.sampleSize = sampleSize
        self.data = []
        self.threshold = threshold

    def push(self, value):
        if len(self.data) >= self.sampleSize:
            self.data.pop(0)
            self.data.append(value)
            return True
        else:
            self.data.append(value)
            return False

    def reset(self):
        self.data = []

    def get(self):
        dataLength = len(self.data)
        if dataLength is 0:
            return 0
        elif dataLength > 4:
            self.removeOutlier()
        return self.average()

    def removeOutlier(self):
        sortedData = self.data[:]
        sortedData.sort()
        
        dataLength = len(sortedData)
        lowerDifference = sortedData[1] - sortedData[0]
        higherDifference = sortedData[dataLength - 1] - sortedData[dataLength - 2]
        
        if lowerDifference > higherDifference and lowerDifference >= self.threshold:
            self.data.remove(sortedData[0])
        else:
            self.data.remove(sortedData[dataLength - 1])

    def average(self):
        return sum(self.data) / len(self.data) 
