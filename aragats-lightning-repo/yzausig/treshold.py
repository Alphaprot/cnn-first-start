from PIL import Image
import os
import numpy as np

treshold = 99

path = "/home/yanik/Downloads/cnn-first-start-master/aragats-raw/bg_subtraction/"
for img in os.listdir(path):
    if img.endswith('.jpg'):
        inImg = Image.open(os.path.join(path, img))
        rawHistogram = inImg.histogram()
        for x in range(0, treshold):
            rawHistogram[x] = 0
        histogram = np.reshape(rawHistogram, (1, 256)).T
        print(img)
        print(histogram)

def sliceInParts(path):
    for example in os.listdir(path):
        if example.endswith('.jpg'):
            inImg = Image.open(os.path.join(path, example))
            x, y = inImg.size()
            for w in range(0, 4):
                for h in range (0, 2):
                    outImg = inImg.crop((0+(x/5)*w), (0+(y/3)*h), ((x/5)*(w+1)), ((y/3)*h+1))
                    outImg.save()


        
sliceInParts("/home/yannik/Downloads/cnn-first-start/aragats-lightning-repo/yzausig/training-expamples/")