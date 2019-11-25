# Place the script into the directory containing the images that should be sliced
# Note that only images whose filename-string starts with a '2' will be taken into account
#  
import os
from PIL import Image

filepath = os.path.dirname(os.path.realpath(__file__))
sliceX = 8
sliceY = 5

for img in os.listdir(filepath):
    if img.startswith("2") and img.endswith(".jpg"):
        inImg = Image.open(img)
        oldName = inImg.filename
        newName = oldName[1:14]
        w, h = inImg.size
        wStep = w/sliceX
        hStep = h/sliceY
        for i in range(0, sliceX):
            for j in range(0, sliceY):
                crop = inImg.crop(((i*wStep), (j*hStep), ((i+1)*wStep), ((j+1)*hStep)))
                if not os.path.exists(filepath + "/3_split/"):
                    os.makedirs(filepath + "/3_split/")
                crop.save("%s/3_split/3%s-%02d%02d.jpg" % (filepath, newName, i, j))

