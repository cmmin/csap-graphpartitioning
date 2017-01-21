import context # to modify the path from which we import modules
import unittest

# import the module that we are currently testing
import utilities.typeutils as typeutils

class TestTypeUtilities(unittest.TestCase):
    def test_checkArgType(self):
        self.assertTrue(typeutils.checkArgType(12, int))
        self.assertFalse(typeutils.checkArgType("12", int))
        self.assertFalse(typeutils.checkArgType(12.5, int))
        self.assertFalse(typeutils.checkArgType(12, str))
        self.assertTrue(typeutils.checkArgType('12', str))

    def test_checkArgtypeConvert(self):
        self.assertTrue(typeutils.checkArgtypeConvert(12, int, True))
        self.assertTrue(typeutils.checkArgtypeConvert("12", int, True))
        self.assertTrue(typeutils.checkArgtypeConvert(12.5, int, True))
        self.assertTrue(typeutils.checkArgtypeConvert(12, str, True))
        self.assertTrue(typeutils.checkArgtypeConvert('12', str, True))

    def test_IsInt(self):
        self.assertTrue(typeutils.isInt(12, False) == True)
        self.assertTrue(typeutils.isInt(12.2, False) == False)
        self.assertTrue(typeutils.isInt("12", False) == False)
        self.assertTrue(typeutils.isInt("12", True) == True)
        self.assertTrue(typeutils.isInt("12.5", True) == False)

    def test_IsStr(self):
        self.assertTrue(typeutils.isStr(12) == False)
        self.assertTrue(typeutils.isStr(12.2) == False)
        self.assertTrue(typeutils.isStr("12") == True)
        self.assertTrue(typeutils.isStr("12") == True)
        self.assertTrue(typeutils.isStr("12.5") == True)

    def test_isFloat(self):
        self.assertTrue(typeutils.isFloat(12) == False)
        self.assertTrue(typeutils.isFloat(12.2) == True)
        self.assertTrue(typeutils.isFloat("12") == False)
        self.assertTrue(typeutils.isFloat("12.5") == False)
        self.assertTrue(typeutils.isFloat("12.5", True) == True)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTypeUtilities)
    unittest.TextTestRunner(verbosity=2).run(suite)
