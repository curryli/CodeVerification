# coding=utf-8
from __future__ import division
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
from keras.models import model_from_json
from keras import backend
from PIL import Image,ImageEnhance,ImageFilter
from scipy.misc import imread
import os.path
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


Pic_Weigth = 200
Pic_Height = 50



def get_pic_array(reversedarray):  #图片处理（灰度化，二值化，切割图片）
    matrix_slice = reversedarray[:,0:Pic_Weigth]
    return np.array(matrix_slice)
   
def get_split_list(reversedarray, split_N): 
    pic_array = get_pic_array(reversedarray)
    oneList = []
    
    for i in range(pic_array.shape[0]):
        for j in range(pic_array.shape[1]):
            if pic_array[i][j]==1:
                oneList.append([i,j])
 
    Xarray = np.array(oneList)            

    y_pred = KMeans(n_clusters= split_N, init='k-means++', precompute_distances=True).fit_predict(Xarray)
    X = Xarray[:, 1]
     
    Y = Pic_Height-Xarray[:, 0]
    plt.scatter(X, Y, c=y_pred)
    #print y_pred    
    plt.xlim(0, Pic_Weigth)
    plt.ylim(0, Pic_Height)
    plt.show()
    #plt.savefig('plt.png')
    
    
  
    y_pred = np.reshape(y_pred,(y_pred.shape[0],1))
    X = np.reshape(X,(X.shape[0],1))

    X_cluster = np.hstack((X, y_pred))
 

    d={}                
    for x, y in X_cluster:
        d.setdefault(x, set())
        d[x].add(y)
 
    dklist0 = d.keys()
    dklist = sorted(dklist0)
    #print dklist
    
    tmp_list = []
    start = dklist[0]
    #print "len", len(dklist)
    for i in range(2,len(dklist)):
        #print dklist[i], d[dklist[i]]
        if ( d[dklist[i]]!=d[dklist[i-1]]):  
            end = dklist[i-1]
            if (end-start)<1:
                continue
            tmp_range = range(start, end+1)
            tmp_list.append(tmp_range)
            start = dklist[i]

    tmp_range = range(start, dklist[-1]+1)
    #print tmp_range 
    tmp_list.append(tmp_range)

    return tmp_list
 
def cut_pic(filename, split_N):  # 图片处理（灰度化，二值化，切割图片）
    filepath = filename
    im = Image.open(filepath)
    imgry = im.convert('L')  # 灰度化
    
    ###################################
    imgry = imgry.filter(ImageFilter.MedianFilter())
    imgry = imgry.filter(ImageFilter.MedianFilter())
    #################################
    
    # 二值化
    threshold = 120
    table = []

    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    biPic = imgry.point(table, '1')

    bi_w = biPic.width
    bi_h = biPic.height
    print "width is ", bi_w, "height is ", bi_h

    data = biPic.getdata()
    data = np.matrix(data, dtype='int32')

    imarray = np.reshape(data, (bi_h, bi_w))

    reversedarray = 1 - imarray

#    colSumList = np.asarray(reversedarray.sum(axis=0))[0]  # 每一列的元素和
#    index_filter = [i for i in range(len(colSumList)) if colSumList[i] < 2]
#
#    for col in index_filter:
#        reversedarray[:, col:col + 1] = 0  # 作为分隔的空白列

    roi_cols_list = get_split_list(reversedarray, split_N)
    print roi_cols_list
   
    roi_rows_list = range(3,Pic_Height-3)
    
    child_img_list = []
    
    roi_weight = Pic_Weigth/4
    for i in range(len(roi_cols_list)):
            if roi_cols_list[i]:
                start_row = roi_rows_list[0]
                end_row = roi_rows_list[-1]
                col_margin = (roi_weight - len(roi_cols_list[i])) / 2
                start_col = roi_cols_list[i][0] - col_margin
                end_col = start_col + roi_weight
                tmp_array = 255 * (1 - reversedarray[start_row:end_row, start_col:end_col])
                tmp_image = Image.fromarray(np.uint8(tmp_array))
                child_img_list.append(tmp_image)
            else:
                child_img_list = []

    return child_img_list


def cnn_single(filename):
    img_tmp = cv2.imread(filename,0)
     
    w_tmp = img_tmp.shape[1]
    h_tmp = img_tmp.shape[0]
    
    #img = cv2.resize(img_tmp, (28,28),interpolation=cv2.INTER_CUBIC)
        
    # 放缩图像
    cal_fx = 28/w_tmp
    cal_fy = 28/h_tmp
    img = cv2.resize(img_tmp, (0,0), fx=cal_fx, fy=cal_fy, interpolation=cv2.INTER_CUBIC)
 
    arr = np.asarray(img,dtype="float32")
    testdata = np.empty((1,1,28,28),dtype="float32")
    
    testdata[0,:,:,:] = arr
    testdata /= np.max(testdata)
    testdata -= np.mean(testdata)   
    

    
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
    single_result = model.predict_classes(testdata)
    return single_result
    
def Img_to_Array(filename):
    origin_img = cv2.imread(filename,0)
    origin_arr = np.asarray(origin_img,dtype="float32")
    origin_data = np.empty((1,1,Pic_Height,Pic_Weigth),dtype="float32")
    origin_data[0,:,:,:] = origin_arr
    origin_data /= np.max(origin_data)
    origin_data -= np.mean(origin_data) 
    return origin_data

if __name__ == '__main__':
    testPic = '43.jpg'
#        
#    print "done1"
#    
#    len_model = model_from_json(open('Len_architecture_2.json').read())
#    sgd = SGD(lr=0.05, decay=1e-6, momentum=0.9, nesterov=True)  
#    len_model.compile(loss='categorical_crossentropy', optimizer=sgd,class_mode="categorical",metrics=['accuracy']) 
#    
#    #加载参数
#    LEN_WEIGHTS = 'Len_weights_2.hdf'
#    len_model.load_weights(LEN_WEIGHTS)    
#     
#    print "done2"
#    
#    LenDict={0:4, 1:5, 2:6}
    
    #print(model.predict(testdata))
    
#    Len_Img = LenDict[len_model.predict_classes(Img_to_Array(testPic))[0]]
    Len_Img = 4
    print "Len_Img: ", Len_Img 
    
    
    child_img_list = cut_pic(testPic, Len_Img)
  
    
    for i in range(0,len(child_img_list)):
        child_img_list[i].save("sp%d.jpg" % i)
    print "Save Done"
    
    
    reversedDict={0:"0", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 
             10:"a", 11:"b", 12:"c", 13:"d", 14:"e", 15:"f", 16:"g", 17:"h", 18:"i", 19:"j", 20:"k", 21:"l", 22:"m", 23:"n", 24:"o", 25:"p", 26:"q", 27:"r", 28:"s", 29:"t", 30:"u", 31:"v", 32:"w", 33:"x", 34:"y", 35:"z",
             36:"A", 37:"B", 38:"C", 39:"D", 40:"E", 41:"F", 42:"G", 43:"H", 44:"I", 45:"J", 46:"K", 47:"L", 48:"M", 49:"N", 50:"O", 51:"P", 52:"Q", 53:"R", 54:"S", 55:"T", 56:"U", 57:"V", 58:"W", 59:"X", 60:"Y", 61:"Z"}
    
   
        
    result = ""
    for i in range(0,len(child_img_list)):
        fname = ("sp%d.jpg" % i)
        result = result + reversedDict[cnn_single(fname)[0]]
 
    print result
    print "done4"
    
    