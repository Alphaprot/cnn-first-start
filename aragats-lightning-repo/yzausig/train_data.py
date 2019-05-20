from __future__ import print_function
import os
import time
import numpy as np
import glob
import json
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
        np.empty([len(self.filenameList), 2, self.matrixSize]) #numpy-Array for training data --> 1st tuple: filename 2nd tuple: human classification result (y/n) 3rd tuple: pixel or part of grid (in different colors)
        self.quick_result_state = 0 # 0 --> undefined, 1 --> user detected lightning, 2 --> user detected no lightning

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

        for i in range(len(self.filenameList)):
            self.preview_image.create_image(250, 250, anchor=CENTER, image=ImageTk.PhotoImage(Image.open(self.folder_path + self.filenameList[i])))
            wait_variable(self.quick_result_state)
            if (self.quick_result_state == 1):
                print("You chose 'Lightning' for file " + filename[i])
                continue

            elif (self.quick_result_state == 2):

                print("You chose 'no Lighning' for file " + filename[i])
                self.quick_result= 0
                continue

    def lightning(self):
        self.quick_result_state = 1

    def noLighnting(self):
        self.quick_result_state = 2

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

    def browseImagePath(self):
        self.folder_path = filedialog.askdirectory(mustexist=True, title="Please specify image directory")
        self.textEntry.set(self.folder_path)

    def acceptPath(self):
        self.folder_path = self.textEntry.get()
        if(os.path.isdir(self.folder_path) == True):
            print("Selected image source is now " + self.folder_path)
            browseWindow.destroy() #FENSTER browseWindow muss geschlossen werden. Funktioniert nicht

            dirListing = os.listdir(self.folder_path)
            for item in dirListing:
                if ".jpg" in item:
                    self.filenameList.append(item)
        else:
            print("Please enter an existing directory")

    def showDetail(self):
        detailWindow = tk.Toplevel(root)
        detailWindow.heading = Label(detailWindow, text="Choose image parts covered with lightning")
        self.preview_image = Canvas(master, width=1280, height=720)
        self.preview_image.create_image(640, 360, anchor=CENTER, image=ImageTk.PhotoImage(Image.open(self.folder_path + self.filenameList[i])))
        detailWindow.chooseKind = Radiobutton()



root = Tk()
my_gui = ApplicationGUI(root)
root.mainloop()
