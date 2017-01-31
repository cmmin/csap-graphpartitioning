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
        self.vlbltab = []
        self.vertexweights = []
        self.parttab = []

        self._verttab = None
        self._edgetab = None
        self._edlotab = None
        self._velotab = None
        self._vlbltab = None
        self._vertexweights = None
        self._parttab = None


        self.vertnbr = 0
        self.edgenbr = 0
        self.baseval = 0

    def _initializeParams(self):
        self.verttab = []
        self.edgetab = []
        self.edlotab = []
        self.velotab = []
        self.vlbltab = []
        self.vertexweights = []
        self.parttab = []

        self._verttab = None
        self._edgetab = None
        self._edlotab = None
        self._velotab = None
        self._vlbltab = None
        self._vertexweights = None
        self._parttab = None


        self.vertnbr = 0
        self.edgenbr = 0
        self.baseval = 0

    def debugPrint(self):
        print('vertnbr', self.vertnbr)
        print('edgenbr', self.edgenbr)
        print('baseval', self.baseval)

        print('len verttab', len(self.verttab))
        print('verttab', self.verttab)
        print('len velotab', len(self.velotab))
        print('velotab', self.velotab)
        print('len vlbltab', len(self.vlbltab))
        print('vlbltab', self.vlbltab)
        print('len vertweights', len(self.vertexweights))
        print('vertweights', self.vertexweights)

        print('len edgetab', len(self.edgetab))
        print('edgetab', self.edgetab)
        print('len edlotab', len(self.edlotab))
        print('edlotab', self.edlotab)

        print('len parttab', len(self.parttab))
        print('parttab', self.parttab)

    def isValid(self):
        # TODO complete this
        if self.vertnbr + 1 != len(self._verttab):
            return False
        if self.vertnbr != len(self._velotab):
            return False
        if self.edgenbr != len(self._edgetab):
            return False
        if self.edgenbr != len(self._edlotab):
            return False

        # deep check
        for edgeID in self._edgetab:
            if edgeID not in self.vlbltab:
                print('EdgeID not in vlbltab', edgeID)
                return False

        return True


    def clearData(self):
        self._initializeParams()

    def fromNetworkxGraph(self, nxGraph, baseval=1, parttab=None, vlbltab=None):
        if isinstance(nxGraph, nx.Graph) == False:
            print('Error, cannot load networkx graph from datatype', type(metisGraph).__name__)
            return False

        # number_of_nodes
        # size() ? number of edges

        self.vertnbr = nxGraph.number_of_nodes()
        self.edgenbr = nxGraph.size() * 2
        self.baseval = baseval

        self.verttab = genArray(nxGraph.number_of_nodes() + 1)
        self.edgetab = genArray(nxGraph.size() * 2)

        self.edlotab = genArray(nxGraph.size() * 2)
        self.velotab = genArray(nxGraph.number_of_nodes())


        if(vlbltab is None):
            self.vlbltab = genArray(nxGraph.number_of_nodes())
            #self.vlbltab = []
        else:
            if len(vlbltab) == self.vertnbr:
                self.vlbltab = vlbltab
            else:
                self.vlbltab = genArray(nxGraph.number_of_nodes())


        if parttab is None:
            self.parttab = genArray(nxGraph.number_of_nodes(), -1)
        else:
            if len(parttab) == self.vertnbr:
                self.parttab = parttab
            else:
                self.parttab = genArray(nxGraph.number_of_nodes(), -1)

        vtabID = 0
        nodes = nxGraph.nodes()

        vertCount = 0
        for vertexID in range(self.baseval, len(nodes) + self.baseval):
            vertex = nodes[vertexID - self.baseval]
            adjustedID = vertexID - self.baseval

            self.vlbltab[vertCount] = nodes[vertexID - self.baseval] # store the lable for this vertex as vertCount != adjustID
            vertCount += 1
            #vertex.printData(False)

            self.verttab[adjustedID] = vtabID

            vWeight = 1

            try:
                vWeight = nxGraph.node[vertex]['weight']
            except KeyError as ke:
                pass

            self.velotab[adjustedID] = vWeight

            indexedEdges = {}
            edgeIndeces = nxGraph.neighbors(vertex)

            edgeCount = 0
            for edgeID in edgeIndeces:

                edgeWeight = 1
                try:
                    edgeWeight = nxGraph[adjustedID][edgeID]['weight']
                except Exception as e:
                    edgeWeight = 1

                self.edgetab[vtabID + edgeCount] = edgeID - self.baseval
                self.edlotab[vtabID + edgeCount] = edgeWeight

                #print('edge:', vertex, edgeID - self.baseval)

                edgeCount += 1
            vtabID += len(edgeIndeces)

        self.verttab[nxGraph.number_of_nodes()] = vtabID

        # update vertex IDs
        updateEdgeIDSUsingLabels = False
        if updateEdgeIDSUsingLabels:
            lblmap = {}
            for newVertID in range(0, len(self.vlbltab)):
                oldVertID = self.vlbltab[newVertID]
                lblmap[oldVertID] = newVertID
            for i in range(0, len(self.edgetab)):
                newVal = lblmap[self.edgetab[i]]
                self.edgetab[i] = newVal

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
        if(len(self.vlbltab) == self.vertnbr):
            self._vlbltab = self._exportToNumpyArray(self.vlbltab)

    def _exportToNumpyArray(self, array):
        return np.asanyarray(array, dtype=np.int32)
