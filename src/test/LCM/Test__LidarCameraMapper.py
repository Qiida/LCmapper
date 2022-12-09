import unittest

from src.lcm.LidarCameraMapper import LidarCameraMapper
from src.lcm.LcmException import LcmException, LcmIOException, LcmMissingDataException
from src.data import TEASY3


class LcmTestCase(unittest.TestCase):

    def test_loadAndPrepareData_raiseLcmIOException(self):
        lcm = LidarCameraMapper(testVehicle=TEASY3())
        self.assertRaises(LcmIOException, lcm.loadLidarFile, "matFile", "matFilePath")
        self.assertRaises(LcmIOException, lcm.loadAndPrepareData, "matFile", "matFilePath", "camFile", "camFilePath")
        self.assertRaises(LcmIOException, lcm.loadAndPrepareData, "matFile", "matFilePath", "camFile", "camFilePath")
        self.assertRaises(LcmIOException, lcm.loadAndPrepareData, "matFile", "matFilePath", None, None)
        self.assertRaises(LcmIOException, lcm.loadAndPrepareData, None, None, "camFile", "camFilePath")

    def test_prepareLidarData_raiseLcmMissingDataException(self):
        lcm = LidarCameraMapper(testVehicle=TEASY3())
        self.assertRaises(LcmMissingDataException, lcm.processLidarData)


if __name__ == '__main__':
    unittest.main()
