from pathlib import Path
from os.path import join

ROOT_DIR = Path(__file__).parent.parent.parent
LIDAR_DIR = join(ROOT_DIR, "resources", "lidar")
CAM_DIR = join(ROOT_DIR, "resources", "camera")

if __name__ == '__main__':
    print(ROOT_DIR)
    print(LIDAR_DIR)
    print(CAM_DIR)
