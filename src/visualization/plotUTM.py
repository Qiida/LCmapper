import matplotlib

from os.path import join
from matplotlib import pyplot, patches

from src.lcm.LidarCameraMapper import LidarCameraMapper
from src.utils.system import ROOT_DIR, LIDAR_DIR
from src.data.preparation.computeUTM import computeUTM_ego_obj
from src.data.readMatlabFiles import readMatFile
from src.data.lidar.TestVehicle import TestVehicle

matplotlib.use("TkAgg")


def plotUTM(ego):

    pyplot.plot(ego.x, ego.y, linewidth=2, color="black")
    pyplot.grid("on")
    pyplot.show()


if __name__ == '__main__':
    path = join(ROOT_DIR, 'resources', 'lidar', 'Export_pp_20191125_IM_1_split_050.mat')
    matFile = readMatFile(path)
    ego, obj = computeUTM_ego_obj(data=matFile['data'], testVehicle=TestVehicle("TEASY3"))

    plotUTM(ego=ego)
