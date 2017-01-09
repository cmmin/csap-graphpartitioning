from utilities.clibrary_loader import CLibrary

from ctypes import POINTER, c_int, c_double, c_void_p

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

        # SCOTCH_archInit
        self.SCOTCH_archInit = self.clib.library.SCOTCH_archInit
        self.SCOTCH_archInit.argtypes = [POINTER(self.SCOTCH_Arch)]

        # SCOTCH_archExit
        self.SCOTCH_archExit = self.clib.library.SCOTCH_archExit
        self.SCOTCH_archExit.argtypes = [POINTER(self.SCOTCH_Arch)]

        # SCOTCH_graphInit
        self.SCOTCH_graphInit = self.clib.library.SCOTCH_graphInit
        self.SCOTCH_graphInit.argtypes = [POINTER(self.SCOTCH_Graph)]

        # SCOTCH_graphExit
        self.SCOTCH_graphExit = self.clib.library.SCOTCH_graphExit
        self.SCOTCH_graphExit.argtypes = [POINTER(self.SCOTCH_Graph)]

        # SCOTCH_graphBuild
        self.SCOTCH_graphBuild = self.clib.library.SCOTCH_graphBuild
        self.SCOTCH_graphBuild.argtypes = [
            POINTER(self.SCOTCH_Graph), c_int, c_int,
            c_void_p, c_void_p, c_void_p, c_void_p,
            c_int, c_void_p, c_void_p
        ]

    def isLoaded(self):
        return self.clib.isLoaded()

    def version(self):
        major_ptr = c_int(0)
        relative_ptr = c_int(0)
        patch_ptr = c_int(0)

        ret = self.SCOTCH_version(major_ptr, relative_ptr, patch_ptr)
        return "{}.{}.{}".format(major_ptr.value, relative_ptr.value, patch_ptr.value)
