## Maybe these will have a different home one day ...

import numpy as np

def bin_image(image, factor):
    # bin some image with dimensions x,y to x/factor, y/factor 
    # this will throw an error if x/factor and y/factor are not integers 
    # this uses addative binning so all flux through the super region is summed together 
    image_x, image_y = np.shape(image)
    if image_x/factor != image_x//factor or image_y/factor != image_y//factor:
        raise Exception('binning factor must leave an integer number of samples')
    binned_image = np.zeros((int(image_x/factor), int(image_y/factor)))
    previous_index_x, counter_x = 0,0
    counter_x = 0
    for x_index in np.arange(factor, image_x+factor, factor):
        previous_index_y, counter_y = 0,0
        for y_index in np.arange(factor, image_y+factor, factor):
            super_region = image[previous_index_x:x_index, previous_index_y:y_index]
            binned_value = np.sum(super_region)
            binned_image[counter_x, counter_y] = binned_value
            counter_y += 1
            previous_index_y = y_index
        counter_x += 1
        previous_index_x = x_index
    return binned_image
