from __future__ import print_function
import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
from scipy import ndimage
import glob

image_x_size = 28
image_y_size = 28
image_list = []
filename_list = []
xImage = None # Leere Variable (spaeter numpy-Array fuer Bilddaten)
yLabel = None
scriptPath = os.path.dirname(os.path.abspath(__file__))


#image_store = os.listdir("test-images/")

def createLists():
    for filename in glob.glob(scriptPath + '/test-images/*.png'):
        img=Image.open(filename)
        image_list.append(img)
        filename_list.append(filename)

    else:
        if len(image_list) == 0:
            print ("No files were read! Please check input directory!") #images_plt = [Image.open(i) for i in range(len(image_store)) if i.endswith(".png")]

    xImage = np.zeros((len(image_list), 784)) # Numpy-Array mit Laenge aller Bilder in der image_list
    yLabel = np.zeros((len(image_list),10)) # Numpy-Array mit Labels 0-9

    print(*image_list, sep='\n')
    print("\n", len(image_list), " images were read.")

def convert():
    for img in image_list:
        #img = Image.open(filename)
        img.convert("LA")
        width, height = img.size

        if (width > image_x_size or height > image_y_size):
            Image.resize(image_x_size, image_y_size)
            print (filename," size is now",width," by ",height)

def makeLabels():
    for i, filename in enumerate(filename_list):
        basename = os.path.basename(filename)
        label = basename[3]
        a, b = basename[1], basename[2]
        filenumber = sum(int(a)*10 + int(b))
        yLabel.insert([filenumber, label])
    print("\n", "Filename is: ", filenumber, "-", label)


createLists()
makeLabels()
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
