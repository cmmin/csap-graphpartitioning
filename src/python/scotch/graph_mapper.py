import os
import os.path

import scotch.scotch as sl
import scotch.io as sio

import graphs.metisgraph as mg

import ctypes


# maybe, build the C++ version directly?
# seems to crash on architecture


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
    print("Loading METIS file:", metisFilePath)
    metisGraph = mg.MetisGraph(metisFilePath)
    metisGraph.printData()

    print("Loading SCOTCH library:", libraryPath)
    scotchData = sio.ScotchGraphArrays()
    scotchData.fromMetisGraph(metisGraph)

    print("Creating GraphMapper instance")
    mapper = GraphMapper(libraryPath)
    mapper.kbalval = 0.01

    print("Intializing Architecture for GraphMap")
    ok = mapper.initArchitecture()
    print("   Architecture =", ok)

    print("Intializing Strategy for GraphMap")
    ok = mapper.initStrategy()
    print("   Strategy =", ok)

    print("Loading Graph for GraphMap")
    ok = mapper.loadGraph(scotchData)
    print("   Graph =", ok)

    #mapper.scotchData.debugPrint()
    if ok == False:
        return None

    print("Running SCOTCH_graphMap()")
    ok = mapper.graphMap()
    print("   Graph Mapped =", ok)

    print("Vertex Partitions")
    print(mapper.scotchData._parttab)

    print("Fixing first ten vertices")
    mapper.scotchData.parttab = sio.genArray(mapper.scotchData.vertnbr, -1)
    for i in range(0, 10):
        mapper.scotchData.parttab[i] = i
        print("  Fixing vertex", i + 1, "to partition with ID", i)
    mapper.scotchData._parttab = mapper.scotchData._exportToNumpyArray(mapper.scotchData.parttab)

    print("Input Vertex Partition IDs")
    print(mapper.scotchData._parttab)


    print("Running graphMapFixed with some fixed vertices")
    ok = mapper.graphMapFixed()
    print("   Graph Mapped Fixed =", ok)

    print("New Vertex Partitions")
    print(mapper.scotchData._parttab)


    return mapper


def isScotchData(data):
    return isinstance(data, sio.ScotchGraphArrays)

def isValidScotchData(data):
    if isScotchData(data) == False:
        return False

    return data.isValid()

class GraphMapper:
    def __init__(self, scotchLibPath = None, numPartitions = 10, kbalval = 0.1, strategyFlag = 1, strategyOptions = ''):
        self.scotchLib = None
        self.scotchData = None

        self.scotchLibPath = scotchLibPath

        # Optional Parameters
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

    def initialize(self, scotchArrayData, verbose=True, skipGraphValidStep=False):
        if(verbose):
            print("Intializing Architecture for GraphMap")

        ok = self.initArchitecture()

        if(verbose):
            print("   Architecture =", ok)

        if(verbose):
            print("Intializing Strategy for GraphMap")

        ok = self.initStrategy()

        if(verbose):
            print("   Strategy =", ok)

        if(verbose):
            print("Loading Graph for GraphMap")

        ok = self.loadGraph(scotchArrayData, skipGraphValidStep=skipGraphValidStep)

        if(verbose):
            print("   Graph =", ok)

        return ok

    def loadLibrary(self, scotchLibPath):
        lib = sl.LibScotch(scotchLibPath)
        if(lib.isLoaded()):
            self.scotchLib = lib
            self.scotchLibPath = scotchLibPath
            return True
        return False

    def delObjects(self):
        if self.scotchLib.isLoaded():
            self.scotchLib.deleteSCOTCHGraph()
            self.scotchLib.deleteSCOTCHStrat()
            self.scotchLib.deleteSCOTCHArch()
        if self.scotchData is not None:
            # clear arrays
            self.scotchData.clearData()

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
            return ok
            ok = self.scotchLib.setStrategyFlags(self.strategyOptions)
            if ok == False:
                return False
            return True
        return False

    def loadGraph(self, scotchData, skipGraphValidStep = False):
        if isValidScotchData(scotchData) == False:
            print("loadGraph: not Valid Scotch Data")
            return False
        else:
            self.scotchData = scotchData

        if self.scotchLib.isLoaded():
            ok = self.scotchLib.createSCOTCHGraph()
            if ok == False:
                print("loadGraph: cannot createSCOTCHGraph")
                return False
            ok  = self.scotchLib.buildSCOTCHGraphFromData(self.scotchData)
            if ok == False:
                print("loadGraph: cannot buildSCOTCHGraphFromData")
                return False

            if skipGraphValidStep == True:
                return ok

            ok = self.scotchLib.scotchGraphValid()
            if ok == False:
                print("loadGraph: scotchGraphValid returned false")
            return ok
        return False

    def graphMap(self):
        if self.scotchLib.isLoaded():

            #arr = (ctypes.c_int * 1000)(*self.scotchData.parttab)
            #return self.scotchLib.graphMap(arr)

            return self.scotchLib.graphMap(self.scotchData._parttab)
        return False

    def graphMapFixed(self):
        if self.scotchLib.isLoaded():
            return self.scotchLib.graphMapFixed(self.scotchData._parttab)
        return False
