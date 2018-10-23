## https://github.com/keras-team/keras/blob/master/examples/mnist_cnn.py

'''Trains a simple convnet on the MNIST dataset.
Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, LocallyConnected2D
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from keras.optimizers import Adam
from TestTools import plot_results, load_data
batch_size = 32
num_classes = 10
epochs = 5

# input image dimensions
img_rows, img_cols = 16, 16


x_train, y_train, x_test, y_test = load_data(img_rows, img_cols)

x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)

loss_results = []
accuracy_results = []

for i in range(0,1):

	model = Sequential()
	model.add(LocallyConnected2D(32, (3,3),
	                 activation='relu',
	                 input_shape=input_shape))
	model.add(LocallyConnected2D(64, (3,3), activation='sigmoid'))
	model.add(Flatten())
	model.add(Dense(128, activation='tanh'))
	model.add(Dense(num_classes, activation='softmax'))
	model.compile(loss='categorical_crossentropy',
	              optimizer=Adam(),
	              metrics=['accuracy'])

	history = model.fit(x_train, y_train,
	          batch_size=batch_size,
	          epochs=epochs,
	          verbose=1,
	          validation_data=(x_test, y_test))
	score = model.evaluate(x_test, y_test, verbose=0)
	print("Test Run: " , i)
	print()
	print('Test loss:', score[0])
	print('Test accuracy:', score[1])
	print()
	loss_results.append(score[0])
	accuracy_results.append(score[1])


	model = None

loss_results = pd.Series(loss_results)
accuracy_results = pd.Series(accuracy_results)

print("Loss Statistics")
print(loss_results.describe())
print()
print("Accuracy Statistics")
print(accuracy_results.describe())

	# plot_results(history,epochs)