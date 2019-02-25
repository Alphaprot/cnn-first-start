# Extract text from image
# A. Kopmann, Oct 2018
#

from PIL import Image
import pytesseract 

# Read commandline

print pytesseract.image_to_string(Image.open('test-1.png'))

#print image_to_string(Image.open('test-english.jpg'), lang='eng')
