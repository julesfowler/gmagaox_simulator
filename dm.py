import time

import numpy as np

from pyMilk.interfacing.shm import SHM


# spin up SHMs (as new objects / overwrite) 
def generate_dm_shm():
    shm_dm = SHM('dm', np.zeros((128, 128), dtype=np.float32))
    return shm_dm

def enforce_strict_timelag(timelag):
    def decorator(func):
        def wrapper(*args, **kwargs):
            time_start = time.time()
            out = func(*args, **kwargs)
            while time_start + timelag > time.time():
                #print(time_start + timelag, time.time())
                time.sleep(timelag/100)
            return out
        return wrapper
    return decorator

@enforce_strict_timelag(0.2)
# this timelag is in units of physical seconds
# but ideally it should be tied to the hcipy benchmark
# or something smarter/more adaptive idk
def calculate_dm_cmd(wfs_read, gain=0.5):
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


