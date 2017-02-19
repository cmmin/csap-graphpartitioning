#from ctypes import POINTER, c_int, c_double, c_void_p, c_char_p, cast
import ctypes


from utilities.clibrary_loader import CLibrary
import utilities.typeutils as typeutils
import utilities.system_utils as sysutils


from pathlib import Path
import os

def defaultLibraryPath():
    if sysutils.getOS() == sysutils.OS.macOS:
        return os.path.join(str(Path(__file__).parents[3]), 'tools/patoh/lib/macOS/libpatoh.dylib')
    elif sysutils.getOS() == sysutils.OS.linux:
        #return '/usr/local/lib/scotch_604/libscotch.so'
        return os.path.join(str(Path(__file__).parents[3]), 'tools/patoh/lib/linux/libpatoh.so')
        return ''

# C++ structures
# http://stackoverflow.com/questions/4351721/python-ctypes-passing-a-struct-to-a-function-as-a-pointer-to-get-back-data

class PATOHParameters(ctypes.Structure):
    _fields_ = [
        ("cuttype",ctypes.c_int),
        ("_k",ctypes.c_int),
        ("outputdetail",ctypes.c_int),
        ("seed",ctypes.c_int),
        ("doinitperm",ctypes.c_int),
        ("bisec_fixednetsizetrsh",ctypes.c_int),
        ("bisec_netsizetrsh",ctypes.c_float),
        ("bisec_partmultnetsizetrsh",ctypes.c_int),
        ("bigVcycle",ctypes.c_int),
        ("smallVcycle",ctypes.c_int),
        ("usesamematchinginVcycles",ctypes.c_int),
        ("usebucket",ctypes.c_int),
        ("maxcellinheap",ctypes.c_int),
        ("heapchk_mul",ctypes.c_int),
        ("heapchk_div",ctypes.c_int),
        ("MemMul_CellNet",ctypes.c_int),
        ("MemMul_Pins",ctypes.c_int),
        ("MemMul_General",ctypes.c_int),
        ("crs_VisitOrder",ctypes.c_int),
        ("crs_alg",ctypes.c_int),
        ("crs_coarsento",ctypes.c_int),
        ("crs_coarsentokmult",ctypes.c_int),
        ("crs_coarsenper",ctypes.c_int),
        ("crs_maxallowedcellwmult",ctypes.c_float),
        ("crs_idenafter",ctypes.c_int),
        ("crs_iden_netsizetrh",ctypes.c_int),
        ("crs_useafter",ctypes.c_int),
        ("crs_useafteralg",ctypes.c_int),
        ("nofinstances",ctypes.c_int),
        ("initp_alg",ctypes.c_int),
        ("initp_runno",ctypes.c_int),
        ("initp_ghg_trybalance",ctypes.c_int),
        ("initp_refalg",ctypes.c_int),
        ("ref_alg",ctypes.c_int),
        ("ref_useafter",ctypes.c_int),
        ("ref_useafteralg",ctypes.c_int),
        ("ref_passcnt",ctypes.c_int),
        ("ref_maxnegmove",ctypes.c_int),
        ("ref_maxnegmovemult",ctypes.c_float),
        ("ref_dynamiclockcnt",ctypes.c_int),
        ("ref_slow_uncoarsening",ctypes.c_float),
        ("balance",ctypes.c_int),
        ("init_imbal",ctypes.c_double),
        ("final_imbal",ctypes.c_double),
        ("fast_initbal_mult",ctypes.c_double),
        ("init_sol_discard_mult",ctypes.c_float),
        ("final_sol_discard_mult",ctypes.c_float),
        ("allargs",ctypes.c_byte * 8192),
        ("inputfilename",ctypes.c_byte * 512),
        ("writepartinfo",ctypes.c_int),
        ("noofrun",ctypes.c_int)
    ]


class LibPatoh:
    def __init__(self, libraryPath = None):
        if libraryPath == None:
            libraryPath = defaultLibraryPath()

        self.clib = CLibrary(libraryPath)
        self.clib.load()

        self.PATOH_version = self.clib.library.Patoh_VersionStr
        self.PATOH_version.restype = (ctypes.c_char_p)

        self.PATOH_InitializeParameters = self.clib.library.Patoh_Initialize_Parameters
        self.PATOH_InitializeParameters.argtypes = (ctypes.POINTER(PATOHParameters), ctypes.c_int, ctypes.c_int)

        self.clib.library.free.argtypes = (ctypes.c_void_p,)

    def version(self):
        return self.PATOH_version().decode('utf-8')

    def initializeParameters(self):
        params = PATOHParameters()
        ok = self.PATOH_InitializeParameters(ctypes.byref(params), 1, 0)
        if(ok == 0):
            return params
        else:
            return None
