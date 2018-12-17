import keras
from keras.datasets import mnist
import numpy as np
import csv
#from scipy.misc import imsave
#from skimage import util
import os
import math
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = mnist.load_data()
for data in x_train [:3]:


    print data
    pixels = np.array(data, dtype='uint8')
    pixels = data.reshape((28, 28))

##   plt.title('Label was (label)'.format(label=label))
    plt.imshow(pixels, cmap='Greys')
    plt.show()
