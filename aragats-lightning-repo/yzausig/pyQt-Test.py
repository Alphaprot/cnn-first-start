from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from PIL.ImageQt import ImageQt
import os


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.createImagePlaceholder()
        self.createTopRightGroupBox()
        self.createBottomRightGroupBox()
        self.createBottomGroupBox()

       
     
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

    def createImagePlaceholder(self):
        self.imagePlaceholder = QGroupBox("Preview")
        img_label = QLabel()
        
        self.currentImg = ImageQt(os.path.dirname(os.path.realpath(__file__)) + "/wumpus.png")
        pixmap = QPixmap.fromImage(self.currentImg)
        img_label.setPixmap(pixmap)
        self.selectToolButton = QPushButton("Select Tool (Click to draw)")
        self.selectToolButton.setEnabled(False)
       
        layout = QVBoxLayout()
        layout.addWidget(self.selectToolButton)
        layout.addWidget(img_label)
        layout.addStretch(1)
        self.imagePlaceholder.setLayout(layout)    

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Picture contains lightning:")
        
        self.lightningYes = QRadioButton("Yes")
        self.lightningNo = QRadioButton("No")

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

        layout = QGridLayout()
        layout.addWidget(self.sky2gnd, 0, 0, 1, 2)
        layout.addWidget(self.sky2sky, 1, 0, 1, 2)
        layout.addWidget(self.burst, 2, 0, 1, 2)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def createBottomGroupBox(self):
        self.bottomGroupBox = QGroupBox("Progress")
        progressBar = QProgressBar()
        closeButton = QPushButton("Close")
        nextButton = QPushButton("Next")

        closeButton.clicked.connect(self.close)

        layout = QHBoxLayout()
        layout.addWidget(progressBar)
        layout.addWidget(closeButton)
        layout.addWidget(nextButton)
        self.bottomGroupBox.setLayout(layout)



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = MainWindow()
    gallery.show()
sys.exit(app.exec_()) 

'''from PIL.ImageQt import ImageQt
from PyQt5 import QtWidgets, QtGui, QtCore
import os
import sys


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupGui()
  
    def setupGui(self):
        self.lightningYes = QtWidgets.QRadioButton("Yes")
        self.lightningNo = QtWidgets.QRadioButton("No")
        self.sky2gnd = QtWidgets.QCheckBox("Sky to ground")
        self.sky2sky = QtWidgets.QCheckBox("Sky to sky")
        self.burst = QtWidgets.QCheckBox("Burst")
        self.selectToolButton = QtWidgets.QPushButton()
        self.selectToolButton.setEnabled(False)
        #self.group2.setEnabled(False)
        self.group3 = QtWidgets.QGroupBox()
   
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
        #self.group2.setEnabled(False)
        self.group3 = QtWidgets.QGroupBox()

        self.img_label = QtWidgets.QLabel()
        
        self.currentImg = ImageQt(os.path.dirname(os.path.realpath(__file__)) + "/wumpus.png")
        self.pixmap = QtGui.QPixmap.fromImage(self.currentImg)
        self.img_label.setPixmap(self.pixmap)
        self.button_next = QtWidgets.QPushButton('Next')
        self.button_quit = QtWidgets.QPushButton('Cancel')
        self.progBar = QtWidgets.QProgressBar()
        self.progBar.setMinimum = 0
        self.progBar.setMaximum = 100

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
                return
            elif self.lightningYes.isChecked():
                if self.sky2gnd.isChecked() or self.sky2sky.isChecked() or self.burst.isChecked():
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

app = QtWidgets.QApplication(sys.argv)
gui = Window()
gui.show()
sys.exit(app.exec_())
'''