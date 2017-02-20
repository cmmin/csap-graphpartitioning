import patoh.patoh as pat

import networkx as nx
import numpy as np

def genArray(n, defaultVal = 0):
    arr = []
    for i in range(0, n):
        arr.append(defaultVal)
    if n != len(arr):
        print('genArr error in generating number of array')
    return arr


class PatohData:
    def __init__(self):
        self.initialize()

    def initialize(self):
        self._c = None
        self._n = None
        self._nconst = 1
        self.cwghts = []
        self.nwghts = []
        self.xpins = []
        self.pins = []
        self.partvec = []
        self.useFixCells = 0 # 0 assumes no partitions assigned
        self.cut = 0
        self.targetweights = []
        self.partweights = []

        #self.params = pat.PATOHParameters()
        self.params = None

        # exported arrays
        self._cwghts = None
        self._nwghts = None
        self._xpins = None
        self._pins = None
        self._partvec = None

        self._targetweights = None
        self._partweights = None

    def debugPrint(self):
        print('_c', self._c)
        print('_n', self._n)
        print('_nconst', self._nconst)
        print('cwghts', self.cwghts)
        print('nwghts', self.nwghts)
        print('xpins', self.xpins)
        print('pins', self.pins)
        print('partvec', self.partvec)
        print('useFixCell', self.useFixCells)
        print('cut', self.cut)
        print('targetweights', self.targetweights)
        print('partweights', self.partweights)

        # exported arrays
        #print('', self._cwghts)
        #print('', self._nwghts)
        #print('', self._xpins)
        #print('', self._pins)
        #print('', self._partvec)

        #print('', self._targetweights)
        #print('', self._partweights)
    def debugPrintExport(self):
        print('_cwghts', self._cwghts, self._cwghts.ctypes)
        print('_nwghts', self._nwghts, self._nwghts.ctypes)
        print('_xpins', self._xpins, self._xpins.ctypes)
        print('_pins', self._pins, self._pins.ctypes)
        print('_partvec', self._partvec, self._partvec.ctypes)

        print('_targetweights', self._targetweights, self._targetweights.ctypes)
        print('_partweights', self._partweights, self._partweights.ctypes)

    def fromNetworkxGraph(self, G, num_partitions, partvec = None):
        if(isinstance(G, nx.Graph) == False):
            return False

        cliques = self._getCliques(G)
        if cliques is None:
            return False

        self._c = self._computeCells(G, cliques)
        self._n = len(cliques)

        #xpins stores the index starts of each net (clique)
        #pins stores the node ides in each clique indexed by xpins
        self.xpins = genArray(self._n + 1, 0)
        self.pins = []

        # _nconst = number of weights for each vertex/cell
        # ASSUME _nconst = 1
        # node weights = cwhgts
        self.cwghts = genArray(self._c * self._nconst, 1)

        # edge weights need to be converted to nwghts
        self.nwghts = genArray(self._n, 1)

        for cliqueID, clique in enumerate(cliques):
            self.xpins[cliqueID] = len(self.pins)

            for node in clique:
                self.pins.append(node)
        # add last ID
        self.xpins[self._n] = len(self.pins)

        if partvec is not None:
            self.useFixCells = 1
            self.partvec = partvec

        self._setTargetWeights(num_partitions)

        self._exportArrays()

    def _getCliques(self, G):
        if(isinstance(G, nx.Graph) == False):
            return None

        return list(nx.find_cliques(G))

    def _computeCells(self, G, cliques):
        '''
        if removeEdgelessNodes:
            cells = []
            for clique in cliques:
                for edge in clique:
                    if edge in cells:
                        continue
                    cells.append(edge)
            return len(cells)
        else:
        '''
        return G.number_of_nodes()

    def _setTargetWeights(self, num_partitions):
        target = 1.0 / float(num_partitions)
        for k in range(0, num_partitions):
            self.targetweights.append(target)
        self.partweights = genArray(num_partitions * self._nconst, 0)

    def _exportArrays(self):
        self._cwghts = self._exportToNumpyArray(self.cwghts)
        self._nwghts = self._exportToNumpyArray(self.nwghts)
        self._xpins = self._exportToNumpyArray(self.xpins)
        self._pins = self._exportToNumpyArray(self.pins)
        self._partvec = self._exportToNumpyArray(self.partvec)

        self._targetweights = self._exportToNumpyArray(self.targetweights, dtype=np.float32)
        self._partweights = self._exportToNumpyArray(self.partweights)

    def _exportToNumpyArray(self, array, dtype=np.int32):
        if array is None:
            array = []
        return np.asanyarray(array, dtype=dtype)
