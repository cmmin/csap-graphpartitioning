import context
import unittest

import scotch
from utilites.system_utils import OS, getOS

class TestScotchLibrary(unittest.TestCase):
    def test_loadScotchLibrary(self):
        if getOS() == OS.linux:
            libPath = "../../tools/scotch/lib/linux/libscotch.a"
        elif getOS() == OS.macOS:
            libPath = "../../tools/scotch/lib/macOS/libscotch.dylib"

        libScotch = scotch.LibScotch(libraryPath=libPath)
        self.assertTrue(libScotch.isLoaded())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestScotchLibrary)
    unittest.TextTestRunner(verbosity=2).run(suite)
