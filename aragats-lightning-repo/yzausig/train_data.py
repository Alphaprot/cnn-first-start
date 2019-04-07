from __future__ import print_function
import os
import numpy as np
import glob
from PIL import Image
from Tkinter import *
import Tkinter as tk
import tkFileDialog as filedialog

class ApplicationGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.title("Lightning - Train Data Classifier")

        self.label1 = Label(master, text="GUI to classify lightning images")
        self.label1.grid(row=0, column=1, padx='5', pady='5')

        self.label2 = Label(master, text="Please specify image path")
        self.label2.grid(row=2, column=1, padx='5', pady='5')

        textEntry = tk.StringVar()
        self.textbox_image_path = Entry(master, textvariable=textEntry)
        self.textbox_image_path.grid(row=3, column=1, padx='5', pady='5')

        self.browse_button = Button(master, text="...", command=self.browseImagePath)
        self.browse_button.grid(row=3, column=2, padx='5', pady='5')

        self.yes_button = Button(master, text="Yes", command=self.lightning)
        self.yes_button.grid(row=5, column=0, padx='5', pady='5')

        self.no_button = Button(master, text="No", command=self.noLighnting)
        self.no_button.grid(row=5, column=1, padx='5', pady='5')

        self.close_button = Button(master, text="Close", command=self.close)
        self.close_button.grid(row=5, column=2, padx='5', pady='5')

    def lightning(self):
        print("You chose 'Lightning' for file " + filename)

    def noLighnting(self):
        print("You chose 'no Lighning' for file " + filename)

    def close(self):
        window = tk.Toplevel(root)
        message = "Please confirm that you want to abort training"
        window.text = Label(window, text = message).grid(row=0, column=1, padx='5', pady='5')
        window.abort_button = Button(window, text ="Abort", command=quit)
        window.abort_button.grid(row=2, column=0, padx='5', pady='5')
        window.return_button = Button(window, text ="Return", command=window.destroy)
        window.return_button.grid(row=2, column=2, padx='5', pady='5')
        #window.return_button = Button(window, text ="Return", command=win.destroy)
        #window.return_button.grid(row=2, column=3, padx='5', pady='5')

    def browseImagePath(self):
        global folder_path
        matrixSize = 32
        filenameList = []
        np.empty([len(filenameList), 2, matrixSize]) #numpy-Array for training data --> 1st tuple: filename 2nd tuple: human classification result (y/n) 3rd tuple: pixel or part of grid
        folder_path = filedialog.askdirectory(mustexist=True, title="Please specify image directory")
        print("Specified image path: " + folder_path)
        textEntry.set(image_path)



root = Tk()
my_gui = ApplicationGUI(root)
root.mainloop()
