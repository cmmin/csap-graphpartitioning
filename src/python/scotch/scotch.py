from utilities.clibrary_loader import CLibrary

from ctypes import POINTER, c_int, c_double, c_void_p, c_char_p

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

        # *****************
        # structures & data
        # *****************

        self.SCOTCH_Arch = c_double*128
        self.SCOTCH_Graph = c_double*128
        self.SCOTCH_Strat = c_double*128

        # *******
        # methods
        # *******

        # Scotch::version()
        self.SCOTCH_version = self.clib.library.SCOTCH_version
        self.SCOTCH_version.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int)]

        # SCOTCH_archAlloc
        self.SCOTCH_archAlloc = self.clib.library.SCOTCH_archAlloc
        self.SCOTCH_archAlloc.argtypes = [None]

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
        self.SCOTCH_graphAlloc.argtypes = [None]

        # SCOTCH_graphInit
        self.SCOTCH_graphInit = self.clib.library.SCOTCH_graphInit
        self.SCOTCH_graphInit.argtypes = [POINTER(self.SCOTCH_Graph)]

        # SCOTCH_graphExit
        self.SCOTCH_graphExit = self.clib.library.SCOTCH_graphExit
        self.SCOTCH_graphExit.argtypes = [POINTER(self.SCOTCH_Graph)]

        # SCOTCH_graphCheck
        self.SCOTCH_graphCheck = self.clib.library.SCOTCH_graphCheck
        self.SCOTCH_graphCHeck.argtypes = [POINTER(self.SCOTCH_graph)]

        # SCOTCH_graphBuild
        self.SCOTCH_graphBuild = self.clib.library.SCOTCH_graphBuild
        self.SCOTCH_graphBuild.argtypes = [
            POINTER(self.SCOTCH_Graph), c_int, c_int,
            c_void_p, c_void_p, c_void_p, c_void_p,
            c_int, c_void_p, c_void_p
        ]

        # SCOTCH_stratAlloc
        self.SCOTCH_stratAlloc = self.clib.library.SCOTCH_stratAlloc
        self.SCOTCH_stratAlloc.argtypes = [ None ]

        # SCOTCH_stratInit
        self.SCOTCH_stratInit = self.clib.library.SCOTCH_stratInit
        self.SCOTCH_stratInit.argtypes = [POINTER(self.SCOTCH_Strat)]

        self.SCOTCH_stratGraphMap = self.clib.library.SCOTCH_stratGraphMap
        self.SCOTCH_stratGraphMap.argtypes = [POINTER(self.SCOTCH_Strat), c_char_p]

        self.SCOTCH_stratGraphMapBuild = self.clib.library.SCOTCH_stratGraphMap
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
        self.SCOTCH_Arch = self.SCOTCH_archAlloc()
        ret = self.SCOTCH_archInit(self.SCOTCH_Arch)
        if(ret == 0):
            return True
        return False

    def deleteSCOTCHArch(self):
        self.SCOTCH_archExit(self.SCOTCH_Arch)
        self.SCOTCH_Arch = None

    def populatePartitionArchitecture(self, numPartitions):
        if(isinstance(numPartitions, int) == False):
            try:
                numPartitions = int(numPartitions)
                if(isinstance(numPartitions, int) == False):
                    return False
            except ValueError as e:
                print(e)
                return False

        ret = self.SCOTCH_archCmplt(self.SCOTCH_Arch, numPartitions)
        if(ret == 0):
            return True

        return False

    def createSCOTCHGraph(self):
        self.SCOTCH_Graph = self.SCOTCH_graphAlloc()
        ret = self.SCOTCH_graphInit(self.SCOTCH_Graph)
        if(ret == 0):
            return True
        return False

    def buildSCOTCHGraphFromMetisGraph(self, metisGraph):
        pass
        # TODO decide the format of metisGraph object

    def deleteSCOTCHGraph(self):
        self.SCOTCH_graphExit(self.SCOTCH_Graph)
        self.SCOTCH_Graph = None

    def scotchGraphValid(self):
        ret = self.SCOTCH_graphCheck(self.SCOTCH_Graph)
        if(ret == 0):
            return True
        return False


    def createSCOTCHGraphMapStrategy(self, strategyFlags):
        self.SCOTCH_Strat = self.SCOTCH_stratAlloc()
        ret = self.SCOTCH_stratInit(self.SCOTCH_Strat)
        if(ret == 0):
            if(isinstance(strategyFlags, str) == False):
                strategyFlags = ''
            success = self.SCOTCH_stratGraphMap(self.SCOTCH_Strat, strategyFlags)
        return False
