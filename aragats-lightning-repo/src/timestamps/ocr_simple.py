# Extract simple text from images
# A. Kopmann, 10.10.2018
#


# Implemented for extraction of timestamps in the Aragats lightning images
#
# Name of the function image_to_text (like in tesseract)
# In the end I hope to get tesseract trainged that it works reliable.
#
# The timestamp information is saved in the metadata of the project
# Sequences are defined by a minimum time between blocks of images
#
# Strukture (JSON):
# 'dataset': "03_img-unique",
# 'images': [
#      {'id': 1, 'ts': 12345678, 'frame': 12, 'skip': 1},
#      {'id': 2, 'ts': 12345678, 'frame': 12, 'skip': 1},
#      ...
#      ]
# 'sequences': [
#      {'id': 1, 'images': [1,2,3,4,5,6,7], 'ref':1, 'skip': 10000 },
#      {'id': 2, 'images': [8,9,10,11], 'ref':8, 'skip': 23000 },
#      ...
#      ]
#

# 19.11.2018
# Changing all the print statements to print functions to make the code Python3 compatible.
# Adding this import statement keeps the Python2 compatibility
from __future__ import print_function

import sys
import os
import time
from datetime import datetime
import json
from glob import glob

from PIL import Image


# Global variables
ch = []
char = []

# Load characters (global variables, in order to load them only onces)
# The simple characters are given only as binary images
# thus the images can be reduced to this representation, RGB is not needed
def load_char():
   ch.append(Image.open(scriptdir + "chars/char-0.png").convert("L"))
   ch.append(Image.open(scriptdir + "chars/char-1.png").convert("L"))
   ch.append(Image.open(scriptdir + "chars/char-2.png").convert("L"))
   ch.append(Image.open(scriptdir + "chars/char-3.png").convert("L"))
   ch.append(Image.open(scriptdir + "chars/char-4.png").convert("L"))
   ch.append(Image.open(scriptdir + "chars/char-5.png").convert("L"))
   ch.append(Image.open(scriptdir + "chars/char-6.png").convert("L"))
   ch.append(Image.open(scriptdir + "chars/char-7.png").convert("L"))
   ch.append(Image.open(scriptdir + "chars/char-8.png").convert("L"))
   ch.append(Image.open(scriptdir + "chars/char-9.png").convert("L"))
   ch.append(Image.open(scriptdir + "chars/char-minus.png").convert("L"))
   ch.append(Image.open(scriptdir + "chars/char-colon.png").convert("L"))
   ch.append(Image.open(scriptdir + "chars/char-space.png").convert("L"))

   char.append("0")
   char.append("1")
   char.append("2")
   char.append("3")
   char.append("4")
   char.append("5")
   char.append("6")
   char.append("7")
   char.append("8")
   char.append("9")
   char.append("-")
   char.append(":")
   char.append(" ")


# Calculate how good a region of the image to test
# matches the reference image (e.g. sample character)
# Both arguments need to be of PIL image type
def get_match(im,ref):
   pix = im.load()
   pixref = ref.load()
   
   diff = 0
   for x in range(12):
      for y in range(14):
         diff += abs(pix[x,y]-pixref[x,y])

   return(diff)

# Alternative implementation of the matching
# Only the white pixel in the references are considered
# Count errors and substract good matches
# In a good match the result will be the number of white pixel
# In a bad match it should be negative?!
def get_match2(im,ref):
   pix = im.load()
   pixref = ref.load()

   err = 0
   for x in range(12):
      for y in range(14):
         #print pixref[x,y], pix[x,y]
         if ((pixref[x,y] == 255) and (pix[x,y] > 200)):
            err = err -1
         if ((pixref[x,y] == 255) and (pix[x,y] < 200)):
            err = err +1

   return(err)

# Identify the best character and give a measure for the
# certainty of the decision
def get_char(im):
   i = 0
   min = 1000000;
   index = 0
   for ref in ch:
      test = get_match2(im,ref)
      #print test
      
      if (test < min):
         min = test
         index = i
      i = i + 1
   
   #print index, min, char[index]
   return(char[index])


# Extract textblocks
def image_to_string(im):
   # The region is defined by a 4-tuple, where coordinates are (left, upper, right, lower)
   # Image size: 1280 x 720
   box = (1280-142, 720-38, 1280, 720)
   timestamp = im.crop(box)
   #timestamp.show()

   text = ""
   for row in range(2):
      for col in range(11):

         box = (12*col, 18*row, 12*col+12, 18*row+14)
         region = timestamp.crop(box)
         #region.show()
         # Compare region with all the available characters
         text +=get_char(region)
      text += "\n"

   return (text)


#
# Main
#

# Read from command line
config = "sample.json"

scriptdir = os.path.dirname(sys.argv[0])
if len(scriptdir) > 0:
   scriptdir = scriptdir + "/"

if len(sys.argv) > 1:
   config = sys.argv[1]


# Check if the timestamp data is already available
with open(config, "r") as fconf:
      data = json.load(fconf)

if type(data) is not dict:
   print("Warning: config file format error - dict is required\n")
   exit()

if 'filelist' in data.keys():
   print("Warning: the key 'filelist' is already exisiting.")
   print("\tRemove, or rename the configuration file and retry\n")
   
   #filelist = data['filelist']
   #print type(filelist), len(filelist)
   exit()


# Read parameters

# Default parameters
datadir = "../../data" # path to the data folder
dataset = "03_img-unique" # name of the dataset
filemask = "aragats-%s.jpg" # mask of the images in the dataset folder

framerate = 30 # number of frames per second
seqsplit = 100 # number of frames to split sequences


# Config file parameters
if 'datadir' in data.keys():
   datadir = data['datadir']

if 'dataset' in data.keys():
   dataset = data['dataset']

if 'filemask' in data.keys():
   filemask = data['filemask']

if 'framerate' in data.keys():
   framerate = data['framerate']

if 'seqsplit' in data.keys():
   seqsplit = data['seqsplit']


# Extract timestamp in the images

# Read all files of a certain format in the dataset folder
# Todo: The file format should also be moved the the parameter section
mask = datadir + "/" + dataset + "/" + (filemask) % "*"
files = glob(mask)

# For testing with a single, or few images
#files = glob(datadir + "/" + dataset + "/" + "aragats-000*.jpg")
#files = [ datadir + "/" + dataset + "/" + "aragats-0001.jpg" ]

# Glob output can be in strange order - needs to be sorted by name
# Alphabetic and time order need to match !!!
files.sort()


# Extract timestamp and frame number
load_char()

id = 0
seq = 0
last_sec = 0
last_frame = 0
skip_list = []
filelist = []
seqlist = []
idlist = []
refId = 0
seqskip = 0
for f in files:
   id = id + 1

   im = Image.open(f).convert("L")
   tstring = image_to_string(im)
   #print tstring

   # Read the timestamp
   t = time.strptime(tstring[1:20], '%Y-%m-%d %H:%M:%S')
   sec = time.mktime(t)
   #print time.mktime(t)
   
   # Read frame number
   frame = int(tstring[21:23])
   
   skip = (sec - last_sec) * framerate + frame - last_frame
   skipinseq = skip
   skip_list.append(skip)
   if (skip > seqsplit):
      # Start of new sequence; store the old one
      if (seq > 0):
         seqlist.append({'id': seq, 'ref': refId, 'images': idlist, 'skip': seqskip})
         seqskip = skip
      
      # Create new sequence
      seq = seq +1
      skipinseq = 0
      idlist = [id]
      refId = id
      
   else:
      idlist.append(id)


   filelist.append({
         'id':id, 'ts': sec, 'frame': frame,
         'seq':seq, 'skip':skipinseq
      })

   last_sec = sec
   last_frame = frame

   #print sec, frame, skip, seq

# Add the last sequence
if len(idlist) > 0:
   seqlist.append({'id': seq, 'ref': refId, 'images': idlist, 'skip': seqskip})


# Save basic information on the images in the dataset
data.update({'filelist':filelist})
data.update({'seqlist':seqlist})

with open(config, "w") as fconf:
      json.dump(data, fconf, indent=4)


# Print summary
print("Proccessed images in dataset: ", id)
print("Total number of sequences   : ", seq)


# Next step:
#
# Validate the definition of reference images (key 'ref')
# A reference image in a image with no lightning that can be used
# for background substraction. If the first image contains lightning
# also the last images of the sequence can be used.

# The reference image need to be validated manually
# This script will not overwrite a exisiting configuration.




