# Place the script into the directory containing the images that should be sliced
# Note that only images whose filename-string starts with a '2' will be taken into account
# The script will create two folders (/3_split contains the labels whereas /4_split contains the corresponding images)
#  
import os
from PIL import Image

filepath = os.path.dirname(os.path.realpath(__file__))
sliceX = 8
sliceY = 5

for img in os.listdir(filepath):
    if img.startswith("2") and img.endswith(".jpg"):
        labelImg = Image.open(img)
        oldName = labelImg.filename
        newName = oldName[1:14]
        w, h = labelImg.size
        wStep = w/sliceX
        hStep = h/sliceY
        for i in range(0, sliceX):
            for j in range(0, sliceY):
                crop = labelImg.crop(((i*wStep), (j*hStep), ((i+1)*wStep), ((j+1)*hStep)))
                if not os.path.exists(filepath + "/3_split/"):
                    os.makedirs(filepath + "/3_split/")
                crop.save("%s/3_split/3%s-%02d%02d.jpg" % (filepath, newName, i, j))
        print("Filepath is: %s" %filepath)        
        try:        
            referenceImg = Image.open(filepath +"/1%s.jpg" % newName)
        except IOError:
            print("No corresponding image named %s for %s could be found!\n" % (referenceImg.filename, labelImg.filename))          

        if (w, h == referenceImg.size):
            for i in range(0, sliceX):
                for j in range(0, sliceY):
                    crop = referenceImg.crop(((i*wStep), (j*hStep), ((i+1)*wStep), ((j+1)*hStep)))
                    if not os.path.exists(filepath + "/4_split/"):
                        os.makedirs(filepath + "/4_split/")
                    crop.save("%s/4_split/4%s-%02d%02d.jpg" % (filepath, newName, i, j))
        else:
            print("Size mismatch!")
