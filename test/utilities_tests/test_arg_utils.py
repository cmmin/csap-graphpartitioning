import context # to modify the path from which we import modules
import unittest

# import the module that we are currently testing
import utilities.argutils as argutils

class TestArgUtilities(unittest.TestCase):
    def test_checkArgType(self):
        self.assertTrue(argutils.checkArgType(12, int))
        self.assertFalse(argutils.checkArgType("12", int))
        self.assertFalse(argutils.checkArgType(12.5, int))
        self.assertFalse(argutils.checkArgType(12, str))
        self.assertTrue(argutils.checkArgType('12', str))

    def test_checkArgtypeConvert(self):
        self.assertTrue(argutils.checkArgtypeConvert(12, int, True))
        self.assertTrue(argutils.checkArgtypeConvert("12", int, True))
        self.assertTrue(argutils.checkArgtypeConvert(12.5, int, True))
        self.assertTrue(argutils.checkArgtypeConvert(12, str, True))
        self.assertTrue(argutils.checkArgtypeConvert('12', str, True))

    def test_IsInt(self):
        self.assertTrue(argutils.isInt(12, False) == True)
        self.assertTrue(argutils.isInt(12.2, False) == False)
        self.assertTrue(argutils.isInt("12", False) == False)
        self.assertTrue(argutils.isInt("12", True) == True)
        self.assertTrue(argutils.isInt("12.5", True) == False)

    def test_IsStr(self):
        self.assertTrue(argutils.isStr(12) == False)
        self.assertTrue(argutils.isStr(12.2) == False)
        self.assertTrue(argutils.isStr("12") == True)
        self.assertTrue(argutils.isStr("12") == True)
        self.assertTrue(argutils.isStr("12.5") == True)

    def test_isFloat(self):
        self.assertTrue(argutils.isFloat(12) == False)
        self.assertTrue(argutils.isFloat(12.2) == True)
        self.assertTrue(argutils.isFloat("12") == False)
        self.assertTrue(argutils.isFloat("12.5") == False)
        self.assertTrue(argutils.isFloat("12.5", True) == True)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestArgUtilities)
    unittest.TextTestRunner(verbosity=2).run(suite)
