from __future__ import print_function
import os

import matplotlib.pyplot as plt
import numpy as np
import glob
from PIL import Image
from scipy import ndimage


scriptPath = os.path.dirname(os.path.abspath(__file__))
imagePath = (scriptPath + '/aragats-raw/*.jpg') #Make sure this is a valid path
configPath = os.dirname(dirname('scriptPath'))
imStore = np.array([], [], []) #Valid for RGB (3-channel) images). If usong other color formats, change tuple count
imTemp
configFile = "03_imag.json"

print ("Dirname is" + scriptPath)

def mask():
    for filename in glob.glob(imagePath):
        im=Image.open(filename)
        imTemp = np.array(im)
        imStore.append()

def save():
    print("Nothing to save")
