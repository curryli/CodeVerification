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
  
 
if __name__ == '__main__':
    pic_array = get_pic_array("imgs/bb3.png")
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
    print Xarray
    
    y_pred = KMeans(n_clusters=5,init='k-means++' , precompute_distances=True).fit_predict(Xarray)
    plt.scatter(Xarray[:, 1], Xarray[:, 0], c=y_pred)
        
    #plt.show()
    plt.savefig('plt.png')