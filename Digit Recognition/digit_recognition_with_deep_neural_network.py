# -*- coding: utf-8 -*-
"""Digit Recognition with Deep Neural Network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1suGqZeAI7u3tUadEy_iDWr1p6Nflssps

## Importing Essential Libraries
"""

import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Dense
from keras.utils.np_utils import to_categorical
from keras.datasets import mnist
import random
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D

"""## Spliting Dataset"""

(x_train,y_train),(x_test,y_test) = mnist.load_data()

"""## Checking Shape of images"""

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

"""## Using Assert Function To Cross Validate Data"""

assert(x_train.shape[0]==y_train.shape[0]),"Image Lengths Are Not Same"
assert(x_test.shape[0]==y_test.shape[0]),'Image Lengths Are Not Same'
assert(x_train.shape[1:]==(28,28)),'Shapes Are Not Same'
assert(x_test.shape[1:]==(28,28)),"Shapes Are Not Same"

"""## Plotting The Images"""

numberOfSamples = []
classes = 10
cols = 5
fig,axs = plt.subplots(nrows=classes,ncols=cols,figsize=(15,10))
fig.tight_layout()
for i in range(cols):
  for j in range(classes):
    x_selected = x_train[y_train==j]
    axs[j][i].imshow(x_selected[random.randint(0,len(x_selected)),:,:],cmap="gray")
    axs[j][i].axis('off')
    if(i==2):
      axs[j][i].set_title(j)
      numberOfSamples.append(len(x_selected))

"""## Ploting Bar Plot For Number Of Samples"""

plt.bar(range(0,len(numberOfSamples)),numberOfSamples)
plt.xticks(np.arange(0,len(numberOfSamples)))
plt.title("Number Of Samples")
plt.xlabel("Numbers")
plt.ylabel("Number Of Samples")

"""## Convert Y Data Into Categorical"""

y_train = to_categorical(y_train,10)
y_test = to_categorical(y_test,10)

"""## Convert Every Image Into 0 To 1 Format For Faster Performance"""

x_train = x_train/255
x_test = x_test/255

"""## Convert Image Into 28 By 28 By 1"""

x_train = x_train.reshape(x_train.shape[0],28,28,1)
x_test = x_test.reshape(x_test.shape[0],28,28,1)

x_train[0].shape

plt.imshow(x_train[0].reshape(28,28))

def lenet():
  model = Sequential()
  model.add(Conv2D(30,(3,3),input_shape=(28,28,1),activation="relu"))
  model.add(MaxPooling2D(pool_size=(2,2)))
  model.add(Conv2D(15,(2,2),activation="relu"))
  model.add(MaxPooling2D(pool_size=(2,2)))
  model.add(Flatten())
  model.add(Dense(500,activation="relu"))
  model.add(Dropout(0.5))
  model.add(Dropout(0.2))
  model.add(Dense(10,activation="softmax"))
  model.compile(Adam(lr=0.01),'categorical_crossentropy',metrics=['accuracy'])
  return model

model = lenet()
model.summary()

h = model.fit(x=x_train,y=y_train,verbose=1,shuffle=123,validation_split=0.1,batch_size=400,epochs=10)

plt.plot(h.history['acc'])
plt.plot(h.history['val_acc'])

plt.plot(h.history['loss'])
plt.plot(h.history['val_loss'])

"""## Testing With Real Data"""

import requests
from PIL import Image
import cv2

url = "https://www.researchgate.net/profile/Jose_Sempere/publication/221258631/figure/fig1/AS:305526891139075@1449854695342/Handwritten-digit-2.png"
res = requests.get(url,stream=True)
img = Image.open(res.raw)
img = np.asarray(img)
img = cv2.resize(img,(28,28))
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img = img.reshape(1,28,28,1)

prediction = model.predict_classes(img)

prediction

