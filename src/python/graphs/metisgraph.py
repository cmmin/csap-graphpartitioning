from utilities.exceptions import MetisGraphFormatException, noExceptPropagate
from utilities.typeutils import isStr, toInt

import os
import os.path

#@noExceptPropagate
def checkGraphFormatString(metisGraphFormatStr):
    if(isStr(metisGraphFormatStr) == False):
        try:
            metisGraphFormatStr = str(metisGraphFormatStr)
        except:
            print("Could not convert metisGraphFormatStr to str.")
            return "000"

    nChars = len(metisGraphFormatStr)
    if(nChars == 0):
        metisGraphFormatStr = "000"
    elif nChars == 1:
        metisGraphFormatStr = "00" + metisGraphFormatStr
    elif nChars == 2:
        metisGraphFormatStr = "0" + metisGraphFormatStr
    elif nChars > 3:
        raise MetisGraphFormatException("The METIS format string has > 3 characters: " + metisGraphFormatStr)

    zero = '0'
    one = '1'

    for c in metisGraphFormatStr:
        if c != zero and c != one:
            raise MetisGraphFormatException("METIS format string contains a character that is not '0' or '1'")

    return metisGraphFormatStr


def parseGraphFormatString(metisGraph, metisGraphFormatStr):
    if(isinstance(metisGraph, MetisGraph)):
        try:
            metisGraphFormatStr = checkGraphFormatString(metisGraphFormatStr)
        except Exception as err:
            print(err)
            print("Using default metis graph format, 000")
            metisGraphFormatStr = "000"

        if(len(metisGraphFormatStr) == 3):
            zero = '0'
            one = '1'

            if metisGraphFormatStr[0] is one:
                metisGraph.hasVertexSize = True

            if metisGraphFormatStr[1] is one:
                metisGraph.hasVertexWeights = True

            if metisGraphFormatStr[2] is one:
                metisGraph.hasEdgeWeights = True


class MetisEdge:
    ''' Represents an Edge in a METIS Graph (u < v) '''
    def __init__(self, u = -1, v = -1, weight = 1):
        self.u = u
        self.v = v
        self.weight = weight

        self.adjustUVMapping()

    def printData(self):
        print("Edge (u,v) =", self.u, ",", self.v,' weight =', self.weight)

    def adjustUVMapping(self):
        if(self.u > self.v):
            tmp = self.u
            self.u = self.v
            self.v = tmp

    def getPair(self):
        return (self.u, self.v)

    def getKey(self):
        return str(self.u) + '_' + str(self.v)

    def hasVertexID(self, vertexID):
        if self.u == vertexID or self.v == vertexID:
            return True
        return False

    def getOtherVertex(self, vertexID):
        if(self.u == vertexID):
            return self.v
        elif(self.v == vertexID):
            return self.u
        else:
            return -1

class MetisVertex:
    def __init__(self, vertexID, vertexSize = 1, weights = None):
        self.vertexID = vertexID
        self.vertexSize = vertexSize

        if(weights is None):
            self.vertexWeights = [ 1 ]
        else:
            self.vertexWeights = weights

        self.edges = {}

    def printData(self, concise = True):
        print('Vertex', self.vertexID, " size =", self.vertexSize, " edges =", len(self.edges))

        if concise:
            return None

        for edgeKey in self.edges:
            self.edges[edgeKey].printData()

    def addEdge(self, metisEdge):
        if(isinstance(metisEdge, MetisEdge)) == False:
            return False

        edgeKey = metisEdge.getKey()

        if self.hasEdge(metisEdge):
            return False
        else:
            self.edges[edgeKey] = metisEdge
            return True

    def hasEdge(self, edge):
        if isinstance(edge, str):
            if len(edge.split("_")) == 2:
                # this is an edge key
                if edge in self.edges:
                    return True
            return False
        elif isinstance(edge, int):
            if edge == self.vertexID:
                return False
            for edgeKey in self.edges:
                if self.edges[edgeKey].hasVertexID(edge):
                    return True
            return False
        else:
            return False

    def numEdges(self):
        return len(self.edges)

    def edgeVertexIDs(self):
        edgeIDs = []
        for edgeKey in self.edges:
            eID = self.edges[edgeKey].getOtherVertex(self.vertexID)
            edgeIDs.append(eID)
        edgeIDs.sort()
        return edgeIDs

class MetisGraph:
    def __init__(self, filePath = None):
        self.baseVertexID = 1

        self.hasEdgeWeights = False
        self.hasVertexWeights = False
        self.hasVertexSize = False

        self.rawFormatString = "000"

        self.vertexWeightsCount = 1
        self.minNumVertexLineValues = 0

        self.uniqueEdges = []

        self.vertices = {}

        if(filePath != None):
            self.load(filePath)

    def load(self, filePath):
        if os.path.isfile(filePath) == False:
            # TODO exception
            print('Could not locate file at', filePath)
            return None
        with open(filePath, 'r') as f:
            lineNum = 0
            for line in f:
                line = line.strip()
                if(self._isLineComment(line)):
                    continue
                if(lineNum == 0):
                    # header line
                    self._parseHeader(line)
                    self._computeMinVertexLineValues()
                else:
                    self._parseVertexLine(line, lineNum)
                lineNum += 1

    def printData(self, concise = True):
        print('Vertices =', self.numVertices(), "Unique Edges =", self.numEdges())
        if(concise == True):
            return False

    def addVertex(self, vertex):
        if isinstance(vertex, MetisVertex) == False:
            return False

        if vertex.vertexID not in self.vertices:
            self.vertices[vertex.vertexID] = vertex
        else:
            return False

        for edgeID in vertex.edges:
            if self.isEdgeUnique(edgeID):
                self.uniqueEdges.append(edgeID)

        return True

    def isEdgeUnique(self, edge):
        if(isinstance(edge, MetisEdge)):
            edgekey = edge.getKey()
            if edgekey in self.uniqueEdges:
                return False
            return True
        elif (isinstance(edge, str)):
            if(len(edge.split('_')) == 2):
                if edge in self.uniqueEdges:
                    return False
                else:
                    return True
        return True

    def numVertices(self):
        return len(self.vertices)

    def numEdges(self):
        return len(self.uniqueEdges)

    def _parseHeader(self, headerStr):
        parts = headerStr.split(" ")
        numParts = len(parts)
        if(numParts >= 2 and numParts <= 4):
            numVertex = toInt(parts[0])
            numEdges  = toInt(parts[1])

            if numParts > 2:
                self.rawFormatString = parts[2]
                parseGraphFormatString(self, self.rawFormatString)
            if numParts > 3:
                self.vertexWeightsCount = toInt(parts[3], 1)
        else:
            # TODO exception
            print('Exception: wrong number of header parameters in metis graph')

    def _parseVertexLine(self, vertexStr, vertexID):
        parts = vertexStr.split(" ")
        values = []

        # convert all parts to integers
        for part in parts:
            value = toInt(part)
            if value is not None:
                values.append(value)

        vertexWeights = [ 1 ]
        vertexSize = 1

        if(len(values) < self.minNumVertexLineValues):
            # TODO exception
            print("Error, mismatch between min number of vertices datapoints and number found: ", self.minNumVertexLineValues, len(values))
            return False

        valueIDStart = 0
        if self.hasVertexSize:
            vertexSize = values[0]
            valueIDStart = 1

        if self.hasVertexWeights:
            vertexWeights = []
            for i in range(valueIDStart, valueIDStart + self.vertexWeightsCount):
                vertexWeights.append(values[i])
            valueIDStart += self.vertexWeightsCount

        vertex = MetisVertex(vertexID, vertexSize, vertexWeights)

        skipNextValue = False
        for i in range(valueIDStart, len(parts)):
            if skipNextValue:
                skipNextValue = False
                continue

            edgeID = values[i]
            edgeWeight = 1

            if self.hasEdgeWeights:
                edgeWeight = values[i + 1]
                skipNextValue = True

            edge = MetisEdge(vertexID, edgeID, edgeWeight)
            vertex.addEdge(edge)

        self.addVertex(vertex)

    def _computeMinVertexLineValues(self):
        self.minNumVertexLineValues = 0
        if self.hasVertexSize:
            self.minNumVertexLineValues += 1
        if self.hasVertexWeights:
            self.minNumVertexLineValues += self.vertexWeightsCount

    def _isLineComment(self, line):
        line = line.replace(" ", "")
        if(len(line)):
            if(line[0] == '%'):
                return True
        return False
