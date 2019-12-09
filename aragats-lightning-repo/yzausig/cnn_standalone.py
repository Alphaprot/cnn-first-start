#! /usr/bin/env python

from __future__ import print_function
import keras
import os
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from time import time #added for line 57 format(time())
from keras.callbacks import TensorBoard #added
from PIL import Image

train_test_ratio = 0.7 # e.g. 7 of 10 pictures will be used for training
batch_size = 40
num_classes = 2
epochs = 10

img_rows = 160
img_cols = 144
filepath = os.path.dirname(os.path.realpath(__file__))
noExample = len([name for name in os.listdir('.') if os.path.isfile(name)]) # count of all available examples (160)

x = np.zeros([1, img_rows, img_cols])
label = np.zeros([1, img_rows, img_cols])

for counter, img in enumerate(os.listdir(filepath+"/3_split")): # create label array
        label_img = Image.open(img)
        filename = label_img.filename
        reqFilename = "4" + filename[1:]
        tempArray = np.asarray(label_img)
        tempArray = np.swapaxes(tempArray, 0, 1)
        tempArray = tempArray[np.newaxis, :, :]
        np.concatenate(label, tempArray)

        if os.path.isfile("4_split/" + reqFilename): # create x array
                tempArray = np.asarray(reqFilename)
                tempArray = np.swapaxes(tempArray, 0, 1)
                tempArray = tempArray[np.newaxis, :, :]
                np.concatenate(x, tempArray)
        else:
                print("No associated x_data found for label file %s!\n" %filename)

x_train, x_test = x[:(noExample*train_test_ratio), :, :], x[(noExample*train_test_ratio):, :, :]
label_train, label_test = x[:(noExample*train_test_ratio), :, :], x[(noExample*train_test_ratio):, :, :]

input_shape = x_train.shape()

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

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
        optimizer=keras.optimizers.Adadelta(),
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
