import context
import unittest

import ctypes

class TestCtypes(unittest.TestCase):
    def test_cast(self):
        x = ctypes.c_double * 128


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCtypes)
    unittest.TextTestRunner(verbosity=2).run(suite)
