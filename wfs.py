import matplotlib.pyplot as plt
import time

import numpy as np
import skimage 

import hcipy
from pyMilk.interfacing.shm import SHM


# spin up SHMs (as new objects / overwrite) 
def generate_wfs_shm():
    shm_wfs = SHM('wfs', np.zeros((128, 128), dtype=np.float32))
    return shm_wfs

# spin up hcipy simulations 
def generate_gmt_aperture():
    pupil_grid = hcipy.make_pupil_grid(256, 25.4)
    gmt_aperture = hcipy.make_gmt_aperture()
    aperture = gmt_aperture(pupil_grid).shaped 
    return aperture

def wfs_sim(turbulence, dm, aperture):
    turb_read = np.array(skimage.transform.resize(turbulence*aperture, (128, 128)), dtype=np.float32)
    wfs_read = turb_read - dm
    return wfs_read

if __name__=="__main__":
    
    shm_wfs = generate_wfs_shm()
    print('Initialize wfs')
    
    aperture = generate_gmt_aperture()
    
    time.sleep(2)
    shm_turb = SHM('turbulence')
    shm_dm = SHM('dm')
    shm_process = SHM('process') 
    run = bool(shm_process.get_data())
    if not run:
        print('No ongoing process / nothing to see here.')
    i = 0
    while run:
        run = bool(shm_process.get_data())
        turbulence_state = shm_turb.get_data()
        dm_state = shm_dm.get_data()
        wfs_read = wfs_sim(turbulence_state, dm_state, aperture)
        print(i)
        shm_wfs.set_data(wfs_read)
        i += 1

# Finally this would run through terminal to spin up the veiwers 
# $ shmImshow.py turbulence --fr=20
# $ shmImshow.py wfs --fr=20 

