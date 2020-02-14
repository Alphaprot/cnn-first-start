# Place the script into the directory aragats-raw 
# Note that only images whose filename-string starts with a '2' will be taken into account
# The script will create two folders (/3_split contains the labels whereas /4_split contains the corresponding images)
#  
import os
import sys, getopt
from PIL import Image

createMode = ''
filepath = os.path.dirname(os.path.realpath(__file__))
sliceX = 8
sliceY = 5

def main(argv):
    global createMode
    try:
        opts, args = getopt.getopt(argv, "hm:", ["help","mode="])
    except getopt.GetoptError as err:
        print(err)
        print(sys.argv[0] + ' -m <greyscale> or <RGB>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(sys.argv[0] + ' -m <greyscale> or <RGB>')
            sys.exit()
        elif opt in ("-m", "--mode"):
            if arg.lower() is 'rgb':
                createMode = 'RGB'
            elif arg.lower() is 'greyscale':
                createMode = 'greyscale'
            else:
                raise ValueError("Unknown option %s for -m (mode)" %arg)
                print(sys.argv[0] + ' -m <greyscale> or <RGB>') 
               

if __name__ == "__main__":
    main(sys.argv[1:])
    print('Mode is %s' % createMode)
    print(filepath)

    for img in os.listdir(filepath + "/bg_subtraction/"):
        if img.startswith("2") and img.endswith(".jpg"):
            labelImg = Image.open(filepath + "/bg_subtraction/" + img)
            oldName = labelImg.filename
            newName = oldName[1:14]
            w, h = labelImg.size
            wStep = w/sliceX
            hStep = h/sliceY
            for i in range(0, sliceX):
                for j in range(0, sliceY):
                    crop = labelImg.crop(((i*wStep), (j*hStep), ((i+1)*wStep), ((j+1)*hStep)))
                    if not os.path.exists(filepath + "/3_split/"):
                        os.makedirs(filepath + "/3_split/")
                    crop.save("%s/3_split/3%s-%02d%02d.jpg" % (filepath, newName, i, j))
            
            if createMode is 'greyscale':
                referenceImageLoc = filepath +"/1%s.jpg" % newName
            elif createMode is 'RGB':
                newName = newName[1:14]
                referenceImageLoc =  +"/%s.jpg" % newName   

            try:
                referenceImg = Image.open()
            except IOError:
                print("No corresponding image named %s for %s could be found!\n" % (referenceImg.filename, labelImg.filename))          

            if (w, h == referenceImg.size):
                for i in range(0, sliceX):
                    for j in range(0, sliceY):
                        crop = referenceImg.crop(((i*wStep), (j*hStep), ((i+1)*wStep), ((j+1)*hStep)))
                        if not os.path.exists(filepath + "/4_split/"):
                            os.makedirs(filepath + "/4_split/")
                        crop.save("%s/4_split/4%s-%02d%02d.jpg" % (filepath, newName, i, j))
            else:
                print("Size mismatch!")
