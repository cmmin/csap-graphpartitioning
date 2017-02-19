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

class LibPatoh:
    def __init__(self, libraryPath = None):
        if libraryPath == None:
            libraryPath = defaultLibraryPath()

        self.clib = CLibrary(libraryPath)
        self.clib.load()


        self.PATOH_version = self.clib.library.Patoh_VersionStr
        self.PATOH_version.restype = (ctypes.c_char_p)

        self.clib.library.free.argtypes = (ctypes.c_void_p,)

    def version(self):
        return self.PATOH_version().decode('utf-8')
