from abc import ABC

import matplotlib
import numpy as np

from src.data.__tuple import Coordinates
from src.data.lidar.BoundaryBox import BoundaryBox

matplotlib.use("TkAgg")


class LidarObject(ABC):

    def __init__(self, data, lidarParameter, classification, color):

        self.data = None
        self.coordinates = None
        self.ID = None
        self.objNr = None
        self.classification = None
        self.idNr = None
        self.timeCan = None
        self.boundaryBox = None
        self.courseAngle = None

        self.__initialize(data, lidarParameter, classification, color)

    def __initialize(self, data, lidarParameter, classification, color):
        if data is not None:
            self.data = data
        if lidarParameter.coordinates is not None:
            self.coordinates = lidarParameter.coordinates
        if color is not None:
            self.color = color
        if lidarParameter.ID is not None:
            self.ID = lidarParameter.ID
        if lidarParameter.objNr is not None:
            self.objNr = lidarParameter.objNr
        if classification is not None:
            self.classification = classification
        if lidarParameter.idNr is not None:
            self.idNr = lidarParameter.idNr
        if lidarParameter.timeCan is not None:
            self.timeCan = lidarParameter.timeCan
        if lidarParameter.courseAngle is not None:
            self.courseAngle = lidarParameter.courseAngle

        self.boundaryBox = self.__buildBoundaryBox(color)

    def __buildBoundaryBox(self, color):
        length, width = self.__getObjectBoxSize()
        # TODO: implement height method
        height = 1.5
        lineWidth = 1.5
        return BoundaryBox(width=width, length=length, height=height, color=color, lineWidth=lineWidth)

    def __getObjectBoxSize(self):
        objectBoxSizeX = np.transpose(self.data["ObjBoxSizeX"])[self.objNr][self.idNr]
        objectBoxSizeX = objectBoxSizeX[0]
        objectBoxSizeY = np.transpose(self.data["ObjBoxSizeY"])[self.objNr][self.idNr]
        objectBoxSizeY = objectBoxSizeY[0]
        return objectBoxSizeX, objectBoxSizeY

    def plotFrame(self, axis, idNr):
        coordinates = self.getCoordinates(idNr)
        courseAngle = self.courseAngle[idNr]
        self.boundaryBox.draw(axis, coordinates, courseAngle)

    def getCoordinates(self, idNr):
        return Coordinates(self.coordinates.x[idNr], self.coordinates.y[idNr])
