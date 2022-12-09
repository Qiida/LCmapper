from collections import namedtuple

Coordinates = namedtuple("Coordinates", ["x", "y"])
Obj = namedtuple("Obj", ["x", "y"])


Ellipsoid = namedtuple("Ellipsoid", ["a", "f", "b"])
ellipsoid = Ellipsoid(float(6378137), float(1 / 298.257223563), float(6378137 * (1 - 1 / 298.257223563)))

