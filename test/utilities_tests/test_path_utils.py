import context # to modify the path from which we import modules
import unittest

# import the module that we are currently testing
import utilities.path_utils as path_utils

class TestPathUtilities(unittest.TestCase):
    def test_checkFileExists(self):
        self.assertTrue(path_utils.checkFileExists("context.py"))
        self.assertFalse(path_utils.checkFileExists("../utilities_tests"))
        self.assertFalse(path_utils.checkFileExists("arandomfilename.py"))

    def test_checkFileExtensionValid(self):
        self.assertTrue(path_utils.checkFileExtensionValid("context.py", [".py"]))
        self.assertTrue(path_utils.checkFileExtensionValid("context.py", [".py", ".txt", ".cpp"]))
        self.assertTrue(path_utils.checkFileExtensionValid("context.txt", [".txt"]))
        self.assertFalse(path_utils.checkFileExtensionValid("context.txt", [".py", ".cpp"]))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPathUtilities)
    unittest.TextTestRunner(verbosity=2).run(suite)
