from __future__ import print_function

import numpy as np
import os
import glob
import json
import math
import tensorflow as tf
from PIL import Image, ImageChops
from getch import getch, pause

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
    counter = 0

    if not os.path.exists(imgpath + "/bg_substraction"):
        os.makedirs(imgpath + "/bg_substraction")

    for seq in seqlist:
        ref = seq['ref']
        extensionlist = []


        #for i in range (4-(int(math.log10(seq['ref']))+1)):
        #    extensionlist.append(0)
        #extensionlist.append(seq['ref'])
        #imgnumber = int(''.join(str(extensionlist)))

        refimg = imgpath + "/aragats-%04d.jpg" % ref
        print(imgpath)
        if(os.path.isfile(refimg)):
            img_compare = Image.open(refimg)

            for counter, img in enumerate(seq['images']):
                print(type(img))
                print(str("Opening image no. %04d\n") % img)
                infile = imgpath + "/aragats-%04d.jpg" % img
                inv_outfile = imgpath + "/bg_substraction/" + "1_aragats-%04d.jpg" % img
                input = Image.open(infile)
                process = ImageChops.subtract(input, img_compare)
                out = ImageChops.invert(process)
                out.save(inv_outfile)


        else:
            print("Invalid format or file not found!\n")

    print(str(counter) + " image files have been successfully converted!\n")
    print("The results have been saved to " + imgpath + "/bg_substraction/\n")
    print("")
    question = "Do you want to train the CNN with this data ((N) will quit the program without training)?"
    prompt = " [y/n] "
    choice = raw_input().lower()
    validInput = {"yes": True, "y": True,
                    "no": False, "n": False}

    while True:
        print(question + prompt)
        if choice in validInput:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n')\n")

    if validInput == True:
        trainCNN();
    if validInput == False:
        exit()

def trainCNN():
    print("Nothing here")

removeBackground()
