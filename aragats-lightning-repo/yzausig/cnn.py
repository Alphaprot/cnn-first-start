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
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, pyqtSignal
from termios import tcflush, TCIFLUSH

#Settings
json_config = "03_img.json"
trainDataRatio = 0.03 #Percentage of images used for training in relation to all images (where 1 equals 100%)

global trainingData
trainingData = np.zeros((1, 5))

def PathValidator(path):
    valid_path = os.path.isdir(path)
    if path.endswith("/"):
        path = path[:-1] #.strip("/")
    while not valid_path:
        print("Invalid path. Please specify a valid path")
        return None
    else:
        print("Input directory is now " + path + "\n")
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
    app = QApplication(sys.argv)
    gui = MainWindow(path)
    gui.show()
    sys.exit(app.exec_())

class MainWindow(QDialog):
    def __init__(self, path, parent=None):
        super(MainWindow, self).__init__(parent)

        self.outputPath = path
        self.totalFiles = len([name for name in os.listdir(self.outputPath) if os.path.isfile(os.path.join(self.outputPath, name))])
        self.reviewBuffer = []
        self.progress = 0
        for self.x in range(0, int(trainDataRatio*self.totalFiles)):
            img = Image.open(self.outputPath + "/" + random.choice([name for name in os.listdir(self.outputPath) if os.path.isfile(os.path.join(self.outputPath, name))]))
            #Hinweis: Möglichkeit, dass gleiches Bild zweimal angezeigt wird! Verhindern?
            self.reviewBuffer.append(img)
        
        self.xPos = None
        self.yPos = None   
        
        self.createImagePlaceholder()
        self.createTopRightGroupBox()
        self.createBottomRightGroupBox()
        self.createBottomGroupBox()
        print(self.progress)
        
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.imagePlaceholder, 1, 0, 2, 1)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        mainLayout.addWidget(self.bottomGroupBox, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("Lightning Classificator")

       # self.selectToolButton.clicked.connect(self.selectTool)

        self.lightningYes.clicked.connect(self.checkIfactionIsDone)
        self.lightningNo.clicked.connect(self.checkIfactionIsDone)

        self.sky2gnd.clicked.connect(self.checkIfactionIsDone)
        self.sky2sky.clicked.connect(self.checkIfactionIsDone)
        self.burst.clicked.connect(self.checkIfactionIsDone)

    def createImagePlaceholder(self):
        self.imagePlaceholder = QGroupBox("Preview")
        self.img_label = QLabel()
        self.currentImg = ImageQt(self.reviewBuffer[self.progress])
        self.pixmap = QPixmap.fromImage(self.currentImg) 
        self.img_label.setPixmap(self.pixmap)
        print("Displaying image %d" % (self.progress +1))
        self.selectToolButton = QPushButton("Select Tool (Click to draw)")
        self.selectToolButton.setEnabled(False)
        
        layout = QVBoxLayout()
        layout.addWidget(self.selectToolButton)
        layout.addWidget(self.img_label)
        layout.addStretch(1)
        self.imagePlaceholder.setLayout(layout)    

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Picture contains lightning:")
        
        self.lightningYes = QRadioButton("Yes")
        self.lightningNo = QRadioButton("No")

        self.radioButtons = QButtonGroup()
        self.radioButtons.addButton(self.lightningYes, -1)
        self.radioButtons.addButton(self.lightningNo, -1)

        layout = QVBoxLayout()
        layout.addWidget(self.lightningYes)
        layout.addWidget(self.lightningNo)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Type of lightning (please check all applicable):")
        self.sky2gnd = QCheckBox("Sky to ground")
        self.sky2sky = QCheckBox("Sky to sky")
        self.burst = QCheckBox("Burst")

        self.bottomRightGroupBox.setEnabled(False)

        layout = QGridLayout()
        layout.addWidget(self.sky2gnd, 0, 0, 1, 2)
        layout.addWidget(self.sky2sky, 1, 0, 1, 2)
        layout.addWidget(self.burst, 2, 0, 1, 2)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def createBottomGroupBox(self):
        self.bottomGroupBox = QGroupBox("Progress")
        self.progressBar = QProgressBar()
        closeButton = QPushButton("Close")
        nextButton = QPushButton("Next")
        self.numericProgress = "Image %d of %d total images" % ((self.progress + 1), len(self.reviewBuffer))
        self.progressLabel = QLabel(self.numericProgress)

        self.progressBar.setMinimum = 0
        self.progressBar.setMaximum = self.totalFiles*trainDataRatio
        nextButton.clicked.connect(self.nextImage) 
        closeButton.clicked.connect(self.close)

        layout = QGridLayout()
        layout.addWidget(self.progressLabel, 0, 0)
        layout.addWidget(self.progressBar, 1, 0)
        layout.addWidget(closeButton, 1, 1)
        layout.addWidget(nextButton, 1, 2)
        self.bottomGroupBox.setLayout(layout)

    def nextImage(self):
        global trainingData
        label1 = None
        label2 = None
        
        if self.checkIfactionIsDone() is "Done":
            if self.lightningYes:
                if self.sky2gnd.isChecked() and self.sky2sky.isChecked():
                    label1 = 3
                elif self.sky2gnd.isChecked():
                    label1 = 1
                elif self.sky2sky.isChecked():
                    label1 = 2    
            else:
                label1 = 0
            if self.burst.isChecked():
                label2 = 1
            else:
                label2 = 0        
            self.img_path = self.reviewBuffer[self.progress].filename
            self.img_name = os.path.basename(self.img_path)
            trainingData = np.vstack((trainingData, [self.img_name, label1, label2, self.xPos, self.yPos]))
            self.progress = self.progress + 1
            if (self.progress) == len(self.reviewBuffer):
                print("You created the following train data:\n")
                trainingData = np.delete(trainingData, 0, 0)
                print(trainingData)
                QApplication.exit(0)
            else:   
                self.currentImg = ImageQt(self.reviewBuffer[self.progress])
                self.pixmap = QPixmap.fromImage(self.currentImg) 
                self.img_label.setPixmap(self.pixmap)
                print("Displaying image %d" %(self.progress +1))
                self.sky2gnd.setChecked(False)
                self.sky2sky.setChecked(False)
                self.burst.setChecked(False)
                self.bottomRightGroupBox.setEnabled(False)
                self.radioButtons.setExclusive(False)
                self.lightningYes.setChecked(False)
                self.lightningNo.setChecked(False)
                self.radioButtons.setExclusive(True)
                self.progressBar.setValue(int((self.progress+1)*(100/len(self.reviewBuffer))))
                self.numericProgress = "Image %d of %d total images" % ((self.progress + 1), len(self.reviewBuffer))
                self.progressLabel.setText(self.numericProgress)
                self.xPos = None
                self.yPos = None

        else:
            print("Please make sure you answer ever question!") 

    def checkIfactionIsDone(self):
        if self.lightningYes.isChecked():
            self.bottomRightGroupBox.setEnabled(True)
            print("Lightning yes")
        if self.lightningNo.isChecked():
            self.bottomRightGroupBox.setEnabled(False)
            print("Lightning no!")
            return "Done"    
        if self.sky2gnd.isChecked() or self.sky2sky.isChecked() or self.burst.isChecked():
            print("Enabling Select Tool")
            self.selectToolButton.setEnabled(True)
        #if self.xPos is not None and self.yPos is not None:
            return "Done"   

# RUBBERBAND! https://wiki.python.org/moin/PyQt/Selecting%20a%20region%20of%20a%20widget
# https://stackoverflow.com/questions/47102224/pyqt-draw-selection-rectangle-over-picture

class GraphicsView(QGraphicsView):
    rectChanged = pyqtSignal(QRect)

    def __init__(self, *args, **kwargs):
        QGraphicsView.__init__(self, *args, **kwargs)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.setMouseTracking(True)
        self.origin = QPoint()
        self.changeRubberBand = False

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberBand.setGeometry(QRect(self.origin, QSize()))
        self.rectChanged.emit(self.rubberBand.geometry())
        self.rubberBand.show()
        self.changeRubberBand = True
        QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.changeRubberBand:
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.rectChanged.emit(self.rubberBand.geometry())
        QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.changeRubberBand = False
        QGraphicsView.mouseReleaseEvent(self, event)

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

if not os.path.exists(imgpath + "/bg_subtraction"):
    os.makedirs(imgpath + "/bg_subtraction")

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
            inv_outfile = imgpath + "/bg_subtraction/" + "1_aragats-%04d.jpg" % img
            imgin = Image.open(infile)
            process = ImageChops.subtract(imgin, img_compare)
            imgout = ImageChops.invert(process)
            imgout.save(inv_outfile)
            globalCounter += 1

    else:
        print("Invalid format or file not found!\n")

print(str(globalCounter) + " image files have been successfully converted!\n") #counter shows wrong value due to variable length of one seq
print("The results have been saved to " + imgpath + "/bg_subtraction/\n")
print("")
outputPath = imgpath + "/bg_subtraction/"
operatingPrompt(outputPath)
