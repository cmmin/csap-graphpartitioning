from ctypes import POINTER, c_int, c_double, c_void_p, c_char_p, cast

from utilities.clibrary_loader import CLibrary
import utilities.typeutils as typeutils

import scotch.io as scotchio

'''
Notes about SCOTCH

vertnbr = number of vertices in a graph (pg54 in scotch manual)
edgenbr = number of arcs in a graph = 2 * number of edges
baseval = graph base index value = value of starting index in the graph = 0 for C, 1 for Fortran (& python?)
numeric_flag = 3 decimal digits (CHACO format similar) vtxlbl_edgwts_vtxwts [vtxwts = vertex weights enabled; edgewts = edgeweights; vrtxlbl = vertex labels provided]

Each vertex definition [=optional]
$ [vertex_label] [vertex_load] vertex_degree (arcs...)

Each Arc:
$ [edge_load] vertex_label_destination

N.B. if vrtxlbl = 1 then vertices can be specified in any order in the file

SCOTCH .grf or .src format
LINE 1: version = 0 currently
LINE 2: vertnbr edgenbr
LINE 3: baseval numeric_flag


'''


'''
Interface being implemented

# Architecture Code

SCOTCH_arch * datastructure;
SCOTCH_archAlloc()
SCOTCH_archInit(SCOTCH_arch *)
SCOTCH_archExit(SCOTCH_arch *)
SCOTCH_archCmplt(SCOTCH_arch *, numpartitions)

# Strategy Code

SCOTCH_stratAlloc
SCOTCH_stratInit(SCOTCH_strat *)
SCOTCH_stratGraphMap(SCOTCH_strat *, char * format)

# Graph Code

SCOTCH_graphAlloc
SCOTCH_graphInit()
SCOTCH_graphExit
SCOTCH_graphCheck
SCOTCH_graphBuild

# Mapping

SCOTCH_graphMap(graph *, arch *, strat *, parttab *)

'''


class LibScotch:
    def __init__(self, libraryPath):
        self.clib = CLibrary(libraryPath)
        self.clib.load()

        self.enableExceptions = False

        # *****************
        # structures & data
        # *****************

        # These describe the type of object to be created
        self.SCOTCH_Arch = c_double*128
        self.SCOTCH_Graph = c_double*128
        self.SCOTCH_Strat = c_double*128

        # These store the scotch data objects (ie. graph = SCOTCH_Graph())
        self.architecture = None
        self.graph = None
        self.strategy = None

        # *******
        # methods
        # *******

        # Scotch::version()
        self.SCOTCH_version = self.clib.library.SCOTCH_version
        self.SCOTCH_version.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int)]

        # SCOTCH_archAlloc
        self.SCOTCH_archAlloc = self.clib.library.SCOTCH_archAlloc
        #self.SCOTCH_archAlloc.argtypes = [ None ]

        # SCOTCH_archInit
        self.SCOTCH_archInit = self.clib.library.SCOTCH_archInit
        self.SCOTCH_archInit.argtypes = [POINTER(self.SCOTCH_Arch)]

        # SCOTCH_archExit
        self.SCOTCH_archExit = self.clib.library.SCOTCH_archExit
        self.SCOTCH_archExit.argtypes = [POINTER(self.SCOTCH_Arch)]

        # SCOTCH_archCmplt - builds architecture for partitioning
        self.SCOTCH_archCmplt = self.clib.library.SCOTCH_archCmplt
        self.SCOTCH_archCmplt.argtypes = [POINTER(self.SCOTCH_Arch), c_int]

        # SCOTCH_graphAlloc
        self.SCOTCH_graphAlloc = self.clib.library.SCOTCH_graphAlloc
        #self.SCOTCH_graphAlloc.argtypes = [ None ]

        # SCOTCH_graphInit
        self.SCOTCH_graphInit = self.clib.library.SCOTCH_graphInit
        self.SCOTCH_graphInit.argtypes = [POINTER(self.SCOTCH_Graph)]

        # SCOTCH_graphExit
        self.SCOTCH_graphExit = self.clib.library.SCOTCH_graphExit
        self.SCOTCH_graphExit.argtypes = [POINTER(self.SCOTCH_Graph)]

        # SCOTCH_graphCheck
        self.SCOTCH_graphCheck = self.clib.library.SCOTCH_graphCheck
        self.SCOTCH_graphCheck.argtypes = [POINTER(self.SCOTCH_Graph)]

        # SCOTCH_graphBuild
        self.SCOTCH_graphBuild = self.clib.library.SCOTCH_graphBuild
        self.SCOTCH_graphBuild.argtypes = [
            POINTER(self.SCOTCH_Graph), c_int, c_int,
            c_void_p, c_void_p, c_void_p, c_void_p,
            c_int, c_void_p, c_void_p
        ]

        # SCOTCH_stratAlloc
        self.SCOTCH_stratAlloc = self.clib.library.SCOTCH_stratAlloc
        #self.SCOTCH_stratAlloc.argtypes = [ None ]

        # SCOTCH_stratInit
        self.SCOTCH_stratInit = self.clib.library.SCOTCH_stratInit
        self.SCOTCH_stratInit.argtypes = [POINTER(self.SCOTCH_Strat)]

        self.SCOTCH_stratGraphMap = self.clib.library.SCOTCH_stratGraphMap
        self.SCOTCH_stratGraphMap.argtypes = [POINTER(self.SCOTCH_Strat), c_char_p]

        self.SCOTCH_stratGraphMapBuild = self.clib.library.SCOTCH_stratGraphMapBuild
        self.SCOTCH_stratGraphMapBuild.argtypes = [POINTER(self.SCOTCH_Strat), c_int, c_int, c_double]

        # MAPPING Functions
        self.SCOTCH_graphMap = self.clib.library.SCOTCH_graphMap
        self.SCOTCH_graphMap.argtypes = [POINTER(self.SCOTCH_Graph), POINTER(self.SCOTCH_Arch), POINTER(self.SCOTCH_Strat), c_void_p]

    def isLoaded(self):
        return self.clib.isLoaded()

    def version(self):
        major_ptr = c_int(0)
        relative_ptr = c_int(0)
        patch_ptr = c_int(0)

        ret = self.SCOTCH_version(major_ptr, relative_ptr, patch_ptr)
        return "{}.{}.{}".format(major_ptr.value, relative_ptr.value, patch_ptr.value)

    def createSCOTCHArch(self):
        #self.SCOTCH_Arch = self.SCOTCH_archAlloc()
        #print(self.SCOTCH_Arch)
        self.architecture = self.SCOTCH_Arch()
        ret = self.SCOTCH_archInit(self.architecture)
        if(ret == 0):
            return True
        return False

    def deleteSCOTCHArch(self):
        self.SCOTCH_archExit(self.architecture)
        self.architecture = None

    def populatePartitionArchitecture(self, numPartitions):
        if(self.architecture is None):
            return False

        if(typeutils.isInt(numPartitions)):
            ret = self.SCOTCH_archCmplt(self.architecture, numPartitions)
            if(ret == 0):
                return True
        return False

    def createSCOTCHGraph(self):
        #self.SCOTCH_Graph = self.SCOTCH_graphAlloc()
        self.graph = self.SCOTCH_Graph()
        ret = self.SCOTCH_graphInit(self.graph)
        if(ret == 0):
            return True
        return False

    def buildSCOTCHGraphFromData(self, scotchData):
        if isinstance(scotchData, scotchio.ScotchGraphArrays) == False:
            return False

        if self.graph is None:
            if(self.createSCOTCHGraph() == False):
                return False

        # graphBuild graph*, baseval, vertnbr, verttab, 0, velotab, 0, edgenbr, eddgetab, edlotab

        success = self.SCOTCH_graphBuild(self.graph, 1, scotchData.vertnbr, scotchData.verttab.ctypes, None, scotchData.velotab.ctypes, None, scotchData.edgenbr, scotchData.edgetab.ctypes, scotchData.edlotab.ctypes)

        if success == 0:
            return True
        return False


    def deleteSCOTCHGraph(self):
        # TODO write test for this
        self.SCOTCH_graphExit(self.graph)
        self.graph = None

    def scotchGraphValid(self):
        # TODO write test for this
        ret = self.SCOTCH_graphCheck(self.graph)
        if(ret == 0):
            return True
        return False


    def createStrategy(self):
        self.strategy = self.SCOTCH_Strat()
        ret = self.SCOTCH_stratInit(self.strategy)
        if ret == 0:
            return True
        return False

    def setStrategyGraphMapBuild(self, straval, partitionNbr, kbalval = 0.1):
        ret = self.SCOTCH_stratGraphMapBuild(self.strategy, straval, partitionNbr, kbalval)
        if ret == 0:
            return True
        return False

    def setStrategyFlags(self, strategyFlags):
        if(typeutils.isStr(strategyFlags) == False):
            strategyFlags = ''
        # Note: must encode the string as that returns a bytecode equivalent
        success = self.SCOTCH_stratGraphMap(self.strategy, strategyFlags.encode('utf-8'))
        if(success == 0):
            return True
        return False

    def createSCOTCHGraphMapStrategy(self, strategyFlags):
        #self.strategy = self.SCOTCH_stratAlloc()
        self.strategy = self.SCOTCH_Strat()
        ret = self.SCOTCH_stratInit(self.strategy)
        if(ret == 0):
            if(typeutils.isStr(strategyFlags) == False):
                strategyFlags = ''
            # Note: must encode the string as that returns a bytecode equivalent
            success = self.SCOTCH_stratGraphMap(self.strategy, strategyFlags.encode('utf-8'))
            if(success == 0):
                return True
        return False


    def graphMap(self, parttab):
        ret = self.SCOTCH_graphMap(self.graph, self.architecture, self.strategy, parttab.ctypes)
        if ret == 0:
            return True
        return False
