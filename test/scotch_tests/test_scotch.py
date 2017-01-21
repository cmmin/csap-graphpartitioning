import context
import unittest

import scotch
from utilities.system_utils import OS, getOS

def getLibPath():
    libPath = ''
    if getOS() == OS.linux:
        libPath = "/usr/lib/libscotch-5.1.so"
        #libPath = "../../tools/scotch/lib/linux/libscotch.so"
        print(libPath)
    elif getOS() == OS.macOS:
        libPath = "../../tools/scotch/lib/macOS/libscotch.dylib"

    return libPath

class TestScotchLibrary(unittest.TestCase):
    def test_loadScotchLibrary(self):
        libPath = getLibPath()
        libScotch = scotch.LibScotch(libraryPath=libPath)
        self.assertTrue(libScotch.isLoaded())

    def test_archMethods(self):
        libPath = getLibPath()
        libScotch = scotch.LibScotch(libraryPath=libPath)
        self.assertTrue(libScotch.isLoaded())

        self.assertTrue(libScotch.createSCOTCHArch())

    def test_archDelete(self):
        libPath = getLibPath()
        libScotch = scotch.LibScotch(libraryPath=libPath)
        self.assertTrue(libScotch.isLoaded())
        self.assertTrue(libScotch.createSCOTCHArch())
        libScotch.deleteSCOTCHArch()
        self.assertTrue(libScotch.architecture is None)

    def test_archPopulate(self):
        libPath = getLibPath()
        libScotch = scotch.LibScotch(libraryPath=libPath)
        self.assertTrue(libScotch.isLoaded())
        self.assertTrue(libScotch.createSCOTCHArch())
        self.assertTrue(libScotch.populatePartitionArchitecture(10))

    def test_graphCreation(self):
        libPath = getLibPath()
        libScotch = scotch.LibScotch(libraryPath=libPath)
        self.assertTrue(libScotch.isLoaded())
        self.assertTrue(libScotch.createSCOTCHGraph())

    def test_stratCreation(self):
        libPath = getLibPath()
        libScotch = scotch.LibScotch(libraryPath=libPath)
        self.assertTrue(libScotch.isLoaded())
        self.assertTrue(libScotch.createSCOTCHGraphMapStrategy(''))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestScotchLibrary)
    unittest.TextTestRunner(verbosity=2).run(suite)
