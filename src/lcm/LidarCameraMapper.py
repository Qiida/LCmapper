import matplotlib
import matplotlib.pyplot as plt

from os.path import join
from src.data.lidar.LidarObjectFactory import LidarObjectFactory
from src.utils.system import LIDAR_DIR
from src.data.lidar.TestVehicle import TestVehicle
from src.data.preparation.filterNanColumns import filterNanColumns
from src.data.readMatlabFiles import readMatFile
from src.lcm.LcmException import LcmMissingDataException, LcmIOException

matplotlib.use("TkAgg")


class LidarCameraMapper:

    def __init__(self, testVehicle, mat=None, matPath=None, cam=None, camPath=None):

        # Public.
        self.camData = None
        self.camFrames = None
        self.testVehicle = None
        self.lidarEgo = None
        self.lidarData = None
        self.lidarObjects = None

        # Private.
        self.__matFile = mat
        self.__matFilePath = matPath
        self.__camFile = cam
        self.__camFilePath = camPath

        self.__lidarObjectFactory = None

        self.loadTestVehicle(testVehicle)
        self.loadAndPrepareData(cam, camPath, mat, matPath)

    def loadTestVehicle(self, testVehicle):
        if testVehicle is None:
            raise LcmMissingDataException(lcm=self)
        self.testVehicle = testVehicle

    def loadAndPrepareData(self, camFile, camFilePath, matFile, matFilePath):
        if (matFile is not None or matFilePath is not None) \
                and (camFile is None and camFilePath is None):

            self.__loadAndPrepareLidarData(matFile, matFilePath)

        elif (camFile is not None or camFilePath is not None) \
                and (matFile is None and matFilePath is None):

            self.__loadAndPrepareCamData(camFile, camFilePath)

        elif (camFile is not None or camFilePath is not None) \
                and (matFile is not None or matFilePath is not None):
            raise LcmIOException

    def loadLidarFile(self, matFile=None, matFilePath=None):
        if (matFile is not None and matFilePath is not None) \
                or (matFile is None and matFilePath is None):
            raise LcmIOException

        elif matFile is not None:
            assert isinstance(matFile, dict)
            self.lidarData = matFile["data"]

        elif matFilePath is not None:
            assert isinstance(matFilePath, str)
            self.lidarData = readMatFile(path=matFilePath)["data"]

    def processLidarData(self):
        if self.lidarData is None:
            raise LcmMissingDataException(lcm=self)

        filterNanColumns(self.lidarData)
        # self.lidarEgo, objectCoordinates = computeUTM_ego_obj(self.lidarData, testVehicle=self.testVehicle)
        # objectCoordinates = Coordinates()
        self.__lidarObjectFactory = LidarObjectFactory(self.lidarData["object_laser_raw"])
        self.lidarObjects = self.__lidarObjectFactory.getLidarObjects()

    def processCamFile(self, camFile=None, camFilePath=None):
        if camFile is not None and camFilePath is not None:
            raise LcmIOException
        # TODO: Implement with openCV
        pass

    def prepareCamData(self):
        # TODO: Implement with openCV
        pass

    def __loadAndPrepareLidarData(self, matFile, matFilePath):
        self.loadLidarFile(matFile=matFile, matFilePath=matFilePath)
        self.processLidarData()

    def __loadAndPrepareCamData(self, camFile, camFilePath):
        self.processCamFile(camFile=camFile, camFilePath=camFilePath)
        self.prepareCamData()


if __name__ == '__main__':
    lcm = LidarCameraMapper(testVehicle=TestVehicle("TEASY3"),
                            matPath=join(LIDAR_DIR, 'Export_pp_20191125_IM_1_split_050.mat'))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.axis("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    idNr = 0

    for lidarObject in lcm.lidarObjects:
        try:
            print(lidarObject.objNr)
            if idNr in lidarObject.idNr[0]:
                lidarObject.plotFrame(ax, idNr)
        except AttributeError:
            pass

    plt.show()


