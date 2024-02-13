# -*- coding: utf-8 -*-
"""ImagesToNumbers.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_ojadvnbO1fLIEyuu3vqfX9njFbtsxw3

Nearest Neighbor Classification on an Image Set of Numbers
 Written by Anthony Krenek

### **Data Initialization**
"""

import numpy as np
from keras.datasets import mnist
from matplotlib import pyplot
from numpy.linalg import norm

(X_train, y_train), (X_test,y_test) = mnist.load_data()

X_train = X_train[:600,:,:].astype("float32")/255 # Scale images to the [0,1] range
y_train = y_train[:600]
N_train = X_train.shape[0]
X_train = X_train.reshape((N_train,28*28))

X_test = X_test[:100,:,:].astype("float32")/255 # Scale images to the [0,1] range
y_test = y_test[:100]
N_test = X_test.shape[0]
X_test = X_test.reshape((N_test,28*28))

print("Trainset X shape: " + str(X_train.shape))
print("train label y shape: " + str(y_train.shape))
print("Testset X shape: " + str(X_test.shape))
print("test label y shape: " + str(y_test.shape))

def visualization(idx_lst,data,label):
  '''
  This function is used to visualize original dataset X or cluster representative matrix Z
  '''
  N = data.shape[0]
  for idx in idx_lst:
    pyplot.imshow(data.reshape((N,28,28))[idx], cmap=pyplot.get_cmap('gray'))
    pyplot.show()
    print("The corresponding label of this image is {}".format(label[idx]))

## Grabbing the trained data set to grab the 2 images
visualization(np.arange(2),X_train,y_train)

"""Alternative way for the above example:"""

visualization([0,1],X_train,y_train)

## Visualzing the first and third image
visualization([0,2], X_train , y_train)
###################################

# Grabbing the last 5 images
# Represented as Row Vectors
visualization([-5,-4,-3,-2,-1], X_test, y_test)

"""**4.2 (1.5/5) Distance Calculation**
These three vectors represents three images
"""

## Vectors that are representing the images
##
v1 = X_train[1]
v2 = X_train[8]
w = X_test[5]
print(v1.shape)
print(w.shape)

visualization([1,8],X_train,y_train)
visualization([5],X_test,y_test)

# Distances between w1 and w2
dist1 = np.linalg.norm(v1 - w)
dist2 = np.linalg.norm(v2 - w)

print("dist between v1 and w = {}; \ndist between v2 and w = {}".format(dist1,dist2))

# KNN Nearest Neighbor
def knn(X_train,y_train,X_test,y_test,k = 7):
  N_train = X_train.shape[0]
  N_test = X_test.shape[0]
  y_predict = -np.ones((N_test, 1), dtype=int)
  k = 7
  for i in range(N_test):
      x = X_test[i, :]
      d = np.zeros((N_train,1))
      y_predict[i] = np.bincount(y_train[np.argsort(d,axis = 0)[:k].reshape(-1)]).argmax()
      for j in range(N_train):
        d[j] = np.linalg.norm(x - X_train[j, :])
        y_predict[i] = np.bincount(y_train[np.argsort(d,axis = 0)[:k].reshape(-1)]).argmax()
  ###################################
  return y_predict

"""Validation code"""

## Prediction Accuracy
y_predict = knn(X_train,y_train,X_test,y_test,7)
y_predict = y_predict.flatten()
predict_acc = np.sum((y_predict-y_test)==0)/N_test
print("The prediction accuracy = {}%, which should be greater than 80%".format(predict_acc*100))