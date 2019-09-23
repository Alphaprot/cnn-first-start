from PyQt5.QtWidgets import QApplication, QLabel, QSlider, QProgressBar, QRadioButton, QPushButton, QCheckBox, QMessageBox, QGridLayout, \
        QGroupBox, QVBoxLayout, QHBoxLayout, QWidget, QDialog
from PyQt5.QtGui import QPixmap, QPen, QColor


class Gui(object):
    def setupUI(self, gui):
        self.grid = QGridLayout()
        self.group1 = QGroupBox("Picture contains lightning:")
        self.lightningYes = QRadioButton("Yes")
        self.lightningNo = QRadioButton("No")
        self.group2 = QGroupBox("Type of lightning (please check all applicable):")
        self.sky2gnd = QCheckBox("Sky to ground")
        self.sky2sky = QCheckBox("Sky to sky")
        self.burst = QCheckBox("Burst")
        self.group2.setEnabled(False)
        self.group3 = QGroupBox()

        self.img_label = QLabel()
        self.pixmap = QPixmap("wumpus.png")
        self.img_label.setPixmap(self.pixmap)
        self.button_next = QPushButton('Next')
        self.button_quit = QPushButton('Cancel')
        self.progBar = QProgressBar()
        self.progBar.setMinimum = 0
        self.progBar.setMaximum = 100

        self.group1Layout = QVBoxLayout()
        self.group1Layout.addWidget(self.lightningYes)
        self.group1Layout.addWidget(self.lightningNo)
        self.group1.setLayout(self.group1Layout)

        self.group2Layout = QVBoxLayout()
        self.group2Layout.addWidget(self.sky2gnd)
        self.group2Layout.addWidget(self.sky2sky)
        self.group2Layout.addWidget(self.burst)
        self.group2.setLayout(self.group2Layout)

        self.group3Layout = QHBoxLayout()
        self.group3Layout.addWidget(self.button_next)
        self.group3Layout.addWidget(self.button_quit)
        self.group3.setLayout(self.group3Layout)

        self.grid.addWidget(self.img_label, 0, 1)
        self.grid.addWidget(self.group1, 1, 1)
        self.grid.addWidget(self.group2, 1, 2)
        self.grid.addWidget(self.progBar, 0, 3)
        self.grid.addWidget(self.group3, 1, 3)

        def group1Choice(self):
            if self.lightningYes.isChecked():
                print("User selected 'lightning' \n Enabling further tasks")
                self.group2.setEnabled(True)
                self.overlay.setEnabled(True)
            if self.lightningNo.isChecked():
                print("User slected 'no lightning'")

        def ProbeSubmissionIntegrity(self):
            if self.lightningNo.isChecked():
                saveTrainData()
                return
            elif self.lightningYes.isChecked():
                if self.sky2gnd.isChecked() or self.sky2sky.isChecked() or self.burst.isChecked():
                    saveTrainData()
                    return
                else:
                    showNoIntegrityWarning()
            else:
                showNoIntegrityWarning()
        def quitDialog(self):
            print("foo")

        def showNoIntegrityWarning(self):
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText("Please provide every requested information")
            self.msg.setInformativeText("The missing fields are highlighted")
            self.msg.setWindowTitle("Missing entries detected!")
            self.msg.setStandardButtons(QMessageBox.Ok)
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

        self.lightningYes.toggled.connect(group1Choice)
        self.lightningNo.toggled.connect(group1Choice)
        self.button_next.clicked.connect(ProbeSubmissionIntegrity)
        self.button_quit.clicked.connect(quitDialog)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    gui = QDialog()
    ui = Gui()
    ui.setupUI(gui)
    gui.show()
    sys.exit(app.exec_())


'''def SelectTool():
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
'''
