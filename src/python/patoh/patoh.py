#from ctypes import POINTER, c_int, c_double, c_void_p, c_char_p, cast
import ctypes


from utilities.clibrary_loader import CLibrary
import utilities.typeutils as typeutils
import utilities.system_utils as sysutils

#import patoh.patoh_data as patdata


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

        self.PATOH_checkUserParameters = self.clib.library.Patoh_Check_User_Parameters
        self.PATOH_checkUserParameters.argtypes = (ctypes.POINTER(PATOHParameters), ctypes.c_int)


        self.PATOH_Alloc = self.clib.library.Patoh_Alloc
        self.PATOH_Alloc.argtypes = (ctypes.POINTER(PATOHParameters), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)
        #self.PATOH_Alloc.argtypes = (ctypes.POINTER(PATOHParameters), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

        self.PATOH_Part = self.clib.library.Patoh_Part

        self.PATOH_Part.argtypes = (ctypes.POINTER(PATOHParameters), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)


        self.PATOH_Free = self.clib.library.Patoh_Free

        self.cfree = self.clib.library.free
        self.cfree.argtypes = (ctypes.c_void_p,)

    def version(self):
        return self.PATOH_version().decode('utf-8')

    def initializeParameters(self, num_partitions =  2):
        if(isinstance(num_partitions, int) == False):
            num_partitions = 2

        params = PATOHParameters()
        ok = self.PATOH_InitializeParameters(ctypes.byref(params), 1, 0)
        if(ok == 0):
            params._k = num_partitions
            return params
        else:
            return None

    def checkUserParameters(self, params, verbose = True):
        if (isinstance(params, PATOHParameters) == False):
            print('Cannot check parameters as params is not of type PATOHParameters')
            return False

        # check verbosity mode
        v = 0
        if verbose == True:
            v = 1

        # perform parameter check
        ok = self.PATOH_checkUserParameters(ctypes.byref(params), v)
        if(ok == 0):
            print('User Parameters Valid')
            return True
        else:
            print('Error in the user parameters. Use verbose mode for greater details.')
            return False

    def alloc(self, patohData):
        #if (isinstance(patohData, patdata.PatohData) == False):
        #        return False

        #PPaToH_Parameters pargs, int _c, int _n, int _nconst, int *cwghts, int *nwghts, int *xpins, int *pins
        ok = self.PATOH_Alloc(ctypes.byref(patohData.params), patohData._c, patohData._n, patohData._nconst, patohData._cwghts.ctypes, patohData._nwghts.ctypes, patohData._xpins.ctypes, patohData._pins.ctypes)
        if (ok == 0):
            return True
        return False

    def part(self, patohData):

        '''
        int PaToH_Part(PPaToH_Parameters pargs, int _c, int _n, int _nconst, int useFixCells,
               int *cwghts, int *nwghts, int *xpins, int *pins, float *targetweights,
               int *partvec, int *partweights, int *cut);


        '''
        cut_val = ctypes.c_int(patohData.cut)
        cut_addr = ctypes.addressof(cut_val)

        ok = self.PATOH_Part(ctypes.byref(patohData.params), patohData._c, patohData._n, patohData._nconst, patohData.useFixCells, patohData._cwghts.ctypes, patohData._nwghts.ctypes, patohData._xpins.ctypes, patohData._pins.ctypes, patohData._targetweights.ctypes, patohData._partvec.ctypes, patohData._partweights.ctypes, cut_addr)

        if (ok == 0):
            # get value back
            patohData.cut = cut_val

            return True
        return False

    def free(self, patohData):
        #self.cfree(patohData._cwghts.ctypes)
        #self.cfree(patohData._nwghts.ctypes)
        #self.cfree(patohData._xpins.ctypes)
        #self.cfree(patohData._pins.ctypes)
        #self.cfree(patohData._partweights.ctypes)
        #self.cfree(patohData._partvec.ctypes)

        ok = self.PATOH_Free()
        if ok == 0:
            return True
        return False
