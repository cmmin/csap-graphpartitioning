from utilities.clibrary_loader import CLibrary

from ctypes import cdll


if __name__ == '__main__':
    lib = CLibrary("../tools/scotch/lib/macOS/libscotch.dylib")
    lib.load()
