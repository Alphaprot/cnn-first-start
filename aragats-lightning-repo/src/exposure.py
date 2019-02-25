# exposure.py
# A. Kopmann, 12.10.18
#

# 16.11.2018
# This enables the usage of the print function "print()" in python 2. Using the print function instead of the
# keyword will make the script executable in python 2 and python 3
from __future__ import print_function

import sys
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.image as mpimg

import os
import json

# 16.11.2018
# Using the relative path to the config file, opening the config and using the parameters from there
folder_path = os.path.dirname(os.path.abspath(__file__))
config_path = "{}/timestamps/config.json".format(folder_path)

with open(config_path, mode='r') as file:
   config_string = file.read()

config = json.loads(config_string)

# Parameters
# Todo: read this parameters from config file !!!
datadir = config['datadir']
filemask = config['filemask'] % "%04d"
dataset = "03_img-unique"
fileimagemask = "imagemask.png"

if len(sys.argv) > 1:
   dataset = sys.argv[1]


fullmask = datadir + "/" + dataset + "/" + filemask


imagemask = Image.open(datadir + "/" + fileimagemask)
mask = imagemask.load()

# Load image add plot sum of grey values in all lines
#
def plot_line(id):
   filename = fullmask % id

   # 16.11.2018
   # Using the print function for python 3 compatibility
   print(filename)
   im = Image.open(filename).convert("L")
   pix = im.load()

   line = []
   for y in range(720):
      sum = 0
      n = 0
      for x in range(1280):
         if mask[x,y]:
            sum += pix[x,y]
            n = n + 1
      line.append(sum/n)

   #print line
   return(line)

# Plot changes in profile
def find_edges(line):

   edges = []
   for y in range(720):
      diff = 0
      if (y > 4) and (y<714):
         diff = abs(line[y+5]-line[y-5])
      edges.append(diff)

   return(edges)


# Callback
#
class Index(object):
   ind = 1
   
   def next(self, event):
      if self.ind < 345:
         self.ind += 1
   
      line = plot_line(self.ind)
      edges = find_edges(line)
      l.set_xdata(line)
      e.set_xdata(edges)
      plt.draw()

   def prev(self, event):
      if self.ind > 1:
         self.ind -= 1

      line = plot_line(self.ind)
      edges = find_edges(line)
      l.set_xdata(line)
      e.set_xdata(edges)
      plt.draw()

# This instructions can be used to calculate results for all
# images at once
filename = fullmask % 1
img = mpimg.imread(filename)

t = range(720,0,-1)
line = plot_line(1)
edges = find_edges(line)
#plt.imshow(img)
l, = plt.plot(line,t)
e, = plt.plot(edges,t)
plt.axis([0, 255, 0, 720])


callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

plt.show()
