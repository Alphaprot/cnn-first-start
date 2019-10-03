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
from PIL.ImageQt import ImageQt
from getch import getch, pause
from PyQt5 import QtWidgets, QtGui, QtCore
from termios import tcflush, TCIFLUSH

#Settings
json_config = "03_img.json"
trainDataRatio = 0.1 #Percentage of images used for training in relation to all images (where 1 equals 100%)

global trainingData
trainingData = np.zeros((4,1))

def PathValidator(path):
    valid_path = os.path.isdir(path)
    if path.endswith("/"):
        path = path[:-1] #.strip("/")
    while not valid_path:
        print("Invalid path. Please specify a valid path")
        return None
    else:
        print("Input directory is now" + path + "\n")
        return path
        


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
            tcflush(sys.stdin, TCIFLUSH)
            continue

    if choice == "1":
        if not path:
            print(path)
            print("You skipped the previous step so no images have been converted (and thus cannot be " \
             "used for training!\n")
            operatingPrompt(None)
        else:
            createTrainDataset(path)
    elif choice == "2":
        print(path)
        loadTrainData()
    elif choice == "3":
        if not path:
            print("No images have been converted because you skipped the previous step.")
            operatingPrompt(None)
        else:
            showImages(path)

def createTrainDataset(path):
    app = QtWidgets.QApplication(sys.argv)
    gui = Window(path)
    gui.setupGui()
    gui.show()
    sys.exit(app.exec_())

class Window(QtWidgets.QMainWindow):
    def __init__(self, path):
        super(Window, self).__init__()
        self.outputPath = path
        self.totalFiles = len([name for name in os.listdir(self.outputPath) if os.path.isfile(os.path.join(self.outputPath, name))])
        print(self.totalFiles)
        self.reviewBuffer = []
        self.progress = 0
  
    def setupGui(self):
        for self.x in range(0, int(trainDataRatio*self.totalFiles)):
            self.img = Image.open(self.outputPath + "/" + random.choice([name for name in os.listdir(self.outputPath) if os.path.isfile(os.path.join(self.outputPath, name))]))
            #Hinweis: Möglichkeit, dass gleiches Bild zweimal angezeigt wird! Verhindern?
            self.reviewBuffer.append(self.img)
        self.grid = QtWidgets.QGridLayout(self)
        self.setLayout = self.grid
        self.group1 = QtWidgets.QGroupBox("Picture contains lightning:")
        self.lightningYes = QtWidgets.QRadioButton("Yes")
        self.lightningNo = QtWidgets.QRadioButton("No")
        self.group2 = QtWidgets.QGroupBox("Type of lightning (please check all applicable):")
        self.sky2gnd = QtWidgets.QCheckBox("Sky to ground")
        self.sky2sky = QtWidgets.QCheckBox("Sky to sky")
        self.burst = QtWidgets.QCheckBox("Burst")
        self.selectToolButton = QtWidgets.QPushButton()
        self.selectToolButton.setEnabled(False)
        self.group2.setEnabled(False)
        self.group3 = QtWidgets.QGroupBox()

        self.img_label = QtWidgets.QLabel()
        print(self.progress)
        print(self.outputPath)
        print(len(self.reviewBuffer))
        self.currentImg = ImageQt(self.reviewBuffer[self.progress])
        self.pixmap = QtGui.QPixmap.fromImage(self.currentImg)
        self.img_label.setPixmap(self.pixmap)
        self.button_next = QtWidgets.QPushButton('Next')
        self.button_quit = QtWidgets.QPushButton('Cancel')
        self.progBar = QtWidgets.QProgressBar()
        self.progBar.setMinimum = 0
        self.progBar.setMaximum = self.totalFiles*trainDataRatio

        self.group1Layout = QtWidgets.QVBoxLayout()
        self.group1Layout.addWidget(self.lightningYes)
        self.group1Layout.addWidget(self.lightningNo)
        self.group1.setLayout(self.group1Layout)

        self.group2Layout = QtWidgets.QVBoxLayout()
        self.group2Layout.addWidget(self.sky2gnd)
        self.group2Layout.addWidget(self.sky2sky)
        self.group2Layout.addWidget(self.burst)
        self.group2.setLayout(self.group2Layout)

        self.group3Layout = QtWidgets.QHBoxLayout()
        self.group3Layout.addWidget(self.button_next)
        self.group3Layout.addWidget(self.button_quit)
        self.group3.setLayout(self.group3Layout)

        self.grid.addWidget(self.img_label, 0, 1)
        self.grid.addWidget(self.group1, 1, 1)
        self.grid.addWidget(self.group2, 1, 2)
        self.grid.addWidget(self.progBar, 0, 3)
        self.grid.addWidget(self.group3, 1, 3)

        def SelectTool(self):
            self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle)
            self.origin = QtWidgets.QPoint()

            def mousePressEvent(self, event):
                if event.button() == QtGui.MouseButton.LeftButton:
                    self.origin = QtGui.QPoint(event.pos())
                    self.rubberBand.setGeometry(QtGui.QRect(self.origin, QtGui.QSize()))
                    self.rubberBand.show()

            def mouseMoveEvent(self, event):
                if not self.orgin.isNull():
                    self.rubberBand.setGeometry(QtGui.QRect(self.origin, event.pos()).normalized())

            def mouseReleaseEvent(self, event):
                if event.button() == QtGui.MouseButton.LeftButton:
                    self.rubberBand.hide()

        def ProbeSubmissionIntegrity(self):
            if self.lightningNo.isChecked():
                saveTrainData(self)
                return
            elif self.lightningYes.isChecked():
                if self.sky2gnd.isChecked() or self.sky2sky.isChecked() or self.burst.isChecked():
                    saveTrainData(self)
                    return
                else:
                    showNoIntegrityWarning(self)
            else:
                showNoIntegrityWarning(self)
        def quitDialog(self):
            print("foo")

        def showNoIntegrityWarning(self):
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("Please provide every requested information")
            self.msg.setInformativeText("The missing fields are highlighted")
            self.msg.setWindowTitle("Missing entries detected!")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.buttonClicked.connect(highlightMissing)


        def highlightMissing(self):
            print("Not implemented yet")

        def saveTrainData(self):
            if self.lightningYes:
                if self.sky2gnd.isChecked() and self.sky2sky.isChecked():
                    self.label = 3
                elif self.sky2gnd.isChecked():
                    self.label = 1
                else:
                    self.label = 2
            else:
                self.label = 0
            self.img_path = self.reviewBuffer[self.progress].filename
            self.img_name = os.path.basename(self.img_path)
            trainingData = np.append((self.img_name, self.filename, self.xPos, self.yPos))

        def group1Choice(self):
            if self.lightningYes.isChecked():
                print("User selected 'lightning' \n Enabling further tasks")
                self.group2.setEnabled(True)
                self.selectToolButton.setEnabled(True)
            if self.lightningNo.isChecked():
                print("User slected 'no lightning'")

        self.lightningYes.toggled.connect(group1Choice)
        self.lightningNo.toggled.connect(group1Choice)
        self.button_next.clicked.connect(ProbeSubmissionIntegrity)
        self.button_quit.clicked.connect(quitDialog)
        self.selectToolButton.clicked.connect(SelectTool)


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
        imgpath = PathValidator(imgpath)
        break
    if imgpath.lower() == "skip":
        print("Skipping...\n"+
        "Provide a path to already converted images or leave empty\n")
        imgpath_secondary = input()
        if PathValidator(imgpath_secondary):
            imgpath_secondary = PathValidator(imgpath_secondary)
            print(imgpath_secondary)
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

globalCounter = 0
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
            globalCounter += 1

    else:
        print("Invalid format or file not found!\n")

print(str(globalCounter) + " image files have been successfully converted!\n") #counter shows wrong value due to variable length of one seq
print("The results have been saved to " + imgpath + "/bg_substraction/\n")
print("")
outputPath = imgpath + "/bg_substraction/"
operatingPrompt(outputPath)
