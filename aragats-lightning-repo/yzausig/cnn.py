from __future__ import print_function

import numpy as np
import os
import sys
import platform
import subprocess
import glob
import json
import math
import random
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, BatchNormalization, Activation
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.constraints import maxnorm
from keras.utils import np_utils
from PIL import Image, ImageChops
from getch import getch, pause
from PyQt5.QtWidgets import QApplication, QLabel, QSlider, QProgressBar, QRadioButton, QPushButton, QCheckBox, QMessageBox, QGridLayout, \
        QGroupBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPen, QColor
from termios import tcflush, TCIFLUSH

#Settings
json_config = "03_img.json"
trainDataRatio = 0.1 #Percentage of images used for training in relation to all images (where 1 equals 100%)

global trainingData
trainingData = np.zeros((4,1))
app = QApplication([])

def PathValidator(path):
    valid_path = os.path.isdir(path)
    if path.endswith("/"):
        path = path[:-1] #.strip("/")
    while not valid_path:
        print("Invalid path. Please specify a valid path")
        return False
        break
    else:
        print("Input directory is now" + path + "\n")
        return True


def operatingPrompt(outputPath):
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
            tcflush(sys.stdin, TCIFLUSH)
            continue

    if choice == "1":
        if not outputPath:
            print("You skipped the previous step so no images have been converted (and thus cannot be " \
             "used for training!\n")
            operatingPrompt(None)
        else:
            createTrainDataset(outputPath)
    elif choice == "2":
        print(outputPath)
        loadTrainData()
    elif choice == "3":
        if not outputPath:
            print("No images have been converted because you skipped the previous step.")
            operatingPrompt(None)
        else:
            showImages(outputPath)

def createTrainDataset(outputPath):

    totalFiles = len([name for name in os.listdir(outputPath) if os.path.isfile(outputPath + name)])
    print(totalFiles)
    reviewBuffer = []
    progress = 0
    for x in range(0, int(trainDataRatio*totalFiles)):
        img = Image.open(outputPath + random.choice([img_file for img_file in os.listdir(outputPath) if os.path.isfile(os.path.join(outputPath, img_file))]))
        #Hinweis: Möglichkeit, dass gleiches Bild zweimal angezeigt wird! Verhindern?
        print(img)
        reviewBuffer.append(img)
    app.setStyle('Fusion')
    grid = QGridLayout()
    group1 = QGroupBox("Picture contains lightning:")
    lightningYes = QRadioButton("Yes")
    lightningNo = QRadioButton("No")
    group2 = QGroupBox("Type of lightning (please check all applicable):")
    sky2gnd = QCheckBox("Sky to ground")
    sky2sky = QCheckBox("Sky to sky")
    burst = QCheckBox("Burst")
    group2.setEnabled(False)
    group3 = QGroupBox()

    img_label = QLabel()
    print(reviewBuffer)
    pixmap = QPixmap(reviewBuffer[progress])
    img_label.setPixmap(pixmap)
    button_next = QPushButton('Next')
    button_quit = QPushButton('Cancel')
    progBar = QProgressBar()
    progBar.setMinimum = 0
    progBar.setMaximum = totalFiles*trainDataRatio

    group1Layout = QVBoxLayout()
    group1Layout.addWidget(lightningYes)
    group1Layout.addWidget(lightningNo)
    group1.setLayout(group1Layout)

    group2Layout = QVBoxLayout()
    group2Layout.addWidget(sky2gnd)
    group2Layout.addWidget(sky2sky)
    group2Layout.addWidget(burst)
    group2.setLayout(group2Layout)

    group3Layout = QHBoxLayout()
    group3Layout.addWidget(button_next)
    group3Layout.addWidget(button_quit)
    group3.setLayout(group3Layout)

    grid.addWidget(img_label, 0, 1)
    grid.addWidget(group1, 1, 1)
    grid.addWidget(group2, 1, 2)
    grid.addWidget(progBar, 0, 3)
    grid.addWidget(group3, 1, 3)

    lightningYes.toggled.connect(group1Choice)
    lightningNo.toggled.connect(group1Choice)
    button_next.clicked.connect(ProbeSubmissionIntegrity)
    button_quit.clicked.connect(quitDialog)
    app.exec_()

    def group1Choice():
      if lightningYes.isChecked():
        print("User selected 'lightning' \n Enabling further tasks")
        group2.setEnabled(True)
        overlay.setEnabled(True)
      if lightningNo.isChecked():
        print("User slected 'no lightning'")

    def SelectTool():
        rubberBand = QRubberBand(QRubberBand.Rectangle)
        origin = QPoint()

        def mousePressEvent(event):
            if event.button() == Qt.LeftButton:
                origin = QPoint(event.pos())
                rubberBand.setGeometry(QRect(origin, QSize()))
                rubberBand.show()

        def mouseMoveEvent(event):
            if not orgin.isNull():
                rubberBand.setGeometry(QRect(origin, event.pos()).normalized())

        def mouseReleaseEvent(event):
            if event.button() == Qt.LeftButton:
                rubberBand.hide()

    def ProbeSubmissionIntegrity():
        if lightningNo.isChecked():
            saveTrainData()
            return
        elif lightningYes.isChecked():
            if sky2gnd.isChecked() or sky2sky.isChecked() or burst.isChecked():
                saveTrainData()
                return
            else:
                showNoIntegrityWarning()
        else:
            showNoIntegrityWarning()
    def quitDialog():
        print("foo")

    def showNoIntegrityWarning():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Please provide every requested information")
        msg.setInformativeText("The missing fields are highlighted")
        msg.setWindowTitle("Missing entries detected!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(highlightMissing)

    def highlightMissing():
        print("Not implemented yet")

    def saveTrainData():
        if lightningYes:
            if sky2gnd.isChecked() and sky2sky.isChecked():
                label = 3
            elif sky2gnd.isChecked():
                label = 1
            else:
                label = 2
        else:
            label = 0
        img_path = reviewBuffer[progress].filename
        img_name = os.path.basename(img_path)
        trainingData = np.append((img_name, filename, xPos, yPos))



    '''def drawOverlay(): # Inspired by snow's answer on  https://stackoverflow.com/questions/39614777/how-to-draw-a-proper-grid-on-pyqt
        gridLines = []
        setSceneRect(0, 0, img_label.width)

        for line in gridLines(visible = True)
            line.setVisible(visible)

    class NewLabel(QLabel):
        def __init__(self, text):
            super(NewLabel, self).__init__(text)

        def resizeEvent(self, event):
            width = self.width()
            height = self.height()
'''
# RUBBERBAND! https://wiki.python.org/moin/PyQt/Selecting%20a%20region%20of%20a%20widget
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
            "2nd column = label \n 3rd column = xPos of area \n 4th column = yPos of area",
            "\n \nSee the documentation for further instructions!")
    else:
        print("Only an array of the shape (4, n) can be used where \n 1st column = filename \n",
        "2nd column = label \n 3rd column = type of lightning \n 4th column = area of image ",
        "with lightning \n \nSee the documentation for further information!")


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
while True:
    imgpath = input()
    if PathValidator(imgpath):
        break
    if imgpath.lower() == "skip":
        print("Skipping...\n"+
        "Provide a path to already converted images or leave empty\n")
        imgpath_secondary = input().lower()
        if PathValidator(imgpath_secondary):
            operatingPrompt(imgpath_secondary)
        else:
            operatingPrompt(None)

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
            imgin = Image.open(infile)
            process = ImageChops.subtract(imgin, img_compare)
            imgout = ImageChops.invert(process)
            imgout.save(inv_outfile)

    else:
        print("Invalid format or file not found!\n")

print(str(counter) + " image files have been successfully converted!\n")
print("The results have been saved to " + imgpath + "/bg_substraction/\n")
print("")
outputPath = imgpath + "/bg_substraction/"
operatingPrompt(outputPath)
