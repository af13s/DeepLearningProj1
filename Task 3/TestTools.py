import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)
    
    plt.rcParams.update(plt.rcParamsDefault)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    # plt.show()

def load_data(img_rows, img_cols):

	trainData = []
	trainLabels = []
	testData = []
	testLabels = []

	classes = [0,1,2,3,4,5,6,7,8,9]
	label_encoder = pd.factorize(classes)
	labels_1hot = OneHotEncoder().fit_transform(label_encoder[0].reshape(-1,1))
	onehot_array = labels_1hot.toarray()

	d1 = dict(zip(classes,onehot_array.tolist()))

	for i,file in enumerate(['zip_train.txt', 'zip_test.txt']):
		f = open(file)

		tempLabels = []
		tempData = []

		for line in f:
			line = line.split()
			thelabel = line.pop(0)
			thelabel = int(float((thelabel)))

			line = [float(i) for i in line]
			theX = np.interp(line, (-1,1), (0, 1))

			tempLabels.append(thelabel)
			tempData.append(theX)

		for label in tempLabels:
		    encoding = d1[label]
		    if i == 0:
		    	trainLabels.append(encoding)
		    else:
		    	testLabels.append(encoding)

		if i == 0:
			trainLabels = np.array(trainLabels).reshape((-1,len(classes)))
			trainData = np.array(tempData)
		else:
			testLabels = np.array(testLabels).reshape((-1,len(classes)))
			testData = np.array(tempData)

		f.close()

	return trainData, trainLabels, testData, testLabels

def show_misclassified(test_set, model):

	tempLabels = []

	for i,file in enumerate(['zip_test.txt']):
		f = open(file)

		tempData = []

		for line in f:
			line = line.split()
			thelabel = line.pop(0)
			thelabel = int(float((thelabel)))

			line = [float(i) for i in line]
			theX = np.interp(line, (-1,1), (0, 1))

			tempLabels.append(thelabel)
			tempData.append(theX)

	misclassified = {}

	
	predictions = model.predict_classes(test_set)
	print (predictions)

	print(len(predictions))
	print(len(tempLabels))

	for i in range(len(predictions)):
		if predictions[i] != tempLabels[i]:
			print(predictions[i] , " was classified as " , tempLabels[i] )
			if tempLabels[i] not in misclassified:
				misclassified[tempLabels[i]] = 0 
			misclassified[tempLabels[i]] += 1

	print (misclassified)

def plot_results(history, epochs, name):
	plt.style.use("ggplot")
	plt.figure()
	plt.plot(np.arange(0, epochs), history.history["loss"], label="train_loss")
	plt.plot(np.arange(0, epochs), history.history["val_loss"], label="val_loss")
	plt.plot(np.arange(0, epochs), history.history["acc"], label="train_acc")
	plt.plot(np.arange(0, epochs), history.history["val_acc"], label="val_acc")
	plt.title("Training Loss and Accuracy")
	plt.xlabel("Epoch #")
	plt.ylabel("Loss/Accuracy")
	plt.legend(loc="upper left")
	plt.savefig(name)