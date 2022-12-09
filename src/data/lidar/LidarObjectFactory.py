import numpy as np

from src.data.__tuple import Coordinates
from src.data.lidar.BoundaryBox import BoundaryBox
from src.data.lidar.LidarParameter import LidarParameter
from src.data.lidar.lidarobjects.Bike import Bike
from src.data.lidar.lidarobjects.Car import Car
from src.data.lidar.lidarobjects.NotClassified import NotClassified
from src.data.lidar.lidarobjects.Pedestrian import Pedestrian
from src.data.lidar.lidarobjects.Truck import Truck
from src.data.lidar.lidarobjects.UnknownBig import UnknownBig
from src.data.lidar.lidarobjects.UnknownClass import UnknownClass
from src.data.lidar.lidarobjects.UnknownSmall import UnknownSmall
from src.data.preparation.computeObjectCenter import computeObjectCenter_x_y


class LidarObjectFactory:

    def __init__(self, objectLaserRaw):

        # Private.
        self.ID = None
        self.data = None
        self.classification = None
        self.lidarObjects = None
        self.timeCan = None
        self.objectCoordinates = None
        self.courseAngle = None

        self.__initialize(objectLaserRaw)
        self.__initializeLidarObjects()

    def getLidarObjects(self):
        return self.lidarObjects

    def __buildObject(self, objNr, ID):
        idNr = np.where(~np.isnan(self.classification[objNr]))
        timeCan = self.timeCan[idNr]
        return self.__buildLidarObject(ID, objNr, idNr, timeCan)

    def __initialize(self, objectLaserRaw):
        self.data = objectLaserRaw
        self.ID = np.transpose(self.data["objectIDList"])
        self.classification = np.transpose(self.data["Classification"])
        self.lidarObjects = list()
        self.timeCan = self.data["time_can"]
        self.objectCoordinates = self.__getObjectCoordinates()
        self.courseAngle = np.transpose(self.data["ObjCourseAngle"])

    def __getObjectCoordinates(self):
        objectCenterX, objectCenterY = computeObjectCenter_x_y(self.data)
        return Coordinates(np.transpose(objectCenterX), np.transpose(objectCenterY))

    def __initializeLidarObjects(self):
        for objNr, ID in enumerate(self.ID):
            self.lidarObjects.append(self.__buildObject(objNr, ID))

    def __getClassification(self, idNr, objNr):
        classification = self.classification[objNr][idNr]
        if np.all(classification == classification[0]):
            classification = classification[0]
            return classification
        return None

    def __getLidarParameter(self, ID, objNr, idNr, timeCan):
        coordinates = Coordinates(self.objectCoordinates.x[objNr], self.objectCoordinates.y[objNr])
        courseAngle = self.courseAngle[objNr]
        return LidarParameter(ID, objNr, idNr, coordinates, timeCan, courseAngle)

    def __buildLidarObject(self, ID, objNr, idNr, timeCan):
        lidarParameter = self.__getLidarParameter(ID, objNr, idNr, timeCan)
        classification = self.__getClassification(idNr, objNr)
        match classification:
            case 0:
                return NotClassified(self.data, lidarParameter)
            case 1:
                return UnknownSmall(self.data, lidarParameter)
            case 2:
                return UnknownBig(self.data, lidarParameter)
            case 3:
                return Pedestrian(self.data, lidarParameter)
            case 4:
                return Bike(self.data, lidarParameter)
            case 5:
                return Car(self.data, lidarParameter)
            case 6:
                return Truck(self.data, lidarParameter)
            case 17:
                return UnknownClass(self.data, lidarParameter)
