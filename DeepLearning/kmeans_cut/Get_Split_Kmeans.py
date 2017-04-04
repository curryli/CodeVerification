# -*- coding: utf-8 -*-
from PIL import Image,ImageEnhance,ImageFilter
import numpy as np
from scipy.misc import imread
import random, string
import os
import os.path
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def get_pic_array(filename):  #图片处理（灰度化，二值化，切割图片）
    filepath = filename
    im = Image.open(filepath)
    #imgSize = im.size #
    #print imgSize   #(130, 50)
    imgry = im.convert('L')  #灰度化
     
       
    #imgry.show()
    #二值化
    threshold = 120
    table = []
    
    for i in range(256):
        if i <threshold:
            table.append(0)
        else:
            table.append(1)
    biPic = imgry.point(table,'1')
    #biPic.show()
      
     
    bi_w = biPic.width    
    bi_h = biPic.height
      
    data = biPic.getdata()
    data = np.matrix(data,dtype='int32')
    #new_data = np.reshape(data,(width,height))
    imarray = np.reshape(data,(bi_h,bi_w))
     
    reversedarray = 1-imarray
    #matrix_slice = reversedarray[:,0:2*bi_w/6]
    matrix_slice = reversedarray[:,0:200]
    
    np.savetxt("matrix_slice.txt", matrix_slice, fmt="%d")
    tmp_array = 255*(1 - matrix_slice)

    tmp_image = Image.fromarray(np.uint8(tmp_array))
    tmp_image.save("reversedPic.jpg")
     
    return np.array(matrix_slice)
  
 

def get_split_list(filename): 
    pic_array = get_pic_array(filename)
    print pic_array.shape
    print type(pic_array)

#    sample_array =  pic_array[pic_array>0]
#    print type(sample_array)
    #sample_array = np.where(pic_array>0)
    oneList = []
    
    for i in range(pic_array.shape[0]):
        for j in range(pic_array.shape[1]):
            if pic_array[i][j]==1:
                oneList.append([i,j])
 
    Xarray = np.array(oneList)            

    y_pred = KMeans(n_clusters=5, init='k-means++', precompute_distances=True).fit_predict(Xarray)
    X = Xarray[:, 1]
    Y = 50-Xarray[:, 0]
    plt.scatter(X, Y, c=y_pred)
    #print y_pred    
    plt.xlim(0, 200)
    plt.ylim(0, 50)
    plt.show()
    #plt.savefig('plt.png')
    
    y_pred = np.reshape(y_pred,(y_pred.shape[0],1))
    X = np.reshape(X,(X.shape[0],1))

    print y_pred.shape
    X_cluster = np.hstack((X, y_pred))
    #print X_cluster
    #np.savetxt("X_cluster.txt", X_cluster, fmt="%d")
    
    d={}                
    for x, y in X_cluster:
        d.setdefault(x, set())
        d[x].add(y)

    #print d  
    
    tmp_list = []
    dklist = d.keys()
    for i in range(1,len(dklist)):
        #print d[dklist[i]]
        if (len(d[dklist[i]])>1 or d[dklist[i]]!=d[dklist[i-1]]):
            tmp_list.append(dklist[i])
            
    #print tmp_list
    cut_list = [tmp_list[0]]
    for i in range(1,len(tmp_list)):
        if (tmp_list[i]-tmp_list[i-1])>5:
            cut_list.append(tmp_list[i])
    
    return cut_list
            

if __name__ == '__main__':
    print get_split_list("imgs/bb2.png") 
    print "Done"
       
 