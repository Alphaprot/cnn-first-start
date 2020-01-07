#! /usr/bin/env python

from __future__ import print_function
import keras
import os
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from time import time #added for line 57 format(time())
from keras.callbacks import TensorBoard #added
from PIL import Image

train_test_ratio = 0.7 # e.g. 7 of 10 pictures will be used for training
numberOfChannels = 3 # How many channels has the input image (1 channel -> greyscale)?
treshold = 180
batch_size = 40
num_classes = 2
epochs = 10
keras.backend.set_image_data_format('channels_first')

img_rows = 160
img_cols = 144
scriptPath = os.path.dirname(os.path.realpath(__file__))
#noExample = len([name for name in os.listdir('.') if os.path.isfile(name)]) # count of all available examples (160)

x = np.zeros([1, numberOfChannels, img_rows, img_cols], dtype=np.uint8) # dtype=int !
#label = np.zeros([1, img_rows, img_cols], dtype=np.int8) # dtype=int !
label = np.zeros([1], dtype=np.int8)

for counter, img in enumerate(os.listdir(scriptPath + "/3_split")): # create label array
        label_img = Image.open(scriptPath + "/3_split/" + img)
        filename = label_img.filename
        label_img = label_img.point(lambda p: p > treshold and 255) 
        label_img = label_img.convert("1") # converts image to binary black and white
        img_array = np.asarray(label_img, dtype=np.int8)
        if 0 in img_array[:, :]:
                label = np.append(label, [1])
        else:
                label = np.append(label, [0])
        
        '''
        tempArray = np.asarray(label_img, dtype=np.int8)
        tempArray = np.swapaxes(tempArray, 0, 1)
        tempArray = tempArray[np.newaxis, :, :]
        print(tempArray.shape, tempArray.dtype)
        
        print(label.shape, label.dtype)

        label = np.concatenate((label, tempArray))
        '''
        head, tail = os.path.split(filename)
        tail =  "4" + tail[2:]
        #tail =  "4" + tail[1:]

        reqPath = scriptPath + "/4_split/" + tail
        print(reqPath)
        if os.path.isfile(reqPath): # create x array
                standard_img = Image.open(reqPath)
                tempArray = np.asarray(standard_img, dtype=np.uint8)
                tempArray = np.swapaxes(tempArray, 0, 2)
                tempArray = tempArray[np.newaxis, :, :, :]
                x = np.concatenate((x, tempArray))
        else:
                print("No associated x_data found for label file %s!\n" %filename)



print("Shape before slicing: " + str(label.shape) + str(x.shape))
noExample = len(x)
x_train, x_test = x[1:int(noExample*train_test_ratio), :, :], x[int(noExample*train_test_ratio):, :, :]
#label_train, label_test = label[1:int(noExample*train_test_ratio), :, :], label[int(noExample*train_test_ratio):, :, :]
label_train, label_test = label[1:int(noExample*train_test_ratio)], label[int(noExample*train_test_ratio):]

print("Shapes are: %s, %s, %s, %s "  %(x_train.shape, x_test.shape, label_train.shape, label_test.shape))
input_shape = (3, img_rows, img_cols)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')


print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_train.ndim)
print(x_test.shape[0], 'test samples')
print(label_test)


label_train = keras.utils.to_categorical(label_train, num_classes)
label_test = keras.utils.to_categorical(label_test, num_classes)


model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
          activation='relu',
          input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
        optimizer=keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.99, amsgrad=False),
       # optimizer=keras.optimizers.Adadelta(),
        metrics=['accuracy'])

tensorboard = keras.callbacks.TensorBoard(log_dir="logs/{}".format(time()),
        histogram_freq=1, write_graph=True, write_images=True)

model.fit(x_train, label_train,
        batch_size=batch_size,
        epochs=epochs,
        verbose=1,
        callbacks=[tensorboard],
        validation_data=(x_test, label_test))
score = model.evaluate(x_test, label_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
print("\n")
print("Do you want to save this network in the current working directory? [y/N]")
user_input = input().lower()

while True:
        if user_input is "y":
                model.save("model.h5")
                print("Saved model and weights in the current working directory.")
                break
        elif user_input is "n" or None:
                break

print("Do you want to re-load the network in order to test it? [y/N]")
user_input = input().lower()

while True:
        if user_input is "y":
                model = load_model('model.h5')
                print("Loaded model and weights")
                model.summary()
        
                # Testing the loaded model
                model.compile(loss=keras.losses.categorical_crossentropy,
                optimizer=keras.optimizers.Adadelta(),
                metrics=['accuracy'])
                score = model.evaluate(test_data)
                break
        elif user_input is "n" or None:
                break