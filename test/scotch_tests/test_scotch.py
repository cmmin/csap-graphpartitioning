import context
import unittest

import scotch

class TestScotchLibrary(unittest.TestCase):
    def test_loadScotchLibrary(self):
        libPath = "../../tools/scotch/lib/macOS/libscotch.dylib"

        libScotch = scotch.LibScotch(libraryPath=libPath)
        self.assertTrue(libScotch.isLoaded())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestScotchLibrary)
    unittest.TextTestRunner(verbosity=2).run(suite)
