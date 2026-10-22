import time

import numpy as np

from pyMilk.interfacing.shm import SHM


if __name__ == "__main__":
    time.sleep(90)
    shm = SHM('process')
    shm.set_data(0)
    print("it's so over")

