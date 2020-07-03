import unittest

import matplotlib.pyplot as plt

from reamber.algorithms.plot.nps import npsPlot, npsPlotByKey
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *


class TestNps(unittest.TestCase):

    # @profile
    def test(self):
        m = OsuMap()
        m.readFile(OSU_PLANET_SHAPER)
        npsPlot(m.notes)
        plt.savefig('main.png')

    def testByKey(self):
        m = OsuMap()
        m.readFile(OSU_PLANET_SHAPER)
        npsPlotByKey(m.notes)
        plt.show()
        plt.savefig('byKey.png')


if __name__ == '__main__':
    unittest.main()
