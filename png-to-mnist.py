import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
import glob

image_x_size = 28
image_y_size = 28


for filename in glob.glob("test-images/*.png"):
    image = Image.open(filename).convert('LA')
    width, height = image.size
    print (filename + "size is" + width + " by " + height)

    if (width > image_x_size || height > image_y_size):
        Image.resize(image_x_size, image_y_size)

    data = np.array(image, dtype='uint8')
    if (np.array)
        numpy.invert(data)
    np.save(filename + '.npy', data)
    print (filename + ".npy was saved")




else:
print "Nichts zu tun"
