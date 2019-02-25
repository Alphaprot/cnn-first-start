# Background removal
# 12.11.2018 (ak)
#

# Use the reference image defined for each sequence
# to remove the background. The resulting lightning
# only images are stored in a black and white version
# in img-light and img-light-inverse. The second
# should be easierer to inspect.
#

# Versions:
# 19.11.2018
# Changing all the print statements to print functions to make the code Python3 compatible.


# Adding this import statement keeps the Python2 compatibility
from __future__ import print_function

import sys
import os
import json
from glob import glob

from PIL import Image, ImageChops, ImageOps

# Read from command line
config = "03_img.json"

scriptdir = os.path.dirname(sys.argv[0])
if len(scriptdir) > 0:
   scriptdir = scriptdir + "/"

if len(sys.argv) > 1:
   config = sys.argv[1]


# Check if the timestamp data is already available
with open(config, "r") as fconf:
      data = json.load(fconf)

if type(data) is not dict:
   print("Error: config file format error - dict is required\n")
   exit()

if 'filelist' not in data.keys():
   print("Error: the key 'filelist' is not exisiting.")
   print("\trun ocr_simple.py and define reference images before background removal\n")
   exit()


# Read parameters

# Default parameters
datadir = "../../data" # path to the data folder
dataset = "03_img-unique" # name of the dataset
light = "04_img-light" # name of the output file
filemask = "aragats-%s.jpg" # mask of the images in the dataset folder

framerate = 30 # number of frames per second
seqsplit = 100 # number of frames to split sequences


# Config file parameters
if 'datadir' in data.keys():
   datadir = data['datadir']

if 'dataset' in data.keys():
   dataset = data['dataset']

if 'light' in data.keys():
   light = data['light']

#if 'filemask' in data.keys():
#   filemask = data['filemask']

if 'framerate' in data.keys():
   framerate = data['framerate']

if 'seqsplit' in data.keys():
   seqsplit = data['seqsplit']


filemask = filemask % "%04d"
filelist = data['filelist']
seqlist = data['seqlist']



# Remove background
# The assumption is that all images are always brighter than the
# reference image. In the general case, the images must also consider
# negative values

# Create output folders
if not os.path.exists(datadir + "/" + light):
   os.makedirs(datadir + "/" + light)
if not os.path.exists(datadir + "/" + light + "-inverse"):
   os.makedirs(datadir + "/" + light + "-inverse")



# Loop over all sequences
for seq in seqlist:
   # Get reference image
   ref = seq['ref']
   reffile = datadir + "/" + dataset + "/" + (filemask % ref)
   imgref = Image.open(reffile)

   # Calculate the difference
   for img in seq['images']:
      infile = datadir + "/" + dataset + "/" + (filemask % img)
      outfile = datadir + "/" + light + "/" + (filemask % img)
      outfile2 = datadir + "/" + light + "-inverse/" + (filemask % img)
    
      imgin = Image.open(infile)
      imgout = ImageChops.subtract(imgin, imgref)
      imgout.save(outfile)
      
      imginv = ImageOps.invert(imgout)
      imginv.save(outfile2)




