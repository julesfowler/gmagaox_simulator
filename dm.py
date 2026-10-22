import time

import numpy as np

from pyMilk.interfacing.shm import SHM


# spin up SHMs (as new objects / overwrite) 
def generate_dm_shm():
    shm_dm = SHM('dm', np.zeros((128, 128), dtype=np.float32))
    return shm_dm

def calculate_dm_cmd(wfs_read, gain=0.5, lag=0.2):
    time.sleep(lag)
    return np.array(wfs_read*gain, dtype=np.float32)

if __name__=="__main__":
    
    shm_dm = generate_dm_shm()
    #shm_turb = SHM('turbulence')
    print('Initialize dm')
    
    time.sleep(5)
    shm_process = SHM('process') 
    shm_wfs = SHM('wfs')
    run = bool(shm_process.get_data())
    if not run:
        print('No ongoing process / nothing to see here.')
    i = 0
    dm_cmd = np.zeros((128, 128), dtype=np.float32)
    while run:
        run = bool(shm_process.get_data())
        wfs_read = shm_wfs.get_data()
        dm_cmd += calculate_dm_cmd(wfs_read)
        print(i)
        shm_dm.set_data(dm_cmd)
        i += 1

# Finally this would run through terminal to spin up the veiwers 
# $ shmImshow.py turbulence --fr=20
# $ shmImshow.py wfs --fr=20 

