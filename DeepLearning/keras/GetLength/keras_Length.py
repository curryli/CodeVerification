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
import time


#统计样本的数目
def __getnum__(path):
    fm=os.listdir(path)
    i=0
    for subf in fm:
        print path + subf
        sfm=os.listdir(path + subf)
        for f in sfm:
            i+=1
    return i        

#生成X,Y列
def __data_label__(path,count): 
    MapDict={"4":0,"5":1,"6":2}
    
    
    data = np.empty((count,1,50,200),dtype="float32")
    label = np.empty((count,),dtype="uint8")
    i=0;
    filelist= os.listdir(path)
    #print filelist
    for ff in filelist:
        #print ff
        fn = path+"/"+ff+"/"
        #print fn
        fn2= os.listdir(fn)
        for filename in fn2:
            #print filename
            #print fn+"/"+filename
            img = cv2.imread(fn+"/"+filename,0)
            arr = np.asarray(img,dtype="float32")
            data[i,:,:,:] = arr
            #fy = ff
            label[i]= MapDict[ff]
            i+=1
    print "i is: "+ str(i)   
    data /= np.max(data)
    data -= np.mean(data)    
    return data,label

###############
#开始建立CNN模型
###############

#生成一个model
def __CNN__(testdata,testlabel,traindata,trainlabel):
    ###############  
#开始建立CNN模型  
###############  
  
#生成一个model  
    model = Sequential()  
      
    #第一个卷积层，4个卷积核，每个卷积核大小5*5。1表示输入的图片的通道,灰度图为1通道。  
    #border_mode可以是valid或者full，具体看这里说明：http://deeplearning.net/software/theano/library/tensor/nnet/conv.html#theano.tensor.nnet.conv.conv2d  
    #激活函数用tanh  
    #你还可以在model.add(Activation('tanh'))后加上dropout的技巧: model.add(Dropout(0.5))  
    model.add(Convolution2D(4, 7, 7, border_mode='valid', input_shape=(1,50,200)))  
    model.add(Activation('tanh'))  
      
      
    #第二个卷积层，8个卷积核，每个卷积核大小3*3。4表示输入的特征图个数，等于上一层的卷积核个数  
    #激活函数用tanh  
    #采用maxpooling，poolsize为(2,2)  
    model.add(Convolution2D(8, 5, 5, border_mode='valid'))  
    model.add(Activation('tanh'))  
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
      
    #第三个卷积层，16个卷积核，每个卷积核大小3*3  
    #激活函数用tanh  
    #采用maxpooling，poolsize为(2,2)  
    model.add(Convolution2D(16,  5, 5, border_mode='valid'))  
    model.add(Activation('tanh'))  
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    

    #第4个卷积层，16个卷积核，每个卷积核大小3*3  
    #激活函数用tanh  
    #采用maxpooling，poolsize为(2,2)  
    model.add(Convolution2D(16,  3, 3, border_mode='valid'))  
    model.add(Activation('tanh'))  
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
	
    #第5个卷积层，16个卷积核，每个卷积核大小3*3  
    #激活函数用tanh  
    #采用maxpooling，poolsize为(2,2)  
    model.add(Convolution2D(16,  3, 3, border_mode='valid'))  
    model.add(Activation('tanh'))  
    model.add(Dropout(0.25))
    
    
    #全连接层，先将前一层输出的二维特征图flatten为一维的。  
    #Dense就是隐藏层。16就是上一层输出的特征图个数。4是根据每个卷积层计算出来的：(28-5+1)得到24,(24-3+1)/2得到11，(11-3+1)/2得到4  
    #全连接有128个神经元节点,初始化方式为normal  
    model.add(Flatten())  
    model.add(Dense(128, init='normal'))  
    model.add(Activation('tanh'))  
    #model.add(Dropout(0.25))  
      
    #Softmax分类，输出是10类别  
    model.add(Dense(3, init='normal'))  
    model.add(Activation('softmax'))  
      
      
    #############  
    #开始训练模型  
    ##############  
    #使用SGD + momentum  
    #model.compile里的参数loss就是损失函数(目标函数)  
    sgd = SGD(lr=0.05, decay=1e-6, momentum=0.9, nesterov=True)  
    model.compile(loss='categorical_crossentropy', optimizer=sgd,class_mode="categorical",metrics=['accuracy']) 
    
    #开始训练， show_accuracy在每次迭代后显示正确率 。  batch_size是每次带入训练的样本数目 ， nb_epoch 是迭代次数，  shuffle 是打乱样本随机。  
   # model.fit(data, label, batch_size=100, nb_epoch=10,shuffle=True,verbose=1,show_accuracy=True,validation_split=0.2)  
  
    model.fit(traindata, trainlabel, batch_size=50,nb_epoch=10,shuffle=True,verbose=1,show_accuracy=True,validation_split=0.2)
    time.sleep(0.1)     
    #设置测试评估参数，用测试集样本
    WEIGHTS_FNAME = 'Len_weights.hdf'
    model.save_weights(WEIGHTS_FNAME)  
    
    Model_Name = 'Len_model.h5'
    model.save(Model_Name) 
    
    json_string = model.to_json()  #等价于 json_string = model.get_config()  
    open('Len_architecture.json','w').write(json_string)
    
    #设置测试评估参数，用测试集样本
#    score = model.evaluate(testdata, testlabel, batch_size=50,verbose=2,show_accuracy=True)
#    print('Test score:', score[0])
#    print('Test accuracy:', score[1])
#    print(model.predict(testdata[1:3]))
#    print(testlabel[1:3])


if __name__ == '__main__':    
    trainpath = r'./TrainImgs/'
    testpath = r'./ValidImgs/'
    testcount=__getnum__(testpath)
    traincount=__getnum__(trainpath)
    testdata,testlabel= __data_label__(testpath, testcount)
    print testdata.shape, testlabel
    #print testlabel
    traindata,trainlabel= __data_label__(trainpath, traincount)
    print traindata.shape, trainlabel
    #label为0~3共4个类别，keras要求格式为binary class matrices,转化一下，直接调用keras提供的这个函数
    testlabel = np_utils.to_categorical(testlabel, 3)
    trainlabel = np_utils.to_categorical(trainlabel, 3)
    
    __CNN__(testdata, testlabel, traindata, trainlabel)
    
    print "Done"