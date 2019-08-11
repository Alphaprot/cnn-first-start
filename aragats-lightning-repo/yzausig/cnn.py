from __future__ import print_function

import numpy as np
import os
import platform
import subprocess
import glob
import json
import math
import tensorflow as tf
from PIL import Image, ImageChops
from getch import getch, pause

json_config = "03_img.json"
global trainingDat
trainingData = np.zeros((3,1))

def operatingPrompt(path):
    question = "Do you want to:\n"
    option1 = "[1] Create training data from the converted images\n"
    option2 = "[2] Train neural network by providing existing training data as .npy\n"
    option3 = "[3] Display images\n"
    options = [question, option1, option2, option3]

    prompt = [" [Enter digit] "]
    validInput =    {"1":1,
                    "2":2,
                    "3":3}

    while True:
        print(*options + prompt)
        choice = input().lower()
        if choice in validInput:
            validInput = choice
            break
        else:
            print("Please respond with a number from 1 to 3!\n")
            continue

    if choice == "1":
        createTrainDataset()
    elif choice == "2":
        loadTrainData()
    elif choice == "3":
        showImages(path)

def createTrainDataset():
    print("foo")

def loadTrainData():
    print("Please specify the abs path to the training data file:\n")
    actionComplete = False
    while not actionComplete:
        trainFile = input()
        validTrainFile = os.path.isfile(trainFile)
        if not validTrainFile:
            print("Train data file does not exist. Please check the file or correct the path")
        else:
            if trainFile.endswith(".npy"):
                print("Selected training file: " + trainFile + "\n")
                trainingData = np.load(trainFile)
                actionComplete = True
                break
            else:
                print("Please select a valid '.npy' file!")
    if trainingData.ndim == 2:
        if np.size(trainingData) == 4:
            trainCNN()
        else:
            print("Only an array of the shape (4, n) can be used where \n 1st column = filename \n",
            "2nd column = label \n 3rd column = type of lightning \n 4th column = area of image",
            "with lightning \n \nSee the documentation for further instructions!")
    else:
        print("Only an array of the shape (4, n) can be used where \n 1st column = filename \n",
        "2nd column = label \n 3rd column = type of lightning \n 4th column = area of image ",
        "with lightning \n \nSee the documentation for further instructions!")


def trainCNN():
    print("Nothing here")

def showImages(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

print("Please specify input directory as an abs path [or enter skip",
"to skip this step]:\n")
pathCheck = False
while pathCheck == False:
    imgpath = input()
    if imgpath.lower() == "skip":
        print("Skipping")
        operatingPrompt(None)

    if imgpath.endswith("/"):
        imgpath = imgpath[:-1] #.strip("/")
    valid_path = os.path.isdir(imgpath)
    while not valid_path:
        print("Invalid path. Please specify a valid path")
        break
    else:
        print("Input directory is now" + imgpath + "\n")
        pathCheck = True
        break

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
outputPath = imgpath + "/bg_substraction/"
operatingPrompt(outputPath)
