import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
import glob

image_x_size = 28
image_y_size = 28
image_list = []

for filename in glob.glob("test-images/*.png"):
    image = Image.open(filename)
    image_list.apped(image)
print (image_list)
print ("Finished")


    '''image = Image.open(file)
    image.convert('LA')
    width, height = image.size
    print (file," size is ",width," by ",height)

    if (width > image_x_size or height > image_y_size):
        Image.resize(image_x_size, image_y_size)

    data = np.array(image, dtype='uint8')
    print data
    if (np.array):
        numpy.invert(data)
        np.save(file,'.npy', data)
        print (file,".npy was saved")
    else:
        print ('Nichts zu tun')
    '''
