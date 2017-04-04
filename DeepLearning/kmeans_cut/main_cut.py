# -*- coding: utf-8 -*-
from PIL import Image,ImageEnhance,ImageFilter
import numpy as np
from scipy.misc import imread

import os
import os.path
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
    
def get_pic_array(reversedarray):  #图片处理（灰度化，二值化，切割图片）
    matrix_slice = reversedarray[:,0:200]
    return np.array(matrix_slice)
   
def get_split_list(reversedarray): 
    pic_array = get_pic_array(reversedarray)
    oneList = []
    
    for i in range(pic_array.shape[0]):
        for j in range(pic_array.shape[1]):
            if pic_array[i][j]==1:
                oneList.append([i,j])
 
    Xarray = np.array(oneList)            

    y_pred = KMeans(n_clusters=5, init='k-means++', precompute_distances=True).fit_predict(Xarray)
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
            if (end-start)<2:
                continue
            tmp_range = range(start, end)
            tmp_list.append(tmp_range)
            start = dklist[i]

    tmp_range = range(start, dklist[-1])
    tmp_list.append(tmp_range)

    return tmp_list
 
def cut_pic(filename):  # 图片处理（灰度化，二值化，切割图片）
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

    roi_cols_list = get_split_list(reversedarray)
   
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
      
if __name__ == '__main__':
    child_img_list = cut_pic('imgs/test5.png')
  
    for i in range(0,len(child_img_list)):
        child_img_list[i].save("b%d.jpg" % i)
    print "Done"