from utilities.clibrary_loader import CLibrary

from ctypes import POINTER, c_int, c_double, c_void_p


class LibScotch:
    def __init__(self, libraryPath):
        self.scotch = CLibrary(libraryPath)
        self.scotch.load()

        # *******
        # methods
        # *******

        # Scotch::version()
        self.SCOTCH_version = self.scotch.library.SCOTCH_version
        self.SCOTCH_version.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int)]

    def isLoaded():
        return self.scotch.isLoaded()

    def version(self):
        major_ptr = c_int(0)
        relative_ptr = c_int(0)
        patch_ptr = c_int(0)

        ret = self.SCOTCH_version(major_ptr, relative_ptr, patch_ptr)
        return "{}.{}.{}".format(major_ptr.value, relative_ptr.value, patch_ptr.value)
