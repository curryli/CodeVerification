# coding=utf-8
import cv2
import os
import numpy as np

#导入各种用到的模块组件
#from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.advanced_activations import PReLU
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.utils import np_utils, generic_utils
import numpy as np
from PIL import Image
from keras import backend as k


if __name__ == '__main__':    
    img = cv2.imread("testPic.png",0)
    arr = np.asarray(img,dtype="float32")
    testdata = np.empty((1,1,28,28),dtype="float32")
    testdata[0,:,:,:] = arr
    testdata /= np.max(testdata)
    testdata -= np.mean(testdata)   
    
    
    from keras.models import model_from_json
    model = model_from_json(open('my_model_architecture.json').read())  
    
    ##############  
    #使用SGD + momentum  
    #model.compile里的参数loss就是损失函数(目标函数)  加载原model前仍需compile 否则报错：  The model needs to be compiled before being used.
    sgd = SGD(lr=0.05, decay=1e-6, momentum=0.9, nesterov=True)  
    model.compile(loss='categorical_crossentropy', optimizer=sgd,class_mode="categorical",metrics=['accuracy']) 
    
    
    #加载参数
    WEIGHTS_FNAME = 'All_Cnn_Weights.hdf'
    model.load_weights(WEIGHTS_FNAME)    
      
    #print(model.predict(testdata))
    print(model.predict_classes(testdata))
    print "Done"
    
    
    
    
#如果新模型和旧模型结构一样，直接调用model.load_weights读取参数就行。如果新模型中的几层和之前模型一样，也通过model.load_weights('my_model_weights.h5', by_name=True)来读取参数， 或者手动对每一层进行参数的赋值，比如x= Dense(100, weights=oldModel.layers[1].get_weights())(x)