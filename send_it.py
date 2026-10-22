import numpy as np
import sys 

import hcipy
from pyMilk.interfacing.shm import SHM


# spin up SHMs (as new objects / overwrite) 
def generate_turbulence_shm():
    shm_turb = SHM('turbulence', np.zeros((256, 256), dtype=np.float32))
    return shm_turb

def generate_process_shm():
    print("we're so back")
    shm_process = SHM('process', np.ones((1), dtype=int))
    return shm_process

# spin up hcipy simulations 
def generate_hcipy_model():
    pupil_grid = hcipy.make_pupil_grid(256, 25.4)
    layers = hcipy.atmosphere.make_las_campanas_atmospheric_layers(pupil_grid)
    multi_layer_model = hcipy.atmosphere.MultiLayerAtmosphere(layers)
    return multi_layer_model

if __name__=="__main__":

    args = sys.argv
    try: 
        iters = int(args[1])
    except IndexError: 
        print('No turbulence limit set using 10000.')
        iters = 10000
    shm_process = generate_process_shm()
    shm_turb = generate_turbulence_shm()
    print('Initialize shm')
    multi_layer_model = generate_hcipy_model()
    print('Turb model built')
    t = 1/(2e3)
    wavelength=800e-9
    #for i in range(iters):
    run = bool(shm_process.get_data()[0])
    i = 0
    while run and i < iters:
        run = bool(shm_process.get_data()[0])
        print(i)
        multi_layer_model.evolve_until(t*(i+1))
        phase = np.array(multi_layer_model.phase_for(wavelength).shaped, dtype=np.float32)
        shm_turb.set_data(phase)
        i += 1
    shm_process.set_data(np.array([0], dtype=int))
# Finally this would run through terminal to spin up the veiwers 
# $ shmImshow.py turbulence --fr=20
# $ shmImshow.py wfs --fr=20 

