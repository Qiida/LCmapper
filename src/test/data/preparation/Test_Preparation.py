import unittest
import numpy as np

from math import isclose
from os.path import join

from src.utils.system import ROOT_DIR, LIDAR_DIR
from src.data.preparation.deg2utm import deg2utm
from src.data.preparation.computeEgoUTM import computeEgoUTM_ego_egoYaw
from src.data.preparation.filterNanColumns import filterNanColumns
from src.data.readMatlabFiles import readMatFiles, findMatFiles, readMatFile
from src.data import TestVehicleFactory


class DataPreparationTest(unittest.TestCase):

    def test_filterNanColumns(self):
        foundFiles = findMatFiles(path=LIDAR_DIR)
        lidarFile = readMatFile(join(LIDAR_DIR, foundFiles[0]))
        data = lidarFile["data"]
        filterNanColumns(data)
        self.assertEqual(333, len(data["object_laser_raw"]["objectIDList"]))

    def test_deg2utm(self):

        matFiles = readMatFiles(join(ROOT_DIR, "src", "python", "test", "resources", "mat"))
        lidarFiles = readMatFiles(LIDAR_DIR)
        longRes = []
        latRes = []
        zoneNoRes = False
        zoneCharRes = False

        for fileName in lidarFiles.keys():

            data = lidarFiles[fileName]['data']
            long, lat, zoneNo, zoneChar = deg2utm(data['ego']['long_abs'], data['ego']['lat_abs'])
            matData = matFiles[fileName + '_deg2utm']

            for i in range(len(long)):
                longRes.append(isclose(long[i], matData['ADMA_UTM_LONG'][i], rel_tol=1e-8))
                latRes.append(isclose(lat[i], matData['ADMA_UTM_LAT'][i], rel_tol=1e-8))
                zoneNoRes = (isclose(zoneNo, matData['ADMA_UTM_ZONE_No'][0][0], rel_tol=1e-8))
                zoneCharRes = (isclose(zoneChar, matData['ADMA_UTM_ZONE_Char'][0][0], rel_tol=1e-8))

            self.assertTrue(np.all(longRes))
            self.assertTrue(np.all(latRes))
            self.assertTrue(zoneNoRes)
            self.assertTrue(zoneCharRes)

    def test_egoTransformation(self):
        foundFiles = findMatFiles(LIDAR_DIR)
        lidarFile = readMatFile(join(LIDAR_DIR, foundFiles[0]))
        matEgo = readMatFile(join(ROOT_DIR, "src", "python", "test", "resources", "mat", foundFiles[0] + '_egoX_egoY'))
        ego,_ = computeEgoUTM_ego_egoYaw(ego=lidarFile['data']['ego'], testVehicle=TestVehicleFactory().build("TEASY3"))
        matEgoX = matEgo['egoX']
        matEgoY = matEgo['egoY']
        resX = []
        resY = []
        for i in range(len(ego.x)):
            resX.append(isclose(ego.x[i], matEgoX[i], rel_tol=1e-8))
            resY.append(isclose(ego.y[i], matEgoY[i], rel_tol=1e-8))

        self.assertTrue(np.all(resX))
        self.assertTrue(np.all(resY))


if __name__ == '__main__':
    unittest.main()
