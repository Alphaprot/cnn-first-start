from __future__ import print_function
import os
import numpy as np
import glob
from PIL import Image
from Tkinter import Tk, Label, Button, LEFT, RIGHT, TOP, BOTTOM
import Tkinter as tk
import tkFileDialog as filedialog

class ApplicationGUI:
    def __init__(self, master):
        self.master = master
        master.title("Lightning - Train Data Classifier")

        self.label = Label(master, text="GUI to classify lightning images")
        self.label.pack()

        self.label = Label(master, text="Please specify image path", command=self.browseImagePath)
        self.label.pakc()


        self.yes_button = Button(master, text="Yes", command=self.lightning)
        self.yes_button.pack(side=LEFT)

        self.no_button = Button(master, text="No", command=self.noLighnting)
        self.no_button.pack(side=BOTTOM)

        self.close_button = Button(master, text="Close", command=self.close)
        self.close_button.pack(side=RIGHT)

    def lightning(self):
        print("You chose 'Lightning' for file " + filename)

    def noLighnting(self):
        print("You chose 'no Lighning' for file " + filename)

    def close(self):
        window = tk.Toplevel(root)
        message = "Please confirm that you want to abort training"
        window.text = Label(window, text = message).pack()
        window.abort_button = Button(window, text = "Abort", command=quit).pack(LEFT)
        window.return_button = Button(window, text = "Return", command=win.destroy).pack(RIGHT)

    def browseImagePath(self):
        global folder_path
        filename = filedialog.askdirectory()
        folder_path.set(filename)
        print(filename)

matrixSize = 32
filenameList = []
np.empty([len(filenameList), 2, matrixSize]) #numpy-Array for training data --> 1st tuple: filename 2nd tuple: human classification result (y/n) 3rd tuple: pixel or part of grid
folder_path = StringVar()

root = Tk()
my_gui = ApplicationGUI(root)
root.mainloop()
