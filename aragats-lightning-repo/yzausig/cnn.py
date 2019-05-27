from __future__ import print_function

import numpy as np
import os
import glob
import json
import math
import tensorflow as tf
from PIL import Image, ImageChops

json_config = "03_img.json"

def removeBackground():
    print("Please specify input directory as an abs path:\n")
    imgpath = raw_input()
    if imgpath.endswith("/"):
        imgpath = imgpath[:-1] #.strip("/")
    valid_path = os.path.isdir(imgpath)
    while not valid_path:
        print("Invalid path. Please specify a valid path")
    else:
        print("Input directory is now" + imgpath + "\n")

    with open(json_config) as fconf:
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
        extensionlist = []


        #for i in range (4-(int(math.log10(seq['ref']))+1)):
        #    extensionlist.append(0)
        #extensionlist.append(seq['ref'])
        #imgnumber = int(''.join(str(extensionlist)))

        refimg = imgpath + "/aragats-%04d.jpg" %ref
        print(imgpath)
        if(os.path.isfile(refimg)):
            print("Klappt")
            #reference = Image.open(refimg)
        else:
            print("Invalid format or file not found!\n")

        print(refimg +"\n")
        #or img in seq['images']:
        #input = imgpath + "aragats-" + imgnumber

removeBackground()
