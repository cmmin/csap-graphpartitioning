import numpy as np
import graphs.metisgraph as mg

import networkx as nx

def genArray(n, defaultVal = 0):
    arr = []
    for i in range(0, n):
        arr.append(defaultVal)
    if n != len(arr):
        print('genArr error in generating number of array')
    return arr


# ctypes conversions
# http://stackoverflow.com/questions/7543675/how-to-convert-pointer-to-c-array-to-python-array



class ScotchGraphArrays:
    def __init__(self):
        self.verttab = []
        self.edgetab = []
        self.edlotab = []
        self.velotab = []
        self.vertexweights = []
        self.parttab = []

        self._verttab = None
        self._edgetab = None
        self._edlotab = None
        self._velotab = None
        self._vertexweights = None
        self._parttab = None


        self.vertnbr = 0
        self.edgenbr = 0
        self.baseval = 0

    def debugPrint(self):
        print(self.vertnbr)
        print(self.edgenbr)
        print(self.baseval)

        print(len(self.verttab))
        print(self.verttab)
        print(len(self.edgetab))
        print(self.edgetab)
        print(len(self.edlotab))
        print(self.edlotab)
        print(len(self.velotab))
        print(self.velotab)
        print(len(self.vertexweights))
        print(self.vertexweights)
        print(len(self.parttab))
        print(self.parttab)


    def fromNetworkxGraph(self, nxGraph):
        if isinstance(nxGraph, nx.Graph) == False:
            print('Error, cannot load networkx graph from datatype', type(metisGraph).__name__)
            return False

        # number_of_nodes
        # size() ? number of edges

        self.vertnbr = nxGraph.number_of_nodes()
        self.edgenbr = nxGraph.size() * 2
        self.baseval = 1

        self.verttab = genArray(nxGraph.number_of_nodes() + 1)
        self.edgetab = genArray(nxGraph.size() * 2)

        self.edlotab = genArray(nxGraph.size() * 2)
        self.velotab = genArray(nxGraph.number_of_nodes())


        self.parttab = genArray(nxGraph.number_of_nodes(), -1)


        vtabID = 0
        nodes = nxGraph.nodes()
        for vertexID in range(1, len(nodes) + 1):
            vertex = nodes[vertexID - 1]
            adjustedID = vertexID - self.baseval

            #vertex.printData(False)

            self.verttab[adjustedID] = vtabID
            self.velotab[adjustedID] = 1 # TODO vertex weights

            indexedEdges = {}
            #edgeIndeces = vertex.edgeVertexIDs()
            edgeIndeces = nxGraph.neighbors(vertex)

            '''
            for edgeKey in vertex.edges:
                edge = vertex.edges[edgeKey]
                otherEdgeVertexID = edge.getOtherVertex(vertex.vertexID)

                indexedEdges[otherEdgeVertexID] = edge
            '''
            edgeCount = 0
            for edgeID in edgeIndeces:

                self.edgetab[vtabID + edgeCount] = edgeID - self.baseval
                self.edlotab[vtabID + edgeCount] = 1

                edgeCount += 1
            vtabID += len(edgeIndeces)

        self.verttab[nxGraph.number_of_nodes()] = vtabID

        #print("Exporting Arrays for SCOTCH")
        self._exportArraysForSCOTCH()

    def fromMetisGraph(self, metisGraph):
        if isinstance(metisGraph, mg.MetisGraph) == False:
            print('Error, cannot load metis graph from datatype', type(metisGraph).__name__)
            return False

        self.vertnbr = metisGraph.numVertices()
        self.edgenbr = metisGraph.numEdges() * 2
        self.baseval = metisGraph.baseVertexID

        self.verttab = genArray(metisGraph.numVertices() + 1)
        self.edgetab = genArray(metisGraph.numEdges() * 2)

        self.edlotab = genArray(metisGraph.numEdges() * 2)
        self.velotab = genArray(metisGraph.numVertices())

        self.parttab = genArray(metisGraph.numVertices(), -1)

        if metisGraph.vertexWeightsCount > 1:
            print("Warning: fromMetisGraph() number of weights for each vertex is unsupported ", metisGraph.vertexWeightsCount)

        vtabID = 0
        for vertexID in range(1, len(metisGraph.vertices) + 1):
            vertex = metisGraph.vertices[vertexID]
            adjustedID = vertexID - metisGraph.baseVertexID

            #vertex.printData(False)

            self.verttab[adjustedID] = vtabID
            self.velotab[adjustedID] = 1 # TODO vertex weights

            indexedEdges = {}
            edgeIndeces = vertex.edgeVertexIDs()
            for edgeKey in vertex.edges:
                edge = vertex.edges[edgeKey]
                otherEdgeVertexID = edge.getOtherVertex(vertex.vertexID)

                indexedEdges[otherEdgeVertexID] = edge

            edgeCount = 0
            for edgeID in edgeIndeces:

                self.edgetab[vtabID + edgeCount] = edgeID - metisGraph.baseVertexID
                self.edlotab[vtabID + edgeCount] = indexedEdges[edgeID].weight

                edgeCount += 1
            vtabID += vertex.numEdges()
        self.verttab[metisGraph.numVertices()] = vtabID

        #print("Exporting Arrays for SCOTCH")
        self._exportArraysForSCOTCH()

    def setFixedVertices(self, parttab):
        if(len(parttab) == self.vertnbr):
            self.parttab = parttab
            self._parttab = self._exportToNumpyArray(parttab)
            return True
        return False

    def _exportArraysForSCOTCH(self):
        self._verttab = self._exportToNumpyArray(self.verttab)
        self._edgetab = self._exportToNumpyArray(self.edgetab)
        self._edlotab = self._exportToNumpyArray(self.edlotab)
        self._velotab = self._exportToNumpyArray(self.velotab)
        self._parttab = self._exportToNumpyArray(self.parttab)
        self._vertexweights = self._exportToNumpyArray(self.vertexweights)

    def _exportToNumpyArray(self, array):
        return np.asanyarray(array, dtype=np.int32)
