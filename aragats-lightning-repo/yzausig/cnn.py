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
desiredArrayShape = '(3,3)'

def removeBackground():
    print("Please specify input directory as an abs path:\n")
    imgpath = raw_input()
    if imgpath.endswith("/"):
        imgpath = imgpath[:-1] #.strip("/")
    valid_path = os.path.isdir(imgpath)
    while not valid_path:
        print("Invalid path. Please specify a valid path")
        exit()
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

def trainDataset():
    if trainingData.shape
def loadTrainData():
    actionComplete = False
    while not actionComplete():
        print("Please specify the abs path to the training data file:\n")
        trainFile = raw_input()
        validTrainFile = os.path.isfile(trainFile)
        if not validTrainFile:
            print("Train data file does not exist. Please check the file or correct the path")
        else:
            if trainFile.endswith(".npy"):
                print("Selected training file: " + trainFile + "\n")
                global trainingData = np.load(trainFile)
                actionComplete = True
                break()
            else:
                print("Please select a valid '.npy' file!")
    trainCNN()

def trainCNN():
    print("Nothing here")

removeBackground()
question = "Do you want to:\n"
option1 = "[1] Create training data from the converted images\n"
option2 = "[2] Train neural network by providing existing training data as .npy\n"
option3 = "[3] Display images\n"
options = [option1, option2, option3]


prompt = " [Enter digit] "
choice = raw_input().lower()
validInput = {"1":1,
                "2":2,
                "3":3}

while True:
    print(*options + prompt)
    if choice in validInput:
        return valid[choice]
    else:
        print("Please respond with 'yes' or 'no' (or 'y' or 'n')\n")

if validInput == 1:
    trainDataset();
if validInput == 2;
    loadTrainData();
if validInput == 3:
    exit()


'''    validInput = {"1": True, "y": True,
                    "no": False, "n": False}
                            print("Please respond with 'yes' or 'no' (or 'y' or 'n')\n")
'''
