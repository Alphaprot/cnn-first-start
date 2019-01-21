from __future__ import print_function
import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
import glob

image_x_size = 28
image_y_size = 28
image_list = []
image_path = "image_store"


#image_store = os.listdir("test-images/")

def show():
    for filename in glob.glob('test-images/*.png'):
        img=Image.open(filename)
        image_list.append(img)

    else:
        if len(image_list) == 0:
            print ("No files were read! Please check input directory!") #images_plt = [Image.open(i) for i in range(len(image_store)) if i.endswith(".png")]


    print(*image_list, sep='\n')
    print("\n", len(image_list), " images were read.")

def convert():
    for filename in image_list:
        img = Image.open(filename)
        img.convert("LA")
        width, height = images_plt.size
        print (filename," size is now",width," by ",height)


show()
convert()
"""
    image = Image.open(file)
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

"""
