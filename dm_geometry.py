## -- IMPORTS

import matplotlib.pyplot as plt
import numpy as np
import scipy

import hcipy


## -- build pupil grid that is DM geometry size 
pupil_grid = hcipy.make_pupil_grid(160, 26.5) # this gives you 50 pixels across each segment 
gmt_aperture = hcipy.make_gmt_aperture()
aperture = gmt_aperture(pupil_grid).shaped

# these are apertures if you want to control every actuator as one big matrix 
# gives 13097 controlled actuators 
# this is about right by the numbers if you assume each segment is a perfect circle r=25 
# and the central segment is between 60-70% of that 
total_control_region_aperture = np.array(aperture, dtype=bool)
total_control_region_flat = total_control_region_aperture.reshape(160*160)

# if instead you want 7 little control matrices ... 
labeled_segments, n_labels = scipy.ndimage.label(aperture)
if n_labels != 10:
    print('Indexing has changed. Automatic segment ID is not going to work.')
    raise Exception 

# Reassign all the gunk in the central obscuration to be one big segment 
# And then make the segement numbers contiguous 
contiguous_segments = np.copy(labeled_segments)
contiguous_segments[labeled_segments == 6] = 4
contiguous_segments[labeled_segments == 7] = 4
contiguous_segments[labeled_segments == 8] = 4
contiguous_segments[labeled_segments == 9] = 6
contiguous_segments[labeled_segments == 10] = 7

segment_1_mask = np.array(contiguous_segments == 1)
segment_2_mask = np.array(contiguous_segments == 2)
segment_3_mask = np.array(contiguous_segments == 3)
segment_4_mask = np.array(contiguous_segments == 4)
segment_5_mask = np.array(contiguous_segments == 5)
segment_6_mask = np.array(contiguous_segments == 6)
segment_7_mask = np.array(contiguous_segments == 7)

plt.imshow(contiguous_segments, cmap='Pastel2', origin='lower')
plt.colorbar()
plt.xlabel('actuators across')
plt.ylabel('actuators across')
plt.savefig('dm_segment_control_gemoetry.png')
