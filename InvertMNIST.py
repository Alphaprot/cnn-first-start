import keras
from keras.datasets import mnist
import numpy as np
import csv
#from scipy.misc import imsave
#from skimage import util
import os
import math
import matplotlib.pyplot as plt

mnist_old = mnist.load_data()
for data in mnist_old :
    label = data[0]
    pixels = data[1:]
    pixels = np.array(pixels, dtype='uint8')
    pixels = pixels.reshape([28, 28])

    plt.title('Label was (label)'.format(label=label))
    plt.imshow(pixels, cmap='grey')
    plt.show()
    
