from __future__ import print_function

import numpy as np
import os
import glob
import json
import math
import tensorflow as tf
from PIL import Image, ImageChops

json-config = "03_img.json"

def removeBackground:
    print("Please specify input directory as an abs path:\n")
    imgpath = str(input()

    while(os.path.isdir(imgpath) == False):
        print("Invalid path. Please specify a valid path")
    else:
        print("Input directory is now" + imgpath + "\n")
        break


with open(json-config) as fconf
    data = json.load(fconf)

if type(data) is not dict:
       print("Error: config file format error - dict is required\n")
       exit()

    if 'filelist' not in data.keys():
       print("Error: the key 'filelist' is not exisiting.")
       exit()

filelist = data['filelist']
seqlist = data['seqlist']

for seq in seqlist:
    ref = seq['ref']
    refimg = imgpath + "/aragats-" + imgnumber
    extensionlist = []
    for i in range 4-(int(math.log10(seq['ref']))+1):
        extensionlist.append("0")
    extensionlist.append(seq['ref'}])
    imgnumber = ''.join(extensionlist)

    if(refimg.lower().endswith('.jpg')):
        reference = Image.open(refimg)
    else:
        print("Not a JPGEG!\n")
