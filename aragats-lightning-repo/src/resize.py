# resize.py
# A. Kopmann, 19.11.2018
#
# Resize the cloud images; if there is low dynamic the effective pixel size is 8x8.
# Which means that blocks of 64 pixel always have the same value.
# I assume this is a result of the jpg encoding.
#

import sys
import os
import json

from PIL import Image, ImageFilter


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
   print "Error: config file format error - dict is required\n"
   exit()

if 'filelist' not in data.keys():
   print "Error: the key 'filelist' is not exisiting."
   print "\trun ocr_simple.py and define reference images before background removal\n"
   exit()


# Read parameters

# Default parameters
datadir = "../../data" # path to the data folder
dataset = "04_img-light" # name of the dataset
outdir = "04_img-resized-nearest" # name of the output file
filemask = "aragats-%s.jpg" # mask of the images in the dataset folder


# Config file parameters
if 'datadir' in data.keys():
   datadir = data['datadir']

#if 'dataset' in data.keys():
#   dataset = data['dataset']

if 'outdir' in data.keys():
   outdir = data['outdir']

if 'filemask' in data.keys():
   filemask = data['filemask'] % "%04d"

filelist = data['filelist']


# Resize the image that they are better matching the real information
# Also all algorithms should be much easier!

# Create output folder
if not os.path.exists(datadir + "/" + outdir):
   os.makedirs(datadir + "/" + outdir)


# Loop over all images
for img in filelist:
   # Get reference image
   id = img['id']
   imgfile = datadir + "/" + dataset + "/" + (filemask % id)
   img = Image.open(imgfile).convert("L")

   # Apply the filter and save in the new folder
   outfile = datadir + "/" + outdir + "/" + (filemask % id)
   #outimg = img.resize((160,90), Image.ANTIALIAS)
   outimg = img.resize((160,90), Image.NEAREST)
   outimg.save(outfile)
