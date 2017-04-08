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
from keras.models import model_from_json
from keras import backend
from PIL import Image,ImageEnhance,ImageFilter
from scipy.misc import imread
import os.path
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

def imageprepare(fname):
    """
    This function returns the pixel values.
    The imput is a png file location.
    """
    im = Image.open(fname).convert('L')
    print "fname is " + fname
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (28, 28), (255)) #creates white canvas of 28x28 pixels
    
    if width > height: #check which dimension is bigger
        #Width is bigger. Width becomes 20 pixels.
        nheight = int(round((20.0/width*height),0)) #resize height according to ratio width
        if (nheight == 0): #rare case but minimum is 1 pixel
            nheight = 1  
        # resize and sharpen
        img = im.resize((20,nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight)/2),0)) #caculate horizontal pozition
        newImage.paste(img, (4, wtop)) #paste resized image on white canvas
    else:
        #Height is bigger. Heigth becomes 20 pixels. 
        nwidth = int(round((20.0/height*width),0)) #resize width according to ratio height
        if (nwidth == 0): #rare case but minimum is 1 pixel
            nwidth = 1
         # resize and sharpen
        img = im.resize((nwidth,20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth)/2),0)) #caculate vertical pozition
        newImage.paste(img, (wleft, 4)) #paste resized image on white canvas

    newImage.save(fname)


def get_pic_array(reversedarray):  #图片处理（灰度化，二值化，切割图片）
    matrix_slice = reversedarray[:,0:200]
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
  
    y_pred = np.reshape(y_pred,(y_pred.shape[0],1))
    X = np.reshape(X,(X.shape[0],1))
 
    X_cluster = np.hstack((X, y_pred))
    
    d={}                
    for x, y in X_cluster:
        d.setdefault(x, set())
        d[x].add(y)

    dklist = d.keys()
    tmp_list = []
    start = dklist[0]
    for i in range(2,len(dklist)):
        #print dklist[i], d[dklist[i]]
        if ( d[dklist[i]]!=d[dklist[i-1]]):  
            end = dklist[i-1]
            if (end-start)<5:       #######################################################
                continue
            tmp_range = range(start, end)
            tmp_list.append(tmp_range)
            start = dklist[i]

    tmp_range = range(start, dklist[-1])
    tmp_list.append(tmp_range)
    
    print len(tmp_list)

    return tmp_list
 
def cut_pic(filename, split_N):  # 图片处理（灰度化，二值化，切割图片）
    filepath = filename
    im = Image.open(filepath)
    imgry = im.convert('L')  # 灰度化

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

    data = biPic.getdata()
    data = np.matrix(data, dtype='int32')

    imarray = np.reshape(data, (bi_h, bi_w))

    reversedarray = 1 - imarray

    colSumList = np.asarray(reversedarray.sum(axis=0))[0]  # 每一列的元素和
    index_filter = [i for i in range(len(colSumList)) if colSumList[i] < 5]

    for col in index_filter:
        reversedarray[:, col:col + 1] = 0  # 作为分隔的空白列

    roi_cols_list = get_split_list(reversedarray, split_N)
   
    roi_height = 42
    roi_weight = 26
    
    child_img_list = []
    roi_rows_list = []
    badFlag = False
    for k in range(len(roi_cols_list)):
        if roi_cols_list[k]:
            start_col = roi_cols_list[k][0]
            start_dict = {}
            for j in range(50 - roi_height):
                maxsum = reversedarray[j:j + roi_height, start_col:].sum()
                start_dict[maxsum] = j
            start_row = start_dict[max(start_dict.keys())]

            roi_rows_list.append(range(start_row, start_row + roi_height))
        else:
            badFlag = True

    if not badFlag:
        for i in range(len(roi_cols_list)):
            if roi_cols_list[i]:
                start_row = roi_rows_list[i][0]
                end_row = start_row + roi_height
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
    img = cv2.imread(filename,0)
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
    adaptive = cv2.adaptiveThreshold(origin_img, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)   # 自适应二值化
    
    adaptive = cv2.medianBlur(adaptive,1) 
    
    origin_arr = np.asarray(adaptive,dtype="float32")
    origin_data = np.empty((1,1,50,200),dtype="float32")
    origin_data[0,:,:,:] = origin_arr
    origin_data /= np.max(origin_data)
    origin_data -= np.mean(origin_data) 
    return origin_data

if __name__ == '__main__':
    testPic = '39.jpg'
        
    print "done1"
    
    len_model = model_from_json(open('Len_architecture_2.json').read())
    sgd = SGD(lr=0.05, decay=1e-6, momentum=0.9, nesterov=True)  
    len_model.compile(loss='categorical_crossentropy', optimizer=sgd,class_mode="categorical",metrics=['accuracy']) 
    
    #加载参数
    LEN_WEIGHTS = 'Len_weights_2.hdf'
    len_model.load_weights(LEN_WEIGHTS)    
     
    print "done2"
    
    LenDict={0:4, 1:5, 2:6}
    
    #print(model.predict(testdata))
    
    Len_Img = LenDict[len_model.predict_classes(Img_to_Array(testPic))[0]]
    
    child_img_list = cut_pic(testPic, Len_Img)
  
    print "Len_Img: ", len(child_img_list) 
    
    for i in range(0,len(child_img_list)):
        child_img_list[i].save("sp%d.jpg" % i)
    print "Save Done"
    
    
    reversedDict={0:"0", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 
             10:"a", 11:"b", 12:"c", 13:"d", 14:"e", 15:"f", 16:"g", 17:"h", 18:"i", 19:"j", 20:"k", 21:"l", 22:"m", 23:"n", 24:"o", 25:"p", 26:"q", 27:"r", 28:"s", 29:"t", 30:"u", 31:"v", 32:"w", 33:"x", 34:"y", 35:"z",
             36:"A", 37:"B", 38:"C", 39:"D", 40:"E", 41:"F", 42:"G", 43:"H", 44:"I", 45:"J", 46:"K", 47:"L", 48:"M", 49:"N", 50:"O", 51:"P", 52:"Q", 53:"R", 54:"S", 55:"T", 56:"U", 57:"V", 58:"W", 59:"X", 60:"Y", 61:"Z"}
    
   
        
    result = ""
    for i in range(0,len(child_img_list)):
        fname = ("sp%d.jpg" % i)
        imageprepare(fname)
        result = result + reversedDict[cnn_single(fname)[0]]
    
    print result
    print "done4"
    
    