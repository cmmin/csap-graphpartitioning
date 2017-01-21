import numpy as np
import graphs.metisgraph as mg

def genArray(n, defaultVal = 0):
    arr = []
    for i in range(0, n):
        arr.append(defaultVal)
    if n != len(arr):
        print('genArr error in generating number of array')
    return arr


class ScotchGraphArrays:
    def __init__(self):
        self.verttab = []
        self.edgetab = []
        self.edlotab = []
        self.velotab = []
        self.vertexweights = []

        self.vertnbr = 0
        self.edgenbr = 0
        self.baseval = 0

    def fromMetisGraph(self, metisGraph):
        if isinstance(metisGraph, mg.MetisGraph) == False:
            print('Error, cannot load data from datatype', type(metisGraph).__name__)
            return False

        self.vertnbr = metisGraph.numVertices()
        self.edgenbr = metisGraph.numEdges() * 2
        self.baseval = metisGraph.baseVertexID

        self.verttab = genArray(metisGraph.numVertices() + 1)
        self.edgetab = genArray(metisGraph.numEdges() * 2)

        self.edlotab = genArray(metisGraph.numEdges() * 2)
        self.velotab = genArray(metisGraph.numVertices())

        if metisGraph.vertexWeightsCount > 1:
            print("Warning: fromMetisGraph() number of weights for each vertex is unsupported ", metisGraph.vertexWeightsCount)

        vtabID = 0
        for vertexID in metisGraph.vertices:
            vertex = metisGraph.vertices[vertexID]

            adjustedID = vertexID - metisGraph.baseVertexID

            self.verttab[adjustedID] = vtabID
            self.velotab[adjustedID] = 1 # TODO vertex weights

            edgeCount = 0
            for edgeKey in vertex.edges:
                edge = vertex.edges[edgeKey]

                otherEdgeVertexID = edge.getOtherVertex(vertex.vertexID)

                self.edgetab[vtabID + edgeCount] = otherEdgeVertexID - metisGraph.baseVertexID
                self.edlotab[vtabID + edgeCount] = edge.weight

                edgeCount += 1
            vtabID += vertex.numEdges()
        self.verttab[metisGraph.numVertices()] = vtabID

        self._exportArraysForSCOTCH()

    def _exportArraysForSCOTCH(self):
        self.verttab = self._exportToNumpyArray(self.verttab)
        self.edgetab = self._exportToNumpyArray(self.edgetab)
        self.edlotab = self._exportToNumpyArray(self.edlotab)
        self.velotab = self._exportToNumpyArray(self.velotab)
        self.vertexweights = self._exportToNumpyArray(self.vertexweights)

    def _exportToNumpyArray(self, array):
        return np.asanyarray(array, dtype=np.int32)
