import unittest

from reamber.algorithms.convert.SMToQua import SMToQua
from reamber.sm.SMMapSet import SMMapSet
from tests.test.RSC_PATHS import *


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestSMToQua(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points

        sm = SMMapSet.read_file(SM_GRAVITY)

        quas = SMToQua.convert(sm)
        quas[0].write_file("gravity.qua")


    def test2(self):
        # Stops and multiple map

        sm = SMMapSet.read_file(SM_ESCAPES)

        quas = SMToQua.convert(sm)
        quas[0].write_file("escapes1.qua")
        quas[1].write_file("escapes2.qua")


if __name__ == '__main__':
    unittest.main()
