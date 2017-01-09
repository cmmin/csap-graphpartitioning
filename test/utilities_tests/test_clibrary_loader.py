import context # to modify the path from which we import modules
import unittest

import utilities.clibrary_loader as libloader

class TestCLibraryLoader(unittest.TestCase):
    def test_setLibraryPath(self):
        validLibPath = "../../tools/scotch/lib/macOS/libscotch.dylib"
        invalidLibPaths = ["../tools/scotch/lib/macOS/libscotch.dll", ""]

        lib = libloader.CLibrary()

        self.assertTrue(lib.setLibraryPath(validLibPath))
        for lPath in invalidLibPaths:
            self.assertFalse(lib.setLibraryPath(lPath))

        # TODO test for specific exceptions

    def test_load(self):
        validLibPath = "../../tools/scotch/lib/macOS/libscotch.so"
        invalidLibPaths = ["../tools/scotch/lib/macOS/libscotch.dll", ""]

        lib = libloader.CLibrary()

        # valid
        lib.setLibraryPath(validLibPath)
        lib.load()
        self.assertTrue(lib.isLoaded())

    def test_init(self):
        lib = libloader.CLibrary()

        self.assertTrue(lib.library == None)
        self.assertTrue(len(self.libraryPath) = 0)
        self.assertFalse(lib.isLoaded())

        with self.assertRaises(Exception) as context:
            lib.load()

    def test__libExtensions(self):
        lib = libloader.CLibrary()
        extensions = lib._libExtensions()
        self.assertTrue(len(extensions) > 0)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCLibraryLoader)
    unittest.TextTestRunner(verbosity=2).run(suite)
