from __future__ import print_function
import os
import time
import numpy as np
import glob
from PIL import Image, ImageTk
from Tkinter import *
import Tkinter as tk
import tkFileDialog as filedialog

class ApplicationGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.title("Lightning - Train Data Classifier")

        self.matrixSize = 32
        self.filenameList = []
        np.empty([len(self.filenameList), 2, self.matrixSize]) #numpy-Array for training data --> 1st tuple: filename 2nd tuple: human classification result (y/n) 3rd tuple: pixel or part of grid

        self.label1 = Label(master, text="GUI to classify lightning images")
        self.label1.grid(row=0, column=1, padx='5', pady='5')

        self.label2 = Label(master, text="1. Select source first")
        self.label2.grid(row=2, column=0, padx='5', pady='5')

        self.openBrowseWindow = Button(master, text='Browse', command=self.browseWindow)
        self.openBrowseWindow.grid(row=2, column=1, padx='5', pady='5')

        self.yes_button = Button(master, text="Yes", command=self.lightning)
        self.yes_button.grid(row=5, column=0, padx='5', pady='5')

        self.no_button = Button(master, text="No", command=self.noLighnting)
        self.no_button.grid(row=5, column=1, padx='5', pady='5')

        self.close_button = Button(master, text="Close", command=self.close)
        self.close_button.grid(row=5, column=2, padx='5', pady='5')

        self.preview_image = Canvas(master, width=500, height=500)
        self.preview_image.grid(row=4, column=1, padx='5', pady='5')

    def lightning(self):
        print("You chose 'Lightning' for file " + filename[i])

    def noLighnting(self):
        print("You chose 'no Lighning' for file " + filename[i])

    def close(self):
        window = tk.Toplevel(root)
        message = "Please confirm that you want to abort training"
        window.text = Label(window, text = message).grid(row=0, column=1, padx='5', pady='5')
        window.abort_button = Button(window, text ="Abort", command=quit)
        window.abort_button.grid(row=2, column=0, padx='5', pady='5')
        window.return_button = Button(window, text ="Return", command=window.destroy)
        window.return_button.grid(row=2, column=2, padx='5', pady='5')


    def browseWindow(self):
        browseWindow = tk.Toplevel(root)
        browseWindow.heading = Label(browseWindow, text="Please specify image path")
        browseWindow.heading.grid(row=2, column=1, padx='5', pady='5')

        browseWindow.label = Label(browseWindow, text="1. Select image browseWindow")
        browseWindow.label.grid(row=2, column=1, padx='5', pady='5')

        self.textEntry = tk.StringVar()
        browseWindow.textbox_image_path = Entry(browseWindow, textvariable=self.textEntry, width=70)
        browseWindow.textbox_image_path.grid(row=3, column=1,  padx='5', pady='5')
        browseWindow.textbox_image_path.focus_set()

        browseWindow.browse_button = Button(browseWindow, text="...", command=self.browseImagePath)
        browseWindow.browse_button.grid(row=3, column=2, padx='5', pady='5')

        browseWindow.ok_button = Button(browseWindow, text="OK", command=self.acceptPath)
        browseWindow.ok_button.grid(row=5, column=0, padx='5', pady='5')

        browseWindow.cancel_button = Button(browseWindow, text="Cancel", command=browseWindow.destroy)
        browseWindow.cancel_button.grid(row=5, column=2, padx='5', pady='5')
        return browseWindow

    def destroyWindow(window):
        window.destroy()

    def browseImagePath(self):
        self.folder_path = filedialog.askdirectory(mustexist=True, title="Please specify image directory")
        self.textEntry.set(self.folder_path)

    def acceptPath(self):
        self.folder_path = self.textEntry.get()
        if(os.path.isdir(self.folder_path) == True):
            print("Selected image source is now " + self.folder_path)
            destroyWindow(browseWindow)
            dirListing = os.listdir(self.folder_path)
            for item in dirListing:
                if ".jpg" in item:
                    self.filenameList.append(item)
        else:
            print("Please enter an existing directory")

    def showDetail(self):
        return showDetail

    def showPreview



root = Tk()
my_gui = ApplicationGUI(root)
root.mainloop()
