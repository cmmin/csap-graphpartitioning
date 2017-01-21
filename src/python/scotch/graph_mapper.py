import os
import os.path

import scotch.scotch as sl
import scotch.io as sio

import graphs.metisgraph as mg

'''
Usage:



# Load graph data
metisGraph = MetisGraph(...)

scotchData = ScotchGraphArrays()
scotchData.fromMetisGraph(metisGraph)

pathToSCOTCHLib = "..."
mapper = GraphMapper(pathToSCOTCHLib)

# change here default strategy options

mapper.initArchitecture()
mapper.initStrategy()
mapper.loadGraph(scotchData)

mapper.graphMap()


'''

def partitionMetis(libraryPath, metisFilePath):
    metisGraph = mg.MetisGraph(metisFilePath)
    metisGraph.printData()

    scotchData = sio.ScotchGraphArrays()
    scotchData.fromMetisGraph(metisGraph)

    mapper = GraphMapper(libraryPath)
    ok = mapper.initArchitecture()
    print("Architecture =", ok)

    ok = mapper.initStrategy()
    print("Strategy =", ok)

    ok = mapper.loadGraph(scotchData)
    print("Graph =", ok)

    ok = mapper.graphMap()
    print("Mapped =", ok)

    return mapper


def isValidScotchData(data):
    return isinstance(data, sio.ScotchGraphArrays)

class GraphMapper:
    def __init__(self, scotchLibPath = None, numPartitions = 10, kbalval = 0.1, strategyFlag = 1, strategyOptions = ''):
        self.scotchLib = None
        self.scotchData = None

        self.scotchLibPath = scotchLibPath

        self.numPartitions = numPartitions
        self.kbalval = kbalval
        self.strategyFlag = strategyFlag
        self.strategyOptions = strategyOptions

        self.loadLibrary(self.scotchLibPath)

    def isInitialized(self):
        if self.scotchLib is None:
            return False
        if self.scotchLib.architecture is None:
            return False
        if self.scotchLib.strategy is None:
            return False
        if self.scotchLib.graph is None:
            return False
        return False

    def loadLibrary(self, scotchLibPath):
        lib = sl.LibScotch(self.scotchLibPath)
        if(lib.isLoaded()):
            self.scotchLib = lib
            self.scotchLibPath = scotchLibPath
            return True
        return False

    def initArchitecture(self):
        if self.scotchLib.isLoaded():
            ok = self.scotchLib.createSCOTCHArch()
            if ok == False:
                return False
            ok = self.scotchLib.populatePartitionArchitecture(self.numPartitions)
            return ok
        return False

    def initStrategy(self):
        if self.scotchLib.isLoaded():
            #self.numPartitions = numPartitions
            ok = self.scotchLib.createStrategy()
            if ok == False:
                return False
            ok = self.scotchLib.setStrategyGraphMapBuild(self.strategyFlag, self.numPartitions, self.kbalval)
            if ok == False:
                return False
            ok = self.scotchLib.setStrategyFlags(self.strategyOptions)
            if ok == False:
                return False
            return True
        return False

    def loadGraph(self, scotchData):
        if isValidScotchData(scotchData) == False:
            return False
        else:
            self.scotchData = scotchData

        if self.scotchLib.isLoaded():
            if self.scotchLib.createSCOTCHGraph():
                if self.scotchLib.buildSCOTCHGraphFromData(self.scotchData):
                    return True
        return False

    def graphMap(self):
        if self.scotchLib.isLoaded():
            return self.scotchLib.graphMap(self.scotchData.verttab)
        return False
