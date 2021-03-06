
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
set_session(sess)  # set this TensorFlow session as the default session for Keras

import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Nadam, Adam
from sklearn.preprocessing import OneHotEncoder
from keras.layers.normalization import BatchNormalization
import pandas as pd
from TestTools import plot_results, show_misclassified, load_data


batch_size = 128
num_classes = 10
epochs = 15
img_rows, img_cols = 16, 16

trainData, trainLabels, testData, testLabels = load_data(img_rows, img_cols)

loss_results = []
accuracy_results = []

for i in range(0,10):
	# # Parameter Intialization
	model = Sequential()
	
	#fast
	# model.add(Dense(128, activation='relu', input_shape=(256,),kernel_initializer=keras.initializers.Constant(value=5),bias_initializer=keras.initializers.Constant(value=0.001),)) # 
	# model.add(Dense(128, activation='sigmoid',kernel_initializer=keras.initializers.Constant(value=0.001),bias_initializer=keras.initializers.Constant(value=0.001))) # kernel_initializer=keras.initializers.Constant(value=0.001),bias_initializer=keras.initializers.Constant(value=0.001),
	# model.add(Dense(128, activation='tanh',kernel_initializer=keras.initializers.Constant(value=0.001),bias_initializer=keras.initializers.Constant(value=0.001))) # kernel_initializer=keras.initializers.Constant(value=0.001),bias_initializer=keras.initializers.Constant(value=0.001),

	#slow parameter
	# model.add(Dense(128, activation='relu', input_shape=(256,),kernel_initializer=keras.initializers.Constant(value=1.2))) # 
	# model.add(Dense(128, activation='sigmoid')) # kernel_initializer=keras.initializers.Constant(value=0.001),bias_initializer=keras.initializers.Constant(value=0.001),
	# model.add(Dense(128, activation='tanh')) # kernel_initializer=keras.initializers.Constant(value=0.001),bias_initializer=keras.initializers.Constant(value=0.001),


	model.add(Dense(128, activation='relu', input_shape=(256,)))
	#model.add(BatchNormalization())
	model.add(Dense(128, activation='sigmoid'))
	#model.add(BatchNormalization())
	model.add(Dense(128, activation='tanh'))
	#model.add(BatchNormalization())
	model.add(Dense(num_classes, activation='softmax'))

	model.summary()

	# # Learning Rate
	#1) learning is very slow; 2) learning is effective; and 3) learning is too fast.

	# model.compile(loss='categorical_crossentropy',
	#               optimizer=Adam(lr=0.05),
	#               metrics=['accuracy'])


	# learning is very slow
	# model.compile(loss='categorical_crossentropy',
	#              optimizer=Adam(lr=0.00005),
	#              metrics=['accuracy'])

	# learning is too fast
	model.compile(loss='categorical_crossentropy',
	              optimizer=Adam(lr=0.05),
	              metrics=['accuracy'])

	# # learning is effective
	# model.compile(loss='categorical_crossentropy',
	#              optimizer=Adam(lr=0.001),
	#              metrics=['accuracy'])

	# Momentum
	# model.compile(loss='categorical_crossentropy',
	#           optimizer=Nadam(lr=0.002, beta_1=0.9, beta_2=0.999),
	#           metrics=['accuracy'])

	#print(model.get_weights())

	history = model.fit(trainData, trainLabels,
	                batch_size=batch_size,
	                epochs=epochs,
	                verbose=2,
	                validation_data=(testData,testLabels))

	score = model.evaluate(testData, testLabels, verbose=0)
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

#plot_results(history,epochs,'FNN_2.png')
