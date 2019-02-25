# Detect unphysical edges
# 14.11.2018 (ak)
#

# Lightnig bursts cause brigth ligth much faster than the camera
# can react. Due to the roling shutter exposure there is a linear
# increase and decreate form line to line. After a couple of line
# all other line see the full exposure.
#
# This edges paralle to the line can be used to detect lightnig with
# a rather good timing precision.
#

# The script uses an convoluton edge filter.
#
# Design parameters:
# - the used filter substracts values that are two pixel apart to detect rising or faling edge. Size of the egde filter 3x3 or 3x5, normalization (default 1)
# - optional: cooeficients of the filter
#

import sys
import os
import json
from glob import glob

from PIL import Image, ImageFilter
import matplotlib.image as mpimg

# Configuration
config = "03_img.json"

# Read from command line
id = 0

scriptdir = os.path.dirname(sys.argv[0])
if len(scriptdir) > 0:
   scriptdir = scriptdir + "/"

if len(sys.argv) > 1:
   id = int(sys.argv[1])


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
dataset = "04_img-resized-nearest" # name of the dataset
outdir = "04_img-edges" # name of the output file
filemask = "aragats-%s.jpg" # mask of the images in the dataset folder


# Config file parameters
if 'datadir' in data.keys():
   datadir = data['datadir']

#if 'dataset' in data.keys():
#   dataset = data['dataset']

if 'outdir' in data.keys():
   outdir = data['outdir']

if 'filemask' in data.keys():
   filemask = data['filemask']

filemask = filemask % "%04d"
filelist = data['filelist']


# Apply filter and create a new copy of the filtered images

# Create output folder
if not os.path.exists(datadir + "/" + outdir):
   os.makedirs(datadir + "/" + outdir)

# Define filter
km1 = (
     -2, -1,  0,
     -1,  2,  1,
      0,  1,  2
      )
km2 = (
     -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1,
      4,  4,  4,  4,  4,
     -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1
      )
km3 = (
      1,  1,  1,
      0,  0,  0,
     -1, -1, -1,
      )
km4 = (
      0,  0,  0,  0,  0,
      1,  1,  1,  1,  1,
      0,  0,  0,  0,  0,
     -1, -1, -1, -1, -1,
      0,  0,  0,  0,  0
      )
km5 = (
     -1, -1, -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1, -1, -1,
      0,  0,  0,  0,  0,  0,  0,
     1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1
      )
k = ImageFilter.Kernel(
    size=(3, 3),
    kernel=km3,
    scale=1,  # sum(km2) default
    offset=128  # default
    )


if id == 0:
   # process all images
   for img in filelist:
      # Get reference image
      id = img['id']
      imgfile = datadir + "/" + dataset + "/" + (filemask % id)
      img = Image.open(imgfile).convert("L")

      # Apply the filter and save in the new folder
      outfile = datadir + "/" + outdir + "/" + (filemask % id)
      img.filter(k).save(outfile)

else:
   imgfile = datadir + "/" + dataset + "/" + (filemask % id)
   img = Image.open(imgfile).convert("L")
   print "Open image %s\n" % imgfile
   pix = img.load()

   # Apply the filter and save in the new folder
   outfile = datadir + "/" + outdir + "/" + (filemask % id)
   edges = img.filter(k)
   edges.save(outfile)
   pixedges = edges.load()

   #x = [120,320,480,720]
   x = [15,40,60,90]
   vline = []
   print " %4s: %3d %3d %3d %3d    %3d %3d %3d %3d" % ("line", x[0], x[1], x[2], x[3], x[0], x[1], x[3], x[3])
   print " -----------------------------------------"
   for y in range(90):
      print " %4d: %3d %3d %3d %3d -- %3d %3d %3d %3d" % ( y, pix[x[0],y], pix[x[1],y], pix[x[2],y], pix[x[3],y], pixedges[x[0],y], pixedges[x[1],y], pixedges[x[2],y], pixedges[x[3],y])






