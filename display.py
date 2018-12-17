# Display MNist dataset
#

from PIL import Image
import PIL.ImageOps

from keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()


print type(x_train), type(y_train)

print y_train


for digit in x_train[:3]:
   #print digit
   img = Image.fromarray(digit, 'L')
   
   img_inv = PIL.ImageOps.invert(img)
   img_inv.show()



