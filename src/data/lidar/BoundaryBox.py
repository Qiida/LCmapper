import matplotlib
import matplotlib.pyplot as plt

from src.data.__tuple import Coordinates

matplotlib.use("TkAgg")


class BoundaryBox:
    def __init__(self, width, length, height, color=None, lineWidth=None):
        self.width = width
        self.length = length
        self.height = height
        self.color = color
        self.lineWidth = lineWidth

    def draw(self, axis, coordinates, courseAngle):
        x = coordinates.x
        y = coordinates.y

        self.__drawBottomLinesY(axis, x, y)
        self.__drawBottomLinesX(axis, x, y)
        self.__drawTopLinesY(axis, x, y)
        self.__drawTopLinesX(axis, x, y)
        self.__drawVerticalLines(axis, x, y)

    def __drawBottomLinesX(self, axis, x, y):
        self.__drawLine(startpoint=[self.__getBottomLeftX(x), self.__getBottomLeftY(y), 0],
                        endpoint=[self.__getTopLeftX(x), self.__getTopLeftY(y), 0],
                        axis=axis)

        self.__drawLine(startpoint=[self.__getBottomRightX(x), self.__getBottomRightY(y), 0],
                        endpoint=[self.__getTopRightX(x), self.__getTopRightY(y), 0],
                        axis=axis)

    def __drawBottomLinesY(self, axis, x, y):
        self.__drawLine(startpoint=[self.__getBottomLeftX(x), self.__getBottomLeftY(y), 0],
                        endpoint=[self.__getBottomRightX(x), self.__getBottomRightY(y), 0],
                        axis=axis)

        self.__drawLine(startpoint=[self.__getTopLeftX(x), self.__getTopLeftY(y), 0],
                        endpoint=[self.__getTopRightX(x), self.__getTopRightY(y), 0],
                        axis=axis)

    def __drawTopLinesX(self, axis, x, y):
        self.__drawLine(startpoint=[self.__getBottomLeftX(x), self.__getBottomLeftY(y), self.height],
                        endpoint=[self.__getTopLeftX(x), self.__getTopLeftY(y), self.height],
                        axis=axis)

        self.__drawLine(startpoint=[self.__getBottomRightX(x), self.__getBottomRightY(y), self.height],
                        endpoint=[self.__getTopRightX(x), self.__getTopRightY(y), self.height],
                        axis=axis)

    def __drawTopLinesY(self, axis, x, y):
        self.__drawLine(startpoint=[self.__getBottomLeftX(x), self.__getBottomLeftY(y), self.height],
                        endpoint=[self.__getBottomRightX(x), self.__getBottomRightY(y), self.height],
                        axis=axis)

        self.__drawLine(startpoint=[self.__getTopLeftX(x), self.__getTopLeftY(y), self.height],
                        endpoint=[self.__getTopRightX(x), self.__getTopRightY(y), self.height],
                        axis=axis)

    def __drawVerticalLines(self, axis, x, y):
        self.__drawLine(startpoint=[self.__getBottomLeftX(x), self.__getBottomLeftY(y), 0],
                        endpoint=[self.__getBottomLeftX(x), self.__getBottomLeftY(y), self.height],
                        axis=axis)

        self.__drawLine(startpoint=[self.__getTopLeftX(x), self.__getTopLeftY(y), 0],
                        endpoint=[self.__getTopLeftX(x), self.__getTopLeftY(y), self.height],
                        axis=axis)

        self.__drawLine(startpoint=[self.__getTopRightX(x), self.__getTopRightY(y), 0],
                        endpoint=[self.__getTopRightX(x), self.__getTopRightY(y), self.height],
                        axis=axis)

        self.__drawLine(startpoint=[self.__getBottomRightX(x), self.__getBottomRightY(y), 0],
                        endpoint=[self.__getBottomRightX(x), self.__getBottomRightY(y), self.height],
                        axis=axis)

    def __drawLine(self, axis, startpoint, endpoint, color=None):
        if color is None:
            color = self.color
        x, y, z = [startpoint[0], endpoint[0]], [startpoint[1], endpoint[1]], [startpoint[2], endpoint[2]]
        axis.plot(x, y, z, color=color, linewidth=self.lineWidth)

    def __getBottomLeftX(self, x):
        return x - self.length / 2

    def __getBottomLeftY(self, y):
        return y - self.width / 2

    def __getBottomRightX(self, x):
        return x - self.length / 2

    def __getBottomRightY(self, y):
        return y + self.width / 2

    def __getTopLeftX(self, x):
        return x + self.length / 2

    def __getTopLeftY(self, y):
        return y - self.width / 2

    def __getTopRightX(self, x):
        return x + self.length / 2

    def __getTopRightY(self, y):
        return y + self.width / 2


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.axis("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    bBox = BoundaryBox(width=2, length=5, height=1.5, color="red", lineWidth=2)
    bBox.draw(ax, Coordinates(0, 0), 30)
